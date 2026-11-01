"""Tests for the lab canary and canary_scan.py (G9, week 2 task 5).

    pytest teams/09-evaluation/decontam/tests -q

No network. The Parquet test needs pyarrow (skipped without it).
"""

import json

import pytest

import canary_scan
from canary import LAB_CANARY, LAB_CANARY_ID, LAB_CANARY_LINE, MARKDOWN_LINE, find, load_canaries, stamp
from decontam_check import DEFAULT_SET
from fpset import Fingerprints
from test_decontam import CANARY as TOY_CANARY
from test_decontam import CLEAN, build_toy

# Named decorators: pr-guard reads a diff line that starts with a dotted decorator as an email address.
module_fixture = pytest.fixture(scope="module")
shipped = pytest.mark.skipif(not (DEFAULT_SET / "MANIFEST.json").exists(), reason="no shipped set")


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def run(capsys, *argv):
    """Run canary_scan.main; return (exit code, stdout records, stderr)."""
    code = canary_scan.main([str(a) for a in argv])
    out, err = capsys.readouterr()
    return code, [json.loads(line) for line in out.splitlines() if line.strip()], err


# ---- the canary string ----

def test_lab_canary_is_plain_ascii_text():
    # Plain text, not a special token (TSAI ruling), and ASCII so JSON escaping cannot change it.
    assert LAB_CANARY.isascii() and LAB_CANARY_LINE.isascii()
    assert LAB_CANARY in LAB_CANARY_LINE and LAB_CANARY_LINE in MARKDOWN_LINE
    assert "<|" not in LAB_CANARY and " " not in LAB_CANARY
    assert json.dumps(LAB_CANARY_LINE, ensure_ascii=True) == '"' + LAB_CANARY_LINE + '"'


def test_stamp_puts_the_canary_first_and_keeps_the_record():
    rec = {"id": "gsm8k/3", "question": "q", "canary": "old"}
    s = stamp(rec)
    assert list(s)[0] == "canary" and s["canary"] == LAB_CANARY_LINE
    assert {k: v for k, v in s.items() if k != "canary"} == {"id": "gsm8k/3", "question": "q"}
    assert rec["canary"] == "old"  # the input is not changed


def test_find_gives_every_occurrence_in_offset_order():
    text = "a " + LAB_CANARY + " b " + TOY_CANARY + " c " + LAB_CANARY
    hits = find(text, {LAB_CANARY: "lab", TOY_CANARY: "toy"})
    assert hits == [(2, LAB_CANARY), (text.index(TOY_CANARY), TOY_CANARY), (text.rindex(LAB_CANARY), LAB_CANARY)]
    assert all(text[o:o + len(c)] == c for o, c in hits)
    assert find(CLEAN[0], {LAB_CANARY: "lab"}) == []


def test_load_canaries_reads_benchmark_canary_files(tmp_path):
    (tmp_path / "toy").mkdir()
    (tmp_path / "toy" / "canaries.txt").write_text(TOY_CANARY + "\n\n", encoding="utf-8")
    assert load_canaries(tmp_path) == {LAB_CANARY: LAB_CANARY_ID, TOY_CANARY: "toy"}
    assert load_canaries(None) == {LAB_CANARY: LAB_CANARY_ID}


@shipped
def test_shipped_set_gives_the_gpqa_and_hle_canaries():
    sources = set(load_canaries(DEFAULT_SET).values())
    assert {LAB_CANARY_ID, "gpqa_diamond", "hle"} <= sources


# ---- canary_scan.py ----

def test_scan_prints_only_canary_doc_id_and_offset(tmp_path, capsys):
    secret = "SECRET BENCHMARK QUESTION TEXT"
    docs = write_jsonl(tmp_path / "docs.jsonl", [
        {"doc_id": "d0", "text": CLEAN[0]},
        {"doc_id": "d1", "text": secret + "\n" + LAB_CANARY_LINE + "\n" + secret},
    ])
    code, recs, err = run(capsys, docs, "--fingerprints", tmp_path / "none")
    assert code == 1
    assert recs == [{"canary": LAB_CANARY, "doc_id": "d1",
                     "offset": len(secret + "\n" + LAB_CANARY_LINE) - len(LAB_CANARY)}]
    assert all(set(r) == {"canary", "doc_id", "offset"} for r in recs)
    out_and_err = json.dumps(recs) + err
    assert secret not in out_and_err and "MUST NEVER" not in out_and_err  # no document text
    assert "docs 2 with_canary 1 hits 1" in err


def test_scan_reports_every_hit_in_a_document(tmp_path, capsys):
    text = LAB_CANARY + " middle " + LAB_CANARY + " end " + TOY_CANARY
    docs = write_jsonl(tmp_path / "docs.jsonl", [{"id": 7, "body": text}])
    (tmp_path / "set" / "toy").mkdir(parents=True)
    (tmp_path / "set" / "toy" / "canaries.txt").write_text(TOY_CANARY + "\n", encoding="utf-8")
    code, recs, err = run(capsys, docs, "--id-field", "id", "--text-field", "body", "--fingerprints", tmp_path / "set")
    assert code == 1
    assert [(r["doc_id"], r["offset"], r["canary"]) for r in recs] == [
        ("7", 0, LAB_CANARY), ("7", text.index(" end") - len(LAB_CANARY), LAB_CANARY),
        ("7", text.index(TOY_CANARY), TOY_CANARY)]
    assert "hits 3" in err


def test_clean_documents_give_no_output_and_exit_0(tmp_path, capsys):
    docs = write_jsonl(tmp_path / "docs.jsonl", [{"doc_id": f"c{i}", "text": t} for i, t in enumerate(CLEAN)])
    code, recs, err = run(capsys, docs, "--fingerprints", tmp_path / "none")
    assert code == 0 and recs == []
    assert f"docs {len(CLEAN)} with_canary 0 hits 0" in err


def test_extra_canary_string(tmp_path, capsys):
    docs = write_jsonl(tmp_path / "docs.jsonl", [{"doc_id": "x", "text": "abc MY-MARKER def"}])
    code, recs, _ = run(capsys, docs, "--fingerprints", tmp_path / "none", "--canary", "MY-MARKER")
    assert code == 1 and recs == [{"canary": "MY-MARKER", "doc_id": "x", "offset": 4}]


def test_parquet_input(tmp_path, capsys):
    pa = pytest.importorskip("pyarrow")
    import pyarrow.parquet as pq
    pq.write_table(pa.table({"doc_id": ["p0", "p1"], "text": [CLEAN[1], "x" + LAB_CANARY]}), tmp_path / "s.parquet")
    code, recs, _ = run(capsys, tmp_path / "s.parquet", "--fingerprints", tmp_path / "none")
    assert code == 1 and recs == [{"canary": LAB_CANARY, "doc_id": "p1", "offset": 1}]


def test_folder_input_finds_a_stamped_eval_item_file(tmp_path, capsys):
    # An item file as make_eval_mini_items.py writes it: pure ASCII JSON with the canary in the file and in each item.
    items = {"items": [stamp({"id": "milu_Hindi/4", "question": "भारत की राजधानी क्या है?", "answer": "A"})]}
    eval_dir = tmp_path / "eval"
    (eval_dir / "runs").mkdir(parents=True)
    (eval_dir / "runs" / "items.json").write_text(json.dumps(stamp(items), ensure_ascii=True, indent=1), encoding="ascii")
    (eval_dir / "notes.md").write_text("# notes\n" + MARKDOWN_LINE + "\n", encoding="utf-8")
    (eval_dir / "clean.txt").write_text(CLEAN[0], encoding="utf-8")
    (eval_dir / "weights.bin").write_bytes(LAB_CANARY.encode())  # not a text suffix: not read
    code, recs, err = run(capsys, eval_dir, "--fingerprints", tmp_path / "none")
    assert code == 1
    assert sorted((r["doc_id"], r["canary"]) for r in recs) == [
        ("items.json", LAB_CANARY), ("items.json", LAB_CANARY), ("notes.md", LAB_CANARY)]
    assert "docs 3 " in err


# ---- the full check (decontam_check.py) also flags the lab canary ----

@module_fixture
def toy_fp(tmp_path_factory):
    out, _ = build_toy(tmp_path_factory.mktemp("toy_canary"))
    return Fingerprints(out)


def test_fingerprints_flag_the_lab_canary(toy_fp):
    text = CLEAN[0] + "\n" + LAB_CANARY_LINE
    flagged, hits = toy_fp.check(text)
    assert flagged
    assert hits[0] == {"item": f"{LAB_CANARY_ID}:canary", "canary": LAB_CANARY, "offset": text.index(LAB_CANARY)}
    assert not toy_fp.check(CLEAN[0])[0]
