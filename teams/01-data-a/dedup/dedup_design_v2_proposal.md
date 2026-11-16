# Dedup v2 proposal: what v1 left open

**Lead:** Vijay Patil (Data A). **Owners:** Kunal Sinha and Aneesha Das (Data A dedup).

**Now (Weeks 3 and 4, 15–28 Nov):** dedup runs v1's rules, frozen, at scale; only items 5, 6 and 16 are done now, because the run needs them (item 5 just after TSAI's dedup run, so the job's pin holds). Plan and requirements: `dedup_v1_1_plan.md`. Everything else in this file is the backlog for after training starts.

**Status:** final draft for team review, 15 Nov 2026 (first draft 13 Nov); updated 15 Nov for the new Indic sources (#461, with Shankar Pandala's review), Aneesha Das's H3 draft (#44 on Vijay's fork) and G2's note that it has no translated-pair work; updated 16 Nov for G10's licence rulings (all 38 packs), the BGE-M3 encoder check (H3-h, H3-i), a first containment count on the rerun (item 8) and item 5 moving after TSAI's dedup run (Kunal Sinha and Aneesha Das, Data A dedup). Nothing here changes v1, its job request or PR #255. v1 runs as agreed; each item below starts only after its own review.
**Builds on:** `dedup_design_v1.md` (how duplicates are found), `source_priority_v1.md` (which copy survives), `results_v1.md` (the numbers) and Sourav Dhar's pipeline (`teams/01-data-a/pipeline/`, which applies the remove list with `apply_dedup.py`). H3 has its own design, `h3_design_v1.md` (Aneesha Das, draft); this file only adds to it.

Every v1 number quoted here comes from TSAI's 5 Nov run or the local runs in `results_v1.md`. The 5 Nov run is superseded by the rerun on the #244 cleaning, so each number is checked again on the rerun before any item below is decided.

## Summary

Items are split by what they need. **v1.1** items change a rule or a setting of the existing method; each needs evidence and one overlap run, nothing new to build. **v2** items add a new method or a new rule and need their own experiment first.

| # | Item | Release | Why (v1 evidence) | Needs |
|---|---|---|---|---|
| 1 | Same-URL pairs count as H2 at ≥ 0.80 | v1.1 | A same-URL math copy scored 0.894 and was missed; two true math copies sharing a URL were rejected by the numbers rule | Team decision, overlap run |
| 2 | Math numbers rule on the body only | v1.1 | The rule rejected true copies whose only numeric difference was a date line or a number in the title | Team decision, overlap run |
| 3 | Indic length minimum | v1.1 | The 50-word minimum rejects 135 near-identical Indic pairs (69 documents); 19.9% of Indic documents are under 50 words | E4 reader labels, overlap run |
| 4 | Code threshold (0.85 on tokens) | v1.1 | "Under review" in v1; `code-rust` has 530 qualifying token pairs but only 3 word pairs ≥ 0.80 | Hand review of code pairs |
| 5 | Summaries record code SHA-256, git commit and part hashes; `remove_list.csv` keeps its five columns | v1.1 | Sourav's runner adopts overlap and dedup but cannot record their code (`code_sha256` stays null); `apply_dedup.py` accepts only the exact five-column header | Code change, tests |
| 6 | Config-only updates: licence map, Data B pack order | v1.1 | G10 now lists all 38 packs in Stage 0, `TSAI reserves` (16 Nov; PR pending); only `ind-hi-hplt`'s web terms remain for TSAI | G10's PR on `main`; `dedup.py` rerun (seconds) |
| 7 | **H3: translations across languages** | v1.1 in `h3_design_v1.md` (Aneesha); recheck in v2.0 | Out of scope in v1 (TSAI, 5 Nov); Sanskrit packs are known to carry translations | H3-a to H3-f for v1.1; H3-g to H3-m after E5 |
| 8 | Containment for truncated copies | v2 | E3 limit: a copy keeping 85 of 100 words is caught, 80 of 100 is missed | Experiment on the overlap outputs |
| 9 | Indic-aware shingles | v2, only if 3 is not enough | Word 5-grams were set on English (Risk 2) | Experiment on Indic packs |
| 10 | Survivor rule: the copy cleaning changed least | v2 | Dropped from v1: no per-document record of fixes | Experiment on the rerun's groups |
| 11 | Scale to the full data: MinHash + LSH agreement test | v2, sooner if #461's sources join | Exact all-pairs took 56 min on 1.4 M documents; the full data is larger, and #461 adds more Common Crawl | Agreement test on the sample |
| 12 | Training ablation of the cross-pack pass | v2, conditional; likely triggered by #461 | Only worth running where cross-pack removes ≥ 1% of a pack; on the sample none does, but MADLAD-400, IndicCorp and Sangraha unverified overlap fw2 | Counts with the new packs |
| 13 | **Pack order for new packs:** a rule, not a hand-made list | Before any new pack joins | v1 ranks only the 38 sample packs; #461 proposes 15 new sources | Team decision; Data B's clean shares |
| 14 | **Packs that are not documents** (word pairs, lexicons, single sentences, speech transcripts) | Before those packs join | #461: Aksharantar, Dakshina, BPCC, Shrutilipi, IndicVoices | A decision per pack |
| 15 | **Licence map for the new sources** | Before those packs join | #461: card text and tag disagree for Aksharantar and MADLAD-400; BPCC's mined part repackages NC data | G10's rulings |
| 16 | **Pipeline contract** with Sourav's runner: remove-list checks, summaries, the dedup job as a `run.json` | Now, for every release | `apply_dedup.py` stops on a list that breaks its checks; `pipeline/open-items.md` lists 7 dedup items | Code and docs; answers to Sourav |

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

### 5. Summaries and the remove list

The remove list is applied by Sourav Dhar's `apply_dedup.py` (`teams/01-data-a/pipeline/`, #37 and #46 on Vijay's fork). Its checks set this item:
- **`remove_list.csv` keeps exactly its five columns** (`pack_id, split, part, row_in_part, doc_id`). `apply_dedup.py` stops on any other header, so no `reason` or `stage` column is added. The rule that removed each document is already in `dedup_log.jsonl` (`rule`, `stage`, `priority_rule`), and H3 removals are logged there too.
- **`overlap_summary.json` and `dedup_summary.json` record `code_sha256` and the git commit** of the script that wrote them. The runner adopts the overlap and dedup jobs as TSAI ran them, and without these fields its `cleaning_pipeline.json` has `code_sha256: null` for both (Sourav's open items).
- **`overlap_summary.json` records the SHA-256 of every input part** (today `checksum_verification: deferred`), and `dedup_summary.json` carries them on. `apply_dedup.py` checks the `doc_id` and `pack_id` of every listed row, which catches a list made from other parts; the hashes also catch a part whose unlisted rows changed.

### 6. Config-only updates

G10 has added a Stage 0 row for every sample pack (16 Nov, `saitej123:g10-week3-post-training`; `en-dclm` stays In, its "research purposes only" line read as a disclaimer and noted for TSAI's Gate 3). Once that is on `main`, `dedup.json` lists all 38 packs in `licence_usable` with `default_licence_usable: false` (`licence_status_before_scale_v1.md`). If TSAI excludes a pack later, set it to `false`. If the Data B lead asks for another order of their 25 packs, change the list in `dedup.json` and `source_priority_v1.md`. Neither needs an overlap run: rerun `dedup.py`, and its tests, on the same overlap outputs.

## v2: new methods

### 7. H3: translations across languages

H3 has its own design: `h3_design_v1.md` (Aneesha Das, draft; #44 on Vijay's fork), for dedup v1.1. It finds candidates with LaBSE and URL keys and decides by sentence coverage (aligned sentences ÷ sentences of the shorter document). That replaces the chunk-embedding sketch this file had on 13 Nov.

The points below split into what Aneesha's v1.1 design should take up before its first TSAI run, and what is rechecked in v2.0 once E5's measurements exist.

**For H3 v1.1 (owner: Aneesha Das, in `h3_design_v1.md`; raised on #44)**

| # | Rule | Why |
|---|---|---|
| H3-a | **Keep H3 out of the survivor rules.** Form the H1/H2 groups first. An H3 edge between two groups may only remove a train copy of a held-out document (rule 0); every other H3 pair is reported, not removed | Otherwise rules 1–4 remove one language's copy, and rule 3 ("longer") does not compare across scripts |
| H3-b | **One `dedup.py` run.** `h3.py` reads all documents of its packs (no `exclude`); `overlap.py` and `h3.py` are independent; one `dedup.py` run reads both match files and writes one remove list | Sourav Dhar's pipeline ask; excluding H1/H2 removals needs a second `dedup.py` run and saves little (0.095% removed on 5 Nov) |
| H3-c | **Keys.** `h3_matches.csv` carries `(pack_id, split, part, row_in_part, doc_id)` | No join on `h3_docs.parquet` rows; matches the remove list's key |
| H3-d | **Parallel packs are not H3 duplicates.** No H3 edge between two documents of the same parallel pack (Pralekha, BPCC human parts); pairs with other packs are reported as usual | They are translations on purpose (#461) |
| H3-e | **Real known pairs.** Positives from FLORES-200 devtest (the same sentences in English, Hindi, Sanskrit and Odia; an evaluation set, read to test the encoder, never trained on). Hard negatives from `ind-sa-fw2`: its documents split by `DB-H3-001` into Sanskrit and "translation" lines are mostly a Sanskrit story with an embedded English or Hindi tweet on the same event (433 pairs, checked by hand on 15 Nov), the same-topic case H3 must keep. Scripts: `h3_checks/build_known_pairs.py`, `labse_check.py` (how it was run: below) | E5a uses a fake encoder; `DB-H3-001` removes embedded foreign-language text more than translations, so it cannot supply positives |
| H3-f | **Ask TSAI, and G3 and G9, before building or removing anything.** Keep-or-remove for translations is not ruled yet (Shankar Pandala, 15 Nov). Does a train document that translates a held-out document affect G3's or G9's results? If not, v1.1 is measurement only (E5c) | Rule 0 is the draft's main reason to remove; it rests on these answers. G2 has no pair finder, no LaBSE/IndicTrans2 runs and no H3 review pack, so H3 is Data A's alone; G2's translation work rates quality (#440), and its proposal has 0% translated text until TSAI decides at Gate 3 |

**Rechecked in v2.0 (after E5c and E5d)**

| # | Question | Evidence it needs |
|---|---|---|
| H3-g | Is anything removed beyond rule 0, for example machine-translated copies (D4/D5)? Which copy survives? | E5d labels by pair type; a TSAI decision |
| H3-h | Thresholds per language pair (coverage 0.6, sentence cosine 0.7, `doc_floor` 0.5 are provisional). **Measured 15 Nov** (`h3_labse_check_results_v1.md`, run steps below): at 0.7, LaBSE finds 100% of Hindi and Odia FLORES translations but only 29% of Sanskrit–English and 19% of Sanskrit–Hindi; at 0.5 Sanskrit rises to 96% / 89%, but 3 of the 7 real-page matches are not translations. **BGE-M3, 16 Nov** (`h3_bge_m3_check_results_v1.md`): at 0.7 it finds 82% of Sanskrit–English and 95% of Sanskrit–Hindi blocks, Hindi and Odia stay at 100%, and 6 of its 8 real-page matches are translations, so one threshold fits every pair | E5d's sweep and hand review, per pair; a margin score with LaBSE |
| H3-i | The encoder: LaBSE or an alternative, per language. **Measured 15 Nov:** Odia and Hindi fine (P@1 1.0 against English); Sanskrit found (P@1 0.95–0.98) but with low cosines (median 0.69). **BGE-M3, 16 Nov:** Sanskrit P@1 0.99, true-pair median 0.74–0.78; but unrelated text also scores higher (best wrong match median 0.57 against LaBSE's 0.41), so `doc_floor` needs retuning (about 0.6), and it is about 8 times slower on CPU (7,255 s against 863 s) | A Sanskrit reader's labels on BGE-M3's 16–27 candidates at 0.5–0.6; its cost on TSAI's GPU |
| H3-j | Head-only retrieval (first 4 sentences, mutual top 3): does it miss pairs on sites whose pages share their opening lines? | The share of URL-found pairs that retrieval also finds (E5b) |
| H3-k | Coverage over at most 16 sentences: is that enough for long documents? | Coverage on long known pairs |
| H3-l | Second opinion: translate-then-embed on a sample, rather than translate-then-H2. It beat a multilingual encoder in Pasch, Petridis and Cutura (arXiv 2406.13695), 82% against 60% F1 | Agreement with sentence coverage on the E5d sample |
| H3-m | Wider scope: Data A ↔ Data B pairs (needs TSAI), more language pairs, and #461's new packs | v1.1's counts and cost per pair |

**H3 encoder check, 15 Nov (measurement only; results in `h3_labse_check_results_v1.md`)**

What was run, and how to repeat it. Scripts and README: `h3_checks/` (`build_known_pairs.py`, `labse_check.py`,
`README_h3_checks.md`). Document text stays in a local `out/` folder outside the repo; only numbers and doc_ids are
reported.

1. **Same-page pairs from `ind-sa-fw2`** (no model needed; 7 s):
   `python build_known_pairs.py --parts <raw ind-sa-fw2 parts> --out out`. It splits each raw document (week-1 pack,
   5,963 documents) into its Sanskrit lines and the lines `DB-H3-001` calls translations. Result: 433 pairs (343 with
   an English half, 90 Hindi). Read by hand, most are not translations (a Sanskrit news story with an embedded tweet on
   the same event), so they serve as same-topic hard negatives; `DB-H3-001` cannot supply positives.
2. **The encoder on Hugging Face models and data** (laptop CPU, 863 s; needs internet access to Hugging Face):
   - Prerequisites, once: in a Python venv, `pip install sentence-transformers datasets pyarrow numpy`; `hf auth login`
     with a read token; accept the terms on the gated dataset page
     `https://huggingface.co/datasets/openlanguagedata/flores_plus`.
   - Run: `python labse_check.py --pairs out/known_pairs.parquet --out out/labse`. The model
     (`sentence-transformers/LaBSE`, about 1.9 GB) downloads on first use into the Hugging Face cache.
   - If it stops with `DatasetNotFoundError: ... is a gated dataset`, the terms were not accepted (or the token is for
     another account). On Windows, a warning about symlinks is harmless.
   - Positives: FLORES-200 devtest, 1,012 sentences in English, Hindi, Sanskrit and Odia (an evaluation set, read to
     test the encoder and never used as training data), as sentences and as 8-sentence pseudo-documents. Negatives:
     other FLORES blocks, and the 433 same-page pairs. H3's own settings throughout (mutual best match, sentence
     threshold swept 0.5 to 0.9, coverage rule 0.6).
3. **Result in one line:** Hindi and Odia are fine at the draft's 0.7 (100% of translated blocks qualify, 0% of other
   blocks); Sanskrit is found (P@1 0.95 to 0.98) but at 0.7 only 29% of Sanskrit-English and 19% of Sanskrit-Hindi
   blocks qualify, and at 0.5 3 of the 7 real-page matches are not translations (H3-h, H3-i).
4. **BGE-M3, 16 Nov** (`h3_bge_m3_check_results_v1.md`): the same command with `--model BAAI/bge-m3` (7,255 s). At 0.7
   it finds 82% of Sanskrit-English and 95% of Sanskrit-Hindi blocks (Hindi and Odia 100%, other blocks 0%); 6 of its 8
   real-page matches are translations. Its cosines run higher for unrelated text too, and it is about 8 times slower.
5. **Next:** a margin score in place of the plain cosine, with LaBSE (`--progress` prints stage times).

### 8. Containment for truncated copies

**Problem.** Jaccard compares two documents as wholes, so a truncated copy is missed once it keeps less than about 80% of the text (E3: on a 100-word text, keeping 85 words scores 0.84 and is caught, keeping 80 scores 0.79 and is missed).

**Change.** Score pairs also by containment: shared shingles ÷ shingles of the shorter document. `overlap.py` already computes the shared count of every pair and the shingle count of every document, so containment costs no new pass. Two things do change:
- **The pair floor.** `overlap.py` keeps only pairs at Jaccard ≥ 0.50. A copy that keeps 40% of the text has a Jaccard near 0.40 and is dropped before any rule sees it, so containment pairs need their own floor.
- **A guard against short texts inside long ones.** A quote, a licence block or a boilerplate paragraph is fully contained in many long documents and is not a copy of them. The guard is a minimum length for the shorter document, plus the family's existing rules.

The survivor is unchanged: rule 3 already keeps the longer copy.

**First count, 16 Nov** (TSAI's rerun on the #244 cleaning, `overlap_pairs.csv`): pairs whose containment is at least 0.90 but which v1 does not match.

| Family | Pairs | Shorter document about 50 words or more |
|---|---:|---:|
| Code | 916 | 891 |
| Indic | 321 | 113 |
| Math | 302 | 299 |
| Prose | 19 | 14 |
| Across families | 5 | 5 |

At least 1,563 pairs, mostly code and math; prose hardly changes, and most short Indic pairs belong to item 3. It is a lower bound: `overlap_pairs.csv` keeps only pairs at Jaccard ≥ 0.50, so copies truncated to less than about half are not in it. None has been read yet.

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

**Proposal.** Replace the list with a rule. Rank packs by their measured clean share (Data B measures it per pack in `native_indic_share_v1.md`. On the rebuilt gold, #439: 85.0% for `ind-hi-indiccorp`, 25.3% for `fw2`, 4.7% for `sangraha-s`, 7.4% for `ind-hi-hplt`. The rule must read the current version of that file, since the numbers moved when the gold was rebuilt; #461's figures came from the 2 Nov gold). Packs without a measurement go after measured ones, in a fixed fallback order: curated sources (Wikipedia, Wikisource, IndicCorp, Sangraha verified) before raw crawl (`fw2`, MADLAD-400, Sangraha unverified). Ties keep v1's order. The ranking is computed once per run and written into `dedup.json`, so a run stays reproducible.

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

Parallel packs (Pralekha, BPCC) are also exempt from H3 within the pack (H3-d, item 7).

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

## Pipeline prerequisites (Sourav's runner and `apply_dedup.py`)

### 16. What the pipeline needs from dedup

Sourav Dhar's runner (`run_pipeline.py`) runs clean → overlap → dedup → apply → F2 → survivor loss → shards. Overlap and dedup are TSAI jobs that it adopts; `apply_dedup.py` applies `remove_list.csv`; `survivor_loss.py` reads `dedup_groups.csv`. Its checks make the following a contract for every dedup release, v1.1 and v2 included.

**`remove_list.csv`, as `apply_dedup.py` checks it (any failure stops the run before anything is written):**

| Check | What dedup must guarantee |
|---|---|
| Header | Exactly `pack_id, split, part, row_in_part, doc_id`. No new column (item 5) |
| Keys | No `(split, part, row_in_part)` listed twice; `row_in_part` a whole number ≥ 0 |
| Held-out | No held-out row. Rule 0, enforced again at apply: one held-out row means the list is broken. H3-a relies on this |
| Part and row | `part` is the path relative to the split folder, with `/` (`code-go/part-00000.parquet`); `row_in_part` is the 0-based row in file order, as `overlap.py` numbers them |
| Same cleaning run | The `doc_id` and `pack_id` at each listed row match the list. A list made from another cleaning run than the parts stops the run |
| Pack column | No empty `pack_id` in any part |

**Other outputs:**
- `dedup_groups.csv` is read by `survivor_loss.py`, and the runner checks that its group count matches. Its format is part of the contract.
- `dedup_summary.json`: the runner checks status, counts, the overlap hashes and **held-out removed = 0**.

**Sourav's open items for the dedup side** (`pipeline/open-items.md`, 14 Nov):
1. `code_sha256` and the git commit in `overlap_summary.json` and `dedup_summary.json` (item 5).
2. Do `overlap_summary.versions` or `block` change what counts as a duplicate? (He assumes no.) Is `gold_dirs` used only by the harm check?
3. Are `inputs`, `out` and `results` safe to override per run (the runner generates them)? Once the scripts take `--input` and `--out` flags, the runner's generated configs can go.
4. The dedup job after the #244 cleaning: a `jobs/<date>-dedup/run.json` that adopts job 244's clean folder, with `to: dedup`, and a request whose `Command:` is `python teams/01-data-a/pipeline/run_pipeline.py --config <run.json>`. The test log is `--plan` plus a small trial with `stages.clean.only`.
5. PR order: the runner's default `pipeline.json` points at `teams/01-data-a/dedup/*.json`, which reach `main` only with #255.
6. Delete the untracked placeholders in `teams/01-data-a/dedup/` once dedup merges.
7. Licence (`licence_status_before_scale_v1.md`): a preflight check that every pack of the manifest is listed in `licence_usable`.

**What this means for H3:** H3 adds no second remove list. Under H3-b, one `dedup.py` run writes one `remove_list.csv` with the same five columns, so `apply_dedup.py` needs no change; H3 removals (rule 0 only, H3-a) are told apart in `dedup_log.jsonl`. `dedup_groups.csv` keeps the H1/H2 groups only; a survivor removed by H3 is written as `removed`, so its group has no survivor. Checked against Sourav's `survivor_loss.py` (16 Nov): such a group is counted as `without_survivor`, as a no-licence group is, never as lost to F2, so no change is needed there. The H3 cases are told apart in `dedup_log.jsonl` (`rule: H3`) and `h3_pairs.csv`.

## Order of work

1. **Now, in parallel with v1:**
   - Item 16: the answers to Sourav's open items; the dedup job as a runner `run.json` if his runner still needs one.
   - H3-a to H3-f into `h3_design_v1.md` (Aneesha, #44).
   - Decisions on items 13–15, so new packs can join with a rule ready.
2. **After TSAI's v1 dedup job:**
   - Item 5: summaries with code SHA-256, commit and part hashes (after the job, so its `6cfc24a` pin holds).
   - Items 1–4 and 6 together in one v1.1 overlap run.
   - The containment experiment (item 8) on the same outputs.
3. **After the v1.1 run:**
   - Item 10 on its groups.
   - Item 9 if E4 calls for it.
   - H3-g to H3-m, once E5c and E5d have run.
4. **When new packs join (#461) or the full-data size is known:** items 11 and 12.

## Questions for review

The team reviews first; only the questions that are TSAI's go to TSAI, in one short note, after the team agrees.

**For the team** (Vijay Patil approves as lead):
- Items 1 (same URL) and 2 (math body) for v1.1: turn their switches on for the overlap rerun, or keep v1's rules?
- The two-week scope in `dedup_v1_1_plan.md`.
- Items 13 and 14 (rule 4 by measured clean share; non-document packs), when #461's packs are about to join.

**For TSAI** (after the team agrees):
- H3 (H3-f): report-only, or may train translations of held-out documents be removed (rule 0, as `h3_design_v1.md` proposes)? Anything else? Asked before `h3.py` is rebuilt for the GPU. If G2's 0% translated text holds at Gate 3, H3's machine-translation case (H3-g) mostly disappears.
- The overlap rerun carries items 1 and 2 if the team turns them on, and v1.1's effect is reported as a difference from v1. Acceptable?
- Later, only when #461's packs join: rule 4 by measured clean share (item 13), since TSAI approved v1's pack order.

**For other teams:**
- Aneesha Das: `h3_matches.csv` keyed by document (H3-c).
- Sourav Dhar: whether the runner's preflight can check the licence map (item 16).
- G10: licences of the H3 model weights (LaBSE, and any alternative chosen in E5); Aksharantar, MADLAD-400 and BPCC's mined part (item 15).
- Data B (G2): clean-share measurements for each new pack (item 13). G2 has no H3 work (15 Nov), so readers for Sanskrit–Hindi and Sanskrit–English pairs have to be found elsewhere.

**Settled:** licence decisions for all 38 sample packs (G10, 16 Nov); how `survivor_loss.py` counts H3-emptied groups (checked, item 16).

## References

- Pasch, Petridis and Cutura, "Multilingual De-Duplication Strategies: Applying scalable similarity search with monolingual & multilingual embedding models", arXiv 2406.13695.
- Feng et al., "Language-agnostic BERT Sentence Embedding" (LaBSE), arXiv 2007.01852.
- Gala et al., "IndicTrans2: Towards High-Quality and Accessible Machine Translation Models for all 22 Scheduled Indian Languages", arXiv 2305.16307.
- Aneesha Das, `h3_design_v1.md` (draft), PR #44 on patilvijay23/era-v5-lab.
- Srinivasan Govindaraj, `teams/02-data-b/indic_sources_v1.md`, PR #461.
- Read, not used: Messmer, Sabolčec and Jaggi, "Enhancing Multilingual LLM Pretraining with Model-Based Data Selection", arXiv 2502.10361. It covers quality selection, not dedup; its decontamination (13-gram match, drop the whole document) is relevant to F2.
