# How the MinHash + LSH agreement test works, and how to repeat it

Companion to `minhash_lsh_agreement_v1.md` (the results). This file explains what each number means and how it was
measured, then gives the exact steps to repeat it.

## 1. The idea in plain words

**What v1 does today.** `overlap.py` turns every document into a set of *shingles*: every run of 5 consecutive words of
its normalised text (the H1 key), each stored as a 64-bit hash. Two documents are compared by **Jaccard similarity**:

    Jaccard(A, B) = shingles both have ÷ shingles either has

v1 computes this **exactly for every pair of documents that share at least one shingle** (2.3 billion pairs on the
sample) with a big sparse matrix. That is accurate, but memory and time grow with the corpus (14 GB and 84 minutes on
1.4 M documents), which is the corpus-v1 risk.

**What MinHash does.** Instead of keeping all shingles, keep a short *fingerprint* of each document:
1. Take 128 different hash functions h₁ … h₁₂₈.
2. For each hash function, hash every shingle of the document and keep only the **smallest** value.
3. The 128 smallest values are the document's **signature** (128 × 8 bytes = 1 KB, whatever the document's length).

The useful fact: for one hash function, the chance that two documents have the **same smallest value** equals their
Jaccard similarity. (The smallest hash over the union of both sets is equally likely to be any shingle in the union; the
two minima agree exactly when that shingle is in both sets.) So the share of the 128 positions where two signatures
agree is an **estimate of Jaccard**. On our pairs the estimate was within 0.035 on average (word shingles) and 0.023
(code tokens).

**What LSH does.** Comparing every signature with every other is still all-pairs. LSH avoids it:
1. Cut each signature into **b bands of r values** (32 × 4 = 128).
2. Two documents become a **candidate pair** if all r values of **at least one band** are identical. Finding these is
   just grouping documents by band value (a sort or hash table per band), never comparing all pairs.
3. Only candidate pairs then go to v1's exact Jaccard and family rules. The exact check is unchanged; MinHash only
   decides which pairs get checked.

The chance that a pair with Jaccard s becomes a candidate is

    P(found) = 1 − (1 − s^r)^b

which is an S-shaped curve. More rows per band (r) makes it stricter, more bands (b) more lenient. Its steepest point,
the "LSH threshold", is about (1/b)^(1/r): 0.42 for 32 × 4, 0.53 for 25 × 5. For 32 × 4, a pair at Jaccard 0.80 is found
with probability 1 − 5×10⁻⁸; at 0.70, 0.9998; at 0.50, 0.87.

## 2. How each number was measured

**Ground truth.** TSAI's 5 Nov overlap run (`out/overlap_tsai/`) on the same cleaned files:
- `overlap_pairs.csv`: every pair it stored, all at word Jaccard ≥ 0.50, with the exact Jaccard;
- `overlap_matches.csv`: the pairs v1's rules qualify as duplicates (H1 exact, H2 near), with word and code Jaccard;
- `overlap_docs.parquet`: each document's global row number and its shingle count.

**Same shingles as v1.** The scripts import v1's own functions (`h1_key`, `jaccard_matrix.shingles` for words,
`overlap_rules.code_shingles` for code), so nothing is reimplemented. Check: every document's shingle count equalled the
5 Nov run's `overlap_docs.parquet` (227,820 of 227,820). Held-out parts were left out because the local held-out files
differ from the 5 Nov run's; train parts matched exactly.

**Recall.** For each ground-truth pair (both documents in the tested parts), compute its two signatures' band values and
check whether any band agrees. Recall = share of ground-truth pairs found. Reported per Jaccard level (≥ 0.50, 0.70,
0.80, 0.90) and per rule (H1, H2).

**Candidates ("pairs to verify").** For each band, group the documents by band value and count the pairs in each group,
C(n, 2) = n(n − 1)/2; add over the 32 bands. That is an upper bound on the exact checks needed (a pair colliding in two
bands is counted twice). For code, only documents with the 20 nonblank lines that `code_scores` needs are counted.

**MinHash error.** For each ground-truth pair, the share of the 128 positions where its signatures agree, compared
with the exact Jaccard from the 5 Nov run: mean and 95th percentile of the absolute difference.

**What the numbers mean.** "32 × 4 finds 100% of the qualifying pairs" means: on these packs, if overlap used MinHash
32 × 4 to choose which pairs to check, and then applied v1's exact rules as today, it would produce the same qualifying
pairs as the exact run. "Candidates 611,114" means those exact checks would cover about 611 k pairs, instead of the
2.3 billion pairs sharing a shingle that the sparse product touches today (on the whole sample).

**Limits.** One seed (recall at the stricter settings could move a little with another seed); 11 packs, not all 38;
pairs only among the tested packs (no cross-pack pairs to other packs); speed measured on a 2-core workspace, not
TSAI's machine.

## 3. Steps to repeat it

Run from the repository root of a `main` checkout (so `teams/01-data-a/dedup/` has `h1_sha256.py`,
`jaccard_matrix.py`, `overlap_rules.py`), with `requirements_overlap.txt` installed (numpy, pandas, pyarrow,
pygments 2.21.0).

**Inputs.**
- The cleaned sample the 5 Nov run used: `tokenizer_sample_v0_clean/{train,heldout}/<pack>/part-*.parquet`.
- That run's outputs: `out/overlap_tsai/{overlap_docs.parquet, overlap_pairs.csv, overlap_matches.csv}`.

**Step 1: word-shingle signatures** (about 4.5 minutes for 120 M shingles):

    export MH_OUT=out/minhash_item11 DEDUP_DIR=teams/01-data-a/dedup OVERLAP_RUN=out/overlap_tsai
    C=../tokenizer_sample_v0_clean/tokenizer_sample_v0_clean/train
    python sigs.py $C/cadj-commits/part-00000.parquet $C/cadj-stackexchange/part-00000.parquet \
      $C/en-dclm/part-00000.parquet $C/en-dclm/part-00001.parquet $C/ind-hi-sangraha-s/part-00000.parquet \
      $C/ind-hi-sangraha-v/part-00000.parquet $C/ind-kn-sangraha-s/part-00000.parquet \
      $C/ind-sa-fw2/part-00000.parquet $C/math-megamath/part-00000.parquet

**Step 2: word-shingle recall and cost** → `$MH_OUT/results.json`:

    python evaluate.py

It stops if any document's shingle count differs from the 5 Nov run (a sign of different input files).

**Step 3: code-token signatures** (Pygments lexing, about 13 ms a document; two processes in parallel took about 30
minutes for 208 k documents):

    python codesigs.py $C/code-rust/part-00000.parquet $C/code-rust/part-00001.parquet \
      $C/code-python/part-00000.parquet $C/code-python/part-00001.parquet \
      $C/code-go/part-00000.parquet $C/code-go/part-00001.parquet

**Step 4: code recall and cost** → `$MH_OUT/results_code.json`:

    python evaluate_code.py

The scripts use a fixed seed (20261122), so the same inputs give the same signatures and the same numbers. On Windows,
set the variables with `set` (cmd) or `$env:MH_OUT = "..."` (PowerShell) instead of `export`.

## 4. Files

| File | What it is |
|---|---|
| `minhash_lsh_agreement_v1.md` | Results and what they mean |
| `README_minhash_item11.md` | This file: method, measurements, steps |
| `sigs.py`, `codesigs.py` | Signatures from v1's word and code shingles |
| `evaluate.py`, `evaluate_code.py` | Recall, candidate counts, MinHash error against the 5 Nov run |
| `results.json`, `results_code.json` | The numbers in the results tables |
| `sigs.log`, `c1.log`, `c2.log` | Run logs (documents, shingles, seconds per part) |
