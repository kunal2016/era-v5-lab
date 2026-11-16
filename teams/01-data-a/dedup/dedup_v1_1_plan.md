# Dedup v1.1: plan for 16–27 Nov 2026 (two weeks)

**Owner:** Kunal Sinha (Data A dedup). **Status:** in progress; updated at most once a day, when a row changes.
**Design:** `dedup_design_v2_proposal.md` is the full backlog (16 items). This file is the part being done this week,
and the requirements it is checked against. Nothing here changes v1's rules or the #255 job unless a switch is turned on.

## Week 1 (16–20 Nov): our own work (item 6 waits on G10, item 16 on answers from Sourav and Vijay)

| Day | Work (proposal item) | Done when |
|---|---|---|
| Mon 16 | **Item 5:** `code_sha256` and git commit in `overlap_summary.json` and `dedup_summary.json`; part SHA-256s carried from overlap to dedup | Tests pass; outputs otherwise byte-identical to v1 |
| Tue 17 | **Item 16:** answers to Sourav's 7 open items; the dedup job as a runner `run.json` (adopt job 244's clean folder, `to: dedup`) | `run_pipeline.py --plan` passes on it |
| Wed 18 | **Items 1 and 2:** same-URL pairs as H2 at ≥ 0.80; math numbers on the body only. Each behind a config switch, off by default | Known-pair tests for both; switches off give byte-identical output |
| Thu 19 | Overlap rerun request carries items 1 and 2, with a fresh test log. **H3:** the BGE-M3 run on Sanskrit (`labse_check.py --model BAAI/bge-m3`) | Request ready for lead approval; result added to `h3_labse_check_results_v1.md` |
| Fri 20 | **Item 6:** all 38 packs in `dedup.json` (`licence_usable`, `default_licence_usable: false`) once G10's PR merges. Buffer for review comments | Branch ready for a PR; team update posted |

**If time allows:** item 4, the code threshold (0.85) hand review.

**Not this week** (in the proposal as "later"): items 3 (waits on E4 readers), 8–12 (v2 methods, conditional ablation),
13–15 (when #461's sources join). H3 beyond the BGE-M3 run waits on Aneesha's `h3.py` and TSAI's ruling.

## Week 2 (23–27 Nov): by support from other teams

Week 2's work depends on what arrives from other teams. Each row says what it needs; if that has not arrived, the row
waits and the next independent row is done instead.

| Work (item) | Needs from another team | If it has not arrived |
|---|---|---|
| **Item 11:** MinHash + LSH agreement test on the sample | Nothing | — (always done) |
| **Item 4:** code threshold hand review, final | Nothing (5 Nov pairs); rerun pairs preferred | Done on the 5 Nov pairs, rechecked later |
| **Item 6:** `dedup.json` lists all 38 packs | G10's PR on `main` | Ready as a one-line change |
| **Item 7:** wire `h3.py` output into `dedup.py`; local H3 run, report-only | Aneesha: `h3_matches.csv` keyed by document | Keep `g1-dedup-h3` ready; nothing else blocked |
| **Item 8:** containment, measured on the rerun's outputs | TSAI: the overlap rerun | Code and known-pair tests only |
| **Item 10:** "changed least" survivor rule, measured on the rerun's groups | TSAI: the overlap rerun | Code and tests only |
| **Item 3:** Indic length minimum | E4 readers' labels | Waits (no code without the labels) |

## Progress by support received

| Scenario | Support received | Items done by 27 Nov | Share of 16 |
|---|---|---|---|
| No outside help | None | 1, 2, 4, 5, 11, 16 | 6 = 38% |
| Expected | G10's merge; the overlap rerun; Aneesha's format | + 6, 7 (dedup side, local run), 8, 10 | 10 = 63% |
| Best case | + E4 labels | + 3 | 11 = 69% |
| Outside a two-week window by design | — | 9, 12 (conditional), 13, 14 (when #461's packs join), 15 (G10) | 5 items |

## All 16 proposal items

Every item of `dedup_design_v2_proposal.md` has a place: this week, next (after a dependency clears), or conditional.
None is dropped.

| # | Item | Release | When | Owner | Blocked by |
|---|---|---|---|---|---|
| 1 | Same-URL pairs as H2 at ≥ 0.80 | v1.1 | **This week** (Wed) | Kunal | Team agreement; takes effect in the overlap rerun |
| 2 | Math numbers on the body only | v1.1 | **This week** (Wed) | Kunal | As item 1 |
| 3 | Indic length minimum | v1.1 | Next: when E4 labels arrive | Kunal | Native readers (issues #392–#395) |
| 4 | Code threshold (0.85) hand review | v1.1 | This week if time allows, else next | Kunal | Rerun pairs for the final review |
| 5 | Code SHA-256, commit and part hashes in summaries | v1.1 | **This week** (Mon) | Kunal | — |
| 6 | Licence map and pack order in `dedup.json` | v1.1 | **This week** (Fri) | Kunal | G10's PR merging |
| 7 | H3: translations across languages | v1.1 track | Dedup side done; **BGE-M3 run this week** (Thu); rest next | Aneesha (`h3.py`), Kunal (`dedup.py`) | Aneesha's format; TSAI's ruling; GPU job (E5c); readers (E5d) |
| 8 | Containment for truncated copies | v2 | Next: with the rerun's outputs | Kunal | Rerun outputs |
| 9 | Indic-aware shingles | v2 | Conditional: only if item 3 is not enough | Kunal | E4 result |
| 10 | Survivor rule: the copy cleaning changed least | v2 | Next: on the rerun's groups | Kunal | Rerun outputs; raw text as a dedup input |
| 11 | MinHash + LSH agreement test | v2 | Next: before the full data | Kunal | Full-data size |
| 12 | Training ablation of the cross-pack pass | v2 | Conditional: only if a pack's cross-pack removals reach 1% | TSAI (compute), G9 (eval) | Rerun counts; #461 packs |
| 13 | Pack order for new packs (by clean share) | Before new packs | Next: when #461's sources join | Kunal | TSAI agreeing to the rule-4 change |
| 14 | Packs that are not documents | Before new packs | Next: when #461's sources join | Kunal | Which #461 packs join |
| 15 | Licence map for new sources | Before new packs | Next: when #461's sources join | G10 | G10's rulings (Aksharantar, MADLAD-400, BPCC mined) |
| 16 | Pipeline contract with Sourav's runner | v1.1 | **This week** (Tue) | Kunal, Sourav | Answers on Sourav's 7 items |

**This week: 5 items** (1, 2, 5, 6, 16) plus H3's BGE-M3 run. **Next: 8** (3, 4, 7's remainder, 8, 10, 11, 13, 14),
each starting when its dependency clears. **Conditional: 2** (9, 12). **Other teams: 1** (15, G10).

## Requirements

Status: **Met** (with evidence), **This week** (with the day), **Waiting** (on whom).

### Functional (what dedup does)

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| FR1 | Find exact (H1) and near (H2) duplicates within and across all 38 packs, with v1's family rules | Met (v1) | `dedup_design_v1.md`; TSAI's overlap run of 5 Nov |
| FR2 | Choose survivors in rule order: held-out, licence, URL, length, pack order | Met (v1) | `source_priority_v1.md`; `tests/test_dedup.py` |
| FR3 | Never remove a held-out document; report held-out ↔ held-out pairs | Met (v1) | `heldout_removed: 0` in `dedup_summary.json`; `apply_dedup.py` also rejects held-out rows |
| FR4 | A copy from an unusable pack never survives; all 38 packs listed explicitly | Waiting: G10's PR | G10 lists all 38 in Stage 0 (`saitej123:g10-week3-post-training`); `dedup.json` change on Fri |
| FR5 | `remove_list.csv` has exactly `pack_id, split, part, row_in_part, doc_id`, each row once | Met (v1) | `apply_dedup.py` checks (Sourav's pipeline) |
| FR6 | `dedup_groups.csv` lists every group's survivors and removed copies, for F2's survivor count | Met (12 Nov) | `dedup_groups.csv`; Sourav's `survivor_loss.py` reads it |
| FR7 | Empty documents are listed, never matched, never removed | Met (10 Nov) | `empty_documents.csv`; decision log, 10 Nov |
| FR8 | Same-URL pairs count as H2 at ≥ 0.80; math numbers compared on the body only | This week: Wed | Known-pair tests (to add) |
| FR9 | H3 is optional and report-only by default; when allowed, it removes only train translations of held-out documents, never within a parallel pack | Code done; waiting: Aneesha's `h3_matches.csv` format, TSAI's ruling | `g1-dedup-h3`: `h3_join.py`, `tests/test_dedup_h3.py` (10 tests) |

### Non-functional (how well)

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| NFR1 | Reproducible: same inputs and config give byte-identical outputs and group IDs | Met (v1) | Windows rerun gave the same `remove_list.csv` (`913e66a6…`); group IDs follow the lowest overlap row |
| NFR2 | Backward compatible: a new feature switched off gives byte-identical v1 output | Met for H3; this week for items 1, 2, 5 | H3: checked on 15 Nov; same test for each new switch |
| NFR3 | Traceable: summaries record input SHA-256s, the code SHA-256 and the git commit | This week: Mon | Sourav's `cleaning_pipeline.json` `code_sha256` no longer null |
| NFR4 | Reversible: dedup never rewrites data; every removal is logged with its rule and survivor | Met (v1) | `dedup_log.jsonl`; `apply_dedup.py` writes new parts, inputs unchanged |
| NFR5 | Safe: stops on mismatched inputs (SHA-256, `doc_id`, incomplete overlap run) | Met (v1) | `check_results()`, `read_urls()`; tests |
| NFR6 | No harm: zero gold documents removed | Met on 4 diagnosis packs; recheck with the #244 cleaner | 727 gold present, 0 removed (`results_v1.md`, section 3) |
| NFR7 | No document text in any output: IDs, scores and counts only | Met (v1) | Output review |
| NFR8 | Fast enough: vectorised PyArrow/SciPy, no Python loop per document; any GPU step batched (TSAI, 14 Nov) | Met for dedup | `benchmarks/2026-11-14-dedup-speed/` |
| NFR9 | Runs offline within the job's limits; dedup on Windows and Linux (overlap on Linux) | Met | `JOB_REQUEST.md` rules; dedup tests pass on Windows and Linux |
| NFR10 | Tested: every rule has a known-pair or unit test; each job request carries a fresh test log | Ongoing | `pytest` log attached to the rerun request (Thu) |

## Dependencies

| What | Who | Needed for |
|---|---|---|
| Overlap rerun on the #244 cleaning | TSAI (after lead approval) | Items 1 and 2 take effect; the dedup job |
| G10's licence table on `main` | Sai Teja (G10) | FR4, item 6 |
| `h3_matches.csv` keyed by document | Aneesha Das | FR9 in a real run |
| Ruling on H3 removals | TSAI | FR9 with `remove: true` |
| Answers on item 16 | Sourav Dhar, Vijay Patil | Tue's `run.json` |

## Log

| Date | Change |
|---|---|
| 16 Nov | Plan written; all 16 proposal items placed; week 2 laid out by support from other teams |
| 16 Nov | G10: `en-dclm` stays In (research line read as a disclaimer, noted for TSAI's Gate 3); FR4 still waits on G10's PR merging |
