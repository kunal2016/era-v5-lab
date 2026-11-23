# Decision: overlap (H1/H2) for corpus-v1, plan item 1.5 (23 Nov 2026)

**Decision.** Corpus-v1 runs **v1's exact overlap method, unchanged**, under the size gate in the job request (#718,
updated in #728). Before the job, `overlap.py`'s 50 MB output check is **fixed so it does not stop the run** (it fails
at about 1.15× the sample today). If the staged rows are over the memory or time gate, TSAI **provisions a larger
host** for the same method. **MinHash + LSH is not used for corpus-v1.** It stays a documented, tested fallback for a
later corpus. Decided by DataA Dedup on the Instructor's instruction of 22 Nov to decide now, on the
38-pack rehearsal extrapolation.

## Basis

38-pack rehearsal (#599, sample-v0, 1.41 M cleaned docs): overlap **14.0 GB peak, 84 min**, on one core. Stages: read
and shingle 770 s, word scoring 190 s, H1/H2 rules and code-token pass about 4,065 s (mostly Pygments lexing). Outputs
43.6 MiB, 32.7 MiB of them `overlap_docs.parquet` (one row per document).

| Rows vs sample | Overlap outputs | Overlap peak RAM | Overlap time, linear | Overlap time, quadratic scoring |
|---:|---:|---:|---:|---:|
| 1× | 44 MiB | 14 GB | 1.4 h | 1.4 h |
| 1.15× | **50 MiB (current limit)** | 16 GB | 1.6 h | 1.6 h |
| 2× | 87 MiB | 28 GB | 2.8 h | 2.9 h |
| 3× | 131 MiB | 42 GB | 4.2 h | 4.5 h |
| 4× | 174 MiB | 56 GB | 5.6 h | 6.2 h |
| 5× | 218 MiB | 70 GB | 7.0 h | 8.0 h |

The superlinear risk the lead raised about #718 (G1, 22 Nov; job request wording fixed in #728) is real but bounded.
Only word scoring grows faster than the row count, and it was 190 s of 5,025 s, so even at 4× the quadratic case adds
about 40 minutes. Memory and outputs stay about linear.

## How it is applied

1. **Output limit: fix before the job.** `overlap.py` fails at its end when its outputs pass `max_output_mb`, which it
   caps at 50 (#728 notes this). JOB_REQUEST.md's 50 MB rule is for what a job **returns to the repository**; inside
   the pipeline job, overlap's files stay in TSAI's job storage and only summaries are returned. So the check should
   not stop a pipeline run. The change is small and does not touch the method (for example, a higher limit when the
   runner starts overlap, or not counting `overlap_docs.parquet`); Data A raises it as
   its own PR, with a test. H3's `h3_docs.parquet` has the same kind of limit and is checked in the same PR.
2. **Memory and time gate, as in #718.** After `build_inventory.py`, TSAI reads the staged `raw_rows` against
   sample-v0's 1,444,766. 64 GiB covers up to about **4×**, and 720 minutes up to about **4.5×** (use the quadratic
   column near the limit).
3. **Over that gate: provision, don't change the method.** Size RAM at about 14 GB per 1× plus headroom, and raise Max
   time to match. Do not start a run that the estimate says will not fit.
4. **Recovery.** If overlap fails, the runner's `"from": "overlap"` continues at overlap after checking the earlier
   stages' outputs, so cleaning is not repeated (#728). Overlap itself has no checkpoint and reruns from its start.
5. **Evidence back.** Overlap's peak RSS, runtime and output size are required in the returned log, to check the
   scaling.

## Why not MinHash for corpus-v1

Tested (dedup v2 item 11, `teams/01-data-a/dedup/minhash/` on `kunal2016:g1-dedup-minhash`): 32×4 bands found every v1
qualifying pair on the train parts of 11 packs (50 H1, 1,924 H2 word; 559 H2, 1 H1 code), at about 1.1 KB per
document against v1's ~10 KB (an estimate, not measured). It is not used this week because:
- **Not built.** It needs a change to `overlap.py` (candidate step plus a re-read to verify), new tests and a
  rehearsal. None of that fits before Tue 24.
- **Not fully tested.** Held-out↔train pairs (the contamination case), `code-cpp/java/js-ts`, a second seed and
  cross-pack pairs are untested.
- **It changes the agreed method** and would need its own TSAI ruling and a data card note.
- **It does not fix time or the output limit.** Pygments lexing, most of overlap's 84 minutes, stays the same, and it
  writes the same per-document files. A larger host fixes memory and time; the output fix above is needed either way.

## Revisit when

- the staged rows are over about 8× (more than about 112 GB for overlap alone) and TSAI cannot provision that host, or
- planning a larger corpus after corpus-v1. Then finish the untested items, implement behind a config switch
  (`overlap.candidates: exact | minhash`, default `exact`), and bring it to TSAI with a rehearsal.

A later switch stays inside the overlap stage. Dedup (`dedup.py`) and apply (`apply_dedup.py`) read overlap's pairs
file and do not change, as long as overlap writes the same pairs; on the tested packs it did.