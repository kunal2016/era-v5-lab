"""Exact per-token decode margins (src/margins/pair_margins.py).

Synthetic tables always run; the real-tokenizer check is skipped without BrahmicTokenizer-131K.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "margins"))

import decode_ref as dr
import pair_margins as pm
from ke2.codec import encode_f64

# Aliases: pr-guard's email check misreads dotted pytest decorators as addresses.
fixture = pytest.fixture
parametrize = pytest.mark.parametrize

SAMPLED_MIN_P32 = 0.0318133707027064  # results/decode_ref/summary.json, raw_P32 min_margin (4,096-ID sample)


def test_overlap_counts_compare_bytes_only_inside_both_lengths(make_byte_table):
    t = make_byte_table([b"abc", b"abd", b"ab", b"xbc", b"a\x00", b"a"], P=4)
    k = pm.overlap_counts(t.bytes, t.lengths, t.bytes, t.lengths)
    assert k.dtype == np.int16
    assert k[0].tolist() == [3, 2, 2, 2, 1, 1]
    assert k[3].tolist() == [2, 1, 1, 3, 0, 0]
    assert k[4, 5] == 1 and k[4, 4] == 2  # a 0x00 byte is a byte; padding is not


def test_pair_cosines_equal_dense_float64_cosines(synthetic_p8):
    t = synthetic_p8
    k = pm.overlap_counts(t.bytes[:10], t.lengths[:10], t.bytes, t.lengths)
    codes = encode_f64(t.bytes, t.lengths, t.pos_dim)
    unit = codes / np.linalg.norm(codes, axis=1, keepdims=True)
    got = pm.pair_cosines(np.arange(10), k, pm.exact_values(t))
    np.testing.assert_allclose(got, unit[:10] @ unit.T, rtol=0, atol=1e-12)


def test_self_margins_equal_decode_ref_margins(synthetic_p8):
    t = synthetic_p8
    ct = dr.CodeTable.from_byte_table(t)
    sm = pm.self_margins(t, [pm.exact_values(t)])["fp64"]
    ref = dr.decode(ct.codes(np.arange(t.vocab_size)), ct)
    assert np.array_equal(sm.token_ids, np.arange(t.vocab_size))
    np.testing.assert_allclose(sm.margins, ref.margins, rtol=0, atol=1e-12)
    assert (sm.rival_ids != sm.token_ids).all()


def test_prefix_pair_reproduces_the_sampled_p32_minimum(make_byte_table):
    t = make_byte_table([b"x" * 15, b"x" * 15 + b"y", b"q"], P=32)
    sm = pm.self_margins(t, [pm.exact_values(t)])["fp64"]
    assert sm.margins[0] == pytest.approx(SAMPLED_MIN_P32, abs=1e-12)
    assert (int(sm.rival_ids[0]), int(sm.overlaps[0])) == (1, 15)


def test_duplicate_rows_have_zero_margin_and_point_at_each_other(make_byte_table):
    t = make_byte_table([b"ab", b"zz", b"ab"], P=4)
    sm = pm.self_margins(t, [pm.exact_values(t)])["fp64"]
    assert sm.margins[[0, 2]].tolist() == [0.0, 0.0]
    assert sm.rival_ids[[0, 2]].tolist() == [2, 0]


def test_chunk_size_and_query_subset_do_not_change_results(synthetic_p8):
    t, v = synthetic_p8, [pm.exact_values(synthetic_p8)]
    full = pm.self_margins(t, v, chunk_rows=64)["fp64"]
    one = pm.self_margins(t, v, chunk_rows=1)["fp64"]
    sub = pm.self_margins(t, v, query_ids=np.array([9, 3, 50]), chunk_rows=2)["fp64"]
    assert np.array_equal(full.margins, one.margins) and np.array_equal(full.rival_ids, one.rival_ids)
    assert sub.token_ids.tolist() == [9, 3, 50]
    assert np.array_equal(sub.margins, full.margins[[9, 3, 50]])


def test_real_raw_p32_sample_matches_decode_ref(raw32, tb):
    ids = dr.sample_token_ids(raw32.vocab_size, tb.special_ids, n=256, seed=5)
    ct = dr.CodeTable.from_byte_table(raw32)
    sm = pm.self_margins(raw32, [pm.exact_values(raw32)], query_ids=ids)["fp64"]
    np.testing.assert_allclose(sm.margins, dr.decode(ct.codes(ids), ct).margins, rtol=0, atol=1e-12)
    assert (sm.margins > 0).all()
