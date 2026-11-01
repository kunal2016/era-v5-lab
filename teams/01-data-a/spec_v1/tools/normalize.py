"""A standard copy of a text, for comparing and matching: match_key(text) and line_keys(text). It never changes a
document: a rule compares keys, and the document keeps its own text, so nothing is fixed or dropped by this file.

  python -I normalize.py --pack <pack>.parquet [--show 5]

prints how many documents of a pack each step would even out, with a few doc_ids. IDs and counts only, never text.

The diseases of diagnosis/DISEASES.md that the key evens out, in this order:
  B1     HTML entities          &amp; &nbsp; &#2361; are decoded
  A2     control characters     \\r\\n and \\r become \\n; U+0000-001F (but tab and newline) and U+007F-009F go
  A1     invisible junk         zero-width space, BOM, soft hyphen and the bidi marks U+202A-202E, U+2066-2069 go.
                                ZWJ U+200D and ZWNJ U+200C stay: in Indic text they are part of the script
  case                          lower case (Latin, Greek, Cyrillic: Indic scripts have no case)
  A5     normal form            NFC, the form DISEASES.md names
  space                         runs of spaces and tabs become one space; match_key also joins the lines

What it never does, so it cannot cause the damage of DISEASES.md section G: no NFKC (G4: x² stays x², ﬁ stays ﬁ),
no Indic digit turned Latin (G4), no ZWJ or ZWNJ removed (G2), no vowel sign or virama split from its letter (G1).
Rules that find a disease by comparing text can compare keys: C1 boilerplate phrases, C2 repeated lines, E4 licence
headers, H1 and H2 duplicates.
"""
import argparse, html, re, sys, unicodedata
from collections import Counter

_INVISIBLE = re.compile("[​﻿­‪-‮⁦-⁩]")  # A1 as DISEASES.md lists it: not ZWJ or ZWNJ
_CONTROL = re.compile("[\x00-\x08\x0b-\x1f\x7f-\x9f]")  # A2: every C0 and C1 control but tab (09) and newline (0a)
_SPACE = re.compile(r"[^\S\n]+")  # spaces, tabs and no-break spaces, not newlines
STEPS = ("B1", "A2", "A1", "case", "A5", "space")


def steps(text):
    """Each step and the text after it, in order. The last text is the key with its lines kept."""
    t = html.unescape(text)
    yield "B1", t
    t = _CONTROL.sub("", t.replace("\r\n", "\n").replace("\r", "\n"))
    yield "A2", t
    t = _INVISIBLE.sub("", t)
    yield "A1", t
    t = t.lower()  # not casefold(): that also turns the ligature ﬁ into fi and ß into ss, which is NFKC's kind of change
    yield "case", t
    t = unicodedata.normalize("NFC", t)
    yield "A5", t
    t = "\n".join(_SPACE.sub(" ", line).strip() for line in t.split("\n"))
    yield "space", t


def line_keys(text):
    """One key per line, for rules that compare lines (C1, C2, E4)."""
    for _, t in steps(text):
        pass
    return t.split("\n")


def match_key(text):
    """One key for the whole text, for rules that compare documents or passages (H1, H2)."""
    return " ".join(k for k in line_keys(text) if k)


def explain(text):
    """The steps that change this text, in order: which diseases its key evens out."""
    out, before = [], text
    for name, after in steps(text):
        if after != before:
            out.append(name)
        before = after
    return out


def main():
    import pyarrow.parquet as pq
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--show", type=int, default=5, help="how many doc_ids to list for each step")
    args = ap.parse_args()
    rows = pq.read_table(args.pack, columns=["doc_id", "text"]).to_pylist()
    hit, ids = Counter(), {s: [] for s in STEPS}
    for r in rows:
        for name in explain(r["text"]):
            hit[name] += 1
            if len(ids[name]) < args.show:
                ids[name].append(r["doc_id"])
    print(f"{args.pack}: {len(rows)} documents. Each line: documents whose key this step changes (the documents are not changed)")
    for name in STEPS:
        print(f"  {name:6} {hit[name]:5}  {', '.join(ids[name])}")


if __name__ == "__main__":
    sys.exit(main())
