# ERA V5 Lab: week 2 update

**Date:** 04 Nov 2026
**Period:** 01 Nov to 04 Nov 2026

The teams of the ERA V5 lab continued their week-1 work and started their week-2 tasks.

## The teams

- **Data A:** Integrated Indic rules, fixed privacy masking. TSAI ran the cleaner on the tokenizer sample. Planned: deduplication design, cleaned document audits, benchmark checks, shard format.
- **Data B:** <text from the team>
- **Tokenizer:** <text from the team>
- **KE2:** <text from the team. The first time, say in a few words what KE2 is.>
- **Architecture:** <text from the team>
- **Performance:** <text from the team>
- **Infrastructure:** <text from the team>
- **Monitoring:** Monitoring built the ClickHouse metric store, the private Grafana dashboard, checkpoint alarm restore, and the node health validator with Infrastructure.
- **Evaluation:** <text from the team>
- **Post-training:** <text from the team>
- **Release:** Release finished the first weekly update, added a test for the number check, and drafted outlines for the model card and the report.
- **Quantization:** <text from the team>

## Next week

After a break, the teams finish their week-2 tasks.

---

## Review record (remove this section before publishing)

This record is public, like the rest of the pull request. Put only public facts in it: yes or no, and links to
public pull requests. Never link to the CAP chat. Chat links are internal.

How to fill it:

1. Collect the text for each team.
   - Week 1: one sentence from each lead. Ask the leads in the CAP chat, and give the due day.
   - From week 2: one short paragraph for each team, from the rotating student of that team or from the lead.
2. Paste each text above. Edit it only for style, and send the edit back to the writer.
3. Mark "Lead OK" when the lead of that team says OK to the final text.
4. Give the source of each fact: a public pull request or a file in this repository. Gate 4 needs a source for
   each fact.
5. Write `[number: waiting for TSAI]` for any number that TSAI has not approved yet.
6. Run `python teams/11-release/style/check_style.py <this file> --numbers` and clear every error.

| Team | Text received | Lead OK | Source |
|---|---|---|---|
| Data A | Yes | Yes | [#244](https://github.com/theschoolofai/era-v5-lab/pull/244) (open), [#255](https://github.com/theschoolofai/era-v5-lab/pull/255) (open) |
| Data B | no | no | |
| Tokenizer | no | no | |
| KE2 | no | no | |
| Architecture | Yes | no (waiting for a new sentence) | [#180](https://github.com/theschoolofai/era-v5-lab/pull/180), [#197](https://github.com/theschoolofai/era-v5-lab/pull/197) |
| Performance | no | no | |
| Infrastructure | no | no | |
| Monitoring | Yes | Yes | [#250](https://github.com/theschoolofai/era-v5-lab/pull/250) (open), [#260](https://github.com/theschoolofai/era-v5-lab/pull/260) (open), [#136](https://github.com/theschoolofai/era-v5-lab/pull/136) (open), [#125](https://github.com/theschoolofai/era-v5-lab/pull/125) (open) |
| Evaluation | no | no | |
| Post-training | no | no | |
| Release | Yes | no | [#142](https://github.com/theschoolofai/era-v5-lab/pull/142), [#152](https://github.com/theschoolofai/era-v5-lab/pull/152), [#234](https://github.com/theschoolofai/era-v5-lab/pull/234), [#237](https://github.com/theschoolofai/era-v5-lab/pull/237), [#264](https://github.com/theschoolofai/era-v5-lab/pull/264) (open) |
| Quantization | no | no | |

- [ ] `check_style.py` gives 0 errors
- [ ] Every number in the text has TSAI approval
- [ ] Every person named has signed the consent form
- [ ] Nothing from the internal list in `public_internal.md`
- [ ] No `[number: waiting for TSAI]` left in the text
- [ ] The G11 lead reviewed the pull request (a pull request from the lead: a team member commented)
- [ ] Sent to TSAI on: <DD Mon YYYY>
- [ ] TSAI approved on: <DD Mon YYYY>
- [ ] Merged after TSAI approved
