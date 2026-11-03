"""Unit tests for overlap.py, the cross-pack all-to-all Jaccard job: its config checks, how it finds and checks the
pinned sample parts, and the scores it writes, checked by hand on a few pairs and against a brute-force Jaccard of every
pair. Every text here is made up; none comes from a pack. The job runs in-process with its repository root pointed at a
temporary folder, so nothing is read from or written to the real inputs/ or out/.

  python3 -B -m pytest dedup/tests/test_overlap.py
"""
import csv
import hashlib
import json
import random
import shutil
import sys
from itertools import combinations
from pathlib import Path

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("scipy")
from scipy import sparse  # noqa: E402
pa = pytest.importorskip("pyarrow")
import pyarrow.parquet as pq  # noqa: E402

DEDUP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DEDUP))
import overlap as ov  # noqa: E402
from h1_sha256 import h1_key  # noqa: E402
from jaccard_matrix import shingles  # noqa: E402

BASE = "the quick brown fox jumps over the lazy dog near a quiet river bank under the old stone bridge today"
EDITED = BASE.replace("today", "tonight")   # last word changed: 15 of the 17 distinct 5-grams shared
SHOUTED = "  THE QUICK  brown\tFox JUMPS over the lazy dog near a quiet\r\nriver bank under the old stone bridge TODAY "
SUPERSCRIPT = "Area is r² times pi"   # NFKC (the H1 layer on top of match_key) makes r2 of r squared
UNRELATED = "completely different words appear in this unrelated sentence about cooking pasta"
EDIT_SCORE = 15 / 17

# The hand-checked sample: split/pack/part -> [(doc_id, text)]. Matrix rows follow pack, split, part, row order.
SAMPLE = {
    "train/en-a/part-00000.parquet": [("a1", BASE), ("a2", EDITED), ("a3", "area is r2 times pi"), ("a4", ""),
                                      ("a5", UNRELATED)],
    "heldout/en-a/part-00000.parquet": [("ah1", "hello world")],
    "train/en-b/part-00000.parquet": [("b1", SHOUTED), ("b2", SUPERSCRIPT), ("b3", "")],
    "train/en-b/part-00001.parquet": [("b4", "Hello   WORLD")],
}
EXPECTED = {   # every pair at or above 0.5: (jaccard, exact)
    ("en-a-a1", "en-b-b1"): (1.0, True),      # same text after case, spaces and line breaks
    ("en-a-a3", "en-b-b2"): (1.0, True),      # same text after NFKC
    ("en-a-a4", "en-b-b3"): (1.0, True),      # two empty documents
    ("en-a-ah1", "en-b-b4"): (1.0, True),     # under 5 words: one shingle each, the same one
    ("en-a-a1", "en-a-a2"): (EDIT_SCORE, False),
    ("en-a-a2", "en-b-b1"): (EDIT_SCORE, False),
}


def make_sample(root, parts):
    """Write parts (split/pack/part -> [(doc_id, text)]) under root/inputs/sample_v0 with their SHA256SUMS; return the
    sha256 of SHA256SUMS, the pin for the config."""
    base = root / "inputs" / "sample_v0"
    lines = []
    for name, docs in parts.items():
        path = base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(pa.Table.from_pylist([{"doc_id": d, "text": t} for d, t in docs]), path)
        lines.append(f"{ov.sha256_file(path)}  {name}")
    (base / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    return ov.sha256_file(base / "SHA256SUMS")


def make_config(root, pin, **over):
    path = root / "overlap_test.json"
    path.write_text(json.dumps({"sha256sums_sha256": pin, "packs": ["en-a", "en-b"], "out": "out/t", **over}))
    return path


def run(monkeypatch, root, cfg_path):
    """Run overlap.main() with root as the repository root; return the output folder, the pairs and the summary."""
    monkeypatch.setattr(ov, "REPO", root)
    monkeypatch.setattr(sys, "argv", ["overlap.py", "--config", str(cfg_path)])
    ov.main()
    out = root / json.loads(cfg_path.read_text())["out"]
    with open(out / "overlap_pairs.csv", newline="") as f:
        pairs = list(csv.DictReader(f))
    return out, pairs, json.loads((out / "overlap_summary.json").read_text())


@pytest.fixture
def hand_run(tmp_path, monkeypatch):
    return run(monkeypatch, tmp_path, make_config(tmp_path, make_sample(tmp_path, SAMPLE)))


def brute_force(texts):
    """Every pair's Jaccard straight from the shingle sets: (row a, row b) -> score; two empty sets score 1.0."""
    sets = []
    for t in texts:
        blob, _ = shingles(h1_key(t), 5)
        sets.append({blob[x:x + 8] for x in range(0, len(blob), 8)})
    return {(i, j): 1.0 if not sets[i] and not sets[j] else len(sets[i] & sets[j]) / len(sets[i] | sets[j])
            for i, j in combinations(range(len(sets)), 2)}


def random_texts(seed, n):
    """n made-up documents cut from a few shared passages with random word swaps, so many pairs share 5-grams."""
    rnd = random.Random(seed)
    vocab = [f"w{i}" for i in range(40)]
    passages = [[rnd.choice(vocab) for _ in range(30)] for _ in range(6)]
    texts = []
    for _ in range(n):
        words = list(rnd.choice(passages))
        for _ in range(rnd.randint(0, 8)):
            words[rnd.randrange(len(words))] = rnd.choice(vocab)
        start = rnd.randint(0, 10)
        texts.append(" ".join(words[start:start + rnd.randint(3, 25)]))
    return texts + ["", ""]


# The hand-checked sample


def test_every_pair_at_or_above_the_floor_is_listed_with_its_score_and_exact_flag(hand_run):
    _, pairs, _ = hand_run
    got = {(p["id_a"], p["id_b"]): (float(p["jaccard"]), p["exact"] == "True") for p in pairs}
    assert got.keys() == EXPECTED.keys()
    for pair, (score, exact) in EXPECTED.items():
        assert got[pair][0] == pytest.approx(score, abs=1e-6), pair
        assert got[pair][1] is exact, pair


def test_pairs_come_highest_first_and_name_both_documents(hand_run):
    _, pairs, _ = hand_run
    scores = [float(p["jaccard"]) for p in pairs]
    assert scores == sorted(scores, reverse=True)
    one = next(p for p in pairs if (p["id_a"], p["id_b"]) == ("en-a-ah1", "en-b-b4"))
    assert (one["pack_a"], one["split_a"], one["part_a"], one["row_a"]) == ("en-a", "heldout", "part-00000.parquet", "5")
    assert (one["pack_b"], one["split_b"], one["part_b"], one["row_b"]) == ("en-b", "train", "part-00001.parquet", "9")


def test_summary_counts_the_documents_pairs_and_exact_groups(hand_run):
    _, _, s = hand_run
    assert s["documents"] == {"en-a": {"train": 5, "heldout": 1, "all": 6}, "en-b": {"train": 4, "heldout": 0, "all": 4}}
    assert s["documents_all"] == 10 and s["pairs_compared"] == 45
    assert (s["h1_exact_groups"], s["documents_in_h1_exact_groups"], s["empty_documents"]) == (4, 8, 2)
    assert s["pairs_sharing_a_shingle"] == 5   # the two empty documents share no shingle; they are added as 1.0
    assert s["pairs_stored"] == 6
    assert s["pairs_at_or_above"] == {"0.70": 6, "0.75": 6, "0.80": 6, "0.85": 6, "0.90": 4, "0.95": 4}
    assert s["pairs_by_pack"]["exact"] == {"en-a x en-a": 0, "en-a x en-b": 4, "en-b x en-b": 0}
    assert s["pairs_by_pack"]["0.50"] == {"en-a x en-a": 1, "en-a x en-b": 5, "en-b x en-b": 0}
    assert [p["documents"] for p in s["inputs"]["parts"]] == [5, 1, 3, 1]
    assert s["peak_rss_mb"] > 0 and s["versions"]["numpy"] == np.__version__


def test_histogram_counts_every_pair_once(hand_run):
    out, _, _ = hand_run
    with open(out / "overlap_histogram.csv", newline="") as f:
        bins = [int(r["pairs"]) for r in csv.DictReader(f)]
    assert sum(bins) == 45
    assert (bins[0], bins[88], bins[99]) == (39, 2, 4)


def test_matrix_is_symmetric_with_ones_on_the_diagonal_and_rows_match_the_docs_table(hand_run):
    out, _, _ = hand_run
    M = sparse.load_npz(out / "overlap_matrix.npz").toarray()
    assert M.shape == (10, 10)
    assert (np.diag(M) == 1).all() and (M == M.T).all()
    ids = pq.read_table(out / "overlap_docs.parquet").column("id").to_pylist()
    assert ids == ["en-a-a1", "en-a-a2", "en-a-a3", "en-a-a4", "en-a-a5", "en-a-ah1", "en-b-b1", "en-b-b2", "en-b-b3",
                   "en-b-b4"]
    row = {d: r for r, d in enumerate(ids)}
    assert M[row["en-a-a1"], row["en-a-a2"]] == pytest.approx(EDIT_SCORE)
    assert M[row["en-a-a4"], row["en-b-b3"]] == 1.0
    assert M[row["en-a-a5"]].sum() == 1.0   # the unrelated document: only its own diagonal cell


def test_outputs_stay_in_out_and_the_summary_hashes_match_them(tmp_path, hand_run):
    out, _, s = hand_run
    assert sorted(p.name for p in tmp_path.iterdir()) == ["inputs", "out", "overlap_test.json"]
    assert sorted(p.name for p in out.iterdir()) == sorted([*s["outputs"], "overlap_summary.json"])
    for name, meta in s["outputs"].items():
        assert meta["sha256"] == hashlib.sha256((out / name).read_bytes()).hexdigest()
        assert meta["bytes"] == (out / name).stat().st_size


# Every pair against brute force


def test_every_score_matches_a_brute_force_jaccard_of_every_pair(tmp_path, monkeypatch):
    texts = random_texts(0, 60)
    half = len(texts) // 2
    parts = {"train/en-a/part-00000.parquet": [(f"r{k}", t) for k, t in enumerate(texts[:half])],
             "train/en-b/part-00000.parquet": [(f"r{k}", t) for k, t in enumerate(texts[half:], half)]}
    # Floor 0.01: the largest shingle set here has 21 members, so every pair that shares a shingle scores 1/41 or more.
    out, pairs, s = run(monkeypatch, tmp_path, make_config(tmp_path, make_sample(tmp_path, parts), floor=0.01))
    want = {k: v for k, v in brute_force(texts).items() if v > 0}
    got = {(int(p["row_a"]), int(p["row_b"])): float(p["jaccard"]) for p in pairs}
    assert len(want) > 20   # the corpus really does overlap
    assert got.keys() == want.keys()
    for pair, score in want.items():
        assert got[pair] == pytest.approx(score, abs=1e-6), pair
    M = sparse.load_npz(out / "overlap_matrix.npz")
    for (i, j), score in want.items():
        assert M[i, j] == pytest.approx(score) and M[j, i] == pytest.approx(score)
    with open(out / "overlap_histogram.csv", newline="") as f:
        bins = [int(r["pairs"]) for r in csv.DictReader(f)]
    expected = [0] * 100
    for score in brute_force(texts).values():
        expected[min(int(score * 100 + 1e-9), 99)] += 1
    assert bins == expected
    assert s["pairs_compared"] == len(texts) * (len(texts) - 1) // 2


# Finding and checking the inputs


def test_parts_are_found_in_pack_split_part_order_and_other_packs_are_skipped(tmp_path):
    make_sample(tmp_path, {**SAMPLE, "train/en-c/part-00000.parquet": [("c1", BASE)]})
    base = tmp_path / "inputs" / "sample_v0"
    got = ov.find_parts(base, base / "SHA256SUMS", ["en-b", "en-a"], ["train", "heldout"])
    assert [f"{sp}/{pk}/{pt}" for sp, pk, pt, _, _ in got] == [
        "train/en-b/part-00000.parquet", "train/en-b/part-00001.parquet",
        "train/en-a/part-00000.parquet", "heldout/en-a/part-00000.parquet"]


def test_a_regrouped_copy_is_found_by_its_sha256(tmp_path):
    make_sample(tmp_path, SAMPLE)
    base = tmp_path / "inputs" / "sample_v0"
    moved = base / "packs" / "en-a" / "Part_1" / "part-00000.parquet"   # the Cap1-packs layout
    moved.parent.mkdir(parents=True)
    shutil.move(base / "train" / "en-a" / "part-00000.parquet", moved)
    got = {f"{sp}/{pk}/{pt}": path for sp, pk, pt, path, _ in ov.find_parts(base, base / "SHA256SUMS", ["en-a"],
                                                                           ["train", "heldout"])}
    assert got["train/en-a/part-00000.parquet"] == moved


def test_a_part_whose_bytes_differ_stops_the_run(tmp_path, monkeypatch):
    cfg = make_config(tmp_path, make_sample(tmp_path, SAMPLE))
    part = tmp_path / "inputs" / "sample_v0" / "train" / "en-b" / "part-00000.parquet"
    pq.write_table(pa.Table.from_pylist([{"doc_id": "b1", "text": "changed"}]), part)
    with pytest.raises(SystemExit, match="no file under .* has the sha256 of train/en-b/part-00000.parquet"):
        run(monkeypatch, tmp_path, cfg)
    assert not (tmp_path / "out").exists()


def test_a_pack_with_no_part_in_sha256sums_stops_the_run(tmp_path, monkeypatch):
    cfg = make_config(tmp_path, make_sample(tmp_path, SAMPLE), packs=["en-a", "en-z"])
    with pytest.raises(SystemExit, match="lists no train/heldout part for \\['en-z'\\]"):
        run(monkeypatch, tmp_path, cfg)


def test_sha256sums_must_match_the_pin(tmp_path, monkeypatch):
    make_sample(tmp_path, SAMPLE)
    with pytest.raises(SystemExit, match="the config pins 0+$"):
        run(monkeypatch, tmp_path, make_config(tmp_path, "0" * 64))


def test_outputs_over_max_output_mb_fail_after_they_are_written(tmp_path, monkeypatch):
    cfg = make_config(tmp_path, make_sample(tmp_path, SAMPLE), max_output_mb=0.001)   # about 1 KB
    with pytest.raises(SystemExit, match="over max_output_mb 0.001"):
        run(monkeypatch, tmp_path, cfg)
    assert (tmp_path / "out" / "t" / "overlap_summary.json").exists()


# The config


@pytest.mark.parametrize("over, message", [
    ({"flor": 0.5}, "unknown keys .*'flor'"),
    ({"sha256sums_sha256": None}, "must pin sha256sums_sha256"),
    ({"floor": 0}, "floor must be above 0"),
    ({"floor": 1.5}, "floor must be above 0"),
    ({"out": "results/t"}, "out must be inside out/"),
    ({"out": "out/../t"}, "out must be inside out/"),
    ({"inputs": "/tmp/sample_v0"}, "must be relative to the repository root"),
    ({"splits": ["dev"]}, "splits must be train and/or heldout"),
])
def test_a_bad_config_is_refused_before_any_work(tmp_path, monkeypatch, over, message):
    monkeypatch.setattr(ov, "REPO", tmp_path)
    with pytest.raises(SystemExit, match=message):
        ov.load_config(make_config(tmp_path, "a" * 64, **over))


def test_a_good_config_gets_the_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr(ov, "REPO", tmp_path)
    cfg = ov.load_config(make_config(tmp_path, "a" * 64, _comment="ignored"))
    assert (cfg["floor"], cfg["k"], cfg["splits"], cfg["max_output_mb"]) == (0.5, 5, ["train", "heldout"], 50)
    assert "_comment" not in cfg
