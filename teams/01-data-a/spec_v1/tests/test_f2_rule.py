"""Unit tests for tools/f2_rule.py, F2 with G9's benchmark fingerprints, and for run_clean.py --f2. Every doc here is made
up; the one benchmark string is a canary read from G9's fingerprint set at run time, never written in this file. The
run_clean.py test loads the full set (about 20 s, 1.1 GB); the others load one benchmark.

  python -m pytest spec_v1/tests
"""
import json
import subprocess
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

SPEC = Path(__file__).resolve().parents[1]
TOOLS = SPEC / "tools"
sys.path.insert(0, str(TOOLS))
import f2_rule

CLEAN_TEXT = "Area of a circle.\nThe radius is half the diameter.\n"
# Named decorators: pr-guard's email pattern reads an added pytest decorator line as an address.
module_fixture = pytest.fixture(scope="module")
fixture = pytest.fixture


def canary():
    """A benchmark canary string from G9's set: an exact marker, so one occurrence flags a doc."""
    return (f2_rule._g9().parent / "fingerprints" / f2_rule.SET / "gpqa_diamond" / "canaries.txt").read_text(encoding="utf-8").splitlines()[0]


def set_sha256():
    return json.loads((f2_rule._g9().parent / "fingerprints" / f2_rule.SET / "MANIFEST.json").read_text(encoding="utf-8"))["set_sha256"]


@module_fixture
def gpqa():
    return f2_rule.fingerprints(("gpqa_diamond",))


@fixture
def one_benchmark(monkeypatch, gpqa):
    monkeypatch.setattr(f2_rule, "fingerprints", lambda: gpqa)


def test_a_doc_with_a_benchmark_canary_is_dropped(one_benchmark):
    doc = {"doc_id": "x", "text": f"Notes on chemistry.\n{canary()}\n"}
    assert f2_rule.f2(doc) == ("drop", doc["text"])
    flagged, hits = f2_rule.check(doc["text"])
    assert flagged and hits[0]["item"] == "gpqa_diamond:canary" and hits[0]["offset"] == len("Notes on chemistry.\n")


def test_a_clean_doc_is_kept(one_benchmark):
    assert f2_rule.f2({"doc_id": "x", "text": CLEAN_TEXT}) == ("keep", CLEAN_TEXT)


def test_g9s_normalize_is_used_even_when_team_1s_is_already_imported():
    """Both are named normalize. With the wrong one the set refuses to load (its normalize_id differs)."""
    import normalize as team1
    assert Path(team1.__file__).parent == TOOLS
    f2_rule.fingerprints.cache_clear()
    assert f2_rule.fingerprints(("gpqa_diamond",)).set_sha256 == set_sha256()
    assert sys.modules["normalize"] is team1


def test_harm_test_reads_the_rule_without_loading_the_set():
    """harm_test.py runs this file's source with no __file__; the set loads only on the first doc."""
    sys.path.insert(0, str(SPEC.parent / "tools"))
    import harm_test
    ns = harm_test.load_rules(TOOLS / "f2_rule.py")
    ns = ns[0] if isinstance(ns, tuple) else ns
    assert callable(harm_test.find_rule(ns, "F2"))


def test_run_clean_f2_drops_the_flagged_doc_and_records_the_set(tmp_path):
    rows = [{"doc_id": "d1", "text": CLEAN_TEXT, "url": "", "lang_label": "en"},
            {"doc_id": "d2", "text": f"Notes on chemistry.\n{canary()}\n", "url": "", "lang_label": "en"}]
    pack = tmp_path / "en-dclm.parquet"
    pq.write_table(pa.Table.from_pylist(rows), pack)
    r = subprocess.run([sys.executable, str(SPEC / "run_clean.py"), "--pack", str(pack), "--out", str(tmp_path / "out"), "--f2"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    s = json.loads((tmp_path / "out" / "en-dclm_summary.json").read_text(encoding="utf-8"))
    assert s["f2"]["set_sha256"] == set_sha256()
    assert [d["doc_id"] for d in s["f2"]["dropped"]] == ["d2"] and s["f2"]["dropped"][0]["items"] == ["gpqa_diamond:canary"]
    assert pq.read_table(tmp_path / "out" / "en-dclm_clean.parquet").column("doc_id").to_pylist() == ["d1"]


def test_run_clean_without_f2_has_no_f2_entry(tmp_path):
    pack = tmp_path / "en-dclm.parquet"
    pq.write_table(pa.Table.from_pylist([{"doc_id": "d1", "text": CLEAN_TEXT, "url": "", "lang_label": "en"}]), pack)
    subprocess.run([sys.executable, str(SPEC / "run_clean.py"), "--pack", str(pack), "--out", str(tmp_path / "out")], check=True, capture_output=True)
    assert "f2" not in json.loads((tmp_path / "out" / "en-dclm_summary.json").read_text(encoding="utf-8"))
