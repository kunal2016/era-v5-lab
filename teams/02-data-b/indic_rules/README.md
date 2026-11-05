# indic_rules: Data B's Indic rules for spec v1

Task 1 of Data B's week 2 (#211). It hands Data B's Indic cleaning rules to Data A in their spec v1 rule form
(`teams/01-data-a/spec_v1/sheets/medicine_english.md`, PR #194), so they can go into `clean.py`.

| File | What it holds |
|---|---|
| `medicine_indic.md` | The 267 rules that are ready, in Data A's form and run order |
| `rules_status.md` | All 373 Indic medicines from the open diagnosis PRs, with the reason each one is in or not yet |
| `load_rules.py` | Reads the rules out of `medicine_indic.md`, so tests and `clean.py` use the sheet itself |
| `test_indic_rules.py` | 7 checks on every rule, with made-up text |
| `rewrites/` | Medicine sheets the harm tool could not read, rewritten in its format under TSAI's ruling 3 on #211. A rewrite's passing rules join once its author OKs it in their own PR (#46, #70 and #112 have; #58 and #83 have not, so theirs wait for the next spec) |

## Which rules are in
A rule is in when it passes the harm test on **its own pack's gold set at today's size**: the gold sets rebuilt on
3 Nov (#222, main `ea7b533`; `teams/02-data-b` is the same on `195f4ff`), unchanged on main since. TSAI (#240, 4 Nov
17:47 IST): only a result on today's gold counts.
- 198 rules: re-run on today's gold set and passed: 143 by Mallikarjun, 38 by the Data B rules owner, 7 by Shankar,
  and 10 by the author of #91 (the author's own run, written in words, not the tool's output). Each result is linked in its rule.
- 52 rules: the author's own `medicine.md` reports a pass on today's gold set.
- 17 rules: Data B's rewrites of #70 (10), #112 (5) and #46 (2), run on today's gold set and OK'd by their authors.

From the 262 published on 4 Nov: 262 − 5 out (2 that add a ZWJ, #63 F1, 2 F2) + 2 (#46) + 5 (#112) + 1 (#30 A6)
+ 1 (#256 C1) + 1 (#177 C1) = 267. #45's 15 rules stay in: Mallikarjun's run before the cut-off said "15 PASS" (#240),
and the Data B rules owner's run of 5 Nov gives the table.

**Out of spec v1, by TSAI's rulings of 4 Nov** (each is in `rules_status.md` with its reason):
- Rules that add a ZWJ by design (TSAI, G2 4 Nov 14:20 IST: for v1 the Gate 2 joiner check stays): `DB-G2-001` (#64),
  `DB-G2-002` (#138), and the G2 rules of #30 and #112. Held for v2.
- A rule that fails on today's gold: `DB-F1-005` (#63 F1, changes 2 of 114).
- Rules that need benchmark text to run, which the eval firewall keeps out of the repo: `DB-F2-001` (#45), `DB-F2-002` (#80).
  They wait for the next spec.

**Waiting on one condition:** #177's C6 (repeated dots) passes on today's gold (1 of 18, inside the limit of 1). TSAI
(G2, 5 Nov): it goes into spec v1 as a new code once the code owner approves #177 after the label fixes.

Rule IDs never change once published (`DB-<code>-<nnn>`); new rules take the next free number, and a rule that leaves
the sheet keeps its ID in the registry. TSAI (G2, 1 Nov): if a rule's harm result is still missing at Wed 4 Nov,
23:59 IST, or was run on a set other than its own pack's gold, the rule stays out of spec v1; it is not rejected, it
waits for the next spec.

## What each rule block holds
- The label card: `RULE_ID`, `CODE`, `ACTION`, `STAGE`, `STATUS`, `LANGS`, `ORIGIN`, `SOURCE`, `AUTHOR` (with the PR
  number and commit).
- The author's code, unchanged: every python block of their section, in order, exactly as `harm_test_indic.py` runs it.
- Lines marked `# added by Data B`: `import re` where the author relied on the harm tool providing it, `_std` (copied
  from Data A), and `medicine(doc)`. The guard in `medicine(doc)` runs a rule only on the pack it was tested on.
- `ACTION` is checked against the code (Shankar's review, 4 Nov). A rule whose function can return True drops the
  document, so a rule its author called "fix" is labelled `drop` or `fix+drop`. A `keep` rule's `medicine(doc)` always
  returns `("keep", text)`. D3 is a label only (TSAI, 31 Oct), so a D3 rule is `keep`. `DB-D4-011` also gets the page
  URL, so its host check runs; every other rule gets the text only, as the harm tool tested it.

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
| 4 | ZWJ, ZWNJ | a word it keeps loses or gains a ZWJ (U+200D) or ZWNJ (U+200C). Deleting a whole repeated sentence or junk line, joiners and all, is allowed |
| 5 | NFC | a fixed document is no longer NFC, or loses a compatibility character from the text it should keep (NFKC) |
| 6 | Nukta | a fixed document has a different number of nukta signs (counted after NFD) |
| 7 | Second run | running the rule again on its output changes it again |

**Result on 5 Nov 2026, all 267 rules: 267 pass, 0 fail, 0 skipped.** (On 4 Nov `DB-F2-001` was skipped because it needs
the Itihasa test set; it is now out of spec v1.) The test was checked on 8 made-up rules, 5 of them broken on purpose (check 2; check 4 twice,
a joiner removed and a joiner added; check 5; check 7): it caught all 5 and passed the 3 good ones, one of which deletes
a repeated sentence that holds joiners.

Check 4 changed on 4 Nov. It used to compare the joiner count of the whole document, so `DB-C2-020` (#30, which deletes a
repeated sentence) failed on the test text: the made-up clean document repeats its sentence, and deleting the copy took
its joiners with it. It now looks at the words the rule keeps.

**What this does not show:** 59 of the 267 rules acted on the test text. The other 208 found nothing to fix in it,
because each targets something of its own pack, so checks 4 to 7 had nothing to test for them. For real text, the
joiner and normal-form audit is part of each author's harm run on their pack's gold set (`harm_test_indic.py`).

## Limits
- For 52 rules, the harm result is as the author reports it, on today's gold set; 198 were re-run on today's gold on
  3 to 5 Nov, and each says who ran it. Data A's integration check re-runs every rule on the current gold.
- **Our mistake, fixed 5 Nov:** up to 4 Nov this README and the sheet said the authors' results were on "the gold of
  2 Nov", but the sizes we checked them against were those of 31 Oct (Shankar found it on #240). Every rule now has a
  result at today's size.
- A pass on a small gold set is weak: 0 changed of n shows only that the rule harms fewer than about 3 in n clean
  documents. Telugu's three packs hold 60 gold documents in all (18, 24 and 18), so a Telugu pass shows harm under 12 to 17%.
- Three rules pass right at the limit: `DB-C1-024` (#256) changes 2 of 244 (limit 2), `DB-C4-010` (#45) 1 of 71 and
  `DB-C2-006` (#63) 1 of 114 (limit 1). Five more change 1 gold document, under their limit of 2 or 4.
- The groups in `rules_status.md` are read from each author's own harm text, or from a re-run on today's gold. If you
  think your rule is in the wrong group, say so in this PR or in #211.
- 76 overlaps, where two or more authors wrote a rule for the same disease on the same pack, are listed at the top of
  `medicine_indic.md`. All are kept, in run order.
- Rule IDs (`DB-<code>-<nnn>`) never change once published; a new rule takes the next free number.

## Add or fix your rule
1. In your own diagnosis PR, give each medicine a `**Disease:** <code>` line and a python block with
   `medicine_<code>(text)`.
2. Run `teams/02-data-b/tools/harm_test_indic.py` on your pack's gold set and put its result in part 4.
3. Tell the rules owner in #211.
