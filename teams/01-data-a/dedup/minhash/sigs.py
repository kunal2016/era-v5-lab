"""MinHash signatures for dedup v2 item 11, using overlap.py's exact word shingles (h1_key + jaccard_matrix.shingles).

Usage (from the repository root):
    MH_OUT=out/minhash_item11 python sigs.py <cleaned part.parquet> ...
writes MH_OUT/sig_<pack>_<split>_<part>.npz with doc_ids, shingle counts and a 128-value signature per document.
"""
import os, pathlib, sys, time
import numpy as np, pyarrow.parquet as pq

OUT = os.environ.get("MH_OUT", "out/minhash_item11")
sys.path.insert(0, os.environ.get("DEDUP_DIR", "teams/01-data-a/dedup"))
from h1_sha256 import h1_key            # noqa: E402  v1's H1 key (normalize.match_key, NFKC, casefold, spaces)
from jaccard_matrix import shingles     # noqa: E402  v1's word 5-grams as 64-bit hashes

P = 128                                  # hash functions (permutations)
rng = np.random.default_rng(20261122)    # fixed seed: same functions on every run
A = (rng.integers(1, 2**63, P, dtype=np.uint64) | np.uint64(1))
B = rng.integers(0, 2**63, P, dtype=np.uint64)


def mix(z):
    """splitmix64 finaliser: turns a*x+b into a well-spread 64-bit value."""
    z ^= z >> np.uint64(30); z *= np.uint64(0xBF58476D1CE4E5B9)
    z ^= z >> np.uint64(27); z *= np.uint64(0x94D049BB133111EB)
    z ^= z >> np.uint64(31)
    return z


def sig(s):
    """MinHash signature: for each of the P hash functions, the smallest hash over the document's shingles."""
    out = np.full(P, np.iinfo(np.uint64).max, dtype=np.uint64)
    if len(s) == 0:
        return out
    with np.errstate(over="ignore"):
        for i in range(0, len(s), 20000):
            c = s[i:i + 20000]
            out = np.minimum(out, mix(c[None, :] * A[:, None] + B[:, None]).min(axis=1))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for path in sys.argv[1:]:
        t0 = time.time(); split, pack, fname = pathlib.Path(path).parts[-3:]
        ids, ns, sigs = [], [], []
        for batch in pq.ParquetFile(path).iter_batches(batch_size=2000, columns=["doc_id", "text"]):
            for d, x in zip(batch.column(0).to_pylist(), batch.column(1).to_pylist()):
                sh, _ = shingles(h1_key(x), 5)
                s = np.frombuffer(sh, dtype=np.uint64) if sh else np.zeros(0, np.uint64)
                ids.append(d); ns.append(len(s)); sigs.append(sig(s))
        np.savez(f"{OUT}/sig_{pack}_{split}_{fname.split('.')[0]}.npz", ids=np.array(ids), n=np.array(ns), sig=np.stack(sigs))
        print(f"{split}/{pack}/{fname}: {len(ids)} docs, {sum(ns)} shingles, {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
