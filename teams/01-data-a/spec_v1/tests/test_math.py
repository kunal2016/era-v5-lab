"""Unit tests for the math family of clean.py (spec/medicine_math.md). Every text here is made up; none comes from a pack.

  python -m pytest spec_v1/tests
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clean as c

BODY = "Let x be a real number. Then x squared is never negative, so the sum of two squares is at least zero.\n"


def fm(text): return {"doc_id": "x", "text": text, "url": "http://a/b", "lang_label": "en", "pack_id": "math-finemath"}
def mm(text): return {"doc_id": "x", "text": text, "url": "http://a/b", "lang_label": "en", "pack_id": "math-megamath"}


@pytest.mark.parametrize("fn, row, action", [
    (c.a1, fm("Area\u200b of a circle is pi r squared.\n" + BODY), "fix"),
    (c.a3, fm("Here\u00e2\u20ac\u2122s the proof.\n" + BODY), "fix"),          # mojibake of a right single quote
    (c.a5, fm("the \ufb01rst term\n" + BODY), "fix"),                            # the fi ligature
    (c.b2, fm("x<br>y and <strong>z</strong>\n" + BODY), "fix"),
    (c.b4, fm("{{ 'course-label' | message }}\n" + BODY), "fix"),
    (c.b5, fm("$$$x^2$$\n" + BODY), "fix"),
    (c.c1, fm(BODY + "Share\nWrite a comment\n"), "fix"),
    (c.c2, fm(BODY + "".join("Introductory Physics Homework Help forum\n" for _ in range(6))), "fix"),
    (c.c3, fm("This preview shows page 1 - 2 out of 4 pages.\n" + BODY), "drop"),
    (c.c5, fm(BODY + "See more: Ten Fun Facts About Algebra\n"), "fix"),
    (c.c5, mm("Study guides\n\nQ: What is 3 divided by 4?\n\nWrite your answer...\n\nSubmit\n\nRelated questions\n\nIt is 0.75.\n"), "drop"),
])
def test_treats_a_sick_math_page(fn, row, action):
    a, new = fn(row)
    assert a == action
    assert action == "drop" or new != row["text"]


def test_a_teaser_cut_is_trimmed_to_the_last_sentence():
    a, new = c.c3(fm(BODY + "The second claim follows from the first. A deeper unders..."))
    assert a == "fix" and new.rstrip().endswith("first.")


@pytest.mark.parametrize("fn", [c.a1, c.a3, c.a5, c.b2, c.b4, c.b5, c.c1, c.c2, c.c3, c.c5])
def test_leaves_a_clean_math_page(fn):
    text = BODY + "Display: $$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$$ and $$a$$$$b$$ are two blocks.\n"
    assert fn(fm(text)) == ("keep", text)


@pytest.mark.parametrize("row", [
    {"doc_id": "x", "text": "x<br>y\n" + BODY, "lang_label": "en"},                                  # no pack_id
    {"doc_id": "x", "text": "x<br>y\n" + BODY, "lang_label": "en", "pack_id": "en-dclm"},           # English, not this family
])
def test_math_rules_run_only_on_math_packs(row):
    assert c.b2(row) == ("keep", row["text"])


def test_a_rule_runs_only_on_its_own_packs():
    text = "Area\u200b of a circle.\n" + BODY
    assert c.a1(fm(text))[0] == "fix" and c.a1(mm(text)) == ("keep", text)   # A1 is a finemath rule only


@pytest.mark.parametrize("row", [fm("Here\u00e2\u20ac\u2122s a\u200b <br>proof.\nShare\n" + BODY),
                                 mm("the \ufb01rst <b>term</b>\n" + BODY)])
def test_clean_twice_is_clean_once_on_math(row):
    a, once = c.clean(row)
    assert a == "fix"
    assert c.clean(dict(row, text=once)) == ("keep", once)
