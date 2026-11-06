# SFT decontamination report

Run for G10 on 2026-11-05 to 2026-11-06. Every set was checked against Team 9's benchmark fingerprints **v2** with the **full set** (no `--benchmarks`, `--tags` or `--exclude`), and scanned for canaries.

- **set_sha256:** `2826a3b883210c653979103c09ce1c79e40fc4f7034b54027f2836482370d22a`
- **Tools:** `teams/09-evaluation/decontam/decontam_check.py` and `canary_scan.py`, lab main `c6b0ce0961028020b3e3eaf86fe0c5873fca3bc0`. sha256 of the files used:
  - `canary_scan.py`: `322066d675e13af8bee0d05602f755f49e33da5a148bf664306ce6d6a9f908c2`
  - `decontam_check.py`: `62a269a25123543b5470c4956ba1be530ea257c597bc2be2eab19201cb62df8f`
  - `fpset.py`: `7f5f48d08506d619ebfadd2742e86d29ec3ea28e5fcfd729f13cd8d959689c59`
  - `lab_canary.py`: `373536a777c9f16367cf6affcc2cc6243755ac23e75850a2624eadf65918ea09`
  - `normalize.py`: `570dcb820ac2ae6c667b1abc5ea1d781a6795aa42a7735aa94377e756d7d70e9`
- **Runner and reconciliation:** `sft/decontam_run.py`; this file is written by `sft/decontam_report.py`.
- **Sets run:** 29. **Rows in:** 124,639. **Removed (flagged or canary):** 3,586 (2.88%). **Kept:** 121,053.
- No benchmark item text is in this file or in the run records: only set names, counts, document ids, benchmark item ids, offsets and sha256 values.

## 1. Result per set

| Set | Rows in | Flagged | Canary | Removed | Rows kept | Clean file sha256 |
|---|---:|---:|---:|---:|---:|---|
| `sft-agentic-nemotron-agentic-v1` | 4,993 | 8 | 0 | 8 (0.16%) | 4,985 | `2818537e669d…` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | 5,000 | 31 | 0 | 31 (0.62%) | 4,969 | `d20e3bd54d43…` |
| `sft-bespoke-stratos-17k` | 3,000 | 63 | 0 | 63 (2.10%) | 2,937 | `e32b7bed3d8b…` |
| `sft-chat-nemotron-if-v1` | 4,963 | 1 | 0 | 1 (0.02%) | 4,962 | `38e757a1a7f8…` |
| `sft-chat-nemotron-if-v2` | 4,997 | 35 | 0 | 35 (0.70%) | 4,962 | `cbc44921ee98…` |
| `sft-code-codeforces-cots` | 972 | 496 | 0 | 496 (51.03%) | 476 | `ff74435ced50…` |
| `sft-code-nemotron-cascade-swe` | 4,987 | 467 | 0 | 467 (9.36%) | 4,520 | `cc8a57ec99fd…` |
| `sft-code-nemotron-cuda` | 2,273 | 2 | 0 | 2 (0.09%) | 2,271 | `f451b673db79…` |
| `sft-code-nemotron-opencode` | 3,000 | 22 | 0 | 22 (0.73%) | 2,978 | `7fdabc9302a1…` |
| `sft-code-nemotron-terminal` | 3,000 | 890 | 0 | 890 (29.67%) | 2,110 | `9217e8595509…` |
| `sft-code-opencodereasoning` | 5,000 | 921 | 0 | 921 (18.42%) | 4,079 | `c6b6a9e4a464…` |
| `sft-code-swe-rebench-openhands` | 442 | 71 | 0 | 71 (16.06%) | 371 | `2a16677599f0…` |
| `sft-code-swe-zero-openhands` | 2,990 | 130 | 0 | 130 (4.35%) | 2,860 | `c26e8f4e4b4a…` |
| `sft-dolly-15k` | 5,000 | 1 | 0 | 1 (0.02%) | 4,999 | `ca33081b26c1…` |
| `sft-indic-aya-collection` | 19,416 | 0 | 0 | 0 (0.00%) | 19,416 | `1bd9cbaeb932…` |
| `sft-indic-aya-dataset` | 1,000 | 0 | 0 | 0 (0.00%) | 1,000 | `df0c80c61c55…` |
| `sft-indic-indic-align-dolly-t` | 3,000 | 0 | 0 | 0 (0.00%) | 3,000 | `3fbb277b99a1…` |
| `sft-math-nemotron-math-v2` | 4,976 | 40 | 0 | 40 (0.80%) | 4,936 | `d61e2d04386a…` |
| `sft-math-nemotron-proofs-v3-sft` | 116 | 2 | 0 | 2 (1.72%) | 114 | `b736c5028194…` |
| `sft-math-nemotron-proofs` | 3,351 | 6 | 0 | 6 (0.18%) | 3,345 | `4cca5dd84294…` |
| `sft-math-nemotron-sft-math-v4` | 4,866 | 51 | 0 | 51 (1.05%) | 4,815 | `1dd5a5d178b4…` |
| `sft-math-openr1-math-raw` | 5,000 | 48 | 0 | 48 (0.96%) | 4,952 | `dbeb9613c3d9…` |
| `sft-math-openr1-math` | 4,988 | 67 | 0 | 67 (1.34%) | 4,921 | `ffc9199c33fd…` |
| `sft-oasst2` | 9,548 | 5 | 0 | 5 (0.05%) | 9,543 | `c89de79a902a…` |
| `sft-rl-math-openmathreasoning` | 5,000 | 115 | 0 | 115 (2.30%) | 4,885 | `b93ea06aede4…` |
| `sft-science-glm51-phd` | 3,000 | 2 | 0 | 2 (0.07%) | 2,998 | `44ec25d7936e…` |
| `sft-science-nemotron-science-v2` | 3,000 | 6 | 0 | 6 (0.20%) | 2,994 | `4f3609eb9849…` |
| `sft-science-nemotron-science` | 5,000 | 23 | 0 | 23 (0.46%) | 4,977 | `ceca90f6057a…` |
| `sft-stem-code-openthoughts3` | 1,761 | 83 | 0 | 83 (4.71%) | 1,678 | `97435a5623d3…` |
| **Total** | **124,639** | **3,586** | **0** | **3,586** (2.88%) | **121,053** | |

A row that is both flagged and carries a canary counts once in Removed.

## 2. Flagged documents by benchmark

| Set | `aime_2024` | `aime_2025` | `bfcl_v3` | `codeforces` | `gaia` | `gpqa_diamond` | `gsm8k` | `heldout_g5_v1` | `hle` | `livecodebench` | `milu` | `mmlu` | `swe_bench_live` | `swe_bench_pro` | `swe_bench_verified` | `terminal_bench_2` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 0 | 0 | 0 |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 1 | 0 | 16 | 0 | 1 | 1 |
| `sft-bespoke-stratos-17k` | 29 | 22 | 0 | 1 | 0 | 1 | 0 | 0 | 19 | 5 | 2 | 6 | 0 | 0 | 0 | 0 |
| `sft-chat-nemotron-if-v1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| `sft-chat-nemotron-if-v2` | 2 | 1 | 2 | 0 | 0 | 0 | 3 | 0 | 2 | 3 | 0 | 12 | 10 | 0 | 0 | 0 |
| `sft-code-codeforces-cots` | 0 | 0 | 0 | 451 | 0 | 0 | 0 | 0 | 40 | 281 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-code-nemotron-cascade-swe` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 358 | 80 | 108 | 0 |
| `sft-code-nemotron-cuda` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-code-nemotron-opencode` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0 | 0 |
| `sft-code-nemotron-terminal` | 0 | 0 | 0 | 718 | 1 | 0 | 0 | 1 | 15 | 506 | 0 | 0 | 1 | 0 | 0 | 0 |
| `sft-code-opencodereasoning` | 0 | 0 | 0 | 438 | 1 | 0 | 0 | 0 | 17 | 629 | 0 | 0 | 0 | 1 | 0 | 0 |
| `sft-code-swe-rebench-openhands` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 64 | 0 | 17 | 0 |
| `sft-code-swe-zero-openhands` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 116 | 1 | 38 | 0 |
| `sft-dolly-15k` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| `sft-indic-aya-collection` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-indic-aya-dataset` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-math-v2` | 12 | 15 | 0 | 7 | 0 | 0 | 0 | 1 | 8 | 5 | 0 | 1 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-proofs-v3-sft` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-proofs` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-sft-math-v4` | 11 | 13 | 0 | 2 | 0 | 0 | 0 | 0 | 25 | 7 | 1 | 1 | 0 | 0 | 0 | 0 |
| `sft-math-openr1-math-raw` | 1 | 0 | 0 | 10 | 0 | 1 | 0 | 0 | 34 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-openr1-math` | 13 | 12 | 1 | 4 | 0 | 2 | 0 | 0 | 34 | 8 | 0 | 2 | 0 | 0 | 0 | 0 |
| `sft-oasst2` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| `sft-rl-math-openmathreasoning` | 28 | 22 | 0 | 7 | 0 | 2 | 0 | 1 | 68 | 6 | 0 | 2 | 0 | 0 | 0 | 0 |
| `sft-science-glm51-phd` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-science-nemotron-science-v2` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 2 | 0 | 0 | 0 |
| `sft-science-nemotron-science` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 5 | 5 | 0 | 0 | 0 | 0 |
| `sft-stem-code-openthoughts3` | 0 | 0 | 0 | 73 | 0 | 0 | 0 | 0 | 6 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |

A document is flagged when it shares at least one 13-word run (20 tokens for code) with a benchmark item. The whole document is removed. The count is documents per benchmark, so a document that matches two benchmarks counts in both columns.

## 3. Flagged documents by coverage

Coverage is the share of one benchmark item's runs that the document contains (the highest over its hits). The bands are for reading the result; every flagged document is removed whatever its band.

| Set | Flagged | Coverage 0.5 or more | 0.1 to 0.5 | Below 0.1 |
|---|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 8 | 0 | 1 | 7 |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | 31 | 0 | 7 | 24 |
| `sft-bespoke-stratos-17k` | 63 | 0 | 5 | 58 |
| `sft-chat-nemotron-if-v1` | 1 | 0 | 1 | 0 |
| `sft-chat-nemotron-if-v2` | 35 | 8 | 5 | 22 |
| `sft-code-codeforces-cots` | 496 | 0 | 32 | 464 |
| `sft-code-nemotron-cascade-swe` | 467 | 8 | 32 | 427 |
| `sft-code-nemotron-cuda` | 2 | 0 | 0 | 2 |
| `sft-code-nemotron-opencode` | 22 | 0 | 0 | 22 |
| `sft-code-nemotron-terminal` | 890 | 37 | 36 | 817 |
| `sft-code-opencodereasoning` | 921 | 0 | 5 | 916 |
| `sft-code-swe-rebench-openhands` | 71 | 2 | 4 | 65 |
| `sft-code-swe-zero-openhands` | 130 | 1 | 14 | 115 |
| `sft-dolly-15k` | 1 | 0 | 0 | 1 |
| `sft-indic-aya-collection` | 0 | 0 | 0 | 0 |
| `sft-indic-aya-dataset` | 0 | 0 | 0 | 0 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-math-v2` | 40 | 0 | 0 | 40 |
| `sft-math-nemotron-proofs-v3-sft` | 2 | 0 | 0 | 2 |
| `sft-math-nemotron-proofs` | 6 | 0 | 0 | 6 |
| `sft-math-nemotron-sft-math-v4` | 51 | 0 | 3 | 48 |
| `sft-math-openr1-math-raw` | 48 | 0 | 0 | 48 |
| `sft-math-openr1-math` | 67 | 0 | 2 | 65 |
| `sft-oasst2` | 5 | 0 | 3 | 2 |
| `sft-rl-math-openmathreasoning` | 115 | 1 | 3 | 111 |
| `sft-science-glm51-phd` | 2 | 0 | 0 | 2 |
| `sft-science-nemotron-science-v2` | 6 | 0 | 0 | 6 |
| `sft-science-nemotron-science` | 23 | 0 | 0 | 23 |
| `sft-stem-code-openthoughts3` | 83 | 0 | 0 | 83 |

## 4. Benchmark items with the largest overlap

**`sft-agentic-nemotron-agentic-v1`**: at least 2 different benchmark items found in 8 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:12344` | 1 | 0.289 | 11 / 38 | `sft-agentic-nemotron-agentic-v1/4106` | 7675 |
| `swe_bench_live:test:streamlink__streamlink-6111` | 7 | 0.014 | 4 / 290 | `sft-agentic-nemotron-agentic-v1/256` | 755 |

**`sft-agentic-nemotron-sft-agentic-v2-tool-calling`**: at least 13 different benchmark items found in 31 documents (top 13 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `livecodebench:release_v6:3748` | 2 | 0.307 | 59 / 192 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/788` | 12320 |
| `livecodebench:release_v6:3461` | 4 | 0.300 | 36 / 120 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/4177` | 15845 |
| `bfcl_v3:test:simple_98` | 1 | 0.167 | 1 / 6 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/3610` | 1060 |
| `milu:test:18206` | 1 | 0.113 | 6 / 53 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/21` | 11253 |
| `livecodebench:release_v6:3733` | 2 | 0.098 | 29 / 295 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/2813` | 10370 |
| `livecodebench:release_v6:3372` | 1 | 0.092 | 14 / 152 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/595` | 16495 |
| `livecodebench:release_v6:3018` | 1 | 0.026 | 6 / 233 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/1482` | 37301 |
| `bfcl_v3:test:parallel_multiple_158` | 1 | 0.025 | 3 / 118 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/2100` | 1112 |
| `terminal_bench_2:test:sparql-university` | 1 | 0.022 | 8 / 356 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/2717` | 93677 |
| `swe_bench_live:test:streamlink__streamlink-6111` | 1 | 0.014 | 4 / 290 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/3997` | 1195 |
| `livecodebench:release_v6:3492` | 1 | 0.012 | 1 / 85 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/4752` | 28250 |
| `swe_bench_live:test:run-llama__llama_deploy-500` | 15 | 0.005 | 2 / 410 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/672` | 13685 |
| `swe_bench_verified:test:django__django-16502` | 1 | 0.002 | 1 / 616 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/3297` | 7629 |

**`sft-bespoke-stratos-17k`**: at least 43 different benchmark items found in 63 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4273` | 1 | 0.417 | 20 / 48 | `sft-bespoke-stratos-17k/2998` | 111 |
| `aime_2025:test:7` | 16 | 0.152 | 7 / 46 | `sft-bespoke-stratos-17k/706` | 189 |
| `mmlu:test:4258` | 1 | 0.130 | 3 / 23 | `sft-bespoke-stratos-17k/2146` | 154 |
| `milu:test:17755` | 1 | 0.123 | 8 / 65 | `sft-bespoke-stratos-17k/745` | 5544 |
| `aime_2025:test:21` | 16 | 0.087 | 4 / 46 | `sft-bespoke-stratos-17k/627` | 478 |
| `mmlu:test:1198` | 1 | 0.062 | 2 / 32 | `sft-bespoke-stratos-17k/2668` | 6700 |
| `mmlu:test:2862` | 1 | 0.059 | 1 / 17 | `sft-bespoke-stratos-17k/2668` | 6700 |
| `mmlu:test:4520` | 1 | 0.057 | 2 / 35 | `sft-bespoke-stratos-17k/2668` | 6700 |
| `mmlu:test:912` | 1 | 0.054 | 2 / 37 | `sft-bespoke-stratos-17k/2668` | 6700 |
| `aime_2025:test:6` | 16 | 0.051 | 4 / 78 | `sft-bespoke-stratos-17k/627` | 478 |
| `aime_2025:test:18` | 15 | 0.045 | 3 / 66 | `sft-bespoke-stratos-17k/627` | 483 |
| `mmlu:test:980` | 1 | 0.045 | 2 / 44 | `sft-bespoke-stratos-17k/2668` | 6700 |
| `aime_2025:test:8` | 2 | 0.043 | 2 / 47 | `sft-bespoke-stratos-17k/2114` | 441 |
| `mmlu:test:1121` | 1 | 0.041 | 4 / 97 | `sft-bespoke-stratos-17k/745` | 5544 |
| `mmlu:test:5639` | 1 | 0.039 | 5 / 129 | `sft-bespoke-stratos-17k/745` | 5544 |

**`sft-chat-nemotron-if-v1`**: at least 1 different benchmark items found in 1 documents (top 1 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:12344` | 1 | 0.289 | 11 / 38 | `sft-chat-nemotron-if-v1/3111` | 7832 |

**`sft-chat-nemotron-if-v2`**: at least 29 different benchmark items found in 35 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4279` | 1 | 0.855 | 71 / 83 | `sft-chat-nemotron-if-v2/1674` | 77 |
| `mmlu:test:4460` | 1 | 0.676 | 25 / 37 | `sft-chat-nemotron-if-v2/2730` | 328 |
| `mmlu:test:4261` | 1 | 0.657 | 23 / 35 | `sft-chat-nemotron-if-v2/4227` | 243 |
| `mmlu:test:4489` | 1 | 0.647 | 22 / 34 | `sft-chat-nemotron-if-v2/2151` | 171 |
| `mmlu:test:718` | 1 | 0.613 | 19 / 31 | `sft-chat-nemotron-if-v2/820` | 77 |
| `mmlu:test:4447` | 1 | 0.593 | 16 / 27 | `sft-chat-nemotron-if-v2/1643` | 676 |
| `mmlu:test:4352` | 1 | 0.588 | 40 / 68 | `sft-chat-nemotron-if-v2/1761` | 67 |
| `mmlu:test:3329` | 1 | 0.539 | 248 / 460 | `sft-chat-nemotron-if-v2/1263` | 77 |
| `gsm8k:test:258` | 1 | 0.304 | 31 / 102 | `sft-chat-nemotron-if-v2/248` | 77 |
| `gsm8k:test:340` | 1 | 0.262 | 39 / 149 | `sft-chat-nemotron-if-v2/2903` | 2302 |
| `bfcl_v3:test:live_multiple_189-83-0` | 1 | 0.185 | 12 / 65 | `sft-chat-nemotron-if-v2/2300` | 67 |
| `gsm8k:test:1172` | 1 | 0.157 | 34 / 217 | `sft-chat-nemotron-if-v2/985` | 74 |
| `mmlu:test:4430` | 1 | 0.121 | 4 / 33 | `sft-chat-nemotron-if-v2/3885` | 278 |
| `bfcl_v3:test:live_irrelevance_302-76-0` | 1 | 0.051 | 4 / 78 | `sft-chat-nemotron-if-v2/37` | 441 |
| `bfcl_v3:test:live_irrelevance_368-81-29` | 1 | 0.030 | 4 / 133 | `sft-chat-nemotron-if-v2/37` | 441 |

**`sft-code-codeforces-cots`**: at least 191 different benchmark items found in 496 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `codeforces:test:2018/B` | 102 | 0.152 | 32 / 210 | `sft-code-codeforces-cots/190` | 1226 |
| `codeforces:test:2060/D` | 50 | 0.150 | 32 / 214 | `sft-code-codeforces-cots/190` | 1226 |
| `codeforces:test:2056/D` | 54 | 0.136 | 37 / 273 | `sft-code-codeforces-cots/190` | 1226 |
| `codeforces:test:2010/A` | 64 | 0.113 | 12 / 106 | `sft-code-codeforces-cots/775` | 1245 |
| `codeforces:test:2065/C1` | 30 | 0.107 | 33 / 307 | `sft-code-codeforces-cots/265` | 1455 |
| `codeforces:test:2013/E` | 5 | 0.106 | 27 / 254 | `sft-code-codeforces-cots/785` | 1345 |
| `codeforces:test:2049/B` | 4 | 0.105 | 33 / 313 | `sft-code-codeforces-cots/320` | 1495 |
| `codeforces:test:2018/D` | 23 | 0.104 | 34 / 328 | `sft-code-codeforces-cots/190` | 1226 |
| `codeforces:test:2018/C` | 10 | 0.103 | 28 / 271 | `sft-code-codeforces-cots/785` | 1345 |
| `codeforces:test:2065/C2` | 20 | 0.101 | 33 / 326 | `sft-code-codeforces-cots/265` | 1455 |
| `codeforces:test:2019/A` | 24 | 0.099 | 28 / 284 | `sft-code-codeforces-cots/190` | 1226 |
| `codeforces:test:2038/B` | 116 | 0.096 | 17 / 178 | `sft-code-codeforces-cots/135` | 2131 |
| `codeforces:test:2022/B` | 10 | 0.085 | 22 / 259 | `sft-code-codeforces-cots/495` | 2212 |
| `codeforces:test:1993/B` | 59 | 0.084 | 23 / 274 | `sft-code-codeforces-cots/670` | 1763 |
| `codeforces:test:2031/B` | 4 | 0.082 | 34 / 417 | `sft-code-codeforces-cots/320` | 1495 |

**`sft-code-nemotron-cascade-swe`**: at least 237 different benchmark items found in 467 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:conan-io__conan-15699` | 1 | 1.000 | 238 / 238 | `sft-code-nemotron-cascade-swe/1423` | 180 |
| `swe_bench_live:test:conan-io__conan-15931` | 2 | 1.000 | 49 / 49 | `sft-code-nemotron-cascade-swe/3235` | 180 |
| `swe_bench_live:test:streamlink__streamlink-6242` | 6 | 0.924 | 171 / 185 | `sft-code-nemotron-cascade-swe/310` | 179 |
| `swe_bench_live:test:streamlink__streamlink-6353` | 5 | 0.904 | 311 / 344 | `sft-code-nemotron-cascade-swe/3763` | 179 |
| `swe_bench_live:test:streamlink__streamlink-6207` | 1 | 0.866 | 629 / 726 | `sft-code-nemotron-cascade-swe/595` | 179 |
| `swe_bench_live:test:streamlink__streamlink-5844` | 1 | 0.830 | 597 / 719 | `sft-code-nemotron-cascade-swe/1030` | 179 |
| `swe_bench_live:test:beeware__briefcase-2075` | 1 | 0.826 | 371 / 449 | `sft-code-nemotron-cascade-swe/389` | 179 |
| `swe_bench_live:test:stanfordnlp__dspy-1472` | 1 | 0.439 | 190 / 433 | `sft-code-nemotron-cascade-swe/2437` | 2667 |
| `swe_bench_live:test:privacyidea__privacyidea-4247` | 1 | 0.357 | 503 / 1408 | `sft-code-nemotron-cascade-swe/1573` | 15215 |
| `swe_bench_live:test:deepset-ai__haystack-6973` | 1 | 0.335 | 560 / 1670 | `sft-code-nemotron-cascade-swe/1773` | 9035 |
| `swe_bench_live:test:streamlink__streamlink-6361` | 3 | 0.325 | 105 / 323 | `sft-code-nemotron-cascade-swe/595` | 290 |
| `swe_bench_live:test:streamlink__streamlink-6389` | 3 | 0.316 | 112 / 354 | `sft-code-nemotron-cascade-swe/310` | 265 |
| `swe_bench_live:test:streamlink__streamlink-6085` | 1 | 0.314 | 133 / 424 | `sft-code-nemotron-cascade-swe/3763` | 269 |
| `swe_bench_live:test:streamlink__streamlink-5858` | 3 | 0.304 | 80 / 263 | `sft-code-nemotron-cascade-swe/310` | 265 |
| `swe_bench_live:test:streamlink__streamlink-6420` | 3 | 0.304 | 112 / 369 | `sft-code-nemotron-cascade-swe/310` | 265 |

**`sft-code-nemotron-cuda`**: at least 2 different benchmark items found in 2 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:6726c7e9d2ad475e400669c7` | 1 | 0.002 | 1 / 635 | `sft-code-nemotron-cuda/952` | 30663 |
| `codeforces:test:2055/C` | 1 | 0.001 | 1 / 885 | `sft-code-nemotron-cuda/272` | 15733 |

**`sft-code-nemotron-opencode`**: at least 2 different benchmark items found in 22 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:streamlink__streamlink-6111` | 21 | 0.014 | 4 / 290 | `sft-code-nemotron-opencode/388` | 55945 |
| `swe_bench_live:test:kozea__weasyprint-2326` | 1 | 0.002 | 1 / 545 | `sft-code-nemotron-opencode/2007` | 103975 |

**`sft-code-nemotron-terminal`**: at least 631 different benchmark items found in 890 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `codeforces:test:2053/D` | 8 | 0.975 | 584 / 599 | `sft-code-nemotron-terminal/1107` | 2924 |
| `codeforces:test:2037/D` | 1 | 0.972 | 486 / 500 | `sft-code-nemotron-terminal/1247` | 2924 |
| `codeforces:test:2022/E1` | 2 | 0.966 | 451 / 467 | `sft-code-nemotron-terminal/2032` | 2924 |
| `codeforces:test:2005/E1` | 1 | 0.965 | 446 / 462 | `sft-code-nemotron-terminal/134` | 2924 |
| `codeforces:test:2046/E1` | 3 | 0.964 | 480 / 498 | `sft-code-nemotron-terminal/568` | 2924 |
| `codeforces:test:2060/B` | 1 | 0.963 | 437 / 454 | `sft-code-nemotron-terminal/602` | 2924 |
| `codeforces:test:2060/E` | 1 | 0.963 | 360 / 374 | `sft-code-nemotron-terminal/1974` | 2924 |
| `codeforces:test:2021/E1` | 3 | 0.962 | 403 / 419 | `sft-code-nemotron-terminal/1002` | 2924 |
| `codeforces:test:2056/B` | 1 | 0.962 | 375 / 390 | `sft-code-nemotron-terminal/1717` | 2924 |
| `codeforces:test:2014/H` | 8 | 0.961 | 371 / 386 | `sft-code-nemotron-terminal/1036` | 2924 |
| `codeforces:test:1993/F2` | 11 | 0.959 | 399 / 416 | `sft-code-nemotron-terminal/2495` | 2924 |
| `codeforces:test:2061/H1` | 10 | 0.956 | 369 / 386 | `sft-code-nemotron-terminal/1810` | 2924 |
| `codeforces:test:2010/C1` | 2 | 0.946 | 300 / 317 | `sft-code-nemotron-terminal/1405` | 2924 |
| `codeforces:test:1993/B` | 69 | 0.945 | 259 / 274 | `sft-code-nemotron-terminal/157` | 2924 |
| `livecodebench:release_v6:1899_D` | 30 | 0.945 | 380 / 402 | `sft-code-nemotron-terminal/1303` | 2924 |

**`sft-code-opencodereasoning`**: at least 654 different benchmark items found in 921 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:672f72e3609b665328565e6b` | 1 | 0.238 | 125 / 526 | `sft-code-opencodereasoning/103` | 67 |
| `hle:test:673627bc10ec0a5f859365ce` | 1 | 0.188 | 69 / 368 | `sft-code-opencodereasoning/801` | 928 |
| `hle:test:67373220a4d09488d430f640` | 1 | 0.185 | 69 / 373 | `sft-code-opencodereasoning/801` | 928 |
| `hle:test:672e24f117ed86a6ef9def55` | 1 | 0.183 | 72 / 393 | `sft-code-opencodereasoning/2086` | 67 |
| `hle:test:66f28a89f1256af80477e15d` | 1 | 0.136 | 100 / 733 | `sft-code-opencodereasoning/2888` | 67 |
| `gaia:2023:2b3ef98c-cc05-450b-a719-711aee40ac65` | 1 | 0.110 | 13 / 118 | `sft-code-opencodereasoning/2300` | 1894 |
| `codeforces:test:2023/A` | 5 | 0.099 | 56 / 565 | `sft-code-opencodereasoning/4540` | 67 |
| `livecodebench:release_v6:abc348_e` | 12 | 0.093 | 24 / 259 | `sft-code-opencodereasoning/3607` | 76 |
| `livecodebench:release_v6:abc350_d` | 13 | 0.091 | 26 / 286 | `sft-code-opencodereasoning/3084` | 563 |
| `livecodebench:release_v6:abc394_f` | 9 | 0.088 | 23 / 261 | `sft-code-opencodereasoning/3607` | 695 |
| `codeforces:test:2018/B` | 78 | 0.086 | 18 / 210 | `sft-code-opencodereasoning/1915` | 1118 |
| `livecodebench:release_v6:abc320_a` | 28 | 0.084 | 7 / 83 | `sft-code-opencodereasoning/3684` | 290 |
| `livecodebench:release_v6:abc378_f` | 3 | 0.084 | 17 / 202 | `sft-code-opencodereasoning/3311` | 578 |
| `livecodebench:release_v6:abc383_d` | 43 | 0.083 | 5 / 60 | `sft-code-opencodereasoning/2544` | 392 |
| `livecodebench:release_v6:abc399_f` | 17 | 0.076 | 11 / 145 | `sft-code-opencodereasoning/2769` | 479 |

**`sft-code-swe-rebench-openhands`**: at least 49 different benchmark items found in 71 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:streamlink__streamlink-6242` | 1 | 0.924 | 171 / 185 | `sft-code-swe-rebench-openhands/92` | 27523 |
| `swe_bench_live:test:beeware__briefcase-1638` | 1 | 0.920 | 103 / 112 | `sft-code-swe-rebench-openhands/257` | 27514 |
| `swe_bench_live:test:streamlink__streamlink-6353` | 1 | 0.326 | 112 / 344 | `sft-code-swe-rebench-openhands/92` | 27609 |
| `swe_bench_live:test:streamlink__streamlink-6389` | 1 | 0.316 | 112 / 354 | `sft-code-swe-rebench-openhands/92` | 27609 |
| `swe_bench_live:test:streamlink__streamlink-5858` | 1 | 0.304 | 80 / 263 | `sft-code-swe-rebench-openhands/92` | 27609 |
| `swe_bench_live:test:streamlink__streamlink-6420` | 1 | 0.304 | 112 / 369 | `sft-code-swe-rebench-openhands/92` | 27609 |
| `swe_bench_live:test:python-pillow__Pillow-9105` | 2 | 0.192 | 68 / 354 | `sft-code-swe-rebench-openhands/487` | 27590 |
| `swe_bench_live:test:joke2k__faker-2155` | 1 | 0.164 | 69 / 422 | `sft-code-swe-rebench-openhands/310` | 27505 |
| `swe_bench_live:test:beeware__briefcase-1598` | 2 | 0.117 | 109 / 928 | `sft-code-swe-rebench-openhands/257` | 129123 |
| `swe_bench_live:test:encode__starlette-2711` | 1 | 0.114 | 28 / 246 | `sft-code-swe-rebench-openhands/183` | 30233 |
| `swe_bench_live:test:deepset-ai__haystack-8969` | 1 | 0.076 | 10 / 131 | `sft-code-swe-rebench-openhands/581` | 31001 |
| `swe_bench_live:test:encode__starlette-2812` | 1 | 0.075 | 28 / 372 | `sft-code-swe-rebench-openhands/183` | 30233 |
| `swe_bench_verified:test:django__django-14238` | 11 | 0.072 | 28 / 389 | `sft-code-swe-rebench-openhands/257` | 41676 |
| `swe_bench_live:test:deepset-ai__haystack-7681` | 1 | 0.048 | 10 / 209 | `sft-code-swe-rebench-openhands/581` | 31001 |
| `swe_bench_live:test:deepset-ai__haystack-9227` | 1 | 0.043 | 7 / 161 | `sft-code-swe-rebench-openhands/581` | 31022 |

**`sft-code-swe-zero-openhands`**: at least 64 different benchmark items found in 130 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:keras-team__keras-19284` | 1 | 0.733 | 203 / 277 | `sft-code-swe-zero-openhands/2919` | 6755 |
| `swe_bench_live:test:celery__celery-9806` | 14 | 0.335 | 628 / 1876 | `sft-code-swe-zero-openhands/1180` | 6843 |
| `swe_bench_live:test:sphinx-doc__sphinx-11879` | 10 | 0.124 | 20 / 161 | `sft-code-swe-zero-openhands/45` | 10366 |
| `swe_bench_live:test:networkx__networkx-8013` | 7 | 0.122 | 23 / 188 | `sft-code-swe-zero-openhands/2578` | 6825 |
| `swe_bench_verified:test:sphinx-doc__sphinx-10449` | 4 | 0.086 | 49 / 570 | `sft-code-swe-zero-openhands/1193` | 53687 |
| `swe_bench_live:test:vacanza__holidays-2780` | 10 | 0.075 | 27 / 359 | `sft-code-swe-zero-openhands/587` | 6828 |
| `swe_bench_live:test:instructlab__instructlab-3060` | 15 | 0.056 | 44 / 786 | `sft-code-swe-zero-openhands/2051` | 6853 |
| `swe_bench_verified:test:django__django-14238` | 4 | 0.049 | 19 / 389 | `sft-code-swe-zero-openhands/504` | 7320 |
| `swe_bench_live:test:django-json-api__django-rest-framework-json-api-1301` | 13 | 0.041 | 12 / 294 | `sft-code-swe-zero-openhands/413` | 7223 |
| `swe_bench_live:test:instructlab__instructlab-3125` | 6 | 0.038 | 20 / 528 | `sft-code-swe-zero-openhands/587` | 6828 |
| `swe_bench_live:test:deepset-ai__haystack-9322` | 9 | 0.032 | 20 / 629 | `sft-code-swe-zero-openhands/45` | 10366 |
| `swe_bench_live:test:run-llama__llama_deploy-384` | 1 | 0.030 | 12 / 394 | `sft-code-swe-zero-openhands/1721` | 7515 |
| `swe_bench_live:test:astronomer__dag-factory-544` | 1 | 0.029 | 13 / 448 | `sft-code-swe-zero-openhands/1215` | 13373 |
| `swe_bench_live:test:google__adk-python-1305` | 12 | 0.029 | 25 / 869 | `sft-code-swe-zero-openhands/2051` | 6853 |
| `swe_bench_live:test:matplotlib__matplotlib-29719` | 1 | 0.024 | 19 / 800 | `sft-code-swe-zero-openhands/543` | 7185 |

**`sft-dolly-15k`**: at least 1 different benchmark items found in 1 documents (top 1 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:5399` | 1 | 0.071 | 4 / 56 | `sft-dolly-15k/903` | 4290 |

**`sft-math-nemotron-math-v2`**: at least 39 different benchmark items found in 40 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `aime_2025:test:21` | 6 | 0.087 | 4 / 46 | `sft-math-nemotron-math-v2/3794` | 432 |
| `aime_2025:test:7` | 6 | 0.087 | 4 / 46 | `sft-math-nemotron-math-v2/1210` | 397 |
| `aime_2025:test:13` | 1 | 0.062 | 4 / 65 | `sft-math-nemotron-math-v2/1892` | 617 |
| `aime_2025:test:27` | 2 | 0.059 | 3 / 51 | `sft-math-nemotron-math-v2/1520` | 487 |
| `aime_2025:test:6` | 6 | 0.051 | 4 / 78 | `sft-math-nemotron-math-v2/3794` | 432 |
| `aime_2025:test:18` | 6 | 0.045 | 3 / 66 | `sft-math-nemotron-math-v2/1210` | 404 |
| `aime_2025:test:20` | 6 | 0.038 | 4 / 104 | `sft-math-nemotron-math-v2/3794` | 432 |
| `aime_2025:test:11` | 2 | 0.030 | 2 / 67 | `sft-math-nemotron-math-v2/935` | 451 |
| `aime_2025:test:10` | 4 | 0.027 | 3 / 111 | `sft-math-nemotron-math-v2/1391` | 496 |
| `mmlu:test:922` | 1 | 0.023 | 2 / 86 | `sft-math-nemotron-math-v2/3405` | 546 |
| `aime_2025:test:8` | 2 | 0.021 | 1 / 47 | `sft-math-nemotron-math-v2/151` | 316 |
| `codeforces:test:2041/H` | 3 | 0.014 | 4 / 287 | `sft-math-nemotron-math-v2/1089` | 284 |
| `livecodebench:release_v6:abc373_c` | 1 | 0.013 | 2 / 156 | `sft-math-nemotron-math-v2/4580` | 29403 |
| `codeforces:test:2005/A` | 1 | 0.012 | 4 / 331 | `sft-math-nemotron-math-v2/2613` | 21944 |
| `hle:test:66f1d9a589b78acd31812b99` | 1 | 0.010 | 1 / 104 | `sft-math-nemotron-math-v2/1475` | 1388 |

**`sft-math-nemotron-proofs-v3-sft`**: at least 2 different benchmark items found in 2 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `aime_2024:test:77` | 1 | 0.001 | 1 / 807 | `sft-math-nemotron-proofs-v3-sft/103` | 48629 |
| `hle:test:67073a60c033e34a5d675f2e` | 1 | 0.001 | 3 / 2027 | `sft-math-nemotron-proofs-v3-sft/42` | 215089 |

**`sft-math-nemotron-proofs`**: at least 2 different benchmark items found in 6 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:673d70ca1b7b41a118b4b786` | 3 | 0.004 | 1 / 246 | `sft-math-nemotron-proofs/34` | 15669 |
| `hle:test:67073a60c033e34a5d675f2e` | 3 | 0.002 | 5 / 2027 | `sft-math-nemotron-proofs/4404` | 11232 |

**`sft-math-nemotron-sft-math-v4`**: at least 55 different benchmark items found in 51 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `aime_2025:test:11` | 3 | 0.164 | 11 / 67 | `sft-math-nemotron-sft-math-v4/1867` | 464 |
| `mmlu:test:4977` | 1 | 0.105 | 2 / 19 | `sft-math-nemotron-sft-math-v4/4383` | 9178 |
| `aime_2025:test:21` | 5 | 0.087 | 4 / 46 | `sft-math-nemotron-sft-math-v4/2337` | 331 |
| `aime_2025:test:7` | 5 | 0.087 | 4 / 46 | `sft-math-nemotron-sft-math-v4/2875` | 396 |
| `milu:test:14412` | 1 | 0.067 | 3 / 45 | `sft-math-nemotron-sft-math-v4/2700` | 13980 |
| `aime_2025:test:13` | 1 | 0.062 | 4 / 65 | `sft-math-nemotron-sft-math-v4/3901` | 519 |
| `hle:test:672065bcff30e78ae646b59c` | 1 | 0.061 | 16 / 264 | `sft-math-nemotron-sft-math-v4/4728` | 67 |
| `aime_2025:test:27` | 2 | 0.059 | 3 / 51 | `sft-math-nemotron-sft-math-v4/2289` | 377 |
| `aime_2025:test:6` | 5 | 0.051 | 4 / 78 | `sft-math-nemotron-sft-math-v4/2337` | 331 |
| `aime_2025:test:18` | 6 | 0.045 | 3 / 66 | `sft-math-nemotron-sft-math-v4/1772` | 297 |
| `mmlu:test:1070` | 1 | 0.039 | 2 / 51 | `sft-math-nemotron-sft-math-v4/4383` | 9178 |
| `aime_2025:test:20` | 5 | 0.038 | 4 / 104 | `sft-math-nemotron-sft-math-v4/2337` | 331 |
| `mmlu:test:1047` | 1 | 0.036 | 2 / 56 | `sft-math-nemotron-sft-math-v4/4383` | 9178 |
| `aime_2025:test:10` | 1 | 0.027 | 3 / 111 | `sft-math-nemotron-sft-math-v4/2411` | 397 |
| `mmlu:test:1041` | 1 | 0.027 | 2 / 73 | `sft-math-nemotron-sft-math-v4/4383` | 9178 |

**`sft-math-openr1-math-raw`**: at least 30 different benchmark items found in 48 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:6736e17253926b38af8c205e` | 9 | 0.012 | 7 / 570 | `sft-math-openr1-math-raw/553` | 20232 |
| `livecodebench:release_v6:2953` | 1 | 0.012 | 2 / 171 | `sft-math-openr1-math-raw/1669` | 25153 |
| `codeforces:test:2041/H` | 7 | 0.010 | 3 / 287 | `sft-math-openr1-math-raw/399` | 79 |
| `codeforces:test:2005/D` | 7 | 0.009 | 3 / 339 | `sft-math-openr1-math-raw/399` | 79 |
| `livecodebench:release_v6:arc183_b` | 1 | 0.009 | 2 / 232 | `sft-math-openr1-math-raw/1282` | 5563 |
| `livecodebench:release_v6:abc364_c` | 3 | 0.008 | 2 / 261 | `sft-math-openr1-math-raw/1117` | 74 |
| `livecodebench:release_v6:abc384_g` | 3 | 0.007 | 2 / 291 | `sft-math-openr1-math-raw/1117` | 74 |
| `livecodebench:release_v6:arc195_b` | 3 | 0.007 | 2 / 303 | `sft-math-openr1-math-raw/1117` | 74 |
| `gpqa_diamond:extended:reclO4qus0iRSevJS` | 1 | 0.006 | 2 / 324 | `sft-math-openr1-math-raw/2404` | 8830 |
| `hle:test:6720ff60488fb478b942537b` | 5 | 0.006 | 2 / 343 | `sft-math-openr1-math-raw/1065` | 11974 |
| `hle:test:6725d1218a8e4959b13450be` | 7 | 0.006 | 4 / 696 | `sft-math-openr1-math-raw/1160` | 26250 |
| `livecodebench:release_v6:abc367_f` | 1 | 0.006 | 2 / 325 | `sft-math-openr1-math-raw/1730` | 138 |
| `livecodebench:release_v6:abc368_g` | 1 | 0.006 | 2 / 356 | `sft-math-openr1-math-raw/1282` | 5563 |
| `hle:test:66f25c95da5074d064015c54` | 1 | 0.005 | 1 / 221 | `sft-math-openr1-math-raw/1597` | 15791 |
| `hle:test:67041442aa877e548ccdc28d` | 1 | 0.005 | 1 / 214 | `sft-math-openr1-math-raw/1445` | 21024 |

**`sft-math-openr1-math`**: at least 44 different benchmark items found in 67 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `aime_2025:test:7` | 7 | 0.152 | 7 / 46 | `sft-math-openr1-math/976` | 784 |
| `aime_2025:test:3` | 2 | 0.118 | 2 / 17 | `sft-math-openr1-math/2984` | 846 |
| `aime_2025:test:21` | 5 | 0.087 | 4 / 46 | `sft-math-openr1-math/2141` | 427 |
| `aime_2025:test:27` | 1 | 0.059 | 3 / 51 | `sft-math-openr1-math/1025` | 184 |
| `aime_2025:test:6` | 5 | 0.051 | 4 / 78 | `sft-math-openr1-math/2141` | 427 |
| `aime_2025:test:18` | 5 | 0.045 | 3 / 66 | `sft-math-openr1-math/976` | 804 |
| `aime_2025:test:20` | 5 | 0.038 | 4 / 104 | `sft-math-openr1-math/2141` | 427 |
| `aime_2025:test:11` | 1 | 0.030 | 2 / 67 | `sft-math-openr1-math/3310` | 547 |
| `mmlu:test:1166` | 2 | 0.028 | 3 / 109 | `sft-math-openr1-math/3243` | 15873 |
| `hle:test:6736e17253926b38af8c205e` | 11 | 0.026 | 15 / 570 | `sft-math-openr1-math/3049` | 7468 |
| `bfcl_v3:test:parallel_multiple_84` | 1 | 0.022 | 2 / 92 | `sft-math-openr1-math/920` | 695 |
| `hle:test:67041442aa877e548ccdc28d` | 1 | 0.019 | 4 / 214 | `sft-math-openr1-math/2768` | 636 |
| `aime_2024:test:69` | 1 | 0.016 | 10 / 618 | `sft-math-openr1-math/4800` | 1735 |
| `hle:test:66fac0eca07ff774fa2219c5` | 2 | 0.013 | 2 / 157 | `sft-math-openr1-math/223` | 4152 |
| `gpqa_diamond:extended:reclO4qus0iRSevJS` | 2 | 0.012 | 4 / 324 | `sft-math-openr1-math/372` | 28448 |

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

**`sft-rl-math-openmathreasoning`**: at least 64 different benchmark items found in 115 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4350` | 1 | 0.727 | 32 / 44 | `sft-rl-math-openmathreasoning/2536` | 67 |
| `aime_2025:test:7` | 17 | 0.152 | 7 / 46 | `sft-rl-math-openmathreasoning/1844` | 348 |
| `mmlu:test:4258` | 1 | 0.130 | 3 / 23 | `sft-rl-math-openmathreasoning/3902` | 6022 |
| `aime_2025:test:21` | 12 | 0.087 | 4 / 46 | `sft-rl-math-openmathreasoning/2270` | 460 |
| `aime_2025:test:27` | 1 | 0.059 | 3 / 51 | `sft-rl-math-openmathreasoning/2618` | 428 |
| `aime_2025:test:6` | 12 | 0.051 | 4 / 78 | `sft-rl-math-openmathreasoning/2270` | 460 |
| `aime_2025:test:18` | 12 | 0.045 | 3 / 66 | `sft-rl-math-openmathreasoning/468` | 338 |
| `aime_2025:test:20` | 12 | 0.038 | 4 / 104 | `sft-rl-math-openmathreasoning/2270` | 460 |
| `aime_2025:test:11` | 2 | 0.030 | 2 / 67 | `sft-rl-math-openmathreasoning/1703` | 405 |
| `aime_2025:test:10` | 2 | 0.027 | 3 / 111 | `sft-rl-math-openmathreasoning/4852` | 435 |
| `hle:test:6736e17253926b38af8c205e` | 23 | 0.026 | 15 / 570 | `sft-rl-math-openmathreasoning/148` | 20877 |
| `livecodebench:release_v6:abc362_b` | 1 | 0.026 | 4 / 156 | `sft-rl-math-openmathreasoning/2622` | 32153 |
| `aime_2025:test:8` | 1 | 0.021 | 1 / 47 | `sft-rl-math-openmathreasoning/1703` | 358 |
| `codeforces:test:2003/F` | 1 | 0.019 | 10 / 520 | `sft-rl-math-openmathreasoning/2434` | 203 |
| `hle:test:67041442aa877e548ccdc28d` | 1 | 0.014 | 3 / 214 | `sft-rl-math-openmathreasoning/3982` | 121 |

**`sft-science-glm51-phd`**: at least 1 different benchmark items found in 2 documents (top 1 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:66fc56f5d90ebe461bfd0c9c` | 2 | 0.004 | 4 / 1065 | `sft-science-glm51-phd/1428` | 1063 |

**`sft-science-nemotron-science-v2`**: at least 5 different benchmark items found in 6 documents (top 5 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:11176` | 1 | 0.020 | 1 / 51 | `sft-science-nemotron-science-v2/1887` | 330 |
| `hle:test:67008bcea2dd0155efb53f1c` | 1 | 0.007 | 3 / 440 | `sft-science-nemotron-science-v2/1726` | 489 |
| `hle:test:67004f7644420b59a377790f` | 1 | 0.003 | 3 / 930 | `sft-science-nemotron-science-v2/1443` | 255 |
| `swe_bench_live:test:spesmilo__electrum-10172` | 2 | 0.002 | 2 / 839 | `sft-science-nemotron-science-v2/53` | 25660 |
| `hle:test:671faf8171f6aa7bd1e604cd` | 1 | 0.001 | 1 / 711 | `sft-science-nemotron-science-v2/1653` | 327 |

**`sft-science-nemotron-science`**: at least 13 different benchmark items found in 23 documents (top 13 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `milu:test:11176` | 2 | 0.020 | 1 / 51 | `sft-science-nemotron-science/3931` | 107 |
| `mmlu:test:2693` | 1 | 0.020 | 1 / 49 | `sft-science-nemotron-science/3804` | 15893 |
| `hle:test:67004f7644420b59a377790f` | 5 | 0.017 | 16 / 930 | `sft-science-nemotron-science/238` | 34594 |
| `hle:test:6700fe18dcd877e17dbc6c26` | 5 | 0.012 | 7 / 601 | `sft-science-nemotron-science/1232` | 222 |
| `mmlu:test:6449` | 1 | 0.012 | 1 / 86 | `sft-science-nemotron-science/4081` | 55567 |
| `milu:test:10689` | 2 | 0.010 | 1 / 98 | `sft-science-nemotron-science/916` | 46686 |
| `mmlu:test:6524` | 2 | 0.010 | 1 / 101 | `sft-science-nemotron-science/916` | 46686 |
| `hle:test:66e91bc08dd8f00467e3d5d8` | 1 | 0.008 | 1 / 123 | `sft-science-nemotron-science/970` | 249 |
| `milu:test:11012` | 1 | 0.008 | 1 / 122 | `sft-science-nemotron-science/4081` | 55567 |
| `mmlu:test:5503` | 2 | 0.008 | 1 / 118 | `sft-science-nemotron-science/916` | 28975 |
| `hle:test:66fc6a20d90ebe461bfd0cc7` | 1 | 0.001 | 1 / 942 | `sft-science-nemotron-science/1768` | 370 |
| `hle:test:671faf8171f6aa7bd1e604cd` | 1 | 0.001 | 1 / 711 | `sft-science-nemotron-science/4299` | 557 |
| `hle:test:67390213fc9dc4f5102ad835` | 3 | 0.001 | 3 / 2066 | `sft-science-nemotron-science/1372` | 439 |

**`sft-stem-code-openthoughts3`**: at least 79 different benchmark items found in 83 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `codeforces:test:2023/A` | 3 | 0.088 | 50 / 565 | `sft-stem-code-openthoughts3/762` | 68 |
| `codeforces:test:2060/D` | 4 | 0.075 | 16 / 214 | `sft-stem-code-openthoughts3/979` | 1110 |
| `codeforces:test:2018/B` | 4 | 0.071 | 15 / 210 | `sft-stem-code-openthoughts3/979` | 1110 |
| `codeforces:test:2062/G` | 3 | 0.061 | 50 / 825 | `sft-stem-code-openthoughts3/762` | 68 |
| `codeforces:test:2056/D` | 1 | 0.055 | 15 / 273 | `sft-stem-code-openthoughts3/979` | 1110 |
| `codeforces:test:2018/C` | 3 | 0.052 | 14 / 271 | `sft-stem-code-openthoughts3/979` | 1110 |
| `codeforces:test:2018/E1` | 1 | 0.050 | 15 / 301 | `sft-stem-code-openthoughts3/979` | 1110 |
| `codeforces:test:2013/D` | 1 | 0.043 | 10 / 230 | `sft-stem-code-openthoughts3/712` | 859 |
| `codeforces:test:2053/H` | 1 | 0.042 | 16 / 382 | `sft-stem-code-openthoughts3/1561` | 688 |
| `codeforces:test:2038/M` | 13 | 0.040 | 12 / 298 | `sft-stem-code-openthoughts3/2823` | 1252 |
| `codeforces:test:2053/G` | 1 | 0.038 | 16 / 426 | `sft-stem-code-openthoughts3/1561` | 688 |
| `codeforces:test:2037/E` | 11 | 0.036 | 23 / 640 | `sft-stem-code-openthoughts3/4304` | 2301 |
| `codeforces:test:1999/G1` | 11 | 0.032 | 23 / 728 | `sft-stem-code-openthoughts3/4304` | 2301 |
| `codeforces:test:2002/A` | 1 | 0.032 | 5 / 158 | `sft-stem-code-openthoughts3/712` | 859 |
| `codeforces:test:2041/L` | 6 | 0.030 | 13 / 438 | `sft-stem-code-openthoughts3/1426` | 1641 |

Coverage is the share of the item's runs found in the document. A value near 1.0 is a full copy; a low value is a short shared passage, for example a common problem statement. The ids above are enough to find the document in the set; the item text stays in Team 9's restricted folder.

## 5. Checks

| Check | Sets passed |
|---|---:|
| `canary_ids_in_input` | 29 of 29 |
| `canary_scan_complete` | 29 of 29 |
| `clean_file_flags_0` | 29 of 29 |
| `docs_match_checker` | 29 of 29 |
| `flagged_count_matches` | 29 of 29 |
| `flagged_ids_in_input` | 29 of 29 |
| `ids_unique` | 29 of 29 |
| `rows_in_eq_kept_plus_removed` | 29 of 29 |

`rows_in_eq_kept_plus_removed`: rows in = rows kept + rows removed. `clean_file_flags_0`: the checker, run again on the clean file, flags 0 of the kept rows. `canary_scan_complete`: `canary_scan.py` read every file (exit 0 or 1). A set with a failed check or a canary is not in this report (the script stops).

## 6. Inputs (to reproduce a run)

| Set | Input file | Bytes | sha256 |
|---|---|---:|---|
| `sft-agentic-nemotron-agentic-v1` | `agentic-nemotron-agentic-v1.jsonl` | 86,404,207 | `9a18b269d1647010e0f885c9fd26dc0a10516118464fff7fabb38295b2a3ed10` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `agentic-nemotron-sft-agentic-v2-tool-calling.jsonl` | 99,593,026 | `cb655f1db22fdf0cfc7b5af60580c415bd277da35250b315479b97a7f4d99cd5` |
| `sft-bespoke-stratos-17k` | `bespoke-stratos-17k.jsonl` | 43,734,748 | `2d8a2dcff66543423e955478ce6042fe323792ff924408e77b086624272c48f6` |
| `sft-chat-nemotron-if-v1` | `chat-nemotron-if-v1.jsonl` | 95,149,354 | `1fdd7943eed071e4b0d942b987b1e87d63b8d16a65be5f36d81f99219681b12d` |
| `sft-chat-nemotron-if-v2` | `chat-nemotron-if-v2.jsonl` | 55,595,228 | `0d746464cd8a4e1468988a7ec4c3b8fd61444ceb741f1fdcdd43672056b6f0d2` |
| `sft-code-codeforces-cots` | `codeforces-cots.jsonl` | 38,519,683 | `349852407044cdf8bb9548ffb38ee179a0e1191b069504493d655d4229f7e2a2` |
| `sft-code-nemotron-cascade-swe` | `code-nemotron-cascade-swe.jsonl` | 214,759,661 | `55930bff36ae2369accfdefdedaa85573376117ccda0b6225d9da8a592a64a93` |
| `sft-code-nemotron-cuda` | `code-nemotron-cuda.jsonl` | 82,578,942 | `af858d047eb12146110c7bb815e1814248faac6d439549d8482a8747bdcace6c` |
| `sft-code-nemotron-opencode` | `code-nemotron-opencode.jsonl` | 276,366,291 | `73bc7f3989be14113c08e100de296db64f5095a1a89815039f97ea757373ea46` |
| `sft-code-nemotron-terminal` | `code-nemotron-terminal.jsonl` | 187,951,083 | `384324c0145df8ebed7a469e348ae016084fcaf63eecfb7c201f00e0487a558e` |
| `sft-code-opencodereasoning` | `code-opencodereasoning.jsonl` | 150,691,393 | `7f87b0371d1c83791f245f3736798c1f323fa331f94b36941904a25b900cede6` |
| `sft-code-swe-rebench-openhands` | `swe-rebench-openhands.jsonl` | 104,052,372 | `b6cf83e02e5cb7bac12f3c97cbb9aad86d452fe6abb949eed4c3d55938a8b93f` |
| `sft-code-swe-zero-openhands` | `code-swe-zero-openhands.jsonl` | 314,195,928 | `cd515d2f3402789ff5df8ace2a2d7e666e37b4965afe812bf773ada52c342fad` |
| `sft-dolly-15k` | `dolly-15k.jsonl` | 5,163,448 | `a916d0097d7e70766d4ae01d9fdbc85d00f371eb741d5d5f4f404063dc286089` |
| `sft-indic-aya-collection` | `indic-aya-collection.jsonl` | 76,813,173 | `1bd9cbaeb93269283734f5f03266546fb908cf6818077a3fa8ce8672362eca77` |
| `sft-indic-aya-dataset` | `aya-dataset.jsonl` | 2,339,073 | `df0c80c61c55ea71fcfa5ef2f99067715989eda0aee504428623995241e7d768` |
| `sft-indic-indic-align-dolly-t` | `indic-indic-align-dolly-t.jsonl` | 4,581,924 | `3fbb277b99a161c47c6ad95fe7fef16be294b57fd6bc4865aac3446b15cdf78d` |
| `sft-math-nemotron-math-v2` | `math-nemotron-math-v2.jsonl` | 286,522,984 | `7d5dfe40bc57e678440e7f82296af7f553f8aea45c5d1bbb472ffd51ad57749e` |
| `sft-math-nemotron-proofs-v3-sft` | `math-nemotron-proofs-v3-sft.jsonl` | 26,129,833 | `84463c88fad4284783cf276762970dd1eacf9f90daa428da50901ca936938bcb` |
| `sft-math-nemotron-proofs` | `math-nemotron-proofs.jsonl` | 103,613,766 | `e6ab9040b703ed584ce9447dfe6d6585356cbf1bf760b1acb8507b219f7035f2` |
| `sft-math-nemotron-sft-math-v4` | `math-nemotron-sft-math-v4.jsonl` | 319,961,670 | `15b298f48748dded6dd72e5e8fc6bfbb99de80e47f4ce6b76165de89ab6b5fc4` |
| `sft-math-openr1-math-raw` | `math-openr1-math-raw.jsonl` | 115,062,763 | `da6f803013e56b53a56af067b76c67ccab1a298faa1d324dac617f2801696120` |
| `sft-math-openr1-math` | `math-openr1-math.jsonl` | 87,174,886 | `a98e5834c31c259fe3425696a2e01d287ca4f190a7eeb0df8d4dd9c5d1fe8c8e` |
| `sft-oasst2` | `oasst2.jsonl` | 20,182,471 | `04ef702f982f8e289223e08b1e9350b111f0266a43c64a871965921c3185ee85` |
| `sft-rl-math-openmathreasoning` | `rl-math-openmathreasoning.jsonl` | 116,307,094 | `e8a488a1148eeed72ab5fa00ce831b9a9a77771ec6bbcc26f46b189afd741bf7` |
| `sft-science-glm51-phd` | `science-glm51-phd.jsonl` | 50,767,551 | `76006c02909fb591f03c3b1fac18fde91d281dcd62c941cc46397b72912adb4b` |
| `sft-science-nemotron-science-v2` | `science-nemotron-science-v2.jsonl` | 16,284,951 | `722249fab4233ff4b35f5ae9fdedf5cabba7cb2b41789faf243ced6ffbf386cc` |
| `sft-science-nemotron-science` | `science-nemotron-science.jsonl` | 46,842,737 | `2e8222fd51cdf316fa840442cdb552cee35a7f46610c33f795cd56f0f67fd909` |
| `sft-stem-code-openthoughts3` | `stem-code-openthoughts3.jsonl` | 92,751,398 | `65d7ed05e3acd66e64f4bbd120b7f3a9ed24a89e86e36c869b2ca1e1325b44e1` |

```
python teams/10-post-training/sft/decontam_run.py --set <set-id> --input <set>.jsonl --out-dir decontam_out
python teams/10-post-training/sft/decontam_report.py --records decontam_out --out teams/10-post-training/sft/decontam_report.md --sets <set-id> ...
```

## 7. Sets not run yet

| Set | Why |
|---|---|
| `sft-code-opencodereasoning-2` | adapter and test written, but upstream withholds the question text ('-') in the python shard; needs a join with the source problem sets (taco, apps, code_contests) before it can be converted |
| `sft-safety-aegis-v1` | safety classification data (text plus labels, no assistant turn); no chat format applies, so no adapter |
| `sft-salesforce-xlam-60k` | gated on the Hub (needs a Hugging Face token with accepted terms); not downloaded |

## 8. What this check does not cover

- **Benchmarks outside the set.** This fingerprint set holds 20 benchmark entries: `aime_2024`, `aime_2025`, `bfcl_v3`, `codeforces`, `flores200`, `gaia`, `gpqa_diamond`, `gsm8k`, `heldout_g5_v1`, `hle`, `in22_conv`, `in22_gen`, `livecodebench`, `longbench_v2`, `milu`, `mmlu`, `swe_bench_live`, `swe_bench_pro`, `swe_bench_verified`, `terminal_bench_2`.
  It has no entry for HumanEval, HumanEval+, MBPP, MBPP+, ARC-Challenge, ARC-Easy, HellaSwag, TruthfulQA, MMLU-Pro, BBH, MuSR, Belebele, which Team 9's harnesses run (eval firewall, section 5, known gap), so a clean result says nothing about them.
  `sft_mix_proposal.md` section 1 lists HumanEval+ and MBPP+ among the benchmarks of this check; this set does not contain them.
- **Paraphrase.** The check finds copied runs of words. A reworded or translated item is not found.
- **Other rows of a set.** Only the rows that were run are covered. A set that was sampled (for example the first rows of a split) is not cleared as a whole.
- **Frozen tokenizer.** The check reads the rendered `text`, so it does not depend on the tokenizer. The effort tiers of the rows do, and Team 3 freezes the tokenizer on Sat 14 Nov.
- **A rerun is needed** when Team 9 publishes a new fingerprint set (a different set_sha256), and for any set whose rows change.

