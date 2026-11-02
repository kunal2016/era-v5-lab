# F2 results: G9 fingerprints v1

`run_clean.py --f2` and the F2 harm test on the 13 Data A packs. Fingerprint set `11e290a44d1467875fdf8bebc55eab21f0a6367f411aab98a4a027a546fd372e` (full set), `clean.py` `d3464bdaa394`, `tools/f2_rule.py` `1e15e74914f4`. The harm reports are `f2_<pack>_harm.json`.

| pack | docs | dropped by `clean.py` | **dropped by F2** | kept | F2 on gold: changed + dropped | limit | harm test |
|---|---:|---:|---:|---:|---|---:|---|
| `code-cpp` | 500 | 10 | **0** | 490 | 0 + 0 of 122 | 1 | PASS |
| `code-go` | 500 | 44 | **0** | 456 | 0 + 0 of 163 | 1 | PASS |
| `code-java` | 500 | 11 | **0** | 489 | 0 + 0 of 116 | 1 | PASS |
| `code-js-ts` | 500 | 22 | **0** | 478 | 0 + 0 of 204 | 2 | PASS |
| `code-python` | 500 | 16 | **0** | 484 | 0 + 0 of 141 | 1 | PASS |
| `code-rust` | 500 | 17 | **0** | 483 | 0 + 0 of 234 | 2 | PASS |
| `en-dclm` | 500 | 9 | **0** | 491 | 0 + 0 of 62 | 1 | PASS |
| `en-fineweb-edu` | 500 | 1 | **1** | 498 | 0 + 1 of 158 | 1 | PASS |
| `en-nemotroncc` | 500 | 17 | **0** | 483 | 0 + 0 of 129 | 1 | PASS |
| `en-nemotroncc-synth` | 500 | 1 | **0** | 499 | 0 + 0 of 326 | 3 | PASS |
| `math-finemath` | 500 | 13 | **7** | 480 | 0 + 0 of 86 | 1 | PASS |
| `math-megamath` | 500 | 10 | **2** | 488 | 0 + 0 of 26 | 1 | PASS |
| `sci-finepdfs` | 500 | 13 | **3** | 484 | 0 + 0 of 202 | 2 | PASS |

The harm test runs F2 on the raw gold docs; `run_clean.py --f2` runs it on the text `clean.py` keeps.

## Dropped by F2

Up to 5 benchmark items per doc. The offset is in the cleaned text.

| pack | doc | benchmark items | offset |
|---|---|---|---:|
| `en-fineweb-edu` | `dabaf841592d630e` | `milu:test:19374` | 2,108 |
| `math-finemath` | `90bbe1d4fc081caa` | `mmlu:test:5219`, `mmlu:test:1329`, `mmlu:test:5403`, `mmlu:test:5019`, `mmlu:test:1040` | 5,586 |
| `math-finemath` | `9fd5f2644b8c04d8` | `milu:test:10689`, `mmlu:test:6524` | 4,994 |
| `math-finemath` | `e9bc93d8821adcec` | `milu:test:16197`, `milu:test:6786`, `milu:test:16261`, `milu:test:10433`, `milu:test:6726` | 109,563 |
| `math-finemath` | `263a5308b96d2e4a` | `milu:test:10090` | 3,850 |
| `math-finemath` | `376e639903abfe9a` | `milu:test:11752` | 1,614 |
| `math-finemath` | `65a9730b24a24909` | `livecodebench:release_v6:3047` | 5,591 |
| `math-finemath` | `3a2ccc88dfcd67c9` | `milu:test:16177` | 10,018 |
| `math-megamath` | `1ad9fec1410f4b83` | `mmlu:test:5219`, `mmlu:test:1329`, `mmlu:test:5403`, `mmlu:test:5019`, `mmlu:test:1040` | 1,543 |
| `math-megamath` | `8aee157afdb8bb59` | `livecodebench:release_v6:2953` | 97 |
| `sci-finepdfs` | `d20d4f04e5704ba7` | `hle:test:6724d81d42ec04c22a24aa83` | 37,440 |
| `sci-finepdfs` | `35eb8b91a98d3a41` | `mmlu:test:5817`, `mmlu:test:5654`, `mmlu:test:5727` | 1,111,191 |
| `sci-finepdfs` | `3f91dba6d4dcbafd` | `hle:test:6724d81d42ec04c22a24aa83` | 22,947 |

A flag is one shared run of words with a benchmark item. Read the dropped docs before you trust them: a run can be shared public text that a benchmark also quotes (answer-option layouts, exam instructions, citations, a quoted passage).
