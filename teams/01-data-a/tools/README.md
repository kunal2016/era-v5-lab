# Data A tools: harm test and gold sets

Three small scripts for the week-1 medicine work. They read pack data from your own
computer; no pack data, labels of other people or results go in this folder.

| Script | What it does |
| --- | --- |
| `harm_test.py` | Runs medicines on a gold set and reports, per medicine, how many gold documents it changes or drops (fails above 1%) and how many labelled cases it fixes |
| `extract_medicines.py` | Reads the runnable medicines out of `medicine.md` files (convention below) |
| `build_gold.py` | Builds a gold set per pack from two or more readers' `labels.csv`: documents that at least two readers read in `full` and marked `clean`. Also reports reader agreement |

Requires Python 3.8+ and `pip install pyarrow`.

## Medicine convention

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

The heading must start `## Medicine <N>: <CODE>` (the code from DISEASES.md). A section
without a block, or with code that does not run, is reported, not skipped silently.

**Loading a `medicine.md` runs its code.** Read other people's blocks before you run them.

## Usage

```
# list the medicines a file defines
python extract_medicines.py diagnosis/submissions/<pack>/<handle>/medicine.md

# preliminary harm test: gold = your own rows marked full + clean
python harm_test.py <pack>.parquet diagnosis/submissions/<pack>/<handle>/labels.csv \
    --md diagnosis/submissions/<pack>/<handle>/medicine.md

# harm test on a team gold set (one doc_id per line); --md takes several files
python harm_test.py <pack>.parquet <labels.csv> --gold gold/<pack>.txt --md <medicine.md> [<medicine.md> ...]

# gold sets from all readers' labels: <root>/<pack_id>/<handle>/labels.csv
python build_gold.py diagnosis/submissions --out gold
```

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
