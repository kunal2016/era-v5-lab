# Dedup plan for Weeks 3 and 4 (15–28 Nov 2026): v1 at scale, then the data card

**Owner:** Kunal Sinha (Data A dedup). **Status:** in progress; updated at most once a day, when a row changes.
**Follows the lab schedule:** Week 3 (15–21 Nov) is cleaning, dedup, decontamination and tokenizing at scale, with
Gate 3 on Sat 21 Nov (the first training shards pass the audit and match their manifests). Week 4 (22–28 Nov) is the
training-week shards, dry run 2 (24 Nov), `data_card_v1.md` and TSAI's data go or no-go on Sat 28 Nov.
**So dedup runs v1's rules, frozen** (as proposed on #255). `dedup_design_v2_proposal.md` is the backlog for after
training starts; nothing in it changes this run.

## Week 3 (15–21 Nov): dedup v1 at scale · Gate 3, Sat 21 Nov

| When | Work (proposal item) | Done when |
|---|---|---|
| Mon 16 | **Item 5:** `code_sha256` and git commit in `overlap_summary.json` and `dedup_summary.json`; part SHA-256s carried from overlap to dedup | Tests pass; outputs otherwise byte-identical to v1; Sourav's `cleaning_pipeline.json` gets the code hashes |
| Tue 17 | **Item 16:** answers to Sourav's 7 open items; the dedup job as a runner `run.json` (adopt the cleaning job's folder, `to: dedup`) | `run_pipeline.py --plan` passes on it |
| When G10's PR merges | **Item 6:** all 38 packs in `dedup.json` (`licence_usable`, `default_licence_usable: false`) | `licence_default_used_for` is empty in the summary |
| After the overlap rerun | **The dedup v1 job at scale**, through the runner (overlap → dedup → apply → F2 → survivor loss) | Lead approval; TSAI's run completes |
| Each day of the run | **Dedup audit:** `heldout_removed` = 0; harm check `pass`; `apply_dedup_summary.json` removed = `remove_list.csv` rows; `survivor_loss` counts; removals per pack against the 5 Nov run | One line per check in the daily audit pack; any problem filed as an issue |
| Each day (team) | **The schedule's audit duties:** daily audit packs; read 100 cleaned documents per source; compare text before and after cleaning; decode 20 documents per shard and check its manifest | Shared out by Vijay |

## Week 4 (22–28 Nov): shards and the data card · Gate 4, Sat 28 Nov

| When | Work | Done when |
|---|---|---|
| By Tue 24 | Dedup numbers for the dry run 2 shards: what was removed, per pack and rule | The shard manifests' dedup record matches `dedup_summary.json` |
| By Fri 27 | **Dedup section of `data_card_v1.md`:** method (H1, H2, family rules), survivor rules, counts per pack, held-out handling, harm check, known limits (no translations (H3); Indic minimum under review (E4); truncated copies under 80%) | Reviewed by Vijay |
| Sat 28 | Dedup part of the data report to TSAI | Sent with the data report |

## After training starts: the v2 backlog

All 16 items of `dedup_design_v2_proposal.md` stay in the backlog; none is dropped. Items 5, 6 and 16 are done in
Week 3 because the run at scale needs them. The rest start after launch, in this order:

| # | Item | Waits on |
|---|---|---|
| 1, 2 | Same-URL rule; math numbers on the body (behind switches, off = v1) | The first overlap rerun after launch |
| 4 | Code threshold hand review | The run's pairs |
| 3, 9 | Indic length minimum; Indic shingles if needed | E4 readers' labels |
| 7 | H3 (dedup side drafted on `g1-dedup-h3`; BGE-M3 run on Sanskrit) | Aneesha's `h3.py` format; TSAI's ruling |
| 8, 10, 11 | Containment; "changed least" survivor rule; MinHash + LSH test | The run's outputs; full-data size |
| 12 | Training ablation of the cross-pack pass | A pack's cross-pack removals reaching 1% |
| 13, 14, 15 | New sources from #461: pack order, non-document packs, licences | #461's packs joining; G10 |

## Requirements for the run at scale

Status: **Met** (with evidence), **This week** (with the day), **Waiting** (on whom).

### Functional

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| FR1 | Find exact (H1) and near (H2) duplicates within and across all 38 packs, with v1's family rules | Met (v1) | `dedup_design_v1.md`; TSAI's overlap run of 5 Nov |
| FR2 | Choose survivors in rule order: held-out, licence, URL, length, pack order | Met (v1) | `source_priority_v1.md`; `tests/test_dedup.py` |
| FR3 | Never remove a held-out document; report held-out ↔ held-out pairs | Met (v1) | `heldout_removed: 0`; `apply_dedup.py` also rejects held-out rows |
| FR4 | A copy from an unusable pack never survives; all 38 packs listed explicitly | Waiting: G10's PR | G10 lists all 38 in Stage 0 (16 Nov); `dedup.json` change when it merges |
| FR5 | `remove_list.csv` has exactly `pack_id, split, part, row_in_part, doc_id`, each row once | Met (v1) | `apply_dedup.py` checks |
| FR6 | `dedup_groups.csv` lists every group's survivors and removed copies, for F2's survivor count | Met (12 Nov) | `survivor_loss.py` reads it |
| FR7 | Empty documents are listed, never matched, never removed | Met (10 Nov) | `empty_documents.csv` |

### Non-functional

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| NFR1 | Reproducible: same inputs and config give byte-identical outputs and group IDs | Met (v1) | Windows rerun: same `remove_list.csv` (`913e66a6…`) |
| NFR2 | Backward compatible: item 5's change leaves every other output byte-identical | This week: Mon | Same check as for H3 on 15 Nov |
| NFR3 | Traceable: summaries record input SHA-256s, the code SHA-256 and the git commit | This week: Mon | `cleaning_pipeline.json` `code_sha256` not null |
| NFR4 | Reversible: dedup never rewrites data; every removal is logged | Met (v1) | `dedup_log.jsonl`; `apply_dedup.py` writes new parts |
| NFR5 | Safe: stops on mismatched inputs | Met (v1) | `check_results()`, `read_urls()`; tests |
| NFR6 | No harm: zero gold documents removed | Met on 4 diagnosis packs; recheck in the run | Harm check in `dedup_summary.json` |
| NFR7 | No document text in any output | Met (v1) | Output review |
| NFR8 | Fast enough for the full sample | Met | `benchmarks/2026-11-14-dedup-speed/` |
| NFR9 | Runs offline within the job's limits | Met | `JOB_REQUEST.md` rules |
| NFR10 | Tested; each job request carries a fresh test log | Ongoing | `pytest` log with the dedup job request |

## Dependencies

| What | Who | Needed for |
|---|---|---|
| Overlap rerun on the #244 cleaning | TSAI (after lead approval) | The dedup job at scale |
| G10's licence table on `main` | Sai Teja (G10) | FR4, item 6 |
| Answers on item 16 | Sourav Dhar, Vijay Patil | Tue's `run.json` |
| Audit duties shared out | Vijay Patil (lead) | Week 3's daily audit packs |

## Log

| Date | Change |
|---|---|
| 16 Nov | Plan written; then aligned to the lab schedule (Weeks 3 and 4): v1 frozen for the run at scale, v2 work after launch |
| 16 Nov | G10: `en-dclm` stays In (research line read as a disclaimer, noted for TSAI's Gate 3); FR4 waits on G10's PR merging |
