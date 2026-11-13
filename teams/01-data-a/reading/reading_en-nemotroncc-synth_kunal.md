# Reading: en-nemotroncc-synth, 50 cleaned docs (kunal)

## How it was read

- Pack files: "Week 2: cleaned tokenizer sample v0-clean", Train `en-nemotroncc-synth/part-00000.parquet` (Part 1) and `part-00001.parquet` (Part 2). Heldout not used.
- Docs: rows **1-50** of `pick_docs.py` (Part 1 then Part 2, 196,907 docs, seed **20261101**). These are the en-nemotroncc-synth half of row 7 (Harini Jasti), taken over to make the spec v1.1 deadline.
- Cleaner: spec v1 `clean.py` of PR #244, as in v0-clean. Checked: the cleaned text of all 50 docs is identical to the output of `clean.py` at `c0b29d1` (patilvijay23/g1-specv1). Cleaning changed 1 of the 50 (`DA-B4-007`); 49 are unchanged; none dropped.
- AI used: <yes/no: describe, e.g. "AI used only to find offsets; every finding read and checked by me">.
- Offsets are character start-end (0-based, end exclusive) in the cleaned text.

<details><summary>doc_ids read (50)</summary>

```
878f9d48ad498922
5aeafd200220c080
f0a4a58b7f9a01e3
8e8d8d665724ee0e
482459b361873245
5ffd22882ba35f3e
7264a177c61434df
0f7b90400c1362df
d8dcee236fef69c3
ccabc5a234934fd0
66059039c4d0cd16
488b525016dbab19
cb69e3410c5bc9df
70ab4763836d77e3
390b9ed0ffbd7fb6
0407920ed49eb6af
82aa41d29e468a85
6ab044802b5ccaed
280503e96a840313
23b10d26ac886d57
51a0b4027f575f76
58f93564f62c3f74
638aac23790e95ea
c4aadf93ec2178b1
9d81ac9b8c93267a
7d820d691c590509
ea84635879759482
bea84f90415a5b5d
92575d2502926a56
40d51909df47f1e0
0f7240ba1fdd3411
94c2efea7c6ce4f6
2c33678d82db9ffa
55eb060ae2bc2600
18fa47308d9fe79e
ffaad5c6d3dde332
c3d88009d8a459e9
f417dd85463514c8
b4281ea0782a6671
52bd1da881ee0592
6d46a2f7ae209851
b36e53dbb443169d
ff4162ecf3f8c204
1877686d8ee63f8c
c9cc0b7d991bbf9f
afec255188660355
f2a8b2cc25bb5c7a
420d6e3cde0965e4
bf1cefdecf84bf1a
af5340cf280d1651
```
</details>

## Findings

| code | kind | docs affected | % of docs read |
|---|---|---|---|
| | | | |

Clean docs (no findings): <n> of 50.

## New diseases

| name | description | docs |
|---|---|---|
| | | |

## Harm

| rule ID | what it deleted or damaged | docs |
|---|---|---|
| | | |

## Open questions for the lead

-
