# medicine_math: math medicines

Packs: finemath 30, megamath 18 gold docs (Data A gold, `teams/01-data-a/gold/`). Each pack is tested on its own gold set.
Rule form: as `medicine_code.md`. `doc = {doc_id, text, url, lang_label, pack_id}`. Both math packs carry the `en` tag, so each rule also checks `pack_id` against `ORIGIN`; a doc with no `pack_id` passes unchanged.
Run order is section order, by stage: 10 characters, 20 markup, 30 source (drops, then strips). F1 is the one shared rule in `../tools/f1_rule.py`, not in this sheet.
Sources: the finemath rules are SomaKorada07's medicines (#61), whose sheet describes them in words and fragments with no functions; kunal2016 wrote each as code, kept as close to her description as possible. `DA-C5-001` is kunal2016's megamath medicine (#151).
IDs are unique inside this sheet; `clean.py` adds the family.
Tested with `harm_test.py` from `g1-harm-test`. Limit: changed + dropped at most `max(1, floor(1% of gold))`. Why each rule was picked, for each disease: `decisions_math.md`.

Each cell: gold harm % (gold docs changed or dropped / gold docs), the result at the limit, and the labelled rows the rule treats / the labelled rows with its code. `off` = not in `ORIGIN`.

| # | ID | disease | action | stage | source | finemath | megamath |
|---|---|---|---|---|---|---|---|
| 1 | `DA-A3-001` | A3 mojibake | fix | 10 | math-finemath | 0.00% (0/30) PASS · 9/11 | 0.00% (0/18) PASS · 8/21 |
| 2 | `DA-A1-001` | A1 invisible junk characters | fix | 10 | math-finemath | 0.00% (0/30) PASS · 14/15 | off |
| 3 | `DA-A5-001` | A5 compatibility forms | fix | 10 | math-finemath | 0.00% (0/30) PASS · 6/6 | 0.00% (0/18) PASS · 9/12 |
| 4 | `DA-B2-001` | B2 HTML tags | fix | 20 | math-finemath | 0.00% (0/30) PASS · 3/8 | 0.00% (0/18) PASS · 6/112 |
| 5 | `DA-B4-001` | B4 template junk | fix | 20 | math-finemath | 0.00% (0/30) PASS · 9/18 | 0.00% (0/18) PASS · 1/10 |
| 6 | `DA-B5-001` | B5 broken LaTeX or markdown | fix | 20 | math-finemath | 0.00% (0/30) PASS · 5/28 | 0.00% (0/18) PASS · 1/192 |
| 7 | `DA-C5-001` | C5 SEO / link lists | drop | 30 | math-megamath | off | 0.00% (0/18) PASS · 10/168 |
| 8 | `DA-C3-001` | C3 truncated document | drop | 30 | math-finemath | 0.00% (0/30) PASS · 10/50 | off |
| 9 | `DA-C1-001` | C1 boilerplate | fix | 30 | math-finemath | 0.00% (0/30) PASS · 47/328 | 0.00% (0/18) PASS · 3/336 |
| 10 | `DA-C2-001` | C2 repeated lines or passages | fix | 30 | math-finemath | 0.00% (0/30) PASS · 39/187 | off |
| 11 | `DA-C5-002` | C5 SEO / link lists | fix | 30 | math-finemath | 0.00% (0/30) PASS · 5/51 | 0.00% (0/18) PASS · 2/168 |
| 12 | `DA-C3-002` | C3 truncated document | fix | 30 | math-finemath | 0.00% (0/30) PASS · 5/50 | off |

## 1. `DA-A3-001` · A3 mojibake · fix · stage 10

1. **Disease:** A3 mojibake. Labelled rows: finemath 11, megamath 21.
2. **Medicine:** A short run starting with a UTF-8 lead byte read as cp1252 (`Â Ã â ð`) is re-encoded as cp1252 and decoded as UTF-8; the repair is kept only if it succeeds and is shorter.

```python
RULE_ID = "DA-A3-001"
CODE = "A3"
ACTION = "fix"
STAGE = "10"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

MOJI = re.compile("[\u00c2\u00c3\u00e2\u00f0][\u0080-\u00bf\u0152\u0153\u0160\u0161\u0178"
                  "\u017d\u017e\u0192\u02c6\u02dc\u2013\u2014\u2018-\u201e\u2020-\u2022"
                  "\u2026\u2030\u2039\u203a\u20ac\u2122]{1,3}")

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
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_a3(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** real Latin-1 text that happens to decode as UTF-8 would be changed (rare).
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 2. `DA-A1-001` · A1 invisible junk characters · fix · stage 10

1. **Disease:** A1 invisible junk characters. Labelled rows: finemath 15, megamath 0.
2. **Medicine:** Delete U+200B, U+FEFF, U+00AD, U+200E, U+200F, U+2060, U+202A–U+202E, U+2066–U+2069. Never touch ZWJ/ZWNJ (U+200D, U+200C). U+00A0 no-break space is not A1 and is kept.

```python
RULE_ID = "DA-A1-001"
CODE = "A1"
ACTION = "fix"
STAGE = "10"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

A1_RX = re.compile("[\u200b\ufeff\u00ad\u200e\u200f\u2060\u202a-\u202e\u2066-\u2069]")

def cure_a1(text):
    return A1_RX.sub("", text)


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_a1(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath.
4. **Harm test:** finemath 0.00% (0/30) PASS.
5. **Side effects:** a zero-width space used as the only word separator joins two words. LRM/RLM matter in right-to-left text: do not run on RTL packs.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 3. `DA-A5-001` · A5 compatibility forms · fix · stage 10

1. **Disease:** A5 compatibility forms. Labelled rows: finemath 6, megamath 12.
2. **Medicine:** Replace ligatures U+FB00–U+FB06 by their NFKC letters; replace fullwidth ASCII U+FF01–U+FF5E by ASCII only where CJK characters are under 1% of the letters. Never full NFKC (x² would become x2).

```python
RULE_ID = "DA-A5-001"
CODE = "A5"
ACTION = "fix"
STAGE = "10"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re
import unicodedata

LIG = re.compile("[\ufb00-\ufb06]")
FULL = re.compile("[\uff01-\uff5e]")
CJK = re.compile("[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]")

def cure_a5(text):
    t = LIG.sub(lambda m: unicodedata.normalize("NFKC", m.group()), text)
    letters = sum(c.isalpha() for c in t) or 1
    if len(CJK.findall(t)) / letters < 0.01:
        t = FULL.sub(lambda m: chr(ord(m.group()) - 0xFEE0), t)
    return t


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_a5(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** a typography page that quotes a ligature loses it.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 4. `DA-B2-001` · B2 HTML tags · fix · stage 20

1. **Disease:** B2 HTML tags. Labelled rows: finemath 8, megamath 112.
2. **Medicine:** `<br>` becomes a newline; simple formatting tags are removed. Documents with a code fence or `<script>` are skipped.

```python
RULE_ID = "DA-B2-001"
CODE = "B2"
ACTION = "fix"
STAGE = "20"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

BR = re.compile(r"(?i)<br\s*/?>")
TAGS = re.compile(r"(?i)</?(?:p|div|span|a|ul|ol|li|sup|sub|strong|em|font|b|i|center)(?:\s[^<>]*)?>")

def cure_b2(text):
    if "```" in text or "<script" in text.lower():
        return text
    return TAGS.sub("", BR.sub("\n", text))


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_b2(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** `x<sup>2</sup>` becomes `x2`.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 5. `DA-B4-001` · B4 template junk · fix · stage 20

1. **Disease:** B4 template junk. Labelled rows: finemath 18, megamath 10.
2. **Medicine:** Delete `{[ name ]}`, `{{ name | filter }}` with spaces inside (so LaTeX `{{x}}` is not hit), `{% … %}`, `[TheoryMissing]`, `document.write(…)`.

```python
RULE_ID = "DA-B4-001"
CODE = "B4"
ACTION = "fix"
STAGE = "20"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

B4_RX = re.compile(r"\{\[\s*\w+\s*\]\}|\{\{\s+['\w][\w'.| :-]*\s+\}\}|\{%.*?%\}|"
                   r"\[TheoryMissing\]|document\.write\([^)]*\);?")

def cure_b4(text):
    return B4_RX.sub("", text)


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_b4(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** a tutorial teaching Angular or Jinja templates loses its examples.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 6. `DA-B5-001` · B5 broken LaTeX or markdown · fix · stage 20

1. **Disease:** B5 broken LaTeX or markdown. Labelled rows: finemath 28, megamath 192.
2. **Medicine:** Exactly `$$$` becomes `$$` (`$$$$` is two display blocks and stays); forum BBCode `[itex]`, `[/itex]`, `[tex]`, `[/tex]`, `[math]`, `[/math]` becomes `$`; an odd number of ``` fences gets a closing fence at the end.

```python
RULE_ID = "DA-B5-001"
CODE = "B5"
ACTION = "fix"
STAGE = "20"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

TRIPLE = re.compile(r"(?<!\$)\$\$\$(?!\$)")
BBCODE = re.compile(r"\[/?(?:itex|tex|math)\]")
FENCE = re.compile(r"```")  # count every fence mark: a fence can close mid-line

def cure_b5(text):
    t = TRIPLE.sub("$$", text)
    t = BBCODE.sub("$", t)
    if len(FENCE.findall(t)) % 2:
        t = t.rstrip("\n") + "\n```\n"
    return t


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_b5(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** a literal `[math]` in prose becomes `$`. LaTeX with stripped backslashes cannot be repaired by rule.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 7. `DA-C5-001` · C5 SEO / link lists · drop · stage 30

1. **Disease:** C5 SEO / link lists. Labelled rows: finemath 51, megamath 168.
2. **Medicine:** **Seen:** 4 of 100 in rows 401-500 (450, 480, 483, 499; asraj labels the same 4 drop), 10 of 500 in the pack. Every one has the same layout: "Study guides", the question, "Write your answer... / Submit", then a list of snippets from other questions. The page's own question is never answered. Drop the document when it starts with exactly that header. Nothing else in the pack starts this way.

```python
RULE_ID = "DA-C5-001"
CODE = "C5"
ACTION = "drop"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-megamath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

ANSWERS = re.compile(r"\AStudy guides\s*\n\s*Q: .{1,300}\n\s*Write your answer\.\.\.\s*\n\s*Submit\s*\n\s*Related questions\s*\n")

def cure_c5(text):
    if ANSWERS.match(text):
        return ("drop", "")
    return text


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_c5(doc["text"]), doc["text"])
```

3. **Action:** drop. **Runs on:** megamath.
4. **Harm test:** megamath 0.00% (0/18) PASS.
5. **Side effects:** an answers.com page that does carry an answer below "Related questions" is also dropped (none seen in this pack). Matching is anchored at the start of the text, so a quotation of the header inside another document is not touched.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: kunal2016, megamath sheet, PR 151. Idempotent on every doc of its packs.

## 8. `DA-C3-001` · C3 truncated document · drop · stage 30

1. **Disease:** C3 truncated document. Labelled rows: finemath 50, megamath 74.
2. **Medicine:** Drop a document that carries a preview or paywall banner. If a document ends in a teaser cut (`word...` or `word…`), trim back to the last full sentence.

```python
RULE_ID = "DA-C3-001"
CODE = "C3"
ACTION = "drop"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

PREVIEW = re.compile(r"This preview shows|Sign up to view the full|View Full Document|"
                     r"intentionally blurred sections|This is the end of the preview")
TEASER = re.compile(r"\w(?:\.\.\.|\u2026)$")

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
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    out = cure_c3(doc["text"])
    return ("drop", doc["text"]) if isinstance(out, tuple) else ("keep", doc["text"])
```

3. **Action:** drop. **Runs on:** finemath.
4. **Harm test:** finemath 0.00% (0/30) PASS.
5. **Side effects:** a good document that quotes "View Full Document" is dropped. A document cut with no marker cannot be detected.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 9. `DA-C1-001` · C1 boilerplate · fix · stage 30

1. **Disease:** C1 boilerplate. Labelled rows: finemath 328, megamath 336.
2. **Medicine:** Delete a line that is a known chrome line, or a short line (at most 120 characters) containing a site-chrome phrase seen in this pack (Course Hero, Bartleby, GMAT Club, OEIS, phpBB, YouTube footer). Never touches a line longer than 120 characters.

```python
RULE_ID = "DA-C1-001"
CODE = "C1"
ACTION = "fix"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
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
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_c1(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** fitted to sites seen in this pack, so other sites' chrome is missed. A real line that is only "Share" or "Sort by" is removed.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 10. `DA-C2-001` · C2 repeated lines or passages · fix · stage 30

1. **Disease:** C2 repeated lines or passages. Labelled rows: finemath 187, megamath 131.
2. **Medicine:** (a) A line of 15 or more characters that appears 5 or more times keeps only its first copy. (b) A blank-line passage of 150 or more characters that appears again keeps only its first copy. Lines inside code fences and list items are left alone.

```python
RULE_ID = "DA-C2-001"
CODE = "C2"
ACTION = "fix"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re
from collections import Counter

def cure_c2(text):
    lines = text.split("\n")
    fence = False
    countable = []
    for l in lines:
        if l.lstrip().startswith("```"):
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
        if len(k) >= 150 and not k.startswith(("-", "*", "\u2022", "```")):
            if k in seen_b:
                continue
            seen_b.add(k)
        res.append(b)
    return "".join(res)


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_c2(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath.
4. **Harm test:** finemath 0.00% (0/30) PASS.
5. **Side effects:** an author who repeats a long passage on purpose loses the copy. Short repeated titles are kept.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 11. `DA-C5-002` · C5 SEO / link lists · fix · stage 30

1. **Disease:** C5 SEO / link lists. Labelled rows: finemath 51, megamath 168.
2. **Medicine:** Delete lines starting `See more:` and lines made of 5 or more comma-separated Title-Case phrases.

```python
RULE_ID = "DA-C5-002"
CODE = "C5"
ACTION = "fix"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath, math-megamath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

SEO = re.compile(r"(?m)^(?:See more: .*|(?:[A-Z][\w\u2019'&.-]*(?: [\w\u2019'&.-]+){1,7}, ){5,}.*)\n?")

def cure_c5(text):
    return SEO.sub("", text)


def _std(out, text):
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    return _std(cure_c5(doc["text"]), doc["text"])
```

3. **Action:** fix. **Runs on:** finemath, megamath.
4. **Harm test:** finemath 0.00% (0/30) PASS; megamath 0.00% (0/18) PASS.
5. **Side effects:** most C5 in this pack is whole SEO pages, which only a drop verdict handles. A real comma list of Title-Case names (a bibliography) would be deleted.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.

## 12. `DA-C3-002` · C3 truncated document · fix · stage 30

1. **Disease:** C3 truncated document. Labelled rows: finemath 50, megamath 74.
2. **Medicine:** Drop a document that carries a preview or paywall banner. If a document ends in a teaser cut (`word...` or `word…`), trim back to the last full sentence.

```python
RULE_ID = "DA-C3-002"
CODE = "C3"
ACTION = "fix"
STAGE = "30"
STATUS = "CANDIDATE"
LANGS = {'en'}
ORIGIN = "math-finemath"  # packs it runs on
PACKS = set(ORIGIN.split(", "))  # the math packs share the "en" tag, so the pack is checked too
SOURCE = "math-finemath"  # pack whose medicine this came from
AUTHOR = "kunal2016"
import re

PREVIEW = re.compile(r"This preview shows|Sign up to view the full|View Full Document|"
                     r"intentionally blurred sections|This is the end of the preview")
TEASER = re.compile(r"\w(?:\.\.\.|\u2026)$")

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
    # the result in the shared form: str -> fix/keep, ("drop", ...) -> drop
    if isinstance(out, tuple) and out and out[0] == "drop": return ("drop", text)
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS or doc.get("pack_id") not in PACKS:
        return ("keep", doc["text"])
    out = cure_c3(doc["text"])
    return ("keep", doc["text"]) if isinstance(out, tuple) else _std(out, doc["text"])
```

3. **Action:** fix. **Runs on:** finemath.
4. **Harm test:** finemath 0.00% (0/30) PASS.
5. **Side effects:** a good document that quotes "View Full Document" is dropped. A document cut with no marker cannot be detected.
6. **Spec v1:** status CANDIDATE, reviewer pending. Source: SomaKorada07's finemath sheet, PR 61 (written as code by kunal2016). Idempotent on every doc of its packs.
