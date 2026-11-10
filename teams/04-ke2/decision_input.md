# KE2 decision input for Gate 2 (Team 04-ke2, consolidated 10 Nov 2026; input due Thu 12 Nov; TSAI decides Sat 14 Nov)

Everything below is read from a committed results file in one of the four week-2 pull requests that form the
Team 4 package, after a joint review of the four on 10 Nov. All four were merged into `ke2-week2-stitch` on 10 Nov
(section 9); the documentation fixes from the review are applied in the same pull request as this file.

| PR | author | what it adds | files cited below |
|---|---|---|---|
| theschoolofai/era-v5-lab #268 | Yasir Reshi | GPU decode determinism, every id, batch 1 / 7 / 4,096 | `determinism_gpu.md`, `results/decode_gpu/` |
| swatibansal/era-v5-lab #2 | avnishbm | Team 3 candidate tables: v0, v0.1, v1-c1, C1, C2, C3 | `output_shape.md`, `results/tokenizer_candidates/` |
| swatibansal/era-v5-lab #3 | mukund-23 | Theorem 2 (structural decode) and Theorem 3 (nearest-code cosine) | `proof.md` sections 5 and 6, `results/decode_checks.json` |
| swatibansal/era-v5-lab #4 | dattatreyamanjunath | exact minimum decode margin per script class, fp64 / fp32 / bf16 | `min_margin.md`, `results/min_margin/` |

Review outcome: all four are approve-with-changes; every change asked for is documentation, none is code or a
number. The four merge together after one stitch commit (section 9). On the merged tree `pytest teams/04-ke2/tests -q`
gives 158 passed, 2 skipped (the opt-in MPS and CUDA tests) with the tokenizer present, and 99 passed, 61 skipped
without it; no failures.

## 1. Byte table type: raw bytes

Use the raw byte table (exact token bytes from the inverted ByteLevel alphabet), not `decode([id])` text.
On all six measured candidates the raw table has 131,072 unique rows and 0 collisions; the decode table has
1,141 (v0, v0.1), 1,098 (v1-c1), 1,095 (C1) and 1,096 (C2, C3) excess tokens, every one of them a partial-UTF-8
fragment that `decode([id])` turns into U+FFFD (`results/tokenizer_candidates/collision_groups.csv`,
`summary.json`). No whole-token and no special-token collision exists. Theorem 1 says the codec adds none
(`proof.md` section 3).

## 2. P = 32

Longest token is 32 bytes on v0, v0.1, v1-c1, C1, C2 and C3; nothing is cut at P = 32; 0 raw collisions
(`results/tokenizer_candidates/summary.json`). P = 64 doubles D for no gain (`output_shape.md`). D = 8,192.
Not measured: Team 3's week-2 replacements C1-s0, C2-s0, C3-s0 (their manifests mark the committed C1 to C3 as
replaced) and the v2 file (sha `0862f6…`). A token over 32 bytes in any of them would reopen P. Re-check with
`python src/revalidate_tokenizer_candidates.py` once Team 3 publishes them; the script refuses a file whose sha256
is not in its registry.

## 3. Decode margins, precision, and what Team 5's decoder must do

This replaces the tau proposal. No PR in the package measures a rejection threshold; see risk 2.

Margin floor. The margin of a token is its best cosine minus its second-best over all 131,072 raw-table codes.
Computed exhaustively in float64 from the two-valued code structure (`results/min_margin/summary_P32.json`), the
smallest margin anywhere is 0.015809, between the 32-space token (id 50346) and the 31-space token (id 83647),
in Code/Structure. Theorem 3 proves this is the worst possible pair shape at P = 32 and that the pair is unique in
the vocabulary (`proof.md` section 6). Other class minima: Latin 0.028234, Devanagari 0.031813, the other Indic
scripts 0.037 to 0.056, Digits 0.111 (`results/min_margin/min_margin_P32.md`). For most Indic scripts the closest
rival of a word is the same word minus its last byte, a partial-UTF-8 fragment.

Sufficient condition. Nearest-code decoding returns the true token for any vector whose cosine to the true code
exceeds 0.99604 at P = 32 (0.99605 at P = 64); the bound is tight (`proof.md` section 6 (d),
`results/decode_checks.json`).

Precision. Storing codes in fp32 or bf16 is harmless: margins move by at most 6.7e-16 and 6.2e-8. Scoring
precision is not: fp32 scores shift margins by -5.3e-5 to +2.6e-4; bf16 inputs with fp32 accumulation by -2.6e-4
to +9.2e-5; bf16-rounded scores by -5.3e-3 to +3.5e-3, which cuts the tightest margin by 23% to 0.012127
(`results/min_margin/summary_P32.json`, `min_margin.md`). On GPU fp32 the worst margin error against float64 is
4.1e-4 at batch 4,096 (`results/decode_gpu/raw_P32.json`), 39 times smaller than the floor.

Requirements for Team 5 (and Team 6 for a fast decoder):
1. Decode by cosine over all 131,072 raw-table codes, each divided by its own norm (the norms differ by length).
2. Keep scores and accumulators in fp32 or better; never rank bf16-rounded scores or raw bf16 dot products.
3. Report the margin (best minus second-best) and ties with every decode. Ties go to the lowest id silently in both
   reference implementations, so a tie is invisible unless reported.
4. Use the cosine decoder, not the structural decoder of Theorem 2, for predicted vectors (section 5).

## 4. Determinism

GPU (closes risk 1). fp32, TF32 off, `torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`,
three fresh processes per batch size: the id hashes of all nine runs match each other and match the CPU float64
reference computed by `decode_ref.decode` in a separate process, elementwise for all 131,072 ids; ties 0
(`results/decode_gpu/raw_P32.json`, `raw_P32_sha256.txt`). The score hashes repeat within a batch size and differ
across batch sizes (cuBLAS picks a kernel per shape); the ids are the portable artefact. fp32 score error against
float64: 2.2e-5, 7.5e-5 and 2.35e-4 at batch 1, 7 and 4,096; `NVIDIA_TF32_OVERRIDE=0` gives identical numbers
(`results/decode_gpu/tf32_override_0/`). Caveats: one consumer laptop GPU (compute capability 8.9, Windows, torch
2.14.1+cu130, CUDA 13.0); the decoder is a dense fp32 GEMM in `src/determinism/decode_gpu.py`, checked only against
the float64 `decode_ref.py`; the 5e-4 tolerance has 22% headroom at batch 4,096 and larger batches were not run.

CPU. The package has no CPU counterpart of the GPU run (three fresh processes per batch size, hashes compared). The
CPU side of the evidence is the single float64 reference pass inside `decode_gpu.py` and the week-1 CPU decode files
in `results/`.

Target for Team 6: id hash `31c8d0e0ac50cff5c8021f88a2b608de2298fdbf216c620a40e83d2adbe26f9a` (raw table, P = 32,
format `ke2-decode-gpu-ids-v1`, the identity map); tolerance 5e-4 on scores and margins against `decode_ref.py`.

## 5. What is proven (proof.md sections 5 and 6)

Theorem 2. A vocabulary-free structural decoder with cut-off 8 recovers every token from its clean code in exact
arithmetic, fp32 and bf16 (131,072 / 131,072 at P = 32 and 64), and under any per-entry error below 7.966
(`results/decode_checks.json`). This is a sup-norm guarantee: a rival mixture of weight 0.3 already lights a short
rival's extra cell while the cosine to the true code is still 0.988, so Theorem 2 does not cover structured noise.
Predicted vectors must use the cosine decoder.

Theorem 3. Closed form for the cosine between any two codes from their lengths and shared byte positions, matching
the codec to 1.7e-15 on 10,010 real pairs; cos = 1 iff the strings are equal; the margin floor and the 0.99604
guarantee of section 3 follow. Both theorems and every number in them were re-derived independently in the 10 Nov
review and agree.

## 6. Revalidation of TSAI's experiments (private repo theschoolofai/era-v5-ke2)

Status as reported in the open PR #5 there, not reviewed as part of this package: R1 single-seed re-runs match
within tolerance for T0, C1, E1, E2, E3a, E4, E4 best, E5, E6, E8, S02a and S10; E3b timings differ; S02b and
S03a blocked; E7, S03b, S04 pending; S05 to S08 depend on the TSAI job request. Nine differences D1 to D9 are listed
there for team review, including a parameter-audit bug (D2) that touches the parameter count behind risk 4.

## 7. EXP-5 bits per byte (Team 5)

Not yet delivered. [Insert Team 5's EXP-5 bpb for the KE2 arm vs the dense baseline when received.] This is the only
item that speaks to whether KE2 helps the language model; everything above speaks to whether it is safe and
well-defined.

## 8. Open risks after the package

| # | owner | status | risk |
|---|---|---|---|
| 1 | TSAI | closed with caveats | CUDA determinism: PR #268, section 4. Caveats: one GPU class, dense decoder, batch <= 4,096. |
| 2 | Team 5 -> Team 4 | open | No predicted vectors yet. No rejection threshold (tau) exists in the package; it must be set on Team 5's vectors, and the margin, not a threshold, is what detects a near-code wrong answer. |
| 3 | TSAI | open | E4 to E8 are single-seed in TSAI's files and single-seed in the R1 re-run (section 6). Multi-seed still needed; E7 not re-run. |
| 4 | Lab decision | open | Unit-norm codes cannot express a per-token frequency prior; the fix is one scalar per token, V extra parameters. D2 in section 6 says the parameter audit script is wrong for every arm, so re-audit before deciding. |
| 5 | Team 4 with Team 3 | partially closed | v0, v0.1, v1-c1, C1 to C3 measured, all 32 bytes max, 0 raw collisions. C1-s0, C2-s0, C3-s0 and v2 unmeasured. |
| 6 | Team 4 with Team 3 | open | The real `special_tokens_map.json` is still unconfirmed; no PR in the package touches it. |
| 7 | Team 5 | partially closed | Margin floor and precision rules are now proven and measured (section 3). The cosine-decoder requirement and the margin-reporting requirement are stated here, not yet in Team 5's decoder. |
| 8 | Team 4 | new | Team 3's `verify_kronecker_constraints_unified.py` reports 131,072 normal and 0 special tokens; the correct split is 130,716 and 356 (`output_shape.md`). Its length and cross-script gates still pass. File with Team 3. |

## 9. How the package was merged

Merged into `swatibansal/era-v5-lab:ke2-week2-stitch` on 10 Nov in the order #3, #2, #4, #268, each as a
non-fast-forward merge so every author's commits are kept as written. #3 and #2 applied cleanly; #4 and #268
conflicted with the earlier ones only in `teams/04-ke2/README.md`, and #268 with #4 in `src/ruff.toml`; both were
resolved as the union of the index rows and of `known-first-party`. On the merged tree `pytest teams/04-ke2/tests -q`
gives 158 passed, 2 skipped with the tokenizer and 99 passed, 61 skipped without it.

Documentation fixes from the review, applied with this file:
- `determinism_gpu.md`: the precision table now labels the first two rows as the 16,384-code study and adds the
  full-run score errors (2.2e-5, 7.5e-5, 2.3e-4); the self-reference on line 6 is fixed; the section 5 clock,
  power-state and worker-memory figures are marked as read during the run with no committed source, and the
  batch-4,096 row as resting on 4 to 5 samples. Hardware names stay: the lab has no rule against them and other
  teams publish them. The lab PR #268 body still quotes the study numbers; only the document was corrected.
- `output_shape.md`: the v0 hash tail is the tokenizer's (`…f2af8e5`), not the build script's; the status line names
  what is measured (v0, v0.1, v1-c1, C1 to C3) and what is not (C1-s0, C2-s0, C3-s0, v2).
- `proof.md`: Theorem 2 and Theorem 3 are sections 5 and 6 and "Run it" is section 7, after them, with the week-2
  commands folded in; section 4 now points at them instead of excluding decoding; Theorem 2's "what it does not say"
  states that structured noise is outside the bound and that predicted vectors use the cosine decoder and the margin.
- `min_margin.md`: says that its fp32 / bf16 storage figures round both query and candidates; "swapped" is explained
  per precision (Code/Structure in both, Latin and Mixed in fp32 only); the raw-dot margin and norm figures are tied
  to the bf16 per-length values they come from.
