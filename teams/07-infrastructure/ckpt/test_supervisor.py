"""Tests for ckpt/supervisor.py. No torch, no GPU: the "trainer" is a tiny Python child whose exit codes come
from a script file, one line per attempt.

    python -m pytest teams/07-infrastructure/ckpt/test_supervisor.py -q
"""
import json
import os
import signal
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ckpt.store import open_store  # noqa: E402
from ckpt.supervisor import EXIT_FATAL, Supervisor, last_complete, main, meaning  # noqa: E402

# The child reads its attempt number and exits with line <attempt> of the plan file.
# "kill" = wait to be killed (the test sends SIGKILL), "sleep" = sleep until a signal arrives.
CHILD = r"""
import os, signal, sys, time
plan = open(sys.argv[1]).read().split()
step = plan[int(os.environ["V5_RESTART_COUNT"])]
open(sys.argv[2], "a").write(os.environ["V5_RESTART_COUNT"] + "\n")
if step in ("kill", "sleep"):
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(75))
    time.sleep(60)
    sys.exit(1)
sys.exit(int(step))
"""


@pytest.fixture
def child(tmp_path):
    script = tmp_path / "child.py"
    script.write_text(CHILD)

    def make(*plan):
        (tmp_path / "plan").write_text(" ".join(str(p) for p in plan))
        return [sys.executable, str(script), str(tmp_path / "plan"), str(tmp_path / "attempts")]
    return make


def attempts(tmp_path) -> list:
    p = tmp_path / "attempts"
    return [int(x) for x in p.read_text().split()] if p.exists() else []


def sup(cmd, tmp_path, **kw):
    kw.setdefault("backoff_s", 0)
    kw.setdefault("log_path", str(tmp_path / "supervisor.jsonl"))
    return Supervisor(cmd, **kw)


def log_rows(tmp_path) -> list:
    return [json.loads(line) for line in (tmp_path / "supervisor.jsonl").read_text().splitlines()]


def commit(root, run_id, step, manifest=True):
    """A committed checkpoint as ckpt.py leaves it: step folder, MANIFEST.json, then latest.json."""
    st = open_store(os.path.join(str(root), run_id))
    path = f"main/step_{step}-e1"
    if manifest:
        st.put_json(f"{path}/{'MANIFEST.json'}", {"step": step, "files": {}})
    st.put_json("latest.json", {"step": step, "branch": "main", "path": path, "epoch": 1})
    return os.path.join(str(root), run_id)


def test_done_first_time(child, tmp_path):
    assert sup(child(0), tmp_path).run() == 0
    assert attempts(tmp_path) == [0]
    rows = log_rows(tmp_path)
    assert [r["action"] for r in rows] == ["stop"] and rows[0]["exit"] == 0


def test_saved_and_stopped_restarts_until_done(child, tmp_path):
    assert sup(child(75, 75, 0), tmp_path).run() == 0
    assert attempts(tmp_path) == [0, 1, 2]
    assert [r["meaning"] for r in log_rows(tmp_path)] == ["saved_and_stopped", "saved_and_stopped", "done"]


def test_fatal_is_never_restarted(child, tmp_path):
    assert sup(child(78, 0), tmp_path).run() == EXIT_FATAL
    assert attempts(tmp_path) == [0]


def test_one_crash_is_retried(child, tmp_path):
    assert sup(child(1, 0), tmp_path).run() == 0
    rows = log_rows(tmp_path)
    assert rows[0]["meaning"] == "crash: exit 1" and rows[0]["action"] == "restart"


def test_crash_loop_holds(child, tmp_path):
    # 3 crashes inside the window: the third is not retried
    assert sup(child(1, 1, 1, 0), tmp_path, crash_n=3, crash_window_s=60).run() == EXIT_FATAL
    assert attempts(tmp_path) == [0, 1, 2]
    assert "crash loop" in log_rows(tmp_path)[-1]["reason"]


def test_crashes_outside_the_window_do_not_count(child, tmp_path):
    # window 0 s: every crash is alone in its window, so only the restart limit stops it
    assert sup(child(1, 1, 1, 0), tmp_path, crash_n=2, crash_window_s=0).run() == 0


def test_restart_limit(child, tmp_path):
    assert sup(child(75, 75, 75, 0), tmp_path, max_restarts=2).run() == EXIT_FATAL
    assert attempts(tmp_path) == [0, 1, 2]
    assert log_rows(tmp_path)[-1]["reason"] == "restart limit reached (2)"


def test_sigkill_is_a_crash_and_restarts(child, tmp_path):
    def kill_first(proc, attempt):
        if attempt == 0:
            time.sleep(0.3)
            proc.kill()
    assert sup(child("kill", 0), tmp_path, on_start=kill_first).run() == 0
    rows = log_rows(tmp_path)
    assert rows[0]["rc"] == -signal.SIGKILL and rows[0]["meaning"] == "crash: killed by SIGKILL"
    assert rows[0]["action"] == "restart" and attempts(tmp_path) == [0, 1]


def test_restart_reports_last_complete_checkpoint(child, tmp_path):
    run_url = commit(tmp_path / "store", "r1", 125)
    assert sup(child(75, 0), tmp_path, run_url=run_url).run() == 0
    row = log_rows(tmp_path)[0]
    assert row["from_step"] == 125 and row["checkpoint"]["path"] == "main/step_125-e1"


def test_last_complete_needs_the_manifest(tmp_path):
    assert last_complete(str(tmp_path / "none")) is None                  # nothing saved: fresh start
    run_url = commit(tmp_path / "store", "r2", 50, manifest=False)
    assert last_complete(run_url) is None                                  # pointer without MANIFEST
    run_url = commit(tmp_path / "store", "r3", 50)
    assert last_complete(run_url)["step"] == 50


def test_sigterm_is_forwarded_and_stops_restarts(child, tmp_path):
    s = sup(child("sleep", 0), tmp_path)

    def term_supervisor(proc, attempt):
        time.sleep(0.3)
        s._forward(signal.SIGTERM, None)     # what the signal handler does
    s.on_start = term_supervisor
    assert s.run() == 75                     # the child saved (75); the supervisor does not restart
    assert attempts(tmp_path) == [0]
    assert log_rows(tmp_path)[0]["reason"] == "supervisor was told to stop"


def test_meaning():
    assert meaning(0) == "done" and meaning(75) == "saved_and_stopped" and meaning(78) == "fatal"
    assert meaning(-9) == "crash: killed by SIGKILL" and meaning(137) == "crash: exit 137"


def test_cli(child, tmp_path, monkeypatch):
    monkeypatch.delenv("V5_REMOTE_ROOT", raising=False)
    log = str(tmp_path / "supervisor.jsonl")
    assert main(["--backoff", "0", "--log", log, "--", *child(75, 0)]) == 0
    assert len(log_rows(tmp_path)) == 2
    assert main(["--max-restarts", "1"]) == 2                              # no "--"
