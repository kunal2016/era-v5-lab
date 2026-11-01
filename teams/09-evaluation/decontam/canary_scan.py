"""Scan documents for canary strings (G9).

    python canary_scan.py shard.parquet                      # Parquet with doc_id and text columns
    python canary_scan.py docs.jsonl --id-field id            # one JSON object per line
    python canary_scan.py some/folder                         # every .parquet .jsonl .json .txt .md below it
    python canary_scan.py shard.parquet --canary "my string"  # also look for an extra string

It looks for the lab canary (canary.py) and for every benchmark canary in the fingerprint set
(<benchmark>/canaries.txt, for example GPQA and HLE). A match is exact: one occurrence is a leak.
It does not load the fingerprints, so it is fast. The full check is still decontam_check.py.

Output: one JSON line per occurrence, with only the canary, the document ID and the offset
(character offset in the document text). It never prints document text.
The summary goes to stderr. Exit code 0: no canary found. 1: a canary was found.
"""

import argparse
import json
import sys
from pathlib import Path

from canary import find, load_canaries
from decontam_check import DEFAULT_SET, read_docs

SUFFIXES = {".parquet", ".jsonl", ".json", ".txt", ".md"}


def expand(inputs):
    """Files as given; a folder gives its files with a known suffix, sorted."""
    for p in map(Path, inputs):
        if p.is_dir():
            yield from sorted(str(f) for f in p.rglob("*") if f.is_file() and f.suffix in SUFFIXES)
        else:
            yield str(p)


def scan(paths, canaries, id_field="doc_id", text_field="text"):
    """Yield (doc_id, [(offset, canary), ...]) for every document, also when it has no hit."""
    for doc_id, text in read_docs(paths, id_field, text_field):
        yield doc_id, find(text, canaries)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="Parquet, JSONL or text files, or folders")
    ap.add_argument("--id-field", default="doc_id")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--fingerprints", default=str(DEFAULT_SET),
                    help="fingerprint set folder for the benchmark canaries (default: the shipped set)")
    ap.add_argument("--canary", action="append", default=[], metavar="STRING", help="an extra string to look for")
    args = ap.parse_args(argv)

    canaries = load_canaries(args.fingerprints)
    for c in args.canary:
        canaries.setdefault(c, "extra")
    sources = sorted(set(canaries.values()))
    print(f"canaries {len(canaries)} from {', '.join(sources)}", file=sys.stderr)

    n_docs = n_with = n_hits = 0
    for doc_id, hits in scan(list(expand(args.inputs)), canaries, args.id_field, args.text_field):
        n_docs += 1
        if hits:
            n_with += 1
            n_hits += len(hits)
        for offset, c in hits:
            print(json.dumps({"canary": c, "doc_id": doc_id, "offset": offset}, ensure_ascii=False))
    print(f"docs {n_docs} with_canary {n_with} hits {n_hits}", file=sys.stderr)
    return 1 if n_hits else 0


if __name__ == "__main__":
    sys.exit(main())
