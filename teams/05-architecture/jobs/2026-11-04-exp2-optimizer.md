# EXP-2: AdamW vs Muon at T2 (DRAFT, not sent)

Updated 2026-11-03 with the lead's answers in G5 (cap 90 min, AdamW lr rule, metrics only, no checkpoint) and the provisional muon_lr 1e-2. Rebased 2026-11-04 onto main after #253 (quality-run test settings) merged; approval.status/evaluation.approved in runtime.yaml are still unset, so this stays a draft. Rebased again 2026-11-05: PR #241 (Muon backend) merged 5 Nov — main now has Muon, so this job no longer needs anything outside main. TSAI proposed a shared EXP-1/Muon-screen training+held-out file (tokenizer sample v0-clean, train/heldout split, tokenizer teams/03-tokenizer/v0) 2h before this update; Shivanshu has not yet confirmed it, and approval.status/evaluation.approved are still unset, so this stays a draft. Checked again same day: Shivanshu confirmed TSAI's proposal and filed PR #310 (one EXP-1 job, all five rates), but #310 is still open and explicitly does not set a sha256 or approval.status; runtime.yaml on main still shows approval.status: pending and evaluation.approved: false, so this stays a draft.

```
Team:            05-architecture
Owner:           Vardhan Walavalkar (vpw)
Lead approval:   shivman
Question:        At T2 with the same budget, does Muon give lower held-out bits per byte than AdamW by more than the larger seed spread?
Script:          teams/05-architecture/harness/train_week2.py   (on main since PR #190). The Muon backend is Deepjyoti Saha's PR #241 (commit ecd9cfd), merged into main 5 Nov.
Command:         for arm in exp2_adamw exp2_muon; do for seed in 1234 1235 1236; do
                   python teams/05-architecture/harness/train_week2.py --config teams/05-architecture/configs/arms/${arm}.yaml --tokenizer inputs/tokenizer.json --byte-table inputs/raw_table_P32.npz --train-data <TBD> --heldout-data teams/05-architecture/heldout_v1/data/heldout_v1.jsonl --heldout-sources teams/05-architecture/heldout_v1/data/heldout_v1_sources.jsonl --heldout-report teams/05-architecture/heldout_v1/heldout_report.json --heldout-sha256 teams/05-architecture/results/heldout_v1.sha256 --device cuda --seed ${seed} --out out/${arm}_s${seed}
                   rm -f out/${arm}_s${seed}/checkpoint.pt   # metrics only, see Outputs
                 done; done
Config:          exp2_adamw.yaml: optim.lr = EXP-1 winner; if EXP-1 has no winner yet, 0.001 and the result is marked "comparison not final" (the file ships with 0.001 and comparison_final: false).
                 exp2_muon.yaml: optim.muon_lr = 1e-2, PROVISIONAL, from Deepjyoti Saha's T1 Muon screen (3 Nov, smoke mode, stand-in data, Colab T4 fp32, one seed: three-group bpb 2.159 at 1e-3, 2.077 at 1e-2, 2.233 at 1e-1). He will tell me if the official screen changes it, and this file follows; optim.lr = the same AdamW rate as the AdamW arm for the non-matrix parameters; momentum 0.95 Nesterov, weight decay 0, router on Muon (as set in #241).
Inputs:          tokenizer v0 sha256 2de039f2…, G4 raw table P32 content sha256 47d411a9…, held-out v1 (1,059 docs, sha 21c6e4b2…, merged in #191), training data TBD (the training mix is not set)
Hardware:        1 GPU, native bf16 (compute capability 8 or higher)
Max time:        90 minutes per run, as the plan says, both arms. 6 runs: 2 arms x seeds 1234, 1235, 1236.
                 Muon is projected at about 96 minutes (L4, see test log) plus evaluation, so it is likely to hit the cap. A run that stops before 1,221 steps is INCOMPLETE_NOT_A_RESULT and is not a result. Stated here on purpose, per the lead.
Precision:       bf16
Measures:        val/bpb (aggregate), per-slice bpb, three-group bpb, loss_ntp, gradient_norm, tokens_per_second, perf/step_ms, final_model_sha256, per seed and per arm
Expected result: Step time on an L4: AdamW about 3.9 s, Muon about 4.7 s at T2 batch 8 x 2048, projecting to about 79 and 96 minutes for 1,221 steps before the 24 held-out evaluations. L4 is not TSAI's GPU and the Muon figure was measured on my own backend, not #241. No bpb estimate; smoke CE starts at 11.79, near ln V. Void if any NaN or inf.
Outputs:         metrics only, 50 MB or less in total: out/<arm>_s<seed>/metrics.jsonl, summary.json, manifest.json, losses.txt, total_losses.txt. No checkpoint is returned.
                 The harness refuses --no-checkpoint in quality runs (train_week2.py line 99) and writes out/<run>/checkpoint.pt, so the command deletes it after each run. final_model_sha256 in summary.json is computed in the run and stays as the weights fingerprint.
Test log:        teams/05-architecture/jobs/2026-11-04-exp2-optimizer.log
```

## Open items before this can be sent
1. ~~**PR #241 merged**~~ — done. Merged into main 5 Nov (Instructor/TSAI), along with #304 (attn-4 gate settings); week-2 tests pass (101) with both. No longer a blocker.
1a. **Quality-run gate:** #253 is merged (4 Nov) — rope_theta, norm_eps, mtp_weight and moe.bias are on main. Still open: `runtime.yaml` approval.status is still `pending` (needs `agreed` with a reference) and evaluation.approved is still `false`. TSAI proposed a concrete fix 5 Nov: training file = train split of the cleaned tokenizer sample v0-clean (all 38 packs), held-out = its heldout split, tokenizer = `teams/03-tokenizer/v0`; TSAI will publish the converted `train.jsonl`/`heldout.jsonl` and their sha256. Shivanshu confirmed this same day and filed PR #310 (one EXP-1 job, all five rates, seeds 1234/1235/1236); #310 is open but explicitly does not set a sha256 or approval.status — it waits on TSAI publishing the files and the agreed resolution. Same two blockers (files published, approval fields set) still apply to the Muon screen and this job.
2. **`muon_lr`** is provisionally 1e-2 (Deepjyoti Saha's smoke-mode T1 screen, one seed). The official screen still needs the same two things as item 1a (approval fields set, shared training file named) — unaffected by #241 merging. If the official value moves, update `exp2_muon.yaml` and the Config line.
3. **AdamW lr** is the EXP-1 winner, or 0.001 and "not final". Only one arm has a posted result so far: Varshith's `lr_1e-2` (PR #286, H200, 3 seeds, val/three_group_bpb 3.2618 mean) — Shivanshu has confirmed this is a record only, not the EXP-1 quality result, pending the same approval fields and shared training file as item 1a. EXP-1 is filed as one lead job for all five rates once those land; TSAI said (5 Nov) compute is ready as soon as Shivanshu confirms the training file.
4. **Date.** Lead (G5, 3 Nov): Wed 4 Nov 23:59 IST was for EXP-1 seeds; that date passed with EXP-1 still unfiled (blocked on item 1a). T2 EXP-2 runs come after EXP-1, so no fixed date for this request yet. Ask when to file.
5. **Training data / mix** is unset on this job, but TSAI's 5 Nov proposal (see item 1a) would resolve it for EXP-1/Muon-screen; once Shivanshu confirms, the same file is the natural choice for this job's "Inputs" line too.
6. **Checkpoint deletion** (`rm -f`) is my workaround for the harness rule. Check with the lead and TSAI that a job command may delete it, or whether the harness should gain a quality-run option.
7. **Muon step time on #241** is not measured. Now that #241 is on main, a real run (not my own backend) would replace the 96 min projection.
8. **Lead approval handle** `shivman` is read from the merged PR #188 branch name and the #197 merge. Confirm it.
