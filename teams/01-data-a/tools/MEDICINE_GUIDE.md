# Medicine sheet guide (proposal for Data A)

One structure for every pack: code, English, maths, science and Indic. It keeps the five
parts of `diagnosis/templates/medicine_TEMPLATE.md`, follows the format the Data A tools read
(`medicine_extract.py`, `harm_test.py`, `rule_report.py`: see `tools/README.md`), and adds a
`Scope:` line and the reach next to the harm, so sheets can be compared.

## Sheet layout

````markdown
# Medicine sheet: <pack_id> (<github handle>)

Domain: <code | English | maths | science | hi | mr | ...>   Rows labelled: <N> of <total>

| Code | Documents | Occurrences | Medicine? |
| --- | --- | --- | --- |
| F1 | 31 | 54 | yes (Medicine 1) |
| A1 | 1 | 2 | no (five or fewer) |

Not found: <codes you checked for and did not see>
False triggers: <patterns that look like a disease but are not, e.g. Java @GeneratedValue is not E1>

## Medicine 1: <CODE> <short title>

Scope: <domains this rule may run on: all | code | hi, mr | ...>

1. **Disease:** <CODE>, count, three examples: `doc_id`: evidence
   (type + offset for F1 and E3; hex cell for A and G codes)
2. **Medicine:** the rule in words, then one self-contained Python block:

   ```python
   import re
   SETTING = "..."                # settings the team may change, at the top
   def cure_<code>(text):         # e.g. cure_f1; returns the new text
       ...
       return new_text            # to drop the document: return ("drop", "")
   ```

3. **Action:** fix (or drop), and why.
4. **Harm test:** gold set used (own clean rows N, or team gold file), changed, dropped, %,
   PASS or FAIL (limit 1%), and reach: labelled cases fixed, x of y.
5. **Side effects:** where the rule is wrong, and what it deliberately leaves alone.
````

## Rules for every medicine

1. Never write a personal data value or a secret into the sheet. Type and offset only.
2. Harm at most 1% on every gold set in the rule's scope, not only your own pack.
3. Standard library only (`re`, `unicodedata`); no network, no extra packages, no randomness.
   The same input always gives the same output.
4. Prefer fix over drop when the rest of the document is good. Drop only when the whole
   document is junk.
5. List what the rule must not touch in the side effects.
6. One medicine per disease. If two rules are needed for one code, give them separate sections.

## What differs by domain

| Domain | Typical medicines | A rule must never touch |
| --- | --- | --- |
| Code | F1 emails, E4 licence text, A2 CRLF, E1, E2, E3 | tabs, HTML or JSX inside code, `@` decorators, short licence notices, Unicode inside strings |
| English web | C1 boilerplate, B1 entities, B2 stray tags, C2 repeats, H2 near-duplicates, F1 | real Markdown and code blocks, curly quotes, accented names |
| Indic | A1 zero-width space and BOM, G1 rejoin a cut vowel sign, A5 NFC, D1 relabel | ZWJ and ZWNJ, nukta forms, Indic digits; never NFKC. D4 and D5 (translation quality) cannot be fixed by a regex: label them |
| Maths and science | B5 broken LaTeX, A3 mojibake, C1 PDF headers and footers, A5 NFC | LaTeX, Greek letters, superscripts and math symbols; never NFKC (it turns x² into x2) |

## Check before you submit

Each section needs a `**Disease:** <CODE>` line and an `**Action:** fix` (or `drop`) line, and
the function must be named `cure_<code>`. Then, with the Data A tools:

```
python -I teams/01-data-a/tools/medicine_extract.py diagnosis/submissions/<pack>/<handle>/medicine.md --out /tmp/rules.py
python -I teams/01-data-a/tools/harm_test.py --pack <pack>.parquet --gold teams/01-data-a/gold/<pack>_gold.csv \
    --rules /tmp/rules.py --rule <CODE>
```

Every medicine should be found by the extractor and pass. Put the numbers into part 4.
