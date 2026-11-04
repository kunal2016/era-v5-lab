#!/usr/bin/env python3
"""eval_detector.py - precision and recall of detector.py on testset_100.csv.

Ground truth is the readers' labels: a document is D2 when at least one reader marked it D2.
Precision = how many of the detector's hits really are D2; recall = how many of the D2 documents it finds.
It also tries a few other thresholds, so the choice in detector.py can be checked, and lists every miss and false alarm.

Usage
  python3 eval_detector.py --testset testset_100.csv --packs-dir packs --out eval_v1.md
"""
import argparse
import csv
from pathlib import Path

import pyarrow.parquet as pq

import detector


def scores(pairs):
    tp = sum(p and y for p, y in pairs)
    fp = sum(p and not y for p, y in pairs)
    fn = sum(y and not p for p, y in pairs)
    tn = len(pairs) - tp - fp - fn
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return tp, fp, fn, tn, prec, rec


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score the D2 detector on the labelled test set.")
    ap.add_argument("--testset", default="testset_100.csv", type=Path)
    ap.add_argument("--packs-dir", default="packs", type=Path)
    ap.add_argument("--out", default="eval_v1.md", type=Path)
    a = ap.parse_args(argv)

    rows = list(csv.DictReader(open(a.testset, encoding="utf-8")))
    text = {}
    for pack in sorted({r["pack"] for r in rows}):
        for d in pq.read_table(a.packs_dir / f"{pack}.parquet", columns=["doc_id", "text"]).to_pylist():
            text[(pack, d["doc_id"])] = d["text"] or ""
    for r in rows:
        r["d2"] = r["reader_label"] == "1"
        r["det"] = detector.detect(text[(r["pack"], r["doc_id"])])

    tp, fp, fn, tn, p, rc = scores([(r["det"]["romanised"], r["d2"]) for r in rows])
    out = ["# D2 detector on 100 labelled documents (v1)", "",
           f"Test set: `{a.testset.name}`, {len(rows)} documents: "
           f"{sum(r['d2'] for r in rows)} that a reader marked D2 and {sum(not r['d2'] for r in rows)} "
           "that no reader marked D2 (half of those chosen among documents with at least 10% Latin letters).",
           "Ground truth: the readers' labels (a document is D2 when at least one reader marked it D2).", "",
           f"Detector rule: at least {detector.MIN_HITS} romanised Indic words, {detector.MIN_DISTINCT} of them "
           f"different, or at least {detector.MIN_IAST} IAST letters (see `detector.py`).", "",
           "## Result", "",
           "| D2 docs | flagged | true pos | false pos | missed | true neg | precision | recall |",
           "|---|---|---|---|---|---|---|---|",
           f"| {tp + fn} | {tp + fp} | {tp} | {fp} | {fn} | {tn} | {p:.0%} | {rc:.0%} |",
           "", "## Other thresholds", "",
           "| min hits | min distinct | min IAST | flagged | precision | recall |", "|---|---|---|---|---|---|"]
    for mh in (2, 3, 4, 5):
        for md in (1, 2):
            for mi in (3, 5, 10):
                pairs = [(detector.detect(text[(r["pack"], r["doc_id"])], mh, md, mi)["romanised"], r["d2"])
                         for r in rows]
                t, f, n, _, pr, re_ = scores(pairs)
                mark = " **(used)**" if (mh, md, mi) == (detector.MIN_HITS, detector.MIN_DISTINCT,
                                                         detector.MIN_IAST) else ""
                out.append(f"| {mh} | {md} | {mi} | {t + f} | {pr:.0%} | {re_:.0%}{mark} |")

    def line(r):
        d = r["det"]
        return (f"| {r['doc_id']} | {r['pack']} | {r['n_d2_marks']}/{r['n_readers']} | {d['hits']} ({d['distinct']}) "
                f"| {d['iast']} | {', '.join(d['examples']) or '-'} |")

    head = ["| doc_id | pack | D2 marks / readers | Indic words (distinct) | IAST | words matched |",
            "|---|---|---|---|---|---|"]
    misses = [r for r in rows if r["d2"] and not r["det"]["romanised"]]
    false = [r for r in rows if not r["d2"] and r["det"]["romanised"]]
    out += ["", f"## Missed (reader D2, not flagged): {len(misses)}", ""] + head + [line(r) for r in misses]
    out += ["", f"## False alarms (flagged, no reader D2): {len(false)}", ""] + head + [line(r) for r in false]
    a.out.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out[:14]))


if __name__ == "__main__":
    main()
