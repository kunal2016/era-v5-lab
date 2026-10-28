# medicine_math: standard maths medicines

Status: DRAFT. Packs: math-finemath (gold 30 docs), math-megamath (gold 0 docs: NOT_EVALUATED). Run order = section order (the drop first, then fixes).
Rule form: `RULE_ID`, `CODE`, `ACTION`, `LANGS`, `ORIGIN`, `AUTHOR`; `medicine(doc) -> (action, text)`, `doc = {text, url, lang_label}`. Rows outside `LANGS` pass unchanged. Same form as `code-medicines/medicine_code.md` and `en-medicines/medicine_en.md`, so `tools/harm_test.py` of PR #4 runs it unchanged.
Origin: every rule is written by kunal2016 from a rule Owner1 gives **in words** in her math-finemath `medicine.md` (her code blocks are fragments, so none of them runs; her full code is in a `medicines.py` that is not in the repo). When her code is added, it goes in as an extra block and guideline 2 decides. IDs: the next free number after `rules/registry.json`, `medicine_code.md` and `medicine_en.md` (29 Oct); check before merging.
Each section follows the medicine template of `diagnosis/DISEASES.md`: the disease, the medicine in words and code, the action, the harm test and the side effects.

Each cell: gold harm % (gold docs changed or dropped / gold docs) and the result at 1%; `proxy` = Owner1's 101 clean rows of math-finemath (one reader, so not gold), shown because the gold set is small (one changed doc = 3.3%); labelled rows = fix or drop rows with the code in the two label sheets of the pack (Owner1 500 rows, Owner2 155 rows). Decision: guideline 2.

| # | ID | disease | action | finemath gold | proxy (101) | labelled rows fixed | megamath | decision |
|---|---|---|---|---|---|---|---|---|
| 1 | `DA-C3-006` | C3 truncated document | fix+drop | 0.00% (0/30) PASS | 0/101 | 15/50 | NOT_EVALUATED | KEEP |
| 2 | `DA-C1-007` | C1 boilerplate | fix | 0.00% (0/30) PASS | 0/101 | 47/328 | NOT_EVALUATED | KEEP |
| 3 | `DA-C2-005` | C2 repeated lines | fix | 0.00% (0/30) PASS | 0/101 | 39/187 | NOT_EVALUATED | KEEP |
| 4 | `DA-C5-003` | C5 keyword lists and SEO spam | fix | 0.00% (0/30) PASS | 0/101 | 5/51 | NOT_EVALUATED | KEEP |
| 5 | `DA-A1-004` | A1 invisible characters | fix | 0.00% (0/30) PASS | 0/101 | 14/15 | NOT_EVALUATED | KEEP |
| 6 | `DA-A3-003` | A3 mojibake | fix | 0.00% (0/30) PASS | 0/101 | 9/11 | NOT_EVALUATED | KEEP |
| 7 | `DA-A5-002` | A5 compatibility forms (ligatures, fullwidth) | fix | 0.00% (0/30) PASS | 0/101 | 6/6 | NOT_EVALUATED | KEEP |
| 8 | `DA-B2-003` | B2 HTML tags | fix | 0.00% (0/30) PASS | 0/101 | 3/8 | NOT_EVALUATED | KEEP |
| 9 | `DA-B4-010` | B4 template junk | fix | 0.00% (0/30) PASS | 0/101 | 9/18 | NOT_EVALUATED | KEEP |
| 10 | `DA-B5-002` | B5 broken LaTeX or Markdown | fix | 0.00% (0/30) PASS | 0/101 | 5/28 | NOT_EVALUATED | KEEP |
| 11 | `DA-F1-004` | F1 personal data | fix | 0.00% (0/30) PASS | 1/101 | 3/29 | NOT_EVALUATED | KEEP |

All 11 rules in sheet order: 0 of 30 gold documents changed or dropped (PASS); 1 of 101 proxy documents changed (0.99%, by `DA-F1-004`).

Not in this sheet:

| disease | why |
|---|---|
| C4 two documents joined | Owner1 tested a rule (cut a trailing block with no maths): it caught 0 labelled cases and changed 2 clean documents. Label, drop by verdict. |
| D4 machine-translated or spun text | no pattern: spun text is grammatical word by word ("sine regulation", "optimistic integers"); needs a language-model score. 22 rows, mostly `drop`. |
| D3 mixed-in foreign script | DISEASES.md: label it, do not judge it. Owner1's line-delete rule is not carried over. |
| A6 symbol-font glyphs | needs Owner1's 46-code Symbol-font table, which her sheet names but does not list. |
| F2 benchmark leak | no rule; open question whether olympiad problems (IMO) count as F2. They are not in `teams/09-evaluation/decontam/benchmarks.toml`. |

## 1. `DA-C3-006` · C3 truncated document · fix+drop · kunal2016 (from Owner1, medicine 4)

1. **Disease:** C3 truncated document. Labelled rows (fix or drop, both label sheets): 50. Examples where this rule acts on a labelled document: `1a679ab5f7dbd03a`, `1d5964cc6cb37bf9`.
2. **Medicine:** Drop a document that carries a preview or paywall banner. If a document ends in a teaser cut
(`word...` or `word…`), trim back to the last full sentence.

```python
RULE_ID = "DA-C3-006"
CODE = "C3"
ACTION = "fix+drop"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 4 (rule given in words)
import re

PREVIEW = re.compile(r"This preview shows|Sign up to view the full|View Full Document|"
                     r"intentionally blurred sections|This is the end of the preview")
TEASER = re.compile(r"\w(?:\.\.\.|…)$")

def cure_c3(text):
    if PREVIEW.search(text):
        return ("drop", "")
    t = text.rstrip()
    if TEASER.search(t):
        cut = max(t.rfind(". ", 0, len(t) - 3), t.rfind(".\n", 0, len(t) - 3))
        if cut > 0:
            return t[:cut + 1]
    return text

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_c3(doc["text"]), doc["text"])
```

3. **Action:** fix+drop.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-C3-006`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 15/50.
5. **Side effects:** a good document that quotes "View Full Document" is dropped. A document cut with no
marker cannot be detected.
6. **Decision (guideline 2):** KEEP (the only rule for C3 in this sheet, and it passes).

## 2. `DA-C1-007` · C1 boilerplate · fix · kunal2016 (from Owner1, medicine 1)

1. **Disease:** C1 boilerplate. Labelled rows (fix or drop, both label sheets): 328. Examples where this rule acts on a labelled document: `03711bb05408344e`, `147b24e3ffbd318c`.
2. **Medicine:** Delete a line that is a known chrome line, or a short line (at most 120 characters) containing a
site-chrome phrase seen in this pack (Course Hero, Bartleby, GMAT Club, OEIS, phpBB, YouTube
footer). Never touches a line longer than 120 characters.

```python
RULE_ID = "DA-C1-007"
CODE = "C1"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 1 (rule given in words)
import re

C1_LINE = re.compile(
    r"(?i)^\s*(?:"
    r"show tags|author message|kudos \[\?\].*|display posts from previous.*|"
    r"subscribe to view the full document\.?|view full document|tagged in|"
    r"see solution|want to see the full answer\??|want to see this answer and more\??|"
    r"comments are closed\.?|write a comment|share|sort by|filter by:.*|"
    r"this site is supported by donations to the oeis foundation\.?|"
    r"the oeis foundation is supported by donations.*|"
    r"hints \(greetings from the on-line encyclopedia of integer sequences!\)|"
    r"lookup \| welcome \| wiki \| register.*|contribute new seq\. or comment.*|"
    r"the oeis community \| maintained by the oeis foundation inc\.|"
    r"last modified .* contains \d+ sequences\. \(running on oeis\d\.\)"
    r")\s*$")
C1_SITE = re.compile(
    r"(?i)this preview shows page|sign up to view the full|this is the end of the preview|"
    r"check gmat club decision tracker|gmat club daily prep|powered by phpbb|"
    r"our solutions are written by experts|ask a homework question - tutors are online|"
    r"about press copyright contact us creators|this solution is locked")


def cure_c1(text):
    keep = [l for l in text.split("\n")
            if not (C1_LINE.match(l) or (C1_SITE.search(l) and len(l) <= 120))]
    return "\n".join(keep)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_c1(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-C1-007`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 47/328.
5. **Side effects:** fitted to sites seen in this pack, so other sites' chrome is missed. A real line
that is only "Share" or "Sort by" is removed. Owner1 reports 109 for her own code: her phrase list (~70 phrases) is not printed in her sheet, so this list holds only the sites seen while adjudicating.
6. **Decision (guideline 2):** KEEP (the only rule for C1 in this sheet, and it passes).

## 3. `DA-C2-005` · C2 repeated lines · fix · kunal2016 (from Owner1, medicine 2)

1. **Disease:** C2 repeated lines. Labelled rows (fix or drop, both label sheets): 187. Examples where this rule acts on a labelled document: `0591bb5d2f4f013c`, `0a2699cd84e3cb6f`.
2. **Medicine:** (a) A line of 15 or more characters that appears 5 or more times keeps only its first copy.
(b) A blank-line passage of 150 or more characters that appears again keeps only its first copy.
Lines inside code fences and list items are left alone.

```python
RULE_ID = "DA-C2-005"
CODE = "C2"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 2 (rule given in words)
FENCE_MARK = "`" * 3  # written this way so the sheet's own fences stay intact
import re
from collections import Counter

def cure_c2(text):
    lines = text.split("\n")
    fence = False
    countable = []
    for l in lines:
        if l.lstrip().startswith(FENCE_MARK):
            fence = not fence
        countable.append(not fence and len(l.strip()) >= 15)
    counts = Counter(l.strip() for l, c in zip(lines, countable) if c)
    seen, out = set(), []
    for l, c in zip(lines, countable):
        key = l.strip()
        if c and counts[key] >= 5:
            if key in seen:
                continue
            seen.add(key)
        out.append(l)
    blocks = re.split(r"(\n\s*\n)", "\n".join(out))
    seen_b, res = set(), []
    for b in blocks:
        k = b.strip()
        if len(k) >= 150 and not k.startswith(("-", "*", "•", FENCE_MARK)):
            if k in seen_b:
                continue
            seen_b.add(k)
        res.append(b)
    return "".join(res)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_c2(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-C2-005`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 39/187.
5. **Side effects:** an author who repeats a long passage on purpose loses the copy. Short repeated
titles are kept.
6. **Decision (guideline 2):** KEEP (the only rule for C2 in this sheet, and it passes).

## 4. `DA-C5-003` · C5 keyword lists and SEO spam · fix · kunal2016 (from Owner1, medicine 3)

1. **Disease:** C5 keyword lists and SEO spam. Labelled rows (fix or drop, both label sheets): 51. Examples where this rule acts on a labelled document: `25901665fc855b35`, `4bbc06d580844d70`.
2. **Medicine:** Delete lines starting `See more:` and lines made of 5 or more comma-separated Title-Case phrases.

```python
RULE_ID = "DA-C5-003"
CODE = "C5"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 3 (rule given in words)
import re

SEO = re.compile(r"(?m)^(?:See more: .*|(?:[A-Z][\w’'&.-]*(?: [\w’'&.-]+){1,7}, ){5,}.*)\n?")

def cure_c5(text):
    return SEO.sub("", text)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_c5(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-C5-003`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 5/51.
5. **Side effects:** most C5 in this pack is whole SEO pages, which only a drop verdict handles. A real
comma list of Title-Case names (a bibliography) would be deleted.
6. **Decision (guideline 2):** KEEP (the only rule for C5 in this sheet, and it passes).

## 5. `DA-A1-004` · A1 invisible characters · fix · kunal2016 (from Owner1, medicine 5)

1. **Disease:** A1 invisible characters. Labelled rows (fix or drop, both label sheets): 15. Examples where this rule acts on a labelled document: `00ac15aab828f732`, `064d8dd19536d1d8`.
2. **Medicine:** Delete U+200B, U+FEFF, U+00AD, U+200E, U+200F, U+2060, U+202A–U+202E, U+2066–U+2069. Never touch
ZWJ/ZWNJ (U+200D, U+200C). U+00A0 no-break space is not A1 and is kept.

```python
RULE_ID = "DA-A1-004"
CODE = "A1"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 5 (rule given in words)
import re

A1_RX = re.compile("[​﻿­‎‏⁠‪-‮⁦-⁩]")

def cure_a1(text):
    return A1_RX.sub("", text)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_a1(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-A1-004`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 14/15.
5. **Side effects:** a zero-width space used as the only word separator joins two words. LRM/RLM
matter in right-to-left text: do not run on RTL packs.
6. **Decision (guideline 2):** KEEP (the only rule for A1 in this sheet, and it passes).

## 6. `DA-A3-003` · A3 mojibake · fix · kunal2016 (from Owner1, medicine 8)

1. **Disease:** A3 mojibake. Labelled rows (fix or drop, both label sheets): 11. Examples where this rule acts on a labelled document: `4477acbfa8e1a6da`, `4aa20d6b132f1bae`.
2. **Medicine:** A short run starting with a UTF-8 lead byte read as cp1252 (`Â Ã â ð`) is re-encoded as cp1252
and decoded as UTF-8; the repair is kept only if it succeeds and is shorter.

```python
RULE_ID = "DA-A3-003"
CODE = "A3"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 8 (rule given in words)
import re

MOJI = re.compile("[ÂÃâð][\u0080-¿ŒœŠšŸ"
                  "Žžƒˆ˜–—‘-„†-•"
                  "…‰‹›€™]{1,3}")

def _fix(m):
    s = m.group(0)
    try:
        r = s.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s
    return r if len(r) < len(s) else s

def cure_a3(text):
    return MOJI.sub(_fix, text)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_a3(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-A3-003`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 9/11.
5. **Side effects:** real Latin-1 text that happens to decode as UTF-8 would be changed (rare).
6. **Decision (guideline 2):** KEEP (the only rule for A3 in this sheet, and it passes).

## 7. `DA-A5-002` · A5 compatibility forms (ligatures, fullwidth) · fix · kunal2016 (from Owner1, medicine 14)

1. **Disease:** A5 compatibility forms (ligatures, fullwidth). Labelled rows (fix or drop, both label sheets): 6. Examples where this rule acts on a labelled document: `2c59f0ca117f6bdf`, `6dbea1b7e4a63a28`.
2. **Medicine:** Replace ligatures U+FB00–U+FB06 by their NFKC letters; replace fullwidth ASCII U+FF01–U+FF5E by
ASCII only where CJK characters are under 1% of the letters. Never full NFKC (x² would become x2).

```python
RULE_ID = "DA-A5-002"
CODE = "A5"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 14 (rule given in words)
import re
import unicodedata

LIG = re.compile("[ﬀ-ﬆ]")
FULL = re.compile("[！-～]")
CJK = re.compile("[぀-ヿ㐀-鿿가-힯]")

def cure_a5(text):
    t = LIG.sub(lambda m: unicodedata.normalize("NFKC", m.group()), text)
    letters = sum(c.isalpha() for c in t) or 1
    if len(CJK.findall(t)) / letters < 0.01:
        t = FULL.sub(lambda m: chr(ord(m.group()) - 0xFEE0), t)
    return t

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_a5(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-A5-002`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 6/6.
5. **Side effects:** a typography page that quotes a ligature loses it.
6. **Decision (guideline 2):** KEEP (the only rule for A5 in this sheet, and it passes).

## 8. `DA-B2-003` · B2 HTML tags · fix · kunal2016 (from Owner1, medicine 9)

1. **Disease:** B2 HTML tags. Labelled rows (fix or drop, both label sheets): 8. Examples where this rule acts on a labelled document: `bf73e54bda1aabdb`, `c5b36a86af256f62`.
2. **Medicine:** `<br>` becomes a newline; simple formatting tags are removed. Documents with a code fence or
`<script>` are skipped.

```python
RULE_ID = "DA-B2-003"
CODE = "B2"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 9 (rule given in words)
FENCE_MARK = "`" * 3  # written this way so the sheet's own fences stay intact
import re

BR = re.compile(r"(?i)<br\s*/?>")
TAGS = re.compile(r"(?i)</?(?:p|div|span|a|ul|ol|li|sup|sub|strong|em|font|b|i|center)(?:\s[^<>]*)?>")

def cure_b2(text):
    if FENCE_MARK in text or "<script" in text.lower():
        return text
    return TAGS.sub("", BR.sub("\n", text))

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_b2(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-B2-003`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 3/8.
5. **Side effects:** `x<sup>2</sup>` becomes `x2`.
6. **Decision (guideline 2):** KEEP (the only rule for B2 in this sheet, and it passes).

## 9. `DA-B4-010` · B4 template junk · fix · kunal2016 (from Owner1, medicine 6)

1. **Disease:** B4 template junk. Labelled rows (fix or drop, both label sheets): 18. Examples where this rule acts on a labelled document: `2b2d4b3ed0f044d5`, `2c59f0ca117f6bdf`.
2. **Medicine:** Delete `{[ name ]}`, `{{ name | filter }}` with spaces inside (so LaTeX `{{x}}` is not hit),
`{% … %}`, `[TheoryMissing]`, `document.write(…)`.

```python
RULE_ID = "DA-B4-010"
CODE = "B4"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 6 (rule given in words)
import re

B4_RX = re.compile(r"\{\[\s*\w+\s*\]\}|\{\{\s+['\w][\w'.| :-]*\s+\}\}|\{%.*?%\}|"
                   r"\[TheoryMissing\]|document\.write\([^)]*\);?")

def cure_b4(text):
    return B4_RX.sub("", text)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_b4(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-B4-010`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 9/18.
5. **Side effects:** a tutorial teaching Angular or Jinja templates loses its examples.
6. **Decision (guideline 2):** KEEP (the only rule for B4 in this sheet, and it passes).

## 10. `DA-B5-002` · B5 broken LaTeX or Markdown · fix · kunal2016 (from Owner1, medicine 7)

1. **Disease:** B5 broken LaTeX or Markdown. Labelled rows (fix or drop, both label sheets): 28. Examples where this rule acts on a labelled document: `3a2ccc88dfcd67c9`, `951a4c150e019bd5`.
2. **Medicine:** Exactly `$$$` becomes `$$` (`$$$$` is two display blocks and stays); forum BBCode `[itex]`,
`[/itex]`, `[tex]`, `[/tex]`, `[math]`, `[/math]` becomes `$`; an odd number of ``` fences gets a
closing fence at the end.

```python
RULE_ID = "DA-B5-002"
CODE = "B5"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 7 (rule given in words)
FENCE_MARK = "`" * 3  # written this way so the sheet's own fences stay intact
import re

TRIPLE = re.compile(r"(?<!\$)\$\$\$(?!\$)")
BBCODE = re.compile(r"\[/?(?:itex|tex|math)\]")
FENCE = re.compile(re.escape(FENCE_MARK))  # count every fence mark: a fence can close mid-line

def cure_b5(text):
    t = TRIPLE.sub("$$", text)
    t = BBCODE.sub("$", t)
    if len(FENCE.findall(t)) % 2:
        t = t.rstrip("\n") + "\n" + FENCE_MARK + "\n"
    return t

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_b5(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-B5-002`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 0/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 5/28.
5. **Side effects:** a literal `[math]` in prose becomes `$`. LaTeX with stripped backslashes cannot be
repaired by rule.
6. **Decision (guideline 2):** KEEP (the only rule for B5 in this sheet, and it passes).

## 11. `DA-F1-004` · F1 personal data · fix · kunal2016 (from Owner1, medicine 15)

1. **Disease:** F1 personal data. Labelled rows (fix or drop, both label sheets): 29. Examples where this rule acts on a labelled document: `02c235b035b38798`, `9c827096ebb5ff42`.
2. **Medicine:** Real-looking emails become `user@example.com`; NNN-NNN-NNNN phone numbers become `[phone removed]`
when no other digit is within 3 characters. Cloudflare's `[email protected]` placeholder holds no
address and is left alone.

```python
RULE_ID = "DA-F1-004"
CODE = "F1"
ACTION = "fix"
LANGS = {"en"}
ORIGIN = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"  # written from Owner1's medicine.md, medicine 15 (rule given in words)
import re

EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])")
SAFE = re.compile(r"(?i)@(?:[\w-]+\.)*example\.(?:com|org|net)$|^(?:no-?reply|info|support|admin)@")
PHONE = re.compile(r"\b\d{3}-\d{3}-\d{4}\b")

def _phone(m):
    s, e, t = m.start(), m.end(), m.string
    near = t[max(0, s - 3):s] + t[e:e + 3]
    return m.group(0) if any(c.isdigit() for c in near) else "[phone removed]"

def cure_f1(text):
    t = EMAIL.sub(lambda m: m.group(0) if SAFE.search(m.group(0)) else "user@example.com", text)
    return PHONE.sub(_phone, t)

def _std(out, text):
    # result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        action, new = out
        if action == "drop": return ("drop", text)
        out = new
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    return _std(cure_f1(doc["text"]), doc["text"])
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_math.md --rule DA-F1-004`): math-finemath gold 0 changed, 0 dropped of 30, 0.00% PASS; proxy 1/101; math-megamath NOT_EVALUATED (gold empty). Labelled rows it fixes: 3/29.
5. **Side effects:** forum usernames and "full name + town" bylines are not caught (needs a team ruling).
Business numbers in the NNN-NNN-NNNN format are masked too. The proxy change is a university page with a staff email and phone; under ruling 6 (business contacts are not F1) that is harm. Team decision needed.
6. **Decision (guideline 2):** KEEP (the only rule for F1 in this sheet, and it passes).
