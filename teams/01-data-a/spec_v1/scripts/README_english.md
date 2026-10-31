# Scripts of the English family

What makes the English files of `spec_v1/` from `medicine_english.md`. Paths start at `teams/01-data-a/`. `harm_test.py` is the team's, run as it is: it is on `g1-harm-test` until PR 140 merges. The packs are not in the repo.

| script | makes |
|---|---|
| `scripts/build_clean_english.py` | `scripts/clean_english.py`: the English cleaner on its own, one function per disease code, `clean(doc)` in the sheet's order. It stops, and writes nothing, if `DA-F1-005` is missing, not under F1 or not last. |
| `tools/build_clean.py` (the team's) | `clean.py` from every sheet but the English one (the code family's cleaner, as committed), and `clean_english.py` from the code and English sheets. A family the shared `tools/f1_rule.py` does not run on keeps its own F1: English runs `DA-F1-005`. |
| `run_clean_english.py` | Runs `clean_english.py` on one pack: `python spec_v1/run_clean_english.py --pack <pack>.parquet --out <dir>`. |
| `scripts/verify_clean_english.py` | `results/verify_clean_english.json`: `clean_english.py`, `scripts/clean_english.py` and the sheet give the same action and text on every English doc; a second run; ZWJ and ZWNJ. |
| `scripts/f1_eval_english.py` | `results/f1_eval_english.json`: F1 on the English packs, real hits and made-up values, as `tools/f1_eval.py` checks code. |
| `scripts/order_checks_english.py` | `results/order_checks_english.json`: the checks of the conflict ledger in `spec_v1_english.md`. |
| `scripts/make_harm_tests_english.py` | `harm_tests_english.md` and the `results/` reports of `clean_english.py`, `scripts/clean_english.py` and the sheet, official gold and with the disputed docs left in. |

## Run it, in this order

```
pip install pyarrow pytest ftfy
python -I spec_v1/scripts/build_clean_english.py
python -I tools/build_clean.py
python -m pytest spec_v1/tests
python -I spec_v1/scripts/verify_clean_english.py <folder with the packs>
python -I spec_v1/scripts/f1_eval_english.py <g1-harm-test checkout> <folder with the packs>
python -I spec_v1/scripts/order_checks_english.py <folder with the packs>
python -I spec_v1/scripts/make_harm_tests_english.py <g1-harm-test checkout> <folder with the packs> <gold made with build_gold.py --allow-disputed>
```

`verify_clean_english.py` takes about 4 minutes, `order_checks_english.py` about 6, the others a minute or two. Every output is IDs, counts and digests, never document text.

Two files are named `clean_english.py`: `spec_v1/clean_english.py` holds the code and English sheets (`tools/build_clean.py`), `spec_v1/scripts/clean_english.py` the English sheet alone (`scripts/build_clean_english.py`).

The sheet itself (`medicine_english.md`), `decisions_english.md` and `results/evidence_english.json`, `results/equivalence_english.json` were compiled from the annotators' sheets by scripts that are not in this repo yet.
