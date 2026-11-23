# MinHash + LSH vs v1 dedup: method, memory, correctness (22 Nov 2026)

Companion to `minhash_lsh_agreement_v1.md` (results) and `README_minhash_item11.md` (method and steps). This note answers
the three questions that come up: how is it different from v1, how does it fare on memory at corpus-v1 scale, and does
it change what is found. Measurement and arithmetic only; nothing in v1 or the corpus-v1 job changes.

## 1. How it differs from v1

MinHash + LSH changes one step of v1: how H2 finds the pairs to score.

**Unchanged**
- **H1** (exact duplicates by hash).
- **H3** (cross-lingual, LaBSE / BGE-M3): embeddings, not shingles.
- **H2's decision:** 5-word shingles (code-token shingles for code), exact Jaccard, v1's thresholds and family rules.
  The same pairs qualify and the same documents are removed.

**Changed: candidate generation for H2**

| | v1 (now) | MinHash + LSH |
|---|---|---|
| Pairs scored | Every pair sharing **any** shingle (inverted index) | Pairs whose 128-value signatures match in **≥ 1 of 32 bands** |
| Pairs on the sample | ~2.3 billion | 611,114 (word packs), 34,495 (code packs) |
| Kept per document | All its shingles + index entries | A fixed 1 KB signature |
| Memory growth | Linear-to-quadratic (shared-shingle pairs); the 14 GB peak | Linear, ~1.1 KB per document |
| Exact or approximate | Exact: cannot miss a qualifying pair | Candidate step is probabilistic: can in principle miss one |

Why v1 does so much work: two documents sharing one common shingle ("as well as the …") are still paired and scored,
though they are ~1% similar. Almost all of the 2.3 B pairs are like that. MinHash skips them because the chance of a
band match is s⁴ (s = Jaccard): 0.0001 at s = 0.1, but 0.41 at s = 0.8, so a near-duplicate is effectively certain to
collide in one of 32 bands.

In v2 it would sit in front of H2: MinHash narrows the pairs, v1's exact check decides.

## 2. Memory at corpus-v1 scale (estimate, not measured)

v1 holds all documents' shingles at once (word shingles, then the code-token sets): 14 GB at 1.41 M documents in the
38-pack rehearsal, about linear in corpus size (`overlap_scaling_corpus_v1.md`).

MinHash per document:

| Item | Bytes per document | Note |
|---|---:|---|
| Signature (128 × uint64) | 1,024 | Held all run; uint32 would halve it |
| One band's sort table | ~36 | Bands processed one at a time |
| Candidate pairs | ~45 | 611k pairs / 228k docs on the sample, ~16 B a pair |
| **Total** | **~1.1 KB** | Shingles dropped after each signature |

k = corpus-v1 documents ÷ 1.41 M:

| k | Documents | v1 peak (estimate) | MinHash step |
|---:|---:|---:|---:|
| 1 | 1.4 M | 14 GB | ~1.6 GB |
| 1.5 | 2.1 M | 21 GB | ~2.3 GB |
| 2 | 2.8 M | 28 GB | ~3.1 GB |
| 3 | 4.2 M | 42 GB | ~4.7 GB |
| 5 | 7.1 M | 70 GB | ~7.8 GB |
| 10 | 14.1 M | 140 GB | ~15.5 GB |

About 9× less, and even at 10× the sample close to what v1 uses today.

Caveats:
1. **The exact check must change too.** v1 scores pairs from shingles already in memory. With MinHash, candidate
   documents are re-read and re-shingled in chunks (only documents in candidate pairs). That is a change to
   `overlap.py` and a second read of those documents.
2. **Boilerplate buckets.** Thousands of documents sharing a band (templates, licence text) give n² pairs in that bucket.
   Usual guard: cap bucket size, exact-check oversized buckets separately. Not tested.
3. **Not counted:** document table, H1 keys, Parquet read batches (same for both methods).
4. **Not measured at scale:** `sigs.py` peak memory and speed on TSAI's machine. One large pack would confirm ~1.1 KB.

Time: Pygments lexing (~13 ms per code document, most of v1's 84 minutes) stays. MinHash fixes memory, not the 2-hour
job limit on its own.

## 3. Correctness and accuracy

**Only one kind of error is possible**

| Error | v1 | MinHash + exact check |
|---|---|---|
| False positive (non-duplicate removed) | Only if v1's rules are wrong | **Same as v1.** Every candidate is scored by v1's exact Jaccard and rules |
| False negative (duplicate missed) | None relative to its own definition | Possible only if a true pair never becomes a candidate |

Precision equals v1's by construction; recall is the only thing to measure.

**Measured recall, 32×4, ground truth = TSAI's 5 Nov run (train parts)**

| Pairs | v1 found | MinHash found |
|---|---:|---:|
| H1 (word) | 50 | 50 |
| H2 (word, ≥ 0.80) | 1,924 | 1,924 |
| All pairs at Jaccard ≥ 0.70 | — | 100% |
| Code H2 (code Jaccard ≥ 0.85) | 559 | 559 |
| Code H1 | 1 | 1 |
| Pairs at 0.50–0.70 (report only, never removed) | 23,207 at ≥ 0.50 | 95% at ≥ 0.50 |

The final duplicate list and remove list would be identical to v1's on these packs.

**Expected misses from the band maths:** P(miss at Jaccard s) = (1 − s⁴)³²

| s | P(miss) |
|---:|---:|
| 0.70 | 1.5 × 10⁻⁴ |
| 0.80 (word H2 threshold) | 4.6 × 10⁻⁸ |
| 0.85 (code threshold) | 6 × 10⁻¹¹ |
| 0.90 | ~10⁻¹⁵ |

Even 30,000 qualifying pairs all at exactly 0.80 (worst case) give about 0.001 expected misses.

**Where accuracy would suffer**
- **Deciding on the MinHash estimate.** Error of the estimate: word mean 0.035 (p95 0.087), code mean 0.023 (p95 0.057).
  Near 0.80 that would wrongly keep or remove pairs. MinHash must only pick candidates, never decide.
- **The low end of the histogram.** v1's report of pairs at 0.50–0.70 becomes approximate (~95%). Nothing removed depends
  on it; the data card should say so.

**What it can't fix or confirm**
- **Ground truth is v1.** MinHash can match v1, not beat it. Duplicates v1 cannot see (paraphrase, reordered text)
  MinHash cannot see either; H3 covers some across languages.
- **Train parts only.** Held-out was left out (local held-out files differ from the 5 Nov run's). Held-out↔train matters
  most for contamination; test it once matching held-out files are available.
- **Not yet tested:** a second seed, cross-pack pairs beyond these 11 packs, `code-cpp`, `code-java`, `code-js-ts`.
  Results are deterministic for a fixed seed (20261122).

## Bottom line

Used only as the candidate step, MinHash 32×4 keeps v1's precision (the same rules decide) and, as tested, its recall
(no qualifying pair missed), at about a ninth of the memory. It trades v1's guarantee for a very high probability, so it
goes to the lead and TSAI as a documented fallback, not a silent switch.

Data A dedup.
