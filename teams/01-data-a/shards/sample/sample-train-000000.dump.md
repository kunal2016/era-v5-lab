# Sample shard `sample-train-000000`

Made by `make_sample_shard.py` from three made-up documents; the `.bin`, `.idx.npy` and `.docs.parquet` are not committed (pr-guard). Tokenizer: BrahmicTokenizer-131K as pinned by G6; EOS id 36 as G6's shards (both open with G3).

## `sample-train-000000.bin` (1,232 bytes)

- header, 1,024 bytes = 256 little-endian int32: `20261025` (magic), `2` (version), `52` (token count), then zeros
- then 52 little-endian uint32 token IDs:

```
sample-0001: 47 422 4038 4773 422 297 1 3373 0 1 978 4 1 1662 2 36
sample-0002: 473 492 151 31973 0 135 415 100 1 245 37153 8 2739 492 1 24580 2447 2 36
sample-0003: 1857 497 4788 802 1316 161 7 49 2 11143 3223 112 737 112 737 11 36
```

## `sample-train-000000.idx.npy`

int64, doc_count + 1 entries (start of each doc, then token_count): `[0, 16, 35, 52]`

## `sample-train-000000.docs.parquet`

| doc_id | input_part | input_row | n_tokens | lang_label |
|---|---|---:|---:|---|
| `sample-0001` | made-up | 0 | 16 | en |
| `sample-0002` | made-up | 1 | 19 | en |
| `sample-0003` | made-up | 2 | 17 | en |

## `sample-train-000000.json`

The manifest, next to this file.
