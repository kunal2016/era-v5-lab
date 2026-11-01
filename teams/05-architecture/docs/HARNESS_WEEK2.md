# Week-2 native harness

## Integration

Additive overlay for G5. Requires existing lead configs/arms and plan_v1.md reviewed against d15edd8 (PR180 plus arm-pinning follow-up). It does not replace those files or the accepted Week-1 harness. A changed plan requires review before refreshing configs/runtime.yaml's normalized plan SHA. G6 defaults are not inherited by this native adapter.

## Files

- train_week2.py: deterministic single-device training, JSONL metrics, checkpoints/resume and held-out evaluation.
- check_week2.py: canonical arm resolution, config validation and optional artifact preflight.
- week2/config.py: inheritance, provenance, dimensions and unsupported-choice guards.
- week2/artifacts.py: tokenizer identity, raw-table integrity and exact UTF-8 round-trip validation.
- week2/data.py: document windows, token/byte accounting and deterministic batches.
- week2/model.py: projected Kronecker tying, GQA/RoPE/SwiGLU and selected-expert dispatch.
- week2/evaluation.py: summed next-token NLL / ln(2) / original UTF-8 bytes.
- runtime.yaml: harness settings and plan-linked budgets; dimensions come from lead arm files.
- smoke_resolution.yaml: provisional development choices, never an approved experiment baseline.
- open_choices.json: unresolved interfaces and supported choices; checked by tests.
- tests/: focused model/gradient, config, artifact, data and BPB checks.

## Commands (repository root)

Use an existing working PyTorch installation; dependencies are listed in harness/requirements-week2.txt.

```bash
python -m unittest discover -s teams/05-architecture/tests -p 'test_week2*.py' -v
python teams/05-architecture/harness/check_week2.py teams/05-architecture/configs/arms/exp1/lr_1e-3.yaml --resolution teams/05-architecture/configs/small/smoke_resolution.yaml --tokenizer /path/tokenizer_v0.json --byte-table /path/raw_table.npz
python teams/05-architecture/harness/train_week2.py --config teams/05-architecture/configs/arms/exp1/lr_1e-3.yaml --tokenizer /path/tokenizer_v0.json --byte-table /path/raw_table.npz --train-data /path/train.jsonl --heldout-data /path/heldout.jsonl --device cpu --seed 1234 --smoke --smoke-steps 2 --smoke-seq-len 16 --smoke-batch-size 1 --out /path/fresh-run
```

Tokenizer/table/text paths are external inputs, not checked-in datasets. JSONL uses id/text; final holdout requires unique IDs. Large datasets are materialized in RAM: use a bounded real-text slice for integration checks.

## Heldout provenance input

The --heldout-report JSON must contain heldout_sha256 (exact input-file hash), fingerprint_set_id, scope: full, matches: 0 (integer), and docs_checked (matching parsed document count). Retain the original G9 checker evidence with the data owner; this sidecar records provenance, not a replacement contamination check.

## Current status and limits

52 unit tests passed in the source candidate; real-v0 artifact preflight passed for all three profiles, LR-arm resolution passed and the accepted Week-1 checker passed. The stripped overlay must be tested again in its target checkout. No fresh full-vocabulary tied training/repeatability or quality-result claim is made.

Reversibility and MTP are off. MTP weight is unset/inactive. Baseline LR 0.001 is timing-only. RoPE theta, expert bias, normalization and precise projected-KE tying agreement remain pending. Proposed tying changes parameter counts relative to the instructor labels; fixed dimensions must not be resized to match those labels.

The G6 loader's KE1 untied/learned-position implementation is not equivalent to this proposed native tied/RoPE path. G4-shipped table identity, official holdout/G9 evidence, approved training mixture and G8 writer integration remain pending. No Muon, alternate attention, DDP or expert-parallel execution is claimed. Unsupported choices fail explicitly. Quality mode requires agreements and holdout evidence; use --help for checkpoint and provenance options.

## Merge dependency

Merge after PR #188. The runtime plan fingerprint and explicit arm pins were reviewed against lead commit d15edd8. This PR does not edit arm files or plan_v1.md. Checks against older main intentionally fail the plan-identity guard. After #188 merges, rerun the tests and preflight on the actual combined branch. The current verification stages this overlay onto the lead snapshot, not onto older main.
