"""Tests for check_shards.py (G9).

    pytest teams/09-evaluation/decontam/tests/test_check_shards.py -q

They test the parts that do not need a real shard: the links file, the reference table, the comparison, resume and
the exit code. check_one (which calls decode_shard.py, decontam_check.py and canary_scan.py) is replaced by a stub,
so no tokenizer, shard or fingerprint set is needed. The three scripts have their own tests.
"""

import json

import pytest

import check_shards as cs

SHA_A = "a" * 64
SHA_B = "b" * 64


def result(shard_id, sha=SHA_A, docs=10, tokens=100, flagged=0, canary_hits=0):
    return {"shard_id": shard_id, "payload_sha256": sha, "docs": docs, "tokens": tokens, "dataset_version": "v0",
            "split": "train", "tokenizer_sha256": "t" * 64, "fingerprints_version": "v2", "set_sha256": "s" * 64,
            "scope": "full set", "flagged": flagged, "flagged_doc_ids": [], "canaries_checked": 4,
            "canary_hits": canary_hits, "canary_hit_list": [], "seconds": 0.1}


def test_read_links_skips_comments_and_header(tmp_path):
    p = tmp_path / "links.tsv"
    p.write_text("# comment line\nfile\turl\nx-train-000000.bin\thttps://h/x.bin?sig=1\n"
                 "x-train-000000.json\thttps://h/x.json\n\ny-train-000001.bin\thttps://h/y.bin\n")
    links = cs.read_links(p)
    assert links["x-train-000000.bin"] == "https://h/x.bin?sig=1"
    assert "file" not in links
    assert cs.shard_ids_from_links(links) == ["x-train-000000", "y-train-000001"]


def test_read_reference_reads_markdown_rows(tmp_path):
    p = tmp_path / "ref.md"
    p.write_text("| # | shard_id | payload_sha256 | docs | tokens | flagged | canary hits |\n"
                 "|---:|---|---|---:|---:|---:|---:|\n"
                 f"| 1 | `code-go-train-000000` | `{SHA_A}` | 56,588 | 56,698,571 | 0 | 0 |\n"
                 f"| 2 | ind-hi-x-train-000000 | {SHA_B} | 14,483 | 9,254,413 | 0 | 0 |\n"
                 "| not | a | row |\n")
    ref = cs.read_reference(p)
    assert ref == {"code-go-train-000000": (SHA_A, 56588, 56698571),
                   "ind-hi-x-train-000000": (SHA_B, 14483, 9254413)}


def test_compare_lists_each_mismatch():
    ref = {"s-train-000000": (SHA_A, 10, 100)}
    assert cs.compare(result("s-train-000000"), ref) == []
    issues = cs.compare(result("s-train-000000", sha=SHA_B, docs=11), ref)
    assert len(issues) == 2 and issues[0].startswith("payload_sha256") and issues[1].startswith("docs")
    assert cs.compare(result("other-train-000000"), ref) == ["no row in the --compare file"]


def test_table_marks_mismatch():
    ref = {"s-train-000000": (SHA_A, 10, 100)}
    text = cs.table([result("s-train-000000"), result("s-train-000000", tokens=99)], ref)
    lines = text.splitlines()
    assert lines[2].endswith("| yes |")
    assert "NO: tokens 99 != 100" in lines[3]


def make_work(tmp_path, ids):
    shards = tmp_path / "in"
    shards.mkdir()
    for i in ids:
        for ext in cs.SHARD_EXTS:
            (shards / f"{i}{ext}").write_bytes(b"x")
    tok = tmp_path / "tokenizer.json"
    tok.write_text("{}")
    return shards, tok


def test_resume_skips_done_shard_and_force_reruns(tmp_path, monkeypatch, capsys):
    ids = ["a-train-000000", "b-train-000000"]
    shards, tok = make_work(tmp_path, ids)
    calls = []

    def fake(shard_id, a, tok_sha):
        calls.append(shard_id)
        r = result(shard_id)
        r["tokenizer_sha256"] = tok_sha
        return r

    monkeypatch.setattr(cs, "check_one", fake)
    args = ["--tokenizer", str(tok), "--work", str(tmp_path / "w"), "--shards", str(shards), "--jobs", "2"]
    assert cs.main(args) == 0
    assert sorted(calls) == ids
    assert json.loads((tmp_path / "w" / "results" / "a-train-000000.json").read_text())["docs"] == 10
    calls.clear()
    assert cs.main(args) == 0
    assert calls == []
    assert cs.main(args + ["--force", "--only", "b-train-000000"]) == 0
    assert calls == ["b-train-000000"]


def test_exit_code_1_on_hit_failure_or_mismatch(tmp_path, monkeypatch):
    shards, tok = make_work(tmp_path, ["a-train-000000"])
    base = ["--tokenizer", str(tok), "--shards", str(shards), "--force"]

    monkeypatch.setattr(cs, "check_one", lambda s, a, t: result(s, flagged=1))
    assert cs.main(base + ["--work", str(tmp_path / "w1")]) == 1

    monkeypatch.setattr(cs, "check_one", lambda s, a, t: result(s, canary_hits=1))
    assert cs.main(base + ["--work", str(tmp_path / "w2")]) == 1

    def fail(s, a, t):
        raise cs.CheckError("decode_shard.py failed")

    monkeypatch.setattr(cs, "check_one", fail)
    assert cs.main(base + ["--work", str(tmp_path / "w3")]) == 1
    assert not (tmp_path / "w3" / "results" / "a-train-000000.json").exists()

    ref = tmp_path / "ref.md"
    ref.write_text(f"| 1 | `a-train-000000` | `{SHA_B}` | 10 | 100 | 0 | 0 |\n")
    monkeypatch.setattr(cs, "check_one", lambda s, a, t: result(s))
    assert cs.main(base + ["--work", str(tmp_path / "w4"), "--compare", str(ref)]) == 1
    ref.write_text(f"| 1 | `a-train-000000` | `{SHA_A}` | 10 | 100 | 0 | 0 |\n")
    assert cs.main(base + ["--work", str(tmp_path / "w5"), "--compare", str(ref)]) == 0


def test_unknown_only_id_is_usage_error(tmp_path):
    shards, tok = make_work(tmp_path, ["a-train-000000"])
    with pytest.raises(SystemExit) as e:
        cs.main(["--tokenizer", str(tok), "--work", str(tmp_path / "w"), "--shards", str(shards),
                 "--only", "missing-train-000000"])
    assert e.value.code == 2
