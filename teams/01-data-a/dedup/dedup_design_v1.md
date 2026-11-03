# Dedup design v1: How duplicates are found

Status: **DRAFT — proposed decisions, not yet agreed by the team.** Thresholds marked *(to test)* will be confirmed on the math and science packs before submission.

Covers the duplicate "diseases" defined in `diagnosis/DISEASES.md`, section H.

---

## Summary of decisions

| Code | Disease | Proposed decision |
|---|---|---|
| H1 | Exact duplicate in the pack | SHA-256 of normalised text; run first |
| H2 | Near duplicate (small changes) | MinHash + LSH, word 5-grams, 128 permutations, Jaccard ≥ 0.80 *(to test)*; verified by exact Jaccard; separate settings for code and math |
| H3 | Same content in another source/language | Same-language copies from another source: H1/H2 within each pack; across packs only if E2 validates it. Translations: **out of scope for v1**, pending TSAI confirmation; v2 candidate is multilingual embeddings or translate-then-match |
| – | Where dedup runs | After `clean.py`. **v1 default: within each pack only** (the per-snapshot analogue). Cross-pack and cross-team passes are measured, and applied only if E2 validates them |
| – | What is recorded | One log row per removed document: `(pack_id, part, doc_id)` for both removed and kept copies, similarity, rule, priority rule that decided |
| – | How it was tested | Known duplicate pairs + known non-duplicate pairs + gold harm check on `build_gold.py` output, matched on `(pack_id, doc_id)`, failing if no gold IDs are in the input |

---

## H1 — Exact duplicates

**Normalisation** (applied only to compute the hash; the stored text is not changed):
1. Unicode NFKC.
2. Case-fold.
3. Collapse every run of whitespace (spaces, tabs, newlines) to one space; strip ends.

**Hash:** SHA-256 of the UTF-8 bytes of the normalised text.

Documents with the same hash form a group; one survivor is chosen by `source_priority_v1.md`, the rest are removed. It is cheap and exact, so it runs before H2 and shrinks the input to H2.

**The H1 hash is a dedup key only.** It never replaces `doc_id`. `doc_id` is `sha256(utf-8 original text)[:16]`, set before cleaning and carried through `run_clean.py` and the sample job unchanged; dedup reads it as-is and never re-hashes the cleaned text.

*Not normalised on purpose:* punctuation and digits. Stripping them would merge math problems that differ only in a number (see H2, math).

## H2 — Near duplicates

**Method:** MinHash signatures with Locality-Sensitive Hashing (e.g. `datasketch` `MinHashLSH`).

| Setting | Prose (default) | Code | Math |
|---|---|---|---|
| Shingles | word 5-grams on H1-normalised text | token 5-grams after stripping licence header and comments | word 5-grams, numbers and LaTeX kept as tokens |
| Permutations | 128 | 128 | 128 |
| Threshold (Jaccard) | **0.80** *(to test)* | **0.85** *(to test)* | **0.90** *(to test)* + numbers must match |
| Minimum length | 50 words; shorter documents get H1 only | 20 lines | none; extra rule below |

**Why 0.80 for prose.** It is the common setting in public pre-training pipelines and catches re-posted pages with changed boilerplate, dates or a few edited sentences, while pages that merely share a topic sit well below it. We will confirm it from the similarity histogram of candidate pairs on our packs: the threshold should sit in the gap between the "same text" cluster and the "related text" cluster.

**Why 5-grams.** Shorter shingles (1–3 words) make unrelated texts look similar through common phrases; longer ones make one edited word break many shingles. Five is the usual middle ground.

**Verification step.** LSH only proposes candidate pairs. Each candidate is checked by computing the exact Jaccard similarity of the two shingle sets; only pairs at or above the threshold are treated as duplicates. This removes LSH false positives, and the exact value is what we log.

**Code.** Files copied between forks differ in licence headers, comments and formatting, so these are stripped before shingling. The higher threshold (0.85) avoids merging different files that share a lot of boilerplate (imports, generated code).

**Math.** Templated problems are the main risk: *"Solve 2x + 3 = 7"* and *"Solve 2x + 5 = 7"* are near-identical in text but are different problems. So for math packs a pair counts as a duplicate only if it passes the 0.90 threshold **and** the multiset of numbers in both documents is identical.

**Clusters.** Duplicate pairs are joined into clusters (union-find). One survivor per cluster is chosen by `source_priority_v1.md`.

## H3 — Same content in another source or language

`DISEASES.md` defines H3 as the same content in another source or language (e.g. a translation of a document seen in English). It has two halves, handled differently:

| Half | v1 | How |
|---|---|---|
| Same text from **another source**, same language | **Covered within each pack; across packs once validated** | H1 and H2 within each pack by default; the cross-pack pass is applied only if E2 validates it (see "Where dedup runs") |
| **Translation** into another language | **Out of scope for v1** | Not detected |

**Out of scope for v1: cross-language duplicates (the translation part of H3).** v1 finds exact (H1) and near (H2) duplicates by text within each pack, and across packs once the cross-pack pass is validated (E2), so the same text from another source in the same language is covered. A translation of a document into another language is not detected: that needs multilingual embeddings or translate-then-match, a different method and cost from hashing or MinHash, planned for **v2**. Within one document, `clean.py` already removes translation lines in Sanskrit (`DB-H3-001`, active on `ind-sa-fw2`); that rule stays and is not affected by this scope limit.

**Basis in the repo.** `spec_v1/README.md` lists H3 among the diseases regex cannot handle (needs a whole-pack check, a language model or a classifier). The instructor note of 30 Oct recorded there ("H3 has no rule") concerns code: a vendored copy is not a disease by itself, and the same file twice in a pack is H1 or H2. No TSAI ruling says dedup may skip the translation half, so this is stated as a **v1 limit pending TSAI confirmation**.

**Fallback if TSAI requires H3 for v1:** a narrow version for Sanskrit/Hindi/English only, where the Sanskrit packs are known to carry translations.

## Where dedup runs

1. **After `clean.py`.** Cleaning removes boilerplate and fixes encoding, which can turn two different pages into identical ones; deduplicating earlier would miss those.
2. **Within each pack** (H1 then H2). **This is the v1 default.** It is the analogue of FineWeb's per-snapshot dedup, which trained better models than global dedup (Session 3, §7; Risk 1).
3. **Across packs** (H1 then H2 on the union of surviving documents) — covers the same-language half of H3. **Measured, not applied by default:** it is run and its removals logged, but applied to the data only if E2 shows it removes a modest share of each pack and no gold document.
4. **Across both teams' packs** if Data B joins: same rule as step 3, plus the Indic check (E4).

Our packs are split by domain or source, not by crawl time as FineWeb's snapshots were, so a copy found in two of our packs is closer to a true duplicate than a page repeated across crawls. The analogy is therefore partial: it does not prove cross-pack dedup harmful here, only that the wider scope should not be the default until checked.

Dedup is not a cleaning job request: TSAI applies the approved spec v1 rules to the full data.

## What is recorded

For every removed document, one row in `dedup_log.jsonl`:

| Field | Meaning |
|---|---|
| `removed_pack_id` | Pack of the removed document |
| `removed_part` | Part of the removed document |
| `removed_id` | `doc_id` of the removed document, unchanged |
| `kept_pack_id` | Pack of the survivor |
| `kept_part` | Part of the survivor |
| `kept_id` | `doc_id` of the surviving copy it duplicated, unchanged |
| `rule` | `H1`, `H2` or `H3` |
| `similarity` | 1.0 for H1; exact Jaccard for H2/H3 |
| `priority_rule` | Which `source_priority_v1.md` rule chose the survivor (1–4) |
| `stage` | `within_pack`, `cross_pack` or `cross_team` |

**Why both sides carry pack and part.** `doc_id` is a hash of the original text, so exact copies share it. Within one part this cannot happen (the sample job stops on a duplicate `doc_id`), but across parts or packs it can, giving `removed_id == kept_id`. A document is therefore identified by `(pack_id, part, doc_id)`, never by `doc_id` alone. No current gold ID appears in two packs (checked across all 3,269), but this can change after a full run.

Plus a summary per pack: documents in, removed by H1, removed by H2, removed cross-pack, documents out.

## How it was tested

1. **Known duplicate pairs** (must be caught): an exact copy; a whitespace/case variant; a copy with one sentence edited; a copy with a licence header added (code); a truncated copy.
2. **Known non-duplicate pairs** (must be kept): two math problems that differ only in a number; two pages on the same topic from different sources; two code files sharing imports only.
3. **Harm check:** no gold document is removed.
   - **Gold source:** `<pack>_gold.csv` (`doc_id,reader_1,reader_2`) written by `build_gold.py`, read by `harm_test.py --gold`. A document is gold only if two different reviewers marked it `read=full`, `verdict=clean` in the same pack, with no disease other than D3. The raw `labels.csv` votes are never read. Data A gold: `teams/01-data-a/gold/`; Data B (Indic, cadj): `teams/02-data-b/gold/`, same format.
   - **Matching:** a gold document counts as removed if `(pack_id, doc_id)` appears on the removed side of `dedup_log.jsonl`. Matching on `doc_id` alone would wrongly flag a gold document whose identical copy was kept.
   - **Coverage first:** gold comes from the week-1 diagnosis packs (~500 docs each); the tokenizer sample (1.44M docs) is a separate draw. Before the check, count how many gold IDs are present in the dedup input and report that number with the result. **If it is zero, the harm check fails**, because it tested nothing. Preferred: run the harm check on the diagnosis packs, where gold coverage is guaranteed.
   - `harm_test.py` already refuses a gold file whose IDs are missing from the pack, so a mismatched pack and gold file fails loudly.
   - Any gold removal is listed and reviewed by hand.
4. **Threshold check:** similarity histogram of H2 candidate pairs on the math and science packs, plus a hand review of ~20 pairs just above and ~20 just below each threshold.
5. **Real counts:** duplicates found per rule per pack, reported in the summary table.

## Risks

**1. Wider scope can remove better text.** Deduplicating across a wider scope removes more documents, but more removal is not automatically better. FineWeb found that global dedup (across all crawl snapshots) trained worse models than per-snapshot dedup; in its oldest snapshot, the documents kept by global dedup were worse than the ones it removed (Session 3, §7). The reason: text repeated across many crawls tends to be good text that is reposted and linked; global dedup cut it to one copy while unique, often low-quality text was untouched, so the low-quality share of the mix grew. Our cross-pack and cross-team passes are the wider kind.
- *Survivor choice does not fix this.* `source_priority_v1.md` picks the better **copy** (licence, provenance, completeness), but the FineWeb risk is about how much **weight** popular content keeps in the mix, which any one-copy rule reduces.
- *Mitigation:* within-pack dedup is the v1 default; the cross-pack pass is measured but applied only if E2 validates it. Each log row records the `stage`, so within-pack and cross-pack removals are counted separately, and each removed document points to its survivor, so cross-pack removals can be reversed. Every dedup scope decision is treated as an ablation, not a given (Session 3, §11).

**2. Thresholds may not transfer to Indic text.** The thresholds are tested on the math and science packs only. Word 5-grams split on whitespace may behave differently on Indic scripts (agglutinative words, code-mixing, varied spacing), and methods tuned on English text are known to erase Indic content (Session 3, §8).
- *Added check:* if Data B joins the cross-team pass, re-run the threshold check (similarity histogram and hand review either side of the threshold) on at least one Indic pack before applying H2 to Indic data, and report Indic removal rates separately.

**3. Benchmark contamination is not covered.** Dedup removes repeated documents within the training data. Exact and fuzzy matching against held-out benchmark sets is a separate evaluation-integrity step (Session 3, §12) and is **not** part of this design. Passing dedup does not mean the data is free of test leakage.

## Experiments before final

Run on the week-1 diagnosis packs (~500 docs each), where gold coverage is guaranteed. Who runs them depends on the Task 4 / Task 5 split (open question to the instructor); results come back into the final version of this file.

| # | Experiment | What is measured | What would change the design |
|---|---|---|---|
| E1 | **Threshold sweep** on the math and science packs: H2 at 0.70, 0.75, 0.80, 0.85, 0.90, 0.95 | Similarity histogram of candidate pairs; hand review of ~20 pairs just above and ~20 just below each proposed threshold; removals per threshold | Move a threshold if the gap between "same text" and "related text" sits elsewhere, or if hand review finds distinct documents above it |
| E2 | **Within-pack vs cross-pack**: run the within-pack pass alone, then add the cross-pack pass | Removal counts per pack and per stage; harm check on each output separately | **Decides whether the cross-pack pass is applied.** Apply it only if it removes a modest share of each pack and no gold document; otherwise report it but keep within-pack dedup only (Risk 1) |
| E3 | **Known-pair tests**: the duplicate and non-duplicate pairs listed in "How it was tested" | Every duplicate pair caught; every non-duplicate pair kept | If math problems differing only in a number are merged, tighten the math rule; if a known copy is missed, revisit normalisation or shingle size |
| E4 | **Indic threshold check** (only if Data B joins): E1 on at least one Indic pack | Same as E1; Indic removal rate reported separately | Use separate Indic thresholds or shingling (e.g. character n-grams) if the English settings over- or under-remove (Risk 2) |

**Training ablation (not run in v1; budget-dependent).** The definitive test of dedup scope is to train small proxy models on the data after within-pack dedup only and after within- plus cross-pack dedup, and compare downstream scores (Session 3, §7 and §11). v1 does not run this; scope is checked by removal counts and the harm check only. If proxy-training budget becomes available, this is the first dedup experiment to run, because it is the only one that can show whether the wider scope helps or hurts the model.

## Open questions for the team

- Agree the three thresholds (0.80 / 0.85 / 0.90) after the 4 Nov test run.
- Is 50 words the right minimum length for H2 on prose?
- Does Data B join the cross-team pass for v1?
- **TSAI to confirm:** is leaving out the translation half of H3 acceptable for v1? (Post the H3 scope statement in the dedup PR or wherever TSAI answers scope questions.)
