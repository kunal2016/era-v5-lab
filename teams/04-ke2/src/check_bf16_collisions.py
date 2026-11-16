#!/usr/bin/env python3
"""Collision checks on the frozen bf16 KE2 codes (C3-s0), including special tokens.

Two tokens have the same bf16 row only if one of these holds; each is checked explicitly:

  A  identical bytes and length (the raw table is not injective)
  B  bf16 rounding makes ``high[L] == low[L]`` for some length L (the support disappears)
  C  bf16 rounding makes two different lengths produce the same ``(high, low)`` pair

Then, end to end: every row of the ``(V, D)`` bf16 matrix (rebuilt in chunks from the committed
compact codes and the raw table) is hashed with SHA-256 and the digests are searched for
duplicates. Equal rows give equal digests, so zero duplicate digests proves zero equal rows.
The special tokens (``special: true`` in the tokenizer's ``added_tokens``) are checked on their
own: ids 36 and 130822 (EOS ``<|endoftext|>``) must be among them, and no special token's row may
equal any other row. The matrix and row-hash SHA-256 must equal the values the builder recorded.

Outputs (default ``teams/04-ke2/results/bf16/``): ``bf16_collisions_P{P}.json`` and the short
results page ``bf16_collisions_P{P}.md``. Exit status 1 if any check fails.

Usage:
  python check_bf16_collisions.py [--tokenizer PATH] [--pos-dim 32] [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from build_bf16_codes import codes_path, tokenizer_arg
from ke2.bf16_codes import Bf16Codes, float_to_bits, stream_rows
from ke2.codec import code_values
from ke2.config import BF16_DIR, BF16_POS_DIM, C3S0_NAME, C3S0_TOKENIZER_SHA256, EOS_ID, EOS_TOKEN
from ke2.tables import ByteTable, build_raw_table
from ke2.tokenizer import TokenizerBundle, load_tokenizer

log = logging.getLogger("check_bf16_collisions")

REQUIRED_SPECIAL_IDS = (36, EOS_ID)
"""Special ids Gate 3 names: 36 (``<|end_of_text|>``) and 130822 (EOS ``<|endoftext|>``)."""


def length_table(codes: Bf16Codes, lengths: np.ndarray) -> list[dict]:
    """One row per L = 0 .. P: token count, bf16 high/low (value and bits), and the f64 cross-check."""
    P = codes.pos_dim
    counts = np.bincount(lengths.astype(np.int64), minlength=P + 1)
    hi64, lo64 = code_values(np.arange(P + 1), P, char_dim=codes.char_dim)
    hi_ref, lo_ref = float_to_bits(hi64), float_to_bits(lo64)
    high, low = codes.high, codes.low
    return [
        {
            "L": L,
            "n_tokens": int(counts[L]),
            "high_bf16": float(high[L]),
            "high_bits": f"0x{int(codes.high_bits[L]):04x}",
            "low_bf16": float(low[L]),
            "low_bits": f"0x{int(codes.low_bits[L]):04x}",
            "high_equals_low": bool(codes.high_bits[L] == codes.low_bits[L]),
            "f64_rounded_matches": bool(hi_ref[L] == codes.high_bits[L] and lo_ref[L] == codes.low_bits[L]),
        }
        for L in range(P + 1)
    ]


def check_a_identical_bytes(table: ByteTable) -> dict:
    unique = len({table.row(i) for i in range(table.vocab_size)})
    return {"n_unique_rows": unique, "n_colliding_tokens": table.vocab_size - unique}


def check_b_high_equals_low(codes: Bf16Codes, present: set[int]) -> dict:
    """L = 0 (the empty string, one value everywhere) is reported apart: it is degenerate by definition."""
    hl = [L for L in range(1, codes.pos_dim + 1) if codes.high_bits[L] == codes.low_bits[L]]
    not_above = [L for L in range(1, codes.pos_dim + 1) if not codes.high[L] > codes.low[L]]
    return {
        "lengths_checked": f"1..{codes.pos_dim}",
        "lengths_with_high_equal_low": hl,
        "lengths_in_vocab_with_high_equal_low": [L for L in hl if L in present],
        "lengths_with_high_not_above_low": not_above,
        "L0_high_equals_low": bool(codes.high_bits[0] == codes.low_bits[0]),
        "L0_tokens_in_vocab": 0 in present,
    }


def check_c_length_pairs(codes: Bf16Codes) -> dict:
    seen: dict[tuple[int, int], int] = {}
    pairs = []
    for L in range(1, codes.pos_dim + 1):
        key = (int(codes.high_bits[L]), int(codes.low_bits[L]))
        if key in seen:
            pairs.append([seen[key], L])
        seen.setdefault(key, L)
    return {"lengths_checked": f"1..{codes.pos_dim}", "n_distinct_pairs": len(seen), "identical_length_pairs": pairs}


def row_hash_check(
    tb: TokenizerBundle, digests: np.ndarray, required_ids: Sequence[int] = REQUIRED_SPECIAL_IDS
) -> tuple[dict, dict]:
    keys = np.ascontiguousarray(digests).view(np.dtype((np.void, 32))).ravel()
    _, inverse, counts = np.unique(keys, return_inverse=True, return_counts=True)
    dup_ids = np.flatnonzero(counts[inverse] > 1)
    rows = {
        "n_rows": len(keys),
        "n_distinct_row_hashes": len(counts),
        "n_duplicate_rows": int(len(keys) - len(counts)),
        "duplicate_ids": dup_ids[:50].tolist(),
    }
    special = sorted(tb.special_ids)
    colliding = [i for i in special if counts[inverse[i]] > 1]
    required = {
        str(i): {
            "content": tb.added[i]["content"] if i in tb.added else None,
            "special": i in tb.special_ids,
            "row_sha256": bytes(digests[i]).hex(),
        }
        for i in required_ids
    }
    a, b = required_ids
    spec = {
        "n_special": len(special),
        "special_ids_source": "tokenizer.json added_tokens with special: true",
        "required_ids": required,
        "required_ids_present": all(i in tb.special_ids for i in required_ids),
        "required_ids_distinct": a != b and bytes(digests[a]) != bytes(digests[b]),
        "eos": {
            "id": EOS_ID,
            "content": EOS_TOKEN,
            "matches_tokenizer": tb.added.get(EOS_ID, {}).get("content") == EOS_TOKEN,
        },
        "n_special_token_collisions": len(colliding),
        "colliding_special_ids": colliding,
    }
    return rows, spec


def run(tb: TokenizerBundle, codes: Bf16Codes, *, chunk_rows: int = 1024) -> dict:
    table = build_raw_table(tb, codes.pos_dim)
    codes.check_table(table)
    res = stream_rows(codes, table, chunk_rows=chunk_rows)
    present = {int(L) for L in np.unique(table.lengths)}
    rows, spec = row_hash_check(tb, res.row_digests)
    out = {
        "tokenizer": {"name": C3S0_NAME, "sha256": tb.sha256, "vocab_size": tb.vocab_size},
        "pos_dim": codes.pos_dim,
        "output_dim": codes.output_dim,
        "hashes": {
            "raw_table_sha256": codes.raw_table_sha256,
            "codes_sha256": codes.sha256(),
            "matrix_sha256": res.matrix_sha256,
            "matrix_sha256_matches_recorded": res.matrix_sha256 == codes.matrix_sha256,
            "row_hashes_sha256": res.row_hashes_sha256,
            "row_hashes_sha256_matches_recorded": res.row_hashes_sha256 == codes.row_hashes_sha256,
        },
        "A_identical_bytes_and_length": check_a_identical_bytes(table),
        "B_high_equals_low": check_b_high_equals_low(codes, present),
        "C_identical_value_pairs_across_lengths": check_c_length_pairs(codes),
        "row_hashes": rows,
        "special_tokens": spec,
        "per_length": length_table(codes, table.lengths),
    }
    out["failures"] = failures(out)
    out["passed"] = not out["failures"]
    return out


def failures(r: dict) -> list[str]:
    f = []
    if r["A_identical_bytes_and_length"]["n_colliding_tokens"]:
        f.append("A: tokens with identical bytes and length")
    b = r["B_high_equals_low"]
    if b["lengths_with_high_equal_low"] or b["lengths_with_high_not_above_low"] or b["L0_tokens_in_vocab"]:
        f.append("B: high == low (or high <= low) at a length that can occur")
    if r["C_identical_value_pairs_across_lengths"]["identical_length_pairs"]:
        f.append("C: two lengths share a (high, low) pair")
    if r["row_hashes"]["n_duplicate_rows"]:
        f.append("rows: duplicate row hashes")
    s = r["special_tokens"]
    if not (s["required_ids_present"] and s["required_ids_distinct"] and s["eos"]["matches_tokenizer"]):
        f.append("special: ids 36 / 130822 missing, not special, or not distinct")
    if s["n_special_token_collisions"]:
        f.append("special: a special token's row equals another row")
    h = r["hashes"]
    if not (h["matrix_sha256_matches_recorded"] and h["row_hashes_sha256_matches_recorded"]):
        f.append("hashes: rebuilt matrix differs from the recorded artifact")
    return f


def length_table_text(rows: list[dict]) -> str:
    head = f"{'L':>3} {'tokens':>7} {'high (bf16)':>12} {'bits':>6} {'low (bf16)':>14} {'bits':>6}  high==low"
    lines = [head, "-" * len(head)]
    for r in rows:
        lines.append(
            f"{r['L']:>3} {r['n_tokens']:>7} {r['high_bf16']:>12.6g} {r['high_bits']:>6} "
            f"{r['low_bf16']:>14.8g} {r['low_bits']:>6}  {'yes' if r['high_equals_low'] else 'no'}"
        )
    return "\n".join(lines)


def markdown(r: dict) -> str:
    h, s = r["hashes"], r["special_tokens"]
    a, b, c, rows = (r[k] for k in ("A_identical_bytes_and_length", "B_high_equals_low",
                                    "C_identical_value_pairs_across_lengths", "row_hashes"))  # fmt: skip
    P, V = r["pos_dim"], r["tokenizer"]["vocab_size"]
    n_spec = s["n_special_token_collisions"]
    sentence = f"{n_spec} special-token collisions"
    req = s["required_ids"]
    out = [
        f"# KE2 bf16 codes: collision check ({r['tokenizer']['name']}, P = {P})",
        "",
        "Generated by `src/check_bf16_collisions.py`; do not edit by hand.",
        "",
        f"**{'PASS' if r['passed'] else 'FAIL'}.** {sentence}. {rows['n_duplicate_rows']} duplicate rows among the "
        f"{V:,} bf16 rows of the `({V:,}, {r['output_dim']:,})` matrix.",
        "",
        "## Hashes",
        "",
        "| What | SHA-256 |",
        "|---|---|",
        f"| tokenizer.json ({r['tokenizer']['name']}) | `{r['tokenizer']['sha256']}` |",
        f"| raw byte table, P = {P} | `{h['raw_table_sha256']}` |",
        f"| compact bf16 codes (`results/bf16/bf16_codes_P{P}.npz`) | `{h['codes_sha256']}` |",
        f"| bf16 matrix, row-major bytes | `{h['matrix_sha256']}` |",
        f"| per-row hash list | `{h['row_hashes_sha256']}` |",
        "",
        "The matrix and row-hash values were recomputed here from the committed compact codes and match the values "
        "the builder recorded after checking the codec's bf16 output row by row.",
        "",
        "## Checks",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| A: tokens with identical bytes and length | {a['n_colliding_tokens']} ({a['n_unique_rows']:,} unique raw rows) |",
        f"| B: lengths 1..{P} with `high[L] == low[L]` in bf16 | {len(b['lengths_with_high_equal_low'])} |",
        f"| C: pairs of lengths with identical bf16 `(high, low)` | {len(c['identical_length_pairs'])} "
        f"({c['n_distinct_pairs']} distinct pairs for {P} lengths) |",
        f"| duplicate row hashes (all {V:,} rows) | {rows['n_duplicate_rows']} |",
        f"| special tokens whose row equals another row | {n_spec} of {s['n_special']} |",
        "",
        "L = 0 (the empty string) has `high == low == 0` by definition; no token in the vocabulary has length 0.",
        "",
        "## Special tokens",
        "",
        f"{s['n_special']} special ids are read from the tokenizer's `added_tokens` (`special: true`). "
        f"Id 36 is `{req['36']['content']}` and id {EOS_ID} is the EOS token `{req[str(EOS_ID)]['content']}`. Both "
        f"are special and their bf16 rows differ. {sentence}.",
        "",
        "## bf16 code values per length",
        "",
        "| L | tokens | high (bf16) | bits | low (bf16) | bits | high == low |",
        "|---:|---:|---:|---|---:|---|---|",
    ]
    for t in r["per_length"]:
        out.append(
            f"| {t['L']} | {t['n_tokens']:,} | {t['high_bf16']:.6g} | `{t['high_bits']}` | {t['low_bf16']:.8g} | "
            f"`{t['low_bits']}` | {'yes' if t['high_equals_low'] else 'no'} |"
        )
    out += ["", closed_form_sentence(r["per_length"], P)]
    out += [
        "",
        "## Reproduce",
        "",
        "The raw table is not committed (lab rule, 15 Nov: script, config and SHA-256 only). Rebuild it locally with "
        "`--write-raw-table` and check it with `verify_c3s0_table.py`; TSAI rebuilds it on request.",
        "",
        "```bash",
        "export KE2_C3S0_TOKENIZER=/path/to/c3-sample-v0/tokenizer.json",
        f"python teams/04-ke2/src/build_bf16_codes.py --pos-dim {P} --write-raw-table   "
        "# add --materialize for the 2 GiB matrix",
        f"python teams/04-ke2/src/check_bf16_collisions.py --pos-dim {P}",
        f"python teams/04-ke2/src/verify_c3s0_table.py teams/04-ke2/results/bf16/materialized/raw_table_P{P}.npz",
        "```",
        "",
    ]
    return "\n".join(out)


def closed_form_sentence(per_length: list[dict], P: int) -> str:
    """Say exactly which lengths differ from the float64 closed form rounded to bf16, and whether any token has them."""
    n_match = sum(t["f64_rounded_matches"] for t in per_length)
    off = [t for t in per_length if not t["f64_rounded_matches"]]
    text = (
        f"Values are the upstream float32 codec output cast to bf16. For {n_match} of {P + 1} lengths they equal "
        "the float64 closed form (`ke2.codec.code_values`) rounded to bf16."
    )
    if not off:
        return text
    where = ", ".join(f"L = {t['L']} ({t['n_tokens']:,} tokens)" for t in off)
    used = [t for t in off if t["n_tokens"]]
    tail = (
        " No token has any of these lengths, so every token's bf16 row is the closed form rounded to bf16."
        if not used
        else f" {sum(t['n_tokens'] for t in used):,} tokens have one of these lengths."
    )
    zero_note = (
        " At L = 0 the codec gives +0 where the closed form gives -0 for `low`, the same value with a different sign bit."
        if any(t["L"] == 0 for t in off)
        else ""
    )
    return f"{text} The exceptions are {where}.{zero_note}{tail}"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizer", default=None, help="C3-s0 tokenizer.json (default: $KE2_C3S0_TOKENIZER)")
    ap.add_argument("--pos-dim", type=int, default=BF16_POS_DIM)
    ap.add_argument("--out", type=Path, default=BF16_DIR)
    ap.add_argument("--chunk-rows", type=int, default=1024)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    tb = load_tokenizer(tokenizer_arg(a.tokenizer), expected_sha256=C3S0_TOKENIZER_SHA256)
    codes = Bf16Codes.load(codes_path(a.out, a.pos_dim), tokenizer=tb)
    r = run(tb, codes, chunk_rows=a.chunk_rows)
    print(length_table_text(r["per_length"]))
    print()
    for line in markdown(r).splitlines()[4:6]:
        print(line)
    for k in ("A_identical_bytes_and_length", "B_high_equals_low", "C_identical_value_pairs_across_lengths",
              "row_hashes"):  # fmt: skip
        print(f"{k}: {json.dumps(r[k])}")
    s = r["special_tokens"]
    print(f"special: {s['n_special']} ids, required present={s['required_ids_present']} "
          f"distinct={s['required_ids_distinct']}, collisions={s['n_special_token_collisions']}")  # fmt: skip
    print(
        f"matrix sha256 {r['hashes']['matrix_sha256']} (matches recorded: {r['hashes']['matrix_sha256_matches_recorded']})"
    )
    stem = f"bf16_collisions_P{a.pos_dim}"
    (a.out / f"{stem}.json").write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    (a.out / f"{stem}.md").write_text(markdown(r), encoding="utf-8")
    if r["failures"]:
        for f in r["failures"]:
            log.error("FAIL %s", f)
        return 1
    log.info("PASS; wrote %s.json and %s.md", a.out / stem, a.out / stem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
