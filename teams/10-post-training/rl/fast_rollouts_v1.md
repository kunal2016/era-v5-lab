# Fast RL Rollouts Survey & Quantized-Rollout GRPO Plan (Lab 5 Task 5 & Design Task 4)

Rollout generation accounts for **70–85%** of wall-clock time in verifiable-reward GRPO (`16` prompts × `8` completions × `1,536+` tokens per step). This document compares published rollout acceleration methods, states their quality/mismatch costs, names the method Team 10 will test first, and specifies the integration with **Team 12** (quantized policy copy) and **Team 9** (mini-benchmark check every `N` steps).

---

## 1. Comparison of Published Rollout Speedup Methods

| Method | Mechanism | Reported Speedup | Quality / Mismatch Cost | Implementation Complexity |
|---|---|---|---|---|
| **1. Batched KV-cached native decoding (`g5_batch`)** | Pre-allocated KV cache + grouped-head attention across all prompts of a step (`rl-loop/g5_decode.py`) | **12.8x** measured vs unbatched `policy` on T4 (`44.3 s -> 3.45 s`/prompt, `results/b5_sampler_2026-11-23.md`) | **Zero precision mismatch** (`K3 KL = 0` at equal dtype; `logprob_gate` verified) | Already built and merged (`#746`, `#797`) |
| **2. FP8 / INT8 Quantized Rollouts + Mismatch Correction (`FlashRL`, `QuRL`, NVIDIA FP8 RL)** | Generate rollouts with an FP8 or INT8/Q8_0 quantized copy of the policy (`vLLM`/`SGLang`/Team 12 quant copy), compute trainer log-probs and updates in BF16/FP32, and correct off-policy drift with Truncated Importance Sampling (**TIS**, `min(exp(lp_train - lp_rollout), C)`) or trust-region masking (`objective_v1`) | **1.4x–2.2x** rollout throughput (higher memory headroom allows larger batch/concurrency) | Small precision gap (`K3 KL ~ 1e-4 to 1e-2`); **can destabilize RL without TIS/trust-region correction**, especially on long CoT and MoE routing flips | Medium — `rl-loop/grpo.py` already implements `mismatch()` (`K3`, `|log ratio|`) and `tis_weights(tis_clip)`; needs Team 12 quantized copy + fast weight refresh |
| **3. 4-bit Quantized Rollouts with LoRA/Error Compensation (`QeRL`)** | NF4/INT4 quantized rollout weights plus low-rank / adaptive quantization-noise compensation | **2x–3x** memory reduction and higher decode throughput on memory-bound GPUs | Higher token-level log-prob divergence (`K3 KL` up to `10x` FP8); Team 12 wide-pass (`#853`) showed `Q4_K_M` degrades weakest Indic languages first | High — unacceptable Indic drift risk at `Q4_K_M` per Team 12 `#853` |
| **4. Speculative / Draft Decoding (with Team 6)** | Small draft model proposes `k` tokens verified in parallel by the policy model | **1.5x–2.5x** on greedy/low-temp code; lower at `T=0.8–1.0` sampling | **Exact** (mathematically lossless under rejection sampling) | Medium-High — requires a draft model matched to `p1536` tokenizer + Team 6 serving integration |
| **5. Async / One-Step Off-Policy Rollout Pipeline** | Overlap rollout generation of step `t+1` with learner update of step `t` | **1.3x–1.8x** end-to-end step throughput (eliminates GPU idle time) | 1-step policy staleness; requires TIS / trust-region mask (`tr_epsilon = 0.2`) | Medium — needs separate rollout & learner GPU pools |

---

## 2. Which Method Team 10 Tests First (Pick-First Decision)

**Pick-first: FP8 / Q8_0 Quantized Rollouts (Method 2) on top of `g5_batch` / `vLLM` with TIS + trust-region mismatch correction.**

**Why first:**
1. **Team 12 alignment (`#853`):** Team 12's wide-pass quantization evidence shows **`Q8_0` preserves scores across every tested model including Indic**, whereas `Q4_K_M` drops points on Indic languages first. Starting at `Q8_0` / `FP8` avoids Indic collapse during RL rollouts.
2. **Existing mismatch instrumentation:** `rl-loop/grpo.py` and `rl-loop/train.py` already compute per-step `mismatch_k3` (`K3 KL(trainer || rollout)`), `mismatch_abs_logratio`, `tis_clip` importance weights, and `objective_v1`'s closed trust-region mask (`tr_epsilon = 0.2`), plus `capstone/mismatch_g5.py` tracks MoE top-k expert flip rates between engines.
3. **Zero extra model needed:** Unlike speculative decoding, it needs no separate `p1536` draft model.

---

## 3. Experimental Protocol with Team 12 and Team 9 (Design Task 4)

1. **Quantized rollout copy (from Team 12):** Receive Team 12's `Q8_0` / `FP8` policy export (`agreement and KL report` against `bf16` base weights) for the target small model or `dryrun2-1234`.
2. **High-precision learner (Team 10):** Recompute token log-probs in `bf16` autocast with `fp32` master weights in `rl-loop/train.py`, applying `--tis-clip 2.0` (under `grpo`) or `tr_epsilon = 0.2` (under `objective_v1`).
3. **Periodic quality guard (from Team 9):** Every `N = 10` RL updates, evaluate the rollout policy copy on **Team 9's mini-benchmark** (`suite definition`, firewalled).
4. **Metrics reported in PR:**
   - Rollout throughput (`tokens/s` quantized vs `bf16` baseline) and GPU idle time.
   - Mismatch metric (`mean_mismatch_k3`, `p95 |log ratio|`, top-k MoE expert flip rate vs `bf16` rollouts).
   - Held-out verifiable reward curve and Team 9 mini-benchmark score every `N` steps.
   - **Hard stop rule:** abort quantized rollouts if `mean_mismatch_k3 > 0.05` or if Team 9 mini-benchmark drops by `> 2 * stderr` relative to the `bf16` control arm.

### External Dependencies to Execute Live Run
- **Team 12:** Quantized `Q8_0` / `FP8` policy copy + agreement/KL report for the RL test model.
- **Team 9:** Mini-benchmark suite definition for every-`N`-step rollout policy checks.
