# indic_rules: Data B's Indic rules for spec v1

Task 1 of Data B's week 2 (#211). It hands Data B's Indic cleaning rules to Data A in their spec v1 rule form
(`teams/01-data-a/spec_v1/sheets/medicine_english.md`, PR #194), so they can go into `clean.py`.

| File | What it holds |
|---|---|
| `medicine_indic.md` | The 229 rules that are ready, in Data A's form and run order |
| `rules_status.md` | All 366 Indic medicines from the open diagnosis PRs, with the reason each one is in or not yet |
| `load_rules.py` | Reads the rules out of `medicine_indic.md`, so tests and `clean.py` use the sheet itself |
| `test_indic_rules.py` | 7 checks on every rule, with made-up text |
| `rewrites/` | Medicine sheets the harm tool could not read, rewritten in its format under TSAI's ruling 3 on #211. Each one waits for its author's OK in their own PR and for its harm test on today's gold set |

## Which rules are in
A rule is in when it passes the harm test on **its own pack's gold set**: either its author's `medicine.md` reports a pass
on the gold set of 2 Nov (176 rules), or it was re-run on the gold set rebuilt on 3 Nov (#222, main `ea7b533`) and
passed (53 rules, by the Data B rules owner and Mallikarjun, as TSAI allows; each result is linked in its rule).
Rule IDs never change once published (`DB-<code>-<nnn>`); new rules take the next free number. TSAI (G2, 1 Nov): if a rule's harm result is still
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

## Tests
```
python -I test_indic_rules.py        # or: python -m pytest test_indic_rules.py
```
For each rule it makes two made-up documents in the rule's language: a clean one and one with junk (boilerplate,
HTML, mojibake, a made-up email). Joiners are written as `‍` and `‌`. It checks:

| # | Check | A rule fails when |
|---|---|---|
| 1 | Loads | its block does not run on its own |
| 2 | Other packs | it changes a document of another pack |
| 3 | Result form | it returns anything but `("keep" \| "fix" \| "drop", text)` |
| 4 | ZWJ, ZWNJ | a fixed document has a different number of ZWJ (U+200D) or ZWNJ (U+200C) |
| 5 | NFC | a fixed document is no longer NFC, or loses a compatibility character from the text it should keep (NFKC) |
| 6 | Nukta | a fixed document has a different number of nukta signs (counted after NFD) |
| 7 | Second run | running the rule again on its output changes it again |

**Result on 3 Nov 2026, all 229 rules: 228 pass, 0 fail, 1 skipped.** `DB-F2-001` is skipped because it needs the Itihasa test set,
which is not in the repo. The test was first checked on 6 made-up rules, 4 of them broken on purpose (one per check
2, 4, 5 and 7): it caught all 4 and passed the 2 good ones.

**What this does not show:** 55 of the 229 rules acted on the test text. The other 174 found nothing to fix in it,
because each targets something of its own pack, so checks 4 to 7 had nothing to test for them. For real text, the
joiner and normal-form audit is part of each author's harm run on their pack's gold set (`harm_test_indic.py`).

## Limits
- For 176 rules, the harm result is as the author reports it, on the gold sets of 2 Nov; the gold sets were rebuilt on 3 Nov, and Data A's integration check re-runs every rule on the current gold. 53 rules were re-run on 3 Nov on today's gold, and each says who ran it.
- The groups in `rules_status.md` are read from each author's own harm text. If you think your rule is in the wrong
  group, say so in this PR or in #211.
- 31 overlaps, where two authors wrote a rule for the same disease on the same pack, are listed at the top of
  `medicine_indic.md`. Both rules are kept, in run order.
- Rule IDs (`DB-<code>-<nnn>`) never change once published; a new rule takes the next free number.

## Add or fix your rule
1. In your own diagnosis PR, give each medicine a `**Disease:** <code>` line and a python block with
   `medicine_<code>(text)`.
2. Run `teams/02-data-b/tools/harm_test_indic.py` on your pack's gold set and put its result in part 4.
3. Tell the rules owner in #211.
