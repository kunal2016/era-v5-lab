# Shard format v0 (draft)

How the cleaned packs become token shards for training. A draft to agree with G3 (tokenizer) and G7 (infrastructure)
before anything is written at scale. The manifest template is `shard_manifest_v0.template.json`.

**Sample:** `sample/` is one complete shard, `code-go-train-000000`: 266 docs, 262,109 tokens (about 1 MiB; a real shard
is 2^26 tokens), from `code-go` part-00001 of the tokenizer sample v0 after `clean.py` and F2. It has every file below plus
`cleaning_pipeline.json`, and `code-go-train-000000.dump.md` describes it. `make_sample_shard.py` made it and checks it:
G6's `open_shard` reads the `.bin`, the sizes and the index match the manifest, and every doc decodes back to its text.
The `.bin` and `.docs.parquet` are here only as a sample for review: pr-guard refuses them in a PR, so they come out
before this is merged.

## Files of one shard

| File | What | Format |
|---|---|---|
| `<shard_id>.bin` | the token IDs | G6's Brahmic shard, unchanged: a 1,024-byte header (256 little-endian int32: magic `20261025`, version `2`, token count, then zeros), then the tokens as little-endian uint32 |
| `<shard_id>.idx.npy` | where each document starts | `np.save` of int64, `doc_count + 1` entries: the start offset of each document, then `token_count` |
| `<shard_id>.docs.parquet` | sample metadata, one row per document in shard order | `doc_id`, input part, row in that part, `n_tokens`, `lang_label`. IDs only, no text |
| `<shard_id>.json` | the manifest | `shard_manifest_v0.template.json` |

- **Why G6's `.bin`:** `teams/06-performance/dataio/loader.py` opens it today, so the perf loader reads our shards with no
  change; the `.idx.npy` is extra and that loader ignores it.
- **uint32:** the vocab is 131,072, above the uint16 limit of 65,535.
- **Documents, not packed sequences:** each document is its tokens followed by one EOS. A shard is not cut into
  fixed-length samples, so the sequence length is a training setting (8k now, 16k later, same shards). The `.idx.npy`
  gives the document boundaries for document masking.
- **A document is never split across shards.** A shard is filled up to about 2^26 tokens (256 MiB); a document longer than that gets a shard
  of its own. The header's int32 count caps a shard at 2^31 − 1 tokens.
- **One pack and one split per shard,** so mixture weights can be set per pack and language by choosing shards.
- **`payload_bytes = 1,024 + 4 × token_count`**, which G6's loader checks.

## Manifest fields

| Field | Meaning |
|---|---|
| `schema_version` | the manifest layout, `shard-v0` |
| `dataset_version` | the corpus release this shard belongs to |
| `shard_id` | `<pack_id>-<split>-<6 digits>`, unique within the release |
| `format`, `token_dtype` | how to read the `.bin` |
| `payload_uri`, `payload_sha256`, `payload_bytes` | the `.bin`: where, its hash, its size |
| `index_uri`, `index_sha256` | the `.idx.npy`: hashed separately, so a broken index is caught too |
| `doc_count`, `token_count` | documents and tokens in the shard, EOS included |
| `eos_token_id` | the token after each document (open, see G3 below) |
| `tokenizer_sha256` | sha256 of the `tokenizer.json` bytes that made the IDs |
| `pack_id`, `language`, `script`, `domain`, `capability_lane`, `split` | what is in the shard. `split` is `train` or `validation` only: test and benchmark data are never sharded (eval firewall, G9 #269) |
| `inputs_sha256` | sha256 of the sorted lines `<input_sha256> <part>` of the input parts `run_clean.py` read (from its summaries) |
| `cleaning_pipeline_sha256` | sha256 of `cleaning_pipeline.json`: the `clean.py` sha256, the F2 fingerprint set and the dedup version |
| `decontam_set_sha256` | the G9 fingerprint set F2 checked against (v2 today). A new set means rechecking every shard with an older one |
| `sample_metadata_*`, `quality_report_*` | links to what is kept outside the manifest, with hashes |
| `created_by` | the git commit of the shard writer |

A manifest never changes after it is written.

## Dataset level

```
corpus-v1/
  SHA256SUMS                 every .json, .bin and .idx.npy of the release, sorted by path
  admission.jsonl            append-only: {"shard_id", "payload_sha256", "license_status", "admission_status", "reason", "date"}
  cleaning_pipeline.json
  <pack_id>/<split>/<shard_id>.{bin,idx.npy,docs.parquet,json}
  <pack_id>/quality_report.json
```

- **License and admission live in `admission.jsonl`, not in the manifest.** They can change (a license revoked, a leak
  found); the manifest and the shard do not. The latest row for a shard wins.
- **A run pins its shard list:** the admitted shards at the start of a run, as `<payload_sha256>  <shard_id>` lines. Its
  sha256 is the `manifest` in the loader state (G7's loader contract), so a resume on another list is refused.

## Kept outside the manifest

| What | Where |
|---|---|
| Document IDs, source IDs, per-document language and provenance | `<shard_id>.docs.parquet` |
| Dedup, contamination and held-out overlap results | `quality_report.json` |
| License and admission status | `admission.jsonl` |
| Sequence length, mixture weights, curriculum | training config |
| OPUS accept/reject decisions | OPUS records |
| Samples consumed per step, resume position | training ledger and checkpoint (G7) |
| Cache location, scheduling | runtime |

## Open with G3 (tokenizer)

1. **Which tokenizer, and when.** C1–C3 are to be retrained on the Data A tokenizer sample (G3 COMPARE.md, Thu 12 Nov), so the final
   sha256 is not known yet. Shards are written only after G3 freezes one `tokenizer.json` and its sha256; any change after
   that means rewriting every shard.
2. **The end-of-document token.** G6's shards end each document with `<|end_of_text|>` (id 36); G10 named
   `<|endoftext|>` (id 130,822) as its end-of-document marker (G3 `v0/special_slots.md`). One ID for pretraining, agreed by G3
   and G10.
3. **BOS and language tags.** Is a token put before each document (`<|begin_of_text|>`, or a `lang_slot` tag: the 32 slots at
   130,886–130,917 are not named yet)? If yes, G3 names the slots and the shard writer adds them.
4. **The normalizer is inside `tokenizer.json`** (C3 / v1 normalizer). We tokenize cleaned text through that file only and
   apply no normalizer of our own, so data and training match. G3 to confirm.
5. **Where the 7.7 MB `tokenizer.json` is fetched from** (it is not in the repo), with its sha256, for the shard writer and the loader.
6. **Throughput.** Tokenizing the full corpus: one process per pack part, batch encode. G3 to say if their encoder has a faster path.

## Open with G7 (infrastructure)

1. **Where shards live.** Shared file system or the S3-compatible store (the same two `ckpt/store.py` supports); the path or bucket and prefix,
   who may write, and whether training nodes read it directly or through a local cache.
2. **Shard size.** About 256 MiB (2^26 tokens) proposed: their object-size limits, upload part size, and whether `V5_VERIFY_MODE=head` (the store's
   checksum at upload) is enough for data too, or a full sha256 at load.
3. **The loader contract.** The loader state is one global offset, the skip list and `manifest` = the sha256 of the run's
   shard list. Teams 01/02 own the loader and run `ckpt/loader_contract.py` on it. Agree that the shard list format above is
   what `manifest` hashes.
4. **A shard revoked mid-run.** Removing it changes the shard list, so a resume is refused (`DataManifestError`). Is
   the answer a new branch on the new list, or the skip list?
5. **The global sampler.** How a global offset maps to (shard, document, window) at any world size, so a resharded resume gives
   the same global batch (`_reshard_check`). Who owns the sampler: Data or G7?
6. **The ledger.** Whether the training ledger logs `(shard_id, document range)` per step, or only the offset (the sampler then replays it).

## Not done yet

- The shard writer for real packs (`make_sample_shard.py` writes one shard from one cleaned part, with the checks).
- The loader and its run of `ckpt/loader_contract.py`.
- The `capability_lane` values: from the training plan.
