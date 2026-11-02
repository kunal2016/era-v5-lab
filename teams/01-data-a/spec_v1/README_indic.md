# Indic integration

The generated cleaner now includes the Indic family from `sheets/medicine_indic.md`. The original source sheet and contributor functions remain unchanged. The consolidated `sheets/specv1.md` contains all 176 source cards, with 115 selected candidates and 61 explicitly deferred cards. The final cleaner has 185 sheet rules plus the existing shared F1, across five families and 26 packs.

Selections remain CANDIDATE. Loading and compatibility checks do not establish positive-case recall or independent approval.

## Selection and deferred rules

`tools/integrate_indic.py` checks return values, mutation, ordinary synthetic prose, ZWJ/ZWNJ preservation, idempotence and unrelated-pack guards. It checks source rules on available full diagnosis packs for runtime errors and single-rule idempotence, then iteratively defers rules that act again after the selected full pipeline. It also runs every source rule on its own current gold when both the week-1 diagnosis pack and Data B gold file exist. Missing inputs are NOT TESTABLE. Combined gold failures defer the affected pack's selected pipeline.

For each of the 43 overlapping pack/disease groups, the first eligible source candidate is provisionally selected; later alternatives are deferred. This avoids stacking competing treatments. It is a deterministic integration choice, not a finding that the selected rule has better precision or recall. Positive-case review is still required.

Four C3 candidates fail synthetic ordinary-prose/joiner probes: `DB-C3-003`, `DB-C3-005`, `DB-C3-009`, `DB-C3-012`. Both F2 candidates are deferred: `DB-F2-001` needs an approved benchmark and `ITIHASA_TEST_SN`; `DB-F2-002` returns text unchanged and does not implement benchmark remediation. Source algorithms are not silently patched or wrapped in exception-to-keep fallbacks.

Each deferred card has `STATUS = "DEFERRED"`, `DEFER_REASON`, and a `python deferred` fence. These fences are intentionally excluded by the repository harm runner. The builder validates the complete numbered inventory but emits only executable candidates. `clean.DEFERRED_RULES` records the exclusions; they are absent from executable `SCOPE`, `_RULE`, and family pipelines.

All 176 source IDs retain their `DB-` prefix. The builder accepts both `DA-` and `DB-`, recognizes the Indic `_PACKS = frozenset(ORIGIN.split(", "))` guard, intersects it with `SPEC_PACKS`, and redirects both to its central `SCOPE` table. Each rule still has an isolated closure. New disease functions include D2, D5, F3, G1, G2, G4 and H3. All G3 and F2 candidates are deferred in this snapshot, so those functions are not emitted; the builder supports them when an eligible rule is added. F1 remains last in the disease registry; per-family execution follows source section order.

## Scope and privacy

Indic uses the pack guard, independently of whether a source language tag uses `mr` or `mar_Deva`. The shared F1 remains restricted to code, math and science; Indic uses its selected source F1 rules. Six covered packs lack a selected F1 candidate: `ind-bn-fw2`, `ind-hi-fw2`, `ind-kn-sangraha-s`, `ind-kn-sangraha-v`, `ind-ta-sangraha-v`, `ind-te-sangraha-s`. Do not interpret a clean gold pass as full privacy coverage.

The source sheet covers 13 Indic packs. The other nine Indic packs in the week-2 manifest have no rules here. `run_clean.py` rejects unsupported packs, as before.

## Rebuild and validate

Run from the repository root, using Python with `spec_v1/requirements.txt` installed:

```bash
python teams/01-data-a/spec_v1/tools/integrate_indic.py \
  --packs ../erav5-lab-other-files/packs \
  --gold teams/02-data-b/gold
python teams/01-data-a/spec_v1/tools/build_clean.py
python -m pytest teams/01-data-a/spec_v1/tests -q
python teams/01-data-a/spec_v1/tools/validate_specv1.py \
  --packs ../erav5-lab-other-files/packs \
  --gold teams/01-data-a/gold \
  --indic-gold teams/02-data-b/gold \
  --allow-missing
```

The integration step refreshes the adapted Indic cards and decisions. The builder still reads only the consolidated spec: rerunning it alone does not discover changes to an individual medicine sheet. To promote or change a selection, update the review policy/source evidence, rerun integration, rebuild, and validate.

The validator uses the repository minimum-one policy, `max(1, floor(1% × gold_count))`. With `--allow-missing`, it records missing inputs and exits 2; actual test failures exit 1. Exit 0 requires all required inputs and tests to pass. The sheet validator tests the executable sheet; generated-cleaner validation additionally exercises dispatch, closures and the shared F1.

Week-2 training shards are not substitutes for the week-1 diagnosis packs: they intentionally contain different document IDs. All 13 covered Indic diagnosis packs and own-pack gold CSVs are now available. The selected source pipelines pass on every pack: Sanskrit changes 1/68 gold documents, within the one-document allowance; the other 12 change or drop none. Generated-cleaner and full-pack results are recorded separately below.

For an independent comparison with the cleaner before integration:

```bash
git show a6eab62:teams/01-data-a/spec_v1/clean.py > /tmp/clean_before_indic.py
python teams/01-data-a/spec_v1/tools/check_indic_integration.py \
  --packs ../erav5-lab-other-files/packs \
  --gold teams/02-data-b/gold \
  --baseline /tmp/clean_before_indic.py
```

This compares actions and text for the original 13 packs, distinguishes matching pre-existing exceptions from new regressions, and tests available Indic gold, full packs and second-run changes. It exits 2 for missing Indic inputs and 1 for regressions, failures, new errors or non-idempotence. A matching baseline exception is recorded, not represented as successful cleaning.

## Measured verification

- The full unit/contract suite passes 774 tests.
- All 13 Indic generated pipelines pass their own gold sets (1,093 documents total); Sanskrit changes 1/68, allowed by the minimum-one policy. No gold document is dropped.
- All 6,500 Indic diagnosis documents execute without errors, and every retained output is unchanged on a second pass.
- Comparing all 6,500 original code/English/math/science documents with the saved baseline finds zero behavior differences. Three documents raise the same pre-existing exceptions in both cleaners (one Java, two Python); they remain recorded rather than counted as successful cleaning.
- Synthetic source/factory equivalence, pack isolation, joiners, source-trigger cases and build reproducibility are covered by the tests. These checks do not prove positive-case recall or final approval.

## Evidence

- `results/cleaner/indic_integration.json`: source digest, every candidate's decision, all overlap selections, synthetic findings and current own-pack gold tests.
- `results/cleaner/specv1_validation.json`: executable sheet rules and combined pipelines, per-pack snapshots, missing inputs and out-of-pack guard checks.
- `results/cleaner/indic_clean_validation.json`: generated cleaner versus the saved baseline, Indic gold/full-pack outcomes and second-run changes.

Reports contain IDs, counts, digests and error types, not source text. The original four medicine sheets, shared F1 implementation and normalization fingerprints are unchanged by this integration.
