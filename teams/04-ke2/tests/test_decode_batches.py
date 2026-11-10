"""Decoding every id in batches of 1, 7 and 4096 gives identical ids, equal to the float64 reference."""

import numpy as np
import torch

import decode_batches as db
import decode_ref as dr
from ke2.codec import encode_f64
from ke2.tables import ByteTable

P = 16


def synthetic_table(n=500, seed=0):
    rng = np.random.default_rng(seed)
    rows = set()
    while len(rows) < n:
        rows.add(bytes(rng.integers(0, 256, int(rng.integers(1, P + 1)), dtype=np.uint8)))
    rows = sorted(rows)
    buf = np.zeros((n, P), dtype=np.uint8)
    lens = np.zeros(n, dtype=np.int16)
    for i, r in enumerate(rows):
        buf[i, : len(r)] = np.frombuffer(r, dtype=np.uint8)
        lens[i] = len(r)
    return ByteTable("raw", P, buf, lens, 0, 0, 0, "synthetic")


def test_batch_sizes_agree_and_match_reference():
    table = synthetic_table()
    ct = dr.CodeTable.from_byte_table(table)
    ref = dr.decode(encode_f64(table.bytes, table.lengths.astype(np.int64), P), ct).token_ids
    runs = {b: db.decode_all(table, ct, "cpu", b) for b in (1, 7, 4096)}
    for b, ids in runs.items():
        assert ids.shape == (table.vocab_size,) and ids.dtype == np.int64
        assert np.array_equal(ids, ref), b
    assert len({db.ids_sha256(ids, P, "cpu", b) for b, ids in runs.items()}) == 3  # header includes batch size
    assert len({db.ids_sha256(ids, P, "cpu", 0) for ids in runs.values()}) == 1  # same ids -> same body hash


def test_gpu_format_digest_matches_decode_gpu():
    import decode_gpu as dg

    assert db.GPU_ID_HASH_FORMAT == dg.ID_HASH_FORMAT
    ids = np.arange(120)
    sha = "ab" * 32
    assert db.ids_sha256_gpu_format(ids, P, sha) == dg.id_digest(P, sha, np.arange(120), ids)
    ids2 = ids.copy()
    ids2[5] = 6
    assert db.ids_sha256_gpu_format(ids2, P, sha) != db.ids_sha256_gpu_format(ids, P, sha)


def test_tf32_is_disabled_by_configure_device():
    db.configure_device("cpu")
    assert torch.backends.cuda.matmul.allow_tf32 is False
    assert torch.backends.cudnn.allow_tf32 is False
    assert torch.get_float32_matmul_precision() == "highest"


def test_reference_cache_write_then_hit_and_stale_fallthrough(tmp_path):
    table = synthetic_table(n=120, seed=1)
    ct = dr.CodeTable.from_byte_table(table)
    cache = tmp_path / "ref.npz"
    ids1, info1 = db.reference_ids(table, ct, cache, chunk=50)
    assert info1["cached"] is False and cache.is_file()
    assert np.array_equal(ids1, np.arange(table.vocab_size))
    ids2, info2 = db.reference_ids(table, ct, cache, chunk=50)
    assert info2["cached"] is True and np.array_equal(ids2, ids1) and info2["sha256"] == info1["sha256"]
    np.savez_compressed(cache, ids=ids1[::-1].copy(), sha256=np.array("x"))  # no table_sha256 key
    ids3, info3 = db.reference_ids(table, ct, cache, chunk=50)
    assert info3["cached"] is False and np.array_equal(ids3, ids1)
    np.savez_compressed(cache, ids=ids1[::-1].copy(), sha256=np.array("x"), table_sha256=np.array("other"))
    ids4, info4 = db.reference_ids(table, ct, cache, chunk=50)
    assert info4["cached"] is False and np.array_equal(ids4, ids1)


def test_environment_reads_flags_back():
    db.configure_device("cpu")
    env = db.environment("cpu")
    assert env["tf32_matmul"] is False and env["tf32_cudnn"] is False
    assert env["float32_matmul_precision"] == "highest"
