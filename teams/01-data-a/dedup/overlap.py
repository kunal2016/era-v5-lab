r"""Cross-pack overlap: the all-to-all Jaccard similarity of every pair of documents across several packs.

Reads the train and heldout parts of each pack named in the config as one combined set, builds each document's H1 key
(h1_sha256.py: spec v1 normalize.match_key, then NFKC, casefold, whitespace), splits it into word 5-grams
(jaccard_matrix.py) and computes the exact Jaccard similarity of every pair of documents, inside a pack and across packs.
A document is named <pack_id>-<doc_id>, e.g. en-dclm-0086b8a3e2a24597. Pairs scoring 1.0 are kept and listed like every
other pair; "exact" marks the pairs whose H1 keys are identical (same SHA-256), and two empty documents score 1.0.
Documents are never changed, and no text is written out: IDs, scores and counts only.

The inputs are Week-2 tokenizer sample v0 parts, pinned by the sample's SHA256SUMS, whose own sha256 is in the config.
Each part is looked for at <inputs>/<split>/<pack>/<part> and otherwise by its sha256 anywhere under <inputs>, so a
renamed or regrouped copy is found too. A missing part, or one whose bytes differ, stops the run before any work.

HOW TO RUN IT
=============
With the sample v0 (SHA256SUMS and the parts) under inputs/sample_v0/ in the repository root. Python 3.9 or later with
numpy, scipy and pyarrow (python3 -m pip install numpy scipy pyarrow). It needs no network and no keys, reads only its
inputs and writes only to out/ in the repository root. Paths in the config are relative to the repository root, the
job's working directory, so the script can also be started from any other folder.

    python teams/01-data-a/dedup/overlap.py --config teams/01-data-a/dedup/overlap_en.json

CONFIG (JSON; keys starting with "_" are comments)
==================================================
  inputs              the sample v0 folder, relative to the repository root      (default inputs/sample_v0)
  sha256sums          its SHA256SUMS                                             (default <inputs>/SHA256SUMS)
  sha256sums_sha256   the sha256 that SHA256SUMS must have                       (required)
  packs, splits       the pack ids, and train and/or heldout                     (default the 4 English packs, both)
  out                 the output folder, inside out/                             (default out/overlap)
  floor               store and list the pairs at or above this Jaccard          (default 0.5)
  k, block, top       words per shingle, matrix rows per step, pairs printed     (default 5, 256, 20)
  max_output_mb       fail if the outputs are larger                             (default 50)

WHAT IT WRITES (in out)
=======================
  overlap_pairs.csv       every pair at or above the floor, 1.0 included, highest first: id_a, id_b, jaccard, shared
                          5-grams, exact, and each document's pack, split, part, size and matrix row
  overlap_matrix.npz      the N x N matrix, for scipy.sparse.load_npz: symmetric, 1 on the diagonal, row i is row i of
                          overlap_docs.parquet. Only scores at or above the floor are stored, so an empty cell means
                          "below the floor", not 0.
  overlap_docs.parquet    matrix row -> document: row, id, pack, split, part, row_in_part, words, shingles
  overlap_by_pack.csv     pack x pack: pairs at or above each level (the floor, the E1 thresholds, 1.0) and exact pairs
  overlap_histogram.csv   all N(N-1)/2 pairs in bins of 0.01, including the pairs that share nothing (Jaccard 0)
  overlap_summary.json    the counts, the input parts and their sha256, wall time, peak RSS, package versions, and
                          each other output's size and sha256
"""
import sys
sys.dont_write_bytecode = True   # write only to ./out/: no __pycache__ beside the scripts

import argparse, hashlib, json, os, platform, resource, time  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from h1_sha256 import NORMALIZE_ID, h1_key, read_file, write_csv  # noqa: E402
from jaccard_matrix import THRESHOLDS, shingles  # noqa: E402

REPO = Path(__file__).resolve().parents[3]   # teams/01-data-a/dedup/overlap.py -> the repository root
ENGLISH = ["en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"]
DEFAULTS = {"inputs": "inputs/sample_v0", "sha256sums": None, "sha256sums_sha256": None, "packs": ENGLISH,
            "splits": ["train", "heldout"], "out": "out/overlap", "floor": 0.5, "k": 5, "block": 256, "top": 20,
            "max_output_mb": 50}
CHUNK = 2000   # documents per block of shingle digests while reading


def load_config(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    unknown = sorted(k for k in raw if not k.startswith("_") and k not in DEFAULTS)
    if unknown:
        sys.exit(f"ERROR: unknown keys in {path}: {unknown}")
    cfg = {**DEFAULTS, **{k: v for k, v in raw.items() if not k.startswith("_")}}
    if not cfg["sha256sums_sha256"]:
        sys.exit(f"ERROR: {path} must pin sha256sums_sha256")
    if any(cfg[k] and Path(cfg[k]).is_absolute() for k in ("inputs", "sha256sums", "out")):
        sys.exit("ERROR: inputs, sha256sums and out must be relative to the repository root")
    if not 0 < cfg["floor"] <= 1:
        sys.exit("ERROR: floor must be above 0 and at most 1; the histogram still counts every pair")
    if not (REPO / cfg["out"]).resolve().is_relative_to((REPO / "out").resolve()):
        sys.exit(f"ERROR: out must be inside out/ in the repository root, not {cfg['out']}")
    if not set(cfg["splits"]) <= {"train", "heldout"}:
        sys.exit(f"ERROR: splits must be train and/or heldout, not {cfg['splits']}")
    return cfg


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_parts(inputs, sums, packs, splits):
    """[(split, pack, part, path, sha256)] for the wanted parts in SHA256SUMS, in pack, split, part order, each checked."""
    want = []
    for line in sums.read_text().splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            fields = name.strip().split("/")
            if len(fields) == 3 and fields[0] in splits and fields[1] in packs and fields[2].endswith(".parquet"):
                want.append((fields[0], fields[1], fields[2], digest))
    absent = [p for p in packs if p not in {w[1] for w in want}]
    if absent:
        sys.exit(f"ERROR: {sums} lists no {'/'.join(splits)} part for {absent}")
    found, by_hash = [], None
    for split, pack, part, digest in sorted(want, key=lambda w: (packs.index(w[1]), splits.index(w[0]), w[2])):
        path = inputs / split / pack / part
        if not (path.is_file() and sha256_file(path) == digest):
            if by_hash is None:   # hash every Parquet file under inputs once, to find renamed or regrouped copies
                by_hash = {}
                for dirpath, _, files in os.walk(inputs, followlinks=True):
                    for f in sorted(files):
                        if f.endswith(".parquet"):
                            by_hash.setdefault(sha256_file(Path(dirpath) / f), Path(dirpath) / f)
            path = by_hash.get(digest)
            if path is None:
                sys.exit(f"ERROR: no file under {inputs} has the sha256 of {split}/{pack}/{part} ({digest})")
        found.append((split, pack, part, path, digest))
    return found


def peak_rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss   # bytes on macOS, KiB on Linux
    return round(r / (1 << 20) if sys.platform == "darwin" else r / 1024, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, help="JSON config; see CONFIG above")
    cfg = load_config(ap.parse_args().config)
    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
        import scipy
        from scipy import sparse
    except ImportError:
        sys.exit("ERROR: needs numpy, scipy and pyarrow: python3 -m pip install numpy scipy pyarrow")
    t0 = time.time()
    inputs, out, packs, splits = REPO / cfg["inputs"], REPO / cfg["out"], cfg["packs"], cfg["splits"]
    sums = REPO / (cfg["sha256sums"] or Path(cfg["inputs"]) / "SHA256SUMS")
    if not sums.is_file():
        sys.exit(f"ERROR: no {sums}; put the sample v0 (SHA256SUMS and the parts) in inputs/sample_v0/ "
                 f"in the repository root {REPO}")
    if sha256_file(sums) != cfg["sha256sums_sha256"]:
        sys.exit(f"ERROR: {sums} has sha256 {sha256_file(sums)}; the config pins {cfg['sha256sums_sha256']}")
    parts = find_parts(inputs, sums, packs, splits)
    print(f"{len(parts)} parts found and checked against {sums.relative_to(REPO)} ({time.time() - t0:.0f}s)", flush=True)

    # 1. Combine every part of every pack: one row per document, with its H1 hash and its set of shingles.
    # docs[i] = (pack, split, part, row_in_part, doc_id, words, shingles, sha256)
    docs, chunks, buf, part_docs = [], [], [], []
    for split, pack, part, path, _ in parts:
        n = 0
        for row, doc_id, text in read_file(path):
            key = h1_key(text or "")
            blob, words = shingles(key, cfg["k"])
            buf.append(blob)
            docs.append((pack, split, part, row, doc_id, words, len(blob) // 8,
                         hashlib.sha256(key.encode("utf-8")).hexdigest()))
            n += 1
            if len(buf) == CHUNK:
                chunks.append(np.frombuffer(b"".join(buf), dtype=np.int64))
                buf = []
        part_docs.append(n)
        print(f"{split}/{pack}/{part}: {n} documents ({time.time() - t0:.0f}s)", flush=True)
    if buf:
        chunks.append(np.frombuffer(b"".join(buf), dtype=np.int64))
    N = len(docs)
    if N < 2:
        sys.exit(f"ERROR: {N} document(s); nothing to compare")
    sizes = np.array([d[6] for d in docs], dtype=np.int64)
    indptr = np.concatenate(([0], np.cumsum(sizes)))
    pack_ix = np.array([packs.index(d[0]) for d in docs], dtype=np.int64)
    ids = [f"{d[0]}-{d[4]}" for d in docs]
    sha = [d[7] for d in docs]

    # 2. X: documents x the shingles found in 2+ documents (a shingle in one document can never be shared).
    s = np.concatenate(chunks)
    s.sort()
    eq = s[1:] == s[:-1]
    shared, distinct = np.unique(s[1:][eq]), len(s) - int(eq.sum())
    del s, eq
    rows, cols, start = [], [], 0
    for c in chunks:
        pos = np.minimum(np.searchsorted(shared, c), max(len(shared) - 1, 0))
        hit = shared[pos] == c if len(shared) else np.zeros(len(c), bool)
        cols.append(pos[hit])
        rows.append(np.searchsorted(indptr, start + np.flatnonzero(hit), side="right") - 1)
        start += len(c)
    del chunks
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    X = sparse.csr_matrix((np.ones(len(rows), np.int32), (rows, cols)), shape=(N, len(shared)))
    XT = X.T.tocsr()
    steps = int((np.bincount(cols).astype(np.int64) ** 2).sum()) if len(cols) else 0
    del rows, cols
    print(f"{N} documents, {distinct} distinct shingles, {len(shared)} of them in 2+ documents; "
          f"about {steps:,} intersection steps", flush=True)

    # 3. All-to-all: |A & B| for every pair that shares a shingle, block by block; every other pair is 0.
    total = N * (N - 1) // 2
    hist, over, sharing = np.zeros(100, np.int64), dict.fromkeys(THRESHOLDS, 0), 0
    kept = ([], [], [], [])   # row a, row b, Jaccard, shared shingles: pairs at or above the floor
    t1 = time.time()
    for step, lo in enumerate(range(0, N, cfg["block"])):
        hi = min(lo + cfg["block"], N)
        P = (X[lo:hi] @ XT).tocoo()
        i, j = P.row.astype(np.int64) + lo, P.col.astype(np.int64)
        m = j > i
        i, j, inter = i[m], j[m], P.data[m].astype(np.int64)
        score = inter / (sizes[i] + sizes[j] - inter)
        sharing += len(score)
        hist += np.bincount(np.minimum((score * 100 + 1e-9).astype(np.int64), 99), minlength=100)
        for t in THRESHOLDS:
            over[t] += int((score >= t).sum())
        k = score >= cfg["floor"]
        for acc, v in zip(kept, (i[k], j[k], score[k], inter[k])):
            acc.append(v)
        if step % 50 == 0 or hi == N:
            el = time.time() - t1
            print(f"  rows {hi}/{N}: {el:.0f}s, about {el * (N - hi) / hi:.0f}s left", flush=True)
    empty = np.flatnonzero(sizes == 0)   # documents with an empty key: identical to each other, so 1.0
    a, b = np.triu_indices(len(empty), 1)
    for acc, v in zip(kept, (empty[a], empty[b], np.ones(len(a)), np.zeros(len(a), np.int64))):
        acc.append(v)
    hist[99] += len(a)
    for t in THRESHOLDS:
        over[t] += len(a)
    hist[0] += total - sharing - len(a)

    I, J, S, K = (np.concatenate(v) for v in kept)
    order = np.lexsort((J, I, -S))
    I, J, S, K = I[order], J[order], S[order], K[order]
    exact = np.array([sha[x] == sha[y] for x, y in zip(I.tolist(), J.tolist())], dtype=bool)

    # 4. Outputs, all inside ./out/.
    out.mkdir(parents=True, exist_ok=True)
    diag = np.arange(N)
    M = sparse.coo_matrix((np.concatenate([S, S, np.ones(N)]),
                           (np.concatenate([I, J, diag]), np.concatenate([J, I, diag]))), shape=(N, N)).tocsr()
    sparse.save_npz(out / "overlap_matrix.npz", M)
    pq.write_table(pa.table({"row": np.arange(N), "id": ids, "pack": [d[0] for d in docs], "split": [d[1] for d in docs],
                             "part": [d[2] for d in docs], "row_in_part": [d[3] for d in docs],
                             "words": [d[5] for d in docs], "shingles": sizes}),
                   out / "overlap_docs.parquet", compression="zstd")
    side = lambda r: [docs[r][0], docs[r][1], docs[r][2], docs[r][6], r]
    write_csv(out / "overlap_pairs.csv", ["id_a", "id_b", "jaccard", "shared_shingles", "exact",
                                          "pack_a", "split_a", "part_a", "shingles_a", "row_a",
                                          "pack_b", "split_b", "part_b", "shingles_b", "row_b"],
              ([ids[x], ids[y], f"{s:.6f}", n, e, *side(x), *side(y)]
               for x, y, s, n, e in zip(I.tolist(), J.tolist(), S.tolist(), K.tolist(), exact.tolist())))
    write_csv(out / "overlap_histogram.csv", ["jaccard_from", "jaccard_to", "pairs"],
              ([f"{b / 100:.2f}", f"{(b + 1) / 100:.2f}", int(hist[b])] for b in range(100)))

    # Rows are in pack order and a < b, so each pair's packs come out in that order too.
    pa_ix, pb_ix = pack_ix[I], pack_ix[J]
    levels = [(f"{t:.2f}", S >= t) for t in sorted({cfg["floor"], *(t for t in THRESHOLDS if t >= cfg["floor"]), 1.0})]
    levels.append(("exact", exact))
    by_pack = {}
    for name, m in levels:
        c = Counter(zip(pa_ix[m].tolist(), pb_ix[m].tolist()))
        by_pack[name] = {f"{packs[x]} x {packs[y]}": c[(x, y)] for x in range(len(packs)) for y in range(x, len(packs))}
    write_csv(out / "overlap_by_pack.csv", ["level", "pack_a", "pack_b", "pairs"],
              ([name, *pair.split(" x "), n] for name, grid in by_pack.items() for pair, n in grid.items()))

    written = ("overlap_pairs.csv", "overlap_matrix.npz", "overlap_docs.parquet", "overlap_by_pack.csv",
               "overlap_histogram.csv")
    files = {f: {"bytes": (out / f).stat().st_size, "sha256": sha256_file(out / f)} for f in written}
    output_bytes = sum(v["bytes"] for v in files.values())
    output_mb = round(output_bytes / (1 << 20), 1)
    h1 = [n for n in Counter(sha).values() if n > 1]
    per_split = Counter((d[0], d[1]) for d in docs)
    summary = {
        "config": cfg,
        "normalize_id": NORMALIZE_ID,
        "key": "h1_key of h1_sha256.py: normalize.match_key, then NFKC, casefold, whitespace runs to one space",
        "shingles": f"word {cfg['k']}-grams of the key as 8-byte BLAKE2b digests; a key under {cfg['k']} words is one shingle",
        "inputs": {"sha256sums": str(sums.relative_to(REPO)), "sha256sums_sha256": cfg["sha256sums_sha256"],
                   "parts": [{"part": f"{sp}/{pk}/{pt}", "sha256": dg, "documents": n}
                             for (sp, pk, pt, _, dg), n in zip(parts, part_docs)]},
        "documents": {p: {**{sp: per_split[(p, sp)] for sp in splits}, "all": sum(per_split[(p, sp)] for sp in splits)}
                      for p in packs},
        "documents_all": N,
        "ids_used_by_2_or_more_documents": sum(n > 1 for n in Counter(ids).values()),
        "h1_exact_groups": len(h1),
        "documents_in_h1_exact_groups": sum(h1),
        "empty_documents": len(empty),
        "distinct_shingles": distinct,
        "shingles_in_2_or_more_documents": len(shared),
        "pairs_compared": total,
        "pairs_sharing_a_shingle": sharing,
        "pairs_at_or_above": {f"{t:.2f}": over[t] for t in THRESHOLDS},
        "pairs_stored": len(S),
        "pairs_by_pack": by_pack,
        "wall_seconds": round(time.time() - t0, 1),
        "peak_rss_mb": peak_rss_mb(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                     "pyarrow": pa.__version__, "platform": platform.platform()},
        "outputs": files,
        "output_mb": output_mb,
    }
    (out / "overlap_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("config", "inputs", "pairs_by_pack", "outputs")},
                     indent=2))
    for name in ("0.80", "1.00", "exact"):
        print(f"\nPairs at {'Jaccard ' + name + ' and above' if name != 'exact' else 'exact (same H1 key)'}:")
        for pair, n in by_pack.get(name, {}).items():
            print(f"  {pair:45} {n}")
    print(f"\nTop {min(cfg['top'], len(S))} pairs:")
    for x, y, s, e in list(zip(I.tolist(), J.tolist(), S.tolist(), exact.tolist()))[:cfg["top"]]:
        print(f"  {s:.4f}  {'exact ' if e else '      '}{ids[x]}  {ids[y]}")
    print(f"\nWrote {', '.join(files)} and overlap_summary.json to {out.relative_to(REPO)} ({output_mb} MB)")
    if output_bytes > cfg["max_output_mb"] * (1 << 20):
        sys.exit(f"ERROR: the outputs are {output_mb} MB, over max_output_mb {cfg['max_output_mb']}; raise floor")


if __name__ == "__main__":
    sys.exit(main())
