# EXP-2: AdamW vs Muon at T2 (DRAFT, not sent)

Updated 2026-11-03 with the lead's answers in G5 (cap 90 min, AdamW lr rule, metrics only, no checkpoint) and the provisional muon_lr 1e-2.

```
Team:            05-architecture
Owner:           Vardhan Walavalkar (vpw)
Lead approval:   shivman
Question:        At T2 with the same budget, does Muon give lower held-out bits per byte than AdamW by more than the larger seed spread?
Script:          teams/05-architecture/harness/train_week2.py   (on main since PR #190). The Muon backend is Deepjyoti Saha's PR #241 (commit ecd9cfd); this job needs #241 merged first.
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
1. **PR #241 merged** (Muon backend, Deepjyoti Saha). Plan rule: no script, no job request. It is rebased on main, 76 tests pass (Udit confirmed, also with #253), review pending.
1a. **Quality-run gate:** #253 merged, `runtime.yaml` approval.status agreed with a reference and evaluation.approved true (or an agreed resolution file), one training file for all arms. Same blockers as the EXP-1 and Muon screen runs.
2. **`muon_lr`** is provisionally 1e-2 (Deepjyoti Saha's smoke-mode T1 screen, one seed). The official screen runs after #253 merges, `runtime.yaml` approval is set and the single training file is named. If it moves, update `exp2_muon.yaml` and the Config line.
3. **AdamW lr** is the EXP-1 winner, or 0.001 and "not final". EXP-1 runs 1234 on 3 Nov, 1235 and 1236 on 4 Nov.
4. **Date.** Lead (G5, 3 Nov): Wed 4 Nov 23:59 IST is for EXP-1 seeds. T2 EXP-2 runs come after EXP-1, so no fixed date for this request. Ask when to file.
5. **Training data / mix** is unset. The request needs a named public dataset or sample pack under "Inputs".
6. **Checkpoint deletion** (`rm -f`) is my workaround for the harness rule. Check with the lead and TSAI that a job command may delete it, or whether the harness should gain a quality-run option.
7. **Muon step time on #241** is not measured. An L4 run of #241 would replace the 96 min projection, which came from my own backend.
8. **Lead approval handle** `shivman` is read from the merged PR #188 branch name and the #197 merge. Confirm it.
