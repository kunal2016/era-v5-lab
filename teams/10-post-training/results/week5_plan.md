# Team 10 Lab 5 (Week 5) Execution Plan & Evidence Tracker

Active branch: `g10-week5-post-training` (cut cleanly from `upstream/main` `317b31f3`).  
Deadlines: **70% due Mon 30 Nov (Day 3)** · **100% due Wed 2 Dec, 7:00 AM IST** · **Next class: Sat 5 Dec**.  
Evidence list owner: `saitej123`. Public text names teams only.

## Done-Gate Rules (TSAI Lab 5 Brief, 28 Nov)

A task is done only when:
1. The output exists and a reviewer can reproduce it from the stated command.
2. It passes the check named for it (`pytest`, `generate.py --check`, `sha256sum -c`, `pr-guard`).
3. Every difference from the reference check is written down (including negative results and scope limits).

## Lab 5 Task Matrix (Status & External Dependencies)

| # | Brief Item | Status (28 Nov) | Deliverable & Check | External Dependency (Who to Contact) |
|---|---|---|---|---|
| **I1** | 2-hour channel ack + evidence owner + NC/ND rule check | **Done** (ack sent) | Team channel reply | **TSAI:** confirm whether "NC, ND and unstated are allowed" in slide 1 is a typo (`excluded` per 3 Nov rule) |
| **I2** | Close `#781` with the two reader OKs | **Code merged (`#861`); issue open** | Comment & close `theschoolofai/era-v5-lab#781` (`6/6` templates `train`) | **None** (issue close only) |
| **I3** | TSAI staging recipe for dry run 2 jobs | **Done (in `#882`)** | `jobs/2026-11-28-g10-dryrun2-staging-recipe.md` (`#564`, `#565` shards `0:4`, `sha256sum -c`) | **TSAI:** stage the 7 files, fix Docker runner on job machine, run `#861`'s two jobs |
| **D0** | Written SFT & RL data request to Teams 1 & 2 (by Sun 29 Nov) | **Request sent (in `#882`); awaiting replies** | `docs/data_request_teams1_2_v1.md` | **Team 1 (Data A, `@patilvijay23`) & Team 2 (Data B, `@shankarpandala`):** reply with `parquet`/`pack_table`/F2 sources & gaps (math RL pool, native Indic SFT, remaining 8 Indic RL languages) |
| **T1** | Licence row for every new source before staging | **In progress** | `licences/licence_table.md` (`tests/test_specs.py`) | **TSAI** (NC/ND wording confirmation) + **Teams 1 & 2** (new candidate sources from D0 reply) |
| **T2** | Confirm Team 3 `special_tokens.md` (`#873`) | **Done (`#882` + `#873` Option (a))** | `special-tokens/special_tokens_v1.md` synced to `e6b93a93...` | **TSAI / Team 3 (`@rjvim`, `@sohamniyogi`):** merge `#873` |
| **T3** | Indic prompts inventory (sources, size, checker, missing) | **Done** | `rl/indic_prompts_v0.md` §0 (`6/6` `train`, `12/12` `reward.py --type indic`) | **Team 2 (Data B, `@shankarpandala`):** human templates + native-reader OKs for `te, kn, bn, mr, gu, ml, or, pa` |
| **T4 + D1** | Base-to-chat plan + SFT plan & small SFT run | **Plan in `#882` (received by Team 11 `#878`); small SFT runs committed** | `docs/post_training_plan_v1.md`, `results/small_sft.md`, `results/dt_vs_fft.md`, `results/lab5_dt_muon_recompute.md` | **Teams 1 & 2:** fill dataset pointers once D0 replies arrive; **Team 11 (`@pyru`)** cites after `#882` merges |
| **D2 + Optim** | Hybrid Muon (no hard-coded AdamW, buffer save/restore, optim step share) + DT SFT & GRPO + recompute + `--dt-unseen` | **Code & CPU stand-in checks done** | `capstone/hybrid_optim.py`, `capstone/sft_g5.py`, `sft/bench/train.py`, `rl-loop/train.py`, `results/lab5_dt_muon_recompute.md`, `results/lab5_grpo_dt_vs_fft.md` | **Team 5 (`@shivman`) / TSAI:** fix idle-expert zero-grad Muon bug in `optim.py:78` (`#875`); **TSAI:** run `dryrun2-1234` comparison + `#142` 4B/8B ladder; **Team 12 (`@SomaKorada07`):** `results/dt_quantized_base.md` (`#889`) |
| **D3** | GRPO setup + small working run + Team 8 metrics feed | **Setup & stand-in done** | `docs/post_training_plan_v1.md` §3, `results/small_rl.md`, `results/dt_then_rl.md`, `results/lab5_grpo_dt_vs_fft.md` | **Team 8 (`@sandeepkunkunuru`):** confirm `metrics.jsonl` RL feed schema; **TSAI:** run `jobs/2026-11-17-dt-then-rl-code.md` on `dryrun2-1234` |
| **T5 + D4** | Fast RL rollouts survey + Quantized-rollout GRPO (with Teams 12 & 9) | **Survey + Team 12 `#894` numbers done** | `rl/fast_rollouts_v1.md` (`Q8_0` pick-first, `Q4_K_M` rejected at `k3=0.0739`) | **Team 12 (`@SreekanthZipsy`, `@SomaKorada07`):** PyTorch `bf16`-reference mismatch (`sarvam-1` + `Qwen2.5-Coder-1.5B`) + `bf16` decode `tok/s` + quantized policy copy; **Team 9 (`@rahulni`):** mini-benchmark suite definition for every-`N`-step checks |
| **D5** | Forgetting vs learning separation | **Tooling & plan done** | `sft/tests/forgetting.py`, `capstone/forget_bpb_kept.py`, `capstone/watcher_rows_to_report.py`, `docs/post_training_plan_v1.md` §4 | **Team 9 (`@rahulni`):** Tier B watcher rows on `dryrun2-1234` base + kept arms (`g10-dr2-{full,lora,dt}`, `g10-rl-final`) |
| **D6** | Waste elimination (shared base weights, rollout cache, restartable stages) | **Done & tested** | `capstone/dryrun2_dt_compare.py` (`--no-before`), `rl-loop/rollout_cache.py` (`66.67%` hit rate across 3 GRPO arms), `dt/test_lab5_grpo_and_cache.py` | **None** |
