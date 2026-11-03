# Source Priority v1 : Which copy survives

Status: **DRAFT — proposed, not yet agreed by the team.**

When dedup (`dedup_design_v1.md`) finds a group of duplicates, exactly one copy survives. The rules below are applied **in order**; each rule only breaks ties left by the one above. The rule that decided is recorded in `dedup_log.jsonl` (`priority_rule`).

| Order | Rule | What it means |
|---|---|---|
| 1 | Licence first | Only copies with a usable licence can win |
| 2 | Provenance | Prefer the copy whose origin is fully known |
| 3 | Completeness | Prefer the longer (complete) copy over a truncated one |
| 4 | Fixed pack order | Deterministic final tie-break |

## 1. Licence first

- **Usable:** permissive licences (e.g. MIT, Apache-2.0, BSD, CC-BY, CC0/public domain) and CC-BY-SA.
- **Not usable:** any NC (non-commercial), any ND (no derivatives), and unstated licences.
- A copy with an unusable licence **never wins**, even if it is better on every other rule.
- If **no** copy in the group has a usable licence, the whole group is removed (none of it should be in the data anyway).

Source: Week 2 licence rule; licence classification follows G10's table, `teams/10-post-training/licences/licence_table.md`.

## 2. Provenance

Prefer the copy for which **source URL, dataset and licence** are all known. Score each copy by how many of the three are present; highest wins.

The provenance record of the survivor (source URL, dataset, licence) is kept with the surviving document. The removed copies' IDs are kept in the dedup log, so their provenance remains traceable.

## 3. Completeness

Prefer the copy with the **longer normalised text**, so a complete copy wins over a truncated one.

**"Fewer fixes" is dropped for v1.** No per-document fix record exists:

| Where | Per document | In total |
|---|---|---|
| `clean.py` | only the action (`keep`/`fix`/`drop`) and the new text | nothing |
| `run_clean.py` summary | dropped and error `doc_id`s | counts of keep, fix, drop |
| `run_tokenizer_sample.py` | nothing | per-rule keep/fix/drop counts per part (`rule_counts.csv`) |

**v2 candidate: measure how much cleaning changed each copy.** Raw text (sample input) and cleaned text (job output) share a `doc_id`, so for each duplicate pair dedup can compute the change, e.g. `1 - difflib ratio` or the character difference, and keep the copy that changed least. This needs no code change to the cleaning tools, and it is a better signal than a rule count: one rule may touch one character or rewrite half a document. Cost: reading both texts, only for the pairs dedup finds.

(Alternative considered: have the sample job's per-rule wrapper write a fix count or the rule IDs into each output row. It is a change to Vijay's tool and the job evidence would need rerunning, so it is not planned for v1.)

## 4. Fixed pack order

Final tie-break so that every run gives the same result. Pack order: **to be agreed** (proposal: the order packs are listed in the spec, earliest first). Within one pack, the lowest document ID wins.

## Example

Three copies of the same article:

| Copy | Pack | Licence | URL/dataset/licence known | Truncated | Result |
|---|---|---|---|---|---|
| A | science | CC-BY-NC | 3/3 | no | out at rule 1 (NC) |
| B | science | CC-BY | 2/3 | no | out at rule 2 |
| C | math | CC-BY-SA | 3/3 | no | **survives** (decided by rule 2) |

## Open questions for the team

- Agree the pack order for rule 4.
