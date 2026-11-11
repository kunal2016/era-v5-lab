"""Write one sample shard in the v0 format (shard_format_v0.md) from a cleaned pack part, check it, and describe it.

  python teams/01-data-a/shards/make_sample_shard.py --clean <out>/code-go_part-00001_clean.parquet \
      --summary <out>/code-go_part-00001_summary.json --language go --script Latn --lane code --out <dir>

The input is run_clean.py --f2 output: docs clean.py kept and F2 (G9 fingerprints) did not drop. Docs are taken in order
until the next one would pass --tokens; a doc is never split. A doc whose text looks like it holds an email address or a
secret (pr-guard's patterns) is skipped and counted.
Writes <dir>/<shard_id>.{bin,idx.npy,docs.parquet,json}, cleaning_pipeline.json and <shard_id>.dump.md (a readable
description: header, index, metadata, never text).
Tokenizer: G6's BrahmicTokenizer-131K (pinned) and EOS id 36, as G6's shards; both are open with G3.
The .bin is written and read with G6's own write_shard / open_shard. Needs numpy, pyarrow, tokenizers and torch.
"""
import argparse
import hashlib
import json
import re
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

# pr-guard's secret and email patterns (.github/workflows/pr-guard.yml)
SECRET = re.compile("|".join([
    r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"gh[pousr]_[A-Za-z0-9]{30,}", r"\bsk-[A-Za-z0-9_-]{20,}",
    r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9][A-Za-z0-9._%+-]*@(?!users\.noreply\.github\.com\b|example\.(?:com|org)\b)"
    r"(?:[A-Za-z0-9-]+\.)+(?:com|org|net|edu|gov|mil|int|in|io|ai|co|uk|us|me|dev|app|info|biz|ac|ca|au|de|fr|jp|sg|ae)\b"]),
    re.IGNORECASE)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--clean", type=Path, required=True, help="a *_clean.parquet from run_clean.py --f2")
ap.add_argument("--summary", type=Path, required=True, help="its *_summary.json")
ap.add_argument("--language", required=True)
ap.add_argument("--script", required=True)
ap.add_argument("--lane", required=True, help="capability_lane")
ap.add_argument("--split", default="train", choices=["train", "validation"])
ap.add_argument("--tokens", type=int, default=2 ** 18, help="fill the shard up to this many tokens (real shards: 2^26)")
ap.add_argument("--out", type=Path, required=True)
a = ap.parse_args()
a.out.mkdir(parents=True, exist_ok=True)

s = json.loads(a.summary.read_text(encoding="utf-8"))
if "f2" not in s:
    sys.exit(f"{a.summary}: no F2 in this run; shards are made only from run_clean.py --f2 output")
pack_id, shard_id = s["pack_id"], f"{s['pack_id']}-{a.split}-000000"
tok = BrahmicTokenizer()
eos = tok.spec["model"]["vocab"]["<|end_of_text|>"]  # 36, as G6's shards; open with G3 and G10

table = pq.read_table(a.clean, columns=["doc_id", "text", "lang_label"])
docs, rows, skipped, total = [], [], 0, 0
for row, (doc_id, text, lang) in enumerate(zip(*(table.column(c).to_pylist() for c in ("doc_id", "text", "lang_label")))):
    if SECRET.search(text):
        skipped += 1
        continue
    ids = tok.encode(text) + [eos]
    if total + len(ids) > a.tokens:
        break
    docs.append((text, ids))
    rows.append({"doc_id": doc_id, "input_part": a.clean.name, "input_row": row, "n_tokens": len(ids), "lang_label": lang})
    total += len(ids)
if not docs:
    sys.exit("no document fits in --tokens")

starts = np.cumsum([0] + [r["n_tokens"] for r in rows]).astype("<i8")  # doc_count + 1 entries, the last is token_count
bin_path, idx_path, meta_path = (a.out / f"{shard_id}{x}" for x in (".bin", ".idx.npy", ".docs.parquet"))
write_shard(bin_path, [t for _, ids in docs for t in ids])
np.save(idx_path, starts)
pq.write_table(pa.Table.from_pylist(rows), meta_path)
pipeline = a.out / "cleaning_pipeline.json"
pipeline.write_text(json.dumps({"clean_py_sha256": s["clean_py_sha256"], "f2_set_sha256": s["f2"]["set_sha256"],
                                "dedup": None}, indent=2) + "\n", encoding="utf-8", newline="\n")

token_count = int(starts[-1])
commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
manifest = {
    "schema_version": "shard-v0", "dataset_version": "sample", "shard_id": shard_id,
    "format": "brahmic_u32_v2+doc_index", "token_dtype": "uint32",
    "payload_uri": bin_path.name, "payload_sha256": sha(bin_path), "payload_bytes": bin_path.stat().st_size,
    "index_uri": idx_path.name, "index_sha256": sha(idx_path),
    "doc_count": len(docs), "token_count": token_count, "eos_token_id": eos,
    "tokenizer_sha256": TOKENIZER_SHA256,
    "pack_id": pack_id, "language": a.language, "script": a.script, "domain": s["family"], "capability_lane": a.lane,
    "split": a.split,
    "inputs_sha256": hashlib.sha256(f"{s['input_sha256']} {s['pack']}\n".encode("utf-8")).hexdigest(),
    "cleaning_pipeline_sha256": sha(pipeline), "decontam_set_sha256": s["f2"]["set_sha256"],
    "sample_metadata_uri": meta_path.name, "sample_metadata_sha256": sha(meta_path),
    "quality_report_uri": None, "quality_report_sha256": None,
    "created_by": commit,
}
(a.out / f"{shard_id}.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")

# Check the shard against its manifest, reading the .bin the way G6's loader does.
tokens = open_shard(bin_path)
idx = np.load(idx_path)
meta = pq.read_table(meta_path)
assert manifest["payload_bytes"] == HEADER_BYTES + 4 * token_count and len(tokens) == token_count <= a.tokens
assert idx[0] == 0 and idx[-1] == token_count and len(idx) == len(docs) + 1 == meta.num_rows + 1
assert meta.column("n_tokens").to_pylist() == np.diff(idx).tolist()
for k, (_, ids) in enumerate(docs):
    assert tokens[idx[k]:idx[k + 1]].tolist() == ids and ids[-1] == eos
roundtrip = sum(tok._encoder.decode(ids[:-1]) == text for text, ids in docs)

header = np.fromfile(bin_path, dtype="<i4", count=3)
n = meta.num_rows
lines = [f"# Sample shard `{shard_id}`\n\n",
         f"Made by `make_sample_shard.py` from `{s['pack']}` of `{pack_id}` (tokenizer sample v0, train), after `clean.py` "
         f"and F2 (fingerprints `{s['f2']['set_sha256'][:12]}`). The first {n:,} docs of the cleaned part that fit in "
         f"{a.tokens:,} tokens; {skipped} doc(s) skipped for an email-like or secret-like string. A real shard is filled to "
         f"2^26 tokens.\n\nTokenizer: BrahmicTokenizer-131K as pinned by G6 (`{TOKENIZER_SHA256[:12]}`); EOS id {eos} as G6's "
         "shards. Both are open with G3.\n\n",
         "| file | bytes | sha256 |\n|---|---:|---|\n",
         *(f"| `{p.name}` | {p.stat().st_size:,} | `{sha(p)[:16]}…` |\n" for p in (bin_path, idx_path, meta_path, pipeline)),
         f"\n## `{bin_path.name}`\n\n- header, {HEADER_BYTES:,} bytes = 256 little-endian int32: `{header[0]}` (magic), "
         f"`{header[1]}` (version), `{header[2]:,}` (token count), then zeros\n"
         f"- then {token_count:,} little-endian uint32 token IDs; every doc ends with {eos}\n"
         f"- checks: G6's `open_shard` reads it; size = {HEADER_BYTES:,} + 4 × {token_count:,}; each doc's tokens equal "
         f"a fresh encode; {roundtrip:,} of {n:,} docs decode back to their text exactly\n\n",
         f"## `{idx_path.name}`\n\nint64, {n + 1:,} entries (start of each doc, then token_count): "
         f"`{idx[:5].tolist()} … {idx[-2:].tolist()}`\n\n",
         f"## `{meta_path.name}`\n\nOne row per doc in shard order, IDs only. First rows:\n\n"
         "| doc_id | input_part | input_row | n_tokens | lang_label |\n|---|---|---:|---:|---|\n",
         *(f"| `{r['doc_id']}` | `{r['input_part']}` | {r['input_row']:,} | {r['n_tokens']:,} | {r['lang_label']} |\n"
           for r in rows[:5]),
         f"\nDoc length in tokens: min {min(r['n_tokens'] for r in rows):,}, median "
         f"{int(np.median([r['n_tokens'] for r in rows])):,}, max {max(r['n_tokens'] for r in rows):,}.\n"]
(a.out / f"{shard_id}.dump.md").write_text("".join(lines), encoding="utf-8", newline="\n")
print(f"{shard_id}: {n} docs, {token_count} tokens, {skipped} skipped, {roundtrip}/{n} decode exactly, checks pass -> {a.out}")
