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
- **Sets run:** 24. **Rows in:** 5,099,163. **Removed (flagged or canary):** 209,211 (4.10%). **Kept:** 4,889,952.
- No benchmark item text is in this file or in the run records: only set names, counts, document ids, benchmark item ids, offsets and sha256 values.

## 1. Result per set

| Set | Run on | Rows in | Flagged | Canary | Removed | Rows kept | Clean file sha256 |
|---|---|---:|---:|---:|---:|---:|---|
| `sft-agentic-nemotron-agentic-v1` | full set | 315,560 | 432 | 0 | 432 (0.14%) | 315,128 | `5f05e6f91fbe…` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | full set | 364,889 | 2,146 | 0 | 2,146 (0.59%) | 362,743 | `b67d3a7e1be4…`, `c08822705eda…`, `22a2f622cb9a…`, `0a25e39d3340…`, `b4ecf0815a4f…`, `053e6ba68c58…`, `0ee5176f74ea…`, `b448e52cf403…`, `93aa60bd3752…`, `d1eba6b18db8…`, `3ac1eff32010…`, `5590c5450663…`, `f00baef059e5…`, `62bf5adbbd09…`, `7c0fe76205f9…`, `486fb688253b…`, `4ea06d2ceddc…`, `d3a9e7b468d1…`, `2da74c01c873…`, `17ffc3edc1b6…`, `4529a5362e3e…`, `42692681da71…`, `8db16ceac7d5…`, `36487f0b971a…`, `b3de6d0991a3…` |
| `sft-bespoke-stratos-17k` | full set | 16,710 | 1,791 | 0 | 1,791 (10.72%) | 14,919 | `7ba1dc2bb254…` |
| `sft-chat-nemotron-if-v1` | full set | 4,963 | 1 | 0 | 1 (0.02%) | 4,962 | `38e757a1a7f8…` |
| `sft-chat-nemotron-if-v2` | full set | 929,130 | 5,820 | 0 | 5,820 (0.63%) | 923,310 | `d275e5fc036a…`, `129921cf9708…`, `fa59bf8e5412…`, `7cfc5eac47ec…`, `9f434f177f06…`, `84b302f24bc3…`, `1de7ab5945bf…`, `95ee581fa4b7…`, `8786b14b2153…`, `2db777df7567…`, `dfe1154ba357…`, `8ee148c1f184…`, `2f9ddc83eca2…`, `ca5c6a4d63bd…`, `58fc17fa19c0…`, `ae4ba4a2e852…`, `a6440d349208…`, `528a1c30fcf2…`, `d5b1a0a38e99…`, `4ab4d078274d…`, `2201fd1dca64…`, `5a792d0c4f3b…`, `a8a7284e9979…`, `da409765b5e0…`, `dd1c17be5e1e…`, `5fde6e9c38f1…`, `a17c0ff681ce…`, `624b556ba607…`, `64edd9dd9c9f…`, `c67e1d319c41…`, `e9ac4479954e…`, `b17bd1527fd8…`, `b0ac423bf558…`, `2de5563c2e80…` |
| `sft-code-codeforces-cots` | full set | 45,734 | 20,796 | 0 | 20,796 (45.47%) | 24,938 | `b5df0cfbc19b…` |
| `sft-code-nemotron-cascade-swe` | full set | 210,582 | 18,248 | 0 | 18,248 (8.67%) | 192,334 | `ec7e6a4e58e8…`, `b9aaf1093062…`, `f1524e849126…`, `b7e3ebb5dc8f…`, `c4700d5da8c7…`, `91de7b00189f…`, `058cccb5229b…`, `3f56e742de15…`, `0fca44d358a8…`, `0b501560491e…`, `7d1e2ef8c7bf…`, `f82da2a04c2f…`, `7618789a1f73…`, `94b8ed89df74…`, `020a4a1c7882…`, `acc3d8f4ef93…`, `f98976abc534…`, `21f6b684fa80…`, `dfac7970bfa9…`, `ff3c3bcbc331…`, `dad9eca584aa…`, `d7c97dad7b3a…`, `356f34dfb865…`, `6bb300fb1545…` |
| `sft-code-nemotron-cuda` | full set | 2,273 | 2 | 0 | 2 (0.09%) | 2,271 | `f451b673db79…` |
| `sft-code-nemotron-opencode` | full set | 67,086 | 332 | 0 | 332 (0.49%) | 66,754 | `dc562d0cc443…`, `3576800758a9…`, `52b89bc87e69…`, `203bfab03d84…`, `79c4877ed535…`, `f51db030cd1b…`, `1b83bfbd73c4…`, `c2dbcd0e59fa…`, `908d315b0121…`, `c74074761b8b…`, `0ae8c0e47d8e…`, `6c1b81f80ad8…`, `97de60f12503…`, `44dea49aa7e2…`, `319e3bec33bd…`, `eecfa70e05a2…`, `ae13045008f6…`, `7b9ae04c4554…`, `90944e688cf0…`, `e9afa04e9c57…`, `ef96eb70bb11…` |
| `sft-code-nemotron-terminal` | full set | 31,928 | 9,901 | 0 | 9,901 (31.01%) | 22,027 | `59278bca72a9…` |
| `sft-code-opencodereasoning` | full set | 567,831 | 112,753 | 0 | 112,753 (19.86%) | 455,078 | `6cbda38e7041…`, `6649b96a6d1c…`, `e47ae9eef7ba…`, `cc55d55aed99…`, `8617985dd2fc…`, `206a80c2ea60…`, `77a7aa9e3030…`, `ab3186f3d36d…`, `6d48fc84bcaf…`, `b6d952120b40…`, `d5f7ea4f1e79…`, `ae1d958b8345…`, `261cfe87985b…`, `9cb52f31f6d5…`, `1b648ddf84fb…`, `72bbb73bf80a…`, `f5ef1be6327e…`, `9d317faedd42…`, `230de697e342…`, `9957957f69b4…`, `27f5797cb00c…`, `e6d63201e69c…`, `453833144bb0…`, `2450161c2948…`, `84e031af054b…`, `3570616e5664…`, `a71405aacf84…`, `630c1c72a0b7…`, `97d64d94325e…`, `7da7db9e6764…`, `5d12d0449a5a…`, `84616c6b65b5…`, `29cefacd0840…`, `1ffd3300e08c…`, `55726df6a17e…`, `1af02cc4882c…`, `0627106dadcc…`, `e22bf8937afc…`, `5978b3c80490…`, `4d5e6a04c323…`, `b3e7cbdda302…`, `3cf268dc0c22…`, `76f0219e3d4d…`, `06b563083508…`, `a9271b57778c…`, `0173b4d26e00…`, `5547374f35af…`, `51a0017a3e11…`, `5a3c2752b787…`, `87bd128d197d…`, `072eec7b0c9e…`, `3a6d9190f470…`, `9c448e424aec…`, `7b723d227bb2…`, `5a5722ee61f0…`, `320a48325003…`, `4a0e637eca75…`, `005db673df8b…`, `9bcffa0ff01e…`, `a35b7ae99304…`, `d8e53ff01022…`, `693421bb13c0…`, `b77316e1aa6c…`, `ced0d14f6e58…`, `a43a36d5603b…`, `27aac9a62f34…`, `a78b0d30a5d3…`, `573b2e8aa4a7…`, `2a86104df132…`, `891a3b6dd635…`, `43e78e2ac6ba…`, `51f128ae0e2a…`, `dee827f24f32…`, `c07ca437384f…`, `a44e07451a5b…` |
| `sft-code-swe-rebench-openhands` | full set | 27,516 | 4,864 | 0 | 4,864 (17.68%) | 22,652 | `7c2b95c36dc0…` |
| `sft-code-swe-zero-openhands` | full set | 317,039 | 22,167 | 0 | 22,167 (6.99%) | 294,872 | `edcee5f6a064…`, `3988bc112a21…`, `369e0425a5dc…`, `ce4d83831cd5…`, `7b2e0a66f36c…`, `453a9a99b878…`, `20e65f2945c2…`, `56c5db671015…`, `d8b51f7f7c1e…`, `2cd5b06a10db…`, `09cb9d40d401…`, `8ede36e3b753…`, `71aaa26ba5bc…`, `e454cfaf4eda…`, `5f10455a35b8…`, `a76f4f1940be…`, `62e2aee444e9…`, `80d3e65146c1…`, `4dfa1e17e0bf…`, `c582bb5e9e2c…`, `35f570d3e389…`, `e6a264589840…`, `fe72b1e7976b…`, `482e1d85265b…`, `96dc4695d2c0…`, `301b0f1d32be…`, `aba62328301d…`, `e8f5fdd23d65…`, `a734d5222a17…`, `bfa9979767a2…`, `111f0d57f0d5…`, `09678231fe30…`, `d4ae0f7850a5…`, `84236c603aaf…`, `35f6b53a2c47…`, `a9e53f0620d6…`, `ca6483ab3cdf…`, `334d76403d86…`, `20ba94f0feb5…`, `d55ea0cf20b5…`, `7077c501b060…`, `59216d0373c3…`, `a31b60f9f057…`, `d5397f87e7f1…`, `618612ec5cb0…`, `6370c661988c…`, `b114b2f7b82f…`, `f1509f6400ad…`, `b47e7b6fd81f…`, `7da236e1c33e…`, `0f541e5dc421…`, `ccadab0a94c3…`, `edada892bc4b…`, `eace8098b643…`, `a4698e5c14a1…`, `eef4a12a42d5…`, `7dcaa2d6b8d1…`, `ac6e46a35d9b…`, `5ebad7ee254b…`, `68b4674ebf00…`, `f7f577dd2b26…`, `1c7140b3488a…`, `f72e436a25b6…`, `dbfc70f0bfb2…`, `17adef40fe86…`, `d3e43f90f8a7…`, `9c08beecd8fe…`, `24333b26ab62…`, `97c2ce7383e3…`, `97458d468e40…`, `4e7745952aad…`, `9d29e3a1b0f8…`, `655fb8c4ef41…`, `735ebe311d2d…`, `9415d384bc81…`, `367ec27efb30…`, `ff161c02e469…`, `668b12aa9a66…`, `ee693bfe563d…`, `cb264c679a47…`, `1776195baf12…`, `c64cc90e9ac4…`, `7850da597c08…`, `52d7b7cc1878…`, `788158c1e0c9…`, `edf1aa166ffa…`, `6d446a80ec37…`, `2ad36b778d1c…`, `6b3e3fe76635…`, `db3f8cebbe9e…`, `ff3672f29529…`, `a5f74e66eceb…`, `e7409a022ac4…`, `e0933c7bde79…`, `3b28ceedf8a7…`, `e2bb5d850415…`, `0f36f26e6ba3…`, `485a5812f4e4…`, `e2bbccdd4101…`, `b6545d17a77a…`, `0de385661863…`, `19bee8bc1a35…`, `5ac9f007915b…`, `954886aa8dbb…`, `92d6903ab073…`, `92119e4c2744…`, `f29bf7273d54…`, `b70d8d5dfacd…`, `ff5c446fa2d1…`, `ebb3e07613ad…`, `186b9a13f4e3…`, `f0691ef3f020…`, `5f2f0c4c0fc3…`, `899ad739cffa…`, `9cb21263fa93…`, `92224f4f2ff0…`, `d028c09995b8…`, `bd3273e35e5d…`, `6565792be46d…`, `3fdf362182d9…`, `976e1c69f96d…`, `5e61eb131deb…`, `16df6caedcfa…`, `1c9f23acc5dc…`, `e7e12bac9b14…`, `a13d972c8de1…`, `171ef9b0732b…`, `a627743038b7…`, `8730fc48449b…`, `e35540bf6497…`, `e42f82509334…`, `5cc14a4748ee…`, `b30cf2df1c8c…`, `f49428587f14…`, `bbb6ff6852fd…`, `6f470e3c953f…`, `16399627cb5d…` |
| `sft-dolly-15k` | full set | 15,011 | 4 | 0 | 4 (0.03%) | 15,007 | `93069f7a3a2c…` |
| `sft-indic-aya-collection` | full set | 654,530 | 6 | 0 | 6 (0.00%) | 654,524 | `cb4b80d9253a…` |
| `sft-indic-aya-dataset` | full set | 41,261 | 8 | 0 | 8 (0.02%) | 41,253 | `a1d2c8f07122…` |
| `sft-indic-indic-align-dolly-t` | full set | 15,011 | 0 | 0 | 0 (0.00%) | 15,011 | `35980cee7f1d…` |
| `sft-math-nemotron-sft-math-v4` | full set | 542,117 | 4,776 | 0 | 4,776 (0.88%) | 537,341 | `20c00f0cd256…` |
| `sft-math-openr1-math-raw` | full set | 321,100 | 2,494 | 0 | 2,494 (0.78%) | 318,606 | `299c9de1dc91…`, `355f0aea6e69…`, `cb1e7fc1a9d6…`, `9c05f245cadd…`, `19bf1cf578a6…`, `a82189572d24…`, `9f6a98aab885…`, `0e8bd325f985…`, `16613e4d5645…`, `c7780d5ca16e…`, `8e6b1327e587…`, `80e01c3c678f…`, `83b138c4f432…`, `ae5faab539b5…`, `4c757b6a6b3a…`, `f95fb27d8798…`, `ba4d49fdb526…`, `a6b8b887a03c…`, `301085696e10…`, `c7d25478204a…`, `94f11dd9a4b0…`, `beb29383f0d4…`, `e72f726b2852…`, `cf1e9710273d…`, `f8babf1e849d…`, `f3c8d66ee3f5…`, `74fa3c1bfff3…`, `2daec71002dc…`, `feec0e65c1b8…`, `c32f8e8f0974…`, `5b5f5fced930…`, `e62b8de9eba1…`, `564c556381c7…`, `de6f8bbc4854…`, `130695e6521c…`, `3b909d785c05…`, `a4addf83f0ca…`, `1e585e4081ac…`, `804739d9ba57…` |
| `sft-math-openr1-math` | full set | 224,882 | 1,803 | 0 | 1,803 (0.80%) | 223,079 | `682344d24ba3…`, `cbc8bcb171c9…`, `d7736b348d63…`, `a33ff5ac1edc…`, `2155e5e92cac…`, `0d8c2e5c3de9…`, `75552335c648…`, `36f998d5f8fb…`, `832b5c5c3dc3…`, `bc563c89f1fa…`, `c4b606aaf3ab…`, `35933e6d4603…`, `995b8e6cf0f8…`, `7d869556febb…`, `252ac9a8d858…`, `d241ab7ff755…`, `4aaba5193b88…`, `81500d615610…`, `d027135dc548…`, `733924cab8a8…` |
| `sft-oasst2` | full set | 9,548 | 5 | 0 | 5 (0.05%) | 9,543 | `c89de79a902a…` |
| `sft-science-glm51-phd` | full set | 103,702 | 207 | 0 | 207 (0.20%) | 103,495 | `54d681c1edc8…` |
| `sft-science-nemotron-science-v2` | full set | 96,605 | 286 | 0 | 286 (0.30%) | 96,319 | `390c839aae1b…` |
| `sft-science-nemotron-science` | full set | 174,155 | 369 | 0 | 369 (0.21%) | 173,786 | `6f9ac4dc35a0…` |
| **Total** | | **5,099,163** | **209,211** | **0** | **209,211** (4.10%) | **4,889,952** | |

**Run on** says what was checked: *full set* is every row the converter produced from the whole source (24 sets); *sample* is the first rows of a split only (0 sets), and is not cleared as a whole.

A row that is both flagged and carries a canary counts once in Removed.

## 2. Flagged documents by benchmark

| Set | `aime_2024` | `aime_2025` | `bfcl_v3` | `codeforces` | `flores200` | `gaia` | `gpqa_diamond` | `gsm8k` | `heldout_g5_v1` | `hle` | `in22_conv` | `in22_gen` | `livecodebench` | `longbench_v2` | `milu` | `mmlu` | `swe_bench_live` | `swe_bench_pro` | `swe_bench_verified` | `terminal_bench_2` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 0 | 0 | 66 | 0 | 6 | 0 | 0 | 0 | 0 | 27 | 2 | 0 | 6 | 0 | 43 | 6 | 277 | 0 | 0 | 0 |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | 0 | 1 | 135 | 1 | 0 | 0 | 0 | 1 | 16 | 18 | 3 | 2 | 636 | 0 | 30 | 14 | 1185 | 12 | 26 | 72 |
| `sft-bespoke-stratos-17k` | 87 | 73 | 1 | 1010 | 0 | 1 | 1 | 0 | 2 | 122 | 0 | 0 | 838 | 0 | 3 | 99 | 0 | 0 | 0 | 0 |
| `sft-chat-nemotron-if-v1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| `sft-chat-nemotron-if-v2` | 322 | 287 | 540 | 61 | 2 | 14 | 2 | 240 | 3 | 559 | 38 | 2 | 461 | 4 | 176 | 1425 | 1916 | 15 | 29 | 31 |
| `sft-code-codeforces-cots` | 0 | 0 | 0 | 19253 | 0 | 5 | 0 | 0 | 6 | 1738 | 0 | 0 | 10720 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| `sft-code-nemotron-cascade-swe` | 0 | 0 | 2 | 5 | 0 | 0 | 0 | 0 | 1 | 30 | 68 | 0 | 2 | 0 | 0 | 5 | 14799 | 2613 | 4375 | 4 |
| `sft-code-nemotron-cuda` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-code-nemotron-opencode` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 332 | 0 | 0 | 0 |
| `sft-code-nemotron-terminal` | 0 | 0 | 0 | 7812 | 0 | 2 | 0 | 0 | 3 | 183 | 0 | 0 | 5743 | 0 | 2 | 0 | 9 | 2 | 0 | 0 |
| `sft-code-opencodereasoning` | 0 | 1 | 0 | 73195 | 0 | 45 | 0 | 0 | 41 | 2573 | 1 | 0 | 65305 | 0 | 3 | 6 | 0 | 7 | 0 | 0 |
| `sft-code-swe-rebench-openhands` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 4474 | 21 | 1058 | 0 |
| `sft-code-swe-zero-openhands` | 0 | 0 | 16 | 23 | 0 | 0 | 0 | 0 | 0 | 111 | 22 | 0 | 3 | 1 | 5 | 16 | 19751 | 255 | 6051 | 2 |
| `sft-dolly-15k` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| `sft-indic-aya-collection` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-indic-aya-dataset` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-sft-math-v4` | 225 | 308 | 1 | 199 | 0 | 1 | 65 | 0 | 52 | 3070 | 0 | 0 | 574 | 1 | 6 | 228 | 299 | 10 | 66 | 0 |
| `sft-math-openr1-math-raw` | 321 | 121 | 11 | 327 | 0 | 1 | 31 | 0 | 13 | 1480 | 0 | 0 | 318 | 0 | 42 | 71 | 0 | 0 | 0 | 0 |
| `sft-math-openr1-math` | 354 | 279 | 14 | 99 | 0 | 0 | 30 | 0 | 7 | 1053 | 0 | 0 | 132 | 0 | 38 | 72 | 0 | 0 | 0 | 0 |
| `sft-oasst2` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| `sft-science-glm51-phd` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 207 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sft-science-nemotron-science-v2` | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 183 | 0 | 0 | 0 | 0 | 34 | 74 | 2 | 0 | 0 | 0 |
| `sft-science-nemotron-science` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 272 | 0 | 0 | 0 | 0 | 42 | 68 | 0 | 0 | 0 | 0 |

A document is flagged when it shares at least one 13-word run (20 tokens for code) with a benchmark item. The whole document is removed. The count is documents per benchmark, so a document that matches two benchmarks counts in both columns.

## 3. Flagged documents by coverage

Coverage is the share of one benchmark item's runs that the document contains (the highest over its hits). The bands are for reading the result; every flagged document is removed whatever its band.

| Set | Flagged | Coverage 0.5 or more | 0.1 to 0.5 | Below 0.1 |
|---|---:|---:|---:|---:|
| `sft-agentic-nemotron-agentic-v1` | 432 | 4 | 53 | 375 |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | 2146 | 27 | 259 | 1860 |
| `sft-bespoke-stratos-17k` | 1791 | 38 | 73 | 1680 |
| `sft-chat-nemotron-if-v1` | 1 | 0 | 1 | 0 |
| `sft-chat-nemotron-if-v2` | 5820 | 669 | 1011 | 4140 |
| `sft-code-codeforces-cots` | 20796 | 45 | 1563 | 19188 |
| `sft-code-nemotron-cascade-swe` | 18248 | 211 | 1620 | 16417 |
| `sft-code-nemotron-cuda` | 2 | 0 | 0 | 2 |
| `sft-code-nemotron-opencode` | 332 | 0 | 0 | 332 |
| `sft-code-nemotron-terminal` | 9901 | 321 | 454 | 9126 |
| `sft-code-opencodereasoning` | 112753 | 0 | 1311 | 111442 |
| `sft-code-swe-rebench-openhands` | 4864 | 147 | 263 | 4454 |
| `sft-code-swe-zero-openhands` | 22167 | 222 | 2230 | 19715 |
| `sft-dolly-15k` | 4 | 0 | 1 | 3 |
| `sft-indic-aya-collection` | 6 | 1 | 0 | 5 |
| `sft-indic-aya-dataset` | 8 | 1 | 2 | 5 |
| `sft-indic-indic-align-dolly-t` | 0 | 0 | 0 | 0 |
| `sft-math-nemotron-sft-math-v4` | 4776 | 0 | 42 | 4734 |
| `sft-math-openr1-math-raw` | 2494 | 0 | 39 | 2455 |
| `sft-math-openr1-math` | 1803 | 0 | 50 | 1753 |
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

**`sft-agentic-nemotron-sft-agentic-v2-tool-calling`**: at least 135 different benchmark items found in 2146 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `bfcl_v3:test:simple_336` | 1 | 1.000 | 1 / 1 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/170675` | 3274 |
| `bfcl_v3:test:simple_379` | 1 | 1.000 | 1 / 1 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/343534` | 2078 |
| `bfcl_v3:test:simple_9` | 12 | 1.000 | 1 / 1 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/22611` | 349 |
| `livecodebench:release_v6:3461` | 252 | 0.775 | 93 / 120 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/96905` | 12160 |
| `heldout_g5_v1:heldout:pes2o-val-000124` | 10 | 0.623 | 48 / 77 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/101126` | 52488 |
| `gsm8k:test:42` | 1 | 0.458 | 54 / 118 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/196745` | 121203 |
| `mmlu:test:5882` | 2 | 0.451 | 107 / 237 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/73659` | 4345 |
| `gsm8k:test:40` | 1 | 0.439 | 25 / 57 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/196745` | 117086 |
| `mmlu:test:6050` | 2 | 0.439 | 107 / 244 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/73659` | 4345 |
| `mmlu:test:5857` | 2 | 0.431 | 107 / 248 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/73659` | 4345 |
| `livecodebench:release_v6:3748` | 96 | 0.422 | 81 / 192 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/35210` | 16187 |
| `mmlu:test:5962` | 2 | 0.392 | 107 / 273 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/73659` | 4345 |
| `gsm8k:test:71` | 1 | 0.391 | 25 / 64 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/196745` | 125785 |
| `gsm8k:test:55` | 1 | 0.378 | 17 / 45 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/196745` | 117563 |
| `gsm8k:test:3` | 1 | 0.371 | 13 / 35 | `sft-agentic-nemotron-sft-agentic-v2-tool-calling/196745` | 116743 |

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

**`sft-chat-nemotron-if-v2`**: at least 1048 different benchmark items found in 5820 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `bfcl_v3:test:irrelevance_139` | 1 | 1.000 | 1 / 1 | `sft-chat-nemotron-if-v2/664081` | 67 |
| `bfcl_v3:test:live_irrelevance_719-238-0` | 2 | 1.000 | 1 / 1 | `sft-chat-nemotron-if-v2/199664` | 2086 |
| `flores200:dev+devtest:dev:eng_Latn:596` | 1 | 1.000 | 1 / 1 | `sft-chat-nemotron-if-v2/621137` | 9237 |
| `mmlu:test:1424` | 1 | 0.948 | 73 / 77 | `sft-chat-nemotron-if-v2/744064` | 77 |
| `mmlu:test:1440` | 1 | 0.915 | 65 / 71 | `sft-chat-nemotron-if-v2/646165` | 77 |
| `mmlu:test:12326` | 1 | 0.881 | 52 / 59 | `sft-chat-nemotron-if-v2/811485` | 67 |
| `mmlu:test:4291` | 18 | 0.872 | 75 / 86 | `sft-chat-nemotron-if-v2/550798` | 331 |
| `mmlu:test:4279` | 20 | 0.867 | 72 / 83 | `sft-chat-nemotron-if-v2/576972` | 3781 |
| `mmlu:test:601` | 1 | 0.857 | 6 / 7 | `sft-chat-nemotron-if-v2/772946` | 77 |
| `mmlu:test:672` | 4 | 0.857 | 6 / 7 | `sft-chat-nemotron-if-v2/31734` | 185 |
| `mmlu:test:100` | 11 | 0.848 | 67 / 79 | `sft-chat-nemotron-if-v2/902982` | 67 |
| `mmlu:test:4423` | 11 | 0.836 | 56 / 67 | `sft-chat-nemotron-if-v2/159143` | 770 |
| `mmlu:test:3472` | 9 | 0.833 | 5 / 6 | `sft-chat-nemotron-if-v2/23309` | 1071 |
| `mmlu:test:4393` | 10 | 0.829 | 58 / 70 | `sft-chat-nemotron-if-v2/55826` | 3343 |
| `livecodebench:release_v6:2792` | 1 | 0.820 | 169 / 206 | `sft-chat-nemotron-if-v2/168382` | 67 |

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

**`sft-code-nemotron-cascade-swe`**: at least 630 different benchmark items found in 18248 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:beeware__briefcase-1867` | 1 | 1.000 | 51 / 51 | `sft-code-nemotron-cascade-swe/200008959` | 181 |
| `swe_bench_live:test:conan-io__conan-15699` | 34 | 1.000 | 238 / 238 | `sft-code-nemotron-cascade-swe/100001423` | 180 |
| `swe_bench_live:test:conan-io__conan-15931` | 108 | 1.000 | 49 / 49 | `sft-code-nemotron-cascade-swe/100003235` | 180 |
| `swe_bench_live:test:streamlink__streamlink-5926` | 74 | 0.996 | 278 / 279 | `sft-code-nemotron-cascade-swe/100017100` | 179 |
| `swe_bench_live:test:streamlink__streamlink-5908` | 9 | 0.973 | 358 / 368 | `sft-code-nemotron-cascade-swe/37451` | 256 |
| `swe_bench_live:test:icloud-photos-downloader__icloud_photos_downloader-1060` | 7 | 0.964 | 319 / 331 | `sft-code-nemotron-cascade-swe/100011480` | 179 |
| `swe_bench_live:test:streamlink__streamlink-6420` | 39 | 0.954 | 352 / 369 | `sft-code-nemotron-cascade-swe/100010333` | 180 |
| `swe_bench_live:test:wireservice__csvkit-1281` | 1 | 0.943 | 477 / 506 | `sft-code-nemotron-cascade-swe/45056` | 256 |
| `swe_bench_live:test:streamlink__streamlink-6242` | 136 | 0.924 | 171 / 185 | `sft-code-nemotron-cascade-swe/100000310` | 179 |
| `swe_bench_live:test:beeware__briefcase-1638` | 8 | 0.920 | 103 / 112 | `sft-code-nemotron-cascade-swe/100011261` | 180 |
| `swe_bench_live:test:streamlink__streamlink-6353` | 101 | 0.904 | 311 / 344 | `sft-code-nemotron-cascade-swe/100003763` | 179 |
| `swe_bench_live:test:kedro-org__kedro-3715` | 20 | 0.875 | 1290 / 1474 | `sft-code-nemotron-cascade-swe/61028` | 256 |
| `swe_bench_live:test:streamlink__streamlink-6207` | 10 | 0.866 | 629 / 726 | `sft-code-nemotron-cascade-swe/100000595` | 179 |
| `swe_bench_live:test:pdm-project__pdm-3393` | 7 | 0.852 | 1584 / 1860 | `sft-code-nemotron-cascade-swe/41285` | 258 |
| `swe_bench_live:test:streamlink__streamlink-5844` | 8 | 0.830 | 597 / 719 | `sft-code-nemotron-cascade-swe/100001030` | 179 |

**`sft-code-nemotron-cuda`**: at least 2 different benchmark items found in 2 documents (top 2 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:6726c7e9d2ad475e400669c7` | 1 | 0.002 | 1 / 635 | `sft-code-nemotron-cuda/952` | 30663 |
| `codeforces:test:2055/C` | 1 | 0.001 | 1 / 885 | `sft-code-nemotron-cuda/272` | 15733 |

**`sft-code-nemotron-opencode`**: at least 3 different benchmark items found in 332 documents (top 3 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:streamlink__streamlink-6111` | 318 | 0.014 | 4 / 290 | `sft-code-nemotron-opencode/388` | 55945 |
| `swe_bench_live:test:kozea__weasyprint-2326` | 11 | 0.006 | 3 / 545 | `sft-code-nemotron-opencode/11431` | 107288 |
| `swe_bench_live:test:lss233__kirara-ai-1445` | 3 | 0.000 | 3 / 11774 | `sft-code-nemotron-opencode/3800` | 104386 |

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

**`sft-code-opencodereasoning`**: at least 990 different benchmark items found in 112753 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `hle:test:66ed458ed841eb51a985ca8d` | 40 | 0.471 | 192 / 408 | `sft-code-opencodereasoning/2000007388` | 67 |
| `hle:test:672f6cfd609b665328565e5c` | 38 | 0.421 | 134 / 318 | `sft-code-opencodereasoning/2000007984` | 67 |
| `hle:test:672f72e3609b665328565e6b` | 39 | 0.238 | 125 / 526 | `sft-code-opencodereasoning/700002908` | 67 |
| `hle:test:66eeea0187ec4a6a04092e78` | 757 | 0.192 | 79 / 412 | `sft-code-opencodereasoning/2300013191` | 194 |
| `hle:test:673627bc10ec0a5f859365ce` | 40 | 0.188 | 69 / 368 | `sft-code-opencodereasoning/700003608` | 928 |
| `hle:test:67373220a4d09488d430f640` | 40 | 0.185 | 69 / 373 | `sft-code-opencodereasoning/700003608` | 928 |
| `hle:test:672e24f117ed86a6ef9def55` | 40 | 0.183 | 72 / 393 | `sft-code-opencodereasoning/2000000557` | 67 |
| `codeforces:test:2018/B` | 10508 | 0.181 | 38 / 210 | `sft-code-opencodereasoning/2300014462` | 857 |
| `codeforces:test:2038/B` | 8186 | 0.169 | 30 / 178 | `sft-code-opencodereasoning/2500005210` | 502 |
| `codeforces:test:2060/D` | 6875 | 0.159 | 34 / 214 | `sft-code-opencodereasoning/2300015043` | 781 |
| `codeforces:test:2010/A` | 3828 | 0.151 | 16 / 106 | `sft-code-opencodereasoning/2300014197` | 673 |
| `codeforces:test:2056/D` | 4717 | 0.150 | 41 / 273 | `sft-code-opencodereasoning/2300012583` | 1048 |
| `livecodebench:release_v6:1873_B` | 4755 | 0.149 | 24 / 161 | `sft-code-opencodereasoning/2300014293` | 943 |
| `in22_conv:test:6-2` | 1 | 0.143 | 1 / 7 | `sft-code-opencodereasoning/1100017410` | 44316 |
| `hle:test:66f28a89f1256af80477e15d` | 40 | 0.136 | 100 / 733 | `sft-code-opencodereasoning/2000001343` | 67 |

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

**`sft-code-swe-zero-openhands`**: at least 670 different benchmark items found in 22167 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `swe_bench_live:test:beeware__briefcase-1867` | 3 | 1.000 | 51 / 51 | `sft-code-swe-zero-openhands/6100001056` | 6757 |
| `swe_bench_live:test:conan-io__conan-15699` | 27 | 1.000 | 238 / 238 | `sft-code-swe-zero-openhands/3900004463` | 6752 |
| `swe_bench_live:test:conan-io__conan-15931` | 95 | 1.000 | 49 / 49 | `sft-code-swe-zero-openhands/1300004903` | 6752 |
| `swe_bench_live:test:streamlink__streamlink-5926` | 450 | 0.996 | 278 / 279 | `sft-code-swe-zero-openhands/4700001046` | 6765 |
| `swe_bench_live:test:streamlink__streamlink-5908` | 8 | 0.973 | 358 / 368 | `sft-code-swe-zero-openhands/4400000861` | 6765 |
| `swe_bench_live:test:streamlink__streamlink-6439` | 148 | 0.972 | 413 / 425 | `sft-code-swe-zero-openhands/6100003918` | 6765 |
| `swe_bench_live:test:icloud-photos-downloader__icloud_photos_downloader-1060` | 6 | 0.964 | 319 / 331 | `sft-code-swe-zero-openhands/6100002261` | 6823 |
| `swe_bench_live:test:streamlink__streamlink-6420` | 21 | 0.954 | 352 / 369 | `sft-code-swe-zero-openhands/6200000014` | 6765 |
| `swe_bench_live:test:wireservice__csvkit-1281` | 1 | 0.943 | 477 / 506 | `sft-code-swe-zero-openhands/6300002902` | 6759 |
| `swe_bench_live:test:streamlink__streamlink-6242` | 589 | 0.924 | 171 / 185 | `sft-code-swe-zero-openhands/6100000054` | 6767 |
| `swe_bench_live:test:beeware__briefcase-1638` | 3 | 0.920 | 103 / 112 | `sft-code-swe-zero-openhands/5700000929` | 6758 |
| `swe_bench_live:test:streamlink__streamlink-6111` | 235 | 0.910 | 264 / 290 | `sft-code-swe-zero-openhands/6200003408` | 6765 |
| `swe_bench_live:test:pybamm-team__pybamm-4644` | 3 | 0.909 | 190 / 209 | `sft-code-swe-zero-openhands/6100004917` | 6764 |
| `swe_bench_live:test:streamlink__streamlink-6353` | 336 | 0.904 | 311 / 344 | `sft-code-swe-zero-openhands/6200004054` | 6765 |
| `swe_bench_live:test:pydata__xarray-9974` | 173 | 0.877 | 580 / 661 | `sft-code-swe-zero-openhands/6200000946` | 6757 |

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

**`sft-math-openr1-math-raw`**: at least 293 different benchmark items found in 2494 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4349` | 1 | 0.481 | 26 / 54 | `sft-math-openr1-math-raw/1400005169` | 166 |
| `mmlu:test:4410` | 1 | 0.462 | 12 / 26 | `sft-math-openr1-math-raw/1400010836` | 67 |
| `mmlu:test:4375` | 1 | 0.391 | 18 / 46 | `sft-math-openr1-math-raw/3800011445` | 68 |
| `bfcl_v3:test:simple_13` | 1 | 0.333 | 1 / 3 | `sft-math-openr1-math-raw/700003475` | 3056 |
| `mmlu:test:4252` | 1 | 0.310 | 9 / 29 | `sft-math-openr1-math-raw/3800011515` | 67 |
| `milu:test:58255` | 1 | 0.250 | 4 / 16 | `sft-math-openr1-math-raw/2000003743` | 3999 |
| `aime_2024:test:60` | 1 | 0.246 | 85 / 345 | `sft-math-openr1-math-raw/3800011332` | 67 |
| `aime_2025:test:8` | 7 | 0.234 | 11 / 47 | `sft-math-openr1-math-raw/1400007666` | 486 |
| `mmlu:test:4258` | 5 | 0.217 | 5 / 23 | `sft-math-openr1-math-raw/9758` | 399 |
| `aime_2024:test:83` | 8 | 0.207 | 41 / 198 | `sft-math-openr1-math-raw/3800011658` | 68 |
| `bfcl_v3:test:multiple_1` | 1 | 0.200 | 1 / 5 | `sft-math-openr1-math-raw/2600002060` | 165 |
| `milu:test:14282` | 3 | 0.188 | 12 / 64 | `sft-math-openr1-math-raw/3100010635` | 670 |
| `bfcl_v3:test:parallel_62` | 4 | 0.167 | 8 / 48 | `sft-math-openr1-math-raw/2000006321` | 1491 |
| `mmlu:test:4348` | 1 | 0.167 | 1 / 6 | `sft-math-openr1-math-raw/1100001251` | 70 |
| `milu:test:14948` | 3 | 0.162 | 11 / 68 | `sft-math-openr1-math-raw/3100010635` | 670 |

**`sft-math-openr1-math`**: at least 238 different benchmark items found in 1803 documents (top 15 by coverage; the checker lists the best 5 items per document, so this is a lower bound)

| Benchmark item | Documents | Highest coverage | Shared runs / item runs | Example document | Offset |
|---|---:|---:|---:|---|---:|
| `mmlu:test:4349` | 2 | 0.481 | 26 / 54 | `sft-math-openr1-math/1100001792` | 67 |
| `mmlu:test:4410` | 1 | 0.462 | 12 / 26 | `sft-math-openr1-math/1544` | 67 |
| `mmlu:test:4302` | 1 | 0.370 | 20 / 54 | `sft-math-openr1-math/800008252` | 240 |
| `bfcl_v3:test:irrelevance_9` | 1 | 0.333 | 1 / 3 | `sft-math-openr1-math/1400000644` | 4537 |
| `bfcl_v3:test:simple_13` | 1 | 0.333 | 1 / 3 | `sft-math-openr1-math/9358` | 3056 |
| `aime_2025:test:8` | 12 | 0.234 | 11 / 47 | `sft-math-openr1-math/1000004728` | 486 |
| `mmlu:test:4258` | 8 | 0.217 | 5 / 23 | `sft-math-openr1-math/1700008372` | 143 |
| `milu:test:14282` | 1 | 0.188 | 12 / 64 | `sft-math-openr1-math/1621` | 670 |
| `mmlu:test:4348` | 1 | 0.167 | 1 / 6 | `sft-math-openr1-math/800005908` | 70 |
| `milu:test:8917` | 2 | 0.164 | 12 / 73 | `sft-math-openr1-math/900000298` | 326 |
| `milu:test:14948` | 1 | 0.162 | 11 / 68 | `sft-math-openr1-math/1621` | 670 |
| `aime_2025:test:7` | 206 | 0.152 | 7 / 46 | `sft-math-openr1-math/1600006189` | 347 |
| `aime_2025:test:14` | 3 | 0.125 | 4 / 32 | `sft-math-openr1-math/300010116` | 1890 |
| `milu:test:14951` | 1 | 0.125 | 11 / 88 | `sft-math-openr1-math/1621` | 670 |
| `milu:test:17755` | 1 | 0.123 | 8 / 65 | `sft-math-openr1-math/1600009687` | 5266 |

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
| `all_source_files_converted` | 8 of 24 |
| `canary_ids_in_input` | 24 of 24 |
| `canary_scan_complete` | 24 of 24 |
| `clean_file_flags_0` | 24 of 24 |
| `docs_match_checker` | 24 of 24 |
| `every_removed_row_is_hit` | 1 of 24 |
| `flagged_count_matches` | 24 of 24 |
| `flagged_ids_in_input` | 24 of 24 |
| `ids_disjoint_across_units` | 8 of 24 |
| `ids_unique` | 24 of 24 |
| `parts_cover_all_converted_rows` | 8 of 24 |
| `rows_in_eq_kept_plus_removed` | 24 of 24 |

`rows_in_eq_kept_plus_removed`: rows in = rows kept + rows removed. `clean_file_flags_0`: the checker, run again on the clean file, flags 0 of the kept rows. `canary_scan_complete`: `canary_scan.py` read every file (exit 0 or 1). A set with a failed check or a canary is not in this report (the script stops).

## 6. Inputs (to reproduce a run)

| Set | Input file | Bytes | sha256 |
|---|---|---:|---|
| `sft-agentic-nemotron-agentic-v1` | `agentic-nemotron-agentic-v1.jsonl` | 5,500,570,007 | `5cca4abb9ead609776b4b4f2df99c7d2a95d27f0dcca0137ec1504a57680d0ec` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0000.jsonl` | 300,000,898 | `da8af19ac90c53b9edae0d147caf17e10bbcb6edf11bb0072cc222a3efa90334` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0001.jsonl` | 300,029,931 | `fb0a3bce896541d4196a868eb7670514052c04c5f19d60e4990b1ad9b5e6eefa` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0002.jsonl` | 300,008,031 | `1eab45d5e748304d4f6c0150e92a1da9c0cdd97967947d393967a1dba7c3fca5` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0003.jsonl` | 300,012,764 | `dcf4b3156f3e5033af64ea27a02e5818f8100258ea6f8aec038c6950d13934e2` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0004.jsonl` | 300,012,600 | `96a1abc61c2b8d0bed464070d3d48ce7df0dd8323a7e09d79d58351184437e1f` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0005.jsonl` | 300,032,657 | `d1815f05e6f1a1331ad56952ba5fe1c9f3c20fa20291cd281a5765995a6c3805` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0006.jsonl` | 300,009,738 | `83e6dd9f7d42a0aab68cec46cfab9f792c72c78b46455fa245b36f6f6d284b2b` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0007.jsonl` | 300,001,752 | `4287506496fac10ba7ec108ec22d8b811e7c39026fe9fc7f97a4749d041e992b` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0008.jsonl` | 300,023,451 | `9b86c032a99a98b76f98314b3bac63aa1a9f8252101287ad29f119126800dbb3` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0009.jsonl` | 300,016,600 | `51b2ce25cc46d11bd3678c20ee92ec8eefb78217a342762f901777904b5ebe23` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0010.jsonl` | 300,014,446 | `51ebd7061c9f54c24898c45030f1c1a88db6d0c32a68c286575154f12813c8bc` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0011.jsonl` | 300,109,260 | `fe61d673c33884c9b159d440216649444ec6aef97f5a6d5e354c812b27ad7129` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0012.jsonl` | 300,009,216 | `e27c6c9e9192fb9efd5aa1bcd87bd849b069775845fa87ad4662fdbd60afc8ef` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0013.jsonl` | 300,032,160 | `6d75728201dcc1221144a0f37e9cdde42f54d06dd6b58a6d2ec123e6e466c03a` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0014.jsonl` | 300,011,788 | `e4fd7bb0fb43fedb5a0ae3979a48c113aa8ed5d537981d68fe9053f78d6028e7` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0015.jsonl` | 300,005,449 | `01b8e97c5f1bb79e534c254863b1a7c6044f130311ab3103c7986cc30c10760c` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0016.jsonl` | 300,036,346 | `7e1f81fab0a3a03311c7a759fd6231164b6d20e6f6131e3eb551ff7e771fc3b3` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0017.jsonl` | 300,010,974 | `a7b16dc466426ddf2e9b6ba1c5beada973cd6b8c56841e562fd4a2e30ec26b17` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0018.jsonl` | 300,008,035 | `14f0b03fcf3b145b236f01fe16d7c6fd68f1b60dc6591843a53830c8557509d1` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0019.jsonl` | 300,003,968 | `4e1dc7bec9ee3d4b4bfba210d9cb79d7b2347f2215c1906aad7ba3debcde0833` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0020.jsonl` | 300,039,366 | `7b187ebecf4843f3af7051829d78f72eeeee7fcaef9150833c9035ebf56c1869` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0021.jsonl` | 300,012,781 | `3dd607b9725abf422c299a1ae95972f5175aca0742f718503379918287fef237` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0022.jsonl` | 300,065,466 | `98c6a5c86f4ba8a3925845678395b8c07037d470cd080ed836f2be9fe78c3707` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0023.jsonl` | 300,018,665 | `c22b95fd8f6e81d6da75400648d66c768c21445dcb18110b8af0c2fccd541cce` |
| `sft-agentic-nemotron-sft-agentic-v2-tool-calling` | `u000.part0024.jsonl` | 277,728,019 | `cf3dc93001dccf1d2c55b3ed6ae04c71de746c5e21781feb46eff62c2d002790` |
| `sft-bespoke-stratos-17k` | `bespoke-stratos-17k.jsonl` | 298,311,597 | `55f7d082ceb9a5df726a20f28b4bdecf07bc4c1b9471b264313f80adc48a2d74` |
| `sft-chat-nemotron-if-v1` | `chat-nemotron-if-v1.jsonl` | 95,149,354 | `1fdd7943eed071e4b0d942b987b1e87d63b8d16a65be5f36d81f99219681b12d` |
| `sft-chat-nemotron-if-v2` | `u000.part0000.jsonl` | 300,014,364 | `e606823d258bb9879c47d7baa0a002f5286170d53f930f8a7e868bb481efb610` |
| `sft-chat-nemotron-if-v2` | `u000.part0001.jsonl` | 300,013,899 | `8aec878469ff050aa42c784e2d82a0eb8bcda5c00133cb87e083b3e4687ef45e` |
| `sft-chat-nemotron-if-v2` | `u000.part0002.jsonl` | 300,000,187 | `7818a24c5780303ba5d604aa9e4bb4f248bd289ce81b97bd95b9f21709f65e31` |
| `sft-chat-nemotron-if-v2` | `u000.part0003.jsonl` | 300,019,724 | `da2651c873dd76a31992edd58ae257004d5d029bceda14ce3820be406e12794f` |
| `sft-chat-nemotron-if-v2` | `u000.part0004.jsonl` | 300,003,157 | `8490f6aff370d410928bb0155dc7ed23abce00660468339d4a422aa36e1c21f5` |
| `sft-chat-nemotron-if-v2` | `u000.part0005.jsonl` | 300,001,379 | `f245f37a1add15c1759f13ecf38577ce960a514d1c5643b0e7f42cbfc50e3fa0` |
| `sft-chat-nemotron-if-v2` | `u000.part0006.jsonl` | 300,009,291 | `713044762365a342f8dbd6d132b5865c48e16522fb962da2cb02e3e3e1c93309` |
| `sft-chat-nemotron-if-v2` | `u000.part0007.jsonl` | 300,006,731 | `df23296a3141290046ecabf30d6e872c241417bd85dbbc99774159a53a188ff5` |
| `sft-chat-nemotron-if-v2` | `u000.part0008.jsonl` | 300,010,472 | `e6dc824f7013f9f929a428707cc5995f619683d8bb0e2496fbd2ff5efdb6aee0` |
| `sft-chat-nemotron-if-v2` | `u000.part0009.jsonl` | 300,004,203 | `736cf09485ecd2e8a5c40ce5082e8f7bde84abad940a656271b6f3abd8d4d2b2` |
| `sft-chat-nemotron-if-v2` | `u000.part0010.jsonl` | 300,017,404 | `e7a85f5a636e92cf0c0575ccad570f0979ea63eb4442a872c2fc5482d1d704a0` |
| `sft-chat-nemotron-if-v2` | `u000.part0011.jsonl` | 300,006,205 | `6036ffccc6f3ae366a7c724619a977c6c07e16cb4a7099246e430924c253a08b` |
| `sft-chat-nemotron-if-v2` | `u000.part0012.jsonl` | 300,027,489 | `41018713bddad85e28531d17caf60281b9b6dba2232ac12673b8a6c5bfb43078` |
| `sft-chat-nemotron-if-v2` | `u000.part0013.jsonl` | 300,007,113 | `e2e01df0fb0bf2c5635fa5f73b14425dc9eaff4229f50535d59287f9d2e8ffd1` |
| `sft-chat-nemotron-if-v2` | `u000.part0014.jsonl` | 300,016,662 | `573cb0e79541e53a6d0bd53ee36ea008828b8a93cd032f3b049b92e0b99c5f43` |
| `sft-chat-nemotron-if-v2` | `u000.part0015.jsonl` | 300,001,399 | `4e16f0c4494023848bb6a188f7c1fd635cc2e350ad0bdecbbab70e0b4bafb754` |
| `sft-chat-nemotron-if-v2` | `u000.part0016.jsonl` | 300,003,569 | `bcc60335b49fb5ab40b0bac6606017a2a2f5c16c2792262d79590f1962d6649d` |
| `sft-chat-nemotron-if-v2` | `u000.part0017.jsonl` | 300,006,470 | `8251e1f4c74e40dd8f5ed2efad45522f9dc34c2650476dce19a10901ca770c24` |
| `sft-chat-nemotron-if-v2` | `u000.part0018.jsonl` | 300,000,345 | `9a802baae305621c261007628b21d2d2c0bd0a8783b96d6f8c4dd173c68c9d98` |
| `sft-chat-nemotron-if-v2` | `u000.part0019.jsonl` | 300,005,535 | `a31755998905737bca545118de55008290f9d35b10abe522c43dcd4cb68abcb8` |
| `sft-chat-nemotron-if-v2` | `u000.part0020.jsonl` | 300,003,235 | `7753ab3f86c674e33afd19782bc926fa2103e8e4f595e46b6d2f3584a61ec602` |
| `sft-chat-nemotron-if-v2` | `u000.part0021.jsonl` | 300,016,133 | `944e7e15a4568f23554079b8c2411df181b465027117b988e61c8edc92836d34` |
| `sft-chat-nemotron-if-v2` | `u000.part0022.jsonl` | 300,001,550 | `f56edab0a612b1b1277f578eb87f34c6749a6dcccbc845188a0711d11a40d860` |
| `sft-chat-nemotron-if-v2` | `u000.part0023.jsonl` | 300,012,232 | `6dceb2e78f6c72c8f3089019561d386402e2dcb7ce28dc594343bab267ea9efc` |
| `sft-chat-nemotron-if-v2` | `u000.part0024.jsonl` | 300,000,277 | `aac91f03e734c5ed25a647c420965ed429719904d655e930818ce7f6b91ad504` |
| `sft-chat-nemotron-if-v2` | `u000.part0025.jsonl` | 300,000,666 | `3248db4f273b00110f8f0d0c4688f7c68be0cc66617184877801bd26ce712afa` |
| `sft-chat-nemotron-if-v2` | `u000.part0026.jsonl` | 300,006,425 | `c71055f6653cc67cbe6e37c9380e69b1d436c71b18449be7080c68ae2e2025cf` |
| `sft-chat-nemotron-if-v2` | `u000.part0027.jsonl` | 300,006,699 | `0c9b10b713d6ec837d862df377621e023dd1335eb99d03a25b29c34c0fcc7372` |
| `sft-chat-nemotron-if-v2` | `u000.part0028.jsonl` | 300,001,716 | `8506046b6cb766822608cf425ae708efc635fdc378cad79a9d84c20b00349ffd` |
| `sft-chat-nemotron-if-v2` | `u000.part0029.jsonl` | 300,006,714 | `ee6612587d27b6f6f50d2da17c0e2e7e8f9d243d2523c546f98cbbf8800bd04f` |
| `sft-chat-nemotron-if-v2` | `u000.part0030.jsonl` | 300,000,317 | `812cb586ddcff098fbcdbb2039a31ae0d175cb0dfc32863a00d5aebccb9f2b33` |
| `sft-chat-nemotron-if-v2` | `u000.part0031.jsonl` | 300,008,024 | `f612bd57f8daf3c7c226eeb834f0007f6f11613883ffc7bcf782a38104048446` |
| `sft-chat-nemotron-if-v2` | `u000.part0032.jsonl` | 300,007,472 | `d6b32d5c1ef0ab9bf3f97cfa51bdc472ab64357e5de390d7f1c5191de88aee4d` |
| `sft-chat-nemotron-if-v2` | `u000.part0033.jsonl` | 240,681,203 | `678489bb8031b72549e4ff2c211b3335c7f729c70f32bf366e9acbef0e265a40` |
| `sft-code-codeforces-cots` | `code-codeforces-cots.jsonl` | 2,287,612,938 | `d3ef4f33f43f1d22c2912fe2de97951d3c44843e20994b9b24b711f635c0e2fa` |
| `sft-code-nemotron-cascade-swe` | `u001.part0000.jsonl` | 300,031,511 | `4a9b2c58c49b9f59cd1c5e90f4022f889eebdd352a5e0d91dbacbcd0666235f6` |
| `sft-code-nemotron-cascade-swe` | `u000.part0000.jsonl` | 300,009,446 | `23468d927ee37b0bad463264a1f7b5fd99c90398c776b62f749399dc98267b13` |
| `sft-code-nemotron-cascade-swe` | `u001.part0001.jsonl` | 300,043,968 | `e7e94b9acec08c3d985ff40f042fafd7ea7671e4ace532611bcd635dfc24f244` |
| `sft-code-nemotron-cascade-swe` | `u002.part0000.jsonl` | 300,009,836 | `0d0c80952234abc2c59a6b7ecf2a90a66a079228356ca9e7978e560219fa456d` |
| `sft-code-nemotron-cascade-swe` | `u000.part0001.jsonl` | 300,063,589 | `e0e3dae3c9e2dbf610cb5c60427b16e640c3a56e9ff72002eb9cc3610f242f78` |
| `sft-code-nemotron-cascade-swe` | `u002.part0001.jsonl` | 300,007,682 | `c2d6152f5a733e22fde4308b0b4a4a8e65d37bae48d01e39a7b7c793af57cd6d` |
| `sft-code-nemotron-cascade-swe` | `u001.part0002.jsonl` | 300,035,081 | `9b2777b17377fb8300b13e9c8b795f389ad14fe64b39a04abe67e76d3cebb62f` |
| `sft-code-nemotron-cascade-swe` | `u000.part0002.jsonl` | 300,017,427 | `7b0af8b5b8d24afd5177cd4746dda8fd57e151dd65130a3d4cf3a6b97c4898e0` |
| `sft-code-nemotron-cascade-swe` | `u002.part0002.jsonl` | 256,322,858 | `565853dc9e9142d21e5c7a16ff06394824d4d15860edb4a9116eb1b8629b9eb3` |
| `sft-code-nemotron-cascade-swe` | `u001.part0003.jsonl` | 300,016,350 | `e4889663a91df29bbcc817b06b177157c43433019c0101f913a7242022807448` |
| `sft-code-nemotron-cascade-swe` | `u000.part0003.jsonl` | 300,008,451 | `d791eb18b877ea455bcc9e50f72d28c03a606351866be5356a6dc64f52777dc8` |
| `sft-code-nemotron-cascade-swe` | `u001.part0004.jsonl` | 300,000,441 | `cbe66728920ef74585c9b796c3a7874cc7b7871c3f3bb9d1d933b433f5dc2718` |
| `sft-code-nemotron-cascade-swe` | `u000.part0004.jsonl` | 300,010,798 | `36477cec7d7024629e17a953b912e0de1725db0323da65e9a957336e3f3bcaa0` |
| `sft-code-nemotron-cascade-swe` | `u001.part0005.jsonl` | 300,041,399 | `a04d36ac1233899e1466c5591601226e2e199534feab35b77df24f9beb80e1be` |
| `sft-code-nemotron-cascade-swe` | `u001.part0006.jsonl` | 300,004,701 | `d4decb5f51c9d86979c0730cfdcd8d6b7f10aee3cbba7949baedebed4147a763` |
| `sft-code-nemotron-cascade-swe` | `u000.part0005.jsonl` | 300,006,220 | `ccd1a900fc03fbb434bb1cca351577fe228e35359acf0ac7c2cf7f875c900d1a` |
| `sft-code-nemotron-cascade-swe` | `u001.part0007.jsonl` | 300,029,939 | `d8e4fc3d1ab47cc301083c0eed3077dfc273b3d0e7416457b0563deaf19175c0` |
| `sft-code-nemotron-cascade-swe` | `u000.part0006.jsonl` | 300,015,093 | `ce04f8dceb2ffa7fd383588b6f5375eb176eeaf092c4c72d776bf6cc8c50191a` |
| `sft-code-nemotron-cascade-swe` | `u001.part0008.jsonl` | 300,002,795 | `2e7c0f6f84f18513ebfc13b1005e6148dbec2aed7bfe46418a760cd686639605` |
| `sft-code-nemotron-cascade-swe` | `u000.part0007.jsonl` | 67,028,164 | `8fc73cbb6c96b2e3b485f42efc30a2a7af2c8428364ce1f9886ef529e184ed8b` |
| `sft-code-nemotron-cascade-swe` | `u001.part0009.jsonl` | 300,006,344 | `8e10b3aa2d657d194add7f604b77713cfb33b8123b8c67d63a85295e99daf19a` |
| `sft-code-nemotron-cascade-swe` | `u001.part0010.jsonl` | 300,035,292 | `bd86016017d5ad2b7bc84a1f5ce1f19fdc8fc03585355e3a53646f2b2a4e928f` |
| `sft-code-nemotron-cascade-swe` | `u001.part0011.jsonl` | 300,042,460 | `c7f4d3a92eef520e9da5c0827ca0b4a432872aaf548e7469db4540ce59cf4837` |
| `sft-code-nemotron-cascade-swe` | `u001.part0012.jsonl` | 147,382,344 | `98201ed0fa4c93631122197a1fbc02351ee329d58cd618d84b7769abb0b18d37` |
| `sft-code-nemotron-cuda` | `code-nemotron-cuda.jsonl` | 82,578,942 | `af858d047eb12146110c7bb815e1814248faac6d439549d8482a8747bdcace6c` |
| `sft-code-nemotron-opencode` | `u000.part0000.jsonl` | 300,027,436 | `f199e01ab57e50834def8797c7deaf062bda3d13a987a9e77874d8b9b5b942fc` |
| `sft-code-nemotron-opencode` | `u000.part0001.jsonl` | 300,003,280 | `a4fde85ca5b3322f13233cc755bdcf375449d9bbfdb0a00c3715f97deeae1b3f` |
| `sft-code-nemotron-opencode` | `u000.part0002.jsonl` | 300,055,130 | `a4237a852a0f63d9c7db7ecba7b114b3c934e052e64111e03a1954f83e889489` |
| `sft-code-nemotron-opencode` | `u000.part0003.jsonl` | 300,142,037 | `14a55f5b32c65d4175fc242afafb78259c588d25ecf5f085831ce63b08cfefdb` |
| `sft-code-nemotron-opencode` | `u000.part0004.jsonl` | 300,107,147 | `f5b7ba091f7d8a132d3420288256429ecc8e3f31353c1f6025c1c754ac8bf931` |
| `sft-code-nemotron-opencode` | `u000.part0005.jsonl` | 300,042,014 | `8ecd0529c3dca75acd5c16d80364910f46dbdb4bf195d92aae5710ce1c82d560` |
| `sft-code-nemotron-opencode` | `u000.part0006.jsonl` | 300,023,240 | `48f1d8edc45534db459f74fc64ddd44c40aafb832517652a73bcfd22f7564f53` |
| `sft-code-nemotron-opencode` | `u000.part0007.jsonl` | 300,055,840 | `dac3f0d1f5e32502aaf9bb2b0a90c6980520a1dcd2c76345d7bbf37220452b81` |
| `sft-code-nemotron-opencode` | `u000.part0008.jsonl` | 300,006,626 | `079672017395652515c59862297a7b3eadf570bf77402845e0cb0698aa31adc4` |
| `sft-code-nemotron-opencode` | `u000.part0009.jsonl` | 300,049,132 | `c012434addd2fbf5ed430e4fc82e4466ff404498edbb802aba80cb41f45c7673` |
| `sft-code-nemotron-opencode` | `u000.part0010.jsonl` | 300,009,665 | `d6bc1a5ef7952d4747afaec7df0c7c558407535352cde7361bcd710be87427d3` |
| `sft-code-nemotron-opencode` | `u000.part0011.jsonl` | 300,061,542 | `7fcbdfaacc0e51cc6d7ab62b54ccc2ca9e8760b54a1f322dab5b037eb6ad5a72` |
| `sft-code-nemotron-opencode` | `u000.part0012.jsonl` | 300,180,450 | `0a95ac019c14f3187cc7efca02dce59890a94e2fb40361892653a0c4f5577f7e` |
| `sft-code-nemotron-opencode` | `u000.part0013.jsonl` | 300,002,540 | `049188c4b5ad3b05d7807480498cb11e343b5a7e5cb6f2e1c9f0c798ef773512` |
| `sft-code-nemotron-opencode` | `u000.part0014.jsonl` | 300,114,273 | `e69f30651e4a99128c034f26830e5fe9580013e7bd8e09891f85ca0f67958ed1` |
| `sft-code-nemotron-opencode` | `u000.part0015.jsonl` | 300,033,847 | `c7e35dc81fcea3f8a3e966466a985dcd043d89d9970bda8520c809c62e83d8a7` |
| `sft-code-nemotron-opencode` | `u000.part0016.jsonl` | 300,012,474 | `d89c6666fa5cef7de819890a21cfa45ff90ddefe4a18ea13f1ffd5c0e82e18b1` |
| `sft-code-nemotron-opencode` | `u000.part0017.jsonl` | 300,037,260 | `d51c415a6240072ea57664c86d81f60fc1e19e8c2f6d9a7000d02c0c7732bd32` |
| `sft-code-nemotron-opencode` | `u000.part0018.jsonl` | 300,136,923 | `780a321855b49a543424510e0e5339b66d3769a33ac76a30535e5b42b03187f7` |
| `sft-code-nemotron-opencode` | `u000.part0019.jsonl` | 300,084,880 | `860ae3a0df4a3ecf64eb720e45e4f7927a1f07e9ee62d3f1321f20e01ea97e53` |
| `sft-code-nemotron-opencode` | `u000.part0020.jsonl` | 247,859,056 | `f402b34105e68b9bcfa5e12edee42f4f3f1cc16cde12f975493852e5a224b067` |
| `sft-code-nemotron-terminal` | `code-nemotron-terminal.jsonl` | 2,231,536,740 | `445c53c776d693214ab7fdf73e8ebdc1e17430a95584f1d3d8a57631226056f5` |
| `sft-code-opencodereasoning` | `u027.part0000.jsonl` | 300,012,540 | `0e4a528b6e975384362e7baf31e47f1ddebdf0d94979f70021ca49930a3810e8` |
| `sft-code-opencodereasoning` | `u027.part0001.jsonl` | 300,001,966 | `0acd4bb64538aeb61894f7055325189a3947f788977d68f3621908c25273ef9d` |
| `sft-code-opencodereasoning` | `u027.part0002.jsonl` | 300,004,178 | `cf5c1f4d2251c47c9be833e9898296b4475a28b6e9997958ef4481da67766fc7` |
| `sft-code-opencodereasoning` | `u027.part0003.jsonl` | 31,412,454 | `768ac93a55a943fd9d26f32b270bcc5bdf90cd66d40244f3db998e8c9be2b245` |
| `sft-code-opencodereasoning` | `u026.part0000.jsonl` | 300,010,251 | `278c4fcccd5e087f9295a1e740ef932d479d805e7b43a6f419e8e864f6ab0c69` |
| `sft-code-opencodereasoning` | `u020.part0000.jsonl` | 300,027,650 | `88dfe3ed4d56a8575cb0babdaad65f92a70efe1cfae4649fa20855fa7fe7bc5b` |
| `sft-code-opencodereasoning` | `u026.part0001.jsonl` | 300,002,889 | `f6c37dc8f7f46329a502927c062a15e07a87fdb52a9d016795cf7f4eb9faf2cb` |
| `sft-code-opencodereasoning` | `u020.part0001.jsonl` | 300,030,648 | `fa84a355413f411270d32328c62fdb91ef15ecc1667cfa3915649a4b6cf896fe` |
| `sft-code-opencodereasoning` | `u020.part0002.jsonl` | 175,058,409 | `7175cbfafaf8afb32677a6314f17d30cc66b2c1467854884c1aea00c91944ca1` |
| `sft-code-opencodereasoning` | `u026.part0002.jsonl` | 300,018,454 | `2452b911a62f062d3daf85eb102da11d376480e7afbe4b57015be9289f15b335` |
| `sft-code-opencodereasoning` | `u026.part0003.jsonl` | 31,597,822 | `48f59160c5801e9706a5425ecddac3b83184cb74bdc37a9c5cb302f8b28d6b6d` |
| `sft-code-opencodereasoning` | `u021.part0000.jsonl` | 300,038,045 | `f4666f84d3c8fb581d755750f865caf891a2a6a56f26cfd11ea7f5807314d7c1` |
| `sft-code-opencodereasoning` | `u021.part0001.jsonl` | 300,052,635 | `b03b4a98b4035486ff6edc6ff5655a6254b1750694f195b77073e5b1d63a4ad3` |
| `sft-code-opencodereasoning` | `u028.part0000.jsonl` | 300,053,018 | `82163a472a0b3228278cb2d9fd80f3eccc9a4d487ad1c468116c06accb21c567` |
| `sft-code-opencodereasoning` | `u021.part0002.jsonl` | 300,048,483 | `22192bcaa8aec11f53cb5de0de9b894ab161a3525d31c129afc85ce0121fa794` |
| `sft-code-opencodereasoning` | `u021.part0003.jsonl` | 34,699,895 | `e48d0d059835626fac62ae4ac6ca71465ad8a64ea8cfc12c39d6c1ef8f199d9f` |
| `sft-code-opencodereasoning` | `u028.part0001.jsonl` | 300,019,940 | `797d2545035bf7d4e56defd0dbcb9ce63ff6b5c925a2ed5bb402a807e4147436` |
| `sft-code-opencodereasoning` | `u023.part0000.jsonl` | 300,042,729 | `b10bbd01b02e2ec43d555abde813757ac9ee3d55c69d7cf55fbc36cd828d21f9` |
| `sft-code-opencodereasoning` | `u022.part0000.jsonl` | 300,013,679 | `13c6adb6b27588e7c6f22c9b06f4b8f6cca6ad475bc6ceb8b641ad20d540f64c` |
| `sft-code-opencodereasoning` | `u029.part0000.jsonl` | 300,021,393 | `2de9562e53c26567adf182006fbafe7611e79ba829725cd568607fc0bb61746f` |
| `sft-code-opencodereasoning` | `u028.part0002.jsonl` | 300,051,640 | `3df7fb09f988d8a2d5a4309a856b641c1d743f3f0b14f5df2e8297d699b87393` |
| `sft-code-opencodereasoning` | `u028.part0003.jsonl` | 27,515,709 | `0a8d450390ea3dac3bf0239a18f1e09194ac3a03650c3d4fa7188ee1e45f052f` |
| `sft-code-opencodereasoning` | `u023.part0001.jsonl` | 300,008,115 | `a95bda702da23318cd94a495457fcf2d3f146832fb13e7caa24344309f15cb2b` |
| `sft-code-opencodereasoning` | `u022.part0001.jsonl` | 300,035,380 | `f007b77e32700c135f3fc0fd84e3c5e7c72a0d7a54368d941cdee018f5b103c6` |
| `sft-code-opencodereasoning` | `u029.part0001.jsonl` | 300,050,786 | `ed5870eb651a2c4038bfca130599f6fc9846656487ef1ff7b2c5b7a7ccd68f51` |
| `sft-code-opencodereasoning` | `u023.part0002.jsonl` | 178,492,709 | `3c0355152aac9d5dc6aa4c23726eb4eae380a41f120473157ddfd4e206ded6a2` |
| `sft-code-opencodereasoning` | `u022.part0002.jsonl` | 300,015,686 | `fe08d2f60a3594436b0a928bb3058218626da67b30a305545e74bf5dd7ea0e9b` |
| `sft-code-opencodereasoning` | `u022.part0003.jsonl` | 33,410,048 | `10d5b4c6bb80744643eff36108b9ad59a3c0af9f0c0e4b4c94136d1d96cb6557` |
| `sft-code-opencodereasoning` | `u029.part0002.jsonl` | 300,011,763 | `854eeff90d55d0c2846f80eae3c4aee155d196cd3f64c744d2979b78e8b93057` |
| `sft-code-opencodereasoning` | `u029.part0003.jsonl` | 28,153,451 | `2138b87160628ff04d5e5180e00012dc7caaa68c51cfe59d50a382c8fc0d9604` |
| `sft-code-opencodereasoning` | `u025.part0000.jsonl` | 300,040,333 | `e569ffb8c3e27c9ba70ad57c24487c3e522e13b2fed585cf2cadb119568db1d8` |
| `sft-code-opencodereasoning` | `u025.part0001.jsonl` | 300,025,829 | `ee1c06dabc9081257a43416419a28156b4dad00c0a513d0f3d94f24c2de1a451` |
| `sft-code-opencodereasoning` | `u025.part0002.jsonl` | 7,413,040 | `f403a84dadf63fd470156caa8b20f2d6d5a9d8769d4bff4f417599cb03507495` |
| `sft-code-opencodereasoning` | `u007.part0000.jsonl` | 300,006,622 | `793be240cae2448058027ec52081c65566a47d868baed67f55af2ed3eb9a3397` |
| `sft-code-opencodereasoning` | `u014.part0000.jsonl` | 300,016,589 | `4f51f0f4ce119ba97e39794d96ebab9609150760058e439e345c2457dcd02587` |
| `sft-code-opencodereasoning` | `u015.part0000.jsonl` | 300,002,468 | `f3b3a0b47a86509d068e6c919bd1aab64f3aa5223e1d2f065d46f2f9173ffc06` |
| `sft-code-opencodereasoning` | `u007.part0001.jsonl` | 270,299,793 | `2c6ea142df98144432968415e9b66356751054cb6e921650eabcf249495d25c5` |
| `sft-code-opencodereasoning` | `u008.part0000.jsonl` | 300,024,950 | `91eeb167b697037532f4d7e4bacb8435ca42126dfdd62cc79958fc739af6da42` |
| `sft-code-opencodereasoning` | `u014.part0001.jsonl` | 270,447,359 | `0680729f897d74f6c7436386d443f652c35df1d4e1cd89c8f44ae9912ccadb34` |
| `sft-code-opencodereasoning` | `u017.part0000.jsonl` | 300,020,537 | `c73516e1935a8144e286df2147b36d95bdd1cdcd1353d5dd13fb2183d659a6c4` |
| `sft-code-opencodereasoning` | `u015.part0001.jsonl` | 270,422,887 | `9fa51f6a334bc0472f2c6540dc1e19f588ce5b0abb50b0927ae59cf242610393` |
| `sft-code-opencodereasoning` | `u008.part0001.jsonl` | 270,620,095 | `0ef51894e4e702c8294cefca583ab7ea3c461e98f2bdf8bed1460346339743c5` |
| `sft-code-opencodereasoning` | `u018.part0000.jsonl` | 300,054,694 | `642c34b1a1b14d0380483625ec23d4c9c7f263b21be16a61c71b040fdfd6214a` |
| `sft-code-opencodereasoning` | `u017.part0001.jsonl` | 269,660,775 | `126fe01b17b3cae371fbec7657419506b5e0a8905c8880efe5d5dd5ea008067b` |
| `sft-code-opencodereasoning` | `u016.part0000.jsonl` | 300,002,547 | `a51cfe35c13b35dec0ac4e329790425bde1c2cce3ebdceba356c8eff53c666ce` |
| `sft-code-opencodereasoning` | `u011.part0000.jsonl` | 300,003,139 | `c1a478a1789c91497ad46e03409b3dddabccc94e47e139e0fadea20626f06f18` |
| `sft-code-opencodereasoning` | `u018.part0001.jsonl` | 269,900,232 | `c4c7828ac7a8cff413f7dc288656bf885d531d2db4744ebfb33f73608c5a4ce9` |
| `sft-code-opencodereasoning` | `u019.part0000.jsonl` | 300,007,423 | `d4eb086f600152150fc2ce09f7d9f98a7d03a5b2b7687e823d737e155034b65a` |
| `sft-code-opencodereasoning` | `u016.part0001.jsonl` | 270,105,572 | `6215389c9a7aaac98061d8232b3acc085ed375162134ca5d35e4134773d0117f` |
| `sft-code-opencodereasoning` | `u005.part0000.jsonl` | 300,019,499 | `4077237ee65b14103a1d35ebb99c559a97aa3b39a49e2874d515d40893ab039d` |
| `sft-code-opencodereasoning` | `u011.part0001.jsonl` | 269,547,307 | `5799a770e5daf3118f218174256e3d50e10bf5167299ab43c707aeffd5bd607f` |
| `sft-code-opencodereasoning` | `u019.part0001.jsonl` | 269,219,457 | `576f8c5057cce1ab7414a6d3bba699a8872377ea06c6f046406b85ef66952e76` |
| `sft-code-opencodereasoning` | `u000.part0000.jsonl` | 300,017,361 | `85e95b7ef98a6b0acce9c6280a3edb44af4abc33cdfb6743eac7846b32131c59` |
| `sft-code-opencodereasoning` | `u005.part0001.jsonl` | 269,098,297 | `6e45af60c76de8bee5f5b36fe5cfb762ea7d5bb263bbd122da247970c50f4844` |
| `sft-code-opencodereasoning` | `u010.part0000.jsonl` | 300,019,937 | `7a8982886e8724de72396e440ef002dc45a81f64b603e96a1408ae11e6e7dba0` |
| `sft-code-opencodereasoning` | `u002.part0000.jsonl` | 300,022,533 | `4be88ab10aec7854e8a455586ec10b41e78ec4c7bc74aec3061b295a80945d6b` |
| `sft-code-opencodereasoning` | `u000.part0001.jsonl` | 268,957,661 | `ae683ae6dd85f83c8307b7400328948374341a3875669068ffc91490e310caf4` |
| `sft-code-opencodereasoning` | `u006.part0000.jsonl` | 300,000,194 | `cdc2ae71e9d4c0291c17dcaca9be4b649fa2a8a80e241eff7490f5dc4bb3c2fd` |
| `sft-code-opencodereasoning` | `u010.part0001.jsonl` | 269,100,297 | `0f245d744f7c9041a0c420253c986d8028488a7793d76653db12064d46e97307` |
| `sft-code-opencodereasoning` | `u002.part0001.jsonl` | 268,764,463 | `329cf3af0ec1f6f4384a3530d987f18d240a15e59d168449fa9694ed999ecd5f` |
| `sft-code-opencodereasoning` | `u012.part0000.jsonl` | 300,017,149 | `cbbe74ceabd8035c2212fa79d2162d3e3633b121faa84db3f1d1872b08b6d246` |
| `sft-code-opencodereasoning` | `u006.part0001.jsonl` | 269,317,400 | `39074fecbec0dc342b7633bd5993bd80809d1818b0534f600a212e1bafaa7d77` |
| `sft-code-opencodereasoning` | `u003.part0000.jsonl` | 300,005,875 | `dee833ed75e683d556ded3c76b69e7bf7e5a0f26af317f61ff6ad9281adee987` |
| `sft-code-opencodereasoning` | `u012.part0001.jsonl` | 268,794,072 | `f201cf0ed0476e10270efa6b06a986e0f01eebd6a558f061a1de09a2f040673b` |
| `sft-code-opencodereasoning` | `u001.part0000.jsonl` | 300,011,404 | `e3693baac107a104ac123e6c3a37b5e9ce55cbe3ddc06e0db5e614d2c165f451` |
| `sft-code-opencodereasoning` | `u013.part0000.jsonl` | 300,045,183 | `f6f19ac4fd8e7bd3e5767bbb245c995f3591c4a9c1c4080c6b918c332f53b8c5` |
| `sft-code-opencodereasoning` | `u003.part0001.jsonl` | 268,627,667 | `119b0421017d16aa1376aa4e0bb640ad32cd784d5886275656dd322288cb4507` |
| `sft-code-opencodereasoning` | `u009.part0000.jsonl` | 300,001,179 | `5a6b58f7cc7b332ec5fe3b3723e3b74926eb63929cf0da90aee610d4f9cd53a2` |
| `sft-code-opencodereasoning` | `u001.part0001.jsonl` | 267,926,553 | `53c6c59ed631febf4d16c247902c728792feb3c6132c9a3a183b78637cd2f2ed` |
| `sft-code-opencodereasoning` | `u004.part0000.jsonl` | 300,000,163 | `576c3a057260de423a683474365012d2c6dca96455b140dc37a6f99a84826f5f` |
| `sft-code-opencodereasoning` | `u013.part0001.jsonl` | 267,747,970 | `547ab86f8545d5fd7e7b01114ddac236b780c18e204f88e26202c1b72536f002` |
| `sft-code-opencodereasoning` | `u009.part0001.jsonl` | 267,851,201 | `78c60bcc7ad5c5629332a0bb6a2be7c4830aa4747171cef01718e2a3411417a9` |
| `sft-code-opencodereasoning` | `u024.part0000.jsonl` | 300,000,216 | `8fb329faa80af96f9412275bac0df13a5f4d983692acd1317b261d257381c381` |
| `sft-code-opencodereasoning` | `u004.part0001.jsonl` | 266,729,611 | `e1befd56e074ad6c8f54cda1459018571b85f6c188276f8e1ffc728791a7be50` |
| `sft-code-opencodereasoning` | `u024.part0001.jsonl` | 268,947,924 | `d25953f5f4d06c05875c5d9b4bc7e6e55d3f69e32ffc0bfa0956bdc53fa460ab` |
| `sft-code-swe-rebench-openhands` | `code-swe-rebench-openhands.jsonl` | 6,432,083,124 | `f2c910ec7ccda9fea8b26b58958a353336a3465e020f495f14d103d9d9319dda` |
| `sft-code-swe-zero-openhands` | `u051.part0000.jsonl` | 300,046,774 | `d5d85e49d50a46e94499bdb09b70af404d009dda1a8593fbb30e5bef4ac8ddc5` |
| `sft-code-swe-zero-openhands` | `u045.part0000.jsonl` | 300,150,459 | `e20dbc865f0a95f190d2685f11da97003b8a7e640d80e92ca3bda5660df7a99f` |
| `sft-code-swe-zero-openhands` | `u051.part0001.jsonl` | 300,187,625 | `ed98415246eb34b0b07116a31da90ceb6f8c5d86db173e0376c8d1ffb13d0732` |
| `sft-code-swe-zero-openhands` | `u045.part0001.jsonl` | 300,064,551 | `bbab6721312cc6a418018adec516b837f8cf25028c336052595d14a3dae1a59c` |
| `sft-code-swe-zero-openhands` | `u051.part0002.jsonl` | 69,558,826 | `82344cd4a39bb4fdcedeb7a61ba7bf2a7ab26627d83bcacb3ee3555b77cb225e` |
| `sft-code-swe-zero-openhands` | `u045.part0002.jsonl` | 33,953,867 | `86b2e59de5d2bf86484155cf84337d907a95a0af3b465c53f0aa8612a684ca3f` |
| `sft-code-swe-zero-openhands` | `u048.part0000.jsonl` | 300,102,355 | `2534532e52507f5aa7a65acaf950edd6aa4064064dd5fe5bc236497b1d1066cc` |
| `sft-code-swe-zero-openhands` | `u050.part0000.jsonl` | 300,031,838 | `8d93bd9845d160bea21655cbe94c9ecfd6eda52f0d86b71f1764f83673f6b55b` |
| `sft-code-swe-zero-openhands` | `u047.part0000.jsonl` | 300,062,026 | `b55f7d45b72a878e05471c176f4d2591a480d40f521365a1fd62595775c0f66a` |
| `sft-code-swe-zero-openhands` | `u048.part0001.jsonl` | 300,093,022 | `9112369a8a00036b4ccdee43a81e492ce407fb650862a2db2408478566755e69` |
| `sft-code-swe-zero-openhands` | `u052.part0000.jsonl` | 300,070,599 | `6fa64495246412f5a5677564b83f3b10f190c866fa846b71c54da5b2f711dc91` |
| `sft-code-swe-zero-openhands` | `u048.part0002.jsonl` | 42,519,796 | `d954c774c450913e28a0acc4fcd4df5950be13f5cacd1017e0f1bc16a9ae5278` |
| `sft-code-swe-zero-openhands` | `u050.part0001.jsonl` | 300,028,446 | `8277a9777c70447473191b901659bd26ac5c2b9704babdbade4f34f3eb5e8160` |
| `sft-code-swe-zero-openhands` | `u047.part0001.jsonl` | 300,012,148 | `8f936712e160047d28bba82e65e138a68dd81863ccfbaa5274b2ebd522457669` |
| `sft-code-swe-zero-openhands` | `u050.part0002.jsonl` | 51,266,730 | `8834385b15efe898fa639aa17be7549f8efc24c465789e9dfa2fb3482ebc0f6e` |
| `sft-code-swe-zero-openhands` | `u047.part0002.jsonl` | 44,542,409 | `2ef9cd732aef67d1643124f49766b4151b4ea0d774b3ee05330027327695eaa2` |
| `sft-code-swe-zero-openhands` | `u046.part0000.jsonl` | 300,036,714 | `14ddf398b883e7464ec36990750fb282633d609b8ff5c53e5fe1f3534932b4b7` |
| `sft-code-swe-zero-openhands` | `u049.part0000.jsonl` | 300,098,211 | `56c99f562de0ce23d390ea022896d3b37cf9750db660658b1458902aaaf692b5` |
| `sft-code-swe-zero-openhands` | `u052.part0001.jsonl` | 300,060,199 | `de9d10da6602b5d982a6516813b5e88ec598429c7eae1d8ccd93fc925ce043a5` |
| `sft-code-swe-zero-openhands` | `u052.part0002.jsonl` | 85,293,272 | `f747c12f03f01590baf570dc4263b9405f1892d377fe29e1f520e5411b0f98c7` |
| `sft-code-swe-zero-openhands` | `u046.part0001.jsonl` | 300,045,659 | `625e9589fcecc422527256399f8b66d81ffd7cbb3109b01c1acde4e66071af65` |
| `sft-code-swe-zero-openhands` | `u049.part0001.jsonl` | 300,065,991 | `28565ca48f1882d9da5a9be58c580700acf7bddbb17be4b162cb6787064b4401` |
| `sft-code-swe-zero-openhands` | `u046.part0002.jsonl` | 39,013,935 | `5dfe5d0aa8a3a6e9805d772e97794eac7e60717a9f18a92554f4acdaf25cd741` |
| `sft-code-swe-zero-openhands` | `u049.part0002.jsonl` | 39,225,032 | `b9cbb5ec2f28cf75e01f6b981b28fb0031e673fe39ad40eb1b835d756a155c4a` |
| `sft-code-swe-zero-openhands` | `u044.part0000.jsonl` | 300,070,849 | `88c52568118aa89c90927964ae3824f42d8e4b047cfc2391ddb44246c71b393c` |
| `sft-code-swe-zero-openhands` | `u042.part0000.jsonl` | 300,083,291 | `ecf5b3b97abfd4143b06c574b32091dd07ab7cc0bea577ec68652509e67bcb4e` |
| `sft-code-swe-zero-openhands` | `u044.part0001.jsonl` | 300,030,212 | `0940ffab0590553bbd37880c39aee920e32df03d4ad0e04592fb8f7253bbaa02` |
| `sft-code-swe-zero-openhands` | `u044.part0002.jsonl` | 33,356,579 | `6165d89469c9c5130fb30b4822ac6f0fea93749dd2f172ec684dd5a50e2ec8f4` |
| `sft-code-swe-zero-openhands` | `u042.part0001.jsonl` | 286,098,097 | `0fc9d5d014bca0a15950d75000ac0f3afed8d7eaacc5bfab49742e7818c0bc6c` |
| `sft-code-swe-zero-openhands` | `u043.part0000.jsonl` | 300,047,467 | `67e798c632faaddfa2b7d0296c7ec2a93acc08bae5534a38e44df5bcb75d0a99` |
| `sft-code-swe-zero-openhands` | `u038.part0000.jsonl` | 300,008,731 | `7ae974e1ce31de65201f6842af357b9d9fef52264712bb15f41b31c575f39260` |
| `sft-code-swe-zero-openhands` | `u043.part0001.jsonl` | 289,582,629 | `30a2ac1b8744f753007f86f179ce648ad73cce8902dd00dbc504120a64229770` |
| `sft-code-swe-zero-openhands` | `u038.part0001.jsonl` | 259,797,047 | `643257f749e2122b7c6b8a67bf898e1b0fdec3ddac6e9b2e110b4ec58ce41a08` |
| `sft-code-swe-zero-openhands` | `u040.part0000.jsonl` | 300,076,641 | `ec0818dfd860a2849a411af0f0932d7747be929605ff4912862c0079fa55617b` |
| `sft-code-swe-zero-openhands` | `u062.part0000.jsonl` | 300,046,264 | `63124fbb0cabda12b51f5672afcaa386e8a57a674c049aa49a9fdf6c03856f7a` |
| `sft-code-swe-zero-openhands` | `u040.part0001.jsonl` | 282,642,225 | `a666ed04e6c39d8fe5c9ef8c2c7a1616063e0fc7e4ddfdcdba326616c392b2e2` |
| `sft-code-swe-zero-openhands` | `u062.part0001.jsonl` | 279,906,783 | `c04483a3b1751de61279bc61fc7ccf7c075f6ecdedbf9327d13396ab8987e9bd` |
| `sft-code-swe-zero-openhands` | `u041.part0000.jsonl` | 300,026,269 | `254bf1c0eb8466b83cceaff4a765642e2b0a672063f514ba67b9faafb1d2e09a` |
| `sft-code-swe-zero-openhands` | `u041.part0001.jsonl` | 281,984,411 | `514938e4258daa683111188ddd405dc03697495a04d606d5337ca7302068e735` |
| `sft-code-swe-zero-openhands` | `u034.part0000.jsonl` | 300,009,326 | `a4288f4df16b9675266d277b578698aa88a2f5d618c9d4286c93d74f97172115` |
| `sft-code-swe-zero-openhands` | `u034.part0001.jsonl` | 260,627,151 | `60e3ef0159541fc834e33254dce581864b0408b581939303f7793ef586a36757` |
| `sft-code-swe-zero-openhands` | `u036.part0000.jsonl` | 300,133,482 | `8663c9b2ea0bbb3a9ac855d7422f2bd6c3be5e3301880a87d7690e35176dd0f0` |
| `sft-code-swe-zero-openhands` | `u036.part0001.jsonl` | 262,812,942 | `082641367ebf53fb7a5a67b4775a2007c3d024f9518719b21401e8252b632d35` |
| `sft-code-swe-zero-openhands` | `u039.part0000.jsonl` | 300,032,802 | `25240467a96e107ee6d3cc7645a83f685a63665a1c124f24ad7275dde3f1e4c2` |
| `sft-code-swe-zero-openhands` | `u039.part0001.jsonl` | 260,517,829 | `7162b055f8bfdfd3d84faf308d4d655aeaa9de2b9d6f84cebaef7c0121675518` |
| `sft-code-swe-zero-openhands` | `u035.part0000.jsonl` | 300,125,560 | `ca13a54578618afe79f63541e45cfa3e682162a5e3d9afc5d3165fb9c767628d` |
| `sft-code-swe-zero-openhands` | `u035.part0001.jsonl` | 257,066,891 | `16181310dbee33773a12ea8fc6cde0d78d1ffff7e604156b8d26baaaa8787ba2` |
| `sft-code-swe-zero-openhands` | `u037.part0000.jsonl` | 300,077,761 | `70eacc86e9ab7c20506194c19e78e36353c33ae3921f2f4972ae21c6a6a63218` |
| `sft-code-swe-zero-openhands` | `u037.part0001.jsonl` | 257,730,683 | `deb648799c828950abb14f39467133c964a6efc60f382bf6d1c07ef6c6aa893c` |
| `sft-code-swe-zero-openhands` | `u009.part0000.jsonl` | 300,066,146 | `1c7d46a85b55d2b0c09f8ac9a29c38a35a44f750e48b0bec7b699f7dc629aaa1` |
| `sft-code-swe-zero-openhands` | `u009.part0001.jsonl` | 224,294,229 | `266d3737ed67c97c38ee0a828e50812d0a47d3a5b82c8262f577f18b8e8f16a0` |
| `sft-code-swe-zero-openhands` | `u061.part0000.jsonl` | 300,048,324 | `eebd20dcd1efe9529884722ac45c4b4b42ed84508c331b00f97721536e2c27bb` |
| `sft-code-swe-zero-openhands` | `u061.part0001.jsonl` | 253,774,686 | `0fb34e3a35665e74fa3499e624159dde58c69df5b32c1f24749dc63c6455de02` |
| `sft-code-swe-zero-openhands` | `u030.part0000.jsonl` | 300,029,063 | `65c2ffcfb61d3471afae3e25ce4fb35944323bee1893e087ac4a898465e9fa48` |
| `sft-code-swe-zero-openhands` | `u030.part0001.jsonl` | 222,774,007 | `91fcb9775f517e9e752de92469ec3efefb99bf8e5912c299c686722f33968038` |
| `sft-code-swe-zero-openhands` | `u056.part0000.jsonl` | 300,019,982 | `7dc31d9f326b6cefd630de74443dc3918916f273947a9ebc28e4b20f1fd65451` |
| `sft-code-swe-zero-openhands` | `u053.part0000.jsonl` | 300,028,076 | `fd0b633feb056010bbc47aee9b5590513208b6b170ca504ed70861e6c8830308` |
| `sft-code-swe-zero-openhands` | `u056.part0001.jsonl` | 223,328,777 | `7de8cb796405730419462e5be9c17f759bd643e728f7fa154176907f143b0d73` |
| `sft-code-swe-zero-openhands` | `u053.part0001.jsonl` | 240,281,446 | `381051e4f76e5a48ceca2efcf4a5f2adf40ef7ac6c4d6e8b4e3b2827c0d7e207` |
| `sft-code-swe-zero-openhands` | `u033.part0000.jsonl` | 300,048,958 | `a5360c788125ad35535138b3c99fac127777b710bc541404b7725dcde5369c8b` |
| `sft-code-swe-zero-openhands` | `u004.part0000.jsonl` | 300,088,855 | `c1de12e994023c65f6341508ad946834b323e0fed19174d526d6e6ddc1aa3cc2` |
| `sft-code-swe-zero-openhands` | `u033.part0001.jsonl` | 234,847,100 | `6f91c1bcb0edaa0a98e3ab29a7c3d174e8d2533ff4da853f503e433984e53369` |
| `sft-code-swe-zero-openhands` | `u004.part0001.jsonl` | 221,696,750 | `2402317045e1550e9d849a934703e028b07a772933e8dbd4cc21266c5ffbabe7` |
| `sft-code-swe-zero-openhands` | `u020.part0000.jsonl` | 300,164,785 | `75f676ec9a86c9d30af58bde0a41b4681397fb246f4c9f713e3c7340bf2451ab` |
| `sft-code-swe-zero-openhands` | `u020.part0001.jsonl` | 222,679,158 | `6e281f93c49dcc77f4ec069756e89de380c2f9898e372ca4364e8ce78d8e74ec` |
| `sft-code-swe-zero-openhands` | `u021.part0000.jsonl` | 300,017,275 | `8aa78719cbcfba78f1de18151e11ac928e725ec01faad711099a4d33b774e05d` |
| `sft-code-swe-zero-openhands` | `u021.part0001.jsonl` | 229,820,829 | `aa58e78b3b7facb2e2d8efb0aeb4f7b19403d4de77562b532876a6d94a2fc3ad` |
| `sft-code-swe-zero-openhands` | `u010.part0000.jsonl` | 300,069,688 | `575408f4fc5cfcb6443735d75cebf8f2e559e8a7df8b8e6d92e7d71587c3468b` |
| `sft-code-swe-zero-openhands` | `u010.part0001.jsonl` | 231,565,016 | `590e64d00efb6aa53a91ae8067ca14be03a1ef044f050c57b7af2fa930032de5` |
| `sft-code-swe-zero-openhands` | `u027.part0000.jsonl` | 300,057,116 | `04d05981b6081febc6b42742687d42f8360ae4fae4bc88136823b44627f701d2` |
| `sft-code-swe-zero-openhands` | `u027.part0001.jsonl` | 227,834,940 | `7feb155ade02d8138b76fffc762adea850101b232c10e14513700e0ebea0a80a` |
| `sft-code-swe-zero-openhands` | `u026.part0000.jsonl` | 300,006,474 | `8d429869ef771fdb0b959054146fe9b5c7f4c53aecc5f0ed6ff1b7225859cee5` |
| `sft-code-swe-zero-openhands` | `u026.part0001.jsonl` | 228,609,540 | `c81947dbe93e47ece4df581d6d84fd7276d2cf1b9c578a2cea49b8a70e2b1167` |
| `sft-code-swe-zero-openhands` | `u029.part0000.jsonl` | 300,076,665 | `8b41ba5951de48004b3e843d0db794dc41a04e9595cfff269df530a54852b57f` |
| `sft-code-swe-zero-openhands` | `u029.part0001.jsonl` | 226,863,475 | `e7bb715f77c9274203b643c61722ac8e4747a691f6ea8ad00589cb77b882dc0f` |
| `sft-code-swe-zero-openhands` | `u013.part0000.jsonl` | 300,105,476 | `23da618bf439cea613c972090752552ca9c89da167bbabc1273c8126b90ee96a` |
| `sft-code-swe-zero-openhands` | `u013.part0001.jsonl` | 220,410,838 | `d2454a9f88bca430dc5a770951004fc4386d27bf53e52ed70bf6a74e602638dc` |
| `sft-code-swe-zero-openhands` | `u008.part0000.jsonl` | 300,073,998 | `087ae8784842e2347266a804645515c8832e9ca3f21632080d96ad099f02ab1b` |
| `sft-code-swe-zero-openhands` | `u008.part0001.jsonl` | 224,869,646 | `2fe31909c33b175b9c48f3dd00a6c128ebaa097dafa4449a6318825e3dbdcc6d` |
| `sft-code-swe-zero-openhands` | `u005.part0000.jsonl` | 300,013,363 | `8c1fe3ea5ff024c0effeeea06ddee9f2ab74237fb33ab38131ad09697711ca0c` |
| `sft-code-swe-zero-openhands` | `u005.part0001.jsonl` | 220,751,569 | `2020515e0d62a60edc7dd07e63536750e767096b96812d477a29a72d50d7aa57` |
| `sft-code-swe-zero-openhands` | `u031.part0000.jsonl` | 300,011,295 | `f91c4a301a1fa951277adffdb90b2fb17de6505fe04a5aeae8fff42a9440c54f` |
| `sft-code-swe-zero-openhands` | `u031.part0001.jsonl` | 226,669,051 | `4a35f89b93ac92b6a9490c89b52d5f05b29324ac1a13f8fb4c27884a78a03c2a` |
| `sft-code-swe-zero-openhands` | `u022.part0000.jsonl` | 300,054,557 | `ad8090a8637dce201308282c38cea49d9cdbf335e58067e1583ff10cce7ef49e` |
| `sft-code-swe-zero-openhands` | `u022.part0001.jsonl` | 227,524,515 | `7b6d5a13266e272a28a6be9cdaf9360679b71075c31d3dc29a4c52c2c369e9b9` |
| `sft-code-swe-zero-openhands` | `u015.part0000.jsonl` | 300,008,517 | `c433a5a65a40f4f5a7e90e4afe446dbadb8da110a212f92073e65eb4c0ad16b9` |
| `sft-code-swe-zero-openhands` | `u015.part0001.jsonl` | 224,836,399 | `44ac19aa9d81e2ea19f9663a105e978b6b14f65b22614ce6ba63bf1213b4b941` |
| `sft-code-swe-zero-openhands` | `u018.part0000.jsonl` | 300,059,288 | `0ea96826256446fc3be9b85ea175ea10fbc22bcab59ff0eeb637c19edb33eeec` |
| `sft-code-swe-zero-openhands` | `u018.part0001.jsonl` | 227,070,136 | `c53e59610664f7f56fb86419d29e21143ebcc89f28ec0a1474ae691e3a57d439` |
| `sft-code-swe-zero-openhands` | `u006.part0000.jsonl` | 300,010,750 | `a5956a34790302b58b2c9bfb933a2e57f27d32f4e4f79b37e13388035c41d852` |
| `sft-code-swe-zero-openhands` | `u006.part0001.jsonl` | 222,434,990 | `25b5881ee92b91510ae1422247a1991dcf8915ba6c1a390b6e624248a16b88b0` |
| `sft-code-swe-zero-openhands` | `u023.part0000.jsonl` | 300,068,149 | `17b3042c40b1d3276d1272f7fcac9035f6332335921b641c7385b8318c22c0a0` |
| `sft-code-swe-zero-openhands` | `u023.part0001.jsonl` | 225,977,033 | `227893d4cddc91a5c8d21584061769bbafdbf87f181e2d93fd02a3e8c1efe629` |
| `sft-code-swe-zero-openhands` | `u011.part0000.jsonl` | 300,071,835 | `a957645304fe115b2adbb149a3432d63a08be08a0510ec0441912f94f81a2017` |
| `sft-code-swe-zero-openhands` | `u012.part0000.jsonl` | 300,073,583 | `5798d80f7ff0bda017e5ac8828f72fd35b1c4e1d578789456e18a5f937707f5e` |
| `sft-code-swe-zero-openhands` | `u011.part0001.jsonl` | 225,868,505 | `6295fb3c9dbf092ccd477e7759c7816cc5c8c93f7c3b45c3b661bd801345daec` |
| `sft-code-swe-zero-openhands` | `u012.part0001.jsonl` | 226,245,624 | `170220ec08eb364aab8328fa3fc76a2afd66e1b9a6c34977c91205ef4725625f` |
| `sft-code-swe-zero-openhands` | `u007.part0000.jsonl` | 300,063,282 | `434b8adba99d021fc8753c0d5af43557145362056bb0d864e06cffc66979df9a` |
| `sft-code-swe-zero-openhands` | `u007.part0001.jsonl` | 223,863,771 | `baafb983f403126508fdb75f29aa1f151b44a9d49cc251f85486f1e4a8660ad5` |
| `sft-code-swe-zero-openhands` | `u060.part0000.jsonl` | 300,018,335 | `4d1d4d6c4d22020dcb761da1c4d74b84d7f85e2dd5dcb6c2309b21c8cbf962f2` |
| `sft-code-swe-zero-openhands` | `u060.part0001.jsonl` | 230,560,447 | `19521a0d4eff06981da97c348c7d64838da8639dd9dcc8718fe23ea727e5e10a` |
| `sft-code-swe-zero-openhands` | `u016.part0000.jsonl` | 300,046,918 | `5e01f5825e377497c78e8e760a18a2a24224f71e4ab7aef8b8c16bec37e67387` |
| `sft-code-swe-zero-openhands` | `u016.part0001.jsonl` | 226,273,462 | `247a21c7427d8ace87f9e60a2638a9e02731e1674b1d2c7dc67f6d19feb85411` |
| `sft-code-swe-zero-openhands` | `u032.part0000.jsonl` | 300,023,069 | `53ba9272beb4b141179d2870cf8004fcd1e0f293039708fd2a46339db6f88f58` |
| `sft-code-swe-zero-openhands` | `u032.part0001.jsonl` | 225,776,990 | `435b49328e2ba8ef27f1fe910124a00359c62e1ea9daa4d9c6fb21d8fdb3ef0c` |
| `sft-code-swe-zero-openhands` | `u014.part0000.jsonl` | 300,078,435 | `b65c69d707a8f0e614bf093062157be8b4887ef1d1cf44ed5a086d178ecd53ca` |
| `sft-code-swe-zero-openhands` | `u014.part0001.jsonl` | 221,784,267 | `58a755240f84613a254a81f50715003fb4cbd0bbef3254dddbdc9e1763356cbe` |
| `sft-code-swe-zero-openhands` | `u017.part0000.jsonl` | 300,019,222 | `506a37dcb0820801a65e4e52e4cd7ba08b4ab9a192ca3549e48a37290537a1b5` |
| `sft-code-swe-zero-openhands` | `u017.part0001.jsonl` | 226,423,996 | `bb9d508596444b69e597a9110b2f12cd82ba3cd550e3ce2637cc10f3d0c7d441` |
| `sft-code-swe-zero-openhands` | `u028.part0000.jsonl` | 300,002,525 | `1a8149030c344a7648d0f9b607a665a8769487b28d000088d176844864a13b47` |
| `sft-code-swe-zero-openhands` | `u025.part0000.jsonl` | 300,001,902 | `84123057af48ece34465ee6489bc50806cb18aae53eca4b33e3d319895821c24` |
| `sft-code-swe-zero-openhands` | `u028.part0001.jsonl` | 225,163,584 | `5ba710504dcc409269f04394692fcd1ec39be1c9ec006fa2e1be6806807ad9c6` |
| `sft-code-swe-zero-openhands` | `u025.part0001.jsonl` | 222,277,854 | `e81194a92452e73c1a8a00c8975f8a75fdd40d8bbddc0ef36e4b0e41276e903a` |
| `sft-code-swe-zero-openhands` | `u019.part0000.jsonl` | 300,005,022 | `0f7c4da158f03a8c6b23df55204c9c0220800bd1ad796f2d0bb2eeb234da375c` |
| `sft-code-swe-zero-openhands` | `u019.part0001.jsonl` | 226,791,728 | `ea92874bf2069340e95ae8450fd10df3568a80d7ca03f3b0b482105bfc8d9f51` |
| `sft-code-swe-zero-openhands` | `u000.part0000.jsonl` | 300,018,833 | `d78945f5261ee6eeea19e67fb989762ab33fe41afa64409a87bf2cb104fbc041` |
| `sft-code-swe-zero-openhands` | `u000.part0001.jsonl` | 227,698,379 | `4e2f1a939334d8b4c77572ec74778100fa75fe3f7566113a712017b94c7ccc18` |
| `sft-code-swe-zero-openhands` | `u003.part0000.jsonl` | 300,100,975 | `fdacebb6ad09dc168c591fcd0143abb685bc5c7d1aa1079c59b4f15cface472b` |
| `sft-code-swe-zero-openhands` | `u003.part0001.jsonl` | 221,549,781 | `e8774c961a4813351a86be80792a5a6b378addd3cb8ec0026bc4b1c52b317a79` |
| `sft-code-swe-zero-openhands` | `u024.part0000.jsonl` | 300,018,247 | `0e9501726e9ee381807767c1696bd2d3a6aa1d8da3ff33ccc105d11dbd47dbde` |
| `sft-code-swe-zero-openhands` | `u024.part0001.jsonl` | 220,519,172 | `e1f0ef4926d43857247aa7a2f1de42a624424ddba03b821bf6bf2a9df34b2236` |
| `sft-code-swe-zero-openhands` | `u057.part0000.jsonl` | 300,044,451 | `dac6fb4f3f0391f653265b748fddc4db78b1845aab771775a4db0085143f3233` |
| `sft-code-swe-zero-openhands` | `u057.part0001.jsonl` | 222,114,052 | `25921cfa4c1eaab4c67d1aab41e8dbb547887f6c37a7b836963d2a698595e7f9` |
| `sft-code-swe-zero-openhands` | `u001.part0000.jsonl` | 300,024,578 | `3e7ca3ffa1961a85f0436d21935e87f1ce5a63a1f93e231c87722e53e26648f8` |
| `sft-code-swe-zero-openhands` | `u001.part0001.jsonl` | 221,003,182 | `c31884117bbc2e5c267a77d1bf47297e647eca62bd916ddba02fdd41cf49cb90` |
| `sft-code-swe-zero-openhands` | `u055.part0000.jsonl` | 300,083,566 | `3ea0df95edc8911c280c213b44d6828b1a32b3d0a691ab4305c744fabfe5220f` |
| `sft-code-swe-zero-openhands` | `u055.part0001.jsonl` | 218,822,572 | `d076f9c6701e728d8db3482ad42970ca0be45b96be859f28ad3e6403ec8417cb` |
| `sft-code-swe-zero-openhands` | `u058.part0000.jsonl` | 300,148,751 | `eb3b49ba29e0d582c031a253ff27d17e0f497b5fd64896fbaa77f35642a427ae` |
| `sft-code-swe-zero-openhands` | `u058.part0001.jsonl` | 217,820,697 | `5ade8f6e168b66d8fb8fa6f3832f00c18cd5b0dd4ee5350c6d954b86a7d3d1c3` |
| `sft-code-swe-zero-openhands` | `u059.part0000.jsonl` | 300,111,704 | `e86cb016205fce6d795e1743e973edf146ddffc82c136b2777af0ca635da5a7a` |
| `sft-code-swe-zero-openhands` | `u002.part0000.jsonl` | 300,121,822 | `48d76908ec5618844746cea891a472ce6bfab938bae49ca68179dc8bc33d56ac` |
| `sft-code-swe-zero-openhands` | `u059.part0001.jsonl` | 216,980,839 | `87b4e264cf828fbfecd399653eadaaa00390227dd54d30280dddd3ad135567f2` |
| `sft-code-swe-zero-openhands` | `u002.part0001.jsonl` | 222,031,374 | `c0c68bf884c657c40011af29d4676f0692612977651c27a629a44dee92158f9b` |
| `sft-code-swe-zero-openhands` | `u054.part0000.jsonl` | 300,004,593 | `3dc068f199e67c64a7fe918500635f6acd7d2b7b42084b030d86ba430c495ed7` |
| `sft-code-swe-zero-openhands` | `u054.part0001.jsonl` | 188,035,216 | `f0983439254caa512b0d286ae1c40b80e8eb0667a6429cb617a372ffecd4c084` |
| `sft-code-swe-zero-openhands` | `u063.part0000.jsonl` | 300,051,959 | `5a99bbdddd88defd6cf65ce0ac1057c51d462e23262b3fc6c723ee9605b28295` |
| `sft-code-swe-zero-openhands` | `u063.part0001.jsonl` | 76,003,515 | `b689aa93304adec95025061c3ac80b14d86477826f40129e489d31428165222f` |
| `sft-dolly-15k` | `dolly-15k.jsonl` | 15,465,770 | `f0e65f12ff0437552f9d8340c5244758ca233693c7c4c982480f3fcbfb50714a` |
| `sft-indic-aya-collection` | `indic-aya-collection.jsonl` | 2,668,534,387 | `be59e274c47778c906e0f5fa531ca5c8c195f29189ef8d09dd046d6beabae9eb` |
| `sft-indic-aya-dataset` | `indic-aya-dataset.jsonl` | 106,423,427 | `fbaf54e2913face83c7a9d1a25b87e086ce574b5debb840d2d159681b0bcb2ea` |
| `sft-indic-indic-align-dolly-t` | `indic-indic-align-dolly-t.jsonl` | 22,694,421 | `35980cee7f1d613dbc7814a7f7d0430c5c6bb98e3a7ecc0d01dcf41ae9f14e17` |
| `sft-math-nemotron-sft-math-v4` | `math-nemotron-sft-math-v4.jsonl` | 18,526,574,137 | `15cf1ff1cb0598540fc7d9f537400823ecdf3c2ee5a6572570989a8d59fff846` |
| `sft-math-openr1-math-raw` | `u000.part0000.jsonl` | 161,568,374 | `8e894ba334c09fe84918734bd0cf6fbfc87888d6f67a75b273c932e1a1db95f1` |
| `sft-math-openr1-math-raw` | `u037.part0000.jsonl` | 205,664,650 | `c7623087db9c93f158652524df9984ec0c04ef384a2aec769196b92c34abda0d` |
| `sft-math-openr1-math-raw` | `u014.part0000.jsonl` | 153,109,040 | `5142d9937a1e9b56c5a4ff6bd55ab9cfb31371e3fa39822aef7cc64e97227bf8` |
| `sft-math-openr1-math-raw` | `u004.part0000.jsonl` | 216,225,538 | `4eeb90bf2125abfeb8763c37bdd1e831c3be99bf4e72be5c0adfa7d515eeb3a5` |
| `sft-math-openr1-math-raw` | `u036.part0000.jsonl` | 173,315,941 | `5f9ae7b44668acaf5db7c2f6629e41a171f8f3da07ca853045acc06cdc74e3b6` |
| `sft-math-openr1-math-raw` | `u001.part0000.jsonl` | 191,071,566 | `8a700ec24c0f77b233dc147dcc546d1b6e7f56502800876df939057bcf3a2660` |
| `sft-math-openr1-math-raw` | `u015.part0000.jsonl` | 139,367,185 | `883270780f6d8ee8043d94d7ea541049907d1be1e2819bc14815f75b395e9be8` |
| `sft-math-openr1-math-raw` | `u010.part0000.jsonl` | 191,599,196 | `00fcda8fa32d14d3619497838b3adefd2eea0ae062f3bc0f04e7ee1fcf4e0baf` |
| `sft-math-openr1-math-raw` | `u007.part0000.jsonl` | 175,084,873 | `55e9afdb86329add1a26ad7ca883e106859573a6db017485d492f57eb6d439f1` |
| `sft-math-openr1-math-raw` | `u009.part0000.jsonl` | 176,360,843 | `48bbaa5f0d931b6ae28984ea2caed0686277cb7c0712565732eece8478ca0c20` |
| `sft-math-openr1-math-raw` | `u008.part0000.jsonl` | 175,007,047 | `fe0322d2758432fcbe8b35beb2c7715e81bf0ac866ad2d5d6afac5bc2ee561f0` |
| `sft-math-openr1-math-raw` | `u012.part0000.jsonl` | 169,167,879 | `54879ad511581f4742f57a2cf326d609646430e12ebfa0de9eaac13d77ac9687` |
| `sft-math-openr1-math-raw` | `u011.part0000.jsonl` | 181,672,218 | `918ee6690df8627ef25b2c1af3c1f9b489d8773161be1291a526b9012259997e` |
| `sft-math-openr1-math-raw` | `u006.part0000.jsonl` | 176,498,511 | `2c685fe8ffffd2254e6e42c864d6aab9184577ef0a0c4740f5045775e74eab17` |
| `sft-math-openr1-math-raw` | `u005.part0000.jsonl` | 186,596,566 | `71e695b88dbc0fb20180ac6f70695f90a56bfdb7130f7f404651e04f511f2111` |
| `sft-math-openr1-math-raw` | `u038.part0000.jsonl` | 176,530,662 | `1518c7b44a6204224458fb44cd1ac0f3a9569ba37f95c2cce66ceceb337e1167` |
| `sft-math-openr1-math-raw` | `u003.part0000.jsonl` | 133,922,001 | `b094db753df34d02724c55141347b7b2659a2ea69ac38b1db4efc8a4d65e2a9e` |
| `sft-math-openr1-math-raw` | `u013.part0000.jsonl` | 126,565,212 | `c295bb8bd0701e7587d776ff0da43bf89ad5654b5c3154ffadd078d4f3304966` |
| `sft-math-openr1-math-raw` | `u002.part0000.jsonl` | 136,062,553 | `7a8d932f5f6c0105ef7dcb8757d695d96c178f1911874531271e26cbfd997f11` |
| `sft-math-openr1-math-raw` | `u034.part0000.jsonl` | 86,667,240 | `13dcd91768442c86a85a723a6530a1abe0225f49f3274baa99938d47ee6a5d65` |
| `sft-math-openr1-math-raw` | `u035.part0000.jsonl` | 93,354,791 | `350cc1c4627eca3d332b36020a398ef7a8797790f2a069a1d29eccc832bd077b` |
| `sft-math-openr1-math-raw` | `u020.part0000.jsonl` | 87,570,519 | `9d4d6751cf6cb9d600f7d9d359bf5d38404e647ff80725c53e0d1b6bdc1c634c` |
| `sft-math-openr1-math-raw` | `u016.part0000.jsonl` | 87,123,528 | `0e94e60a1e7e6e94a526678d4dbfba016ce4c98de95672d504650cc0e2e2e92e` |
| `sft-math-openr1-math-raw` | `u019.part0000.jsonl` | 87,560,526 | `e3165eb8a6c55d954d1f0a74dbe4ddb015bea68dd0ba2d8580003bfaa0f4560a` |
| `sft-math-openr1-math-raw` | `u030.part0000.jsonl` | 86,479,177 | `6f3bb4f726b989f81159932e523bf4679b8596f396ce1dff205388852efa9948` |
| `sft-math-openr1-math-raw` | `u033.part0000.jsonl` | 87,573,827 | `60440dd8497ae249a86086606ab533c3b55c505ebd7baf593481ab0971ca994f` |
| `sft-math-openr1-math-raw` | `u031.part0000.jsonl` | 86,440,695 | `a217a48c0aed40c86b74e31f700b7a46177c65248c858d78b5c64d9f2d44c787` |
| `sft-math-openr1-math-raw` | `u028.part0000.jsonl` | 87,688,375 | `ca4a09a62df36154d434c9eee6ed5d247733f739ffed7aff89c615676eb2999d` |
| `sft-math-openr1-math-raw` | `u023.part0000.jsonl` | 86,946,828 | `9dc1ef2c7bff9318fb0f12651554349dea344bef9dd751cbe0f573604d7b94fa` |
| `sft-math-openr1-math-raw` | `u026.part0000.jsonl` | 85,550,762 | `065843dacc68e5de048ae714a790c3d407410329896ca1584328a84204d4783d` |
| `sft-math-openr1-math-raw` | `u024.part0000.jsonl` | 87,671,860 | `3ac26b196465429712ea99a6dd6f1ef5d1f65b709855424d6bdf218676999f3d` |
| `sft-math-openr1-math-raw` | `u032.part0000.jsonl` | 87,645,776 | `a87dc26f789bbbfefb064794ea6369b72dda2300426f665242a1e93761ec5b4e` |
| `sft-math-openr1-math-raw` | `u018.part0000.jsonl` | 85,940,673 | `e1d2720651a6cfd8dc320cd74a063419f09419dfa813767e8d28d2ff1fa5d639` |
| `sft-math-openr1-math-raw` | `u025.part0000.jsonl` | 87,044,489 | `dc0814e36f40bdc0ce8f6ff23f177a8c917dfc60406881a3c4d1ff0dafdf00e4` |
| `sft-math-openr1-math-raw` | `u022.part0000.jsonl` | 86,346,272 | `ed8d796f709d795387af5c027a5882f39b0b190b5d32ded489c5cf9b7cffb986` |
| `sft-math-openr1-math-raw` | `u021.part0000.jsonl` | 86,461,147 | `0272d6bd42c64c5dca1b950c15dab2d35db74feabad4090d7aae788c0167d3d8` |
| `sft-math-openr1-math-raw` | `u029.part0000.jsonl` | 87,530,949 | `e9e946cd67ff00b08efa63d5089446a5e7e57e9ada77017ee4978335856881da` |
| `sft-math-openr1-math-raw` | `u027.part0000.jsonl` | 86,741,896 | `2810eeca50a2fd909ae2d268203f467c274b849903c24b91435374e91adeede7` |
| `sft-math-openr1-math-raw` | `u017.part0000.jsonl` | 86,358,279 | `624fbfa7d77d26e1408d7f4cba8f19f3e650f9fa16b66f85f099abaeab829bbb` |
| `sft-math-openr1-math` | `u001.part0000.jsonl` | 164,760,896 | `a2a7ca7ed491d67627bea3df52bc8af652080b5e07d26addafc2db70f7fede9e` |
| `sft-math-openr1-math` | `u011.part0000.jsonl` | 165,560,381 | `626788110033364273165288e81585906e79acf97ea3ebdae50ba25058878427` |
| `sft-math-openr1-math` | `u017.part0000.jsonl` | 165,282,504 | `087c24de3bafcd2b93e4373acdd0296c663b745a438fb57671271e7462d4be6a` |
| `sft-math-openr1-math` | `u005.part0000.jsonl` | 164,801,471 | `1cb8d818957d5efdde8745cf759631166616063838da74fca1da538b87b4459a` |
| `sft-math-openr1-math` | `u008.part0000.jsonl` | 164,358,965 | `36649a5b08403330ac0ed51ee07c0523c4e3ffa25180617887e26e40c3d1fc15` |
| `sft-math-openr1-math` | `u016.part0000.jsonl` | 164,618,033 | `aca83ad1c95bc8774defa402951e4c7d37f0c2992675f4ba964c655a2f6c3b69` |
| `sft-math-openr1-math` | `u010.part0000.jsonl` | 164,021,158 | `915703d0931d91af8812cee5f8c1252ce12e1508f85f965d80dacad818993cf7` |
| `sft-math-openr1-math` | `u002.part0000.jsonl` | 163,929,606 | `5320e931abe03ec2cf37ad9c1555f05933c233c7ad74b14bdeb8d43e45a0b2e7` |
| `sft-math-openr1-math` | `u018.part0000.jsonl` | 163,567,923 | `fe3242c643956938787d2c05f3f73259d929f51849be7c1f8e3711da502322d6` |
| `sft-math-openr1-math` | `u007.part0000.jsonl` | 163,285,749 | `6806e7ef2c5a7d0c28a00b2128e3b9cdaeeea3cecb089cdd083c02f1af254d3d` |
| `sft-math-openr1-math` | `u006.part0000.jsonl` | 164,388,491 | `7d59a9ccb5abf2ec36efdbe28b27a56ab1c1f3779e8874257c51a2de53150b72` |
| `sft-math-openr1-math` | `u009.part0000.jsonl` | 163,829,207 | `7ed955a660b37f52e0d4917eb676ccf7cad0bbbd8a849f689555351230bd416f` |
| `sft-math-openr1-math` | `u000.part0000.jsonl` | 163,630,594 | `60ced059bc1df6691124c3bf31b8dd0ff7fa0149c86977a73379f1e7a370afc0` |
| `sft-math-openr1-math` | `u015.part0000.jsonl` | 163,388,108 | `8ce74858ab2407fe37ba46f5cd8024a98e70a3d42ba765b3bc6865456d19411d` |
| `sft-math-openr1-math` | `u012.part0000.jsonl` | 162,903,741 | `62a6479602a6edb1bcf622d33f5972aba2f4178b01def83baca581ed43700b2c` |
| `sft-math-openr1-math` | `u004.part0000.jsonl` | 162,897,106 | `edc0864c95975ae24e8f82412aed74487c29eefe0ac63aad4d60c2aa27fcbf1a` |
| `sft-math-openr1-math` | `u013.part0000.jsonl` | 162,878,576 | `56f347a083ba636828279f5590f5c8e6f4f89bf0a3e7cb686ba34e26ff6b1180` |
| `sft-math-openr1-math` | `u003.part0000.jsonl` | 162,609,635 | `bb16ee687f274dadb33e2e95082d255e9d592d514425f118a7cf461a45eec7a9` |
| `sft-math-openr1-math` | `u019.part0000.jsonl` | 162,790,199 | `de357d23c684f16ff0c0f74f05964110d834360b9c8d8c886106a0bb83b47bb0` |
| `sft-math-openr1-math` | `u014.part0000.jsonl` | 162,564,725 | `1fe2737b3b2e8a879614050338b127bfa752e5949fad42e943c6e2c45d2ad739` |
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
| `sft-code-opencodereasoning-2` | adapter and test written, but upstream withholds the question text ('-') in the python shard; needs a join with the source problem sets (taco, apps, code_contests) before it can be converted |
| `sft-math-nemotron-math-v2` | full run not done yet |
| `sft-math-nemotron-proofs` | full run not done yet |
| `sft-math-nemotron-proofs-v3-sft` | full run not done yet |
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

