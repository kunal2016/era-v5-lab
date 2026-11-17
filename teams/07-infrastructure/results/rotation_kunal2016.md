# Rotation log: kunal2016, Team 07 Infrastructure, week 3

**Run:** dry run 1 (Team 05 job request, PR #475, merged 16 Nov)  |  **Run ID:** `dryrun1-1234` (output folder in the request)
**Setup:** exp2_muon at T2 size, muon_lr 0.01, seed 1234, tokenizer p1536 (sha256 `e6b93a93...a64b`), TSAI text bundle, 1 GPU, bf16, one process
**Run by:** TSAI. Result posted as a comment on PR #475 (16 Nov 2026)
**Logs read:** TSAI's result comment on PR #475. The per-step logs (`metrics.jsonl`, `losses.txt`) are **not yet returned to the repo** (checked on main at `6614178`, 17 Nov).
**Steps assigned:** 611 to 915 (R1 is an offline review split by step range; acting lead, G7 chat, 17 Nov).
**If the per-step logs are not returned by Wed 18 Nov EOD**, R1 stays as written here, from TSAI's summary, and says so (acting lead's rule). This PR is not held for them.

---

## 1. Shift summary (R1, due Wed 18 Nov)

For steps 611 to 915, check step continuity, loss spikes, gradient norm and throughput, and run Team 08's alarms
offline (`alarms.py --jsonl`). None of these can be done yet: the evidence folder
`teams/05-architecture/jobs/evidence/2026-11-15-dryrun1/` still holds only the 3-step smoke run (checked on main at
`6614178`, 17 Nov). The values below are TSAI's whole-run summary.

| Item | Value | Source |
|---|---|---|
| Steps completed | 1,221 of 1,221. Status COMPLETED | TSAI comment |
| Final train cross-entropy | 4.8906 | TSAI comment |
| Final gradient norm | 0.7037 | TSAI comment |
| NaN or inf in the loss | none | TSAI comment |
| Held-out val/bpb | 1.5159 (English 1.9844, code 1.8901, Indic mean 1.3289, three-group 1.7345) | TSAI comment |
| Same arm with old tokenizer v0, seed 1234 | 1.6443 (change −0.1284) | TSAI comment |
| Checkpoints written | 1, at the last step (about 2.2 GB), kept by TSAI | TSAI comment; job request open item 3 |
| Tokens per second, step time, wall time | **not reported yet** | needs `metrics.jsonl` |
| Loss curve, spikes | **not reported yet** | needs `metrics.jsonl` / `losses.txt` |
| Alerts | none reported | Team 08 has `alarms_dryrun1.md` (#494); no alert posted |
| Overall | finished cleanly by the summary; the curve is not yet checked | |

---

## 2. Failure log (R2, due Thu 19 Nov)

No failures reported. TSAI reports the run COMPLETED, 1,221 of 1,221 steps, with no NaN or inf.

| # | Time | Step | Exit / code | Cause | Evidence | What the system did |
|---|---|---|---|---|---|---|
| — | — | — | — | none reported | TSAI comment, PR #475 | — |

To confirm when the logs come back: step numbers run 1 to 1,221 with none missing and none repeated
(a repeat would mean an unlogged restart).

---

## 3. Restart log (R2)

No restarts in the run. The trainer ran as one process. It was not run under `ckpt/supervisor.py` and it does not
save during the run (job request, open item 3), so a crash would have lost the whole run rather than restarting.

The only restart this week is the restore drill (core task 5, PR #491). It is being rewritten for the
finished run (G7 chat, 16 Nov, acting lead and task 5 owner):
- **(A)** restore the saved final checkpoint with a fresh `--out`. Pass: identity check passes, step 1,221,
  `final_model_sha256` and `losses.txt` bit-equal to #475.
- **(B)** if TSAI agrees: rerun with `--stop-after 610`, resume to 1,221, compare `losses.txt` bit for bit with #475.

**To log here when its logs return:**

| # | Failure | Restored from | Steps restored / resumed | Steps skipped | Loss before / after | Result |
|---|---|---|---|---|---|---|
| R1 (planned drill) | planned stop | final checkpoint (A) or step 610 (B) | | | | |

---

## 4. Gate 3 checks

- [x] The run ended: 1,221 of 1,221 steps, COMPLETED (TSAI)
- [x] No NaN or inf in the loss (TSAI)
- [x] No restart during the run, so no restart from a non-COMPLETE checkpoint
- [ ] No step lost or repeated: **needs `metrics.jsonl`** to check every step from 1 to 1,221
- [x] COMPLETE-only restarts: shown by `results/restart_cpu.txt` and `results/restart_node.txt` (dry run 1 had none)
- [ ] Restore drill (#491) gives the same loss and model hash as #475: **waits for its logs**

## 5. Gaps and questions for the team

1. **Per-step logs.** TSAI returned a summary, not `metrics.jsonl` / `losses.txt`. Without them R1 has no tokens per
   second, step time or loss curve, and the "no lost steps" check cannot be done. Team 05 also needs them for
   `dryrun1_loss.md`. Ask TSAI to return them to `teams/05-architecture/jobs/results/2026-11-15-dryrun1/`.
2. **COMPLETE checkpoint.** The final checkpoint is the trainer's own `checkpoint.pt`, with no `MANIFEST.json` and no
   `commits.jsonl`, so it is not COMPLETE by queue rules v1.1 (R4). **Answered** (acting lead, G7 chat, 16 Nov): dry run 1 had
   zero restarts and did not use the Checkpointer; the COMPLETE-only restart evidence stays `results/restart_cpu.txt`
   and `results/restart_node.txt`.
3. **Periodic saves.** Dry run 1 saved only at the end, so the 10-minute interval (`docs/checkpoint_interval.md`, PR #463) and
   the supervisor were not exercised. Should dry run 2 run under `ckpt/supervisor.py` with Team 07's checkpointer?
4. **Save timing not measured.** `docs/checkpoint_interval.md` §4 (PR #463) expects dry run 1 to give, for each
   10-minute save, the stall (`save_seconds.stall`, limit 12 s) and the time from `checkpoint.started` to
   `checkpoint.committed` (limit 600 s, CK-10 at 0). Dry run 1 made one save, outside Team 07's checkpointer, so it
   gives none of these. The interval stays provisional until a run saves every 10 minutes.
