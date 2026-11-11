# Dedup design v1: How duplicates are found

**Status:** v1. [decision log](#decision-log) at the end; open items are listed before it.
**Scope:** the duplicate diseases H1–H3 of `diagnosis/DISEASES.md`, section H. Which copy survives a duplicate group is defined in `source_priority_v1.md`.

## Summary of decisions

| Topic | Decision | Status |
|---|---|---|
| H1, exact duplicates | SHA-256 of the H1 key: spec v1 `normalize.match_key`, then NFKC, casefold, whitespace collapse | Decided |
| H2, near duplicates | Exact Jaccard of every pair. Prose: word 5-grams ≥ 0.80, both ≥ 50 words. Math: ≥ 0.90 and the same numbers. Code: token 5-grams ≥ 0.85, both ≥ 20 non-blank lines. A pair from two families must pass both families' rules | Decided; code threshold under review |
| H3, another source or language | Same-language copies from another source: covered by H1/H2 within and across packs. Translations: out of scope for v1 | Agreed |
| Where dedup runs | After `clean.py`; within each pack, across packs and across both teams (Data A and Data B) | Agreed |
| Which copy survives | `source_priority_v1.md`: held-out first, licence, provenance, completeness, pack order | Agreed |
| Hand-off to TSAI | A remove list `(pack_id, split, part, doc_id)` and `dedup_log.jsonl`; TSAI filters the cleaned data, our code never rewrites it | Agreed |
| Validation | Known pairs, threshold sweep and hand review per family, gold harm check on the diagnosis packs | Partly done |

## H1: exact duplicates

**The H1 key** (used only for matching; the stored text is never changed), `h1_key()` in `h1_sha256.py`:
1. Spec v1 `normalize.match_key(text)` from `spec_v1/tools/normalize.py`, unchanged (spec v1 is frozen): HTML entities decoded, control and invisible characters removed, NFC with its listed folds, casefold, spaces collapsed.
2. Then Unicode NFKC, casefold, and every run of whitespace to one space. NFKC is applied here, never inside `normalize.py`, so spec v1 and G9's fingerprints are unaffected.

Two documents are H1 duplicates when the SHA-256 of their keys is equal. H1 bypasses the H2 length guards.

- **Punctuation and digits are kept** in the key on purpose: stripping them would merge math problems that differ only in a number.
- **The H1 hash never replaces `doc_id`.** `doc_id` is `sha256(utf-8 original text)[:16]`, set before cleaning and carried through unchanged; dedup never re-hashes the cleaned text.

## H2: near duplicates

**Terms.** A document's *shingles* are the set of its word 5-grams (overlapping 5-word windows of the H1 key; repeats count once). The *Jaccard similarity* of two documents is shingles in both ÷ shingles in either. Example with 3-word shingles: "the cat sat on the mat" and "the cat sat on a mat" share 2 of 6 distinct shingles, J = 0.33; compared word by word they would score 5/6 = 0.83, which is why single words are not used.

**Method: exact Jaccard of every pair** (`overlap.py`, `jaccard_matrix.py`). Each shingle is stored as an 8-byte BLAKE2b digest. The documents × shingles matrix times its transpose gives the shared count of every pair that shares a shingle, block by block. There is no sampling and no MinHash estimate, so every score is exact and is the value logged. On the 38-pack sample (1.4 million documents) this ran in 56 minutes. MinHash + LSH remains the fallback for a run that does not fit.

`overlap.py` keeps every pair at word Jaccard ≥ 0.5 (at most 0.80, so no prose candidate is lost). `overlap_rules.py` decides which pairs qualify (`overlap_matches.csv`):

| Setting | Prose (English, science, Indic, `cadj-*`) | Code (`code-*`) | Math (`math-*`) |
|---|---|---|---|
| Shingles | word 5-grams of the H1 key | token 5-grams from the language's Pygments lexer; comments and a leading licence docstring dropped; strings and preprocessor directives kept | word 5-grams of the H1 key; numbers and LaTeX kept |
| Threshold (Jaccard) | 0.80 | 0.85 | 0.90, and the multisets of signed numbers must match |
| Minimum length | 50 words; shorter documents get H1 only | 20 non-blank lines after comment removal | none |

**Why these settings**
- **0.80 for prose:** the common setting in public pre-training pipelines. It catches re-posted pages with changed boilerplate, dates or a few edited sentences; pages that only share a topic score far lower.
- **5-grams:** shorter shingles make unrelated texts look similar through common phrases; longer ones let one edited word break many shingles.
- **Minimum length:** in a 60-word document one changed word breaks 5 of about 56 shingles, so short template pages that differ only in a name or date score 0.82–0.85.
- **Code on tokens:** files copied between forks differ in licence headers, comments and formatting. Code pairs are scored in their own all-pairs pass, independent of the word floor, so a forked file is found even when comments lower its word score. 0.85 avoids merging different files that share boilerplate (imports, generated code).
- **Math numbers rule:** *"Solve 2x + 3 = 7"* and *"Solve 2x + 5 = 7"* are near-identical text but different problems.

**Families.** H1 compares every pack with every other. For H2, a pair inside one family uses that family's rules; a pair from two families must pass both families' rules on both documents. Notebooks and math pages can contain code, so mixed pairs are kept but judged strictly.

**Clusters.** Qualifying pairs are joined into clusters (union-find); `source_priority_v1.md` chooses the survivors of each cluster.

## H3: another source or language

| Half of H3 | v1 |
|---|---|
| Same text from another source, same language | Covered by H1 and H2, within and across packs |
| A translation into another language | Out of scope: not detected |

Detecting translations needs multilingual embeddings or translate-then-match, a different method and cost from hashing; it is the v2 candidate, starting with Sanskrit/Hindi/English, where the Sanskrit packs are known to carry translations. `clean.py`'s within-document rule `DB-H3-001` (translation lines in `ind-sa-fw2`) stays. `spec_v1/README.md` already lists H3 among the diseases that regex cannot handle.

## Where dedup runs

1. **After `clean.py`.** Cleaning can make two different pages identical, so deduplicating earlier would miss those copies.
2. **Within each pack**, the analogue of FineWeb's per-snapshot dedup (Session 3, §7).
3. **Across packs, and across both teams' packs.** Data B's Indic and `cadj-*` packs join the H1/H2 pass. Translations between the teams stay out of v1. The cross-pack pass was gated on experiment E2 because of Risk 1; on the 38-pack run it adds very few removals (see Evidence), so v1 applies it. Its removals carry `stage = cross_pack` in the log and can be reversed.

## Pipeline and hand-off to TSAI

```
raw sample ─▶ clean.py (TSAI, spec v1) ─▶ cleaned parts (doc_id, text, url, lang_label, pack_id)
                                              │
                                              ▼
                     overlap.py   MEASURES + QUALIFIES: H1 key, exact Jaccard of every pair, family rules
                                  → overlap_matches.csv, overlap_matrix.csv, overlap_docs.parquet, summary
                                              │
                                              ▼
                     dedup.py     DECIDES: clusters, which copy survives
                                  → remove_list.csv, dedup_log.jsonl, dedup_summary.json
                                              │
                                              ▼
                     harm check   gold, matched on (pack_id, doc_id)
```

| Step | Code | Status |
|---|---|---|
| Measure and qualify | `overlap.py`, `overlap_rules.py`, `h1_sha256.py`, `jaccard_matrix.py`, `overlap_report.py`, tests; config `overlap.json` (38 cleaned packs) | Done (Aneesha Das, Vijay Patil). Job `jobs/2026-11-04-overlap.md`, run by TSAI on 5 Nov |
| Reviewed matrix | `overlap_report.py`, `confirm_matrix.py` → `dedup/overlap_matrix.csv` | Done (Aneesha Das, 10 Nov): byte-identical to TSAI's matrix; `matrix_confirmation.md` |
| Decide | `dedup.py` + `dedup.json`: read `overlap_matches.csv` and `overlap_docs.parquet`, set aside matches between empty documents, form clusters, apply `source_priority_v1.md`, write the remove list and log. A scope switch can turn the cross-pack pass off without rerunning the overlap job | Written (Kunal Sinha), with tests and `README_dedup.md`. Local run on TSAI's outputs (no urls): 1,345 removed. Job `jobs/2026-11-10-dedup.md` pending approval |
| Check | Harm check of the remove list against gold | Built into `dedup.py`. `not_testable` on sample v0; **pass** on 4 diagnosis packs (727 gold, 0 removed) |

**What TSAI receives:** this design and `source_priority_v1.md`; the code, configs, tests and test logs above; the reviewed overlap matrix (`dedup/overlap_matrix.csv`); and a job request for `dedup.py` on sample v0 ("which documents would v1 remove, per pack and stage, and does it remove any gold?"). After approval, TSAI filters the full cleaned data with the remove list, as it applies spec v1. Our code never rewrites the data, so every removal can be reversed from the log. This is not a cleaning job request.

## What is recorded

For every removed document, one row in `dedup_log.jsonl`:

| Field | Meaning |
|---|---|
| `removed_pack_id`, `removed_split`, `removed_part`, `removed_row_in_part`, `removed_id` | The removed document; `removed_id` is its `doc_id`, unchanged |
| `kept_pack_id`, `kept_split`, `kept_part`, `kept_row_in_part`, `kept_id` | The surviving copy it duplicated (empty when no copy could survive) |
| `rule` | `H1` or `H2` |
| `similarity` | 1.0 for H1; exact Jaccard for H2 (token Jaccard for code) |
| `priority_rule` | The `source_priority_v1.md` rule that chose the survivor (0–4) |
| `stage` | `within_pack`, `cross_pack`, or `none` when no copy could survive |
| `direct` | `false` when the removed copy reached the survivor only through other copies |

Plus `remove_list.csv` (`pack_id, split, part, row_in_part, doc_id`: what TSAI filters out), a list of held-out ↔ held-out duplicates for G3, a list of empty documents for the cleaning team (`empty_documents.csv`; nothing is removed for them), and a summary per pack: documents in, removed by H1, removed by H2, removed cross-pack, documents out.

**A document is identified by `(pack_id, split, part, doc_id)`, never by `doc_id` alone.** `doc_id` hashes the original text, so exact copies in different parts or packs share it, and `removed_id` can equal `kept_id`.

## Validation

| # | Check | What it shows | Status |
|---|---|---|---|
| E1 | **Threshold sweep and hand review per family:** pair counts at 0.70–0.95 (`overlap_histogram.csv`), ~20 pairs read on each side of the threshold | Whether each threshold sits in the gap between "same text" and "related text" | Math reviewed (findings below). Prose and code: counts in, hand review open |
| E2 | **Within-pack vs cross-pack** removal counts | Whether the cross-pack pass is worth applying (Risk 1) | Answered by the TSAI run: applied |
| E3 | **Known pairs:** an exact copy, a whitespace/case variant, an edited sentence, a forked code file, a truncated copy (must be caught); math problems differing in a number, same-topic pages, code sharing only imports (must be kept) | The rules behave as specified | Done. The earlier tests check an edited copy, exact scores against brute force, the math numbers rule, code comment removal and mixed families. `tests/test_known_pairs.py` adds the rest: a whitespace/case variant is caught as H1; a truncated copy is caught as H2; same-topic pages (same site header and vocabulary) and code sharing only its imports are kept, and a one-value fork of that code is caught. **Limit found:** a truncated copy is caught only while it keeps about 80% of the text (on a 100-word text, 85 words kept scores 0.84 and is caught, 80 words scores 0.79 and is missed), because Jaccard compares the two documents as a whole, not whether one is contained in the other |
| E4 | **Indic threshold check:** E1 on at least one Indic pack | Whether the prose rules suit Indic text (Risk 2) | Measured (`results_v1.md`, section 3): the 50-word minimum causes every rejection of a near-identical pair in the three Indic `sangraha-s` packs (106 pairs), and 19.9% of Indic documents are under 50 words. Rebuilt from the raw text (`e4_review.py`): all 106 give TSAI's score; they come from only 35 documents in 4 clusters, and each pair differs by 1–5 words per side. Across all `ind-*` packs the 50-word minimum rejects 135 near-identical pairs (69 documents). Open: a human reader's labels |
| Harm | **No gold document is removed.** Gold is `<pack>_gold.csv` from `build_gold.py` (`teams/01-data-a/gold/`, `teams/02-data-b/gold/`), matched on `(pack_id, doc_id)`. The number of gold IDs present in the input is reported first; if it is zero, the check fails, because it tested nothing | No harm to reviewed clean documents | Done on the 4 diagnosis packs on hand (`math-finemath`, `math-megamath`, `sci-finepdfs`, `cadj-commits`): 727 gold IDs present (314 from the gold in this branch, plus 413 for `cadj-commits` from `main`), 0 removed (`results_v1.md`, section 3). The only pair at word Jaccard ≥ 0.50 is two `cadj-commits` gold documents at 0.716, both kept; no math or science gold document is in any pair at ≥ 0.50. Limit: 4 of the 13 Data A packs have gold here |

## Evidence

The full numbers, per pack and per run, are in **`results_v1.md`**. This section lists only what the decisions rest on. Final measurements come from TSAI's run of `overlap.py` (commit `86ecdd4`) on the 38 cleaned sample v0 packs, 5 Nov 2026 (`jobs/results/2026-11-04-overlap/`). Document removal counts come from `dedup.py`.

- **Scale:** 1,416,236 documents in 56 minutes with a 9.6 GiB peak, within the requested 60 minutes and 32 GiB, so exact all-pairs scoring fits (Risk 4).
- **Duplicates are rare:** 98 H1 pairs and 2,613 H2 pairs. 21 of the H1 pairs are between 7 documents that cleaning emptied without dropping (1 `code-cpp`, 4 `code-java`, 2 `code-js-ts`); they share one H1 key but are not copies, so `dedup.py` sets them aside and lists them for the cleaning team. On the sample, `dedup.py` removes 1,345 documents (0.095%).
- **Cross-pack overlap is small:** 50 of the 2,711 qualifying pairs are cross-pack, 14 of them between the empty documents. This answers E2: the cross-pack pass cannot cause a measurable FineWeb effect, so v1 applies it and no training ablation is needed.
- **Held-out copies exist:** 63 qualifying pairs join a train and a held-out document, so rule 0 matters.
- **Concentration:** most near duplicates are in `cadj-commits`, `cadj-stackexchange` and `ind-hi-sangraha-s`; English packs have very few.
- **Two signals for the hand review** (`results_v1.md`, section 1): the code token pass finds many pairs that word scores miss (`code-rust`: 3 pairs ≥ 0.80 by words, 530 qualifying), and the 50-word minimum removes almost every pair in three Indic `sangraha-s` packs, which is where E4 starts.

Findings from local test runs on raw sample v0 parts (details in `results_v1.md`, section 2):
- **Math numbers rule** (math E1, 47,250 documents): it keeps different worked examples apart as intended, but it also rejected two true copies of the same page whose only numeric difference was a date line or a number in the title. Both pairs share their URL.
- **Template pages pass the thresholds:** slideserve.com pages with different titles inside identical site boilerplate (math, ~117 words, above 0.90) and short template pages that differ only in a name or date (English, 0.82–0.85). They are not copies of one document; this is a quality-filter problem, not a dedup one.
- **A same-URL copy can fall just below the threshold:** one math page with an identical URL scored 0.894.

## Risks

1. **A wider scope can remove better text.** FineWeb found that global dedup trained worse models than per-snapshot dedup, because text repeated across crawls tends to be good text, and cutting it to one copy raised the share of unique low-quality text (Session 3, §7). Choosing a better survivor does not fix this. *Mitigation:* the cross-pack pass was gated on E2, and its effect is negligible on the sample; every removal records its `stage` and can be reversed.
2. **Thresholds may not suit Indic text.** Whitespace word 5-grams and a 50-word minimum were set on English. Indic scripts have longer, agglutinative words and code-mixing, and English-tuned methods are known to erase Indic content (Session 3, §8). *Mitigation:* E4 before H2 removals are applied to Indic packs, with Indic removal rates reported separately.
3. **Benchmark contamination is not covered.** Matching against benchmark sets is a separate evaluation step (Session 3, §12). Passing dedup does not mean the data is free of test leakage. Train/held-out copies inside the sample are handled by rule 0.

**Training ablation.** The definitive test of dedup scope is to train small proxy models on data with and without the cross-pack pass (Session 3, §7 and §11). It is only worth running where the cross-pack pass removes a measurable share (≥ 1% of a pack). No pack comes close on the sample, so v1 requests none.

## Open items before the final (Fri 13 Nov)

- **`dedup.py` TSAI run:** approve `jobs/2026-11-10-dedup.md`; TSAI runs it with the cleaned parts, so rule 2 (url) applies.
- **Hand review:** prose (0.80) and code (0.85), as done for math; and a sample of `cadj-commits`, the pack with the most duplicates.
- **E4:** a human Kannada, Telugu and Tamil reader to label the 106 rejected `sangraha-s` pairs (copy, template, different or unsure) on the blind sheets in `out/e4/review/`. The measured part and the rebuild from the raw text are done (`results_v1.md`, section 3). Whatever the labels, a lower minimum would affect at most 69 Indic documents.
- **Math numbers rule and same URL (team decision):** compare numbers in the body only (ignoring the title and first line), and count same-URL pairs as H2 duplicates at ≥ 0.80. Either change needs a new overlap run before it applies.

## Decision log

It covers this file and `source_priority_v1.md`. The body states the decisions; this log is the record of approval. Add a row whenever a decision is made or changed.

| Date | Decision | Agreed by | Where |
|---|---|---|---|
| 3 Nov 2026 | First drafts of both design files | Data A team | PR #255, commit `8a772b2` |
| 4 Nov 2026 | Method follows the implemented `overlap.py` / `overlap_rules.py`: exact Jaccard; family rules (prose 0.80 + 50 words, math 0.90 + numbers, code 0.85 tokens + 20 lines); a mixed pair must pass both families' rules | Data A team | PR #255, commits `1718918`, `16c479c` |
| 4 Nov 2026 | Design v1 agreed by the team | Data A team | PR #255, commit `16c479c` |
| 5 Nov 2026 | H3: translations out of scope for v1; H1/H2 cover same-language copies from another source; `DB-H3-001` stays | TSAI | PR #255, TSAI comment of 5 Nov, point 1 |
| 5 Nov 2026 | Data B packs join the cross-team H1/H2 pass; E4 required; translations between the teams stay out | TSAI | PR #255, point 2 |
| 5 Nov 2026 | Pack order (rule 4): the order in which `clean.py` lists the packs, written in `source_priority_v1.md` | TSAI | PR #255, point 3 |
| 5 Nov 2026 | Held-out first (rule 0): a train copy of a held-out document is removed; held-out ↔ held-out duplicates are reported, not removed; dedup never shrinks the held-out set | TSAI | PR #255, point 4 |
| 5 Nov 2026 | Hand-off: a remove list `(pack_id, split, part, doc_id)` and `dedup_log.jsonl`; TSAI filters the cleaned data, our code never rewrites it | TSAI | PR #255, point 5 |
| 5 Nov 2026 | Location: code and design in `teams/01-data-a/dedup/`, job requests in `teams/01-data-a/jobs/` | TSAI | PR #255, point 6 |
| 10 Nov 2026 | The 25 Data B packs, which `clean.py` does not list, follow the Data A packs in alphabetical order. It affects 23 of the 50 cross-pack pairs. The Data B lead may ask for a different order, with a reason, by Fri 13 Nov | Data A team; approved by TSAI | `source_priority_v1.md`, rule 4; TSAI in G1 |
| 10 Nov 2026 | Cross-pack pass applied in v1 (E2 answered: 50 of 2,711 qualifying pairs are cross-pack); no training ablation for v1 | Data A team | `results_v1.md`, section 1 |
| 10 Nov 2026 | Reviewed source matrix: `dedup/overlap_matrix.csv` is TSAI's returned matrix, unchanged; rebuilt byte-identically with and without `overlap_docs.parquet` and with `overlap_report.py --results` | Aneesha Das (Data A) | `matrix_confirmation.md`; PR #255 |
| 10 Nov 2026 | Empty documents (no shingles) are not duplicates: `dedup.py` sets aside their matches, removes none of them and lists them in `empty_documents.csv` for the cleaning team. On the sample: 7 documents, 21 matches; 1,345 removed instead of 1,351. The 7 documents stay in the data; dropping them is a cleaning change for spec v1.1 | Data A team (proposed by Aneesha Das, agreed by Kunal Sinha; Kunal's Windows rerun gave the same result, `remove_list.csv` `913e66a6…`) | PR #255, commit `497dbd3`; `dedup.py`, `README_dedup.md`, `jobs/2026-11-10-dedup.md` |
| 11 Nov 2026 | Licence (rule 1): all 38 sample-v0 packs usable; `dedup.json` unchanged (empty `licence_usable`, default true). G10's table on `main` lists 8 of the packs, none excluded; `code-js-ts` and `ind-hi-hplt` left open for TSAI, with no effect on the v1 remove list | Data A team (Vijay pointed to the table) | `source_priority_v1.md`, rule 1; G10 `licence_table.md` |