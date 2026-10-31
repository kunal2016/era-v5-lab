# decisions_math: why each math rule was picked or not

Packs: `math-finemath` (gold 30), `math-megamath` (gold 18). Limit `max(1, floor(1% of gold))` = 1 document on both.
Inputs: every math diagnosis PR. finemath: SomaKorada07 #61 (labels and medicine), uz9ai #41 (labels). megamath: asraj
#146 (labels; its `medicine.md` is a copy of its `labels.csv`), mukund-23 #102 (labels), kunal2016 #151 (labels and medicine).
Gold built with `build_gold.py` from those labels, 30 Oct. Numbers in `medicine_math.md` are per pack, never pooled.

**v1.1: the finemath rules are SomaKorada07's own functions.** In v1 her sheet (#61) described the medicines in words and
fragments, so kunal2016 wrote them as code. On 31 Oct she reviewed those rewrites on #19 and put every medicine in #61 as a
complete `medicine_<code>(text)` function (commit `cc74c7e`), each matching her `medicines.py` on the 500-doc pack. v1.1
copies her functions unchanged (rule fields, the `pack_id` guard and `\u` escapes for non-ASCII characters added) and
adds her A6 and D3. Her F1 is not used: F1 is the one shared rule. kunal2016's megamath C5 drop is unchanged.

## Per disease

| code | rule(s) | packs | decision | why |
|---|---|---|---|---|
| A3 | `DA-A3-001` | both | keep | finemath 10/11 (v1: 9; her cp866 repair and the extra lead characters), megamath 8/21, 0 gold. Runs first: a repaired run can hold an invisible character, which A1 then removes. |
| A1 | `DA-A1-001` | finemath | keep | 14 of 15 labelled rows, 0 gold. megamath has no A1 rows. |
| A6 | `DA-A6-001` | finemath | keep (new) | finemath 5/9, 0 gold: the Symbol-font map for 46 codes. Changes nothing on megamath, so it is off there. |
| A5 | `DA-A5-001` | both | keep | finemath 6/6, megamath 9/12, 0 gold. Ligatures and fullwidth punctuation only; never full NFKC (x² must stay). |
| B2 | `DA-B2-001` | both | keep | finemath 3/8, megamath 6/112, 0 gold. Skips documents that hold code; most megamath B2 rows do. |
| B4 | `DA-B4-001` | both | keep | finemath 9/18, megamath 1/10, 0 gold. Leaves `<EMAIL>`, the F1 tag. |
| B5 | `DA-B5-001` | both | keep | finemath 5/28 (7 docs changed: case-insensitive BBCode), megamath 1/192, 0 gold. Formulas stripped by the scraper cannot be repaired; those documents are `drop` by verdict. |
| C5 | `DA-C5-001` (drop), `DA-C5-002` (fix) | drop: megamath; fix: both | keep both | They fix different rows: the drop takes answers.com "related questions" pages (megamath 10); the fix removes "See more:" and title-case keyword lines (finemath 5/51, megamath 2/168). |
| D3 | `DA-D3-001` | both | keep (new) | finemath 5/10, megamath 2/9, 0 gold. Removes lines that are mostly Cyrillic, Indic, CJK, kana, Hangul or Arabic; drops a page where those hold over 30% of the letters. Greek is left alone: it is maths. |
| C3 | `DA-C3-001` (drop), `DA-C3-002` (fix) | finemath | keep, as two blocks of one medicine | The preview drop runs before C1, which would otherwise delete the banner it reads; the teaser trim runs after the strips. Off on megamath: there the trim is not idempotent on one doc. |
| C1 | `DA-C1-001` | finemath | keep | finemath 109/328 (v1: 47; her full `C1_LINE`, `C1_SITE` and phpBB block), 0 gold. Off on megamath because, as she says, the site list was fitted on finemath; on megamath it would change 72 docs, all labelled C1, with 0 gold harm, so it is a candidate for v1.2 if she agrees. |
| C2 | `DA-C2-001` | finemath | keep on finemath, off on megamath | finemath 40/187 (v1: 39; keeps repeated answer options and code-like passages, ruling 13), 0 gold. On megamath it changes 1 of 18 gold docs: inside the limit, but it would use all of it. |
| F1 | shared `../tools/f1_rule.py` | | separate | One F1 for all families, per the TSAI ruling. Math F1 is the prose path (separate draft PR). |
| C4, D4 | none | | no rule | Her sheet: a tested C4 rule caught 0 labelled cases and changed 2 clean docs; D4 (spun text) needs a language model. |
| G3 | none | | open | megamath loses hyphens and minus signs pack-wide (`2^n1` for `2^n-1`). No rule can restore them; documents whose maths became wrong are `drop` by verdict. |

## Combined

`harm_test.py --rules spec_v1/clean.py --rule all`: finemath 0/30, megamath 0/18 for every function and for ALL IN ORDER;
the same with disputed docs left in. `clean()` on the whole pack: finemath 176 fixed, 13 dropped, 311 kept; megamath 37
fixed, 10 dropped, 453 kept. A second `clean()` changes nothing on any doc of either pack.

## Open

- Routing: `build_clean.py` now sends a doc to the family whose rules list its pack in `ORIGIN`, and a family whose
  rules all check `pack_id` (math) claims no language tag, so English keeps `en` (separate commit in this PR).
- Gold is small (30 and 18): with 0 hits the harm rate is only shown to be below about 10% and 17%.
- Reviewer for all 14 rules.
