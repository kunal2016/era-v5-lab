"""Frozen bf16 codes (results/bf16/): zero collisions, and the committed artifact matches a rebuild.

Most tests need only the upstream codec. The full rebuild (raw table, every row, matrix hash) needs
the C3-s0 tokenizer.json via $KE2_C3S0_TOKENIZER and is skipped without it.
"""

import json
import os
from types import SimpleNamespace

import numpy as np
import pytest

from build_bf16_codes import build, codes_path, config_path
from check_bf16_collisions import (
    check_a_identical_bytes,
    check_b_high_equals_low,
    check_c_length_pairs,
    closed_form_sentence,
    markdown,
    row_hash_check,
    run,
)
from ke2.bf16_codes import Bf16Codes, codec_bf16_bits, compact_from_codec, expand, stream_rows
from ke2.config import BF16_DIR, BF16_POS_DIM, C3S0_TOKENIZER_ENV, C3S0_TOKENIZER_SHA256, EOS_ID, EOS_TOKEN
from ke2.tables import TableContractError
from ke2.tokenizer import load_tokenizer
from verify_c3s0_table import main as verify_main
from verify_c3s0_table import verify

# Aliases: pr-guard's email check misreads dotted pytest decorators as addresses.
fixture = pytest.fixture
parametrize = pytest.mark.parametrize

P = BF16_POS_DIM


def committed():
    return Bf16Codes.load(codes_path(BF16_DIR, P), tokenizer_sha256=C3S0_TOKENIZER_SHA256)


def results():
    return json.loads((BF16_DIR / f"bf16_collisions_P{P}.json").read_text(encoding="utf-8"))


def config():
    return json.loads(config_path(BF16_DIR, P).read_text(encoding="utf-8"))


@fixture(scope="module")
def c3s0():
    path = os.environ.get(C3S0_TOKENIZER_ENV)
    if not path:
        pytest.skip(f"C3-s0 tokenizer not found; set {C3S0_TOKENIZER_ENV} to its tokenizer.json")
    return load_tokenizer(path, expected_sha256=C3S0_TOKENIZER_SHA256)


# --- committed artifact, no tokenizer needed -------------------------------------------------------


def test_committed_codes_are_bound_to_c3s0():
    c = committed()
    assert (c.pos_dim, c.char_dim, c.vocab_size) == (P, 256, 131072)
    with pytest.raises(TableContractError):
        Bf16Codes.load(codes_path(BF16_DIR, P), tokenizer_sha256="0" * 64)


def test_committed_compact_codes_match_a_codec_rebuild():
    high, low = compact_from_codec(P)
    c = committed()
    np.testing.assert_array_equal(c.high_bits, high)
    np.testing.assert_array_equal(c.low_bits, low)


def test_committed_codes_have_zero_value_collisions():
    c = committed()
    b = check_b_high_equals_low(c, present=set(range(1, P + 1)))
    assert b["lengths_with_high_equal_low"] == [] and b["lengths_with_high_not_above_low"] == []
    assert check_c_length_pairs(c)["identical_length_pairs"] == []


def test_committed_results_report_zero_collisions():
    r, c, cfg = results(), committed(), config()
    assert r["passed"] and r["failures"] == []
    assert r["A_identical_bytes_and_length"]["n_colliding_tokens"] == 0
    assert r["B_high_equals_low"]["lengths_in_vocab_with_high_equal_low"] == []
    assert not r["B_high_equals_low"]["L0_tokens_in_vocab"]
    assert r["C_identical_value_pairs_across_lengths"]["identical_length_pairs"] == []
    assert r["row_hashes"]["n_duplicate_rows"] == 0
    s = r["special_tokens"]
    assert s["n_special_token_collisions"] == 0 and s["n_special"] == 356
    assert s["required_ids_present"] and s["required_ids_distinct"]
    assert s["required_ids"][str(EOS_ID)]["content"] == EOS_TOKEN
    # one set of hashes across the npz, the config and the check results
    assert r["hashes"]["codes_sha256"] == c.sha256() == cfg["compact"]["sha256"]
    assert r["hashes"]["matrix_sha256"] == c.matrix_sha256 == cfg["matrix"]["sha256"]
    assert r["hashes"]["row_hashes_sha256"] == c.row_hashes_sha256 == cfg["matrix"]["row_hashes_sha256"]
    assert r["hashes"]["raw_table_sha256"] == c.raw_table_sha256 == cfg["raw_table"]["sha256"]
    assert cfg["tokenizer"]["sha256"] == C3S0_TOKENIZER_SHA256 == c.tokenizer_sha256


def test_results_markdown_is_current_and_quotable():
    r = results()
    md = (BF16_DIR / f"bf16_collisions_P{P}.md").read_text(encoding="utf-8")
    assert md == markdown(r)
    assert "0 special-token collisions" in md
    assert r["hashes"]["matrix_sha256"] in md


def test_only_the_empty_string_differs_from_the_closed_form():
    """The one length whose bf16 value is not the closed form rounded is L = 0 (sign of zero); no token has it."""
    r = results()
    off = [t for t in r["per_length"] if not t["f64_rounded_matches"]]
    assert [t["L"] for t in off] == [0] and off[0]["n_tokens"] == 0
    sentence = closed_form_sentence(r["per_length"], P)
    assert "L = 0 (0 tokens)" in sentence and "No token has any of these lengths" in sentence
    assert closed_form_sentence([dict(t, f64_rounded_matches=True) for t in r["per_length"]], P).endswith("to bf16.")


def test_raw_table_is_not_committed_but_its_hash_is():
    """Lab rule (15 Nov): the script, the config and the sha256 are committed, not the table."""
    cfg = config()
    assert cfg["raw_table"]["committed"] is False
    assert "verify_c3s0_table.py" in cfg["raw_table"]["rebuild"]
    assert not (BF16_DIR / "materialized").exists() or not any((BF16_DIR / "materialized").glob("raw_table_*.npz"))
    assert len(cfg["raw_table"]["sha256"]) == 64 and cfg["raw_table"]["sha256"] == committed().raw_table_sha256


# --- the checks detect what they claim to ---------------------------------------------------------


def test_expand_equals_codec_bits(make_byte_table):
    rows = [b"a", b"ab", b"\x00", b"\xff" * 8, bytes(range(32)), b"<|endoftext|>"]
    t = make_byte_table(rows, P)
    high, low = compact_from_codec(P)
    np.testing.assert_array_equal(expand(t.bytes, t.lengths, high, low, P), codec_bf16_bits(t.bytes, t.lengths, P))


def _codes_for(t, high, low):
    return Bf16Codes(P, 256, high, low, t.tokenizer_sha256, t.sha256(), t.vocab_size)


def test_duplicate_rows_are_found(make_byte_table):
    t = make_byte_table([b"x", b"yz", b"x"], P)
    assert check_a_identical_bytes(t)["n_colliding_tokens"] == 1
    res = stream_rows(_codes_for(t, *compact_from_codec(P)), t, verify_codec=True)

    # token 0 is "special", token 2 has the same bytes
    toy = SimpleNamespace(special_ids={0, 1}, added={0: {"content": "x"}, 1: {"content": "yz"}})
    rows, spec = row_hash_check(toy, res.row_digests, required_ids=(0, 1))
    assert rows["n_duplicate_rows"] == 1 and rows["duplicate_ids"] == [0, 2]
    assert spec["n_special_token_collisions"] == 1 and spec["colliding_special_ids"] == [0]
    assert spec["required_ids_present"] and spec["required_ids_distinct"]


def test_rounding_collisions_are_found(make_byte_table):
    t = make_byte_table([b"a"], P)
    high, low = compact_from_codec(P)
    flat = high.copy()
    flat[5] = low[5]
    assert check_b_high_equals_low(_codes_for(t, flat, low), {5})["lengths_in_vocab_with_high_equal_low"] == [5]
    h2, l2 = high.copy(), low.copy()
    h2[7], l2[7] = high[6], low[6]
    assert check_c_length_pairs(_codes_for(t, h2, l2))["identical_length_pairs"] == [[6, 7]]


def test_codes_refuse_another_raw_table(make_byte_table):
    t = make_byte_table([b"a", b"b"], P)
    c = _codes_for(t, *compact_from_codec(P))
    with pytest.raises(TableContractError):
        stream_rows(c, make_byte_table([b"a", b"c"], P))


def test_verify_accepts_the_recorded_table_and_refuses_others(make_byte_table, tmp_path, capsys):
    """verify_c3s0_table: a locally rebuilt table passes only if it hashes to the codes' raw_table_sha256."""
    sha = "a" * 64
    good = make_byte_table([b"a", b"bc"], P)
    good.tokenizer_sha256 = sha
    codes = _codes_for(good, *compact_from_codec(P))
    codes_file = tmp_path / f"bf16_codes_P{P}.npz"
    codes.save(codes_file)
    good_path = tmp_path / "good.npz"
    good.save(good_path)
    r = verify(good_path, codes_file, tokenizer_sha256=sha)
    assert r["raw_table_sha256"] == good.sha256() == codes.raw_table_sha256

    other = make_byte_table([b"a", b"bd"], P)  # same tokenizer sha, different bytes
    other.tokenizer_sha256 = sha
    other_path = tmp_path / "other.npz"
    other.save(other_path)
    with pytest.raises(TableContractError):
        verify(other_path, codes_file, tokenizer_sha256=sha)

    foreign = make_byte_table([b"a", b"bc"], P)  # same bytes, another tokenizer
    foreign.tokenizer_sha256 = "b" * 64
    foreign_path = tmp_path / "foreign.npz"
    foreign.save(foreign_path)
    with pytest.raises(TableContractError):
        verify(foreign_path, codes_file, tokenizer_sha256=sha)

    # the CLI against the committed codes: a toy table is refused with exit status 1
    assert verify_main([str(good_path)]) == 1
    assert "FAIL" in capsys.readouterr().err


# --- full rebuild from the C3-s0 tokenizer ---------------------------------------------------------


def test_full_rebuild_matches_committed_artifact(c3s0):
    table, codes, _ = build(c3s0, P)  # runs the codec on every token and compares bit for bit
    c = committed()
    assert table.sha256() == c.raw_table_sha256
    assert codes.sha256() == c.sha256()
    assert codes.matrix_sha256 == c.matrix_sha256
    assert codes.row_hashes_sha256 == c.row_hashes_sha256


def test_full_check_has_zero_collisions(c3s0):
    r = run(c3s0, committed())
    assert r["passed"], r["failures"]
    assert r["special_tokens"]["n_special_token_collisions"] == 0
    assert {36, EOS_ID} <= c3s0.special_ids
    assert r == results()
