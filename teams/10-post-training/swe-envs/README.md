# SWE environments (G10 week 2, tasks D/E/F)

Each folder `swe-envs/<instance_id>/` is one SWE environment built from **one merged upstream GitHub PR**:
a fixed commit, a failing test and a gold patch, in Docker. `results/swe_gold_check.md` shows that each one
passes the gold check: the test fails before the patch and passes after it.

## What is in an environment

| File | What | Where it comes from |
|---|---|---|
| `env.json` | `instance_id`, `repo`, `base_commit`, `FAIL_TO_PASS`, `PASS_TO_PASS` (same names as SWE-bench), plus `licence`, `pr_url`, `issue_urls`, `merged_at`, `provenance`, `base_image`, `image`, `test_files`, `test_cmd`, `timeout_s` | `make_env.py` |
| `issue.md` | the problem statement | the linked GitHub issue, text unchanged, with its URL |
| `gold.patch` | the fix | the non-test files of the upstream PR |
| `test.patch` | the hidden tests | the test files of the upstream PR |
| `Dockerfile` | repo at `base_commit`, **no git history**, base image pinned by digest, runs as a non-root user | `make_env.py` |
| `requirements.lock` | exact dependency versions, resolved as of the PR merge date | `make_env.py` (`uv pip install --exclude-newer <merge date>`) |

## Rules every environment follows

- **Human content only (TSAI 3 Nov rule).** The issue, fix and tests are all upstream, written by people. We use PRs merged **before 2023** that close a human-filed issue. `make_env.py` refuses a PR whose body, commits or issue mention an AI coding tool. No model writes any environment content; the scripts here only cut the PR apart, pin the environment and measure the tests.
- **Permissive repos only** (MIT, BSD, Apache-2.0 ...), recorded in `env.json.licence`.
- **Not a benchmark repo.** No repo from SWE-bench (incl. Lite and Verified), SWE-bench Multimodal, SWE-bench Live or SWE-bench Pro (`benchmark_repos.txt`).
- **No leaks.** The image has the repo at the base commit only, with a fresh one-commit git history, so the fix cannot be read from `.git`. Tests run with `--network=none`.
- **Hidden tests win.** `verify.py` refuses a candidate patch that touches a test file (`tests/`, `test_*.py`, `conftest.py`, `tox.ini` ...). It then restores the test files and applies `test.patch` after the candidate.

## Commands

```bash
# reward for a candidate patch (RL): prints {"reward": 0|1, ...}
python swe-envs/verify.py swe-envs/<instance_id> --patch candidate.patch

# gold check: one env, or all of them (writes the results table)
python swe-envs/verify.py swe-envs/<instance_id> --check --runs 5
python swe-envs/verify.py --check-all --runs 5 --write results/swe_gold_check.md

# build a new env from an upstream PR (needs `gh` logged in, Docker, network)
python swe-envs/make_env.py --repo pallets/click --pr 1934

# list more candidates from an open pool (default nebius/SWE-rebench) with the same filters
python swe-envs/import_pool.py --out pool_manifest.json

# harness tests (offline, no Docker)
python -m pytest swe-envs/test_verify.py -q
```

## How FAIL_TO_PASS and PASS_TO_PASS are chosen

`make_env.py` runs the test files from `test.patch` twice on the base commit and twice after the gold patch:

- **FAIL_TO_PASS:** passes after every time, and fails (or does not exist) before every time.
- **PASS_TO_PASS:** passes on both sides every time.
- **Dropped and recorded in `build_notes`:** any test that changes between runs.

`verify.py --check` then runs both sides 5 times. Every run must agree, or the env fails.

## Dependencies

- Runtime and test dependencies are resolved as of the merge date and frozen in `requirements.lock`.
- Build tools (setuptools, wheel) may be newer, up to 2025-06-01, because setuptools before 64 cannot do editable installs.
- The Python version follows the merge year: 3.8 up to 2020, 3.9 in 2021, 3.10 in 2022.
- Base images are multi-arch (`python:3.x-slim`) and pinned by manifest digest, so the same Dockerfile builds on arm64 and amd64.

## Using these in an RL loop

The shared fields use SWE-bench names, so SWE-bench-style loaders can read `env.json` with little glue. The env format for a specific RL framework (verifiers, OpenEnv, Harbor, slime) is a week 3-4 task, once the team picks the framework.
