# indic_rules: Data B's Indic rules for spec v1

Task 1 of Data B's week 2 (#211). It hands Data B's Indic cleaning rules to Data A in their spec v1 rule form
(`teams/01-data-a/spec_v1/sheets/medicine_english.md`, PR #194), so they can go into `clean.py`.

| File | What it holds |
|---|---|
| `medicine_indic.md` | The 146 rules that are ready, in Data A's form and run order |
| `rules_status.md` | All 363 Indic medicines from the open diagnosis PRs, with the reason each one is in or not yet |
| `load_rules.py` | Reads the rules out of `medicine_indic.md`, so tests and `clean.py` use the sheet itself |

## Which rules are in
A rule is in when its author's `medicine.md` reports a pass on **its own pack's gold set at today's size**
(`teams/02-data-b/gold/gold_coverage.csv` on main, 2 Nov). TSAI (G2, 1 Nov): if a rule's harm result is still
missing at Wed 4 Nov, 23:59 IST, or was run on a set other than its own pack's gold, the rule stays out of spec v1.

## What each rule block holds
- The label card: `RULE_ID`, `CODE`, `ACTION`, `STAGE`, `STATUS`, `LANGS`, `ORIGIN`, `SOURCE`, `AUTHOR` (with the PR
  number and commit).
- The author's code, unchanged: every python block of their section, in order, exactly as `harm_test_indic.py` runs it.
- Lines marked `# added by Data B`: `import re` where the author relied on the harm tool providing it, `_std` (copied
  from Data A), and `medicine(doc)`. The guard in `medicine(doc)` runs a rule only on the pack it was tested on.

## Use
```python
from load_rules import load
for rule in load():                      # in run order
    action, text = rule.medicine(doc)    # doc = {doc_id, text, url, lang_label, pack_id}
```
The code in the sheet is run as code: read it first.

## Limits
- Harm results are as each author reports them. Data B has not re-run them, because the packs are not in the repository.
- The groups in `rules_status.md` are read from each author's own harm text. If you think your rule is in the wrong
  group, say so in this PR or in #211.
- 31 overlaps, where two authors wrote a rule for the same disease on the same pack, are listed at the top of
  `medicine_indic.md`. Both rules are kept, in run order.
- Rule IDs (`DB-<code>-<nnn>`) are provisional.

## Add or fix your rule
1. In your own diagnosis PR, give each medicine a `**Disease:** <code>` line and a python block with
   `medicine_<code>(text)`.
2. Run `teams/02-data-b/tools/harm_test_indic.py` on your pack's gold set and put its result in part 4.
3. Tell the rules owner in #211.
