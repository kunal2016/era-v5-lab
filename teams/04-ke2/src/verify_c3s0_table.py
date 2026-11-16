#!/usr/bin/env python3
"""Check that a locally built raw byte table is the C3-s0 table the frozen bf16 codes were built from.

The raw table is not committed (lab rule, 15 Nov: commit the build script, the config and the
SHA-256 of the table, not the table). A trainer or loader that needs the file rebuilds it with
``build_bf16_codes.py --write-raw-table`` (or ``build_tables.py --tokenizer <C3-s0 tokenizer.json>``)
and then runs this script on the result. It passes only if the file

* is a Team 4 format-v2 ``raw`` table at the frozen P, bound to the C3-s0 tokenizer SHA-256,
* has the content hash recorded in ``results/bf16/bf16_codes_P{P}.npz`` (``raw_table_sha256``),
  so it is byte for byte the table Team 4 built and checked.

No tokenizer file is needed. Exit status 0 and one line ``OK ...`` on success, 1 otherwise.

Usage:
  python verify_c3s0_table.py PATH/raw_table_P32.npz [--pos-dim 32] [--codes DIR]
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_bf16_codes import codes_path
from ke2.bf16_codes import Bf16Codes
from ke2.config import BF16_DIR, BF16_POS_DIM, C3S0_NAME, C3S0_TOKENIZER_SHA256
from ke2.tables import ByteTable, TableContractError


def verify(table_path: Path, codes_file: Path, tokenizer_sha256: str = C3S0_TOKENIZER_SHA256) -> dict:
    """Return the matching hashes; raise ``TableContractError`` if the table is not the recorded one."""
    codes = Bf16Codes.load(codes_file, tokenizer_sha256=tokenizer_sha256)
    table = ByteTable.load(table_path, tokenizer_sha256=tokenizer_sha256)
    codes.check_table(table)  # kind, P, tokenizer and content hash
    if table.n_truncated:
        raise TableContractError(f"{table_path}: {table.n_truncated} truncated rows; the frozen table has none")
    if table.n_empty_rows:
        raise TableContractError(f"{table_path}: {table.n_empty_rows} empty rows; the frozen table has none")
    return {
        "table": str(table_path),
        "vocab_size": table.vocab_size,
        "pos_dim": table.pos_dim,
        "tokenizer_sha256": table.tokenizer_sha256,
        "raw_table_sha256": table.sha256(),
        "codes_sha256": codes.sha256(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", type=Path, help="a raw_table_P{P}.npz built locally from the C3-s0 tokenizer")
    ap.add_argument("--pos-dim", type=int, default=BF16_POS_DIM)
    ap.add_argument("--codes", type=Path, default=BF16_DIR, help="folder holding the committed bf16_codes_P{P}.npz")
    a = ap.parse_args(argv)
    try:
        r = verify(a.table, codes_path(a.codes, a.pos_dim))
    except (TableContractError, FileNotFoundError, KeyError, ValueError) as e:
        print(f"FAIL {a.table}: {e}", file=sys.stderr)
        return 1
    print(
        f"OK {r['table']}: {C3S0_NAME} raw table, V={r['vocab_size']}, P={r['pos_dim']}, "
        f"sha256 {r['raw_table_sha256']} matches the frozen bf16 codes ({r['codes_sha256'][:12]}…)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
