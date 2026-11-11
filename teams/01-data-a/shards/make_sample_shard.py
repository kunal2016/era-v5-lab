"""Write one sample shard in the v0 format (shard_format_v0.md) from three made-up documents, check it, and print it.

  python teams/01-data-a/shards/make_sample_shard.py --out <dir>

Writes <dir>/sample-train-000000.{bin,idx.npy,docs.parquet,json} and <dir>/sample-train-000000.dump.md.
Only the .json and the .dump.md are committed (sample/): pr-guard refuses .bin and .parquet files.
Uses G6's tokenizer (BrahmicTokenizer-131K, pinned) and G6's write_shard / open_shard, so the .bin is G6's format.
The final tokenizer and the EOS id are still open with G3: the sample uses G6's (id 36).
Needs numpy, pyarrow, tokenizers and torch (G6's dataio imports torch).
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "teams" / "06-performance"))
from dataio.loader import HEADER_BYTES, open_shard  # noqa: E402
from dataio.prepare_fineweb import write_shard  # noqa: E402
from dataio.tokenizer import BrahmicTokenizer, SHA256 as TOKENIZER_SHA256  # noqa: E402

SHARD_ID = "sample-train-000000"
DOCS = [  # made up for this sample
    ("sample-0001", "The water cycle moves water between the sea, the air and the land."),
    ("sample-0002", "To add two fractions, first give them the same denominator.\nThen add the numerators."),
    ("sample-0003", "def area(r):\n    return 3.14159 * r * r\n"),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--out", type=Path, required=True)
out = ap.parse_args().out
out.mkdir(parents=True, exist_ok=True)

tok = BrahmicTokenizer()
eos = tok.spec["model"]["vocab"]["<|end_of_text|>"]  # 36, as G6's shards; open with G3 and G10
docs = [tok.encode(text) + [eos] for _, text in DOCS]
starts = np.cumsum([0] + [len(d) for d in docs]).astype("<i8")  # doc_count + 1 entries, the last is token_count

bin_path, idx_path, meta_path = (out / f"{SHARD_ID}{s}" for s in (".bin", ".idx.npy", ".docs.parquet"))
write_shard(bin_path, [t for d in docs for t in d])
np.save(idx_path, starts)
pq.write_table(pa.table({"doc_id": [i for i, _ in DOCS], "input_part": ["made-up"] * len(DOCS),
                         "input_row": list(range(len(DOCS))), "n_tokens": [len(d) for d in docs],
                         "lang_label": ["en"] * len(DOCS)}), meta_path)

token_count = int(starts[-1])
commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
manifest = {
    "schema_version": "shard-v0", "dataset_version": "sample", "shard_id": SHARD_ID,
    "format": "brahmic_u32_v2+doc_index", "token_dtype": "uint32",
    "payload_uri": bin_path.name, "payload_sha256": sha(bin_path), "payload_bytes": bin_path.stat().st_size,
    "index_uri": idx_path.name, "index_sha256": sha(idx_path),
    "doc_count": len(docs), "token_count": token_count, "eos_token_id": eos,
    "tokenizer_sha256": TOKENIZER_SHA256,
    "pack_id": "sample", "language": "en", "script": "Latn", "domain": "web", "capability_lane": "general_language",
    "split": "train",
    "inputs_sha256": hashlib.sha256(json.dumps(DOCS).encode("utf-8")).hexdigest(),
    "cleaning_pipeline_sha256": None, "decontam_set_sha256": None,  # made-up docs: not cleaned, not F2-checked
    "sample_metadata_uri": meta_path.name, "sample_metadata_sha256": sha(meta_path),
    "quality_report_uri": None, "quality_report_sha256": None,
    "created_by": commit,
}
(out / f"{SHARD_ID}.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")

# Check the shard against its manifest, reading it the way G6's loader does.
tokens = open_shard(bin_path)
idx = np.load(idx_path)
assert manifest["payload_bytes"] == HEADER_BYTES + 4 * token_count == len(tokens) * 4 + HEADER_BYTES
assert idx[0] == 0 and idx[-1] == token_count and len(idx) == manifest["doc_count"] + 1
for k, (_, text) in enumerate(DOCS):
    doc = tokens[idx[k]:idx[k + 1]]
    assert doc[-1] == eos and tok._encoder.decode(doc[:-1].tolist()) == text

header = np.fromfile(bin_path, dtype="<i4", count=4)
lines = [f"# Sample shard `{SHARD_ID}`\n\n",
         "Made by `make_sample_shard.py` from three made-up documents; the `.bin`, `.idx.npy` and `.docs.parquet` are not "
         "committed (pr-guard). Tokenizer: BrahmicTokenizer-131K as pinned by G6; EOS id 36 as G6's shards (both open with G3).\n\n",
         f"## `{bin_path.name}` ({manifest['payload_bytes']:,} bytes)\n\n",
         f"- header, 1,024 bytes = 256 little-endian int32: `{header[0]}` (magic), `{header[1]}` (version), "
         f"`{header[2]}` (token count), then zeros\n- then {token_count} little-endian uint32 token IDs:\n\n```\n"]
for k, (doc_id, _) in enumerate(DOCS):
    lines.append(f"{doc_id}: {' '.join(map(str, tokens[idx[k]:idx[k + 1]].tolist()))}\n")
lines += ["```\n\n", f"## `{idx_path.name}`\n\nint64, doc_count + 1 entries (start of each doc, then token_count): "
          f"`{idx.tolist()}`\n\n", f"## `{meta_path.name}`\n\n| doc_id | input_part | input_row | n_tokens | lang_label |\n"
          "|---|---|---:|---:|---|\n"]
lines += [f"| `{d}` | made-up | {k} | {len(docs[k])} | en |\n" for k, (d, _) in enumerate(DOCS)]
lines.append(f"\n## `{SHARD_ID}.json`\n\nThe manifest, next to this file.\n")
(out / f"{SHARD_ID}.dump.md").write_text("".join(lines), encoding="utf-8", newline="\n")
print(f"{SHARD_ID}: {len(docs)} docs, {token_count} tokens, checks pass, written to {out}")
