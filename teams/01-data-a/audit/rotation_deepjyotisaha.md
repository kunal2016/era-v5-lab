# Rotation check, deepjyotisaha

Week 3 rotation in Team 01 Data A (R1 and R2). The task is to check 2 tokenized shards for manifest fields, hashes,
and token counts, and to file each problem as an issue.

**Status: DRAFT.** The two shards are not assigned yet. Tejaskumar assigns two real shard ids per rotator when TSAI
returns the first shards (week-3 plan, R1.1). This file shows the checks that will be run and the shape of the
results. No result is claimed until the tables below are filled in from the actual files.

## Shards

| | Shard id | Pack | Split | Where the files were read |
|---|---|---|---|---|
| 1 | _to be assigned_ | | | TSAI download link (not recorded here) |
| 2 | _to be assigned_ | | | TSAI download link (not recorded here) |

Checked against main `<commit>` on `<date>`.

## The checks

Each check compares a value recomputed from the files with the value the manifest records. The rules come from
`teams/01-data-a/shards/shard_format_v1.md` and `shard_manifest_v1.template.json`.

| # | Check | How |
|---|---|---|
| 1 | Manifest fields | Every field of `shard_manifest_v1.template.json` is present and filled; `schema_version` is `shard-v1` |
| 2 | Payload sha256 | sha256 of the `.bin` bytes (header included) equals `payload_sha256` |
| 3 | Payload size | `.bin` size equals `payload_bytes` and 1,024 + 4 × `token_count` |
| 4 | Header | magic `20261025`, version `2`, header token count equals `token_count` |
| 5 | Index sha256 | sha256 of the `.idx.npy` equals `index_sha256` |
| 6 | Index | int64, starts at 0, strictly increasing, last entry equals `token_count`; length − 1 equals `doc_count` |
| 7 | Document metadata | sha256 of the `.docs.parquet` equals `sample_metadata_sha256`; one row per document; sum of `n_tokens` equals `token_count` |
| 8 | Quality report | sha256 equals `quality_report_sha256` |
| 9 | Tokenizer | `tokenizer_sha256` is the frozen C3 hash `15468e66457b43af79f695cbe585c0d03e3cfe7a4a5d04d189dd3c6b9f02ddc3` |
| 10 | EOS | `eos_token_id` is `130822`; every document ends with it |
| 11 | Decontamination set | `decontam_set_sha256` equals `f2_set_sha256` in the shard's `cleaning_pipeline.json` |
| 12 | Writer | `created_by` names a commit of the shard writer |

## Shard 1: _to be assigned_

| # | Check | Manifest | Recomputed | Match |
|---|---|---|---|---|
| 1 | Manifest fields | | | |
| 2 | Payload sha256 | | | |
| 3 | Payload size | | | |
| 4 | Header | | | |
| 5 | Index sha256 | | | |
| 6 | Index | | | |
| 7 | Document metadata | | | |
| 8 | Quality report | | | |
| 9 | Tokenizer | | | |
| 10 | EOS | | | |
| 11 | Decontamination set | | | |
| 12 | Writer | | | |

## Shard 2: _to be assigned_

| # | Check | Manifest | Recomputed | Match |
|---|---|---|---|---|
| 1 | Manifest fields | | | |
| 2 | Payload sha256 | | | |
| 3 | Payload size | | | |
| 4 | Header | | | |
| 5 | Index sha256 | | | |
| 6 | Index | | | |
| 7 | Document metadata | | | |
| 8 | Quality report | | | |
| 9 | Tokenizer | | | |
| 10 | EOS | | | |
| 11 | Decontamination set | | | |
| 12 | Writer | | | |

## Problems filed (R2)

None yet. Each problem gets one issue in the lab repo with the shard and manifest identity, the expected and observed
value, how to reproduce it, and its severity. A problem already covered by an open issue (for example issue 448, the
missing second shard on main) is linked, not filed again. No document text and no download links go in an issue.
