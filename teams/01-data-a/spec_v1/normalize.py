"""Spec v1 text normalize, for matching only (decontamination fingerprints, dedup). Team 1 (Data A) shares it with G9.

    from normalize import NORMALIZE_ID, DESCRIPTION, normalize, words_with_offsets
    normalize("Janet’s DUCKS, lay 16-eggs!")  ->  ["janet", "s", "ducks", "lay", "16", "eggs"]

It never changes or drops a document: it only turns text into a list of words, so that a benchmark item and a cleaned
document compare equal when they hold the same words. Same interface as G9's teams/09-evaluation/decontam/normalize.py,
so it can replace that file as it is.

What it does, in order, for each word:
  1. A word is a run of Unicode letters (L*), marks (M*) and numbers (N*). Marks keep Indic vowel signs inside the word.
     Format characters (Cf: zero-width space, ZWJ, ZWNJ, soft hyphen, byte-order mark, bidi marks) do not split a word.
  2. Format characters are removed. This is spec v1 A1 (invisible characters), so a word that clean.py has repaired and
     the same word still carrying a zero-width space give the same result.
  3. NFKC, then casefold(). NFKC folds the compatibility forms of spec v1 A5 (ligatures such as "fi", fullwidth letters,
     superscripts) and composes accents; casefold() is lower() plus ss for sharp s and similar.
  4. NFKC can add separators ("1/2" from the fraction character), so the result is split again.
Everything else (spaces, punctuation, symbols, underscore) separates words.

Not done, on purpose: mojibake repair (A3) and markup removal (B2) belong to clean.py, which runs before matching;
no stemming, no stop words, no transliteration. Changing any step changes NORMALIZE_ID, and a fingerprint set built
with another ID is refused by G9's decontam_check.py.
"""
import re
import sys
import unicodedata

NORMALIZE_ID = "g1-spec-v1"
DESCRIPTION = ("words = runs of Unicode L/M/N characters (Cf format characters do not split and are removed); "
               "each word NFKC then casefold(); everything else separates words")


def _ranges(first_letters):
    """Character-class ranges of every code point whose Unicode category starts with one of first_letters."""
    out, start, prev = {c: [] for c in first_letters}, {}, {}
    for cp in range(sys.maxunicode + 1):
        cat = unicodedata.category(chr(cp))
        for c in first_letters:
            hit = cat == c if len(c) == 2 else cat[0] == c
            if hit:
                start.setdefault(c, cp)
                prev[c] = cp
            elif c in start:
                out[c].append((start.pop(c), prev[c]))
    for c in list(start):
        out[c].append((start[c], prev[c]))
    return {c: "".join(f"\\U{a:08x}-\\U{b:08x}" for a, b in rs) for c, rs in out.items()}


_R = _ranges(("M", "Cf"))
WORD_RE = re.compile(f"(?:[^\\W_]|[{_R['M']}])+")                         # a normalized word: L, M, N
_RAW_WORD_RE = re.compile(f"(?:[^\\W_]|[{_R['M']}]|[{_R['Cf']}])+")       # in the original text, Cf joins too
_CF_RE = re.compile(f"[{_R['Cf']}]+")


def words_with_offsets(text):
    """Return [(word, char_offset)] for text. Offsets point into the original text, at the start of the word."""
    out = []
    for m in _RAW_WORD_RE.finditer(text):
        tok = unicodedata.normalize("NFKC", _CF_RE.sub("", m.group())).casefold()
        for w in WORD_RE.findall(tok):
            out.append((w, m.start()))
    return out


def normalize(text):
    """Text -> list of normalized words."""
    return [w for w, _ in words_with_offsets(text)]
