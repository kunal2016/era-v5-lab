# SFT decontamination report

Run for G10 on 2026-11-06 to 2026-11-07. Every set was checked against Team 9's benchmark fingerprints **v2** with the **full set** (no `--benchmarks`, `--tags` or `--exclude`), and scanned for canaries.

- **set_sha256:** `2826a3b883210c653979103c09ce1c79e40fc4f7034b54027f2836482370d22a`
- **Tools:** `teams/09-evaluation/decontam/decontam_check.py` and `canary_scan.py`, lab main `c6b0ce0961028020b3e3eaf86fe0c5873fca3bc0`. sha256 of the files used:
  - `canary_scan.py`: `322066d675e13af8bee0d05602f755f49e33da5a148bf664306ce6d6a9f908c2`
  - `decontam_check.py`: `62a269a25123543b5470c4956ba1be530ea257c597bc2be2eab19201cb62df8f`
  - `fpset.py`: `7f5f48d08506d619ebfadd2742e86d29ec3ea28e5fcfd729f13cd8d959689c59`
  - `lab_canary.py`: `373536a777c9f16367cf6affcc2cc6243755ac23e75850a2624eadf65918ea09`
  - `normalize.py`: `570dcb820ac2ae6c667b1abc5ea1d781a6795aa42a7735aa94377e756d7d70e9`
- **Runner and reconciliation:** `sft/decontam_run.py`; this file is written by `sft/decontam_report.py`.
- **Sets run:** 16. **Rows in:** 2,096,624. **Removed (flagged or canary):** 43,448 (2.07%). **Kept:** 2,053,176.
- No benchmark item text is in this file or in the run records: only set names, counts, document ids, benchmark item ids, offsets and sha256 values.

## 1. Result per set

| Set | Rows in | Flagged | Canary | Removed | Rows kept | Clean file sha256 |
|---|---:|---:|---:|---:|---:|---|
| `sft-agentic-nemotron-agentic-v1` | 315,560 | 432 | 0 | 432 (0.14%) | 315,128 | `5f05e6f91fbe…` |
| `sft-bespoke-stratos-17k` | 16,710 | 1,791 | 0 | 1,791 (10.72%) | 14,919 | `7ba1dc2bb254…` |
| `sft-chat-nemotron-if-v1` | 4,963 | 1 | 0 | 1 (0.02%) | 4,962 | `38e757a1a7f8…` |
| `sft-code-codeforces-cots` | 45,734 | 20,796 | 0 | 20,796 (45.47%) | 24,938 | `b5df0cfbc19b…` |
| `sft-code-nemotron-cuda` | 2,273 | 2 | 0 | 2 (0.09%) | 2,271 | `f451b673db79…` |
| `sft-code-nemotron-terminal` | 31,928 | 9,901 | 0 | 9,901 (31.01%) | 22,027 | `59278bca72a9…` |
| `sft-code-swe-rebench-openhands` | 27,516 | 4,864 | 0 | 4,864 (17.68%) | 22,652 | `7c2b95c36dc0…` |
| `sft-dolly-15k` | 15,011 | 4 | 0 | 4 (0.03%) | 15,007 | `93069f7a3a2c…` |
| `sft-indic-aya-collection` | 654,530 | 6 | 0 | 6 (0.00%) | 654,524 | `cb4b80d9253a…` |
| `sft-indic-aya-dataset` | 41,261 | 8 | 0 | 8 (0.02%) | 41,253 | `a1d2c8f07122…` |
| `sft-indic-indic-align-dolly-t` | 15,011 | 0 | 0 | 0 (0.00%) | 15,011 | `35980cee7f1d…` |
| `sft-math-nemotron-sft-math-v4` | 542,117 | 4,776 | 0 | 4,776 (0.88%) | 537,341 | `20c00f0cd256…` |
| `sft-oasst2` | 9,548 | 5 | 0 | 5 (0.05%) | 9,543 | `c89de79a902a…` |
| `sft-science-glm51-phd` | 103,702 | 207 | 0 | 207 (0.20%) | 103,495 | `54d681c1edc8…` |
| `sft-science-nemotron-science-v2` | 96,605 | 286 | 0 | 286 (0.30%) | 96,319 | `390c839aae1b…` |
| `sft-science-nemotron-science` | 174,155 | 369 | 0 | 369 (0.21%) | 173,786 | `6f9ac4dc35a0…` |
| **Total** | **2,096,624** | **43,448** | **0** | **43,448** (2.07%) | **2,053,176** | |

A row that is both flagged and carries a canary counts once in Removed.

## 2. Flagged documents by benchmark

| Set | `aime_2024` | `aime_2025` | `bfcl_v3` | `codeforces` | `flores200` | `gaia` | `gpqa_diamond` | `heldout_g5_v1` | `hle` | `in22_conv` | `in22_gen` | `livecodebench` | `longbench_v2` | `milu` | `mmlu` | `swe_bench_live` | `swe_bench_pro` | `swe_bench_verified` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 0 | 0 | 66 | 0 | 6 | 0 | 0 | 0 | 27 | 2 | 0 | 6 | 0 | 43 | 6 | 277 | 0 | 0 |
| `sft-bespoke-stratos-17k` | 87 | 73 | 1 | 1010 | 0 | 1 | 1 | 2 | 122 | 0 | 0 | 838 | 0 | 3 | 99 | 0 | 0 | 0 |
| `sft-chat-nemotron-if-v1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| `sft-code-codeforces-cots` | 0 | 0 | 0 | 19253 | 0 | 5 | 0 | 6 | 1738 | 0 | 0 | 10720 | 0 | 1 | 1 | 0 | 0 | 0 |
| `sft-code-nemotron-cuda` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-code-nemotron-terminal` | 0 | 0 | 0 | 7812 | 0 | 2 | 0 | 3 | 183 | 0 | 0 | 5743 | 0 | 2 | 0 | 9 | 2 | 0 |
| `sft-code-swe-rebench-openhands` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 4474 | 21 | 1058 |
| `sft-dolly-15k` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 |
| `sft-indic-aya-collection` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-indic-aya-dataset` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-sft-math-v4` | 225 | 308 | 1 | 199 | 0 | 1 | 65 | 52 | 3070 | 0 | 0 | 574 | 1 | 6 | 228 | 299 | 10 | 66 |
| `sft-oasst2` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 0 |
| `sft-science-glm51-phd` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 207 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-science-nemotron-science-v2` | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 183 | 0 | 0 | 0 | 0 | 34 | 74 | 2 | 0 | 0 |
| `sft-science-nemotron-science` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 272 | 0 | 0 | 0 | 0 | 42 | 68 | 0 | 0 | 0 |

A document is flagged when it shares at least one 13-word run (20 tokens for code) with a benchmark item. The whole document is removed. The count is documents per benchmark, so a document that matches two benchmarks counts in both columns.

## 3. Flagged documents by coverage

Coverage is the share of one benchmark item's runs that the document contains (the highest over its hits). The bands are for reading the result; every flagged document is removed whatever its band.

| Set | Flagged | Coverage 0.5 or more | 0.1 to 0.5 | Below 0.1 |
|---|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 432 | 4 | 53 | 375 |
| `sft-bespoke-stratos-17k` | 1791 | 38 | 73 | 1680 |
| `sft-chat-nemotron-if-v1` | 1 | 0 | 1 | 0 |
| `sft-code-codeforces-cots` | 20796 | 45 | 1563 | 19188 |
| `sft-code-nemotron-cuda` | 2 | 0 | 0 | 2 |
| `sft-code-nemotron-terminal` | 9901 | 321 | 454 | 9126 |
| `sft-code-swe-rebench-openhands` | 4864 | 147 | 263 | 4454 |
| `sft-dolly-15k` | 4 | 0 | 1 | 3 |
| `sft-indic-aya-collection` | 6 | 1 | 0 | 5 |
| `sft-indic-aya-dataset` | 8 | 1 | 2 | 5 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-sft-math-v4` | 4776 | 0 | 42 | 4734 |
| `sft-oasst2` | 5 | 0 | 3 | 2 |
| `sft-science-glm51-phd` | 207 | 0 | 0 | 207 |
| `sft-science-nemotron-science-v2` | 286 | 0 | 6 | 280 |
| `sft-science-nemotron-science` | 369 | 0 | 3 | 366 |

## 4. Benchmark items with the largest overlap

**`sft-agentic-nemotron-agentic-v1`**: at least 44 different benchmark items found in 432 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `bfcl_v3:test:live_irrelevance_719-238-0` | 2 | 1.000 | 1 / 1 | `sft-agentic-nemotron-agentic-v1/179971` | 12558 |
| `bfcl_v3:test:simple_336` | 1 | 1.000 | 1 / 1 | `sft-agentic-nemotron-agentic-v1/117494` | 1382 |
| `bfcl_v3:test:simple_0` | 2 | 0.800 | 4 / 5 | `sft-agentic-nemotron-agentic-v1/227915` | 975 |
| `mmlu:test:5882` | 3 | 0.451 | 107 / 237 | `sft-agentic-nemotron-agentic-v1/21810` | 5053 |
| `mmlu:test:6050` | 3 | 0.439 | 107 / 244 | `sft-agentic-nemotron-agentic-v1/21810` | 5053 |
| `mmlu:test:5857` | 3 | 0.431 | 107 / 248 | `sft-agentic-nemotron-agentic-v1/21810` | 5053 |
| `mmlu:test:5962` | 3 | 0.392 | 107 / 273 | `sft-agentic-nemotron-agentic-v1/21810` | 5053 |
| `milu:test:12344` | 37 | 0.289 | 11 / 38 | `sft-agentic-nemotron-agentic-v1/4106` | 7675 |
| `bfcl_v3:test:parallel_19` | 4 | 0.176 | 3 / 17 | `sft-agentic-nemotron-agentic-v1/114753` | 1367 |
| `milu:test:19953` | 2 | 0.167 | 1 / 6 | `sft-agentic-nemotron-agentic-v1/36422` | 42473 |
| `milu:test:18206` | 2 | 0.151 | 8 / 53 | `sft-agentic-nemotron-agentic-v1/57058` | 35190 |
| `bfcl_v3:test:parallel_145` | 12 | 0.133 | 4 / 30 | `sft-agentic-nemotron-agentic-v1/34328` | 1959 |
| `mmlu:test:5718` | 1 | 0.128 | 19 / 148 | `sft-agentic-nemotron-agentic-v1/297793` | 13058 |
| `mmlu:test:5752` | 1 | 0.124 | 19 / 153 | `sft-agentic-nemotron-agentic-v1/297793` | 13058 |
| `mmlu:test:5680` | 1 | 0.119 | 19 / 160 | `sft-agentic-nemotron-agentic-v1/297793` | 13058 |

**`sft-bespoke-stratos-17k`**: at least 864 different benchmark items found in 1791 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4291` | 1 | 0.860 | 74 / 86 | `sft-bespoke-stratos-17k/8225` | 111 |
| `mmlu:test:4279` | 1 | 0.855 | 71 / 83 | `sft-bespoke-stratos-17k/7617` | 111 |
| `mmlu:test:4393` | 1 | 0.829 | 58 / 70 | `sft-bespoke-stratos-17k/7103` | 111 |
| `mmlu:test:4423` | 1 | 0.821 | 55 / 67 | `sft-bespoke-stratos-17k/3900` | 111 |
| `mmlu:test:4302` | 1 | 0.778 | 42 / 54 | `sft-bespoke-stratos-17k/3719` | 111 |
| `mmlu:test:4384` | 1 | 0.778 | 42 / 54 | `sft-bespoke-stratos-17k/7505` | 111 |
| `mmlu:test:4263` | 1 | 0.765 | 39 / 51 | `sft-bespoke-stratos-17k/4632` | 111 |
| `mmlu:test:4399` | 1 | 0.745 | 35 / 47 | `sft-bespoke-stratos-17k/5292` | 111 |
| `mmlu:test:4457` | 1 | 0.733 | 33 / 45 | `sft-bespoke-stratos-17k/5216` | 111 |
| `mmlu:test:4360` | 1 | 0.692 | 27 / 39 | `sft-bespoke-stratos-17k/7653` | 111 |
| `mmlu:test:4451` | 1 | 0.692 | 27 / 39 | `sft-bespoke-stratos-17k/5609` | 111 |
| `mmlu:test:4460` | 1 | 0.676 | 25 / 37 | `sft-bespoke-stratos-17k/4457` | 111 |
| `mmlu:test:4261` | 1 | 0.657 | 23 / 35 | `sft-bespoke-stratos-17k/4603` | 111 |
| `mmlu:test:4262` | 3 | 0.657 | 23 / 35 | `sft-bespoke-stratos-17k/6359` | 111 |
| `mmlu:test:4303` | 1 | 0.657 | 23 / 35 | `sft-bespoke-stratos-17k/3229` | 111 |

**`sft-chat-nemotron-if-v1`**: at least 1 different benchmark items found in 1 documents (top 1 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:12344` | 1 | 0.289 | 11 / 38 | `sft-chat-nemotron-if-v1/3111` | 7832 |

**`sft-code-codeforces-cots`**: at least 544 different benchmark items found in 20796 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `livecodebench:release_v6:1899_D` | 473 | 0.883 | 355 / 402 | `sft-code-codeforces-cots/12840` | 461 |
| `livecodebench:release_v6:1883_B` | 186 | 0.871 | 371 / 426 | `sft-code-codeforces-cots/10455` | 462 |
| `livecodebench:release_v6:1899_B` | 157 | 0.868 | 356 / 410 | `sft-code-codeforces-cots/27580` | 807 |
| `livecodebench:release_v6:1883_C` | 703 | 0.837 | 272 / 325 | `sft-code-codeforces-cots/22480` | 807 |
| `livecodebench:release_v6:1873_D` | 516 | 0.796 | 215 / 270 | `sft-code-codeforces-cots/37935` | 806 |
| `livecodebench:release_v6:1899_C` | 298 | 0.769 | 163 / 212 | `sft-code-codeforces-cots/40055` | 807 |
| `livecodebench:release_v6:1873_B` | 958 | 0.739 | 119 / 161 | `sft-code-codeforces-cots/44217` | 807 |
| `livecodebench:release_v6:1873_A` | 326 | 0.694 | 161 / 232 | `sft-code-codeforces-cots/44420` | 806 |
| `livecodebench:release_v6:1899_A` | 35 | 0.683 | 95 / 139 | `sft-code-codeforces-cots/11290` | 462 |
| `hle:test:66ed458ed841eb51a985ca8d` | 5 | 0.429 | 175 / 408 | `sft-code-codeforces-cots/5090` | 452 |
| `hle:test:672f6cfd609b665328565e5c` | 5 | 0.343 | 109 / 318 | `sft-code-codeforces-cots/8195` | 461 |
| `codeforces:test:2018/B` | 3878 | 0.267 | 56 / 210 | `sft-code-codeforces-cots/33780` | 1391 |
| `codeforces:test:2060/D` | 2117 | 0.248 | 53 / 214 | `sft-code-codeforces-cots/1095` | 1479 |
| `hle:test:672f72e3609b665328565e6b` | 5 | 0.213 | 112 / 526 | `sft-code-codeforces-cots/37475` | 806 |
| `codeforces:test:2018/A` | 139 | 0.209 | 83 / 398 | `sft-code-codeforces-cots/4730` | 462 |

**`sft-code-nemotron-cuda`**: at least 2 different benchmark items found in 2 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:6726c7e9d2ad475e400669c7` | 1 | 0.002 | 1 / 635 | `sft-code-nemotron-cuda/952` | 30663 |
| `codeforces:test:2055/C` | 1 | 0.001 | 1 / 885 | `sft-code-nemotron-cuda/272` | 15733 |

**`sft-code-nemotron-terminal`**: at least 1034 different benchmark items found in 9901 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `codeforces:test:2041/K` | 8 | 0.978 | 619 / 633 | `sft-code-nemotron-terminal/18418` | 2924 |
| `codeforces:test:2005/C` | 12 | 0.977 | 597 / 611 | `sft-code-nemotron-terminal/20488` | 2924 |
| `codeforces:test:2036/E` | 3 | 0.977 | 644 / 659 | `sft-code-nemotron-terminal/27896` | 2924 |
| `codeforces:test:2045/D` | 1 | 0.977 | 558 / 571 | `sft-code-nemotron-terminal/15045` | 2924 |
| `codeforces:test:2038/A` | 161 | 0.976 | 569 / 583 | `sft-code-nemotron-terminal/6020` | 2924 |
| `codeforces:test:2053/I2` | 14 | 0.976 | 648 / 664 | `sft-code-nemotron-terminal/14967` | 2924 |
| `codeforces:test:2053/D` | 35 | 0.975 | 584 / 599 | `sft-code-nemotron-terminal/1107` | 2924 |
| `codeforces:test:2037/F` | 10 | 0.974 | 520 / 534 | `sft-code-nemotron-terminal/3412` | 2924 |
| `codeforces:test:2045/M` | 3 | 0.974 | 482 / 495 | `sft-code-nemotron-terminal/14150` | 2924 |
| `codeforces:test:2056/E` | 63 | 0.974 | 530 / 544 | `sft-code-nemotron-terminal/6225` | 2924 |
| `codeforces:test:1993/E` | 12 | 0.972 | 527 / 542 | `sft-code-nemotron-terminal/28570` | 2924 |
| `codeforces:test:2029/I` | 41 | 0.972 | 492 / 506 | `sft-code-nemotron-terminal/25304` | 2923 |
| `codeforces:test:2034/F1` | 40 | 0.972 | 630 / 648 | `sft-code-nemotron-terminal/9760` | 2924 |
| `codeforces:test:2037/D` | 10 | 0.972 | 486 / 500 | `sft-code-nemotron-terminal/1247` | 2924 |
| `codeforces:test:2049/D` | 19 | 0.972 | 480 / 494 | `sft-code-nemotron-terminal/19100` | 2924 |

**`sft-code-swe-rebench-openhands`**: at least 248 different benchmark items found in 4864 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:conan-io__conan-15699` | 7 | 1.000 | 238 / 238 | `sft-code-swe-rebench-openhands/2389` | 27508 |
| `swe_bench_live:test:conan-io__conan-15931` | 16 | 1.000 | 49 / 49 | `sft-code-swe-rebench-openhands/3506` | 27508 |
| `swe_bench_live:test:streamlink__streamlink-5926` | 67 | 0.996 | 278 / 279 | `sft-code-swe-rebench-openhands/4242` | 27521 |
| `swe_bench_live:test:streamlink__streamlink-5908` | 8 | 0.973 | 358 / 368 | `sft-code-swe-rebench-openhands/2596` | 27521 |
| `swe_bench_live:test:streamlink__streamlink-6242` | 99 | 0.924 | 171 / 185 | `sft-code-swe-rebench-openhands/92` | 27523 |
| `swe_bench_live:test:beeware__briefcase-1638` | 10 | 0.920 | 103 / 112 | `sft-code-swe-rebench-openhands/257` | 27514 |
| `swe_bench_live:test:streamlink__streamlink-6111` | 29 | 0.910 | 264 / 290 | `sft-code-swe-rebench-openhands/54362` | 27521 |
| `swe_bench_live:test:pdm-project__pdm-3393` | 6 | 0.853 | 1587 / 1860 | `sft-code-swe-rebench-openhands/3420` | 27512 |
| `swe_bench_live:test:beeware__briefcase-2075` | 8 | 0.826 | 371 / 449 | `sft-code-swe-rebench-openhands/5499` | 27513 |
| `swe_bench_live:test:beeware__briefcase-2035` | 9 | 0.793 | 219 / 276 | `sft-code-swe-rebench-openhands/14829` | 27513 |
| `swe_bench_live:test:pypsa__pypsa-891` | 20 | 0.760 | 409 / 538 | `sft-code-swe-rebench-openhands/18871` | 27503 |
| `swe_bench_live:test:pdm-project__pdm-2743` | 8 | 0.739 | 345 / 467 | `sft-code-swe-rebench-openhands/2163` | 27511 |
| `swe_bench_live:test:beeware__briefcase-2088` | 10 | 0.671 | 112 / 167 | `sft-code-swe-rebench-openhands/4500` | 27513 |
| `swe_bench_live:test:pdm-project__pdm-3420` | 6 | 0.647 | 306 / 473 | `sft-code-swe-rebench-openhands/36635` | 27511 |
| `swe_bench_live:test:run-llama__llama_deploy-356` | 5 | 0.643 | 220 / 342 | `sft-code-swe-rebench-openhands/2618` | 27523 |

**`sft-dolly-15k`**: at least 4 different benchmark items found in 4 documents (top 4 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:18206` | 1 | 0.151 | 8 / 53 | `sft-dolly-15k/5001` | 1325 |
| `milu:test:18158` | 1 | 0.094 | 3 / 32 | `sft-dolly-15k/8241` | 1277 |
| `mmlu:test:5399` | 1 | 0.071 | 4 / 56 | `sft-dolly-15k/903` | 4290 |
| `mmlu:test:3762` | 1 | 0.042 | 2 / 48 | `sft-dolly-15k/6631` | 2232 |

**`sft-indic-aya-collection`**: at least 2 different benchmark items found in 6 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `heldout_g5_v1:heldout:fw2-hi-test-000022` | 2 | 0.830 | 210 / 253 | `sft-indic-aya-collection/91215` | 223 |
| `in22_gen:test:803` | 4 | 0.011 | 10 / 913 | `sft-indic-aya-collection/31863` | 1702 |

**`sft-indic-aya-dataset`**: at least 10 different benchmark items found in 8 documents (top 10 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `flores200:dev+devtest:dev:mar_Deva:259` | 1 | 1.000 | 8 / 8 | `sft-indic-aya-dataset/166237` | 110 |
| `flores200:dev+devtest:dev:hin_Deva:259` | 1 | 0.650 | 13 / 20 | `sft-indic-aya-dataset/166237` | 334 |
| `flores200:dev+devtest:devtest:hin_Deva:630` | 1 | 0.250 | 2 / 8 | `sft-indic-aya-dataset/52284` | 279 |
| `milu:test:56156` | 1 | 0.240 | 6 / 25 | `sft-indic-aya-dataset/144625` | 120 |
| `milu:test:79035` | 1 | 0.088 | 5 / 57 | `sft-indic-aya-dataset/19493` | 146 |
| `milu:test:35432` | 2 | 0.050 | 5 / 101 | `sft-indic-aya-dataset/16747` | 383 |
| `milu:test:37859` | 2 | 0.041 | 6 / 147 | `sft-indic-aya-dataset/16747` | 416 |
| `milu:test:34937` | 2 | 0.039 | 6 / 155 | `sft-indic-aya-dataset/16747` | 416 |
| `milu:test:76394` | 2 | 0.018 | 1 / 57 | `sft-indic-aya-dataset/27660` | 165 |
| `milu:test:34930` | 2 | 0.009 | 1 / 114 | `sft-indic-aya-dataset/16747` | 437 |

**`sft-math-nemotron-sft-math-v4`**: at least 377 different benchmark items found in 4776 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `aime_2025:test:11` | 45 | 0.269 | 18 / 67 | `sft-math-nemotron-sft-math-v4/6516` | 432 |
| `hle:test:6720ff60488fb478b942537b` | 3 | 0.181 | 62 / 343 | `sft-math-nemotron-sft-math-v4/14349` | 183 |
| `hle:test:66f5fd3235147083021a66c6` | 5 | 0.176 | 13 / 74 | `sft-math-nemotron-sft-math-v4/510982` | 37907 |
| `mmlu:test:4348` | 1 | 0.167 | 1 / 6 | `sft-math-nemotron-sft-math-v4/40570` | 90857 |
| `hle:test:676433a3921b0ce4e14c557f` | 3 | 0.165 | 36 / 218 | `sft-math-nemotron-sft-math-v4/224103` | 26138 |
| `aime_2025:test:7` | 137 | 0.152 | 7 / 46 | `sft-math-nemotron-sft-math-v4/10585` | 288 |
| `mmlu:test:4258` | 3 | 0.130 | 3 / 23 | `sft-math-nemotron-sft-math-v4/544334` | 7785 |
| `livecodebench:release_v6:2791` | 1 | 0.126 | 47 / 372 | `sft-math-nemotron-sft-math-v4/223273` | 32874 |
| `aime_2025:test:14` | 9 | 0.125 | 4 / 32 | `sft-math-nemotron-sft-math-v4/65308` | 83047 |
| `mmlu:test:4977` | 1 | 0.105 | 2 / 19 | `sft-math-nemotron-sft-math-v4/4383` | 9178 |
| `aime_2025:test:16` | 3 | 0.100 | 1 / 10 | `sft-math-nemotron-sft-math-v4/397447` | 57192 |
| `mmlu:test:6857` | 1 | 0.100 | 1 / 10 | `sft-math-nemotron-sft-math-v4/9701` | 1251 |
| `mmlu:test:4344` | 2 | 0.095 | 2 / 21 | `sft-math-nemotron-sft-math-v4/287992` | 60463 |
| `aime_2025:test:21` | 119 | 0.087 | 4 / 46 | `sft-math-nemotron-sft-math-v4/2337` | 331 |
| `mmlu:test:5219` | 1 | 0.080 | 2 / 25 | `sft-math-nemotron-sft-math-v4/361487` | 11982 |

**`sft-oasst2`**: at least 8 different benchmark items found in 5 documents (top 8 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:5882` | 1 | 0.451 | 107 / 237 | `sft-oasst2/7181` | 969 |
| `mmlu:test:6050` | 1 | 0.439 | 107 / 244 | `sft-oasst2/7181` | 969 |
| `mmlu:test:5857` | 1 | 0.431 | 107 / 248 | `sft-oasst2/7181` | 969 |
| `mmlu:test:5962` | 1 | 0.392 | 107 / 273 | `sft-oasst2/7181` | 969 |
| `milu:test:15661` | 1 | 0.200 | 8 / 40 | `sft-oasst2/8966` | 2153 |
| `milu:test:18206` | 1 | 0.132 | 7 / 53 | `sft-oasst2/5847` | 999 |
| `swe_bench_live:test:kozea__weasyprint-2326` | 1 | 0.004 | 2 / 545 | `sft-oasst2/11303` | 2187 |
| `hle:test:66e932f00bd16d40d4bc4d81` | 1 | 0.003 | 1 / 378 | `sft-oasst2/8809` | 228 |

**`sft-science-glm51-phd`**: at least 9 different benchmark items found in 207 documents (top 9 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:6722870ef7bda9406bc723ac` | 2 | 0.014 | 5 / 349 | `sft-science-glm51-phd/23360` | 93359 |
| `hle:test:6700fe18dcd877e17dbc6c26` | 23 | 0.008 | 5 / 601 | `sft-science-glm51-phd/24646` | 11316 |
| `hle:test:66fc56f5d90ebe461bfd0c9c` | 156 | 0.007 | 7 / 1065 | `sft-science-glm51-phd/54631` | 884 |
| `hle:test:6769bce8a4435c3c69035510` | 1 | 0.006 | 7 / 1139 | `sft-science-glm51-phd/73911` | 46536 |
| `hle:test:67253690bcd1c268662e77bb` | 4 | 0.004 | 3 / 769 | `sft-science-glm51-phd/20343` | 32260 |
| `hle:test:676edcd5fc03fd7d07467628` | 5 | 0.002 | 3 / 1915 | `sft-science-glm51-phd/3252` | 49833 |
| `hle:test:6771d50cff6d0a6c35d7ca99` | 1 | 0.002 | 4 / 1725 | `sft-science-glm51-phd/16544` | 12169 |
| `hle:test:66eb707cb1d5bf033573afa3` | 3 | 0.001 | 3 / 2460 | `sft-science-glm51-phd/52594` | 32233 |
| `hle:test:67390213fc9dc4f5102ad835` | 12 | 0.001 | 2 / 2066 | `sft-science-glm51-phd/20387` | 2181 |

**`sft-science-nemotron-science-v2`**: at least 66 different benchmark items found in 286 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:1421` | 4 | 0.167 | 1 / 6 | `sft-science-nemotron-science-v2/10650` | 320 |
| `milu:test:8418` | 1 | 0.143 | 1 / 7 | `sft-science-nemotron-science-v2/31057` | 4764 |
| `mmlu:test:1470` | 1 | 0.143 | 7 / 49 | `sft-science-nemotron-science-v2/80821` | 231 |
| `mmlu:test:7288` | 1 | 0.095 | 2 / 21 | `sft-science-nemotron-science-v2/47397` | 438 |
| `mmlu:test:7375` | 1 | 0.095 | 2 / 21 | `sft-science-nemotron-science-v2/47397` | 438 |
| `milu:test:14642` | 2 | 0.087 | 4 / 46 | `sft-science-nemotron-science-v2/3023` | 846 |
| `mmlu:test:5219` | 1 | 0.080 | 2 / 25 | `sft-science-nemotron-science-v2/87583` | 2856 |
| `mmlu:test:7306` | 1 | 0.080 | 2 / 25 | `sft-science-nemotron-science-v2/47397` | 438 |
| `mmlu:test:7348` | 1 | 0.080 | 2 / 25 | `sft-science-nemotron-science-v2/47397` | 438 |
| `mmlu:test:7374` | 1 | 0.080 | 2 / 25 | `sft-science-nemotron-science-v2/47397` | 438 |
| `mmlu:test:5403` | 1 | 0.065 | 2 / 31 | `sft-science-nemotron-science-v2/87583` | 2856 |
| `milu:test:15172` | 1 | 0.063 | 4 / 63 | `sft-science-nemotron-science-v2/25763` | 652 |
| `mmlu:test:3078` | 2 | 0.055 | 4 / 73 | `sft-science-nemotron-science-v2/88744` | 203520 |
| `milu:test:11467` | 1 | 0.048 | 1 / 21 | `sft-science-nemotron-science-v2/93322` | 9733 |
| `mmlu:test:5019` | 1 | 0.047 | 2 / 43 | `sft-science-nemotron-science-v2/87583` | 2856 |

**`sft-science-nemotron-science`**: at least 63 different benchmark items found in 369 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:1421` | 2 | 0.167 | 1 / 6 | `sft-science-nemotron-science/86581` | 320 |
| `mmlu:test:1470` | 1 | 0.143 | 7 / 49 | `sft-science-nemotron-science/50243` | 219 |
| `mmlu:test:7288` | 3 | 0.095 | 2 / 21 | `sft-science-nemotron-science/14799` | 306 |
| `mmlu:test:7375` | 3 | 0.095 | 2 / 21 | `sft-science-nemotron-science/14799` | 306 |
| `milu:test:14642` | 2 | 0.087 | 4 / 46 | `sft-science-nemotron-science/65764` | 846 |
| `mmlu:test:7306` | 3 | 0.080 | 2 / 25 | `sft-science-nemotron-science/14799` | 306 |
| `mmlu:test:7348` | 3 | 0.080 | 2 / 25 | `sft-science-nemotron-science/14799` | 306 |
| `mmlu:test:7374` | 3 | 0.080 | 2 / 25 | `sft-science-nemotron-science/14799` | 306 |
| `milu:test:19498` | 1 | 0.068 | 4 / 59 | `sft-science-nemotron-science/33738` | 56350 |
| `milu:test:19813` | 1 | 0.067 | 4 / 60 | `sft-science-nemotron-science/33738` | 56350 |
| `milu:test:15172` | 1 | 0.063 | 4 / 63 | `sft-science-nemotron-science/104153` | 652 |
| `milu:test:20141` | 1 | 0.056 | 2 / 36 | `sft-science-nemotron-science/33738` | 56350 |
| `milu:test:20151` | 1 | 0.053 | 2 / 38 | `sft-science-nemotron-science/33738` | 56350 |
| `mmlu:test:7326` | 2 | 0.053 | 1 / 19 | `sft-science-nemotron-science/16853` | 2578 |
| `milu:test:10786` | 1 | 0.050 | 4 / 80 | `sft-science-nemotron-science/33738` | 56350 |

Coverage is the share of the item's runs found in the document. A value near 1.0 is a full copy; a low value is a short shared passage, for example a common problem statement. The ids above are enough to find the document in the set; the item text stays in Team 9's restricted folder.

## 5. Checks

| Check | Sets passed |
|---|---:|
| `canary_ids_in_input` | 16 of 16 |
| `canary_scan_complete` | 16 of 16 |
| `clean_file_flags_0` | 16 of 16 |
| `docs_match_checker` | 16 of 16 |
| `every_removed_row_is_hit` | 1 of 16 |
| `flagged_count_matches` | 16 of 16 |
| `flagged_ids_in_input` | 16 of 16 |
| `ids_unique` | 16 of 16 |
| `rows_in_eq_kept_plus_removed` | 16 of 16 |

`rows_in_eq_kept_plus_removed`: rows in = rows kept + rows removed. `clean_file_flags_0`: the checker, run again on the clean file, flags 0 of the kept rows. `canary_scan_complete`: `canary_scan.py` read every file (exit 0 or 1). A set with a failed check or a canary is not in this report (the script stops).

## 6. Inputs (to reproduce a run)

| Set | Input file | Bytes | sha256 |
|---|---|---:|---|
| `sft-agentic-nemotron-agentic-v1` | `agentic-nemotron-agentic-v1.jsonl` | 5,500,570,007 | `5cca4abb9ead609776b4b4f2df99c7d2a95d27f0dcca0137ec1504a57680d0ec` |
| `sft-bespoke-stratos-17k` | `bespoke-stratos-17k.jsonl` | 298,311,597 | `55f7d082ceb9a5df726a20f28b4bdecf07bc4c1b9471b264313f80adc48a2d74` |
| `sft-chat-nemotron-if-v1` | `chat-nemotron-if-v1.jsonl` | 95,149,354 | `1fdd7943eed071e4b0d942b987b1e87d63b8d16a65be5f36d81f99219681b12d` |
| `sft-code-codeforces-cots` | `code-codeforces-cots.jsonl` | 2,287,612,938 | `d3ef4f33f43f1d22c2912fe2de97951d3c44843e20994b9b24b711f635c0e2fa` |
| `sft-code-nemotron-cuda` | `code-nemotron-cuda.jsonl` | 82,578,942 | `af858d047eb12146110c7bb815e1814248faac6d439549d8482a8747bdcace6c` |
| `sft-code-nemotron-terminal` | `code-nemotron-terminal.jsonl` | 2,231,536,740 | `445c53c776d693214ab7fdf73e8ebdc1e17430a95584f1d3d8a57631226056f5` |
| `sft-code-swe-rebench-openhands` | `code-swe-rebench-openhands.jsonl` | 6,432,083,124 | `f2c910ec7ccda9fea8b26b58958a353336a3465e020f495f14d103d9d9319dda` |
| `sft-dolly-15k` | `dolly-15k.jsonl` | 15,465,770 | `f0e65f12ff0437552f9d8340c5244758ca233693c7c4c982480f3fcbfb50714a` |
| `sft-indic-aya-collection` | `indic-aya-collection.jsonl` | 2,668,534,387 | `be59e274c47778c906e0f5fa531ca5c8c195f29189ef8d09dd046d6beabae9eb` |
| `sft-indic-aya-dataset` | `indic-aya-dataset.jsonl` | 106,423,427 | `fbaf54e2913face83c7a9d1a25b87e086ce574b5debb840d2d159681b0bcb2ea` |
| `sft-indic-indic-align-dolly-t` | `indic-indic-align-dolly-t.jsonl` | 22,694,421 | `35980cee7f1d613dbc7814a7f7d0430c5c6bb98e3a7ecc0d01dcf41ae9f14e17` |
| `sft-math-nemotron-sft-math-v4` | `math-nemotron-sft-math-v4.jsonl` | 18,526,574,137 | `15cf1ff1cb0598540fc7d9f537400823ecdf3c2ee5a6572570989a8d59fff846` |
| `sft-oasst2` | `oasst2.jsonl` | 20,182,471 | `04ef702f982f8e289223e08b1e9350b111f0266a43c64a871965921c3185ee85` |
| `sft-science-glm51-phd` | `science-glm51-phd.jsonl` | 2,013,871,482 | `88165c31230c1a5efab08882c7c5160ebe032b7b0b1a7e500cbca1e3903aa387` |
| `sft-science-nemotron-science-v2` | `science-nemotron-science-v2.jsonl` | 571,034,022 | `ec5a5bf12503b7e798da641a895ccae1ade0ba3c0e9c31f22d9cf02473d5148b` |
| `sft-science-nemotron-science` | `science-nemotron-science.jsonl` | 1,808,296,419 | `339a9bdf19fc9fcc12124ed9c1ded743b22afe45c818249b028fe293c250ba95` |

```
python teams/10-post-training/sft/decontam_run.py --set <set-id> --input <set>.jsonl --out-dir decontam_out
python teams/10-post-training/sft/decontam_report.py --records decontam_out --out teams/10-post-training/sft/decontam_report.md --sets <set-id> ...
```

## 7. Sets not run yet

| Set | Why |
|---|---|
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | full run not done yet |
| `sft-chat-nemotron-if-v2` | full run not done yet |
| `sft-code-nemotron-cascade-swe` | full run not done yet |
| `sft-code-nemotron-opencode` | full run not done yet |
| `sft-code-opencodereasoning` | full run not done yet |
| `sft-code-opencodereasoning-2` | adapter and test written, but upstream withholds the question text ('-') in the python shard; needs a join with the source problem sets (taco, apps, code_contests) before it can be converted |
| `sft-code-swe-zero-openhands` | full run not done yet |
| `sft-math-nemotron-math-v2` | full run not done yet |
| `sft-math-nemotron-proofs` | full run not done yet |
| `sft-math-nemotron-proofs-v3-sft` | full run not done yet |
| `sft-math-openr1-math` | full run not done yet |
| `sft-math-openr1-math-raw` | full run not done yet |
| `sft-rl-math-openmathreasoning` | full run not done yet |
| `sft-safety-aegis-v1` | safety classification data (text plus labels, no assistant turn); no chat format applies, so no adapter |
| `sft-salesforce-xlam-60k` | gated on the Hub (needs a Hugging Face token with accepted terms); not downloaded |
| `sft-stem-code-openthoughts3` | full run not done yet |

## 8. What this check does not cover

- **Benchmarks outside the set.** This fingerprint set holds 20 benchmark entries: `aime_2024`, `aime_2025`, `bfcl_v3`, `codeforces`, `flores200`, `gaia`, `gpqa_diamond`, `gsm8k`, `heldout_g5_v1`, `hle`, `in22_conv`, `in22_gen`, `livecodebench`, `longbench_v2`, `milu`, `mmlu`, `swe_bench_live`, `swe_bench_pro`, `swe_bench_verified`, `terminal_bench_2`.
  It has no entry for HumanEval, HumanEval+, MBPP, MBPP+, ARC-Challenge, ARC-Easy, HellaSwag, TruthfulQA, MMLU-Pro, BBH, MuSR, Belebele, which Team 9's harnesses run (eval firewall, section 5, known gap), so a clean result says nothing about them.
  `sft_mix_proposal.md` section 1 lists HumanEval+ and MBPP+ among the benchmarks of this check; this set does not contain them.
- **Paraphrase.** The check finds copied runs of words. A reworded or translated item is not found.
- **Other rows of a set.** Only the rows that were run are covered. A set that was sampled (for example the first rows of a split) is not cleared as a whole.
- **Frozen tokenizer.** The check reads the rendered `text`, so it does not depend on the tokenizer. The effort tiers of the rows do, and Team 3 freezes the tokenizer on Sat 14 Nov.
- **A rerun is needed** when Team 9 publishes a new fingerprint set (a different set_sha256), and for any set whose rows change.

