"""Tests for dedup.py on small made-up overlap runs (no real data). Run: python -m pytest -q teams/01-data-a/dedup/tests"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import pytest

pa = pytest.importorskip("pyarrow")
import pyarrow.parquet as pq  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dedup  # noqa: E402

ORDER = ["code-java", "code-js-ts", "en-a", "en-b", "ind-x-fw2", "ind-x-sangraha-v"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def make_run(root, docs, matches, status="complete"):
    """docs: [(doc_id, pack, split, words)], row = position. matches: [(row_a, row_b, rule, word, code)]."""
    res = root / "res"
    res.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({
        "row": list(range(len(docs))), "id": [f"{p}-{d}" for d, p, _, _ in docs], "doc_id": [d for d, *_ in docs],
        "pack": [p for _, p, _, _ in docs], "split": [s for _, _, s, _ in docs],
        "part": [f"{p}/part-00000.parquet" for _, p, _, _ in docs],
        "row_in_part": [sum(1 for x in docs[:i] if x[1] == docs[i][1] and x[2] == docs[i][2]) for i in range(len(docs))],
        "words": [w for *_, w in docs], "shingles": [max(w - 4, 1) for *_, w in docs]}), res / "overlap_docs.parquet")
    with (res / "overlap_matches.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_a", "row_b", "rule", "stage", "pack_a", "pack_b", "word_jaccard", "code_jaccard"])
        for a, b, rule, wj, cj in matches:
            stage = "within_pack" if docs[a][1] == docs[b][1] else "cross_pack"
            w.writerow([a, b, rule, stage, docs[a][1], docs[b][1], wj, cj])
    summary = {"status": status, "documents_all": len(docs),
               "outputs": {n: {"sha256": sha(res / n)} for n in ("overlap_docs.parquet", "overlap_matches.csv")}}
    (res / "overlap_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    return res


def config(root, **over):
    cfg = {"results": "res", "inputs": "", "out": "out/dedup", "cross_pack": True, "pack_order": ORDER,
           "licence_usable": {}, "default_licence_usable": True, "gold_dirs": []}
    cfg.update(over)
    p = root / "dedup.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")
    return p


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(dedup, "REPO", tmp_path)
    return tmp_path


def run(repo, **over):
    s = dedup.run(dedup.load_config(config(repo, **over)))
    log = [json.loads(l) for l in (repo / "out/dedup/dedup_log.jsonl").read_text(encoding="utf-8").splitlines()]
    return s, {e["removed_id"]: e for e in log}


def test_longest_copy_survives_and_two_are_removed(repo):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 120), ("c", "en-a", "train", 90)],
             [(0, 1, "H2", 0.9, ""), (1, 2, "H2", 0.85, "")])
    s, log = run(repo)
    assert set(log) == {"a", "c"} and s["removed"] == 2
    assert log["a"]["kept_id"] == "b" and log["a"]["priority_rule"] == 3 and log["a"]["stage"] == "within_pack"
    assert s["by_pack"]["en-a"] == {"documents_in": 3, "removed": 2, "removed_H1": 0, "removed_H2": 2,
                                    "removed_cross_pack": 0, "documents_out": 1}


def test_transitive_member_logs_its_strongest_match(repo):
    # a~b, b~c, no a~c: b (longest) survives; a and c are both direct matches of b
    # c~d only: d reaches b through c, so it is logged with direct = false
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 120), ("c", "en-a", "train", 90),
                    ("d", "en-a", "train", 80)],
             [(0, 1, "H2", 0.9, ""), (1, 2, "H2", 0.85, ""), (2, 3, "H2", 0.95, "")])
    _, log = run(repo)
    assert log["c"]["direct"] is True and log["c"]["similarity"] == 0.85
    assert log["d"]["direct"] is False and log["d"]["similarity"] == 0.95


def test_heldout_always_survives_and_train_copy_goes(repo):
    make_run(repo, [("t", "en-a", "train", 500), ("h", "en-a", "heldout", 100)], [(0, 1, "H2", 0.9, "")])
    s, log = run(repo)
    assert set(log) == {"t"} and log["t"]["kept_id"] == "h" and log["t"]["priority_rule"] == 0
    assert s["heldout_removed"] == 0


def test_heldout_heldout_pairs_are_reported_not_removed(repo):
    make_run(repo, [("h1", "en-a", "heldout", 100), ("h2", "en-a", "heldout", 100)], [(0, 1, "H1", 1.0, "")])
    s, log = run(repo)
    assert log == {} and s["heldout_heldout_pairs_reported"] == 1
    rows = list(csv.DictReader((repo / "out/dedup/heldout_duplicates.csv").open(encoding="utf-8")))
    assert {rows[0]["doc_id_a"], rows[0]["doc_id_b"]} == {"h1", "h2"}


def test_unusable_licence_never_survives(repo):
    make_run(repo, [("x", "en-a", "train", 900), ("y", "en-b", "train", 100)], [(0, 1, "H2", 0.9, "")])
    _, log = run(repo, licence_usable={"en-a": False})
    assert set(log) == {"x"} and log["x"]["kept_id"] == "y" and log["x"]["priority_rule"] == 1


def test_no_usable_copy_removes_every_train_copy(repo):
    make_run(repo, [("x", "en-a", "train", 100), ("y", "en-a", "train", 100)], [(0, 1, "H1", 1.0, "")])
    s, log = run(repo, licence_usable={"en-a": False})
    assert set(log) == {"x", "y"} and log["x"]["kept_id"] is None and log["x"]["stage"] == "none"


def test_url_decides_when_inputs_are_given(repo):
    make_run(repo, [("long", "en-a", "train", 300), ("url", "en-a", "train", 100)], [(0, 1, "H2", 0.9, "")])
    part = repo / "clean/train/en-a"
    part.mkdir(parents=True)
    pq.write_table(pa.table({"doc_id": ["long", "url"], "url": ["", "https://example.org/p"]}),
                   part / "part-00000.parquet")
    s, log = run(repo, inputs="clean")
    assert set(log) == {"long"} and log["long"]["priority_rule"] == 2 and s["url_known"]
    s, log = run(repo)                                   # without inputs, rule 2 decides nothing: length wins
    assert set(log) == {"url"} and log["url"]["priority_rule"] == 3 and s["rule_2_note"]


def test_inputs_that_do_not_match_the_run_are_refused(repo):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90)], [(0, 1, "H2", 0.9, "")])
    part = repo / "clean/train/en-a"
    part.mkdir(parents=True)
    pq.write_table(pa.table({"doc_id": ["other", "b"], "url": ["", ""]}), part / "part-00000.parquet")
    with pytest.raises(dedup.Fatal, match="do not match"):
        run(repo, inputs="clean")


def test_pack_order_breaks_a_full_tie(repo):
    make_run(repo, [("j", "code-js-ts", "train", 100), ("v", "code-java", "train", 100)],
             [(0, 1, "H1", 1.0, "")])
    s, log = run(repo)
    assert set(log) == {"j"} and log["j"]["kept_pack_id"] == "code-java" and log["j"]["priority_rule"] == 4
    assert log["j"]["stage"] == "cross_pack" and s["by_pack"]["code-js-ts"]["removed_cross_pack"] == 1


def test_cross_pack_switch_off_keeps_cross_pack_copies(repo):
    make_run(repo, [("x", "ind-x-fw2", "train", 100), ("y", "ind-x-sangraha-v", "train", 100)],
             [(0, 1, "H2", 0.9, "")])
    s, log = run(repo, cross_pack=False)
    assert log == {} and s["cross_pack_matches_dropped"] == 1


def test_code_pairs_log_the_token_score(repo):
    make_run(repo, [("a", "code-java", "train", 100), ("b", "code-java", "train", 99)], [(0, 1, "H2", 0.4, 0.91)])
    _, log = run(repo)
    assert log["b"]["similarity"] == 0.91


def test_harm_check_pass_fail_and_not_testable(repo):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90), ("g", "en-b", "train", 50)],
             [(0, 1, "H2", 0.9, "")])
    gold = repo / "gold"
    gold.mkdir()
    (gold / "en-b_gold.csv").write_text("doc_id,reader_1,reader_2\ng,x,y\n", encoding="utf-8")
    s, _ = run(repo, gold_dirs=["gold"])
    assert s["harm_check"]["status"] == "pass" and s["harm_check"]["gold_ids_in_input"] == 1
    (gold / "en-a_gold.csv").write_text("doc_id,reader_1,reader_2\nb,x,y\n", encoding="utf-8")
    s, _ = run(repo, gold_dirs=["gold"])
    assert s["harm_check"]["status"] == "fail" and s["harm_check"]["gold_removed_ids"] == ["en-a:b"]
    for f in gold.iterdir():
        f.write_text("doc_id,reader_1,reader_2\nzz,x,y\n", encoding="utf-8")
    s, _ = run(repo, gold_dirs=["gold"])
    assert s["harm_check"]["status"] == "not_testable"


def test_same_doc_id_in_two_packs_is_matched_by_pack(repo):
    make_run(repo, [("same", "en-a", "train", 100), ("same", "en-b", "train", 90)], [(0, 1, "H1", 1.0, "")])
    gold = repo / "gold"
    gold.mkdir()
    (gold / "en-a_gold.csv").write_text("doc_id,reader_1,reader_2\nsame,x,y\n", encoding="utf-8")
    s, _ = run(repo, gold_dirs=["gold"])
    # en-b's copy is removed; en-a's gold copy is kept, so the harm check passes
    assert s["harm_check"]["status"] == "pass" and s["by_pack"]["en-b"]["removed"] == 1


def test_remove_list_matches_the_log(repo):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90)], [(0, 1, "H2", 0.9, "")])
    s, log = run(repo)
    rows = list(csv.DictReader((repo / "out/dedup/remove_list.csv").open(encoding="utf-8")))
    assert [(r["pack_id"], r["split"], r["doc_id"]) for r in rows] == [("en-a", "train", "b")]
    assert s["outputs"]["remove_list.csv"]["sha256"] == sha(repo / "out/dedup/remove_list.csv")


def test_checksum_mismatch_is_refused(repo):
    res = make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90)], [(0, 1, "H2", 0.9, "")])
    with (res / "overlap_matches.csv").open("a", encoding="utf-8") as f:
        f.write("0,1,H2,within_pack,en-a,en-a,0.99,\n")
    with pytest.raises(dedup.Fatal, match="SHA-256 mismatch"):
        run(repo)


def test_incomplete_run_is_refused(repo):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90)], [(0, 1, "H2", 0.9, "")],
             status="failed_output_limit")
    with pytest.raises(dedup.Fatal, match="did not complete"):
        run(repo)


@pytest.mark.parametrize("over, message", [
    ({"pack_order": ["en-a"]}, "no rank"),
    ({"out": "elsewhere"}, "inside out/"),
    ({"licence_usable": {"en-a": "yes"}}, "true or false"),
    ({"results": ""}, "results is required"),
])
def test_bad_configs_are_refused(repo, over, message):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-b", "train", 90)], [(0, 1, "H2", 0.9, "")])
    with pytest.raises(dedup.Fatal, match=message):
        run(repo, **over)


def test_main_returns_2_on_error_and_0_on_success(repo, capsys):
    make_run(repo, [("a", "en-a", "train", 100), ("b", "en-a", "train", 90)], [(0, 1, "H2", 0.9, "")])
    assert dedup.main(["--config", str(config(repo))]) == 0
    assert "removed 1" in capsys.readouterr().out
    assert dedup.main(["--config", str(config(repo, pack_order=["zz"]))]) == 2
