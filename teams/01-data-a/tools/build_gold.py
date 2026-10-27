"""Build gold sets from two (or more) readers' label sheets, and measure their agreement.

Layout it reads (the same as the repo):
    <root>/<pack_id>/<reader>/labels.csv

Usage:
    python build_gold.py <root> [--out gold] [--target 200]

For every pack with at least two readers:
    gold      doc_ids that at least two readers read in `full` and both marked `clean`
    agreement on documents both readers labelled: same verdict, and same disease codes
Writes <out>/<pack_id>.txt (one doc_id per line, at most --target ids) and prints a table.
Packs with one reader are listed: they need a second reader before they have gold.
"""
import argparse, csv, itertools, os, random


def read_labels(path):
    try:
        rows = list(csv.DictReader(open(path, encoding="utf-8-sig", newline="")))
    except Exception:
        return {}
    out = {}
    for r in rows:
        d = (r.get("doc_id") or "").strip()
        if d:
            out[d] = {"read": (r.get("read") or "").strip().lower(),
                      "verdict": (r.get("verdict") or "").strip().lower(),
                      "codes": frozenset(c.strip().upper() for c in (r.get("diseases") or "").split(";") if c.strip())}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--out", default="gold"); ap.add_argument("--target", type=int, default=200)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    single, table = [], []
    for pack in sorted(os.listdir(a.root)):
        pdir = os.path.join(a.root, pack)
        if not os.path.isdir(pdir):
            continue
        readers = {h: read_labels(os.path.join(pdir, h, "labels.csv"))
                   for h in sorted(os.listdir(pdir)) if os.path.isfile(os.path.join(pdir, h, "labels.csv"))}
        readers = {h: l for h, l in readers.items() if l}
        if len(readers) < 2:
            single.append((pack, ", ".join(readers) or "none", sum(len(l) for l in readers.values())))
            continue
        clean_by = {}
        overlap = same_verdict = same_codes = 0
        for (h1, l1), (h2, l2) in itertools.combinations(readers.items(), 2):
            for d in set(l1) & set(l2):
                overlap += 1
                same_verdict += l1[d]["verdict"] == l2[d]["verdict"]
                same_codes += l1[d]["codes"] == l2[d]["codes"]
        for h, l in readers.items():
            for d, r in l.items():
                if r["read"] == "full" and r["verdict"] == "clean":
                    clean_by.setdefault(d, set()).add(h)
        gold = sorted(d for d, hs in clean_by.items() if len(hs) >= 2)
        random.Random(pack).shuffle(gold)
        gold = sorted(gold[:a.target])
        with open(os.path.join(a.out, f"{pack}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(gold) + ("\n" if gold else ""))
        table.append((pack, len(readers), overlap, same_verdict, same_codes, len(gold)))

    print(f"{'pack':22} {'readers':>7} {'shared':>7} {'same verdict':>13} {'same codes':>11} {'gold':>5}")
    for pack, n, ov, sv, sc, g in table:
        pv = f"{100 * sv / ov:.0f}%" if ov else "-"
        pc = f"{100 * sc / ov:.0f}%" if ov else "-"
        print(f"{pack:22} {n:7d} {ov:7d} {pv:>13} {pc:>11} {g:5d}" + ("   (short of target)" if g < a.target else ""))
    if single:
        print("\nOne reader only, so no gold yet (needs a second reader):")
        for pack, who, n in single:
            print(f"  {pack:22} {n:4d} rows by {who}")


if __name__ == "__main__":
    main()
