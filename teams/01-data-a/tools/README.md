# Data A tools: harm test and hex check

Small scripts for the week-1 medicine work. They read pack data from your own
computer; no pack data, labels of other people or results go in this folder.

| Script | What it does |
| --- | --- |
| `harm_test.py` | Runs medicines on a gold set and reports, per medicine, how many gold documents it changes or drops (fails above 1%) and how many labelled cases it fixes |
| `extract_medicines.py` | Reads the runnable medicines out of `medicine.md` files (convention below) |
| `hexcheck.py` | For one or more doc_ids, lists only the unusual characters in the whole document (no 2,000-character limit), with a hint per character (A1 to A6), and G-group candidates: G1 word cut before a vowel sign or virama, G2 joiner not after a virama, G4 Latin digit inside an Indic number, and characters an NFKC step would change. For documents labelled with an Indic language, also G3 hints (traces of dropped text). Prints ready `hex` cells in the agreed format |

Requires Python 3.8+ and `pip install pyarrow`.

## Medicine convention

`MEDICINE_GUIDE.md` has the proposed common layout for every pack (code, English, maths,
science, Indic), the rules every medicine follows, and what a rule must never touch per domain.

So one script can test every student's medicines, end each medicine section in
`medicine.md` with one complete block in this shape:

````markdown
## Medicine 1: F1 personal emails

...rule in words, harm test, side effects...

```python medicine
import re
def medicine(text):          # always this name and signature
    ...
    return new_text, "fix"   # "keep" | "fix" | "drop"
```
````

The heading must start `## Medicine <N>: <CODE>` (the code from DISEASES.md). The spec v1
contract `def apply_rule(text, metadata)` returning `(new_text or None, dropped)` is accepted too. A section
without a block, or with code that does not run, is reported, not skipped silently.

**Loading a `medicine.md` runs its code.** Read other people's blocks before you run them.

## Usage

```
# unusual characters and G candidates, with hex cells in the agreed format
python hexcheck.py <pack>.parquet <doc_id> [<doc_id> ...]

# list the medicines a file defines
python extract_medicines.py diagnosis/submissions/<pack>/<handle>/medicine.md

# preliminary harm test: gold = your own rows marked full + clean
python harm_test.py <pack>.parquet diagnosis/submissions/<pack>/<handle>/labels.csv \
    --md diagnosis/submissions/<pack>/<handle>/medicine.md

# harm test on a team gold set: the doc_id,reader_1,reader_2 CSVs that build_gold.py writes
# to teams/01-data-a/gold/ (a plain one-id-per-line list also works); --md takes several files
python harm_test.py <pack>.parquet <labels.csv> --gold gold/<pack>.txt --md <medicine.md> [<medicine.md> ...]

```

`hexcheck.py` finds candidates only. G3 (Indic text dropped by an English-only step) has no
character to point at, so it gives hints instead: under half the letters in the labelled script,
three or more empty lines in a row, headings or list items with nothing after them, and text that
ends mid-sentence. G3 has no hex cell: put a short quote and the offset in `evidence`. A missing
joiner (G2) cannot be seen from the characters at all: judge that by reading. In an Indic document, the ordinary letters, signs
and digits of the document's own script are treated as normal and not listed.

The harm test needs the pack's text, so it runs per pack: each pack's readers run the
domain's medicines on their own pack's gold set and post the table.

## Example (cadj-commits, preliminary: 123 of the reader's own clean rows)

| Medicine | Gold changed | Harm | Result | Labelled cases fixed |
| --- | --- | --- | --- | --- |
| F1 emails and profile URLs | 1 | 0.8% | PASS | 23 of 23 |
| E4 licence headers | 0 | 0.0% | PASS | 3 of 4 |
| A2 carriage returns | 0 | 0.0% | PASS | 1 of 1 |
| A1 BOM at file start | 0 | 0.0% | PASS | 1 of 1 |

A deliberately careless test rule ("strip all HTML tags") changed 26 of the same 123
documents (21.1%, FAIL), including HTML that the code produces on purpose.
