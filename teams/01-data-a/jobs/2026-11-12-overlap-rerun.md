# Overlap rerun on the #244 cleaning of sample v0 — Thursday 12 November 2026

**DRAFT: not ready to submit.** Before this request goes to TSAI, fill in the items marked TODO (the #255 commit, the
code changes since `86ecdd4` and a fresh local test log), and confirm the input path with the #244 cleaning job.

```text
Team:            01-data-a
Owner:           Aneesha Das (aneeshads)
Lead approval:   Pending team-lead review/approval on the job-request PR
Question:        On the sample v0 cleaned with #244, what share of documents in each source has an H1 exact or eligible H2 near duplicate in each source, including its own?
Script:          teams/01-data-a/dedup/overlap.py (with h1_sha256.py, jaccard_matrix.py, overlap_rules.py, overlap_report.py and the frozen spec v1 normalize.py), PR #255 at commit TODO
Command:         python teams/01-data-a/dedup/overlap.py --config teams/01-data-a/dedup/overlap.json
Config:          teams/01-data-a/dedup/overlap.json (unchanged from the 5 Nov run: the 38 sample-v0 packs)
Inputs:          All 38 sample-v0 packs from TSAI's #244 cleaning job (run after #244 merges), staged under ./out/tokenizer_sample_v0_clean/{train,heldout}/; each Parquet row has pack_id, doc_id and text. Not the 3 Nov cleaned parts
Hardware:        CPU (single process; request 2 vCPU and 32 GiB RAM; no GPU)
Max time:        90 minutes
Precision:       not used
Measures:        Directional source-by-source document shares; matched-document numerators and source denominators; H1/H2 qualifying pairs; raw word-Jaccard threshold sweep and histogram; pack/part/split document counts; wall time, peak RSS, versions and output SHA-256
Expected result: 38 x 38 source matrix with values in [0,1], potentially asymmetric; counts to be measured. The 5 Nov run on the 3 Nov cleaning gives the scale, not expected values: 1,416,236 documents, 2,711 qualifying pairs (98 H1, 2,613 H2; 50 cross-pack), 7 empty documents, 56 minutes, 9.6 GiB peak
Outputs:         out/overlap/{overlap_matrix.csv,overlap_matrix_counts.csv,overlap_matches.csv,overlap_pairs.csv,overlap_by_pack.csv,overlap_histogram.csv,overlap_matrix.npz,overlap_docs.parquet,overlap_summary.json}; 50 MiB maximum including summary
Test log:        TODO: a local run of overlap.py at the commit above (overlap_local.json), saved under teams/01-data-a/jobs/logs/
```

## Why a rerun

TSAI answered in G1 on 12 Nov: #244 changes the cleaner, so the cleaned sample of 3 Nov is out of date. TSAI runs the
#244 cleaning job on sample v0 after #244 is merged. The overlap measurement is then run again on the new cleaned output,
and the `dedup.py` job (`2026-11-10-dedup.md`) is approved and run on that output. The 5 Nov results
(`2026-11-04-overlap.md`) are not used.

This is the same measurement as `2026-11-04-overlap.md`, on new inputs. That request describes the method, the matrix
definition and the H1/H2 scope; they are unchanged and are not repeated here. The full method and reproduction commands
are in `dedup/README_overlap.md`.

## What changed since the 5 Nov run

| | 5 Nov run | This run |
|---|---|---|
| Cleaned input | #244's cleaner as of 3 Nov | #244's cleaner as merged (it changed on 10, 11 and 12 Nov) |
| Code | PR #255 at `86ecdd4` | PR #255 at the commit above. `h1_sha256.py` now finds `normalize.py` both where #244 puts it and where it was before. TODO: list any other change to the five scoring files since `86ecdd4` |
| Rules | v1: prose 0.80 and 50 words, math 0.90 and the same numbers, code 0.85 tokens and 20 lines | The same, unless the team changes a rule before this request is submitted (open: the math numbers rule, same-URL pairs, a lower Indic word minimum from E4). A change after submission needs another run |
| Max time | 60 minutes (it took 56) | 90 minutes, for headroom |

If #244 changes the contents of `normalize.py`, and not only its place, the H1 keys change. The run records what it
used, so this shows in the results; it is not assumed either way.

## Inputs and execution

Stage the cleaned parts returned by the #244 cleaning job in `out/tokenizer_sample_v0_clean/train/` and
`out/tokenizer_sample_v0_clean/heldout/`, as on 5 Nov. That folder must hold only the new parts: move the 3 Nov parts
aside first. The #244 runner refuses an existing output folder, so they are likely moved for the cleaning job anyway. If
the cleaning job writes elsewhere, stage its parts here, or change `inputs` in `overlap.json` and say so in the run log.

`overlap.json` asserts the exact 38-pack inventory before scoring; a missing or unexpected pack fails. Packs that #244's
cleaner does not support pass through it unchanged and are still in the inventory.

Install `teams/01-data-a/dedup/requirements_overlap.txt` (`numpy`, `scipy`, `pyarrow`, pinned `pygments==2.21.0`);
Python 3.9+ on Linux or macOS. No network access or keys; all output stays under `out/`. Stop at 90 minutes and return
the partial console log if the limit is reached; incomplete output must not be used.

## Returned artifacts

Return the nine output files and the console log to `teams/01-data-a/jobs/results/2026-11-12-overlap-rerun/`, as
described in `JOB_REQUEST.md`. On 5 Nov, `overlap_docs.parquet` (34 MB) and `overlap_pairs.csv` (6.7 MB) stayed out of
the repository and were sent separately. Please send them again the same way: `dedup.py` needs `overlap_docs.parquet`,
and the matrix confirmation, E4 and the hand review need both.

## After the results return

1. Rebuild and confirm the matrix: `python teams/01-data-a/dedup/confirm_matrix.py --results <returned folder>`, and
   with `--docs` once `overlap_docs.parquet` is here. Replace `teams/01-data-a/dedup/overlap_matrix.csv` with the
   confirmed matrix and update `matrix_confirmation.md`.
2. Run `dedup.py` locally on the returned files without urls and add its counts to `2026-11-10-dedup.md`; then the lead
   approves that job.
3. Run `e4_review.py` again on the new outputs before an Indic reader labels the pairs.
4. Replace the 5 Nov numbers in `results_v1.md`, `dedup_design_v1.md` and `source_priority_v1.md`.
