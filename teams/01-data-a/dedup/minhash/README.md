# MinHash + LSH for overlap (dedup v2 item 11)

**Status: measurement only. Proposed as a fallback, not adopted.** Nothing in v1 (`overlap.py`, `overlap_rules.py`,
`dedup.json`, the corpus-v1 job) uses or changes because of this folder. It is here so the evidence can be reviewed if
exact all-pairs overlap does not fit the corpus-v1 job's memory or time (week-4 plan item 1.5, resource fit).

| File | What it is |
|---|---|
| `minhash_vs_v1_comparison_v1.md` | Start here: how it differs from v1, memory at corpus-v1 scale, correctness |
| `minhash_lsh_agreement_v1.md` | Results: recall and candidate counts for each band setting, word and code |
| `README_minhash_item11.md` | Method, how each number was measured, steps to rerun |
| `sigs.py`, `codesigs.py` | Signatures from v1's own word and code shingle functions |
| `evaluate.py`, `evaluate_code.py` | Recall, candidates and MinHash error against TSAI's 5 Nov overlap run |
| `results.json`, `results_code.json` | The numbers in the tables (counts only, no document text or IDs) |

Run from the repo root, with the script paths prefixed by `teams/01-data-a/dedup/minhash/`
(for example `python teams/01-data-a/dedup/minhash/sigs.py ...`); the defaults `DEDUP_DIR=teams/01-data-a/dedup`,
`MH_OUT=out/minhash_item11` and `OVERLAP_RUN=out/overlap_tsai` then work as they are. Signatures and outputs go to `out/`,
which is not committed.

Not yet tested: held-out↔train pairs, `code-cpp`, `code-java`, `code-js-ts`, a second seed, cross-pack pairs beyond
the 11 packs, and memory and speed on TSAI's machine.
