"""Verifier for G10 SWE environments: patch in, reward out.

An environment is a folder `swe-envs/<instance_id>/` with:
    env.json      fields named as in SWE-bench where they overlap (instance_id, repo, base_commit,
                  FAIL_TO_PASS, PASS_TO_PASS) plus our own (image, test_cmd, test_files, licence, provenance)
    Dockerfile    builds the repo at base_commit with no git history and pinned dependencies
    gold.patch    non-test part of the upstream PR
    test.patch    test part of the upstream PR (hidden: applied after the candidate patch)
    issue.md      the upstream issue text

Reward rule: 1 only if the candidate patch applies, touches no test file, and every FAIL_TO_PASS and
PASS_TO_PASS test passes. A missing test counts as a failure.

Gold check (TSAI Gate 2: "the test fails before the patch and passes after it"):
    before = base + test.patch:        every FAIL_TO_PASS test fails, every PASS_TO_PASS test passes
    after  = base + gold + test.patch:  every test in both lists passes
Each side is run `--runs` times and must give the same result every time.

Usage:
    python verify.py <env_dir> --patch candidate.patch      # prints {"reward": 0|1, ...}
    python verify.py <env_dir> --check [--runs 5]           # gold check of one env
    python verify.py --check-all [--runs 5] [--write ../results/swe_gold_check.md]
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results" / "swe_gold_check.md"

REPORT_START, REPORT_END = "@@G10_REPORT_START@@", "@@G10_REPORT_END@@"
APPLY_FAIL, TEST_PATCH_FAIL = "@@G10_APPLY_FAIL@@", "@@G10_TEST_PATCH_FAIL@@"


# --- patches ----------------------------------------------------------------------------------

def patch_paths(patch: str) -> list[str]:
    """Paths a unified diff touches (both sides of renames, without a/ b/ prefixes)."""
    paths = []
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            m = re.match(r"diff --git a/(.+?) b/(.+)$", line)
            if m:
                paths += [m.group(1), m.group(2)]
        elif line.startswith(("--- a/", "+++ b/")):
            paths.append(line[6:])
    return sorted(set(paths))


def is_test_path(path: str) -> bool:
    """Files the hidden tests own or that change how tests run. Candidates may not touch them."""
    p = path.lower()
    name = p.rsplit("/", 1)[-1]
    parts = p.split("/")[:-1]
    return (
        any(d in ("test", "tests", "testdata") for d in parts)
        or name.startswith("test_")
        or name.endswith(("_test.py", "_test.go", "_tests.py"))
        or name in ("conftest.py", "pytest.ini", "tox.ini", "noxfile.py")
    )


def split_patch(patch: str) -> tuple[str, str]:
    """Split a unified diff into (gold, test) parts by file."""
    gold, test = [], []
    for chunk in re.split(r"(?m)^(?=diff --git )", patch):
        if not chunk.strip():
            continue
        paths = patch_paths(chunk)
        (test if paths and all(is_test_path(p) for p in paths) else gold).append(chunk)
    return "".join(gold), "".join(test)


# --- test reports -----------------------------------------------------------------------------

def parse_junit(xml_text: str) -> dict[str, bool]:
    """pytest junit XML -> {"classname::name": passed}."""
    out: dict[str, bool] = {}
    root = ET.fromstring(xml_text)
    for case in root.iter("testcase"):
        test_id = f"{case.get('classname', '')}::{case.get('name', '')}"
        out[test_id] = not any(child.tag in ("failure", "error", "skipped") for child in case)
    return out


def parse_go_json(stream: str) -> dict[str, bool]:
    """`go test -json` events -> {"package::TestName": passed}."""
    out: dict[str, bool] = {}
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("Test") and event.get("Action") in ("pass", "fail", "skip"):
            out[f"{event['Package']}::{event['Test']}"] = event["Action"] == "pass"
    return out


# --- running one side in Docker -------------------------------------------------------------

def container_script(env: dict, with_candidate: bool) -> str:
    restore = " ".join(shlex.quote(f) for f in env["test_files"])
    report = "/tmp/g10_report.out"
    if env.get("language", "python") == "go":
        run = f"{env['test_cmd']} > {report} 2>/tmp/g10_test.log"
    else:
        run = f"{env['test_cmd']} --junitxml={report} > /tmp/g10_test.log 2>&1"
    lines = [
        "cd /repo",
        f"if ! git apply --whitespace=nowarn /patches/candidate.patch; then echo {APPLY_FAIL}; exit 0; fi"
        if with_candidate else ":",
        # Hidden tests win: put every test file back to the base version (or remove it if new) ...
        f"for f in {restore}; do if git cat-file -e HEAD:\"$f\" 2>/dev/null; then git checkout -q HEAD -- \"$f\"; "
        "else rm -f \"$f\"; fi; done",
        # ... then apply the upstream test change.
        f"if ! git apply --whitespace=nowarn /patches/test.patch; then echo {TEST_PATCH_FAIL}; exit 0; fi",
        f"timeout {int(env.get('timeout_s', 300))} {run}; echo \"@@G10_EXIT $?@@\"",
        f"echo {REPORT_START}; cat {report} 2>/dev/null; echo {REPORT_END}",
        "tail -c 2000 /tmp/g10_test.log 2>/dev/null",
    ]
    return "\n".join(lines)


def run_side(env_dir: Path, env: dict, candidate: str | None) -> dict:
    """Run the hidden tests once on base (+ candidate). Returns {"results": {...}} or {"error": ...}."""
    with tempfile.TemporaryDirectory(prefix="g10swe-") as tmp:
        pdir = Path(tmp)
        (pdir / "test.patch").write_bytes((env_dir / "test.patch").read_bytes())
        if candidate is not None:
            (pdir / "candidate.patch").write_bytes(candidate.encode("utf-8"))  # bytes: no CRLF change
        name = f"g10swe-{uuid.uuid4().hex[:12]}"
        cmd = ["docker", "run", "--rm", "--name", name, "--network=none", "--memory=2g", "--cpus=2",
               "-v", f"{pdir}:/patches:ro", env["image"], "bash", "-c",
               container_script(env, candidate is not None)]
        start = time.monotonic()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=int(env.get("timeout_s", 300)) + 60)
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", name], capture_output=True)
            return {"error": "timeout"}
        seconds = time.monotonic() - start
    out = proc.stdout
    if APPLY_FAIL in out:
        return {"error": "candidate patch does not apply"}
    if TEST_PATCH_FAIL in out:
        return {"error": "test.patch does not apply"}
    if REPORT_START not in out:
        return {"error": "no report: " + (out + proc.stderr)[-500:]}
    report = out.split(REPORT_START, 1)[1].split(REPORT_END, 1)[0].strip()
    try:
        results = parse_go_json(report) if env.get("language") == "go" else parse_junit(report)
    except ET.ParseError:
        return {"error": "unreadable test report: " + out[-500:]}
    return {"results": results, "seconds": round(seconds, 1)}


def load_env(env_dir: Path) -> dict:
    return json.loads((env_dir / "env.json").read_text(encoding="utf-8"))


def ensure_image(env_dir: Path, env: dict) -> str:
    """Build the env image if it is not present. Returns the image id."""
    have = subprocess.run(["docker", "image", "inspect", "-f", "{{.Id}}", env["image"]], capture_output=True, text=True)
    if have.returncode != 0:
        subprocess.run(["docker", "build", "-q", "-t", env["image"], str(env_dir)], check=True,
                       capture_output=True, text=True)
        have = subprocess.run(["docker", "image", "inspect", "-f", "{{.Id}}", env["image"]],
                              capture_output=True, text=True, check=True)
    return have.stdout.strip()


# --- reward and gold check ------------------------------------------------------------------

def reward(env_dir: Path, candidate: str) -> dict:
    env = load_env(env_dir)
    touched = [p for p in patch_paths(candidate) if is_test_path(p) or p in env["test_files"]]
    if touched:
        return {"instance_id": env["instance_id"], "reward": 0, "reason": f"patch edits test files: {touched}"}
    ensure_image(env_dir, env)
    side = run_side(env_dir, env, candidate)
    if "error" in side:
        return {"instance_id": env["instance_id"], "reward": 0, "reason": side["error"]}
    wanted = env["FAIL_TO_PASS"] + env["PASS_TO_PASS"]
    failed = [t for t in wanted if not side["results"].get(t, False)]
    return {"instance_id": env["instance_id"], "reward": int(not failed), "failed": failed[:20],
            "n_failed": len(failed), "seconds": side["seconds"]}


def gold_check(env_dir: Path, runs: int = 5) -> dict:
    env = load_env(env_dir)
    image_id = ensure_image(env_dir, env)
    gold = (env_dir / "gold.patch").read_text(encoding="utf-8")
    f2p, p2p = env["FAIL_TO_PASS"], env["PASS_TO_PASS"]
    row = {"instance_id": env["instance_id"], "repo": env["repo"], "f2p": len(f2p), "p2p": len(p2p),
           "image_id": image_id[:19], "runs": runs, "problems": []}
    before_ok = after_ok = 0
    seconds = []
    for _ in range(runs):
        b = run_side(env_dir, env, None)
        if "error" in b:
            row["problems"].append("before: " + b["error"])
        else:
            bad = [t for t in f2p if b["results"].get(t, False)] + [t for t in p2p if not b["results"].get(t, False)]
            before_ok += not bad
            if bad:
                row["problems"].append(f"before: {len(bad)} wrong, e.g. {bad[0]}")
        a = run_side(env_dir, env, gold)
        if "error" in a:
            row["problems"].append("after: " + a["error"])
        else:
            bad = [t for t in f2p + p2p if not a["results"].get(t, False)]
            after_ok += not bad
            seconds.append(a["seconds"])
            if bad:
                row["problems"].append(f"after: {len(bad)} failing, e.g. {bad[0]}")
    row.update(fails_before=f"{before_ok}/{runs}", passes_after=f"{after_ok}/{runs}",
               seconds=round(max(seconds), 1) if seconds else None,
               ok=before_ok == runs and after_ok == runs and len(f2p) > 0)
    row["problems"] = sorted(set(row["problems"]))
    return row


def env_dirs() -> list[Path]:
    return sorted(p.parent for p in HERE.glob("*/env.json"))


def write_table(rows: list[dict], path: Path) -> None:
    arch = subprocess.run(["docker", "info", "-f", "{{.Architecture}}"], capture_output=True, text=True).stdout.strip()
    ok = sum(r["ok"] for r in rows)
    lines = [
        "# SWE environments: gold check",
        "",
        f"Generated by `swe-envs/verify.py --check-all --runs {rows[0]['runs'] if rows else 0}` on "
        f"{time.strftime('%Y-%m-%d %H:%M %Z')}, Docker arch `{arch}`.",
        "",
        "Gold check: with the test patch applied, every FAIL_TO_PASS test fails on the base commit, and every "
        "FAIL_TO_PASS and PASS_TO_PASS test passes after the gold patch. Each side runs N times and must agree "
        "every time. Tests run with `--network=none`.",
        "",
        f"**{ok} of {len(rows)} environments pass.**",
        "",
        "| # | instance_id | repo | FAIL_TO_PASS | PASS_TO_PASS | fails before | passes after | max run (s) | image | result |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        result = "pass" if r["ok"] else "FAIL: " + "; ".join(r["problems"])[:200]
        lines.append(f"| {i} | `{r['instance_id']}` | {r['repo']} | {r['f2p']} | {r['p2p']} | {r['fails_before']} | "
                     f"{r['passes_after']} | {r['seconds']} | `{r['image_id']}` | {result} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("env_dir", nargs="?", type=Path)
    ap.add_argument("--patch", type=Path, help="candidate patch file; prints the reward")
    ap.add_argument("--check", action="store_true", help="gold check of env_dir")
    ap.add_argument("--check-all", action="store_true", help="gold check of every env in swe-envs/")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--write", type=Path, help="write the markdown table here (with --check-all)")
    args = ap.parse_args(argv)
    if args.check_all:
        rows = [gold_check(d, args.runs) for d in env_dirs()]
        for r in rows:
            print(json.dumps(r))
        if args.write:
            write_table(rows, args.write)
        return 0 if rows and all(r["ok"] for r in rows) else 1
    if args.env_dir is None:
        ap.error("give an env_dir, or use --check-all")
    if args.check:
        row = gold_check(args.env_dir, args.runs)
        print(json.dumps(row, indent=1))
        return 0 if row["ok"] else 1
    if args.patch:
        print(json.dumps(reward(args.env_dir, args.patch.read_text(encoding="utf-8"))))
        return 0
    ap.error("give --patch, --check or --check-all")
    return 2


if __name__ == "__main__":
    sys.exit(main())
