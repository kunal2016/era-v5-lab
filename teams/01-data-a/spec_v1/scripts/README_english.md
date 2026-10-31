# Scripts of the English family

What checks the English family of `clean.py` on the English packs. Paths start at `teams/01-data-a/`. `clean.py` is the one cleaner: [../README_clean.md](../README_clean.md) says how to build and run it. `harm_test.py` is the team's, run as it is: it is on `g1-harm-test` until PR 140 merges. The packs are not in the repo.

| script | makes |
|---|---|
| `scripts/verify_clean_english.py` | `results/verify_clean_english.json`: `clean.py` gives the same action and text as the English rules of `specv1.md` on every English doc; a second run; ZWJ and ZWNJ. |
| `scripts/f1_eval_english.py` | `results/f1_eval_english.json`: F1 on the English packs, real hits and made-up values, as `tools/f1_eval.py` checks code. |
| `scripts/order_checks_english.py` | `results/order_checks_english.json`: the checks of the conflict ledger in `spec_v1_english.md`, on `medicine_english.md`. |
| `scripts/make_harm_tests_english.py` | `harm_tests_english.md` and the `results/` reports of `clean.py` and `medicine_english.md`, official gold and with the disputed docs left in. |

## Run it, in this order

```
pip install pyarrow pytest ftfy
python -I tools/build_clean.py
python -m pytest spec_v1/tests
python -I spec_v1/scripts/verify_clean_english.py <folder with the packs>
python -I spec_v1/scripts/f1_eval_english.py <g1-harm-test checkout> <folder with the packs>
python -I spec_v1/scripts/order_checks_english.py <folder with the packs>
python -I spec_v1/scripts/make_harm_tests_english.py <g1-harm-test checkout> <folder with the packs> <gold made with build_gold.py --allow-disputed>
```

`verify_clean_english.py` takes about 4 minutes, `order_checks_english.py` about 6, the others a minute or two. Every output is IDs, counts and digests, never document text. The packs must carry `pack_id`: `clean.py` picks the English rules by it.

## Kept, not used

`spec_v1/clean_english.py`, `spec_v1/scripts/clean_english.py` and `spec_v1/scripts/build_clean_english.py` made the English cleaners before `specv1.md`. They are kept for the record. No script or test loads them, and `clean.py` runs the same English rules. `run_clean_english.py` is kept so the old command still works: it runs `run_clean.py`, which runs `clean.py`.

The sheet itself (`medicine_english.md`), `decisions_english.md` and `results/evidence_english.json`, `results/equivalence_english.json` were compiled from the annotators' sheets by scripts that are not in this repo yet.
