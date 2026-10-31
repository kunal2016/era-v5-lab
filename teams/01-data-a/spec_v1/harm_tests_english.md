# Spec v1 harm tests: English

DRAFT. Each cell: gold docs changed + dropped, for that function or medicine on that pack's gold set. Limit: `max(1, floor(1% of gold))`, that is `max(1 document, 1%)` (TSAI decision); each pack on its own gold set, never pooled; an empty gold set is NOT TESTABLE (exit code 2), never a PASS. A result other than PASS is shown after the count. Made by `scripts/make_harm_tests_english.py` on 31 Oct 2026 with the team's `harm_test.py`, run as it is (sha256 `4dcc04bf8ac5`, `g1-harm-test` at `bae5163`, the same file as PR 140's head). The code packs are in `harm_tests.md`.

## 1. Each function of clean_english.py on the English packs

`clean_english.py`: the code and English sheets, as `tools/build_clean.py` builds them (`clean.py` holds the code sheet only). The 14 functions with English rules; the other functions hold code rules only, which keep every English document (section 5).

| function | dclm | fineweb-edu | nemotroncc | synth |
|---|---:|---:|---:|---:|
| gold docs (limit) | 62 (1) | 158 (1) | 34 (1) | 96 (1) |
| A1 | 0 | 0 | 0 | 0 |
| A2 | 0 | 0 | 0 | 0 |
| A5 | 0 | 0 | 0 | 0 |
| A3 | 0 | 0 | 0 | 0 |
| B1 | 0 | 0 | 0 | 0 |
| B2 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 0 |
| C1 | 0 | 0 | 0 | 0 |
| C2 | 0 | 0 | 0 | 0 |
| D3 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0 |
| F1 | 0 | 0 | 0 | 0 |
| ALL IN ORDER | 0 | 0 | 0 | 0 |

`ALL IN ORDER` is `harm_test.py` running every function of `clean_english.py` one after another, in `RULES` order. Section 5 shows whether that gives the same as `clean()`, which runs the English rules in the sheet's order and F1 last.

## 2. The same, with the disputed docs left in the gold sets

| function | dclm | fineweb-edu | nemotroncc | synth |
|---|---:|---:|---:|---:|
| gold docs (limit) | 170 (1) | 295 (2) | 34 (1) | 96 (1) |
| A1 | 0 | 0 | 0 | 0 |
| A2 | 0 | 0 | 0 | 0 |
| A5 | 0 | 0 | 0 | 0 |
| A3 | 0 | 0 | 0 | 0 |
| B1 | 0 | 0 | 0 | 0 |
| B2 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 0 |
| C1 | 0 | 0 | 0 | 0 |
| C2 | 1 | 1 | 0 | 0 |
| D3 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0 |
| F1 | 0 | 0 | 0 | 0 |
| ALL IN ORDER | 1 | 1 | 0 | 0 |

## 3. Each medicine on its own, on the English packs

`medicine_english.md --rule all`: each of the 20 medicines alone, then the whole sheet in its order.

| medicine | function | dclm | fineweb-edu | nemotroncc | synth | with the disputed docs left in |
|---|---|---:|---:|---:|---:|---|
| gold docs (limit) | | 62 (1) | 158 (1) | 34 (1) | 96 (1) | dclm 170 (1), fineweb-edu 295 (2), nemotroncc 34 (1), synth 96 (1) |
| `DA-A1-004` | A1 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-A2-008` | A2 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-A5-001` | A5 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-A3-002` | A3 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B1-002` | B1 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B2-002` | B2 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C3-001` | C3 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C3-002` | C3 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C5-002` | C5 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C5-005` | C5 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-D4-001` | D4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C1-006` | C1 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-C2-003` | C2 | 0 | 0 | 0 | 0 | 1, 1, 0, 0 |
| `DA-D3-003` | D3 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B4-007` | B4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B4-008` | B4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B4-009` | B4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B4-010` | B4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-B4-011` | B4 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| `DA-F1-005` | F1 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| ALL IN ORDER | the sheet | 0 | 0 | 0 | 0 | 1, 1, 0, 0 |

## 4. scripts/clean_english.py, the English cleaner on its own

`scripts/clean_english.py --rule all`. Its `RULES` follow the sheet's order, so its `ALL IN ORDER` is `clean()`.

| function | dclm | fineweb-edu | nemotroncc | synth |
|---|---:|---:|---:|---:|
| gold docs (limit) | 62 (1) | 158 (1) | 34 (1) | 96 (1) |
| A1 | 0 | 0 | 0 | 0 |
| A2 | 0 | 0 | 0 | 0 |
| A5 | 0 | 0 | 0 | 0 |
| A3 | 0 | 0 | 0 | 0 |
| B1 | 0 | 0 | 0 | 0 |
| B2 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 0 |
| C1 | 0 | 0 | 0 | 0 |
| C2 | 0 | 0 | 0 | 0 |
| D3 | 0 | 0 | 0 | 0 |
| B4 | 0 | 0 | 0 | 0 |
| F1 | 0 | 0 | 0 | 0 |
| ALL IN ORDER | 0 | 0 | 0 | 0 |

## 5. Checks on every document of the English packs

From `scripts/verify_clean_english.py` (`results/verify_clean_english.json`). Each cell: documents where the check fails.

| check | dclm | fineweb-edu | nemotroncc | synth |
|---|---:|---:|---:|---:|
| documents | 500 | 500 | 500 | 500 |
| a `clean_english.py` function differs from its English medicines run in order (a code function must keep) | 0 | 0 | 0 | 0 |
| `clean()` differs from the sheet run in order | 0 | 0 | 0 | 0 |
| `clean_english.py` and `scripts/clean_english.py` differ | 0 | 0 | 0 | 0 |
| `ALL IN ORDER` of `clean_english.py` (RULES order) differs from `clean()` | 0 | 0 | 0 | 0 |
| `ALL IN ORDER` of `scripts/clean_english.py` differs from `clean()` | 0 | 0 | 0 | 0 |
| a second `clean()` changes the text again | 0 | 0 | 0 | 0 |
| documents with a ZWJ or ZWNJ | 0 | 0 | 0 | 0 |
| a ZWJ or ZWNJ deleted on its own | 0 | 0 | 0 | 0 |

## 6. F1 on the English packs

From `scripts/f1_eval_english.py` (`results/f1_eval_english.json`). `DA-F1-005` is the F1 that `clean_english.py` runs on English; the shared `tools/f1_rule.py` is switched on for `en` and `eng` in memory only, to show what that would do. Each cell: docs F1 changes or drops after the other English rules, then the gold docs among them.

| F1 rule | dclm | fineweb-edu | nemotroncc | synth |
|---|---:|---:|---:|---:|
| DA-F1-005 | 2, gold 0 | 0, gold 0 | 1, gold 0 | 2, gold 0 |
| shared F1 (in memory) | 14, gold 1 | 6, gold 0 | 14, gold 0 | 8, gold 0 |

A second `clean()` leaves every F1 tag as it is: dclm 0 of 2, fineweb-edu 0 of 0, nemotroncc 0 of 1, synth 0 of 2 docs change again. Planted made-up values: `decisions_english.md`, F1.

## Gold docs touched

| pack | official gold | with the disputed docs left in |
|---|---|---|
| dclm | - | `0b6d3f138a3faac0` |
| fineweb-edu | - | `ab731016903cbb4f` |
| nemotroncc | - | - |
| synth | - | - |

Affected gold IDs are in `results/clean_<pack>_harm.json`, `results/clean_stress_<pack>_harm.json` and `results/<pack>_harm.json`. No document text is kept.

## Not run

| family | pack | gold docs | why |
|---|---|---:|---|
| - | - | - | every English pack ran |

Overall: 20 of 20 runs PASS.
