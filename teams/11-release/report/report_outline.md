# ERA V5 Lab: run report outline

**Date:** 3 Nov 2026
**Owner of this outline:** Release

The run report is the long public document that explains how the lab built and trained the model.
The V4 run report (https://lightninglm.theschoolofai.in/) is the model for its shape.
This file lists the sections of the run report.
Each section has an owner team, a status and a lead confirmation.

## How to use this outline

- The owner team writes the text of its section.
- Release edits the text for style and runs `check_style.py` on it.
- TSAI approves the text before it goes into the run report.
- A section can have more than one owner team. The first team named leads the section.

**Status** is one of these:

- **empty:** nobody has written the text yet.
- **in progress:** the owner team is writing the text.
- **approved:** TSAI approved the text.

**Lead OK** tracks whether the lead of each owner team confirmed the section and its scope.
Write `pending` until they confirm. Then write `OK` and the GitHub handle of each lead who confirmed.
For a shared section, record an OK from the lead of each owner team.
This confirms the outline only. TSAI still approves the final text.

## Sections

| Section | Owner team | Status | Lead OK |
|---|---|---|---|
| Abstract | Release | empty | pending |
| Introduction | Release, Data B, Evaluation | empty | pending |
| Background and Related Work | Release, Data A, Tokenizer, KE2, Architecture, Post-training | empty | pending |
| Training Data | Data A, Data B, Evaluation | empty | pending |
| Tokenizer | Tokenizer | empty | pending |
| KE2 | KE2 | empty | pending |
| Model Design | Architecture | empty | pending |
| Training Speed and Correctness | Performance, KE2 | empty | pending |
| Training Infrastructure | Infrastructure | empty | pending |
| Monitoring the Training Run | Monitoring | empty | pending |
| The Training Run | Infrastructure, Data A, Architecture, Monitoring | empty | pending |
| What Went Wrong and How We Fixed It | Monitoring, Infrastructure | empty | pending |
| Post-training | Post-training | empty | pending |
| Quantization and Serving | Quantization | empty | pending |
| Results | Evaluation, Quantization | empty | pending |
| Limitations | Evaluation, Release | empty | pending |
| Reproducibility | Release, Architecture, Infrastructure | empty | pending |
| Licence and Attribution | Post-training, Data A, Data B | empty | pending |
| Conclusion | Release | empty | pending |
| Contributors and Acknowledgments | Release | empty | pending |
| Resources and Citation | Release | empty | pending |

## Rules for every section

- Write only about work that is done. Do not promise dates, sizes or results.
- Write `[number: waiting for TSAI]` in place of any number that TSAI has not approved.
- Name a person only if they signed the consent form.
- Follow `teams/11-release/style/style_guide.md`.
