# H3 E5d: questions for G2 (22 Nov 2026)

H3 finds the same content in two languages ([h3_design_v1.md](h3_design_v1.md)). E5d sets its sentence thresholds
per language pair from blind labels by bilingual readers. Each reader marks a candidate pair as a translation or not,
on both sides of each threshold. The candidates come from E5c (#625) and, for the Sanskrit pairs, from the BGE-M3 job
(#666). Both jobs are approved and have not run yet.

This file asks G2 for readers, for labelled pairs, and for its view on H3's exemptions and exclusions.

## What TSAI has decided

| Date | Decision | Where |
|---|---|---|
| 19 Nov | Scope: Indic ↔ English and Sanskrit ↔ Hindi, prose packs only. Packs with several languages (Pralekha) are designed before they join | #625 |
| 21 Nov | Odia ↔ English stays report-only until Odia has gold. E5d labels the Sanskrit candidates of both LaBSE and BGE-M3 | #626 |
| 21 Nov | Gate 3: native-script Indic is 8% of every batch; romanised Indic is at most 1% of tokens per language | [gate3.md](../../11-release/updates/gate3.md) |
| 22 Nov | corpus-v1's 38 sample-v0 packs are final; no pack is added without a separate ruling | [approved_inputs.json](../jobs/2026-11-19-first-training/approved_inputs.json) |

## E5c's packs against corpus-v1 and the Gate 3 mix

E5c reads 10 packs ([h3.json](../jobs/2026-11-18-h3-e5c/h3.json)). Mix shares are from
[indic_share_v1.csv](../../02-data-b/mix/indic_share_v1.csv).

| Pack | Language | In corpus-v1's 38 | In the mix |
|---|---|---|---|
| `ind-sa-fw2` | sa | yes | yes: 0.95% of every batch |
| `ind-hi-fw2`, `ind-hi-hplt`, `ind-hi-indiccorp`, `ind-hi-sangraha-v` | hi | yes | yes: 1.97% of every batch for the four |
| `ind-hi-sangraha-s` | hi | yes | 0%: machine-translated, until TSAI admits a translated language |
| `ind-or-fw2` | or | yes | 0%: no shard yet |
| `en-fineweb-edu`, `en-dclm`, `en-nemotroncc` | en | yes | yes, outside the 8% |

`en-nemotroncc-synth` is in corpus-v1 but not in E5c: it is synthetic rephrasings.

## 1. Readers and labelled pairs

| # | Question | Our reading or proposal | G2's answer |
|---|---|---|---|
| 1.1 | Who can read Sanskrit–English and Sanskrit–Hindi? | The readers of the `ind-sa-fw2` gold set (dattatreyamanjunath, swatibansal), if they read English and Hindi. [readers.md](../../02-data-b/readers.md) has no Sanskrit reader in Data B | Open |
| 1.2 | Who can read Hindi–English? | Any reader of [hindi_gold.csv](../../02-data-b/gold/hindi_gold.csv) who also reads English | Open |
| 1.3 | Who can read Odia–English? | [readers.md](../../02-data-b/readers.md) has one Odia reader, Pritish52718. A second one would also make an Odia gold set possible | Open |
| 1.4 | How many pairs, and how many readers per pair? | About 100 pairs per language pair, two readers each, as for gold. The sheets go out when E5c and #666 return | Open |
| 1.5 | Which labelled translation pairs exist for these languages, and where are they from? | Known to us: FLORES-200, an evaluation set used only for the encoder check; G2's `sangraha-s` ratings (kn, ta, te), which score translation quality, not translation or not | Open |

## 2. Exemptions and exclusions

| # | Question | Our reading or proposal | G2's answer |
|---|---|---|---|
| 2.1 | Which packs are parallel by design? H3 makes no edge inside such a pack (H3-d, [h3_design_v1.md](h3_design_v1.md)) | None of corpus-v1's 38. Pralekha and BPCC are in [indic_sources_v1.md](../../02-data-b/indic_sources_v1.md) but not in corpus-v1, so the exempt list is empty for v1.1 | Open |
| 2.2 | `ind-hi-sangraha-s` is IndicTrans2 translations of English Wikipedia, and 0% of the mix | Keep it in H3's counts, as its own row in `h3_by_pack.csv`; not exempt | Open |
| 2.3 | `ind-or-fw2` has no shard yet, so it is 0% of the mix | Keep it in H3's counts; report-only (TSAI, #626) | Open |
| 2.4 | `en-nemotroncc-synth` is left out of E5c | Agree? | Open |
| 2.5 | Does G2 want any other pack excluded or exempted? | None proposed | Open |
