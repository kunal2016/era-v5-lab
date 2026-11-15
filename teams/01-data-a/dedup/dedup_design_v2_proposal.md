# Dedup v2 proposal: what v1 left open

**Status:** proposal for team review, 13 Nov 2026; updated 15 Nov 2026 for the new Indic sources (#461) and Aneesha Das's H3 draft (#44 on Vijay's fork) (Kunal Sinha, Data A dedup). Nothing here changes v1, its job request or PR #255. v1 runs as agreed; each item below starts only after its own review.
**Builds on:** `dedup_design_v1.md` (how duplicates are found), `source_priority_v1.md` (which copy survives), `results_v1.md` (the numbers) and `removal_list_interface_v1.md` (how removals are applied). H3 has its own design, `h3_design_v1.md` (Aneesha Das, draft); this file only adds to it.

Every v1 number quoted here comes from TSAI's 5 Nov run or the local runs in `results_v1.md`. The 5 Nov run is superseded by the rerun on the #244 cleaning, so each number is checked again on the rerun before any item below is decided.

## Summary

Items are split by what they need. **v1.1** items change a rule or a setting of the existing method; each needs evidence and one overlap run, nothing new to build. **v2** items add a new method or a new rule and need their own experiment first.

| # | Item | Release | Why (v1 evidence) | Needs |
|---|---|---|---|---|
| 1 | Same-URL pairs count as H2 at ≥ 0.80 | v1.1 | A same-URL math copy scored 0.894 and was missed; two true math copies sharing a URL were rejected by the numbers rule | Team decision, overlap run |
| 2 | Math numbers rule on the body only | v1.1 | The rule rejected true copies whose only numeric difference was a date line or a number in the title | Team decision, overlap run |
| 3 | Indic length minimum | v1.1 | The 50-word minimum rejects 135 near-identical Indic pairs (69 documents); 19.9% of Indic documents are under 50 words | E4 reader labels, overlap run |
| 4 | Code threshold (0.85 on tokens) | v1.1 | "Under review" in v1; `code-rust` has 530 qualifying token pairs but only 3 word pairs ≥ 0.80 | Hand review of code pairs |
| 5 | Remove list carries `reason`, `stage` and part hashes | v1.1 | `removal_list_interface_v1.md`; `overlap_summary.json` has `checksum_verification: deferred` | Code change, tests |
| 6 | Config-only updates: licence map, Data B pack order | v1.1 | G10 owns licences (`code-js-ts`, `ind-hi-hplt` unverified); Data B lead may reorder their packs | Their decisions; `dedup.py` rerun (seconds) |
| 7 | **H3: translations across languages** | Own track (`h3_design_v1.md`) | Out of scope in v1 (TSAI, 5 Nov); Sanskrit packs are known to carry translations | Aneesha's E5 experiments; additions below |
| 13 | **Pack order for new packs:** a rule, not a hand-made list | Before any new pack joins | v1 ranks only the 38 sample packs; #461 proposes 15 new sources | Team decision; Data B's clean shares |
| 14 | **Packs that are not documents** (word pairs, lexicons, single sentences, speech transcripts) | Before those packs join | #461: Aksharantar, Dakshina, BPCC, Shrutilipi, IndicVoices | A decision per pack |
| 15 | **Licence map for the new sources** | Before those packs join | #461: card text and tag disagree for Aksharantar and MADLAD-400; BPCC's mined part repackages NC data | G10's rulings |
| 8 | Containment for truncated copies | v2 | E3 limit: a copy keeping 85 of 100 words is caught, 80 of 100 is missed | Experiment on the overlap outputs |
| 9 | Indic-aware shingles | v2, only if 3 is not enough | Word 5-grams were set on English (Risk 2) | Experiment on Indic packs |
| 10 | Survivor rule: the copy cleaning changed least | v2 | Dropped from v1: no per-document record of fixes | Experiment on the rerun's groups |
| 11 | Scale to the full data: MinHash + LSH agreement test | v2, sooner if #461's sources join | Exact all-pairs took 56 min on 1.4 M documents; the full data is larger, and #461 adds more Common Crawl | Agreement test on the sample |
| 12 | Training ablation of the cross-pack pass | v2, conditional; likely triggered by #461 | Only worth running where cross-pack removes ≥ 1% of a pack; on the sample none does, but MADLAD-400, IndicCorp and Sangraha unverified overlap fw2 | Counts with the new packs |

**Not dedup, handed on:**
- Empty documents (7 in v1) are a spec v1.1 cleaning rule.
- Template pages that pass the thresholds (slideserve.com, name/date templates) are a quality-filter problem.
- Benchmark contamination belongs to F2 (G9's fingerprints).

## v1.1: rule and setting changes

All of v1.1 goes into **one** overlap run, after TSAI's v1 dedup job, so that v1's remove list stays the record for the experiment and v1.1's effect can be reported as a difference: documents removed or kept, per pack and per item.

### 1. Same URL

**Change:** a pair whose documents have the same non-empty `url` counts as an H2 duplicate at Jaccard ≥ 0.80, in every family. This overrides the math numbers rule and the 0.90 math threshold for that pair only.
**Evidence:** reference.com's "examples of quadrilaterals" is in `math-finemath` train and `math-megamath` held-out with the identical URL, at 0.894. Two true math copies were rejected by the numbers rule; both share their URL.
**Check before deciding:** list every same-URL pair at 0.50–0.90 on the rerun and read them. A site that serves different content at one URL (a feed, a search page) would make this rule wrong for that site.

### 2. Math numbers rule on the body

**Change:** compare the multisets of numbers in the body only, ignoring the title and first line.
**Evidence:** the two rejected copies differed only in a date line or a number in the title.
**Check:** the worked-example pairs that the rule correctly keeps apart (math E1) must still be kept apart.

### 3. Indic length minimum

**Change:** a lower minimum for `ind-*` packs, or a minimum in shingles instead of words, set from E4's labels.
**Evidence:** across all `ind-*` packs the 50-word minimum rejects 135 near-identical pairs (69 documents); the three `sangraha-s` packs lose almost all their pairs (106 pairs, 35 documents, 4 clusters, each pair differing by 1–5 words per side).
**Needs:** the native readers' labels (issues #392–#395) on sheets rebuilt from the rerun. If they label the pairs as copies, lower the minimum. If they label them as templates, v1's minimum stays.
**Bound:** whatever the labels, the change affects at most 69 Indic documents on the sample.

### 4. Code threshold

**Change:** keep, raise or lower 0.85, from a hand review of about 20 code pairs on each side of the threshold, as was done for math. Include a sample of `cadj-commits`, the pack with the most duplicates.

### 5. Remove list and part hashes

As listed in `removal_list_interface_v1.md`:
- `overlap.py` records the SHA-256 of every input part in `overlap_summary.json`.
- `dedup.py` carries those hashes into `dedup_summary.json`.
- `dedup.py` adds `reason` (`H1`, `H2`) and `stage` (`dedup`) to `remove_list.csv`.

The remover's check 3 (part hash) then works.

### 6. Config-only updates

If G10 excludes a pack, set it to `false` in `licence_usable`. If the Data B lead asks for another order of their 25 packs, change the list in `dedup.json` and `source_priority_v1.md`. Neither needs an overlap run: rerun `dedup.py`, and its tests, on the same overlap outputs.

## v2: new methods

### 7. H3: translations across languages

H3 now has its own design: `h3_design_v1.md` (Aneesha Das, draft; #44 on Vijay's fork). It finds candidates with LaBSE and URL keys and decides by sentence coverage (aligned sentences ÷ sentences of the shorter document). That replaces the chunk-embedding sketch this file had on 13 Nov. What this proposal adds, as review points on #44:

- **Keep H3 out of the survivor rules.** Form the H1/H2 groups first. An H3 edge between two groups may only remove a train copy of a held-out document (rule 0); every other H3 pair is reported. Otherwise rules 1–4 would remove one language's copy, and rule 3 ("longer") does not compare across scripts.
- **One `dedup.py` run.** `h3.py` reads all documents of its packs (no `exclude`), so `overlap.py` and `h3.py` are independent, and one `dedup.py` run reads both match files and writes one remove list (Sourav Dhar's pipeline ask).
- **Keys.** `h3_matches.csv` carries `(pack_id, split, part, row_in_part, doc_id)` directly.
- **Parallel packs are never H3 duplicates.** Pralekha (document-level English–Indic) and BPCC's human parts (sentence-level) are translations on purpose (#461). No H3 edge is drawn between two documents of the same parallel pack; pairs between a parallel pack and another pack are reported like any other.
- **Real known pairs.** Split the `ind-sa-fw2` documents that `DB-H3-001` flags into their Sanskrit and translation parts, for a recall check before E5d's hand review.
- **Second opinion.** Translate-then-embed rather than translate-then-H2: it beat a multilingual encoder in Pasch, Petridis and Cutura (arXiv 2406.13695), 82% against 60% F1.
- **Question for G3 and G9.** Does a train document that translates a held-out document affect their results? If not, H3 can stay measurement-only in its first release.

### 8. Containment for truncated copies

**Problem.** Jaccard compares two documents as wholes, so a truncated copy is missed once it keeps less than about 80% of the text (E3: on a 100-word text, keeping 85 words scores 0.84 and is caught, keeping 80 scores 0.79 and is missed).

**Change.** Score pairs also by containment: shared shingles ÷ shingles of the shorter document. `overlap.py` already computes the shared count of every pair and the shingle count of every document, so containment costs no new pass. Two things do change:
- **The pair floor.** `overlap.py` keeps only pairs at Jaccard ≥ 0.50. A copy that keeps 40% of the text has a Jaccard near 0.40 and is dropped before any rule sees it, so containment pairs need their own floor.
- **A guard against short texts inside long ones.** A quote, a licence block or a boilerplate paragraph is fully contained in many long documents and is not a copy of them. The guard is a minimum length for the shorter document, plus the family's existing rules.

The survivor is unchanged: rule 3 already keeps the longer copy.

**Experiment.** On the rerun's outputs:
- Count pairs at containment ≥ 0.90 that Jaccard misses, per family.
- Read 20 of them.
- Add known pairs to `tests/test_known_pairs.py`: truncated copies at 70%, 50% and 30%, which must be caught, and a quoted paragraph inside a long page, which must be kept.

### 9. Indic-aware shingles (only if item 3 is not enough)

Whitespace word 5-grams were set on English. If E4's readers find copies that a lower word minimum still misses, or false matches from long agglutinative words, try shingles that do not depend on word boundaries: character n-grams of the H1 key, or 5-grams of a tokenizer's subwords such as G3's. Compare the two on the E4 pairs and on Indic gold. The harm check must stay at zero gold removed.

### 10. Survivor rule: the copy cleaning changed least

From `source_priority_v1.md`, "Not used in v1".
- **Rule:** among copies that tie on rules 0–3, prefer the one whose cleaned text differs least from its raw text, for example 1 − `difflib` ratio, measured only for the pairs dedup finds.
- **Why it's feasible:** raw and cleaned text share a `doc_id`, so no change to the cleaning tools is needed.
- **Placement:** after rule 3 (completeness) and before rule 4 (pack order), so it can only change survivors that pack order decides today.
- **Experiment:** count how many of the rerun's groups it would decide differently, and read those.

### 11. Scale: MinHash + LSH agreement test

Exact all-pairs scoring ran in 56 minutes and 9.6 GiB on 1.4 M documents. v1 keeps MinHash + LSH as the fallback for a run that does not fit. Before it is ever needed, measure on the sample how many of the exact method's qualifying pairs MinHash + LSH finds at a given number of permutations and bands, and at what cost. Then the switch is a measured choice, not a guess. Exact scoring stays the default while it fits.

### 12. Training ablation (conditional)

Unchanged from v1. Train small proxy models with and without the cross-pack pass only where cross-pack removes at least 1% of a pack. Recheck this on the full data's counts.

## New sources (#461): what dedup needs before they join

PR #461 (Srinivasan Govindaraj, Data B, `teams/02-data-b/indic_sources_v1.md`) lists 9 new Indic datasets (N1–N9) and 6 extensions of sources the lab already has (its E1–E6). v1 is unaffected: it covers only the 38 sample packs. Before any of these packs joins, dedup needs the following.

### 13. Pack order for new packs (rule 4)

**Problem.** Rule 4 is a hand-made list of the 38 sample packs: Data A in `clean.py` order, then Data B in alphabetical order. A new pack has no place in it, and a hand-placed list will not scale to 50+ packs. Alphabetical order also decides today that an `fw2` copy beats a `sangraha-v` copy of the same page, with no reason behind it.

**Proposal.** Replace the list with a rule. Rank packs by their measured clean share (Data B measures it per pack: for example 85.0% for `ind-hi-indiccorp` against 25.8% for `fw2`, as #461 cites from `native_indic_share_v1.md`). Packs without a measurement go after measured ones, in a fixed fallback order: curated sources (Wikipedia, Wikisource, IndicCorp, Sangraha verified) before raw crawl (`fw2`, MADLAD-400, Sangraha unverified). Ties keep v1's order. The ranking is computed once per run and written into `dedup.json`, so a run stays reproducible.

**Check.** On the rerun's groups, count how many survivors the new order would change, and read a sample of them: the surviving copy should look cleaner.

### 14. Packs that are not documents

**Problem.** v1's family rules assume documents: prose needs 50 words for H2, and shorter documents get H1 only. Several #461 sources are not documents:
- Aksharantar: native/romanised word pairs.
- Dakshina: a lexicon and short hand-romanised sentences.
- BPCC: single translated sentences.
- Shrutilipi and IndicVoices: speech transcripts, often short.

**Proposal.** A decision per pack, recorded in `dedup.json`:
- **Excluded from dedup:** Aksharantar and Dakshina's lexicon. They are for romanisation (D2) work, not pretraining text, and exact repeats of a word pair carry no harm.
- **H1 only:** BPCC sentences, Dakshina sentences and the speech transcripts. Exact repeats are removed; near-duplicate scoring of single sentences would mostly match common phrasing.
- **Normal rules:** every document-level source (Wikipedia, Wikisource, Pralekha, MADLAD-400, IndicCorp, FinePDFs, Sangraha).

Parallel packs (Pralekha, BPCC) are also exempt from H3 within the pack (item 7).

### 15. Licence map for the new sources (rule 1)

Rule 1 already treats permissive and CC-BY-SA licences as usable, so most of #461's In list needs no change. Three need G10's ruling before they go into `licence_usable`:
- **Aksharantar:** the tag says only "cc"; the card text says CC-BY (manual part) and CC0 (mined and existing parts).
- **MADLAD-400:** ODC-By tag, but the card text says CC-BY-4.0.
- **BPCC's mined part:** tagged CC0, but it repackages Samanantar, which is CC-BY-NC-4.0. #461 does not propose it.

### Effect on items 11 and 12

MADLAD-400, IndicCorp and Sangraha unverified are Common Crawl again and overlap `fw2` (#461 expects most of MADLAD-400 to dedup against `fw2`). Two v1 conclusions therefore need checking again:
- **Cross-pack scope (item 12).** v1 applied the cross-pack pass without a training ablation because only 50 of 2,711 qualifying pairs were cross-pack. With these packs, cross-pack removals may pass 1% of a pack. Where they do, the ablation runs before the cross-pack pass is applied to that pack (Risk 1: text repeated across sources tends to be good text).
- **Scale (item 11).** More packs bring the MinHash + LSH agreement test forward.

Also from #461:
- **Held-out overlap.** Its FineWeb-2 extension adds Punjabi and Assamese train data, and `heldout_v1` holds FineWeb-2's test splits for both. Rule 0 handles any overlap; the first run reports pa/as train ↔ held-out pairs separately.
- **Naming.** #461's extensions are numbered E1–E6, the same names as dedup's experiments E1–E5. Renaming them (e.g. X1–X6) avoids mixing them up.

## Order of work

1. **Now, in parallel with v1:**
   - Item 5, a code change with tests and no effect on v1's decisions.
   - H3's review points on #44 (item 7).
   - Decisions on items 13–15, so new packs can join with a rule ready.
2. **After TSAI's v1 dedup job:**
   - Items 1–4 and 6 together in one v1.1 overlap run.
   - The containment experiment (item 8) on the same outputs.
3. **After the v1.1 run:**
   - Item 10 on its groups.
   - Item 9 if E4 calls for it.
4. **When new packs join (#461) or the full-data size is known:** items 11 and 12.

## Questions for review

- **TSAI:** are found translation pairs reported only, or may train copies of held-out documents be removed (rule 0, as `h3_design_v1.md` proposes)? Should anything else be removed?
- **TSAI:** v1.1 as one overlap run after the v1 dedup job, reported as a difference from v1. Is that acceptable?
- **Team:** item 1 (same URL) and item 2 (math body) for v1.1, or keep v1's rules?
- **Team:** rule 4 by measured clean share for new packs (item 13); the per-pack decisions for non-document packs (item 14).
- **G10:** licences of the H3 model weights (LaBSE, and any alternative chosen in E5) for use in the data pipeline; Aksharantar, MADLAD-400 and BPCC's mined part (item 15).
- **Data B:** readers for Sanskrit–Hindi and Sanskrit–English pairs; clean-share measurements for each new pack (item 13).

## References

- Pasch, Petridis and Cutura, "Multilingual De-Duplication Strategies: Applying scalable similarity search with monolingual & multilingual embedding models", arXiv 2406.13695.
- Feng et al., "Language-agnostic BERT Sentence Embedding" (LaBSE), arXiv 2007.01852.
- Gala et al., "IndicTrans2: Towards High-Quality and Accessible Machine Translation Models for all 22 Scheduled Indian Languages", arXiv 2305.16307.
- Aneesha Das, `h3_design_v1.md` (draft), PR #44 on patilvijay23/era-v5-lab.
- Srinivasan Govindaraj, `teams/02-data-b/indic_sources_v1.md`, PR #461.
- Read, not used: Messmer, Sabolčec and Jaggi, "Enhancing Multilingual LLM Pretraining with Model-Based Data Selection", arXiv 2502.10361. It covers quality selection, not dedup; its decontamination (13-gram match, drop the whole document) is relevant to F2.
