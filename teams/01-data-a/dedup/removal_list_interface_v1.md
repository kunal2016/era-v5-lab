# Removal lists and the remover: interface v1

Status: proposal for the Clean → Dedup → F2 pipeline task (Sourav Dhar). Owners of the list format: Data A dedup (Kunal Sinha, Aneesha Das). 12 Nov 2026.

Stages that **decide** what to remove (dedup, F2) write a removal list. One tool, `apply_removals.py`, **applies** a list to the Parquet parts. It never decides, never edits text, and every removal can be undone from its log. This note fixes the list format, the checks the remover makes and the order of the passes, so each stage can be built and tested on its own.

## The pipeline with the remover

```
clean.py ─▶ cleaned parts (+ manifest)
              │
              ├─▶ overlap.py ─▶ dedup.py ─▶ remove_list.csv, dedup_groups.csv, dedup_summary.json
              │
              ▼
   remover pass 1: apply_removals.py --parts cleaned/ --list dedup/remove_list.csv
              │                      → deduped parts, removals.jsonl, apply_summary.json
              ▼
   F2 (G9 fingerprints) on the deduped parts ─▶ f2_remove_list.csv (same format)
              │
              ▼
   remover pass 2: apply_removals.py --parts deduped/ --list f2/f2_remove_list.csv --groups dedup/dedup_groups.csv
              │                      → final parts, removals.jsonl, apply_summary.json (+ groups lost to F2)
              ▼
   final parts ─▶ shard writer (#358)
```

Two passes, not one combined list: each list is checked against the parts it was computed on (dedup's against the cleaned parts, F2's against the deduped parts), F2's rows never point at rows dedup already removed, and each summary shows what that stage removed (TSAI, 12 Nov: Clean, then Dedup, then F2).

## The removal list (CSV, UTF-8, header row)

| Column | Example | Meaning |
|---|---|---|
| `pack_id` | `cadj-commits` | Pack of the document |
| `split` | `train` | `train` or `heldout`. **Required**: train and held-out parts share part names, and an exact copy can share its `doc_id` across splits (dedup rule 0 removes the train copy and keeps the held-out one) |
| `part` | `cadj-commits/part-00000.parquet` | Part path relative to the split folder, as in the cleaned sample |
| `row_in_part` | `62` | 0-based row of the document in that part, in the parts the list was computed on |
| `doc_id` | `a847a350bfac3252` | The document's ID; checked against the row |
| `reason` | `H1`, `H2`, `F2` | Why it is removed (added in dedup v1.1; until then, read from `dedup_log.jsonl`) |
| `stage` | `dedup`, `f2` | Which stage decided (added in dedup v1.1; until then, implied by the list) |

The key is `(pack_id, split, part, row_in_part)`, and `doc_id` must match at that row. `dedup.py` already writes the first five columns (`remove_list.csv`). F2 writes the same columns for the deduped parts.

Each list comes with its producer's summary JSON, which records the SHA-256 of every part the list was computed on (dedup v1.1: carried from `overlap_summary.json`, which today has `checksum_verification: deferred`).

## What the remover checks, and refuses

It stops before writing anything if:
1. a row's part does not exist, or `row_in_part` is outside the part;
2. the `doc_id` at `row_in_part` is not the listed `doc_id` (the list was computed on other parts);
3. a part's SHA-256 does not match the producer's summary (once the summaries record it; until then checks 1–2 are the guard, and they do not catch a text-only change);
4. the same key appears twice in one list.

It never refuses F2 removing a dedup survivor: that removal stands, no other copy is promoted, and the group is reported (below).

## What the remover writes

| Output | Contents |
|---|---|
| `<out>/{train,heldout}/<pack>/<part>.parquet` | The parts without the listed rows: same schema, same part names, same row order otherwise, text untouched |
| `removals.jsonl` | One line per removed document: its key, `doc_id`, `reason`, `stage`, the list file and its SHA-256 |
| `apply_summary.json` | Per pack and split: documents in, removed by reason, documents out; the SHA-256 of every input list and every output part; the input manifest's `clean.py` hash; the harm check; with `--groups`, the groups lost to F2 |
| `groups_lost.csv` (pass 2, with `--groups`) | For each dedup group whose survivor F2 removed: `group_id`, group size, the removed survivor's key, and whether any other survivor of the group remains (groups can have several held-out survivors) |

`--restore <out> --log removals.jsonl` puts the removed rows back; the result must be byte-identical to the input parts.

## Harm check

Over the documents that pass removed, matched on `(pack_id, doc_id)` against the gold folders. Dedup's rule is **zero**: `fail` if any gold document is removed, `not_testable` if no gold ID is in the input (as `dedup.py` reports; sample v0 contains no gold IDs, so the real harm evidence is the run on the week-1 diagnosis packs). For F2's pass, report gold removed separately; G9 sets F2's tolerance.

## Not inputs to the remover

- `empty_documents.csv`: for cleaning (a spec v1.1 rule), not removed here.
- `heldout_duplicates.csv`: for G3. If held-out documents must leave training, that comes as one more list with its own `reason`.

## Tests the remover needs

1. Every listed row is removed and nothing else; text is byte-identical.
2. A missing row or a `doc_id` mismatch at `row_in_part` is refused.
3. A train and a held-out document with the same part name and `doc_id`: only the listed one is removed.
4. A part-hash mismatch is refused (once hashes are recorded).
5. F2 removes a dedup survivor: the removal stands and the group appears in `groups_lost.csv`; a group with another held-out survivor is marked as not lost entirely.
6. Pass 1 then pass 2 gives the expected final set; `--restore` gives the input back byte-identical.
7. The same inputs give byte-identical outputs on every run and OS.

## Changes this needs elsewhere

| Where | Change | When |
|---|---|---|
| `overlap.py` | SHA-256 of every input part in `overlap_summary.json` | Dedup v1.1 |
| `dedup.py` | Carry those hashes into `dedup_summary.json`; add `reason` and `stage` to `remove_list.csv` | Dedup v1.1, after TSAI's dedup run |
| F2 runner | Write its removals in this format, computed on the deduped parts | Pipeline task |
| `apply_removals.py` | New tool as above | Pipeline task |

Pass 1 can run on today's `remove_list.csv`: checks 1, 2 and 4 work without the v1.1 changes.
