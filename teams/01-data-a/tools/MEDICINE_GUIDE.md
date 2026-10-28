# Medicine sheet guide (proposal for Data A)

One structure for every pack: code, English, maths, science and Indic. It keeps the five
parts of `diagnosis/templates/medicine_TEMPLATE.md` and adds three things so that sheets can
be compared and tested by one script: a `Scope:` line, a runnable `python medicine` block, and
the reach next to the harm.

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

1. **Disease:** code, count, three examples: `doc_id`: evidence
   (type + offset for F1 and E3; hex cell for A and G codes)
2. **Medicine:** the rule in words, then one self-contained block:

   ```python medicine
   import re
   SETTING = "..."                # settings the team may change, at the top
   def medicine(text):
       ...
       return new_text, "fix"     # "keep" | "fix" | "drop"
   ```

3. **Action:** fix or drop, and why.
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

```
python teams/01-data-a/tools/extract_medicines.py diagnosis/submissions/<pack>/<handle>/medicine.md
python teams/01-data-a/tools/harm_test.py <pack>.parquet diagnosis/submissions/<pack>/<handle>/labels.csv \
    --md diagnosis/submissions/<pack>/<handle>/medicine.md
```

Every medicine should load (`OK`) and pass. Put the numbers the harm test prints into part 4.
