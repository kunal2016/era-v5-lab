# Week 2 Rotation Checks: Open Model Agreement with Published Scores

Each Week 2 rotation member in Team 09 (`09-evaluation`) runs one benchmark on one open model and compares our harness score against its published reference score.

## 1. Agreement Rule (Fixed Before Any Run)

- **Gate rule:** `PASS` if `|ours - published| <= 2.0` percentage points on the **full test set**, using the publisher's protocol (task definition, number of shots, metric, and aggregation).
- **No cherry-picking:** The rule and protocol are fixed before any run starts. A `FAIL` stands and is recorded with its observed difference and investigation notes.
- **Full test set:** Run the complete benchmark (`no --limit`, `no --log-samples`). Do not commit raw run outputs or per-item benchmark logs to git; post `results.json` and its `sha256` in `G9` chat.

## 2. How to Claim a Pair

1. Check the table below and `G9` chat first so no two rotation members run the same `(model, benchmark)` pair.
2. Post your claim in `G9` chat naming the model, pinned Hugging Face revision, benchmark task, shot count, metric, and published score with its source link.
3. Run via `teams/09-evaluation/harness_code_indic/run_lm_eval.py` (or the matching Team 09 harness) with weights fetched via `fetch_weights.py`.
4. Open a pull request adding your row to the results table below.

## 3. Results

| rotator | model @ revision | benchmark (task, shots, metric) | published (source link) | ours ± s.e. | Δ | verdict | harness commit | results.json sha256 | date |
|---|---|---|---|---|---|---|---|---|---|
| Sandeep Kunkunuru (`@sandeepkunkunuru`) | `Qwen/Qwen2.5-1.5B` @ `e5dfabbc` | BBH (`leaderboard_bbh`, 3-shot, `acc_norm`, $n=5761$) | `40.46 ± 0.60` ([Open LLM Leaderboard v2](https://huggingface.co/datasets/open-llm-leaderboard/results) / [`baselines.yaml`](../harness_code_indic/configs/baselines.yaml)) | `40.50 ± 0.60` | `+0.04` | `PASS` | `5a1c5f3` | `1efac93132366cbb3004b31742728669dcc99a127891dba43fafcf0b957a67b5` | `2026-11-02` |
