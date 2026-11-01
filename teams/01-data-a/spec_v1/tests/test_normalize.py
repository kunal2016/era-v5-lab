"""Tests for spec_v1/normalize.py, the matching normalize that Team 1 shares with G9. Every text is made up."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clean as c
import normalize as n

KA, VIRAMA, SSA, ZWNJ, ZWJ = "\u0915", "\u094d", "\u0937", "\u200c", "\u200d"


def test_g9_examples_still_hold():  # the cases in G9's own tests, so the file can replace theirs
    assert n.normalize("Janet\u2019s DUCKS, lay 16-eggs!") == ["janet", "s", "ducks", "lay", "16", "eggs"]
    assert n.normalize("\uff21\uff22\uff23 \u00bd") == ["abc", "1", "2"]
    assert n.normalize("\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0 \u0aad\u0abe\u0ab7\u0abe") == ["\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0", "\u0aad\u0abe\u0ab7\u0abe"]
    assert n.normalize("\u0939\u093f\u0928\u094d\u0926\u0940 \u092d\u093e\u0937\u093e") == ["\u0939\u093f\u0928\u094d\u0926\u0940", "\u092d\u093e\u0937\u093e"]


def test_offsets_point_into_original_text():
    text = "Hello,   wide World"
    for w, off in n.words_with_offsets(text):
        assert text[off:off + len(w)].lower() == w


@pytest.mark.parametrize("dirty, word", [
    ("com\u200bpute", "compute"),       # zero-width space (A1) does not split the word
    ("co\u00adoperate", "cooperate"),   # soft hyphen (A1)
    ("\ufeffimport", "import"),         # byte-order mark (A1)
    ("ab\u202ecd", "abcd"),             # bidi mark (A1)
    ("\ufb01rst", "first"),             # fi ligature (A5 compatibility form)
    ("\uff26\uff4f\uff4f", "foo"),      # fullwidth letters
    ("Stra\u00dfe", "strasse"),         # casefold
    ("cafe\u0301", "caf\u00e9"),        # NFC composes
])
def test_a1_characters_and_listed_compatibility_forms_match_the_plain_word(dirty, word):
    assert n.normalize(dirty) == [word]


def test_zwnj_and_zwj_are_kept_in_indic_words():  # DISEASES.md A1 and G2
    with_zwnj = KA + VIRAMA + ZWNJ + SSA
    with_zwj = KA + VIRAMA + ZWJ + SSA
    plain = KA + VIRAMA + SSA
    assert n.normalize(with_zwnj) == [with_zwnj]
    assert n.normalize(with_zwj) == [with_zwj]
    assert len({n.normalize(w)[0] for w in (with_zwnj, with_zwj, plain)}) == 3  # three different words stay different


@pytest.mark.parametrize("a, b", [
    ("\u095b", "\u091c\u093c"),                  # Hindi nukta: precomposed and base + nukta (NFC)
    ("\u0995\u09cb", "\u0995\u09c7\u09be"),      # Bengali two-part vowel sign
    ("\u0b95\u0bca", "\u0b95\u0bc6\u0bbe"),      # Tamil two-part vowel sign
    ("\u0d15\u0d47\u0d30\u0d33\u0d02", "\u0d15\u0d47\u0d30\u0d33\u0d02"),
    ("\u0d7a", "\u0d23\u0d4d\u200d"),             # Malayalam chillu: atomic and ZWJ spelling
    ("\u0d05\u0d35\u0d7b", "\u0d05\u0d35\u0d28\u0d4d\u200d"),
    ("\u09ce", "\u09a4\u09cd\u200d"),             # Bengali khanda ta: atomic and ZWJ spelling
    ("\u0939\u093f\u0928\u094d\u0926\u0940", "\u0939\u093f\u0928\u200b\u094d\u0926\u0940"),   # zero-width space inside a Hindi word
    ("\u0644\u0627", "\ufefb"),                  # Arabic presentation form
])
def test_indic_spellings_of_the_same_word_match(a, b):
    assert n.normalize(a) == n.normalize(b) and len(n.normalize(a)) == 1


def test_indic_digits_and_danda():
    assert n.normalize("\u0967\u0968") != n.normalize("12")               # Indic digits stay Indic (G4)
    assert n.normalize("\u092d\u093e\u0937\u093e\u0964 \u0905") == ["\u092d\u093e\u0937\u093e", "\u0905"]   # danda separates


def test_a_lone_joiner_is_not_a_word():
    assert n.normalize("a " + ZWNJ + " b") == ["a", "b"]


def test_nukta_written_two_ways_matches():  # DISEASES.md A5: NFC
    assert n.normalize("\u0958") == n.normalize(KA + "\u093c")


@pytest.mark.parametrize("text, words", [
    ("x\u00b2 + y\u00b2", ["x\u00b2", "y\u00b2"]),          # superscripts stay (no full NFKC, G4)
    ("\u0967\u0968\u0969 \u0e51\u0e52", ["\u0967\u0968\u0969", "\u0e51\u0e52"]),   # Indic and Thai digits stay
    ("\u2460 \u33a1", ["\u2460"]),               # circled digit stays itself (not 1); the m-squared sign is a symbol
])
def test_no_full_nfkc(text, words):
    assert n.normalize(text) == words


@pytest.mark.parametrize("text", ["", "   ", "!!! --- ???", "\u200b\u200b"])
def test_no_words(text):
    assert n.normalize(text) == []


@pytest.mark.parametrize("text", ["Janet\u2019s DUCKS, lay 16-eggs!", "x\u00b2 + \u00bd = \u2153",
                                  "com\u200bpute the \ufb01rst Stra\u00dfe", KA + VIRAMA + ZWNJ + SSA + " \u0130stanbul"])
def test_normalize_is_stable(text):
    once = n.normalize(text)
    assert n.normalize(" ".join(once)) == once


def test_clean_character_fixes_do_not_change_the_words():
    """A doc that clean.py repairs for invisible characters or ligatures gives the same words before and after."""
    doc = {"doc_id": "x", "url": "http://a/b", "lang_label": "en", "pack_id": "math-finemath",
           "text": "Area\u200b of a circle: the \ufb01rst result is pi r squared.\n" * 3}
    action, text = c.clean(doc)
    assert action == "fix" and text != doc["text"]
    assert n.normalize(text) == n.normalize(doc["text"])


def test_id_and_description():
    assert n.NORMALIZE_ID == "g1-spec-v1" and "NFC" in n.DESCRIPTION and "ZWJ/ZWNJ (kept)" in n.DESCRIPTION
