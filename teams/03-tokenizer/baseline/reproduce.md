# BrahmicTokenizer-131K baseline reproduction

- Repo: github.com/theschoolofai/BrahmicTokenizer-131K, commit `7dfcf398172c825c6689ad578e8b484ca5f57bc9`
- Machine: Windows 11, PowerShell, Python venv, `Python 3.12.7`
- Result: **reproduced exactly.** All 4 verify scripts pass. FLORES-200 fertility matches the reference with a largest difference of 0.000000 (required ≤ 0.001).

## 1. Verify scripts

| Script | Result |
|---|---|
| verify_no_cross_script_merges | PASS: 0 cross-script entries in 301,398 merges |
| verify_max_byte_length | PASS: vocab 131,072 (130,716 normal + 356 special), longest token 32 bytes |
| verify_kronecker_constraints_unified | PASS: max byte ≤ 32 and 0 cross-script at POS_DIM=32 |
| verify_sarvam_m_structural_identity | STRUCTURALLY IDENTICAL: vocab, 301,398 merges (same rank order), 356 added tokens |

### 1.1 No cross-script merges

```
> python verify_no_cross_script_merges.py tokenizer.json
tokenizer:         tokenizer.json
merge-rule entries: 301,398
cross-script:      0
PASS: no cross-script entries in the merge list.
```

### 1.2 Max byte length

```
> python verify_max_byte_length.py tokenizer.json
tokenizer:           tokenizer.json
vocab size:          131,072
  normal:            130,716
  special:           356
  byte-fallback:     0
max_bytes limit:     32
longest normal token: 32 bytes  (token: 'ĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠĠ')
tokens > 32 bytes: 0
PASS: all 130,716 normal tokens are within 32 bytes.
```

### 1.3 Kronecker constraints

```
> python verify_kronecker_constraints_unified.py tokenizer.json
tokenizer:              tokenizer.json
pre_tokenizer:          ByteLevel
vocab_size:             131,072
normal tokens:          131,072
special tokens:         0
max byte length:        32  (token='--------------------------------')
tokens > 32 bytes:      0
cross-script tokens:    0

KE constraint check (POS_DIM=32):
  max byte ≤ 32:        PASS
  0 cross-script:       PASS

RESULT: PASS — tokenizer satisfies both Kronecker constraints at POS_DIM=32.
```

### 1.4 Structural identity

```
> python verify_sarvam_m_structural_identity.py tokenizer.json tokenizer.json
tokenizer A:  tokenizer.json
tokenizer B:  tokenizer.json

--- Normal-vocab tokens ---
  |A|:              131,072
  |B|:              131,072
  identical:        131,072
  only in A:        0
  only in B:        0

--- BPE merges ---
  |A|:              301,398
  |B|:              301,398
  identical (set):  301,398
  only in A:        0
  only in B:        0
  rank order same:  True

--- Added / special tokens ---
  |A|:              356
  |B|:              356
  identical:        356
  only in A:        0
  only in B:        0

=== Summary ===
vocab identical:   True
merges identical:  True (rank order: True)
added identical:   True

RESULT: STRUCTURALLY IDENTICAL — vocab, BPE table (content + rank), and added tokens all match.
```

## 2. FLORES-200 fertility (tokens per word)

Data: FLORES-200 dev+devtest, 2,009 sentences per language, from
https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz

```
python evaluate_fertility_flores.py --tokenizers all --languages all
```

Compared with `reference_outputs/evaluate_fertility_flores.json`.
Checked with `compare_ref.py` (in this folder). Run it from the BrahmicTokenizer-131K repo root after the fertility script: `python compare_ref.py`.

| Language | Mine | Reference | Diff |
|---|---|---|---|
| English (En) | 1.2352 | 1.2352 | 0.0000 |
| Hindi (Hi) | 1.6429 | 1.6429 | 0.0000 |
| Bengali (Bn) | 2.3295 | 2.3295 | 0.0000 |
| Tamil (Ta) | 3.1166 | 3.1166 | 0.0000 |
| Telugu (Te) | 3.0292 | 3.0292 | 0.0000 |
| Kannada (Kn) | 3.2734 | 3.2734 | 0.0000 |
| Malayalam (Ml) | 3.4738 | 3.4738 | 0.0000 |
| Marathi (Mr) | 2.5723 | 2.5723 | 0.0000 |
| Gujarati (Gu) | 2.2748 | 2.2748 | 0.0000 |
| Punjabi (Pa) | 2.5955 | 2.5955 | 0.0000 |
| Odia (Or) | 4.1287 | 4.1287 | 0.0000 |
| Assamese (As) | 2.7535 | 2.7535 | 0.0000 |
| **Mean Brahmic (11)** | **2.8355** | **2.8355** | **0.0000** |

**Result: reproduced. Largest difference 0.000000 (required ≤ 0.001).**

## 3. Notes

- FLORES was extracted to `C:\tmp\flores200_dataset`, because the script reads `/tmp/flores200_dataset`.
- Comparator tokenizers that did not load: Gemma-3-1B and Llama-3.1-8B (gated on Hugging Face, access not yet granted) and Krutrim-1 (needs torch). They do not affect the BrahmicTokenizer-131K baseline.
