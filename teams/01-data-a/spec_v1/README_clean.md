# Running clean.py

How to build, test and run `clean.py`, the Spec v1 cleaner of Data A. Paths start at `teams/01-data-a/`.

`clean.py` holds the 68 rules of `specv1.md` and the shared F1 rule, `tools/f1_rule.py`. The rules come from four families, which together cover 13 packs. It has one function per disease code, 24 in all, and `clean(doc)`, which runs a document through every rule of its family in sheet order. At the top is `SCOPE`, a table of the packs each rule applies to. A rule runs only on its own packs, and its harm test uses only the gold sets of those packs.

`clean.py` is generated. Do not edit it: change `specv1.md` and rebuild (step 1).

`clean.py` is the only cleaner to run. `clean_english.py` and `scripts/clean_english.py`, made for the English family before `specv1.md`, are kept but not used: no script or test loads them. `run_clean_english.py` is kept so the old command still works; it runs `run_clean.py`.

## Contents

1. [What you need](#what-you-need)
2. [Quick start](#quick-start)
3. [Step 1: build clean.py](#step-1-build-cleanpy)
4. [Step 2: run the unit tests](#step-2-run-the-unit-tests)
5. [Step 3: clean a pack](#step-3-clean-a-pack)
6. [Step 4: run the harm tests](#step-4-run-the-harm-tests)
7. [Use clean.py from Python](#use-cleanpy-from-python)
8. [The 24 functions](#the-24-functions)
9. [Run order in each family](#run-order-in-each-family)
10. [The scope table](#the-scope-table)
11. [Troubleshooting](#troubleshooting)

## What you need

| what | why |
|---|---|
| Python 3.9 or later (tested on 3.12) | `functools.cache` |
| `pyarrow` | reads and writes the Parquet packs |
| `ftfy` | the English mojibake rule, `DA-A3-002` |
| `tree-sitter-language-pack` | the shared F1 on code: it looks for private details only inside comments and strings |
| `pytest` | the unit tests |
| the packs, `<pack_id>.parquet` | not in the repo; get your link from the lab plan sheet |
| a `g1-harm-test` checkout | only for step 4: it has `harm_test.py` (until PR 140 merges) and the gold sets |

```bash
pip install pyarrow ftfy tree-sitter-language-pack pytest
```

`clean.py` imports without `ftfy` and `tree-sitter-language-pack`. Without them, the rules that need them raise an error when they run. `run_clean.py` then reports those documents as errors (see [Troubleshooting](#troubleshooting)).

### The packs

| family | packs |
|---|---|
| code | `code-cpp`, `code-go`, `code-java`, `code-js-ts`, `code-python`, `code-rust` |
| english | `en-dclm`, `en-fineweb-edu`, `en-nemotroncc`, `en-nemotroncc-synth` |
| math | `math-finemath`, `math-megamath` |
| sci | `sci-finepdfs` |

A pack file must be named after its pack ID, for example `en-dclm.parquet`. It needs the columns `doc_id`, `text`, `url` and `lang_label`. The `pack_id` column may be missing: `run_clean.py` then takes the pack ID from the file name.

## Quick start

Run these from `teams/01-data-a/`:

```bash
python -I spec_v1/tools/build_clean.py
```

```bash
python -m pytest spec_v1/tests
```

```bash
python -I spec_v1/run_clean.py --pack <packs folder>/en-dclm.parquet --out out
```

```bash
python -I spec_v1/tools/make_harm_tests.py <g1-harm-test checkout> <packs folder>
```

## Step 1: build clean.py

```bash
python -I spec_v1/tools/build_clean.py
```

This reads `spec_v1/sheets/specv1.md` and writes `spec_v1/clean.py`. Use `--sheet` and `--out` to read or write somewhere else:

```bash
python -I spec_v1/tools/build_clean.py --sheet spec_v1/sheets/specv1.md --out /tmp/clean.py
```

**Rebuild after every change to `specv1.md` or `spec_v1/tools/f1_rule.py`.** The build gives the same file every time, and a unit test checks that `clean.py` matches a fresh build.

### What the build does

1. It finds each `## Medicine N — <family> / <code> / \`<ID>\`` section and its Python block.
2. It reads the block's packs: the `SPEC_PACKS` line, and for a math rule its `ORIGIN` packs as well (`PACKS = set(ORIGIN.split(", "))`). The rule's scope is the packs both allow.
3. It writes those packs into `SCOPE` at the top of `clean.py`, and points the block's `SPEC_PACKS` (and `PACKS`) at its `SCOPE` entry. So pack IDs are written in one place.
4. It puts each block in its own closure (`_<family>_<code>_<nnn>`), so helpers with the same name in two blocks do not clash. Two other changes are made to the blocks:
   - The `AUTHOR` line is dropped.
   - The code `DA-B4-009` rule no longer rewrites `<EMAIL>`, which is the F1 tag.
5. It adds `spec_v1/tools/f1_rule.py` as the shared F1, in `SCOPE` under the name `f1_rule.py`, for the code packs.
6. It writes the 24 disease-code functions, `RULES`, `_PIPELINES` (each family's rules in sheet order), `_FAMILY` (pack to family) and `clean()`.

### What it prints

One line for each docstring or verbose regex whose indentation changed, for example `DA-E1-001 code strings changed: 1 [...]`. These are expected: the indentation of a docstring or a verbose regex does not change what the rule does. The last line is the summary:

```
clean.py: rules 68 + shared F1 | code 24 rules on 6 packs, english 20 rules on 4 packs, math 12 rules on 2 packs, sci 12 rules on 1 packs | functions: 24
```

### When the build stops

It stops with an `AssertionError` that names the rule, and writes nothing, when:

- a section has no Python block, or more than one;
- the block's `RULE_ID` or `CODE` does not match its heading;
- two rules share an ID, or the sections are not numbered 1, 2, 3, ...;
- a block does not have exactly one `SPEC_PACKS` line, or its scope is empty;
- a block reads `pack_id` anywhere except its pack check;
- one pack belongs to two families;
- `DA-F1-005`, the instructor's F1 rule, is missing, not under F1, or not on all four English packs.

## Step 2: run the unit tests

```bash
python -m pytest spec_v1/tests
```

| file | what it tests |
|---|---|
| `test_functions.py` | Every one of the 24 functions, on every family that has a rule for it: a sick document it fixes or drops, and a clean document of each family that it keeps. It also checks that the table covers every function and family in `clean.py`, so a new rule cannot go untested. |
| `test_scope.py` | The scope table, on all 13 packs:<br>• every rule has one entry, and each pack is in one family;<br>• each family runs in sheet order;<br>• a rule acts on its own packs only, and nothing runs without a known `pack_id`;<br>• the build reproduces `clean.py` and stops on a bad scope. |
| `test_clean.py` | The code family in detail: a licence goes and the build tag stays, the shared F1 on prose and on code, and a second clean changes nothing. |
| `test_math.py` | The math family in detail, including the rules that apply to one math pack only. |
| `test_clean_english.py` | The English family in detail: sick documents and look-alikes for each code, ZWJ and ZWNJ kept, `DA-F1-005` on the English packs, and `clean()` equal to the English rules of `specv1.md`. |

Every text in the tests is made up. Some science rules act only on documents the reviewers listed, so those tests use the doc_ids named in `specv1.md`. Expect `471 passed, 5 skipped` without `tree-sitter-language-pack`: the 5 skipped tests are the shared F1 on code.

## Step 3: clean a pack

```bash
python -I spec_v1/run_clean.py --pack <packs folder>/en-dclm.parquet --out out
```

| option | meaning |
|---|---|
| `--pack` | The pack, a Parquet file named `<pack_id>.parquet`. |
| `--out` | The folder for the results (default `out`); it is made if missing. |

It reads only the pack, writes only to `--out`, and needs no network.

### What it writes

| file | what is in it |
|---|---|
| `out/<pack>_clean.parquet` | The documents that were kept, with their cleaned text and all their columns. A `pack_id` column is added if the pack had none. |
| `out/<pack>_summary.json` | IDs and counts only, no text: `pack`, `family`, `rows`, `actions` (keep / fix / drop), `errors` (doc_id and error type), `dropped` (doc_ids), `seconds`, `docs_per_second`. |

On this machine `en-dclm` took 12 seconds for 500 documents (437 kept, 54 fixed, 9 dropped) and `sci-finepdfs` took under a second.

`run_clean.py` exits with 0 when no rule raised and 1 when one did. A document whose rule raised is left out of `_clean.parquet`, and its doc_id is listed under `errors`. It also exits with 1 if the pack's `pack_id` column does not match its file name.

The cleaned Parquet holds document text. Keep it out of the repo: the packs are not in the repo, and pr-guard rejects files over 5 MB.

### All 13 packs

```bash
PACKS=<packs folder>
for p in code-cpp code-go code-java code-js-ts code-python code-rust en-dclm en-fineweb-edu en-nemotroncc en-nemotroncc-synth math-finemath math-megamath sci-finepdfs; do
  python -I spec_v1/run_clean.py --pack "$PACKS/$p.parquet" --out out || echo "$p: see out/${p}_summary.json"
done
```

## Step 4: run the harm tests

```bash
python -I spec_v1/tools/make_harm_tests.py <g1-harm-test checkout> <packs folder> [<another packs folder> ...]
```

| argument | meaning |
|---|---|
| `<g1-harm-test checkout>` | A checkout that has `teams/01-data-a/tools/harm_test.py` and `teams/01-data-a/gold/<pack>_gold.csv`. `harm_test.py` is imported as it is, never changed. |
| `<packs folder>` | One or more folders holding the packs; a pack is looked for in each. |
| `--out` | The report (default `spec_v1/results/cleaner/harm_tests.md`). |
| `--results` | The folder for the per-pack JSON reports (default `spec_v1/results/cleaner`). |

### What it tests on each pack

1. **Each rule alone,** but only a rule whose `SCOPE` entry includes this pack, on that pack's gold set.
2. **Each disease-code function,** on the packs where one of its rules applies.
3. **`clean()`,** on the gold set, and on the whole pack for the fixed and dropped counts.
4. **The scope table holds:** every rule that does not apply to the pack is run on the whole pack, past the scope check. It must change nothing, drop nothing and raise nothing.
5. **The cross-check:** the `clean()` gold result is compared with `results/cleaner/specv1_validation.json` when both used the same gold and pack. The code packs may differ, because `clean.py` adds the shared F1 and the `DA-B4-009` change.

### The limit

At most `max(1, floor(1% of gold))` gold documents changed or dropped, for each pack on its own; packs are never pooled.

- An empty gold set is NOT TESTABLE.
- An error is never a PASS.
- A rule passes only if it passes on every pack of its scope.

### What it writes

| file | what is in it |
|---|---|
| `spec_v1/results/cleaner/harm_tests.md` | Section 1: `clean()` per pack. Section 2: each rule alone, one table per family, with `·` where the rule does not apply. Section 3: each function per pack. Then the packs it could not run. |
| `spec_v1/results/cleaner/specv1_<pack>_harm.json` | The same per pack, with the affected gold doc_ids and the sha256 of the pack, the gold, `clean.py` and `harm_test.py`. No text. |

It exits with 0 when everything it ran passed. It exits with 1 when any result is not PASS, a gold set is empty, or a rule acted on a pack it does not apply to. A pack it cannot find is listed as not run and does not fail the run. So run it where all 13 packs and the current gold sets are, before you commit `harm_tests.md`.

## Use clean.py from Python

```python
import sys
sys.path.insert(0, "spec_v1")
import clean

doc = {"doc_id": "x", "text": "Some text.", "url": "", "lang_label": "en", "pack_id": "en-dclm"}
action, text = clean.clean(doc)          # the whole pipeline of the doc's family
action, text = clean.RULES["B4"](doc)    # one disease code: its rules for this pack, in sheet order
clean.SCOPE["DA-A1-005"]                 # frozenset({'math-finemath'})
clean._FAMILY["en-dclm"]                 # 'english'
```

- **`action`:** `"keep"`, `"fix"` or `"drop"`.
- **`text`:** the cleaned text after a fix. After a keep or a drop it is the original text.
- **The document:** never changed in place.
- **Without a known pack:** a document with no `pack_id`, or one that no family has, comes back as `("keep", text)`. Such a document is not eligible for release.

## The 24 functions

One function per disease code. Each runs the rules of that code that apply to the document's pack. `·` means the family has no rule for that code.

| function | code | english | math | sci |
|---|---|---|---|---|
| `a1` | `DA-A1-001` | `DA-A1-004` | `DA-A1-005` | `DA-A1-006` |
| `a2` | `DA-A2-007` | `DA-A2-008` | · | · |
| `a6` | `DA-A6-001` | · | · | `DA-A6-002` |
| `a4` | `DA-A4-002`, `DA-A4-003` | · | · | · |
| `a5` | · | `DA-A5-001` | `DA-A5-002` | · |
| `a3` | · | `DA-A3-002` | `DA-A3-001` | · |
| `b1` | · | `DA-B1-002` | · | · |
| `b2` | · | `DA-B2-002` | `DA-B2-001` | `DA-B2-003` |
| `b5` | · | · | `DA-B5-001` | `DA-B5-002` |
| `b3` | `DA-B3-001` | · | · | · |
| `e1` | `DA-E1-001`, `DA-E1-004`, `DA-E1-008`, `DA-E1-006`, `DA-E1-005`, `DA-E1-007` | · | · | · |
| `e2` | `DA-E2-001` | · | · | · |
| `c3` | `DA-C3-002` | `DA-C3-001`, `DA-C3-003` | `DA-C3-004`, `DA-C3-005` | `DA-C3-006` |
| `c4` | `DA-C4-002` | · | · | `DA-C4-003` |
| `c5` | · | `DA-C5-002`, `DA-C5-005` | `DA-C5-001`, `DA-C5-006` | · |
| `d4` | · | `DA-D4-001` | · | · |
| `e4` | `DA-E4-005`, `DA-E4-010`, `DA-E4-009`, `DA-E4-007` | · | · | · |
| `c1` | `DA-C1-004`, `DA-C1-005` | `DA-C1-006` | `DA-C1-001` | `DA-C1-007` |
| `c2` | · | `DA-C2-003` | `DA-C2-001` | `DA-C2-004` |
| `d1` | · | · | · | `DA-D1-001` |
| `d3` | · | `DA-D3-003` | · | `DA-D3-004` |
| `b4` | `DA-B4-009` | `DA-B4-007`, `DA-B4-008`, `DA-B4-012`, `DA-B4-010`, `DA-B4-011` | `DA-B4-001` | `DA-B4-013` |
| `e3` | `DA-E3-003`, `DA-E3-004` | · | · | · |
| `f1` | `f1_rule.py` (shared) | `DA-F1-005` | · | `DA-F1-006` |

`RULES` maps each code to its function in the order above. `harm_test.py --rules spec_v1/clean.py --rule all` runs them in that order. That order is not a family's run order: use `clean()` for the real pipeline.

## Run order in each family

`clean()` runs these in order. A drop ends the document, and a fix passes the new text to the next rule. The code family then runs the shared F1 last.

| family | order |
|---|---|
| code | A1-001, A2-007, A6-001, A4-002, A4-003, B3-001, E1-001, E1-004, E1-008, E1-006, E1-005, E1-007, E2-001, C3-002, C4-002, E4-005, E4-010, E4-009, E4-007, C1-004, C1-005, B4-009, E3-003, E3-004, then the shared F1 |
| english | A1-004, A2-008, A5-001, A3-002, B1-002, B2-002, C3-001, C3-003, C5-002, D4-001, C1-006, C2-003, C5-005, D3-003, B4-007, B4-008, B4-012, B4-010, B4-011, F1-005 |
| math | A3-001, A1-005, A5-002, B2-001, B4-001, B5-001, C5-001, C3-004, C1-001, C2-001, C5-006, C3-005 |
| sci | B4-013, B2-003, B5-002, A1-006, A6-002, C1-007, C2-004, C3-006, C4-003, D1-001, F1-006, D3-004 |

## The scope table

```python
SCOPE = {
    "DA-A1-001": frozenset({"code-cpp", "code-go", "code-java", "code-js-ts", "code-python", "code-rust"}),  # code A1, medicine 1
    ...
    "DA-A1-005": frozenset({"math-finemath"}),  # math A1, medicine 46
    ...
    "f1_rule.py": frozenset({"code-cpp", "code-go", "code-java", "code-js-ts", "code-python", "code-rust"}),  # the shared F1
}
```

Each rule applies to every pack of its family, except for five math rules whose `ORIGIN` names one math pack:

| packs | rules |
|---|---|
| `math-finemath` only | `DA-A1-005`, `DA-C2-001`, `DA-C3-004`, `DA-C3-005` |
| `math-megamath` only | `DA-C5-001` |

The scope is checked twice, and both checks read `SCOPE`:

- `_run` skips a rule whose `SCOPE` entry does not hold the document's `pack_id`.
- Each rule's own pack check reads its `SCOPE` entry.

**To change a rule's packs,** do these in order:

1. Edit its `SPEC_PACKS` line in `specv1.md`. For a math rule, edit `ORIGIN` too.
2. Rebuild (step 1).
3. Run the unit tests (step 2).
4. Run the harm tests (step 4).

## Troubleshooting

| what you see | why | what to do |
|---|---|---|
| `run_clean.py` keeps every document, and the summary says `"family": null` | The pack ID is not one of the 13: the file was renamed and has no `pack_id` column. | Name the file `<pack_id>.parquet`. |
| `<file>: doc_id ... has pack_id '...'` and exit code 1 | The pack's `pack_id` column does not match its file name. | Rename the file to the pack ID in the column. |
| `errors` lists `ModuleNotFoundError` on English documents | `ftfy` is not installed (`DA-A3-002`). | `pip install ftfy` |
| `errors` lists `ModuleNotFoundError` on code documents | `tree-sitter-language-pack` is not installed. The shared F1 needs it when it finds an email, phone or address in code. | `pip install tree-sitter-language-pack` |
| `ModuleNotFoundError: No module named 'harm_test'` | The first argument of `make_harm_tests.py` is not a `g1-harm-test` checkout. | Pass the checkout's root folder. |
| `harm_tests.md` lists packs as "pack not on this machine" | The pack is in none of the folders you passed. | Pass every folder that holds packs. |
| `harm_tests.md` says "other snapshot" | Your gold set or pack is not the one `specv1_validation.json` used, so the two are not compared. | Use the current gold sets. |
| `AssertionError` from `build_clean.py` | The sheet breaks one of the checks under [When the build stops](#when-the-build-stops). | Fix the rule the message names, and rebuild. |
| `test_the_build_writes_this_clean_py` fails | `specv1.md` or `f1_rule.py` changed after the last build. | Rebuild (step 1). |

## What not to do

- Do not edit `clean.py`. It is generated.
- Do not commit a `harm_tests.md` made without all 13 packs.
- Do not commit packs or `_clean.parquet` outputs.
- Do not take a rule off a pack to make a harm test pass. A failing rule stays in, and blocks release until it is reviewed, as `specv1.md` says.
