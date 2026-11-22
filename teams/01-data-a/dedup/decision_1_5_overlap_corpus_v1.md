# Decision: overlap (H1/H2) for corpus-v1, plan item 1.5 (22 Nov 2026)

**Decision.** Corpus-v1 runs **v1's exact overlap, unchanged**, under the size gate already in the merged job request
(#718). If the staged rows are over that gate, TSAI **provisions a larger host** for the same method. **MinHash + LSH is
not used for corpus-v1.** It stays a documented, tested fallback for a later corpus. Decided by Kunal Sinha (Data A
dedup) on the Instructor's instruction of 22 Nov to decide now, on the 38-pack rehearsal extrapolation.

## Basis

38-pack rehearsal (#599, sample-v0, 1.41 M cleaned docs): overlap **14.0 GB peak, 84 min**, on one core. Stages: read
and shingle 770 s, word scoring 190 s, H1/H2 rules and code-token pass about 4,065 s (mostly Pygments lexing).

| Rows vs sample | Overlap peak RAM | Overlap time, linear | Overlap time, quadratic scoring |
|---:|---:|---:|---:|
| 1× | 14 GB | 1.4 h | 1.4 h |
| 2× | 28 GB | 2.8 h | 2.9 h |
| 3× | 42 GB | 4.2 h | 4.5 h |
| 4× | 56 GB | 5.6 h | 6.2 h |
| 5× | 70 GB | 7.0 h | 8.0 h |

The superlinear risk Vijay raised on #718 is real but bounded. Only word scoring grows faster than the row count, and it
was 190 s of 5,025 s, so even at 4× the quadratic case adds about 40 minutes. Memory stays about linear.

## How it is applied

1. **Gate, as in #718.** After `build_inventory.py`, TSAI reads the staged `raw_rows` against sample-v0's 1,444,766.
   64 GiB covers up to about **4×**, and 720 minutes up to about **4.5×** (use the quadratic column near the limit).
2. **Over the gate: provision, don't change the method.** Size RAM at about 14 GB per 1× plus headroom, and raise Max
   time to match. Do not start a run that the estimate says will not fit.
3. **Recovery.** If overlap fails, the runner's `"from"` continuation restarts at overlap with prior-output checks, so
   the cleaning time is not lost. The job request's wording is being corrected in #728.
4. **Evidence back.** Overlap's peak RSS and runtime are required in the returned log, to check the scaling.

## Why not MinHash for corpus-v1

Tested (dedup v2 item 11, `teams/01-data-a/dedup/minhash/` on `kunal2016:g1-dedup-minhash`): 32×4 bands found every v1
qualifying pair on the train parts of 11 packs (50 H1, 1,924 H2 word; 559 H2, 1 H1 code), at about 1.1 KB per
document against v1's ~10 KB. It is not used this week because:
- **Not built.** It needs a change to `overlap.py` (candidate step plus a re-read to verify), new tests and a
  rehearsal. None of that fits before Tue 24.
- **Not fully tested.** Held-out↔train pairs (the contamination case), `code-cpp/java/js-ts`, a second seed and
  cross-pack pairs are untested.
- **It changes the agreed method** and would need its own TSAI ruling and a data card note.
- **It does not fix time.** Pygments lexing, most of overlap's 84 minutes, stays the same. A larger host does fix both
  memory and time.

## Revisit when

- the staged rows are over about 8× (more than about 112 GB for overlap alone) and TSAI cannot provision that host, or
- planning a larger corpus after corpus-v1. Then finish the untested items, implement behind a config switch
  (`overlap.candidates: exact | minhash`, default `exact`), and bring it to TSAI with a rehearsal.

## Owners

Kunal Sinha: this note; the MinHash follow-ups if revisited. Smita Sasindran: plan 1.5 and #728. TSAI: the row count,
host sizing, and the go/no-go at the gate.
