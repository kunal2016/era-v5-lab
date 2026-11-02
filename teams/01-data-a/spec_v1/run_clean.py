"""Run clean.py on one pack, or on one part of a pack. Reads only that file, writes only to --out, needs no network.

  python run_clean.py --pack code-go.parquet --out out
  python run_clean.py --pack train/code-go/part-00000.parquet --pack-id code-go --out out

The pack is --pack-id when given, else the file name (<pack_id>.parquet). It must be one of the 13 packs clean.py has
rules for: any other stops the run with exit code 1 before the file is read or anything is written, since clean.py would
pass every doc through unchanged. A pack_id column in the file must name the same pack.
Writes out/<name>_clean.parquet (the kept docs, with their cleaned text) and out/<name>_summary.json (counts, dropped
doc_ids, and the SHA-256 of the input file and of the clean.py that ran; no text). <name> is the file name without
.parquet, after the pack when --pack-id names another (code-go_part-00000), so parts of two packs never overwrite each other.

--f2 then runs F2, G9's benchmark fingerprints (tools/f2_rule.py), on each doc clean.py keeps, and drops the ones it flags.
The summary gets "f2": the set_sha256, and each dropped doc_id with up to 5 benchmark items and the offset in the cleaned text.
"""
import argparse, hashlib, json, sys, time
from collections import Counter
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clean as c


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--pack", type=Path, required=True, help="the Parquet file: a pack, or a part of one")
ap.add_argument("--pack-id", help="the pack the file belongs to, for a file not named <pack_id>.parquet (a tokenizer sample part)")
ap.add_argument("--out", type=Path, default=Path("out"))
ap.add_argument("--f2", action="store_true", help="after clean.py, drop the docs G9's benchmark fingerprints flag (about 1.1 GB, 20 s to load)")
args = ap.parse_args()
pack = args.pack_id or args.pack.stem
name = args.pack.stem if args.pack.stem == pack else f"{pack}_{args.pack.stem}"
if pack not in c._FAMILY:  # no rule applies to it, so a run would "succeed" without cleaning anything
    sys.exit(f"{args.pack.name}: {pack!r} is not one of the {len(c._FAMILY)} packs clean.py has rules for, so nothing would be cleaned. "
             f"Name the file <pack_id>.parquet or pass --pack-id, with one of: {', '.join(sorted(c._FAMILY))}")
rows = pq.read_table(args.pack).to_pylist()
for row in rows:  # clean.py picks the rules by pack_id: a file without the column takes the pack above
    if row.setdefault("pack_id", pack) != pack:
        sys.exit(f"{args.pack.name}: doc_id {row['doc_id']} has pack_id {row['pack_id']!r}, not {pack!r}")
f2 = None
if args.f2:
    sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
    import f2_rule as f2
    f2.fingerprints()  # load and check the set before anything is written
args.out.mkdir(parents=True, exist_ok=True)
t0, actions, dropped, errors, kept, f2_dropped = time.time(), Counter(), [], [], [], []
for row in rows:
    try:
        action, text = c.clean(row)
        flagged, hits = f2.check(text) if f2 and action != "drop" else (False, [])
    except Exception as e:  # a rule that crashes keeps the doc out and is reported by type, never by text
        errors.append([row["doc_id"], type(e).__name__])
        continue
    actions[action] += 1
    if action == "drop": dropped.append(row["doc_id"])
    elif flagged: f2_dropped.append({"doc_id": row["doc_id"], "items": [h["item"] for h in hits[:5]], "offset": hits[0]["offset"]})
    else: kept.append(dict(row, text=text))
pq.write_table(pa.Table.from_pylist(kept), args.out / f"{name}_clean.parquet")
summary = {"pack": args.pack.name, "input_sha256": sha256(args.pack), "pack_id": pack, "family": c._FAMILY[pack], "rows": len(rows), "actions": dict(actions), "errors": errors, "dropped": dropped, "seconds": round(time.time() - t0, 1), "docs_per_second": round(len(rows) / max(time.time() - t0, 1e-9), 1),
           "clean_py_sha256": sha256(Path(c.__file__))}  # which rules ran: the same hash means the same clean.py
if f2:
    summary["f2"] = {"set_sha256": f2.fingerprints().set_sha256, "dropped": f2_dropped}
(args.out / f"{name}_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
print({k: v for k, v in summary.items() if k not in ("dropped", "f2")}, "dropped:", len(dropped), *(("F2 dropped:", len(f2_dropped)) if f2 else ()))
sys.exit(1 if errors else 0)
