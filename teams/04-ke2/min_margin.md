# Minimum decode margin per script class (P = 32): fp32 vs bf16

**Status:** 8 Nov, week 2. Raw table, P = 32, BrahmicTokenizer-131K (`01d968a7…739fff`).
Full generated table: [results/min_margin/min_margin_P32.md](results/min_margin/min_margin_P32.md).

## Summary

- The smallest margin anywhere in the vocabulary is **0.015809**: a run of 32 spaces next to a
  run of 31 spaces (Code/Structure). Among the Indic scripts the smallest is Devanagari at
  0.031813, and the Latin minimum is 0.028234. Every one of the 131,072 tokens decodes to itself, in
  every precision.
- **Storing** the codes in fp32 or bf16 changes margins by at most 6.7e-16 (fp32) and 6.2e-8
  (bf16). It never changes which pair is closest.
- **Scoring** in reduced precision is what costs margin. fp32 arithmetic moves margins by up to
  2.6e-4. If the scores themselves are rounded to bf16, they move by up to 5.3e-3, and the
  tightest margin drops from 0.0158 to 0.0121 (−23%). Ranking bf16 codes by raw dot product
  instead of cosine costs about the same (0.0124).
- No checked token decoded wrongly or tied in any mode. The tightest pair is 4 bf16 steps wide
  (one step = 2⁻⁸ ≈ 0.0039 near 1.0), so a fast decoder should keep fp32 scores.

## What this is

For each token t, the **self margin** is `cos(z_t, z_t) − max over s ≠ t of cos(z_t, z_s)`, taken
over the whole vocabulary. The token s that achieves the maximum is t's **rival** (lowest ID on
ties). When t decodes to itself, this is exactly the margin `decode_ref.py` reports: best minus
second-best cosine. A value ≤ 0 would mean a tie or a wrong decode.

The table covers every token (131,072 × 131,072 pairs), not a sample. The earlier 4,096-ID
sample in `results/decode_ref/summary.json` found 0.031813; the exhaustive minimum is half that.
A pair counts toward the class of its first token; the rival can be in another class.

Two separate effects are measured:

| Stage | What is reduced-precision | How it is scored | Covers |
|---|---|---|---|
| storage (`src/margins/pair_margins.py`) | the stored code values: fp64 reference, fp32 (upstream codec output, what G5 gets), bf16 (that output cast down) | exact float64 | all tokens, all pairs |
| scoring (`src/margins/dense_check.py`) | the arithmetic: `fp32`; `bf16_fp32acc` (bf16 codes, fp32 accumulate); `bf16_out` (as before, dot products rounded to bf16, like a GEMM with bf16 output) | dense matrix products on CPU | the 3 lowest-margin tokens of every class, 110 tokens |

## Why a margin depends only on lengths and shared bytes

Each code has one value (`high`) on its L support cells and another (`low`) everywhere else
(Lemma 1). For tokens s and t that agree on k byte positions, with D = 256 · P:

```
dot = k·h_s·h_t + (L_s − k)·h_s·l_t + (L_t − k)·l_s·h_t + (D − L_s − L_t + k)·l_s·l_t
cos = dot / (‖z_s‖ · ‖z_t‖)
```

So a margin is set by (L_s, L_t, k) alone, and it shrinks as tokens get longer. Every class minimum
below is one of two shapes:

- **one-byte extension** (L, L+1, k = L): a token and the same token with one more byte, e.g.
  ` unterschiedliche` → ` unterschiedlichen`. Margin ≈ 1 − √(L/(L+1)).
- **one-byte substitution** (L, L, k = L−1): two tokens that differ in one byte, e.g. Telugu
  `ుకున్నారు` → `ుతున్నారు`.

For most Indic scripts the closest rival of a word is a **partial-UTF-8 fragment**: the same word
minus its last byte, which cuts the final character in half (` वर्ष` → ` वर्\xe0\xaa`). These
fragments are real vocabulary entries. Their margins are healthy (≥ 0.031), but they are the
nearest thing a predicted vector can drift to.

## Minimum margin per class

fp64 storage, sorted by margin. Bytes are (token length, rival length, shared positions). The
21 `Partial-UTF8[…]` subclasses are in the [generated table](results/min_margin/min_margin_P32.md).
Their minima range from 0.031813 (`Partial-UTF8[Devanagari]`) to 0.292936.

| script class | tokens | min margin | token → rival | bytes | bf16 steps |
|---|--:|--:|---|---|--:|
| Code/Structure | 4,275 | 0.015809 | 32 spaces (50346) → 31 spaces (83647) | 32, 31, 31 | 4.0 |
| Latin | 107,453 | 0.028234 | ` unterschiedliche` (112024) → ` unterschiedlichen` (111303) | 17, 18, 17 | 7.2 |
| Devanagari | 4,138 | 0.031813 | ` सिर्फ` (44736) → ` सिर्\xe0\xa4` (120200) | 16, 15, 15 | 8.1 |
| Mixed | 530 | 0.033967 | `’informations` (93823) → `’information` (96773) | 15, 14, 14 | 8.7 |
| Telugu | 1,467 | 0.037160 | `ుకున్నారు` (54136) → `ుతున్నారు` (55825) | 27, 27, 26 | 9.5 |
| Bengali | 2,257 | 0.039290 | ` অভিন` (57432) → ` অভি\xe0\xa6` (111887) | 13, 12, 12 | 10.1 |
| Gujarati | 1,803 | 0.039290 | ` વર્ષ` (29237) → ` વર્\xe0\xaa` (44409) | 13, 12, 12 | 10.1 |
| Kannada | 1,485 | 0.039290 | ` ವರ್ಷ` (38652) → ` ವರ್\xe0\xb2` (64682) | 13, 12, 12 | 10.1 |
| Malayalam | 1,888 | 0.039290 | ` പരിശ` (98130) → ` പരി\xe0\xb4` (43033) | 13, 12, 12 | 10.1 |
| Tamil | 1,117 | 0.047741 | `ுக்கும்` (19225) → `ைக்கும்` (49874) | 21, 21, 20 | 12.2 |
| Gurmukhi | 647 | 0.051375 | ` ਵਿਚ` (11896) → ` ਵਿ\xe0\xa8` (14128) | 10, 9, 9 | 13.2 |
| Oriya | 725 | 0.055678 | `ପ୍ରଦାନ` (126812) → `ପ୍ରଧାନ` (128013) | 18, 18, 17 | 14.3 |
| Special/Control | 356 | 0.062622 | `<\|reserved_100\|>` (130922) → `<\|reserved_101\|>` (130923) | 16, 16, 15 | 16.0 |
| Other | 478 | 0.064643 | `……\x0a` (78864) → `……\x0a\x0a` (113444) | 7, 8, 7 | 16.5 |
| Digits | 1,147 | 0.111233 | `２００` (126045) → `２０１` (126679) | 9, 9, 8 | 28.5 |

"bf16 steps" is the margin divided by 2⁻⁸, the spacing of bf16 numbers just below 1.0. It says
how many bf16 rounding steps separate the right token from its rival.

## fp32 vs bf16

### Storage: no practical difference

| | fp64 | fp32 | bf16 |
|---|--:|--:|--:|
| smallest margin | 0.015809320 | 0.015809320 | 0.015809340 |
| largest change in any token's margin vs fp64 | 0 | 6.7e-16 | 6.2e-8 |
| tokens with margin ≤ 0 | 0 | 0 | 0 |
| distinct (high, low) pairs per length | 1 | 1 | 1 |
| ‖z‖² across all tokens | 8189.515 – 8189.517 | 8189.514 – 8189.518 | 8146.09 – 8239.47 |

Every code is still two-valued after rounding. In fp32 and bf16, all tokens of the same length
also share the same two values, so rounding rescales codes per length without changing their
shape. Cosine ignores scale, which is why stored precision barely moves the margin.

Five class rows report a different pair under fp32 or bf16. Four are the same two tokens in the
other direction ("swapped" in the generated table): a pair's margin is the same seen from either
token, and rounding broke the tie the other way. The fifth (Other, bf16) is a different pair with
the same shape (7, 8, 7) and the same fp64 margin, chosen by a 6e-10 difference.

### Scoring: where the margin goes

110 tokens (the 3 lowest-margin tokens of each class, over all three storage precisions), each
scored against all 131,072 candidates:

| mode | wrong | ties | min margin | largest change vs exact |
|---|--:|--:|--:|--:|
| `fp32` | 0 | 0 | 0.015795 | 2.6e-4 |
| `bf16_fp32acc` | 0 | 0 | 0.015795 | 2.6e-4 |
| `bf16_out` | 0 | 0 | 0.012127 | 5.3e-3 |

- fp32 accumulation over D = 8,192 terms costs up to 2.6e-4, about 1.6% of the tightest margin,
  and bf16 inputs with fp32 accumulation cost no more. The same rounding makes dense results
  shift by about 1e-5 with the candidate block size (measured in `tests/test_dense_check.py`).
- Rounding dot products to bf16 costs far more. The largest absolute loss was Telugu token 57875
  (0.039290 → 0.034032). The largest relative loss was the tightest pair (0.015809 → 0.012127,
  −23%). There, the self dot (8,216.8) rounds down to 8,192 and the rival's dot rounds up, because
  the bf16 step is 64 at and above 8,192.

## Risks

**bf16 score output.** A bf16 cosine near 1.0 moves in steps of 2⁻⁸ ≈ 0.0039, and a raw dot product
near ‖z‖² ≈ 8,190 moves in steps of 32 to 64. The tightest pair is only 4.0 steps wide, and
`bf16_out` already loses 23% of it on exact codes. A fast decoder should accumulate in fp32 and
compare scores in fp32; bf16 GEMM output is not enough headroom once predicted vectors add their
own error.

**Silent ties.** `decode_ref` breaks exact ties toward the lowest token ID, as does `argmax`. If
reduced precision makes two scores equal, the decoder returns the lower-ID token with no error or
warning. None of the 110 checked tokens tied, but a bf16 decoder should report ties instead of
resolving them silently.

**Raw dot-product ranking.** After the bf16 cast, ‖z‖² depends on the token length (8,146 to
8,239, against a spread of 0.004 in fp32), because `high` rounds differently for each length.
Cosine cancels this; a raw dot product does not. For the tightest pair, ranking bf16 codes by dot
product gives the 32-byte token a margin of 0.012388 instead of 0.015809 (−22%), because its
31-byte rival's norm is 0.35% larger. Normalise, or score fp32 codes.

**Longer tokens.** The extension margin is about 1 − √(L/(L+1)), so it shrinks as tokens get
longer. P = 32 has no spare room (`output_shape.md`): this tokenizer already has 32-byte tokens.
A future tokenizer with 64-byte tokens at P = 64 gives 0.007874 for a 63/64-byte pair, about
2 bf16 steps, which leaves almost nothing for score rounding.

**Scope limits.**
- These margins are for exact codes. A predicted vector (week 2) has its own error, so the
  minimum margin is an upper bound on the score error a decoder can tolerate.
- Pure-bf16 accumulation (bf16 partial sums) was not tested; it would be much worse than
  `bf16_out`.
- The dense numbers come from CPU BLAS on an Apple M1. They are not bitwise reproducible across
  machines, and they make no GPU claim.
- The exact-margin CSV is fully reproducible: a second run produced it byte for byte.

## Reproduce

```bash
.venv/bin/python teams/04-ke2/src/margins/build_min_margin.py --P 32   # about 11 minutes on an M1
.venv/bin/python -m pytest teams/04-ke2/tests -q
```

Outputs go to `results/min_margin/`. `tests/test_min_margin_results.py` checks that the committed
results cover every class, that each committed pair reproduces its margin and rival, and that the
exhaustive minimum is not above the sampled one.
