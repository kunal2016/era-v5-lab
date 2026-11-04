# Romanised Indic (D2): share and detector, v1

Issue #213, part 1. How much of each Indic language in the `ind-*` packs is written in Latin letters (D2 in
`diagnosis/DISEASES.md`, for example Hindi as "aap kaise ho"), measured with a small detector that was tested on
100 documents readers had already labelled. Part 2, the cap proposal, will be `romanised_policy_v1.md`.

## Result

`romanised_share_v1.csv`: share of documents the detector flags, per language, on the full packs (500 documents per pack).

| lang | packs | docs | flagged | share |
|---|---|---|---|---|
| hi | 5 | 2500 | 17 | 0.68% |
| sa | 1 | 500 | 4 | 0.80% |
| gu | 1 | 500 | 3 | 0.60% |
| bn | 2 | 1000 | 2 | 0.20% |
| ta | 3 | 1500 | 3 | 0.20% |
| te | 3 | 1500 | 2 | 0.13% |
| kn | 3 | 1500 | 1 | 0.07% |
| ml, mr, or | 1, 2, 1 | 500, 1000, 500 | 0 | 0% |
| all | 22 | 11000 | 32 | 0.29% |

Per pack (`romanised_share_by_pack_v1.csv`): ind-hi-fw2 1.4%, ind-hi-hplt 1.2%, every other pack 0.8% or less.

What this means:
- Romanised Indic is rare: about 3 documents in 1000 overall, and about 1 in 100 in the Hindi web packs (fw2, hplt).
- A flagged document is rarely romanised from start to end. Most are Devanagari (or other script) articles with
  romanised SEO headings ("Photo Se Background Kaise Hataye", "Aaj Ka Love Rashifal"), a reader comment, or a tweet.
  Longer romanised passages are in a Bengali tech forum thread, a Telugu story site, a Kannada phrasebook, a Tamil
  drug page, and Sanskrit verses in IAST (three ind-sa-fw2 pages and a Gita page in ind-gu-fw2).
- The detector finds 42% of the documents readers marked D2 (below). Most of the ones it misses have only one or
  two romanised words, so the share of documents with a real amount of romanised text is close to the numbers above.
- Counts per language are small (0 to 17 documents), so differences between languages below 1% are noise.

## The detector (`detector.py`)

1. Take the words in Latin letters, without URLs, emails, @handles, #hashtags and all-capital acronyms (ANI, AAP, EMI).
2. Count the ones on a short list of common romanised Indic words: hai, nahi, kaise, kya, aur, ke, ki, ko, se ... for
   Hindi, and a few for bn, mr, ta, te, kn, ml, gu. Words that are also English (in, to, me, is, na ...) are not on it.
3. Count the letters with IAST diacritics (ā ī ū ṛ ṃ ṇ ś ṣ ḥ ...), the usual romanisation of Sanskrit.
4. Flag the document when it has at least 3 list words, 2 of them different, or at least 5 IAST letters.

No model and no training data; `python3 detector.py "aap kaise ho, sab theek hai?"` shows what it matched.

## The test (`build_testset.py`, `eval_detector.py`, `eval_v1.md`)

`testset_100.csv`: all 52 documents that any reader marked D2 (76 D2 rows in 48 sheets of 22 packs, 37 of them in
ind-hi-hplt), plus 48 documents no reader marked D2: 24 drawn among documents with at least 10% Latin letters
(English text, names, URLs, so the detector meets hard cases) and 24 drawn from all others. Seed 0, and the draw does
not use the detector.

Ground truth is the readers' labels: a document is D2 when at least one reader marked it D2.

| D2 docs | flagged | true pos | false pos | missed | precision | recall |
|---|---|---|---|---|---|---|
| 52 | 22 | 22 | 0 | 30 | 100% | 42% |

- Missed (30): SEO titles or comments with one or two romanised words ("Vish Ke Dant", "Sariya Cement Ka Rate",
  "Nagar Palika Bharti", "Shiksha k Odisha kya hai"), short comments with words not on the list ("1 no pic madhe"),
  and documents whose D2 mark points at English text or a proper name (for example ind-mr-fw2 rows 146 and 231).
  Every miss is listed in `eval_v1.md`.
- False alarms: none.
- Thresholds: 2 words instead of 3 raises recall to 48% and flags 7 more documents on the full packs; 3 words was
  kept. The full table is in `eval_v1.md`.
- Precision on a test set that is half D2 is easier than on real packs, where D2 is rare (about 0.3%).

## Reproduce

```bash
cd teams/02-data-b/romanised
# packs/<pack_id>.parquet: the 22 ind-* sample packs; sheets/: readers' labels.csv
python3 ../tools/fetch_sheets.py --packs ind-hi-hplt ind-hi-fw2 ... --out sheets
uv run --with pyarrow python build_testset.py      # testset_100.csv
uv run --with pyarrow python eval_detector.py      # eval_v1.md
uv run --with pyarrow python share.py              # romanised_share_v1.csv, romanised_share_by_pack_v1.csv
```

`packs/` and `sheets/` are not committed (`.gitignore`): the packs are large and the sheets are other readers' files.
`fetch_sheets.py` refuses one sheet (PR #43, ind-mr-fw2/vpw): a note in it holds a stray terminal escape character,
and gh will not print it. That sheet was taken from the pull request's commit with git instead:
`git fetch https://github.com/theschoolofai/era-v5-lab.git pull/43/head` and
`git show FETCH_HEAD:diagnosis/submissions/ind-mr-fw2/vpw/labels.csv > sheets/ind-mr-fw2/vpw.csv`.
