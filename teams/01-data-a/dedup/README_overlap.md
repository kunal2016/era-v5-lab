# overlap.py: how much do packs overlap?

`overlap.py` compares every document with every other document across several packs and scores each pair by its
**Jaccard similarity**: the share of word 5-grams the two documents have in common. It answers one question:

> How much do the four English packs of the Week-2 tokenizer sample v0 (en-dclm, en-fineweb-edu, en-nemotroncc,
> en-nemotroncc-synth) overlap, inside each pack and across packs?

It **measures**; it removes nothing. Which copy would survive is a separate step (`source_priority_v1.md`). The method
follows `dedup_design_v1.md`: the H1 key for exact copies, word 5-grams and exact Jaccard for near copies (H2), and the
cross-pack pass that the design measures before deciding whether to apply it (experiment E2).

---

## What it does

1. **Checks the config** (see [Config](#config)). A bad config stops the run before any input is read.
2. **Checks the inputs.** It hashes the sample's `SHA256SUMS` and stops unless the hash equals the one pinned in the
   config. Then, for every train and heldout part of the chosen packs listed in `SHA256SUMS`, it looks for the file at
   `inputs/sample_v0/<split>/<pack>/<part>`, and otherwise for any Parquet file under `inputs/sample_v0/` with the same
   sha256 (so a renamed or regrouped copy is found too). A part that is missing, or whose bytes differ, stops the run
   before any work.
3. **Combines all parts into one set.** It reads `doc_id` and `text` of every document, in pack, split, part and row
   order. That order is the matrix row order. Each document is named **`<pack_id>-<doc_id>`**, for example
   `en-dclm-0086b8a3e2a24597`.
4. **Normalises each document into its H1 key** (the document itself is never changed):
   1. `normalize.match_key(text)` from `spec_v1/tools/normalize.py`, unchanged (spec v1 is frozen): HTML entities
      decoded, control and invisible characters removed, NFC with its listed folds, casefold, spaces collapsed.
   2. Then the H1 normalisation of `dedup_design_v1.md` on top: NFKC, casefold, every run of whitespace to one space.
      NFKC is applied here, never in `normalize.py`, so spec v1 and G9's fingerprints are unaffected.

   The SHA-256 of the key decides whether two documents are **exact** copies.
5. **Splits each key into shingles**: its set of word 5-grams (`the quick brown fox jumps`, `quick brown fox jumps
   over`, ...). A key under 5 words is one shingle, the whole key. An empty key has no shingles. Each shingle is
   stored as an 8-byte BLAKE2b digest.
6. **Scores every pair**: Jaccard = shingles in both / shingles in either. It does this exactly, for all
   N(N-1)/2 pairs, with no sampling and no MinHash estimate: the documents x shingles matrix X times its transpose,
   one block of rows at a time, gives the shared count for every pair that shares a shingle; every other pair scores 0.
   A shingle found in only one document is left out of X (it can never be shared) but still counts in that document's
   size. Two empty documents score 1.0.
7. **Writes the results** to `out/` (see [Outputs](#outputs)). Pairs at or above `floor` (default 0.5) are listed and
   stored in the matrix, **1.0 included**; the histogram counts every pair.

**Example.** Two 20-word documents that differ only in their last word have 16 shingles each. 15 are shared and 17 are
distinct in total, so the score is 15/17 = 0.882. The same document in capitals with extra spaces scores 1.0 and is
marked `exact`.

**What it does not do**
- It does not change, drop or rank documents, and it writes no document text: only IDs, scores and counts.
- It does not pick a survivor for each group of copies (`source_priority_v1.md`).
- It does not find translations (the H3 half that is out of scope for v1).
- It does not clean. It reads the sample parts as they are; `dedup_design_v1.md` runs dedup after `clean.py`, so on raw
  parts some copies that differ only in boilerplate score lower than they would after cleaning.

---

## Requirements

- **Python 3.9 or later**, with `numpy`, `scipy` and `pyarrow`:
  ```
  python3 -m pip install numpy scipy pyarrow
  ```
  Tested with Python 3.12, numpy 2.4.3 and scipy 1.18.1.
- **macOS or Linux.** The peak-memory measure uses the `resource` module, which Windows does not have.
- **No network and no keys.** The script reads only its inputs and writes only to `out/` in the repository root. It
  writes no `__pycache__` beside the scripts.
- **These files in the checkout**, all imported by `overlap.py`:

  | File | Role |
  |---|---|
  | `teams/01-data-a/dedup/overlap.py` | the job |
  | `teams/01-data-a/dedup/overlap_en.json` | its config for the four English packs |
  | `teams/01-data-a/dedup/h1_sha256.py` | the H1 key (`h1_key`) and the Parquet reader |
  | `teams/01-data-a/dedup/jaccard_matrix.py` | the shingles and the E1 thresholds |
  | `teams/01-data-a/spec_v1/tools/normalize.py` | spec v1 `match_key` (frozen) |

- **Time and memory.** One pack, en-dclm (61,975 documents), took 104 seconds with `jaccard_matrix.py`, the same
  method. The four packs together hold about four times as many documents; the wall time and peak memory of the full
  run are in its test log and in `overlap_summary.json` (`wall_seconds`, `peak_rss_mb`).

---

## Inputs

The **Week-2 tokenizer sample v0**, in `inputs/sample_v0/` in the repository root:

```
inputs/sample_v0/
  SHA256SUMS                                  the sample's list of parts and their sha256 (pinned in the config)
  train/<pack_id>/part-NNNNN.parquet
  heldout/<pack_id>/part-NNNNN.parquet
```

- **Every part needs a `doc_id` and a `text` column.** Other columns are ignored.
- **`SHA256SUMS` must have sha256 `0b7da76396a7078b07a5e5f96a4ced88279e77205c164a35f284f387b0546faa`**, the same pin as
  `teams/03-tokenizer/train/rebuild_c3_s0.json`.
- **Any layout below `inputs/sample_v0/` works**, because a part not at its expected path is found by its sha256. A
  symbolic link to a folder with the parts in another layout, such as `Cap1-packs/<pack>/Part_1/`, is followed.

The 12 parts that `overlap_en.json` reads, as listed in `SHA256SUMS`:

| Part | sha256 |
|---|---|
| `train/en-dclm/part-00000.parquet` | `67b305d60aa0f4091612f6fefe0c7aee867872943017c5ebb598293c19dfeb88` |
| `train/en-dclm/part-00001.parquet` | `0dec2d4fc09db2950d6f619810b6d2abf6d854b5d44d402c646cce2b74bd96a6` |
| `heldout/en-dclm/part-00000.parquet` | `60d0741e754b70dffab4398ca617b37a408121b2f60fed95f8cf871996aacc36` |
| `train/en-fineweb-edu/part-00000.parquet` | `53cbbf7a77b84e46108836c889e6cb83e6fcdc048c316fbf699586a7fef1dbe2` |
| `train/en-fineweb-edu/part-00001.parquet` | `bdd5d5b4f7aa8ec00e17865b5ebe13344728569aa7ffff7f37ba942b6fe42229` |
| `heldout/en-fineweb-edu/part-00000.parquet` | `727ee3f5ee0ef235fdd5839e516130e3b3fbb4a95345bfc827175f69ecd2647a` |
| `train/en-nemotroncc/part-00000.parquet` | `19d641f52f5fc9c884da2fc4b4df1bc0327d73e327c12abb8efe0201c1668fda` |
| `train/en-nemotroncc/part-00001.parquet` | `afba6a19de409e5208b3eb690ed360ad90aebb5c4cfd7f2bd389b468d2066202` |
| `heldout/en-nemotroncc/part-00000.parquet` | `76653abac4785a2a7b14931142af29f64d3d621e8ea0c26c8d729a82b29f7845` |
| `train/en-nemotroncc-synth/part-00000.parquet` | `a601748f22e32bfb839bdb76e8e645f3beae510460857eb206fbdf3ce53a2427` |
| `train/en-nemotroncc-synth/part-00001.parquet` | `03a9efeb92e210dcb5b32d350cdee60fa032d21ea9454cefc913b0785f55ae9f` |
| `heldout/en-nemotroncc-synth/part-00000.parquet` | `3fcbb50614d90f680168e0c95479e364e995a6ebbbdfc56df90746b58c38aff8` |

**Setting up the inputs on your own machine** (once, from the repository root). This copies `SHA256SUMS`, links a
folder that holds the parts instead of copying them, and keeps `inputs/` and `out/` out of git:

```
mkdir -p inputs/sample_v0
cp <download folder>/SHA256SUMS inputs/sample_v0/
ln -s <folder with the parts> inputs/sample_v0/packs
printf 'inputs/\nout/\n' >> .git/info/exclude
```

---

## Config

A JSON file. Keys starting with `_` are comments. Paths are relative to the repository root, the job's working
directory, and must not be absolute. An unknown key stops the run, so a misspelled key is never silently ignored.

| Key | Meaning | Default |
|---|---|---|
| `inputs` | the sample v0 folder | `inputs/sample_v0` |
| `sha256sums` | its `SHA256SUMS` | `<inputs>/SHA256SUMS` |
| `sha256sums_sha256` | the sha256 that `SHA256SUMS` must have | none: **required** |
| `packs` | pack IDs to compare, in this order | the four English packs |
| `splits` | `train` and/or `heldout` | both |
| `out` | output folder; must be inside `out/` | `out/overlap` |
| `floor` | list and store the pairs at or above this score; above 0 and at most 1 | `0.5` |
| `k` | words per shingle | `5` |
| `block` | matrix rows per step; lower it if memory runs short | `256` |
| `top` | how many top pairs to print at the end | `20` |
| `max_output_mb` | fail if the outputs are larger than this | `50` |

`overlap_en.json`, the config for the job:

```json
{
  "inputs": "inputs/sample_v0",
  "sha256sums_sha256": "0b7da76396a7078b07a5e5f96a4ced88279e77205c164a35f284f387b0546faa",
  "packs": ["en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"],
  "splits": ["train", "heldout"],
  "out": "out/overlap_en",
  "floor": 0.5,
  "k": 5,
  "block": 256,
  "top": 20,
  "max_output_mb": 50
}
```

---

## Run

From the repository root (the script finds `inputs/` and `out/` from the repository root, so it also works from any
other folder):

```
python teams/01-data-a/dedup/overlap.py --config teams/01-data-a/dedup/overlap_en.json
```

For a test log, run the same command with the network off and save its output:

```
python3 teams/01-data-a/dedup/overlap.py --config teams/01-data-a/dedup/overlap_en.json 2>&1 | tee teams/01-data-a/jobs/logs/<YYYY-MM-DD>-overlap-en-local.txt
```

**What it prints, in order**
1. `12 parts found and checked against inputs/sample_v0/SHA256SUMS`
2. One line per part: `<split>/<pack>/<part>: <n> documents (<seconds>s)`. This stage takes most of the time.
3. The document and shingle counts, and the number of intersection steps the scoring faces.
4. `rows <done>/<N>` lines with a time-left estimate.
5. The summary counts, the pack x pack tables at Jaccard 0.80, at 1.0 and exact, the top pairs, and the output size.

---

## Outputs

All in `out/overlap_en/` (the config's `out`), 50 MB or less in total (`max_output_mb`).

| File | What it holds |
|---|---|
| `overlap_pairs.csv` | every pair at or above `floor`, 1.0 included, highest score first |
| `overlap_by_pack.csv` | pack x pack pair counts at each level |
| `overlap_histogram.csv` | every pair, in score bins 0.01 wide |
| `overlap_matrix.npz` | the N x N score matrix |
| `overlap_docs.parquet` | which document each matrix row is |
| `overlap_summary.json` | all counts, the inputs, wall time, peak memory, versions, output sizes and hashes |

### `overlap_pairs.csv`

One row per pair at or above `floor`, sorted by score (highest first), then by row.

| Column | Meaning |
|---|---|
| `id_a`, `id_b` | the two documents, as `<pack_id>-<doc_id>`; `a` is always the earlier matrix row |
| `jaccard` | the score, 6 decimals |
| `shared_shingles` | the 5-grams the two have in common (0 for two empty documents) |
| `exact` | `True` if the two H1 keys are identical (same SHA-256) |
| `pack_a`, `split_a`, `part_a` | where document a is |
| `shingles_a` | how many distinct 5-grams document a has |
| `row_a` | document a's row in the matrix and in `overlap_docs.parquet` |
| `pack_b` ... `row_b` | the same for document b |

`exact` and a score of 1.0 are not the same thing: two documents with the same set of 5-grams score 1.0 even if the
order or repetition of their text differs, while `exact` means the normalised texts are identical.

### `overlap_by_pack.csv`

| Column | Meaning |
|---|---|
| `level` | the floor (`0.50`), each E1 threshold at or above it (`0.70` ... `0.95`), `1.00`, or `exact` |
| `pack_a`, `pack_b` | a pack pair; `en-dclm`, `en-dclm` counts pairs inside en-dclm |
| `pairs` | pairs of that pack pair at or above the level (for `exact`: exact pairs) |

Every pack pair appears at every level, with 0 where there is none.

### `overlap_histogram.csv`

`jaccard_from`, `jaccard_to`, `pairs`: 100 bins of 0.01 from 0.00 to 1.00 (the last bin includes 1.0). The counts add
up to every pair, N(N-1)/2, including the pairs that share no shingle, which fall in the first bin. Use it to see where
the gap between "same text" and "related text" sits (`dedup_design_v1.md`, experiment E1).

### `overlap_matrix.npz`

The full N x N matrix in scipy's sparse format: symmetric, 1 on the diagonal, row i is row i of
`overlap_docs.parquet`. **Only scores at or above `floor` are stored, so an empty cell means "below the floor", not 0.**
A dense matrix would not fit: N x N cells for about 250,000 documents is tens of billions of numbers.

```python
from scipy import sparse
import pyarrow.parquet as pq
M = sparse.load_npz("out/overlap_en/overlap_matrix.npz")
ids = pq.read_table("out/overlap_en/overlap_docs.parquet").column("id").to_pylist()
row = {doc: i for i, doc in enumerate(ids)}
M[row["en-dclm-0086b8a3e2a24597"], row["en-dclm-16319b1bf96d1124"]]   # their score, or 0 if below the floor
```

### `overlap_docs.parquet`

One row per document, in matrix row order: `row`, `id`, `pack`, `split`, `part`, `row_in_part`, `words` (in the H1
key) and `shingles` (distinct 5-grams). It is Parquet with zstd compression to stay under the output limit.

### `overlap_summary.json`

| Key | Meaning |
|---|---|
| `config` | the config as used, defaults filled in |
| `normalize_id`, `key`, `shingles` | spec v1's `NORMALIZE_ID`, and how the key and the shingles were made |
| `inputs` | the `SHA256SUMS` path and pin, and for each part: its name, sha256 and number of documents |
| `documents`, `documents_all` | documents per pack and split, and in total (N) |
| `ids_used_by_2_or_more_documents` | IDs that name two or more documents (the same `doc_id` in two parts of one pack); `split` and `part` tell them apart |
| `h1_exact_groups`, `documents_in_h1_exact_groups` | groups of documents with identical H1 keys, and the documents in them |
| `empty_documents` | documents with an empty key |
| `distinct_shingles`, `shingles_in_2_or_more_documents` | all distinct 5-grams, and the ones that can be shared |
| `pairs_compared` | N(N-1)/2 |
| `pairs_sharing_a_shingle` | pairs with a score above 0 (not counting pairs of empty documents) |
| `pairs_at_or_above` | pairs at or above 0.70, 0.75, 0.80, 0.85, 0.90 and 0.95, over all pairs, whatever the floor |
| `pairs_stored` | rows of `overlap_pairs.csv` |
| `pairs_by_pack` | the same counts as `overlap_by_pack.csv` |
| `wall_seconds`, `peak_rss_mb` | run time and peak memory |
| `versions` | Python, numpy, scipy, pyarrow and the platform |
| `outputs`, `output_mb` | each other output's size and sha256, and their total |

---

## Read the result

- **Exact copies**: `pairs_by_pack` → `exact`. For example, a count under `en-dclm x en-fineweb-edu` is that many pairs
  of identical documents across the two packs.
- **Near copies**: the `0.80` level is the H2 threshold proposed in `dedup_design_v1.md`; the levels from 0.70 to 0.95
  are the E1 sweep. Before relying on a threshold, read about 20 pairs just above and 20 just below it.
- **Held-out overlap**: pairs whose `split_a` or `split_b` is `heldout` and whose other side is `train` are held-out
  documents with a copy in training data.
- **Short documents score high easily.** In a 60-word document one changed word breaks 5 of about 56 shingles, so
  template pages that differ in one name or date score about 0.82 to 0.85.

---

## Errors

Every error stops the run with `ERROR: ...` and exit code 1. A missing `--config` stops it with exit code 2.

| Message | What to do |
|---|---|
| `unknown keys in <config>: [...]` | Fix the spelling of the key, or start it with `_` if it is a comment. |
| `<config> must pin sha256sums_sha256` | Add the sha256 of the sample's `SHA256SUMS`. |
| `inputs, sha256sums and out must be relative to the repository root` | Use paths like `inputs/sample_v0`, not `/Users/...`. |
| `floor must be above 0 and at most 1` | Set `floor`, for example 0.3 or 0.5. |
| `out must be inside out/ in the repository root` | Use an `out` like `out/overlap_en`. |
| `splits must be train and/or heldout` | Use `["train"]`, `["heldout"]` or both. |
| `no <path>/SHA256SUMS; put the sample v0 ...` | Set up `inputs/sample_v0/` (see [Inputs](#inputs)). |
| `<path> has sha256 <x>; the config pins <y>` | This is a different or edited `SHA256SUMS`. Use the sample's own file. |
| `<path> lists no train/heldout part for [...]` | A pack ID is misspelled or not in the sample. |
| `no file under <inputs> has the sha256 of <part>` | The part is missing, or its bytes differ from the sample's. Copy it again. |
| `<part> has no ['doc_id'] column` (or `text`) | The file is not a sample part. |
| `needs numpy, scipy and pyarrow` | `python3 -m pip install numpy scipy pyarrow` |
| `<n> document(s); nothing to compare` | The chosen parts hold fewer than 2 documents. |
| `the outputs are <x> MB, over max_output_mb <y>; raise floor` | The outputs were written but are too large. Raise `floor`, for example to 0.6. |

---

## Tests

```
python3 -B -m pytest teams/01-data-a/dedup/tests/test_overlap.py -q -p no:cacheprovider
```

22 tests on made-up documents in a temporary folder; nothing is read from or written to the real `inputs/` or
`out/`. They check:
- the scores, `exact` flags and IDs of hand-built pairs: the same text after case and spacing changes, after NFKC
  (`r²` and `r2`), two empty documents, two documents under 5 words, and a one-word edit scoring exactly 15/17;
- every score, matrix cell and histogram bin against a brute-force Jaccard of all pairs of 62 random documents;
- the order and details of the pairs, the summary counts, the matrix and the documents table;
- that outputs stay in `out/` and match the hashes in the summary;
- that a moved part is found by its sha256, and that a changed part, a missing pack, a wrong `SHA256SUMS` pin and
  outputs over the limit stop the run;
- that each kind of bad config is refused before any work, and that defaults are filled in.

`-B` and `-p no:cacheprovider` keep `__pycache__` and `.pytest_cache` folders out of the repository.
