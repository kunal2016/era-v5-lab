#!/usr/bin/env python3
"""Build the frozen bf16 KE2 codes from the raw byte table, bound to the C3-s0 tokenizer.

Steps: load the tokenizer (refused unless its SHA-256 is the pinned C3-s0 hash), build the raw
table at P, read the per-length bf16 code values from the upstream float32 codec, then run the
codec on every token and require its bf16 output to equal the rows rebuilt from the compact
values, bit for bit. Every row is hashed on the way; the matrix is never held in memory.

Outputs (default ``teams/04-ke2/results/bf16/``):
  bf16_codes_P{P}.npz    compact codes: ``high_bits``/``low_bits`` (P + 1,) uint16 bf16 patterns, index L,
                         plus tokenizer, raw-table, codes, matrix and row-hash SHA-256 (committed)
  bf16_codes_P{P}.json   the config: shapes, layout, EOS, codec source, and the same hashes (committed)
  materialized/bf16_matrix_P{P}.npy   with ``--materialize`` only: the ``(V, D)`` matrix as uint16 bf16
                         bits (2 GiB at P = 32; git-ignored). Load with
                         ``torch.from_numpy(np.load(path)).view(torch.bfloat16)``.

Usage:
  python build_bf16_codes.py [--tokenizer PATH] [--pos-dim 32] [--out DIR] [--materialize]

``--tokenizer`` defaults to ``$KE2_C3S0_TOKENIZER``. Takes about two minutes at P = 32 on an M1.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import logging
import os
import sys
import time
from collections.abc import Sequence
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from ke2.bf16_codes import BF16_FORMAT, Bf16Codes, codes_for_table, stream_rows
from ke2.config import (
    BF16_DIR,
    BF16_POS_DIM,
    C3S0_NAME,
    C3S0_TOKENIZER_ENV,
    C3S0_TOKENIZER_SHA256,
    EOS_ID,
    EOS_TOKEN,
    UPSTREAM_CODEC_COMMIT,
)
from ke2.tables import ByteTable, TableContractError, build_raw_table
from ke2.tokenizer import TokenizerBundle, load_tokenizer
from ke2.upstream import ensure_kronecker_embeddings

log = logging.getLogger("build_bf16_codes")


def codes_path(out_dir: Path, pos_dim: int) -> Path:
    return Path(out_dir) / f"bf16_codes_P{pos_dim}.npz"


def config_path(out_dir: Path, pos_dim: int) -> Path:
    return Path(out_dir) / f"bf16_codes_P{pos_dim}.json"


def matrix_path(out_dir: Path, pos_dim: int) -> Path:
    return Path(out_dir) / "materialized" / f"bf16_matrix_P{pos_dim}.npy"


def tokenizer_arg(arg: str | None) -> str:
    path = arg or os.environ.get(C3S0_TOKENIZER_ENV)
    if not path:
        raise SystemExit(f"pass --tokenizer or set ${C3S0_TOKENIZER_ENV} to the C3-s0 tokenizer.json")
    return path


def check_eos(tb: TokenizerBundle) -> None:
    a = tb.added.get(EOS_ID)
    if a is None or a.get("content") != EOS_TOKEN or EOS_ID not in tb.special_ids:
        raise TableContractError(f"id {EOS_ID} is not the special token {EOS_TOKEN!r} in {tb.path}")


def build(tb: TokenizerBundle, pos_dim: int, *, materialize: Path | None = None, chunk_rows: int = 1024):
    """Raw table, compact codes with their matrix hashes, and the stream result."""
    table = build_raw_table(tb, pos_dim)
    codes = codes_for_table(table)
    out = None
    if materialize is not None:
        materialize.parent.mkdir(parents=True, exist_ok=True)
        out = np.lib.format.open_memmap(
            materialize, mode="w+", dtype=np.uint16, shape=(table.vocab_size, codes.output_dim)
        )
    res = stream_rows(codes, table, chunk_rows=chunk_rows, verify_codec=True, out=out)
    if out is not None:
        out.flush()
        del out
    codes.matrix_sha256 = res.matrix_sha256
    codes.row_hashes_sha256 = res.row_hashes_sha256
    return table, codes, res


def config_dict(tb: TokenizerBundle, table: ByteTable, codes: Bf16Codes, npz_name: str) -> dict:
    P, D, V = codes.pos_dim, codes.output_dim, codes.vocab_size
    return {
        "format": BF16_FORMAT,
        "tokenizer": {
            "name": C3S0_NAME,
            "file": tb.path.name,
            "sha256": tb.sha256,
            "vocab_size": tb.vocab_size,
            "special_ids": len(tb.special_ids),
            "eos": {"id": EOS_ID, "content": EOS_TOKEN},
        },
        "raw_table": {
            "kind": table.kind,
            "pos_dim": P,
            "shape": list(table.bytes.shape),
            "n_truncated": table.n_truncated,
            "n_empty_rows": table.n_empty_rows,
            "sha256": table.sha256(),
            "rebuild": "ke2.tables.build_raw_table(tokenizer, P); not committed",
        },
        "codec": {
            "char_dim": codes.char_dim,
            "pos_dim": P,
            "output_dim": D,
            "source": "kronecker_embeddings.codec.kronecker_codec (float32) then .to(torch.bfloat16)",
            "upstream_commit": UPSTREAM_CODEC_COMMIT,
            "torch": importlib.metadata.version("torch"),
        },
        "compact": {
            "file": npz_name,
            "arrays": {"high_bits": [P + 1], "low_bits": [P + 1]},
            "dtype": "uint16 bit patterns of bfloat16, indexed by byte length L",
            "sha256": codes.sha256(),
            "hash_rule": f"sha256('{BF16_FORMAT}|P|char_dim|tokenizer_sha256|raw_table_sha256|' + high_bits + low_bits, uint16 LE)",
        },
        "matrix": {
            "shape": [V, D],
            "dtype": "bfloat16",
            "bytes": V * D * 2,
            "layout": "row t: low[L_t] everywhere, high[L_t] at index byte * P + position for position < L_t",
            "sha256": codes.matrix_sha256,
            "hash_rule": "sha256 of the row-major little-endian bf16 bytes, no header",
            "row_hashes_sha256": codes.row_hashes_sha256,
            "row_hashes_rule": "sha256 of the (V, 32) array of per-row sha256 digests, in id order",
            "file": f"materialized/bf16_matrix_P{P}.npy (uint16 bits, only with --materialize; not committed)",
        },
        "verified": "every row of the codec's bf16 output equals the row rebuilt from the compact codes, bit for bit",
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizer", default=None, help=f"C3-s0 tokenizer.json (default: ${C3S0_TOKENIZER_ENV})")
    ap.add_argument("--pos-dim", type=int, default=BF16_POS_DIM)
    ap.add_argument("--out", type=Path, default=BF16_DIR)
    ap.add_argument("--materialize", action="store_true", help="also write the (V, D) bf16 matrix as .npy")
    ap.add_argument("--chunk-rows", type=int, default=1024)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ensure_kronecker_embeddings()

    tb = load_tokenizer(tokenizer_arg(a.tokenizer), expected_sha256=C3S0_TOKENIZER_SHA256)
    check_eos(tb)
    log.info("tokenizer %s: %s (V=%d, sha256=%s…)", C3S0_NAME, tb.path, tb.vocab_size, tb.sha256[:12])
    t0 = time.perf_counter()
    mpath = matrix_path(a.out, a.pos_dim) if a.materialize else None
    table, codes, _ = build(tb, a.pos_dim, materialize=mpath, chunk_rows=a.chunk_rows)
    npz = codes_path(a.out, a.pos_dim)
    codes.save(npz)
    cfg = config_dict(tb, table, codes, npz.name)
    config_path(a.out, a.pos_dim).write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    log.info("raw table sha256   %s", table.sha256())
    log.info("codes sha256       %s", codes.sha256())
    log.info("matrix sha256      %s  (%d x %d bf16)", codes.matrix_sha256, codes.vocab_size, codes.output_dim)
    log.info("row-hashes sha256  %s", codes.row_hashes_sha256)
    if mpath is not None:
        log.info("materialized       %s", mpath)
    log.info("wrote %s and %s in %.0f s", npz, config_path(a.out, a.pos_dim), time.perf_counter() - t0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
