# decisions_math: why each math rule was picked or not

Packs: `math-finemath` (gold 30), `math-megamath` (gold 18). Limit `max(1, floor(1% of gold))` = 1 document on both.
Inputs: every math diagnosis PR. finemath: SomaKorada07 #61 (labels and medicine), uz9ai #41 (labels). megamath: asraj
#146 (labels; its `medicine.md` is a copy of its `labels.csv`), mukund-23 #102 (labels), kunal2016 #151 (labels and medicine).
Gold built with `build_gold.py` from those labels, 30 Oct. Numbers in `medicine_math.md` are per pack, never pooled.

**Only two math sheets have rules.** SomaKorada07's finemath sheet describes 15 medicines with recall figures, examples
and side effects, but its python blocks are fragments that use names from her `medicines.py`, which is not in the repo,
so the extractor finds no function. kunal2016 wrote 10 of them as code, as close to her words as possible; they are the
finemath rules here, credited to her sheet. If her `medicines.py` arrives, her versions go in as new blocks (README rule 5).
kunal2016's megamath C5 drop is the only megamath medicine with code.

## Per disease

| code | rule(s) | packs | decision | why |
|---|---|---|---|---|
| A1 | `DA-A1-001` | finemath | keep | 14 of 15 labelled rows, 0 gold. megamath has no A1 rows, so it is off there. |
| A3 | `DA-A3-001` | both | keep | finemath 9/11, megamath 8/21, 0 gold. Runs first: a repaired run can hold an invisible character, which A1 then removes (on one finemath doc, A1 before A3 left a second clean() with work to do). |
| A5 | `DA-A5-001` | both | keep | finemath 6/6, megamath 9/12, 0 gold. Ligatures and fullwidth punctuation only; never full NFKC (x² must stay). |
| B2 | `DA-B2-001` | both | keep | finemath 3/8, megamath 6/112, 0 gold. Low recall on megamath: most of its B2 rows are tags inside documents that also hold code, which the rule skips on purpose. |
| B4 | `DA-B4-001` | both | keep | finemath 9/18, megamath 1/10, 0 gold. Does not touch `<EMAIL>`, the F1 tag. |
| B5 | `DA-B5-001` | both | keep | finemath 5/28, megamath 1/192, 0 gold. Most megamath B5 is formulas stripped by the scraper, which no rule can repair: those documents are `drop` by verdict. |
| C1 | `DA-C1-001` | both | keep | finemath 47/328, megamath 3/336, 0 gold. The phrase list is fitted to finemath sites; Soma's sheet reports 109 with her fuller list, which is not in the repo. |
| C2 | `DA-C2-001` | finemath | keep on finemath, off on megamath | finemath 39/187, 0 gold. On megamath it changes 1 of 18 gold docs: inside the limit, but it would use all of it, so the combined run could not take any other harm. |
| C3 | `DA-C3-001` (drop), `DA-C3-002` (fix) | finemath | keep, as two blocks of one medicine | The preview drop runs before C1, which would otherwise delete the banner it reads (12 finemath previews dropped). The teaser trim runs after the strips, which can leave a cut at the end. Off on megamath: there the trim was not idempotent on one doc. |
| C5 | `DA-C5-001` (drop), `DA-C5-002` (fix) | drop: megamath; fix: both | keep both | They fix different rows: the drop takes answers.com "related questions" pages (megamath 10, all labelled diseased by every reader who read them); the fix removes "See more:" and title-case keyword lines (finemath 5/51, megamath 2/168). Most C5 is whole SEO pages, which only a `drop` verdict handles. |
| F1 | shared `../tools/f1_rule.py` | both | via the prose path (separate draft PR) | One F1 for all families, per the README and the TSAI ruling. Its prose path is keyed by `pack_id` (`math-*`): finemath 0/30, megamath 0/18 gold. |
| C4, D4 | none | | no rule | Soma's sheet: a tested C4 rule caught 0 labelled cases and changed 2 clean docs; D4 (spun text) needs a language model. |
| A6, D3 | none yet | | waiting | In Soma's sheet (a 46-code symbol-font table; a foreign-script line rule), but their code is in `medicines.py`. |
| G3 | none | | open | megamath loses hyphens and minus signs pack-wide (`2^n1` for `2^n-1`). No rule can restore them; documents whose maths became wrong are `drop` by verdict. Needs a team decision on G3. |

## Combined

`harm_test.py --rules spec_v1/clean.py --rule all`: finemath 0/30, megamath 0/18 for every function and for ALL IN ORDER;
the same with disputed docs left in. `clean()` on the whole pack: finemath 122 fixed, 12 dropped, 366 kept; megamath 37
fixed, 10 dropped, 453 kept. A second `clean()` changes nothing on any doc of either pack.

## Open

- Both math packs carry `en`. `build_clean.py` maps a language tag to one family, so when the English sheet arrives with
  `en` the build will stop ("en is in two families"). The math rules already check `pack_id`; the build needs to route by
  `pack_id` too (a change to `build_clean.py`, for its owner).
- Gold is small (30 and 18): with 0 hits the harm rate is only shown to be below about 10% and 17%.
- Reviewer for all 12 rules.
