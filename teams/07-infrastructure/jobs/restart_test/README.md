# Restart test

Week-2 task (Gate 2): **a killed job restarts from the last COMPLETE checkpoint with equal loss.**

- **Run A** trains Team 05's tiny MoE (`teams/05-architecture/harness/train.py`, `configs/config_v0.yaml` +
  `configs/small/tiny_moe.yaml`, seed 1234) from step 1 to 200 without a stop, with a checkpoint every 25 steps.
- **Run B** is the same command under `ckpt/supervisor.py`. Once it is past step 140 and has a COMPLETE
  checkpoint, it is killed with **SIGKILL** (no warning, no save: a lost node or the OOM killer). The supervisor
  sees the crash and starts the same command again; the trainer's `Checkpointer.restore()` loads the newest
  COMPLETE checkpoint (`MANIFEST.json` written, `latest.json` moved) and trains on to step 200.
- For **every step 1 to 200**, `loss_ntp` and `loss_mtp` must be **bit-equal** to run A and the batch data ID
  (global batch position + sha256 of the batch tokens) must be the same. For the steps run B did twice
  (between the checkpoint and the kill), the value after the restart counts.
- The supervisor log must show exactly one restart (exit -9) and then exit 0, and the restarted trainer must
  start at the step after the checkpoint the supervisor named.

The model, config, loss and data stream are imported from `jobs/restore_test/restore_test.py`, so both tests
train exactly the same thing.

## How to run

Same requirements as the restore test (torch 2.14.1 or newer; `pip install -r teams/04-ke2/src/requirements.txt`).
One command, no GPU, no network, about 10 s on a laptop:

```bash
CUDA_VISIBLE_DEVICES="" python teams/07-infrastructure/jobs/restart_test/restart_test.py
CUDA_VISIBLE_DEVICES="" python teams/07-infrastructure/jobs/restart_test/restart_test.py --report teams/07-infrastructure/results/restart_cpu.txt
```

| Flag | Default | Meaning |
|---|---|---|
| `--steps` | 200 | last step |
| `--save-every` | 25 | checkpoint every N steps |
| `--kill-at` | 140 | SIGKILL run B once it is past this step |
| `--out` | `out/` next to the script (git-ignored) | the only folder the script writes, apart from `--report` |
| `--report` | none | also write the plain-text result (the file in `results/`) |

Exit 0 and one `PASS` line when every check holds; 1 at the first difference; 78 if a run crashed.
`out/result.json` has every step of both runs and the supervisor log; `out/supervisor.jsonl` one line per attempt.

Result on CPU: [`results/restart_cpu.txt`](../../results/restart_cpu.txt). One process only for now; the GPU
run goes through a TSAI job request.
