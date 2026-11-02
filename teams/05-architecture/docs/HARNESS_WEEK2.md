# Week-2 harness: TSAI review revision

## Contract

Input: arm setting `embedding: ke1`, implemented by the native G4 raw-byte-code projection. This is an explicit adapter mapping, not a change to the arm. The physical raw table must match tokenizer v0 and G4 format v2. G4-shipped artifact verification is still required; passing a locally rebuilt table does not imply G4 approval.

Output: dense untied `nn.Linear(d_model, vocab_size, bias=False)` only, per TSAI's 1 Nov decision. No KE-tied output code, output-head switch or EXP-5 remains. Input projection and output parameters are independent.

`embedding`, `attn_impl`, `mtp`, `reversible`, `ce_impl` and `moe.dispatch` must come explicitly from the arm chain. The native harness does not load mutable G6 defaults. Unknown/unsupported settings fail. Muon and alternate attention are pending owner integration; no DDP/EP implementation is claimed.

RoPE theta, expert bias and normalization are pending. Router bias_gamma 0 and rotary_fraction 1 are implementation limits, not selected experiment values. Smoke choices must not be copied into approved arms. Production runs require an agreement reference, scoring agreement and holdout provenance. G8 writer is optional follow-up integration, not a Monday submission blocker.

## Run from repository root

Requires the #188 arm pins (explicit eager attention and MTP off). Exact top-level dependency versions used for CPU verification are in harness/requirements-week2.txt. GPU wheels may require the appropriate PyTorch installation source; dependencies are not a complete hardware/driver lock.

```bash
python -m pytest teams/05-architecture/tests/test_week2_*.py -q
python -m unittest discover -s teams/05-architecture/tests -p 'test_week2*.py' -v
python teams/05-architecture/harness/check_week2.py teams/05-architecture/configs/arms/exp1/lr_1e-3.yaml --resolution teams/05-architecture/configs/small/smoke_resolution.yaml --tokenizer /path/tokenizer_v0.json --byte-table /path/raw_table.npz
python teams/05-architecture/harness/train_week2.py --config teams/05-architecture/configs/arms/exp1/lr_1e-3.yaml --tokenizer /path/tokenizer_v0.json --byte-table /path/raw_table.npz --train-data /path/train.jsonl --heldout-data /path/heldout.jsonl --device cpu --seed 1234 --smoke --smoke-steps 2 --smoke-seq-len 8 --smoke-batch-size 1 --out /path/fresh-output
```

On Windows use explicit test filenames or unittest discovery if the shell does not expand wildcards. Data is materialized in RAM: start with bounded text slices.

## Evaluation and metrics

UTF-8 JSONL uses id/text. Heldout IDs must be unique for quality runs. Every text-token target is scored once; padding and artificial BOS are excluded. BPB = summed FP32 next-token NLL / ln(2) / original UTF-8 bytes. Byte-table target lengths must conserve original bytes. Evaluation restores RNG and model mode.

All metrics.jsonl rows expose the legacy alarm keys: step, tokens_per_second, loss_ntp, loss_mtp, loss, lr, gpu_alloc_gb and gradient_norm. Training loss/loss_ntp are NTP, loss_mtp is 0 when disabled, gradient_norm is the pre-clipping norm, and gpu_alloc_gb uses GiB. Additional train/val fields are additive. Evaluation-only step 0 has zero placeholders for legacy training fields and is identifiable by val/* fields without train/ce_loss; consumers should apply training alarms only to training records.

The --heldout-report JSON needs heldout_sha256, fingerprint_set_id, scope="full", matches=0 and docs_checked. This records the data owner's evidence; it does not perform the G9 check. Official results require the file named by results/heldout_v1.sha256 and retained G9 logs.

## Provenance and experiment selection

The complete plan hash is recorded for traceability only. Editing plan prose does not block the harness. Arm shapes and rates are read directly; missing widths, invalid geometry and unsupported settings fail validation. Steps/time budgets remain harness-only defaults reviewed from the plan, and an arm can explicitly override run.steps/max_time_min. They must be reviewed if the lead changes budgets. A fixed whole-document hash is not used as enforcement.

Before EXP-1, the lead must select one harness for all five rates and all seeds in plan_v1.md. This revision supplies a proposed one-harness plan note separately; it does not silently change the lead's plan. Do not submit an EXP-1 job using this harness until that selection, real-data inputs and baseline decisions are ready.

## Remaining work

Official holdout/G9 evidence, G4-shipped table, approved mixture and unresolved baseline choices remain external inputs. CPU smoke results are not full-budget quality results. Full-context GPU feasibility, long-run stability and checkpoint-resume execution evidence remain required before relevant jobs. EXP-5 is removed by TSAI decision.
