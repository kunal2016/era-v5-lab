# Dedup results v1

The measurements behind `dedup_design_v1.md`, for discussion. The design states the decisions; this file holds the numbers, and grows as new runs come in.

**How to read it**
- **Final** means measured by TSAI on the approved input with committed code. It changes only if the rules change.
- **Estimate** means computed by us from TSAI's files without `dedup.py`. Removal counts from `dedup.py` itself are given separately; they are local (no urls) until TSAI runs `jobs/2026-11-10-dedup.md`.
- **Local** means a test run on raw (not cleaned) sample v0 parts. It shows the code works and gives findings for the hand review; the TSAI run supersedes its counts.
- Every number is for the Week-2 tokenizer sample v0 (1.4 million documents). Applied to the full data, the counts will differ.

## 1. TSAI 38-pack run (final, except the removal estimates)

Job `jobs/2026-11-04-overlap.md`, approved by the Data A lead; run by TSAI on a CPU host on 5 Nov 2026 at commit `86ecdd4`. Results: `jobs/results/2026-11-04-overlap/` (merged to `main` in PR #307). Input: the 38 cleaned sample v0 packs, 86 parts, train + held-out.

| | |
|---|---|
| Documents | 1,416,236 (7 empty) |
| Wall time, peak memory | 3,351 s (56 min), 9.6 GiB (9,835.6 MiB); requested 60 min, 32 GiB |
| Pairs that share a shingle | 2,347,235,732 |
| Pairs stored (word Jaccard ≥ 0.50) | 32,738 |
| Pairs by word Jaccard ≥ 0.70 / 0.75 / 0.80 / 0.85 / 0.90 / 0.95 | 4,620 / 3,396 / 2,407 / 1,576 / 860 / 314 |
| Qualifying pairs (after the family rules) | **2,711**: 98 H1 (71 exact groups, 150 documents) + 2,613 H2. One H1 group is the 7 empty documents (21 pairs; observation 6) |
| Within pack / cross pack | 2,661 / **50** |
| Train ↔ held-out pairs among the qualifying pairs | 63 |
| `doc_id`s used by two or more documents | 0 |

The word-Jaccard counts cover every pair, before the family rules; the qualifying pairs are what dedup acts on.

*Source:* `overlap_summary.json` (documents, time, memory, pairs at each threshold, H1 groups, qualifying pairs by rule); `overlap_matches.csv` (within / cross pack). The train ↔ held-out count (63) is confirmed from `overlap_docs.parquet` (`matrix_confirmation.md`).

### Per pack

Where each column comes from (all files in `jobs/results/2026-11-04-overlap/`):

| Column | Source |
|---|---|
| Documents | `overlap_summary.json`, `documents` |
| Pairs ≥ 0.80 | `overlap_by_pack.csv`, level `0.80`, same pack on both sides (raw word score, before the family rules) |
| Qualifying | `overlap_matches.csv`, `stage = within_pack` (pairs that pass the family rules) |
| Docs matched, own pack | `overlap_matrix_counts.csv`, the diagonal (`source_a = source_b`) |
| Docs matched, other packs | `overlap_matches.csv`, `stage = cross_pack`: distinct documents per pack |
| Est. removed, Est. % | **Our estimate**, computed from `overlap_matches.csv`: within-pack matches joined into union-find clusters, one survivor per cluster. Rule 0 is not applied, because `overlap_matches.csv` has no split column; held-out survivors can shift a few |

TSAI kept the large files (`overlap_docs.parquet`, `overlap_pairs.csv`) out of the repo. This table was computed before they arrived. They were received separately on 10 Nov, match the summary's SHA-256, and were used for the matrix confirmation (`matrix_confirmation.md`) and the `dedup.py` run below.

| Pack | Documents (train + held-out) | Pairs ≥ 0.80 | Qualifying | Docs matched, own pack | Docs matched, other packs | Est. removed | Est. % |
|---|---:|---:|---:|---:|---:|---:|---:|
| `cadj-commits` | 75,579 | 1,094 | 1,094 | 1,664 | 9 | 895 | 1.18% |
| `cadj-notebooks` | 15,732 | 15 | 15 | 27 | 0 | 14 | 0.09% |
| `cadj-stackexchange` | 41,805 | 208 | 208 | 384 | 0 | 199 | 0.48% |
| `code-cpp` | 55,195 | 6 | 5 | 10 | 2 | 5 | 0.01% |
| `code-go` | 77,765 | 8 | 6 | 12 | 0 | 6 | 0.01% |
| `code-java` | 85,518 | 8 | 9 | 10 | 5 | 6 | 0.01% |
| `code-js-ts` | 117,208 | 1 | 1 | 2 | 2 | 1 | 0.00% |
| `code-python` | 73,305 | 1 | 24 | 13 | 4 | 9 | 0.01% |
| `code-rust` | 58,795 | 3 | 530 | 66 | 3 | 58 | 0.10% |
| `en-dclm` | 60,802 | 14 | 14 | 19 | 5 | 11 | 0.02% |
| `en-fineweb-edu` | 72,100 | 7 | 7 | 14 | 11 | 7 | 0.01% |
| `en-nemotroncc` | 89,183 | 23 | 19 | 27 | 6 | 15 | 0.02% |
| `en-nemotroncc-synth` | 198,877 | 1 | 1 | 2 | 1 | 1 | 0.00% |
| `ind-bn-fw2` | 10,750 | 0 | 0 | 0 | 1 | 0 | 0 |
| `ind-bn-sangraha-v` | 10,213 | 0 | 0 | 0 | 1 | 0 | 0 |
| `ind-gu-fw2` | 23,011 | 0 | 0 | 0 | 0 | 0 | 0 |
| `ind-hi-fw2` | 14,257 | 0 | 0 | 0 | 1 | 0 | 0 |
| `ind-hi-hplt` | 8,719 | 0 | 0 | 0 | 0 | 0 | 0 |
| `ind-hi-indiccorp` | 111,851 | 29 | 5 | 7 | 1 | 4 | 0.00% |
| `ind-hi-sangraha-s` | 8,368 | 545 | 540 | 37 | 0 | 35 | 0.42% |
| `ind-hi-sangraha-v` | 14,831 | 134 | 134 | 18 | 2 | 17 | 0.11% |
| `ind-kn-fw2` | 7,764 | 0 | 0 | 0 | 3 | 0 | 0 |
| `ind-kn-sangraha-s` | 5,222 | 20 | 0 | 0 | 0 | 0 | 0 |
| `ind-kn-sangraha-v` | 8,448 | 0 | 0 | 0 | 3 | 0 | 0 |
| `ind-ml-fw2` | 19,161 | 0 | 0 | 0 | 0 | 0 | 0 |
| `ind-mr-fw2` | 11,365 | 0 | 0 | 0 | 5 | 0 | 0 |
| `ind-mr-sangraha-v` | 12,299 | 0 | 0 | 0 | 5 | 0 | 0 |
| `ind-or-fw2` | 34,012 | 0 | 0 | 0 | 0 | 0 | 0 |
| `ind-sa-fw2` | 5,721 | 13 | 13 | 23 | 0 | 12 | 0.21% |
| `ind-ta-fw2` | 6,824 | 0 | 0 | 0 | 1 | 0 | 0 |
| `ind-ta-sangraha-s` | 4,372 | 55 | 1 | 2 | 0 | 1 | 0.02% |
| `ind-ta-sangraha-v` | 6,826 | 0 | 0 | 0 | 1 | 0 | 0 |
| `ind-te-fw2` | 5,009 | 0 | 0 | 0 | 2 | 0 | 0 |
| `ind-te-sangraha-s` | 4,468 | 32 | 0 | 0 | 0 | 0 | 0 |
| `ind-te-sangraha-v` | 8,174 | 0 | 0 | 0 | 2 | 0 | 0 |
| `math-finemath` | 28,830 | 18 | 3 | 6 | 2 | 3 | 0.01% |
| `math-megamath` | 17,803 | 100 | 32 | 20 | 1 | 14 | 0.08% |
| `sci-finepdfs` | 6,074 | 0 | 0 | 0 | 0 | 0 | 0 |
| **All** | **1,416,236** | **2,335** | **2,661** | **2,363** | **79** | **1,313** | **0.09%** |

**Estimate, with the cross-pack pass:** 1,351 documents removed (0.095%); the cross-pack pass adds 38. *Source:* our union-find estimate over all of `overlap_matches.csv`.

**`dedup.py` (local, 10 Nov, no urls):** 1,345 documents removed (0.095%): 1,289 H2 and 56 H1; 1,309 within a pack and 36 across packs; 0 held-out removed; 63 train copies removed by rule 0. The 6 fewer than the estimate are empty documents: `dedup.py` sets aside the matches between the 7 empty documents and lists them in `empty_documents.csv` (observation 6). *Source:* `jobs/logs/2026-11-10-dedup-local.txt`, section 4. TSAI's run with urls can change which copy survives, not how many are removed.

**By family (estimate, within-pack):** code-adjacent 1,108 of 133,116 (0.83%); code 85 of 467,786 (0.02%); Indic 69 of 341,665 (0.02%); English 34 of 420,962 (0.01%); math 17 of 46,633 (0.04%); science 0 of 6,074. *Source:* the per-pack table, summed by the pack name's prefix.

### Cross-pack pairs (50)

| Packs | Qualifying pairs |
|---|---:|
| `code-java` × `code-js-ts` | 8 |
| `en-fineweb-edu` × `en-nemotroncc` | 5 |
| `ind-mr-fw2` × `ind-mr-sangraha-v` | 5 |
| `code-cpp` × `code-java` | 4 |
| `en-dclm` × `en-fineweb-edu` | 4 |
| `cadj-commits` × `code-python` | 4 |
| `ind-kn-fw2` × `ind-kn-sangraha-v` | 3 |
| `cadj-commits` × `code-rust` | 3 |
| `code-cpp` × `code-js-ts` | 2 |
| `ind-te-fw2` × `ind-te-sangraha-v` | 2 |
| Other pack pairs (1 each) | 10 |

*Source:* `overlap_matches.csv`, `stage = cross_pack`, counted by pack pair.

**14 of these 50 are between empty documents:** all 8 `code-java` × `code-js-ts`, all 4 `code-cpp` × `code-java` and both `code-cpp` × `code-js-ts` pairs (observation 6). The real cross-pack pairs number 36.

**Pairs affected by the Data B pack order** (`source_priority_v1.md`, rule 4): **23 of the 50** have a Data B pack on at least one side. 14 are between two Data B packs, mostly the same Indic language in `fw2` and `sangraha-v` (`ind-mr` 5, `ind-kn` 3, `ind-te` 2; `ind-hi`, `ind-bn`, `ind-ta` 1 each; `ind-hi-indiccorp` × `ind-hi-sangraha-v` 1). 9 are between `cadj-commits` and a code pack (`code-python` 4, `code-rust` 3, `code-cpp` 1, `code-java` 1). The other 27 are between two Data A packs (14 of them between empty documents). Rule 4 decides a pair only if the copies are still tied after rules 0–3. TSAI approved this order in G1 on 10 Nov 2026. *Source:* `overlap_matches.csv`, by each side's pack.

### Observations for discussion

1. **`cadj-commits` holds two-fifths of all qualifying pairs** (1,094 of 2,711) and 45 of the 98 exact pairs; by our estimate it would lose 1.18% of its documents, the only pack above 1%. A sample should be read to confirm they are true copies (for example repeated commit messages) before they are removed.
2. **The code token pass finds what word scores miss.** `code-rust` has 3 pairs at word Jaccard ≥ 0.80 but 530 qualifying pairs; `code-python` has 1 and 24. These come from the token pass, which ignores comments and licence headers. The code hand review (0.85) should look at these.
3. **E4 signal: the Indic `sangraha-s` packs.** `ind-kn-sangraha-s` (20 pairs ≥ 0.80), `ind-te-sangraha-s` (32) and `ind-ta-sangraha-s` (55) end with 0, 0 and 1 qualifying pairs. The likely cause is the 50-word minimum, since Indic words are longer and fewer (Risk 2). In contrast, `ind-hi-sangraha-s` keeps 540 of 545, all among only 37 documents, so a few near-identical documents form large clusters. These packs are the first place to run E4.
4. **Cross-pack overlap is small and mostly expected:** English web crawls, the `fw2` and `sangraha-v` versions of the same Indic language, and `cadj-commits` with code packs. The pairs between code languages (Java, JS/TS, C++) are not shared files: all 14 are between empty documents (observation 6).
5. **Cleaning changed the math counts slightly:** `math-finemath` has 28,830 documents after cleaning against 29,434 raw; `math-megamath` 17,803 against 17,816.
6. **7 documents are empty after cleaning:** 1 `code-cpp`, 4 `code-java`, 2 `code-js-ts`, all train (0 words and 0 shingles in `overlap_docs.parquet`; their `doc_id`s are in `matrix_confirmation.md`). Cleaning emptied them without dropping them. They share one H1 key, so `overlap.py` counts them as one exact group: 21 of the 98 H1 pairs and 14 of the 50 cross-pack pairs, inflating 8 code cells of the source matrix. `dedup.py` sets their matches aside and lists them in `empty_documents.csv`. Cleaning should drop documents it empties.

## 2. Local runs (raw sample v0 parts)

### English packs (Aneesha Das, 4 Nov)

`en-dclm`, `en-fineweb-edu`, `en-nemotroncc`, `en-nemotroncc-synth`; 426,508 documents; 845 s, 3.4 GB. Raw word scores, before the family rules. *Source:* the run log, `jobs/logs/2026-11-04-overlap-en-local.txt`.

| | Within pack | Cross pack | All |
|---|---:|---:|---:|
| Exact (H1) pairs | 16 | 0 | 16 |
| Pairs at word Jaccard ≥ 0.80 | 44 | 11 | 55 |

- H1: 9 groups, 21 documents, all in `en-nemotroncc`.
- Pairs at ≥ 0.70 / 0.75 / 0.80 / 0.85 / 0.90 / 0.95: 135 / 90 / 55 / 43 / 33 / 25.
- **Finding:** short template pages that differ only in a name or date score 0.82–0.85; this is why H2 has a minimum length.

### Five packs (Vijay Patil, 4 Nov)

`code-rust`, `en-fineweb-edu`, `ind-hi-hplt`, `ind-mr-sangraha-v`, `math-finemath`; 183,976 documents; 571 s, 2.76 GiB. With the family rules. *Source:* the run's transcript and result snapshots in `jobs/logs/2026-11-04-overlap-local/`.

- 0 H1 groups; 372 qualifying H2 pairs: 371 within packs, 1 cross-pack (`en-fineweb-edu` × `math-finemath`).
- Largest share: `code-rust`, 57 of 60,738 documents with a match in their own pack (0.09%).

### Math packs, E1 (Kunal Sinha, 4 Nov)

`math-finemath`, `math-megamath`; 47,250 documents; 97 s, 1.0 GB. Config `overlap_math.json`, log `jobs/logs/2026-11-04-overlap-math-local.txt`. *Source:* that run's `overlap_summary.json`, `overlap_pairs.csv`, `overlap_matches.csv` and `overlap_docs.parquet` (local, in `out/overlap_math/`, not in the repo); the hand review also read the document text from the input parts. Gold IDs were checked against `teams/01-data-a/gold/math-*_gold.csv`.

| | |
|---|---|
| H1 exact groups | 0 |
| Pairs by word Jaccard ≥ 0.70 / 0.75 / 0.80 / 0.85 / 0.90 / 0.95 | 369 / 243 / 131 / 68 / 46 / 18 |
| Of the 46 at ≥ 0.90: qualify / rejected by the numbers rule | 36 / 10 |
| Qualifying: within `megamath` / within `finemath` / cross-pack | 32 / 3 / 1 |
| Train ↔ held-out qualifying pairs | 1 |
| Gold IDs present in this input | 0 of 112 |

**Hand review** (all 10 rejected pairs and the lowest-scoring kept pairs):
1. **The numbers rule rejects true copies with a different header.** Two pairs are the same page saved twice (Jaccard 0.987 and 0.972), differing only in a date line ("Dec 10, 2015 · 15 minute read") or a number in the title ("UVa 11357"), plus Markdown formatting. Both pairs share their URL.
2. **Template pages pass 0.90.** The largest cluster (7 documents) is slideserve.com pages: different presentations ("projectile motion", "the preprocessor", …) inside about 117 words of identical site boilerplate. Only the title differs, so they are not copies of one document.
3. **The rule works where it should:** two chemistry textbook chapters with different worked values are kept apart.
4. **A same-URL copy is missed just below 0.90:** reference.com's "examples of quadrilaterals" is in `finemath` train and `megamath` held-out with the identical URL, at 0.894.
5. **The gold harm check cannot run on the sample:** none of the 112 math gold IDs are in it.

Per-pack `jaccard_matrix.py` outputs for the two math packs (histogram, matrix, pairs with shingle counts) are in `out/jaccard_math/` on the local machine; they match the within-pack counts above.

## 3. Still to come

| Result | From | Needs |
|---|---|---|
| Final removal counts and remove list, with urls | TSAI's run of `jobs/2026-11-10-dedup.md` | Lead approval and the licence map. Local count without urls: 1,345 |
| Gold harm check | Diagnosis packs | `dedup.py` (written) and the diagnosis pack files |
| Hand review: prose 0.80, code 0.85, `cadj-commits` sample | Pairs from the TSAI run | `overlap_pairs.csv` and text |
| E4, Indic threshold check | `sangraha-s` packs first | Indic pack text |

**Done on 10 Nov:** the reviewed source matrix, `dedup/overlap_matrix.csv`, byte-identical to TSAI's (`matrix_confirmation.md`); `dedup.py` written and run locally on TSAI's outputs (1,345 removed, above).
