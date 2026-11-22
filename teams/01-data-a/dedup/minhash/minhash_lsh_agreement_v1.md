# Dedup v2 item 11: MinHash + LSH agreement with v1's exact Jaccard (22 Nov 2026)

**Question.** If exact all-pairs scoring does not fit corpus-v1, can MinHash + LSH replace it as the candidate step for
H1/H2, and with which settings, without losing v1's duplicates?

**Answer.** On 8 prose, Indic and math packs (227,820 documents) and 3 code packs (207,759), MinHash with 128 permutations and LSH with **32 bands × 4 rows** finds
**every** one of v1's 1,974 word-shingle qualifying pairs (50 H1, 1,924 H2) and all 560 code-token ones and every pair at Jaccard ≥ 0.70, while passing about
611,000 candidate pairs to the exact check. **25 bands × 5 rows** also finds all qualifying pairs with 116,000
candidates, but keeps less margin below the 0.80 threshold. Measurement only; nothing in v1 or the corpus-v1 job changes.

## Method

- **Data:** the train parts of 8 packs of the cleaned sample (`tokenizer_sample_v0_clean`), chosen for having the most
  H2 pairs across families: `cadj-commits`, `cadj-stackexchange`, `en-dclm`, `ind-hi-sangraha-s`, `ind-hi-sangraha-v`,
  `ind-kn-sangraha-s`, `ind-sa-fw2`, `math-megamath`.
- **Ground truth:** TSAI's 5 Nov overlap run on the same files (`overlap_pairs.csv`, all pairs at Jaccard ≥ 0.50;
  `overlap_matches.csv`, the qualifying pairs), restricted to pairs with both documents in these parts. Every document's
  shingle count matched that run's `overlap_docs.parquet` exactly (100% of 227,820), so the shingle sets are identical.
  (Held-out parts were left out: the local held-out files differ from the 5 Nov run's.)
- **Shingles:** exactly `overlap.py`'s: `h1_key`, then word 5-grams as 64-bit hashes (`jaccard_matrix.shingles`).
- **MinHash:** 128 hash functions `splitmix64(a·x + b)` over each document's shingle hashes (fixed seed 20261122).
- **LSH:** band configurations from 64×2 to 8×16. A pair is found if it collides in at least one band. "Candidate pairs"
  is the upper bound Σ C(bucket, 2) over bands (duplicates across bands counted).
- **Scripts:** `sigs.py` (signatures), `evaluate.py` (recall and cost); results in `results.json`.

## Results

227,820 documents in scope; 23,207 pairs at Jaccard ≥ 0.50; MinHash's estimate of Jaccard on those pairs: mean absolute
error 0.035, 95th percentile 0.087.

| Bands × rows | LSH threshold ≈ | Candidates (upper) | Recall ≥ 0.50 | ≥ 0.70 | ≥ 0.80 | ≥ 0.90 | H1 | H2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 64 × 2 | 0.13 | 17,362,359 | 100% | 100% | 100% | 100% | 100% | 100% |
| 42 × 3 | 0.29 | 2,130,961 | 99.9% | 100% | 100% | 100% | 100% | 100% |
| **32 × 4** | **0.42** | **611,114** | **95.0%** | **100%** | **100%** | **100%** | **100%** | **100%** |
| 25 × 5 | 0.53 | 116,036 | 69.1% | 99.97% | 100% | 100% | 100% | 100% |
| 21 × 6 | 0.60 | 55,508 | 51.7% | 98.4% | 99.95% | 100% | 100% | 99.95% (1 missed) |
| 16 × 8 | 0.71 | 20,376 | 27.6% | 88.5% | 98.7% | 100% | 100% | 98.6% (27 missed) |
| 8 × 16 | 0.88 | 3,275 | 6.0% | 35.1% | 58.7% | 94.0% | 100% | 58.0% |

Theory agrees: the chance a pair at Jaccard s is found is 1 − (1 − s^r)^b; at s = 0.80 that is 1 − 5×10⁻⁸ for 32×4 and
0.99995 for 25×5; at s = 0.70, 0.9998 and 0.990.

## Code packs (code-token shingles)

Same 128 hash functions on `overlap_rules.code_shingles` (Pygments token 5-grams, comments and licence headers left
out), for the train parts of `code-rust`, `code-python` and `code-go`: 207,759 documents, 170,373 of them with the 20
nonblank lines that `code_scores` needs. Ground truth: the 5 Nov run's code/code qualifying pairs among them (529
`code-rust`, 24 `code-python`, 6 `code-go` H2 at code Jaccard ≥ 0.85; 1 H1). MinHash's error on those pairs: mean 0.023,
95th percentile 0.057.

| Bands × rows | Candidates (upper) | H2 found | H1 found |
|---|---:|---:|---:|
| **32 × 4** | **34,495** | **559 / 559** | 1 / 1 |
| 25 × 5 | 19,147 | 559 / 559 | 1 / 1 |
| 21 × 6 | 11,030 | 559 / 559 | 1 / 1 |
| 16 × 8 | 5,904 | 555 / 559 (4 missed, all at 0.875) | 1 / 1 |

So the same 32×4 setting finds every qualifying code pair too. The cost of code is dominated by Pygments lexing (about
13 ms a document here, the same with exact or MinHash scoring); MinHash only replaces `code_scores`' sparse matrix.

## What it means for corpus-v1 and dedup v2

- **A tested fallback exists.** If exact scoring exceeds the corpus-v1 job's memory or time, MinHash + LSH (32×4) as the
  candidate step, followed by v1's exact Jaccard and family rules on the candidates, reproduces every v1 duplicate on
  these packs. Its memory is a fixed 1 KB signature per document (128 × 8 bytes), linear in documents, instead of the
  shingle matrix.
- **What it loses:** only pairs between 0.50 and 0.70, which v1 reports in its histogram but never removes (the lowest
  removal threshold is 0.80). 32×4 keeps 95% of them; the histogram below 0.70 would become approximate.
- **Not yet tested:** (1) `code-cpp`, `code-java`, `code-js-ts` (code is covered by rust, python and go above); (2) a second seed, to confirm recall at 21×6 and below;
  (3) cross-pack pairs (here only among the 8 packs); (4) the speed on TSAI's machine. Signatures took about 4.5 minutes
  for 120 M shingles on a 2-core workspace, single-threaded.
- **Decision needed before using it:** it changes the method (v1's exact all-pairs is the agreed design), so it goes to
  the lead and TSAI as a fallback with this evidence, not as a silent switch.

Kunal Sinha (Data A dedup).
