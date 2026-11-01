"""Spec v1 normalize for matching (decontamination fingerprints, dedup). Team 1 (Data A) shares it with G9.

    from normalize import NORMALIZE_ID, DESCRIPTION, normalize, words_with_offsets
    normalize("Janet\u2019s DUCKS, lay 16-eggs!")  ->  ["janet", "s", "ducks", "lay", "16", "eggs"]

This is a comparison key, not the cleaning policy. It never changes or drops a document: it turns text into a list of
words, so that a benchmark item and a cleaned document compare equal when they hold the same words. The cleaning itself
is clean.py, which follows TSAI's DISEASES.md (A5: "We use NFC"). Same interface as G9's
teams/09-evaluation/decontam/normalize.py, so it can replace that file as it is.

It is the same function for every language and pack, on purpose: a benchmark item has no pack, and both sides of a
match must get exactly the same treatment. Language-specific repairs (A3 mojibake, B2 markup, and the rest) are done by
clean.py on the documents before matching.

For each word:
  1. A word is a run of Unicode letters (L*), marks (M*) and numbers (N*), plus ZWJ and ZWNJ. Marks keep Indic vowel
     signs inside the word. The A1 invisible characters of DISEASES.md (zero-width space U+200B, BOM U+FEFF, soft
     hyphen U+00AD, bidi marks U+202A-U+202E and U+2066-U+2069) do not split a word either.
  2. Those A1 characters are removed. ZWJ U+200D and ZWNJ U+200C are kept: in Indic text they are part of the script
     (DISEASES.md A1 and G2), so two words that differ only by one stay different.
  3. NFC (DISEASES.md A5). Never full NFKC (G4: over-normalised); only these compatibility characters are folded to
     their plain form: Latin ligatures U+FB00-U+FB06 ("fi"), fullwidth ASCII U+FF01-U+FF5E, vulgar fractions
     (U+00BC-U+00BE, U+2150-U+215F, U+2189) and Arabic presentation forms (U+FB50-U+FDFF, U+FE70-U+FEFF).
     Superscripts, Indic digits and all other characters are left as they are.
     The old ZWJ spellings of the Malayalam chillus (for example NNA + virama + ZWJ) and of Bengali khanda ta
     (TA + virama + ZWJ) become the atomic letters Unicode encodes for them (U+0D7A-U+0D7F, U+09CE), so the two
     spellings of the same letter match. Every other ZWJ and ZWNJ stays.
  4. casefold(), then NFC again. A fraction becomes "1/2", so the result is split again.
Everything else (spaces, punctuation, symbols, underscore, other format characters) separates words.
Changing any step changes NORMALIZE_ID; G9's decontam_check.py refuses a fingerprint set built with another ID.
"""
import re
import sys
import unicodedata

NORMALIZE_ID = "g1-spec-v1"
DESCRIPTION = ("words = runs of Unicode L/M/N characters plus ZWJ/ZWNJ (kept); DISEASES.md A1 invisible characters do "
               "not split and are removed; each word NFC, ZWJ chillu and khanda ta spellings to the atomic letters, "
               "Latin ligatures, fullwidth ASCII, vulgar fractions and Arabic presentation forms folded, then casefold(); "
               "everything else separates words")

A1_CHARS = "\u200b\ufeff\u00ad\u202a-\u202e\u2066-\u2069"   # DISEASES.md A1, removed
JOINERS = "\u200c\u200d"                                    # ZWNJ, ZWJ: part of Indic script (A1, G2), kept
_FOLD = re.compile("[\ufb00-\ufb06\uff01-\uff5e\u00bc-\u00be\u2150-\u215f\u2189\ufb50-\ufdff\ufe70-\ufeff]")   # the only compatibility folds
_ATOMIC = {"\u0d23\u0d4d\u200d": "\u0d7a", "\u0d28\u0d4d\u200d": "\u0d7b", "\u0d30\u0d4d\u200d": "\u0d7c",   # Malayalam chillus
           "\u0d32\u0d4d\u200d": "\u0d7d", "\u0d33\u0d4d\u200d": "\u0d7e", "\u0d15\u0d4d\u200d": "\u0d7f",
           "\u09a4\u09cd\u200d": "\u09ce"}                                                                # Bengali khanda ta
_ATOMIC_RE = re.compile("|".join(_ATOMIC))


def _mark_ranges():
    # Python \w does not match combining marks (Unicode M*), so Indic vowel signs would split words.
    ranges, start, prev = [], None, None
    for cp in range(sys.maxunicode + 1):
        if unicodedata.category(chr(cp))[0] == "M":
            if start is None:
                start = cp
            prev = cp
        elif start is not None:
            ranges.append((start, prev))
            start = None
    if start is not None:
        ranges.append((start, prev))
    return "".join(f"\\U{a:08x}-\\U{b:08x}" for a, b in ranges)


_M = _mark_ranges()
WORD_RE = re.compile(f"(?:[^\\W_]|[{_M}{JOINERS}])+")                  # a normalized word
_RAW_WORD_RE = re.compile(f"(?:[^\\W_]|[{_M}{JOINERS}{A1_CHARS}])+")   # in the original text, A1 characters join too
_A1_RE = re.compile(f"[{A1_CHARS}]+")
_ONLY_JOINERS = re.compile(f"[{JOINERS}]+")


def _key(token):
    t = unicodedata.normalize("NFC", _A1_RE.sub("", token))
    t = _ATOMIC_RE.sub(lambda m: _ATOMIC[m.group()], t)
    t = _FOLD.sub(lambda m: unicodedata.normalize("NFKC", m.group()), t)
    return unicodedata.normalize("NFC", t.casefold())


def words_with_offsets(text):
    """Return [(word, char_offset)] for text. Offsets point into the original text, at the start of the word."""
    out = []
    for m in _RAW_WORD_RE.finditer(text):
        for w in WORD_RE.findall(_key(m.group())):
            if not _ONLY_JOINERS.fullmatch(w):
                out.append((w, m.start()))
    return out


def normalize(text):
    """Text -> list of normalized words."""
    return [w for w, _ in words_with_offsets(text)]
