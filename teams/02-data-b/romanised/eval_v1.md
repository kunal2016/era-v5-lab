# D2 detector on 100 labelled documents (v1)

Test set: `testset_100.csv`, 100 documents: 52 that a reader marked D2 and 48 that no reader marked D2 (half of those chosen among documents with at least 10% Latin letters).
Ground truth: the readers' labels (a document is D2 when at least one reader marked it D2).

Detector rule: at least 3 romanised Indic words, 2 of them different, or at least 5 IAST letters (see `detector.py`).

## Result

| D2 docs | flagged | true pos | false pos | missed | true neg | precision | recall |
|---|---|---|---|---|---|---|---|
| 52 | 22 | 22 | 0 | 30 | 48 | 100% | 42% |

## Other thresholds

| min hits | min distinct | min IAST | flagged | precision | recall |
|---|---|---|---|---|---|
| 2 | 1 | 3 | 28 | 100% | 54% |
| 2 | 1 | 5 | 28 | 100% | 54% |
| 2 | 1 | 10 | 27 | 100% | 52% |
| 2 | 2 | 3 | 25 | 100% | 48% |
| 2 | 2 | 5 | 25 | 100% | 48% |
| 2 | 2 | 10 | 24 | 100% | 46% |
| 3 | 1 | 3 | 22 | 100% | 42% |
| 3 | 1 | 5 | 22 | 100% | 42% |
| 3 | 1 | 10 | 21 | 100% | 40% |
| 3 | 2 | 3 | 22 | 100% | 42% |
| 3 | 2 | 5 | 22 | 100% | 42% **(used)** |
| 3 | 2 | 10 | 21 | 100% | 40% |
| 4 | 1 | 3 | 20 | 100% | 38% |
| 4 | 1 | 5 | 20 | 100% | 38% |
| 4 | 1 | 10 | 19 | 100% | 37% |
| 4 | 2 | 3 | 20 | 100% | 38% |
| 4 | 2 | 5 | 20 | 100% | 38% |
| 4 | 2 | 10 | 19 | 100% | 37% |
| 5 | 1 | 3 | 16 | 100% | 31% |
| 5 | 1 | 5 | 16 | 100% | 31% |
| 5 | 1 | 10 | 15 | 100% | 29% |
| 5 | 2 | 3 | 16 | 100% | 31% |
| 5 | 2 | 5 | 16 | 100% | 31% |
| 5 | 2 | 10 | 15 | 100% | 29% |

## Missed (reader D2, not flagged): 30

| doc_id | pack | D2 marks / readers | Indic words (distinct) | IAST | words matched |
|---|---|---|---|---|---|
| 7e24bbd21ca4942b | ind-bn-sangraha-v | 1/2 | 1 (1) | 0 | rashifal |
| a3a0a3d543d77afe | ind-bn-sangraha-v | 1/2 | 0 (0) | 0 | - |
| aecb9893b814c81f | ind-bn-sangraha-v | 1/2 | 0 (0) | 0 | - |
| 3776d34f591f896d | ind-hi-fw2 | 1/2 | 0 (0) | 0 | - |
| ee19639bfb2e22a0 | ind-hi-fw2 | 1/2 | 1 (1) | 0 | ki |
| 25f028264b1d21a1 | ind-hi-hplt | 2/4 | 2 (1) | 0 | ke |
| 27c3cc715e797fcf | ind-hi-hplt | 1/4 | 2 (2) | 0 | ek, ka |
| 2d3b04f109d069ec | ind-hi-hplt | 4/4 | 2 (2) | 0 | hai, kya |
| 3cf3a36bf10de245 | ind-hi-hplt | 1/4 | 1 (1) | 0 | bharti |
| 7143c8411c407518 | ind-hi-hplt | 1/4 | 0 (0) | 0 | - |
| 7b6db4f0bb885a22 | ind-hi-hplt | 3/4 | 1 (1) | 0 | ka |
| 8298b653e0d7e1b6 | ind-hi-hplt | 1/4 | 1 (1) | 0 | yojana |
| 8a6a9e11bf0f5d9f | ind-hi-hplt | 1/4 | 2 (1) | 0 | bharti |
| a42a9bf9f5e4dc0b | ind-hi-hplt | 1/4 | 1 (1) | 0 | bharti |
| c80b6ba958512284 | ind-hi-hplt | 2/4 | 0 (0) | 0 | - |
| e988773eff0ee985 | ind-hi-hplt | 1/4 | 2 (1) | 0 | yojana |
| ef3ed1ee60b1d6fd | ind-hi-hplt | 1/4 | 0 (0) | 0 | - |
| 4d9bf15a8b501e04 | ind-mr-fw2 | 1/3 | 0 (0) | 0 | - |
| 6584bcd16dc3fdbf | ind-mr-fw2 | 1/3 | 0 (0) | 0 | - |
| 8542df4ed14728c2 | ind-mr-fw2 | 1/3 | 0 (0) | 0 | - |
| e6b4976ea98d0201 | ind-mr-fw2 | 1/3 | 0 (0) | 0 | - |
| 49ee950543dc49b6 | ind-sa-fw2 | 1/2 | 0 (0) | 0 | - |
| 6a58a10566aca6d8 | ind-sa-fw2 | 1/2 | 0 (0) | 0 | - |
| 7bc67301a58f3aec | ind-sa-fw2 | 1/2 | 1 (1) | 0 | mere |
| adebf77350ddfac0 | ind-sa-fw2 | 1/2 | 0 (0) | 0 | - |
| 128625bd74c59385 | ind-ta-fw2 | 1/1 | 0 (0) | 0 | - |
| aabcbb5c1a89c890 | ind-ta-fw2 | 1/1 | 0 (0) | 0 | - |
| fdf1699f0d8575a1 | ind-ta-fw2 | 1/1 | 0 (0) | 0 | - |
| 13de1d751434be22 | ind-ta-sangraha-v | 1/2 | 2 (2) | 0 | irrunga, unga |
| b54a137e794fc027 | ind-ta-sangraha-v | 1/2 | 1 (1) | 0 | ji |

## False alarms (flagged, no reader D2): 0

| doc_id | pack | D2 marks / readers | Indic words (distinct) | IAST | words matched |
|---|---|---|---|---|---|
