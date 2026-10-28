# Data A tools: hex check and medicine guide

Two additions next to the team's harm-test tools (`medicine_extract.py`, `harm_test.py`,
`rule_report.py`, `build_gold.py`).

| File | What it is |
| --- | --- |
| `hexcheck.py` | For one or more doc_ids, lists only the unusual characters in the whole document (no 2,000-character limit), with a hint per character (A1 to A6), and G-group candidates: G1 word cut before a vowel sign or virama, G2 joiner not after a virama, G4 Latin digit inside an Indic number, characters an NFKC step would change, and for Indic-labelled documents G3 hints (traces of dropped text). Prints ready `hex` cells in the agreed format |
| `MEDICINE_GUIDE.md` | One proposed layout for every `medicine.md` (code, English, maths, science, Indic), in the format the team's extractor reads, with the rules every medicine follows and what a rule must never touch per domain |

## hexcheck.py

Requires `pip install pyarrow`.

```
python -I teams/01-data-a/tools/hexcheck.py <pack>.parquet <doc_id> [<doc_id> ...]
```

It finds candidates only. In an Indic document, the ordinary letters, signs and digits of the
document's own script are treated as normal and not listed. G3 (Indic text dropped by an
English-only step) has no character to point at, so it gives hints instead: under half the
letters in the labelled script, three or more empty lines in a row, headings or list items with
nothing after them, and text that ends mid-sentence. G3 has no hex cell: put a short quote and the
offset in `evidence`. A missing joiner (G2) cannot be seen from the characters: judge it by reading.
