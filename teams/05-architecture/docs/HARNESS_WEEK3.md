# Week 3 harness

## G8 live metrics

Pass the job package's run ID as `--run-id "$RUN_ID"` to use the same identity in G5 and G8. IDs begin with a letter or digit and may also contain dots, dashes, and underscores. A fresh invocation without the flag generates an ID. The trainer records it in `manifest.json`, `summary.json`, and the native checkpoint. Resume uses a fresh output directory and recovers the checkpoint ID if the flag is omitted. If supplied, the ID must match the checkpoint. For a compatible legacy checkpoint without an ID, the checkpoint file's SHA-256 is its ID. The resume identity check still applies.

To enable the G8 adapter, put `teams/08-monitoring/metrics_logger` on `PYTHONPATH` and pass `--logger-factory g5_adapter:make_writer`. The trainer writes the manifest before calling the factory once with the output directory. The returned writer receives `write(row)` in step order, including the initial evaluation at step 0 and the saved history on resume. The trainer calls `flush()` before writing final artifacts and `close()` on exit. A logger error fails the invocation.

The adapter writes `g8/metrics.jsonl` with `run_id`, `step`, `time`, and the existing G8 metrics. It flushes at step 0, every 10 steps, on a nonfinite metric, and on close. Replayed rows retain their step and run ID and receive timestamps when written. Use the newest segment's G8 file for ingestion because it includes the checkpoint's history. The ClickHouse loader reads the embedded run ID. The trainer also writes its native `metrics.jsonl`.

## Optimizer-step watchdog

Add `teams/07-infrastructure` to `PYTHONPATH`. `--watchdog-s SECONDS` overrides `WATCHDOG_S`; when neither is supplied the watchdog is off. Explicit `--watchdog-s 0` disables it for local smoke runs even if the environment supplies a value. Team 7's production guidance is the greater of 600 seconds and five times the p99 step duration.

The timer starts before the initial evaluation and resets at each optimizer step and after each completed update. It covers data loading, device synchronization, in-loop evaluation, and periodic checkpoint saves when integrated with #608. It is disarmed after the optimizer loop before final artifacts are written.

On timeout the trainer dumps all Python thread stacks, emits `train.watchdog` with the last completed step, writes the `hang_watchdog` exit note, and exits 75. Set `V5_EVENTS_DIR`, `V5_RUNS_DIR`, and `RUN_ID` for Team 7's job runner. `os._exit` drops metrics still in memory; #608 replays history retained in the last committed checkpoint. Two watchdog restarts in an hour page under H-14; three crashes in 30 minutes become a hold with exit 78 under Team 7's supervisor.

For Dry Run 2, use a job wrapper with G5's input arguments and checkpoint flags. Team 7's reference `mainrun.sbatch` supplies simulation-trainer flags such as `--remote-root` and `--step-sleep`; the G5 trainer does not accept that command unchanged.
