# Maths medicines

Status: DRAFT. The medicines of the maths packs as rules that the team's tools run unchanged.

| File | What it is |
|---|---|
| `medicine_math.md` | the standard sheet: 11 rules, one `RULE_ID` block each, in the form of `code-medicines/medicine_code.md`. Each section follows the medicine template of `diagnosis/DISEASES.md` and ends with the decision of guideline 2. |

## Run

```
python -I teams/01-data-a/tools/harm_test.py --pack math-finemath.parquet --gold teams/01-data-a/gold/math-finemath_gold.csv --rules teams/01-data-a/math-medicines/medicine_math.md --rule all
python -I teams/01-data-a/tools/harm_test.py --pack math-finemath.parquet --gold teams/01-data-a/gold/math-finemath_gold.csv --rules teams/01-data-a/math-medicines/medicine_math.md --rule DA-C1-007
```

The sheet needs the `harm_test.py` of PR #4 (`g1-harm-test-code-medicines`), which reads one rule per block and has `--rule all`. The pack Parquet files are not in the repo.

## Where the rules come from

- math-finemath has one medicine sheet, Owner1's. It describes 15 medicines well in words, but its code blocks are fragments (`medicine_extract.py`: 0 rules), and her full code (`medicines.py`) is not in the repo.
- The 11 rules here are written by kunal2016 from her words, then checked against both label sheets (Owner1 500 rows, Owner2 155 rows) and the 20 rows a third reader adjudicated. Reach matches her reported numbers for 10 of 11 rules; C1 is lower (47 vs 109) because her ~70-phrase list is not printed.
- math-megamath: no medicine sheet and an empty gold set.

## Open questions (team decisions)

1. **C1 ruling.** Owner1 marks C1 on 328 of 500 documents; Owner2 calls most small site chrome clean. This decides the size of the gold set (30 today; up to ~150-200 if small chrome counts as clean) and what the C1 rule may strip: a document with chrome cannot be gold if the C1 rule removes that chrome.
2. **F1.** Are forum usernames personal data? Is a full name with age and town (rows 35, 107 of the adjudication)? Are business contacts (staff email and phone on a university page) left alone?
3. **F2.** Are olympiad problems (IMO) a benchmark leak? They are not in the evaluation team's decontamination list.
4. **Gold size.** 30 gold documents make the 1% limit a zero-change limit. A second full read of math-finemath (Owner2 has 155 of 500) is the main way to grow it.

## Notes

- `LANGS = {"en"}`: the maths packs are labelled `en`, so these rules would also run on English packs in a shared pipeline. They have not been tested on the English gold sets yet.
- Examples give the doc_id only, never the text.
- No rule uses full NFKC: it would turn x² into x2.
