"""Run clean_english.py (the code and English sheets, built by ../tools/build_clean.py) on one pack. Reads only the pack,
writes only to --out, needs no network.

  python run_clean_english.py --pack en-dclm.parquet --out out

Writes out/<pack>_clean.parquet (the kept docs, with their cleaned text) and out/<pack>_summary.json (counts and dropped doc_ids, no text).
"""
import argparse, json, sys, time
from collections import Counter
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clean_english as c  # this folder's clean_english.py, not scripts/clean_english.py

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--pack", type=Path, required=True)
ap.add_argument("--out", type=Path, default=Path("out"))
args = ap.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
rows = pq.read_table(args.pack).to_pylist()
t0, actions, dropped, errors, kept = time.time(), Counter(), [], [], []
for row in rows:
    try:
        action, text = c.clean(row)
    except Exception as e:  # a rule that crashes keeps the doc out and is reported by type, never by text
        errors.append([row["doc_id"], type(e).__name__])
        continue
    actions[action] += 1
    if action == "drop": dropped.append(row["doc_id"])
    else: kept.append(dict(row, text=text))
pq.write_table(pa.Table.from_pylist(kept), args.out / f"{args.pack.stem}_clean.parquet")
summary = {"pack": args.pack.name, "rows": len(rows), "actions": dict(actions), "errors": errors, "dropped": dropped, "seconds": round(time.time() - t0, 1), "docs_per_second": round(len(rows) / max(time.time() - t0, 1e-9), 1)}
(args.out / f"{args.pack.stem}_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
print({k: v for k, v in summary.items() if k != "dropped"}, "dropped:", len(dropped))
sys.exit(1 if errors else 0)
