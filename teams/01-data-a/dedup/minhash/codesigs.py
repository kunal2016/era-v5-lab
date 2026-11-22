"""MinHash signatures on overlap_rules.code_shingles (v1's code-token 5-grams). Usage: python codesigs.py <parquet>..."""
import os, pathlib
OUT = os.environ.get("MH_OUT", "out/minhash_item11")
import sys, time, numpy as np, pyarrow.parquet as pq
sys.path.insert(0, os.environ.get("DEDUP_DIR", "teams/01-data-a/dedup"))
from overlap_rules import code_shingles
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigs import sig  # same 128 hash functions and seed
os.makedirs(OUT, exist_ok=True)
for path in sys.argv[1:]:
    t0 = time.time(); split, pack, fname = pathlib.Path(path).parts[-3:]
    ids, ns, lines, sigs = [], [], [], []
    for batch in pq.ParquetFile(path).iter_batches(batch_size=2000, columns=["doc_id", "text"]):
        for d, x in zip(batch.column(0).to_pylist(), batch.column(1).to_pylist()):
            blob, nl = code_shingles(x, pack)
            s = np.frombuffer(blob, dtype=np.uint64) if blob else np.zeros(0, np.uint64)
            ids.append(d); ns.append(len(s)); lines.append(nl); sigs.append(sig(s))
    np.savez(f"{OUT}/csig_{pack}_{split}_{fname.split('.')[0]}.npz", ids=np.array(ids), n=np.array(ns),
             lines=np.array(lines), sig=np.stack(sigs))
    print(f"{split}/{pack}/{fname}: {len(ids)} docs, {sum(ns)} code shingles, {time.time()-t0:.0f}s", flush=True)
