"""Restart test: a trainer killed with SIGKILL is restarted by the supervisor and gives the same losses.

In simple words:
- Run A trains Team 05's tiny MoE from step 0 to step 200 without a stop. It saves a checkpoint every 25 steps.
- Run B is the same command under ckpt/supervisor.py. Once run B is past step 140 (and has a COMPLETE
  checkpoint), we kill it with SIGKILL: no warning, no chance to save, like a lost node or the OOM killer.
  The supervisor sees a crash and starts the same command again; the trainer restores the newest COMPLETE
  checkpoint (latest.json, MANIFEST written) and trains on to step 200.
- For every step 1..200 the training losses (next-token and t+2) of run B must be bit-equal to run A, and
  the batch data ID (global batch position + sha256 of the batch tokens) must be the same. For the steps run
  B did twice (between the checkpoint and the kill), the value after the restart is compared.
- The supervisor log must show exactly one restart (exit -9, SIGKILL) and then a normal finish, and the
  restart must start at the step after the checkpoint it named.

Exit 0 and one PASS line when all of that holds; exit 1 at the first difference; exit 78 if a run crashed.
Writes only --out (default out/ next to this script, git-ignored), and --report if given.

    python restart_test.py                                   # CPU, 1 process
    python restart_test.py --report ../../results/restart_cpu.txt
"""
import argparse
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEAM = HERE.parents[1]                                   # teams/07-infrastructure
sys.path[:0] = [str(TEAM), str(TEAM / "jobs" / "restore_test")]
# Team 05's model, config, loss and data stream exactly as the restore test uses them (imported, never copied)
import restore_test as rt  # noqa: E402
from ckpt.supervisor import Supervisor, last_complete  # noqa: E402

FIELDS = rt.FIELDS
EXIT_FATAL = 78


# ------------------------------------------------------------------ the trainer (one process, any attempt)
def trainer(a) -> int:
    import torch
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    os.environ.setdefault("RUN_ID", a.run_id)
    cfg = rt.load_cfg(a.config, a.tiny, a.steps)
    seed = int(cfg["run.seed"])
    torch.manual_seed(seed)
    model = rt.TinyMoE(cfg)
    optim = torch.optim.AdamW(model.parameters(), lr=float(cfg["optim.lr"]))
    loader = rt.StreamLoader(cfg, seed, 0, 1)
    clip = float(cfg["run.grad_clip"])
    probe_batch = rt.stream_for(cfg, seed + 1)[:int(cfg["tiny.batch"])]

    def probe(m) -> float:
        m.eval()
        with torch.no_grad():
            ntp, _ = rt.losses(m, probe_batch)
        m.train()
        return ntp.item()

    ck = rt.Checkpointer(a.run_id, str(a.out / "ckpt_local"), str(a.out / "ckpt_store"),
                         config_path=str(a.tiny), seed=seed)
    info = ck.restore(model, optim, loader, probe)          # newest COMPLETE checkpoint, or None: step 0
    step = info["step"] if info else 0
    attempt = int(os.environ.get("V5_RESTART_COUNT", "0"))
    with open(a.out / "rows.jsonl", "a") as f:
        while step < a.steps:
            batch_id = loader.next_batch_id()
            tokens = loader.next()
            optim.zero_grad(set_to_none=True)
            ntp, mtp = rt.losses(model, tokens)
            (ntp + mtp).backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
            optim.step()
            step += 1
            n, m = float(ntp.detach()), float(mtp.detach())
            f.write(json.dumps({"attempt": attempt, "step": step, "loss_ntp": n, "loss_mtp": m,
                                "loss_ntp_bits": rt.float_bits(n), "loss_mtp_bits": rt.float_bits(m),
                                "batch_id": batch_id}) + "\n")
            f.flush()
            if step % a.save_every == 0 or step == a.steps:
                if not ck.save(step, model, optim, loader, probe, reason="restart_test"):
                    return EXIT_FATAL
    return 0 if ck.wait() else EXIT_FATAL


# ------------------------------------------------------------------ the test
def trainer_cmd(a, run_id: str, out: Path) -> list:
    return [sys.executable, str(Path(__file__).resolve()), "--trainer", "--run-id", run_id, "--out", str(out),
            "--steps", str(a.steps), "--save-every", str(a.save_every),
            "--config", str(a.config), "--tiny", str(a.tiny)]


def read_rows(path: Path) -> list:
    """Every complete row. A SIGKILL can land in the middle of a write, so a last line that does not parse is
    skipped: that step counts as not finished (the restarted trainer does it again)."""
    rows = []
    lines = [x for x in path.read_text().splitlines() if x.strip()] if path.exists() else []
    for i, line in enumerate(lines):
        try:
            rows.append(json.loads(line))
        except ValueError:
            if i != len(lines) - 1:
                raise                      # only the line being written at the kill may be cut
    return rows


def last_step(path: Path) -> int:
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 4096))
            lines = [x for x in f.read().decode().splitlines() if x.strip()]
        return json.loads(lines[-1])["step"] if lines else 0
    except (OSError, ValueError, IndexError):
        return 0


def check(a, run_a: list, run_b: list, sup_rows: list, kill: dict) -> dict:
    """None if every check passes, else the first problem."""
    by_a = {r["step"]: r for r in run_a}
    final_b = {}
    for r in run_b:                    # later attempts overwrite: the value after the restart counts
        final_b[r["step"]] = r
    for step in range(1, a.steps + 1):
        if step not in by_a or step not in final_b:
            return {"step": step, "field": "missing", "a": step in by_a, "b": step in final_b}
        for k in FIELDS:
            if by_a[step][k] != final_b[step][k]:
                return {"step": step, "field": k, "a": by_a[step][k], "b": final_b[step][k]}
    restarts = [r for r in sup_rows if r["action"] == "restart"]
    if len(restarts) != 1 or restarts[0]["rc"] != -signal.SIGKILL or sup_rows[-1].get("exit") != 0:
        return {"field": "supervisor log", "want": "one restart after SIGKILL (-9), then exit 0", "got": sup_rows}
    from_step = restarts[0]["pointer_step"]
    second = [r["step"] for r in run_b if r["attempt"] == 1]
    # the trainer must have restored exactly the checkpoint latest.json pointed to (no silent fallback)
    if not (0 < from_step <= kill["step"] and from_step % a.save_every == 0 and second and second[0] == from_step + 1):
        return {"field": "restart step", "pointer_step": from_step, "killed_at": kill["step"],
                "first_step_after_restart": second[0] if second else None}
    return None


def run_test(a) -> int:
    import torch
    out = a.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    os.environ["V5_EVENTS_DIR"] = str(out / "events")
    os.environ.setdefault("OMP_NUM_THREADS", "1")

    t0 = time.time()
    a_out = out / "run_a"
    a_out.mkdir()
    rc_a = subprocess.call(trainer_cmd(a, "restart-a", a_out), env=dict(os.environ, RUN_ID="restart-a"))
    t_a = time.time() - t0
    if rc_a != 0:
        print(f"FAIL restart_test: run A crashed (exit {rc_a})", file=sys.stderr)
        return EXIT_FATAL

    b_out = out / "run_b"
    b_out.mkdir()
    run_url = str(b_out / "ckpt_store" / "restart-b")
    kill = {}

    def killer(proc, attempt):
        if attempt != 0:
            return

        def watch():
            while proc.poll() is None:
                s = last_step(b_out / "rows.jsonl")
                ck = last_complete(run_url) if s >= a.kill_at else None
                if ck and ck.get("step"):
                    proc.send_signal(signal.SIGKILL)
                    kill.update(step=s, last_complete_seen=ck["step"], time=time.time())
                    return
                time.sleep(0.005)
        threading.Thread(target=watch, daemon=True).start()

    os.environ["RUN_ID"] = "restart-b"
    t1 = time.time()
    rc_b = Supervisor(trainer_cmd(a, "restart-b", b_out), run_url=run_url, log_path=str(out / "supervisor.jsonl"),
                      max_restarts=3, backoff_s=0, on_start=killer).run()
    t_b = time.time() - t1
    sup_rows = read_rows(out / "supervisor.jsonl")
    if rc_b != 0 or not kill:
        print(f"FAIL restart_test: run B exit {rc_b}, killed: {bool(kill)}", file=sys.stderr)
        return EXIT_FATAL

    run_a, run_b = read_rows(a_out / "rows.jsonl"), read_rows(b_out / "rows.jsonl")
    kill["step"] = max(r["step"] for r in run_b if r["attempt"] == 0)   # last step the killed child finished
    diff = check(a, run_a, run_b, sup_rows, kill)
    restart = next(r for r in sup_rows if r["action"] == "restart")
    after = [r["step"] for r in run_b if r["attempt"] == 1]
    restored = after[0] - 1 if after else None          # what the trainer really loaded (its first step - 1)
    result = {"pass": diff is None, "first_diff": diff, "device": "cpu", "nproc": 1, "steps": a.steps,
              "save_every": a.save_every, "kill_at": a.kill_at, "killed_after_step": kill["step"],
              "restarted_from_step": restored, "pointer_step": restart["pointer_step"],
              "redone_steps": kill["step"] - restored if restored is not None else None,
              "fields": FIELDS, "torch": torch.__version__, "seconds": {"run_a": round(t_a, 1), "run_b": round(t_b, 1)},
              "supervisor": sup_rows}
    (out / "result.json").write_text(json.dumps(result, indent=1) + "\n")
    where = (f"cpu: SIGKILL after step {kill['step']}, restarted from COMPLETE checkpoint step "
             f"{restored}, steps 1-{a.steps}")
    line = (f"PASS restart_test {where}: loss_ntp and loss_mtp bit-equal, data ids equal" if diff is None
            else f"FAIL restart_test {where}: {json.dumps(diff)[:600]}")
    print(line)
    if a.report:
        write_report(a, result, line)
    return 0 if diff is None else 1


def write_report(a, r: dict, line: str) -> None:
    import numpy
    import torch
    rel = Path(os.path.relpath(Path(__file__).resolve(), TEAM.parents[1]))
    other = ""
    if getattr(a, "other_kills", None):
        other = "\nOther kill points (same command with --kill-at N):\n" + "\n".join(f"  {x}" for x in a.other_kills) + "\n"
    sup = "\n".join(f"  attempt {s['attempt']}: exit {s['rc']} ({s['meaning']}) -> {s['action']}"
                    + (f" (latest.json at step {s['pointer_step']})" if s["action"] == "restart" else f", supervisor exit {s['exit']}")
                    for s in r["supervisor"])
    text = f"""Restart test on CPU, Team 05 tiny MoE, ckpt/supervisor.py
Date: {time.strftime('%d %b %Y')}

Command (from the repo root; CUDA_VISIBLE_DEVICES="" hides any GPU so it runs on CPU only; output goes to
teams/07-infrastructure/jobs/restart_test/out/, git-ignored):

  CUDA_VISIBLE_DEVICES="" python {rel} --also-kill-at 31,99,164 --report teams/07-infrastructure/results/restart_cpu.txt

Environment:
  Python   {platform.python_version()}
  torch    {torch.__version__} (CPU only)
  numpy    {numpy.__version__}
  OS       {platform.platform()}
  Team 05 config: teams/05-architecture/configs/config_v0.yaml + teams/05-architecture/configs/small/tiny_moe.yaml
  seed {rt.load_cfg(a.config, a.tiny, a.steps)['run.seed']} (run.seed in config_v0.yaml)

What it does:
  Run A: steps 1-{a.steps}, no stop, checkpoint every {a.save_every} steps.
  Run B: the same command under ckpt/supervisor.py. Killed with SIGKILL once past step {a.kill_at} and a COMPLETE
         checkpoint exists. The supervisor restarts the same command; the trainer restores latest.json.
  Compared: loss_ntp and loss_mtp bits and the batch data ID for every step 1-{a.steps} (for steps run B did
            twice, the value after the restart).

Bit equality is between run A and run B on the same machine; the numbers are not expected to match other
OSes (the restore test results are from Ubuntu and Windows).

Result: {'PASS' if r['pass'] else 'FAIL'}

  killed after step          {r['killed_after_step']}
  restarted from step        {r['restarted_from_step']} (first step of the restarted trainer, minus 1)
  latest.json at the restart {r['pointer_step']} (the last COMPLETE checkpoint: MANIFEST.json written, latest.json moved)
  steps done twice           {r['redone_steps']} (step {r['restarted_from_step'] + 1} to {r['killed_after_step']})
  compared steps             1-{a.steps}, fields {', '.join(FIELDS)}
  wall time                  run A {r['seconds']['run_a']} s, run B {r['seconds']['run_b']} s

Supervisor log (out/supervisor.jsonl):
{sup}

Last line:
  {line}
{other}"""
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--save-every", type=int, default=25, help="checkpoint every N steps")
    ap.add_argument("--kill-at", type=int, default=140, help="SIGKILL run B once it is past this step")
    ap.add_argument("--out", type=Path, default=HERE / "out")
    ap.add_argument("--report", default=None, help="also write a plain-text result file here")
    ap.add_argument("--also-kill-at", default="", help="comma list: also run with these kill points and add "
                    "their result lines to --report (e.g. 31,99,164)")
    ap.add_argument("--config", type=Path, default=rt.CONFIGS / "config_v0.yaml")
    ap.add_argument("--tiny", type=Path, default=rt.CONFIGS / "small" / "tiny_moe.yaml")
    ap.add_argument("--trainer", action="store_true", help=argparse.SUPPRESS)   # one attempt of the trainer
    ap.add_argument("--run-id", default="restart", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.trainer:
        return trainer(a)
    if not (0 < a.save_every <= a.kill_at < a.steps):
        ap.error("need 0 < --save-every <= --kill-at < --steps")
    import torch
    # torch.__version__ is a TorchVersion: it compares as a version ("2.9.0" < "2.14.1"; "2.15.0a0+git" passes),
    # the same check as restore_test.py
    if torch.__version__ < rt.MIN_TORCH:
        ap.error(f"needs torch >= {rt.MIN_TORCH} (the restore test's pin), found {torch.__version__}")
    a.out, a.config, a.tiny = a.out.resolve(), a.config.resolve(), a.tiny.resolve()
    a.other_kills = []
    for k in [int(x) for x in a.also_kill_at.split(",") if x.strip()]:
        b = argparse.Namespace(**vars(a))
        b.kill_at, b.report, b.out = k, None, a.out.parent / f"{a.out.name}_kill{k}"
        if not (0 < b.save_every <= k < b.steps):
            ap.error(f"--also-kill-at {k}: need --save-every <= N < --steps")
        rc, lines = run_captured(b)
        a.other_kills.append(lines[-1] if lines else f"--kill-at {k}: no result line (exit {rc})")
        if rc != 0:
            print(a.other_kills[-1], file=sys.stderr)
            return rc
    return run_test(a)


def run_captured(a) -> tuple:
    """run_test() for one extra kill point; returns (exit code, PASS/FAIL lines it printed)."""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run_test(a)
    return rc, [x for x in buf.getvalue().splitlines() if x.startswith(("PASS", "FAIL"))]


if __name__ == "__main__":
    sys.exit(main())
