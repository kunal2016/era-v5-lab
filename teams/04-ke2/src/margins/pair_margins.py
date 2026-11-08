"""Exact decode margins of every token against the whole vocabulary, from the two-valued code structure.

Self margin of token t: ``cos(z_t, z_t) - max over s != t of cos(z_t, z_s)``. The maximiser is the
*rival* (lowest ID on ties). When t decodes to itself this is ``decode_ref``'s margin (best minus
second-best cosine); a value <= 0 means t ties with or loses to its rival.

Why this is cheap and exact
---------------------------
Every code is two-valued (Lemma 1): ``high`` on the L support cells ``b_p * P + p`` and ``low``
everywhere else. For a query token s and a candidate t that agree on k byte positions
(``p < min(L_s, L_t)`` with ``b_s[p] == b_t[p]``), with D = char_dim * P:

    dot = k*h_s*h_t + (L_s - k)*h_s*l_t + (L_t - k)*l_s*h_t + (D - L_s - L_t + k)*l_s*l_t
    cos = dot / (|z_s| * |z_t|)          (0 where the norm product is 0, as decode_ref does)

so all pairs need only the overlap counts k and per-token ``(high, low)``. The code evaluates the
same dot in decode_ref's arrangement, ``l_t * sum(z_s) + (h_t - l_t) * (k*(h_s - l_s) + L_t*l_s)``.
``(high, low)`` may come from the float64 reference or from rounded fp32 / bf16 codes; the arithmetic
is float64 either way, so the result measures the effect of *storing* codes in that precision.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from ke2.codec import code_values
from ke2.config import CHAR_DIM
from ke2.tables import ByteTable

PRECISIONS: tuple[str, ...] = ("fp64", "fp32", "bf16")


@dataclass(frozen=True)
class CodeValues:
    """Per-token code values: ``high`` on the support, ``low`` elsewhere (both float64)."""

    precision: str
    pos_dim: int
    char_dim: int
    lengths: np.ndarray  # int64 (V,)
    high: np.ndarray  # float64 (V,)
    low: np.ndarray  # float64 (V,)

    @property
    def dim(self) -> int:
        """Code width D = char_dim * pos_dim."""
        return self.char_dim * self.pos_dim

    @property
    def norms(self) -> np.ndarray:
        """Euclidean norm of every code, float64 (V,)."""
        L = self.lengths.astype(np.float64)
        return np.sqrt(L * self.high**2 + (self.dim - L) * self.low**2)


def exact_values(table: ByteTable) -> CodeValues:
    """Float64 reference values (``ke2.codec.code_values``, upstream codec defaults)."""
    lengths = table.lengths.astype(np.int64)
    high, low = code_values(lengths, table.pos_dim, char_dim=CHAR_DIM)
    return CodeValues("fp64", table.pos_dim, CHAR_DIM, lengths, high, low)


def overlap_counts(q_rows: np.ndarray, q_lens: np.ndarray, c_rows: np.ndarray, c_lens: np.ndarray) -> np.ndarray:
    """Number of positions ``p < min(L_q, L_c)`` where the bytes agree, int16 (n, V).

    Rows are zero-padded, so positions past either length never count (a real 0x00 byte does).
    """
    q_lens = np.asarray(q_lens, dtype=np.int64)
    c_lens = np.asarray(c_lens, dtype=np.int64)
    out = np.zeros((q_rows.shape[0], c_rows.shape[0]), dtype=np.int16)
    top = min(int(q_lens.max(initial=0)), q_rows.shape[1])
    for p in range(top):  # one (n, V) slice per position, never an (n, V, P) broadcast
        same = q_rows[:, p, None] == c_rows[None, :, p]
        same &= (p < q_lens)[:, None]
        same &= (p < c_lens)[None, :]
        out += same
    return out


def pair_cosines(query_ids: np.ndarray, overlaps: np.ndarray, values: CodeValues) -> np.ndarray:
    """Cosine of each query token's code to every code, float64 (n, V), from overlap counts."""
    q = np.asarray(query_ids, dtype=np.int64)
    hs, ls = values.high[q][:, None], values.low[q][:, None]
    Ls = values.lengths[q].astype(np.float64)[:, None]
    Lt = values.lengths.astype(np.float64)[None, :]
    ht, lt = values.high[None, :], values.low[None, :]
    query_sum = Ls * hs + (values.dim - Ls) * ls  # sum of the query code's entries
    on_support = overlaps * (hs - ls) + Lt * ls  # sum of the query over t's support cells
    dots = lt * query_sum + (ht - lt) * on_support
    norms = values.norms
    denom = norms[q][:, None] * norms[None, :]
    out = np.zeros_like(dots)
    np.divide(dots, denom, out=out, where=denom > 0)
    return out


@dataclass(frozen=True)
class SelfMargins:
    """Self margin, rival and shared-byte count of each query token, for one precision."""

    precision: str
    token_ids: np.ndarray  # int64 (n,)
    self_scores: np.ndarray  # float64 (n,): cos(z_t, z_t)
    margins: np.ndarray  # float64 (n,): self score minus best rival score
    rival_ids: np.ndarray  # int64 (n,): best other token, lowest ID on ties
    overlaps: np.ndarray  # int64 (n,): k between the token and its rival


def self_margins(
    table: ByteTable,
    values: Sequence[CodeValues],
    *,
    query_ids: np.ndarray | None = None,
    chunk_rows: int = 64,
) -> dict[str, SelfMargins]:
    """Exhaustive self margins of the query tokens for every set of code values, keyed by precision.

    ``query_ids=None`` scores every token in ID order; otherwise results follow the caller's order.
    Overlap counts are computed once per chunk and shared by all precisions. Results are bitwise
    independent of ``chunk_rows``. Scoring temporaries are about ``4 * 8 * chunk_rows * V`` bytes.
    """
    if chunk_rows < 1:
        raise ValueError("chunk_rows must be positive")
    V = table.vocab_size
    if V < 2:
        raise ValueError("a margin needs at least two tokens")
    for v in values:
        if v.pos_dim != table.pos_dim or v.lengths.shape[0] != V:
            raise ValueError(f"{v.precision} values do not match the table (P={table.pos_dim}, V={V})")
    ids = np.arange(V, dtype=np.int64) if query_ids is None else np.asarray(query_ids, dtype=np.int64)
    n = ids.shape[0]
    lengths = table.lengths.astype(np.int64)
    order = np.argsort(lengths[ids], kind="stable")  # short chunks loop over few positions
    out = {
        v.precision: {
            "self": np.empty(n),
            "margin": np.empty(n),
            "rival": np.empty(n, np.int64),
            "k": np.empty(n, np.int64),
        }
        for v in values
    }
    for start in range(0, n, chunk_rows):
        where = order[start : start + chunk_rows]
        q = ids[where]
        k = overlap_counts(table.bytes[q], lengths[q], table.bytes, lengths)
        rows = np.arange(q.shape[0])
        for v in values:
            cos = pair_cosines(q, k, v)
            own = cos[rows, q].copy()
            cos[rows, q] = -np.inf
            rival = np.argmax(cos, axis=1)  # first maximum: lowest ID on ties
            o = out[v.precision]
            o["self"][where] = own
            o["margin"][where] = own - cos[rows, rival]
            o["rival"][where] = rival
            o["k"][where] = k[rows, rival]
    return {p: SelfMargins(p, ids.copy(), o["self"], o["margin"], o["rival"], o["k"]) for p, o in out.items()}
