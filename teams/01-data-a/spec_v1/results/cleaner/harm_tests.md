# Spec v1 harm tests

DRAFT. Each cell: gold docs changed + dropped, for that function on that pack's gold set. Limit: `max(1, floor(1% of gold))`. Made by `tools/make_harm_tests.py` with the team's `harm_test.py`.

| function | go | rust | js-ts | java | cpp | python |
|---|---:|---:|---:|---:|---:|---:|
| gold docs (limit) | 163 (1) | 78 (1) | 204 (2) | 116 (1) | 120 (1) | 46 (1) |
| A1 | 0 | 0 | 0 | 0 | 0 | 0 |
| A2 | 0 | 0 | 0 | 0 | 0 | 0 |
| A6 | 0 | 0 | 0 | 0 | 0 | 0 |
| A4 | 0 | 0 | 0 | 0 | 0 | 0 |
| B3 | 0 | 0 | 0 | 0 | 0 | 0 |
| E1 | 0 | 0 | 0 | 0 | 0 | 0 |
| E2 | 0 | 0 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 | 0 | 0 |
| C4 | 0 | 0 | 0 | 0 | 0 | 0 |
| E4 | 0 | 0 | 1 | 0 | 0 | 0 |
| C1 | 0 | 0 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0 | 0 | 0 |
| E3 | 0 | 0 | 0 | 0 | 0 | 0 |
| F1 | 0 | 0 | 0 | 0 | 0 | 0 |
| ALL IN ORDER | 0 | 0 | 1 | 0 | 0 | 0 |

Affected gold IDs are in `results/clean_<pack>_harm.json`. No document text is kept.

## Not run

| family | pack | gold docs | why |
|---|---|---:|---|
| English | en-dclm | 62 | pack not on this machine: NOT RUN |
| English | en-fineweb-edu | 158 | pack not on this machine: NOT RUN |
| English | en-nemotroncc | 34 | pack not on this machine: NOT RUN |
| English | en-nemotroncc-synth | 96 | pack not on this machine: NOT RUN |
| math | math-finemath | 30 | pack not on this machine: NOT RUN |
| math | math-megamath | 0 | gold set is empty: NOT TESTABLE |
| science | sci-finepdfs | 40 | pack not on this machine: NOT RUN |
