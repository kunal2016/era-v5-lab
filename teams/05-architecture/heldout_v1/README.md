# Held-out set v1 (G5): sample for review, and what comes next

**Owner:** Deepjyoti Saha (G5). **Reviewers:** Shivanshu Thapliyal (G5 lead), Rohan Shravan (instructor, TSAI).

This folder holds G5's held-out set, the fixed text on which models are scored in bits per byte
([`experiments/plan_v1.md`](https://github.com/theschoolofai/era-v5-lab/blob/main/teams/05-architecture/experiments/plan_v1.md)).
The held-out text is **one file, `data/heldout_v1.jsonl`**, with 15 slices one after the other.
**This PR has a sample**, 20 documents per slice, so the harness can be tested now and the approach can be checked
before the full set is built. The full set replaces this file on Mon 2 Nov, with the same script and name, and
`results/heldout_v1.sha256` names it.

## Purpose

- **Score the week-2 experiments.** Every arm of plan v1 (EXP-1 to EXP-5, the attention arms, the T3 confirms) is scored
  on exactly the same text, so the winner rule compares like with like.
- **Score the final V5 model** (and the dry-run checkpoints) on the same text, with the same metric.
- **Check that the experiments were a faithful small-scale copy of the real thing.** The week-2 choices are made on small
  test models (T1 to T3) and a small training stream. Scoring the final model on the same held-out text shows whether
  those choices still hold at full size, on the real data mix. Bits per byte makes this possible: it does not depend on
  the model size or on the tokenizer.
- **Give the lab one fixed, reproducible, benchmark-free text** for any team that needs a perplexity check.

Because of the second and third points, the set is **permanent**: its bytes are frozen once the full set is built, and it
must never be trained on.

## Rules every source follows

1. A split its makers set aside (validation or test), so no one's *train* split contains it.
2. An accepted licence: [ODC-By 1.0](https://opendatacommons.org/licenses/by/1-0/) or [MIT](https://opensource.org/license/mit).
3. Not a benchmark: Team 9's fingerprint check
   ([`teams/09-evaluation/decontam/`](https://github.com/theschoolofai/era-v5-lab/blob/main/teams/09-evaluation/decontam/README.md)) flags 0 documents.
4. Not Team 1 or Team 2 data: their data is V5's own training data.
5. Close to one of V5's data packs, so the final model is scored on the kind of text it learns from.

## Layout

| Path | What |
|---|---|
| `data/heldout_v1.jsonl` | The held-out text: one file, 15 slices; each id starts with its slice |
| `data/heldout_v1_sources.jsonl` | **Source tracking**: where each document came from (see below) |
| `data/SHA256SUMS` | The **sample's** checksums of both JSONL files (see "Checksums" below) |
| `data/heldout_manifest.json` | Selection rule, pinned dataset revisions, excluded documents with the reason, the file's documents, text bytes and sha256; per slice: dataset, part, id prefix, documents, text bytes, documents skipped for personal data |
| `heldout_decontam_v1.txt` | Output of Team 9's check on the file |
| `build_heldout.py` | Rebuilds `data/` byte for byte |
| `.gitattributes` | Keeps the data files byte for byte on every operating system, so the sha256 values stay valid |

## Composition (this sample)

| Slice | Id prefix | Dataset | Part | Docs | Text bytes |
|---|---|---|---|---|---|
| English web | `c4-val` | [allenai/c4](https://huggingface.co/datasets/allenai/c4) | en/c4-validation.00000-of-00008.json.gz | 20 | 35,259 |
| Indic: Hindi | `fw2-hi-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | hin_Deva test | 20 | 168,897 |
| Indic: Bengali | `fw2-bn-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | ben_Beng test | 20 | 168,896 |
| Indic: Tamil | `fw2-ta-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | tam_Taml test | 20 | 146,109 |
| Indic: Telugu | `fw2-te-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | tel_Telu test | 20 | 247,821 |
| Indic: Kannada | `fw2-kn-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | kan_Knda test | 20 | 169,563 |
| Indic: Malayalam | `fw2-ml-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | mal_Mlym test | 20 | 144,730 |
| Indic: Marathi | `fw2-mr-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | mar_Deva test | 20 | 108,632 |
| Indic: Gujarati | `fw2-gu-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | guj_Gujr test | 20 | 147,451 |
| Indic: Punjabi | `fw2-pa-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | pan_Guru test | 20 | 220,946 |
| Indic: Odia | `fw2-or-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | ory_Orya test | 20 | 82,276 |
| Indic: Assamese | `fw2-as-test` | [HuggingFaceFW/fineweb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | asm_Beng test | 20 | 253,230 |
| Math | `owm-test` | [EleutherAI/proof-pile-2](https://huggingface.co/datasets/EleutherAI/proof-pile-2) | open-web-math/test/test.jsonl.zst | 20 | 80,135 |
| Science | `pes2o-val` | [allenai/peS2o](https://huggingface.co/datasets/allenai/peS2o) | data/v2/validation-00000-of-00002.json.gz | 20 | 27,677 |
| Code (Python, C++, Go, Java, JavaScript, Rust) | `vault-<lang>-test` | [Fsoft-AIC/the-vault-function](https://huggingface.co/datasets/Fsoft-AIC/the-vault-function) | data/test/{python,cpp,go,java,javascript,rust} | 20 | 17,695 |
| **`data/heldout_v1.jsonl`** | | | | **300** | **2,019,317** |

Text bytes = the sum of `len(text.encode("utf-8"))`, the denominator of bits per byte. The JSON quotes and line breaks
are not counted. The full set takes about 0.25 MB of text per slice instead of 20 documents.
To score a single slice, keep the lines whose id starts with its prefix.

### Why these sources

| Slice | Source | Why |
|---|---|---|
| English | [C4](https://huggingface.co/datasets/allenai/c4) `en`, validation | A released split of a cleaned web crawl; close to V5's English packs (DCLM, FineWeb-Edu, Nemotron-CC); one of the most-reported language-model evaluation texts. |
| Indic (11 languages) | [FineWeb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2), test | V5's Indic packs come from FineWeb-2's train side; its test split is the same kind of text, set aside by its makers. It covers all 11 G3 languages. |
| Math | [OpenWebMath](https://huggingface.co/datasets/open-web-math/open-web-math) (in [Proof-Pile-2](https://huggingface.co/datasets/EleutherAI/proof-pile-2)), test | Web math pages, close to V5's FineMath and MegaMath packs. ODC-By 1.0. |
| Science | [peS2o](https://huggingface.co/datasets/allenai/peS2o) v2, validation | Academic papers, close to the FinePDFs science pack. |
| Code | [The Vault](https://huggingface.co/datasets/Fsoft-AIC/the-vault-function) (function level), test | Built from permissively licensed GitHub code ([The Stack](https://huggingface.co/datasets/bigcode/the-stack)). Its test split covers all six languages of V5's code packs. Only functions whose repo licences are all permissive are kept. |

Not used, with the reason: Team 1/2 data (it is V5's training data); benchmarks such as FLORES, IN22, MILU, MMLU,
GSM8K, HumanEval and MBPP (lab rule); our own carve-out of FineWeb (not a released split); mC4 validation (no Odia
or Assamese); Sangraha, HPLT and CulturaX (no held-out split, and likely training sources); arXiv (licences vary per paper);
codeparrot-clean (unstated licences); CodeSearchNet (licence "other", widely used as a benchmark); The Stack v2 (gated, no
split); [Paloma](https://huggingface.co/datasets/allenai/paloma) (gated, mixed licences; a possible later slice to compare with outside models).

## How documents are chosen

Rows in the order the source stores them (code: the six languages in turn); text stripped; empty texts skipped; code only when every repo licence is permissive; a document with an email address, a phone number or a secret-looking string is skipped (no personal data in the repo, and pr-guard rejects emails); stop at --docs documents or once --mb megabytes of text are reached. No shuffling, no other filtering.

Dataset revisions are pinned, so a rebuild gives the same bytes:

- [`EleutherAI/proof-pile-2`](https://huggingface.co/datasets/EleutherAI/proof-pile-2/tree/901a9273a770e9d4138c5ddd91802f9c5c6cdc4b) at `901a9273a770e9d4138c5ddd91802f9c5c6cdc4b`
- [`Fsoft-AIC/the-vault-function`](https://huggingface.co/datasets/Fsoft-AIC/the-vault-function/tree/505c679056e49a2a269b64777ee7c496d22e1440) at `505c679056e49a2a269b64777ee7c496d22e1440`
- [`HuggingFaceFW/fineweb-2`](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2/tree/af9c13333eb981300149d5ca60a8e9d659b276b9) at `af9c13333eb981300149d5ca60a8e9d659b276b9`
- [`allenai/c4`](https://huggingface.co/datasets/allenai/c4/tree/1588ec454efa1a09f29cd18ddd04fe05fc8653a2) at `1588ec454efa1a09f29cd18ddd04fe05fc8653a2`
- [`allenai/peS2o`](https://huggingface.co/datasets/allenai/peS2o/tree/636a503e44a3ca1b58e01fb61eab0825cd574de0) at `636a503e44a3ca1b58e01fb61eab0825cd574de0`

Documents dropped after Team 9's check, with the reason (also in the manifest):

- `owm-test-000011`: shares 13-word runs with LiveCodeBench release_v6 items (coverage 1%); fingerprints v1, 1 Nov 2026

## Format

One JSON object per line, UTF-8: `{"id": "...", "text": "..."}`. Ids are unique and say where the text came from:
`c4-val-000000`, `fw2-hi-test-000000`, `owm-test-000000`, `pes2o-val-000000`, `vault-py-test-000000`.

## Source tracking

`data/heldout_v1_sources.jsonl` has one line per document, in the same order and with the same `id` as
`heldout_v1.jsonl`, so any document can be traced back to its source, attributed, or removed:

| Field | Meaning | Example |
|---|---|---|
| `id` | joins to `heldout_v1.jsonl` | `fw2-hi-test-000003` |
| `slice` | the slice | `hi` |
| `dataset`, `revision` | Hugging Face dataset and pinned revision | `HuggingFaceFW/fineweb-2`, `af9c1333…` |
| `file`, `row` | the file in that dataset, and the row number in it (counting rows that were skipped) | `data/hin_Deva/test`, `3` |
| `source_id` | the source's own key where it has one: FineWeb-2 and peS2o `id`; for code `path@hexsha` | |
| `url` | the page URL (C4, FineWeb-2, OpenWebMath); for code, the GitHub repository | |
| `licence` | ODC-By-1.0, or for code the repository's licences (all permissive) | `Apache-2.0` |
| `text_sha256` | sha256 of the document's text, so anyone can check it was not changed | |

It is also the list the Data teams and Team 9 can use to keep these documents out of training: by URL and source id,
not only by our id. Documents whose URL or source id contains an email address or phone number are skipped like the
text itself.

## Checksums

- **Sample (this PR):** `data/SHA256SUMS` holds the sha256 of both files:

  ```
  51805f10ab9bdfe75722205d82d3a5d3e152e72d9ddd5d689818803a646c18c7  heldout_v1.jsonl
  65f5eca9bc5c1a379869c7bfb18076c90c4413d6ee3d9d96f7b220a3a26f0d33  heldout_v1_sources.jsonl
  ```

  Check it from `data/` with `sha256sum -c SHA256SUMS` (Linux, macOS, Git Bash), or in PowerShell with
  `Get-FileHash heldout_v1.jsonl -Algorithm SHA256`. The script writes this file on every build.
- **Final set (Mon 2 Nov):** plan v1 names the scored held-out set by `results/heldout_v1.sha256`. That file is written
  only for the full set, so the sample can never be mistaken for it. Until it exists, no arm is scored for the record.

## Rebuild it

From the repo root (needs `pip install datasets zstandard`, and network access to Hugging Face):

```
python teams/05-architecture/heldout_v1/build_heldout.py --out teams/05-architecture/heldout_v1/data --docs 20   # this sample
python teams/05-architecture/heldout_v1/build_heldout.py --out teams/05-architecture/heldout_v1/data --mb 0.25   # the full set
```

A rebuild of this sample into an empty folder gave the same `heldout_v1.jsonl`, `heldout_v1_sources.jsonl`, manifest and `SHA256SUMS`, byte for byte. TSAI jobs run without
network ([`JOB_REQUEST.md`](https://github.com/theschoolofai/era-v5-lab/blob/main/JOB_REQUEST.md)), so they read the committed files, not the script.

## Benchmark check (Team 9)

`heldout_decontam_v1.txt` is the output of Team 9's
[`decontam_check.py`](https://github.com/theschoolofai/era-v5-lab/blob/main/teams/09-evaluation/decontam/decontam_check.py) on `data/heldout_v1.jsonl`, full fingerprint set:

```
fingerprints v1 set_sha256 11e290a44d1467875fdf8bebc55eab21f0a6367f411aab98a4a027a546fd372e (full set)
docs 300 flagged 0 (0.00%) by benchmark {}
```

It is repeated on the full set, and again on fingerprints v2 (due Wed 4 Nov).

## What comes next

| When | What | Who |
|---|---|---|
| Now (this PR) | The sample: the harness owner tests loading, tokenization and bits per byte; the lead and TSAI review the approach and the open points below | Udit; Shivanshu, Rohan |
| Mon 2 Nov | **The full set**: the same script with `--mb 0.25` (about 0.25 MB of text per slice, about 3.75 MB, over 1M tokens), same file names in `data/`; Team 9's check on the full fingerprint set; `results/heldout_v1.sha256` written, naming the scored file; this README's tables updated | Deepjyoti |
| Tue 3 Nov onward | EXP-1 and every later arm scored on it; one bits per byte per slice (lines selected by id prefix) and pooled | Udit's harness, arm owners |
| Wed 4 Nov | Re-check on Team 9's **fingerprints v2** (new cleaning rule `spec-v1`, plus Terminal-Bench 2 and BFCL v3); its `set_sha256` added next to v1's | Deepjyoti, Team 9 |
| Being agreed | **Protection**: Team 9 fingerprints this set as a protected set, so every training shard is checked against it; the Data teams' dedup excludes copies, using `heldout_v1_sources.jsonl` | Team 9, Teams 1 and 2 |
| When spec v1 code lands | **Cleaned copy** (`heldout_v1_clean`): Team 1 and Team 2's final cleaning run on the set, then Team 9's check; both scored from then on | Deepjyoti |
| Later (v1.1, separate slices) | A whole-file code slice; possibly a Paloma slice to compare with outside models; possibly a "temporal" slice (text newer than any training crawl) | to be decided |

The v1 bytes never change once the full set is built. Anything new is a separate, named slice or file.

## Open points for the lead and TSAI to confirm

1. **Permanent and protected.** This set also scores the dry runs and the final model, so it must stay out of all training.
   Proposal: Team 9 fingerprints it as a protected set, so every training shard is checked against it, copies included.
2. **Which slice decides week-2 winners.** The arms train on English text. Proposal: English decides, and every slice is
   reported.
3. **Size.** About 0.25 MB of text per slice in the full set (15 slices in one file of about 3.75 MB, over 1M tokens). Fixed before any
   arm is scored.
4. **Cleaning.** No cleaning spec is approved yet. Proposal: freeze the raw set now, and add a cleaned copy
   (`heldout_v1_clean`) when Team 1 and Team 2's spec v1 code lands, then run Team 9's check on it.
5. **Code is function level.** The Vault gives single functions with their docstrings, not whole files. A whole-file
   code slice can follow in v1.1.

## Licences and attribution

[C4](https://huggingface.co/datasets/allenai/c4), [FineWeb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2),
[OpenWebMath](https://huggingface.co/datasets/open-web-math/open-web-math) (via [Proof-Pile-2](https://huggingface.co/datasets/EleutherAI/proof-pile-2)) and
[peS2o](https://huggingface.co/datasets/allenai/peS2o) are under [ODC-By 1.0](https://opendatacommons.org/licenses/by/1-0/); users should also
follow the [Common Crawl terms of use](https://commoncrawl.org/terms-of-use). [The Vault](https://huggingface.co/datasets/Fsoft-AIC/the-vault-function)
is under [MIT](https://opensource.org/license/mit) and is built from permissively licensed code.
No text was changed except for stripping leading and trailing white space.
