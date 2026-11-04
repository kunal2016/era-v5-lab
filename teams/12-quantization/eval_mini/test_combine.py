#!/usr/bin/env python3
"""combine.py must refuse a run whose sample rows carry eval item text (Team 9 eval firewall).

    python test_combine.py            # exits non-zero if a check fails
    python -m pytest test_combine.py

Copies the committed bf16 and Q8_0/Q6_K runs to a temp folder, combines them (must work), puts a `target` field into
one Q8_0 row and combines again (must stop, naming the problem). The text added is a placeholder, not an eval item.
"""
from __future__ import annotations

import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "results" / "raw"


def combine(tmp: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HERE / "combine.py"), str(tmp / "runs_bf16"), str(tmp / "runs_Q8_0-Q6_K"),
                           "--out", str(tmp / "out")], capture_output=True, text=True)


def test_refuses_item_text():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for name in ("runs_bf16", "runs_Q8_0-Q6_K"):
            shutil.copytree(RAW / name, tmp / name)
        ok = combine(tmp)
        assert ok.returncode == 0, ok.stderr[-1500:]

        victim = next((tmp / "runs_Q8_0-Q6_K" / "Q8_0").glob("*.samples.jsonl"))
        lines = victim.read_text().splitlines()
        row = json.loads(lines[0]); row["target"] = "placeholder"
        victim.write_text("\n".join([json.dumps(row)] + lines[1:]) + "\n")
        shutil.rmtree(tmp / "out")
        bad = combine(tmp)
        assert bad.returncode != 0, "combine.py accepted a row with a target field"
        assert "eval item text" in bad.stderr and victim.name in bad.stderr, bad.stderr[-1500:]


if __name__ == "__main__":
    test_refuses_item_text()
    print("PASS: combine.py combines the committed runs and refuses a row with item text")
