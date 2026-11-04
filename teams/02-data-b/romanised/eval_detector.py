#!/usr/bin/env python3
"""eval_detector.py - precision and recall of detector.py on testset_100.csv.

Two sets of labels are scored:
  reader   a document is D2 when at least one reader marked it D2
  checked  the reader label, corrected by checked_labels.csv where a second look found no romanised Indic phrase
           (English text, or only a proper name such as a film title or a scheme name)
Precision = how many of the detector's hits really are D2; recall = how many of the D2 documents it finds.
It also tries a few other thresholds, so the choice in detector.py can be checked, and lists every miss and false alarm.

Usage
  python3 eval_detector.py --testset testset_100.csv --checked checked_labels.csv --packs-dir packs --out eval_v1.md
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
    ap.add_argument("--checked", default="checked_labels.csv", type=Path)
    ap.add_argument("--packs-dir", default="packs", type=Path)
    ap.add_argument("--out", default="eval_v1.md", type=Path)
    a = ap.parse_args(argv)

    rows = list(csv.DictReader(open(a.testset, encoding="utf-8")))
    checked = {(r["pack"], r["doc_id"]): r for r in csv.DictReader(open(a.checked, encoding="utf-8"))}
    text = {}
    for pack in sorted({r["pack"] for r in rows}):
        for d in pq.read_table(a.packs_dir / f"{pack}.parquet", columns=["doc_id", "text"]).to_pylist():
            text[(pack, d["doc_id"])] = d["text"] or ""
    for r in rows:
        k = (r["pack"], r["doc_id"])
        r["reader"] = r["reader_label"] == "1"
        r["checked"] = checked[k]["checked_label"] == "1" if k in checked else r["reader"]
        r["why"] = checked[k]["reason"] if k in checked else ""
        r["det"] = detector.detect(text[k])

    out = ["# D2 detector on 100 labelled documents (v1)", "",
           f"Test set: `{a.testset.name}`, {len(rows)} documents: "
           f"{sum(r['reader'] for r in rows)} that a reader marked D2 and {sum(not r['reader'] for r in rows)} "
           "that no reader marked D2 (half of those chosen among documents with at least 10% Latin letters).",
           f"Checked labels: {len(checked)} reader D2 marks were looked at again and turned out to hold no romanised "
           "Indic phrase (`checked_labels.csv` gives the reason for each). No negative was changed.", "",
           f"Detector rule: at least {detector.MIN_HITS} romanised Indic words, {detector.MIN_DISTINCT} of them "
           f"different, or at least {detector.MIN_IAST} IAST letters (see `detector.py`).", "",
           "## Result", "",
           "| labels | D2 docs | flagged | true pos | false pos | missed | precision | recall |",
           "|---|---|---|---|---|---|---|---|"]
    for name in ("reader", "checked"):
        tp, fp, fn, tn, p, rc = scores([(r["det"]["romanised"], r[name]) for r in rows])
        out.append(f"| {name} | {tp + fn} | {tp + fp} | {tp} | {fp} | {fn} | {p:.0%} | {rc:.0%} |")

    out += ["", "## Other thresholds (checked labels)", "",
            "| min hits | min distinct | min IAST | flagged | precision | recall |", "|---|---|---|---|---|---|"]
    for mh in (2, 3, 4, 5):
        for md in (1, 2):
            for mi in (3, 5, 10):
                pairs = [(detector.detect(text[(r["pack"], r["doc_id"])], mh, md, mi)["romanised"], r["checked"])
                         for r in rows]
                tp, fp, fn, tn, p, rc = scores(pairs)
                mark = " **(used)**" if (mh, md, mi) == (detector.MIN_HITS, detector.MIN_DISTINCT,
                                                         detector.MIN_IAST) else ""
                out.append(f"| {mh} | {md} | {mi} | {tp + fp} | {p:.0%} | {rc:.0%}{mark} |")

    def line(r):
        d = r["det"]
        return (f"| {r['doc_id']} | {r['pack']} | {r['n_d2_marks']}/{r['n_readers']} | {d['hits']} ({d['distinct']}) "
                f"| {d['iast']} | {', '.join(d['examples']) or '-'} | {r['why'] or '-'} |")

    head = ["| doc_id | pack | D2 marks / readers | Indic words (distinct) | IAST | words matched | checked note |",
            "|---|---|---|---|---|---|---|"]
    misses = [r for r in rows if r["checked"] and not r["det"]["romanised"]]
    false = [r for r in rows if not r["checked"] and r["det"]["romanised"]]
    out += ["", f"## Missed (checked D2, not flagged): {len(misses)}", ""] + head + [line(r) for r in misses]
    out += ["", f"## False alarms (flagged, checked not D2): {len(false)}", ""] + head + [line(r) for r in false]
    out += ["", f"## Reader D2 marks set to 0 by the check: {len(checked)}", ""] + head + \
           [line(r) for r in rows if r["reader"] and not r["checked"]]
    a.out.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out[:16]))


if __name__ == "__main__":
    main()
