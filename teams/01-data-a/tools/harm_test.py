"""Harm test: run each medicine on a set of documents that readers marked clean.

Usage:
    python harm_test.py <pack.parquet> <labels.csv> --md <medicine.md> [<medicine.md> ...] [--gold <gold_ids.txt>]

Medicines come from the ```python medicine blocks in one or more medicine.md files
(see extract_medicines.py). Loading a medicine.md runs its code: read other people's
blocks first.

Without --gold, it uses every row of labels.csv with verdict `clean` and read `full`
as a PRELIMINARY gold set (your own clean rows). With --gold, it uses the doc_ids
listed in that file (one per line): the team gold set once it exists.

For each medicine it reports:
    harm  : gold documents the medicine changes or drops (fails if > 1%)
    reach : labelled cases of that disease the medicine actually fixes
"""
import argparse, csv, difflib, os, re, sys
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_medicines  # noqa: E402


def read_gold(path):
    """Gold file: a CSV with a doc_id column (e.g. doc_id,reader_1,reader_2 from build_gold.py),
    or a plain list with one doc_id per line."""
    lines = [l.strip() for l in open(path, encoding="utf-8-sig") if l.strip() and not l.startswith("#")]
    if lines and "doc_id" in [c.strip() for c in lines[0].split(",")]:
        return [r["doc_id"].strip() for r in csv.DictReader(open(path, encoding="utf-8-sig")) if r.get("doc_id")]
    return [l.split(",")[0].strip() for l in lines]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack"); ap.add_argument("labels"); ap.add_argument("--gold")
    ap.add_argument("--show", type=int, default=3, help="show this many changed gold docs per medicine")
    ap.add_argument("--md", nargs="+", required=True, help="load medicines from these medicine.md files")
    a = ap.parse_args()

    docs = {r["doc_id"]: r["text"] for r in pq.read_table(a.pack).to_pylist()}
    labels = list(csv.DictReader(open(a.labels, encoding="utf-8-sig")))
    if a.gold:
        gold = read_gold(a.gold)
        gold_name = f"team gold set ({os.path.basename(a.gold)})"
    else:
        gold = [l["doc_id"] for l in labels if l["verdict"] == "clean" and l["read"] == "full"]
        gold_name = "PRELIMINARY gold = my own clean rows"
    gold = [g for g in gold if g in docs]

    meds, problems = extract_medicines.load_many(a.md)
    source = ", ".join(a.md)
    print(f"Medicines: {len(meds)} from {source}")
    for p in problems:
        print(f"   could not load {p}")
    print(f"Gold set: {gold_name}, {len(gold)} documents" +
          ("  (none of these doc_ids are in this pack: harm test NOT_EVALUATED)" if not gold else "") + "\n")
    ok_all = True
    rows = []
    for name, (code, med) in meds.items():
        changed, dropped = [], []
        for g in gold:
            new, action = med(docs[g])
            if action == "drop":
                dropped.append(g)
            elif new != docs[g]:
                changed.append(g)
        harm = len(changed) + len(dropped)
        pct = 100 * harm / len(gold) if gold else 0
        verdict = "NOT_EVALUATED" if not gold else ("PASS" if pct <= 1.0 else "FAIL")
        ok_all &= verdict == "PASS"

        cases = [l["doc_id"] for l in labels if code in l["diseases"].split(";")]
        fixed = [c for c in cases if med(docs[c])[0] != docs[c]]
        missed = [c for c in cases if c not in fixed]

        rows.append((name, len(changed), len(dropped), pct, verdict, len(fixed), len(cases)))
        print(f"== {name}  harm test: {verdict}  changed {len(changed)}, dropped {len(dropped)} "
              f"of {len(gold)} gold documents ({pct:.1f}%, limit 1%)")
        print(f"   reach: fixes {len(fixed)} of {len(cases)} labelled {code} cases" +
              (f"; missed: {', '.join(missed)}" if missed else ""))
        for g in (changed + dropped)[:a.show]:
            new, _ = med(docs[g])
            diff = [l for l in difflib.unified_diff(docs[g].splitlines(), new.splitlines(), lineterm="", n=0)
                    if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
            mask = lambda x: re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email>", x)
            print(f"   changed gold doc {g}: " + " | ".join(mask(d)[:90] for d in diff[:4]))
        print()
    if len(rows) > 1:
        print(f"{'medicine':28} {'changed':>7} {'dropped':>7} {'harm':>6}  result  reach")
        for name, c, d, pct, v, fx, n in rows:
            print(f"{name:28} {c:7d} {d:7d} {pct:5.1f}%  {v:13}  {fx}/{n}")
        print()
    if problems:
        ok_all = False
    if ok_all:
        print("ALL MEDICINES PASS")
    elif not gold:
        print("NOT EVALUATED: no gold documents from this pack")
    else:
        print("AT LEAST ONE MEDICINE FAILS (or could not be loaded)")


if __name__ == "__main__":
    main()
