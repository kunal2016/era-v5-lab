"""Tests for spec_v1/normalize.py, the matching normalize that Team 1 shares with G9. Every text is made up."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clean as c
import normalize as n


def test_g9_examples_still_hold():  # the cases in G9's own tests, so the file can replace theirs
    assert n.normalize("Janet’s DUCKS, lay 16-eggs!") == ["janet", "s", "ducks", "lay", "16", "eggs"]
    assert n.normalize("ＡＢＣ ½") == ["abc", "1", "2"]
    assert n.normalize("ગુજરાતી ભાષા") == ["ગુજરાતી", "ભાષા"]
    assert n.normalize("हिन्दी भाषा") == ["हिन्दी", "भाषा"]


def test_offsets_point_into_original_text():
    text = "Hello,   wide World"
    for w, off in n.words_with_offsets(text):
        assert text[off:off + len(w)].lower() == w


@pytest.mark.parametrize("dirty, word", [
    ("com​pute", "compute"),       # zero-width space (A1) does not split the word
    ("co­operate", "cooperate"),   # soft hyphen
    ("﻿import", "import"),         # byte-order mark
    ("ﬁrst", "first"),             # fi ligature (A5)
    ("Ｆｏｏ", "foo"),      # fullwidth letters (A5)
    ("Straße", "strasse"),         # casefold
    ("café", "café"),        # e + combining accent composes
])
def test_invisible_and_compatibility_forms_match_the_plain_word(dirty, word):
    assert n.normalize(dirty) == [word]


def test_zwnj_inside_an_indic_word_keeps_it_whole():
    assert n.normalize("क्‌ष अ") == ["क्ष", "अ"]


@pytest.mark.parametrize("text", ["", "   ", "!!! --- ???", "​​"])
def test_no_words(text):
    assert n.normalize(text) == []


@pytest.mark.parametrize("text", ["Janet’s DUCKS, lay 16-eggs!", "x² + ½ = ⅓", "com​pute the ﬁrst Straße"])
def test_normalize_is_stable(text):
    once = n.normalize(text)
    assert n.normalize(" ".join(once)) == once


def test_clean_character_fixes_do_not_change_the_words():
    """A doc that clean.py repairs for invisible characters or ligatures gives the same words before and after."""
    doc = {"doc_id": "x", "url": "http://a/b", "lang_label": "en", "pack_id": "math-finemath",
           "text": "Area​ of a circle: the ﬁrst result is pi r squared.\n" * 3}
    action, text = c.clean(doc)
    assert action == "fix" and text != doc["text"]
    assert n.normalize(text) == n.normalize(doc["text"])


def test_id_and_description():
    assert n.NORMALIZE_ID == "g1-spec-v1" and "casefold" in n.DESCRIPTION
