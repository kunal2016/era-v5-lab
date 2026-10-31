"""Unit tests for the English rules of clean_english.py (both sheets, as tools/build_clean.py builds them) and for
scripts/clean_english.py (the English sheet alone). Every value here is made up; none comes
from a pack.

  python -m pytest spec_v1/tests
"""
import hashlib
import importlib.util
import re
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "medicine_english.md"
_both = importlib.util.spec_from_file_location("clean_both", ROOT / "clean_english.py")
c = importlib.util.module_from_spec(_both)
_both.loader.exec_module(c)

_spec = importlib.util.spec_from_file_location("clean_english", ROOT / "scripts" / "clean_english.py")
e = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e)

AT = "@"  # pr-guard reads added lines for email addresses, so made-up ones are joined at run time
ZWJ, ZWNJ = chr(0x200D), chr(0x200C)  # written as numbers: a raw joiner in code is invisible
PARA = ("The river rises in the hills and runs south to the sea. "
        "Farmers along its banks grow rice and wheat in the dry months.")
RUSSIAN = "Это строка на русском языке."
HINDI_ZWJ = "क्‍ष"      # half ka + ssa: the joiner asks for the half form
HINDI_ZWNJ = "क्‌ष"     # ka + virama + ssa: the joiner stops the conjunct
ENGLISH_CODES = list(e.RULES)
OTHER_LANGS = ("hi", "mr", "fr", None)      # not English and not a code language: every rule keeps


def en(text, lang="en"):
    return {"doc_id": "x", "text": text, "url": "http://a/b", "lang_label": lang}


def sheet():
    """The sheet's blocks, each in its own namespace, as harm_test.py runs them."""
    out = []
    for b in re.findall(r"^```python\n(.*?)^```[ \t]*$", SHEET.read_text(encoding="utf-8"), re.S | re.M):
        if 'RULE_ID = "' in b:
            ns = {"__name__": "rules"}
            exec(textwrap.dedent(b), ns)
            out.append((ns["RULE_ID"], ns["medicine"]))
    return out


def run_sheet(doc):
    d = dict(doc)
    for _, m in sheet():
        a, t = m(d)
        if a == "drop":
            return ("drop", doc["text"])
        d["text"] = t
    return ("fix" if d["text"] != doc["text"] else "keep", d["text"])


# (code, sick text, action, the text after a fix or None for a drop)
SICK = [
    ("A1", "Hello​world﻿ and more.", "fix", "Helloworld and more."),
    ("A2", "Bell\x07 here\r\nnext line", "fix", "Bell here\nnext line"),
    ("A3", "The cafÃ© didnâ€™t open on Monday. " + PARA, "fix", "The café didn't open on Monday. " + PARA),
    ("A5", "Café au lait", "fix", "Café au lait"),
    ("B1", "Fish &amp; chips&nbsp;today &mdash; fresh.", "fix", "Fish & chips today — fresh."),
    ("B2", "<p>First paragraph.</p><div>Second paragraph.</div>", "fix", " First paragraph. Second paragraph. "),
    ("C3", "The council will meet on Monday to discuss the", "drop", None),
    ("C3", "Short teaser ending here [...]", "drop", None),
    ("C5", "Buy cheap nfl jerseys today and ray ban sunglasses outlet deals. " + PARA, "drop", None),
    ("C5", PARA + "\nTags: river, farming, rice", "fix", PARA),
    ("D4", "{Hello|Hi} there, {friend|buddy}. " + PARA, "drop", None),
    ("C1", PARA + "\nShare this:\n" + PARA, "fix", PARA + "\n" + PARA),
    ("C2", "Subscribe to our newsletter\n" + PARA + "\nSubscribe to our newsletter\nMore text.\nSubscribe to our newsletter",
     "fix", "Subscribe to our newsletter\n" + PARA + "\n\nMore text.\n"),
    ("D3", PARA + "\n" + RUSSIAN + "\n" + PARA, "fix", PARA + "\n" + PARA),
    ("B4", "Welcome {{ user.name }} to the shop. " + PARA, "fix", "Welcome  to the shop. " + PARA),
    ("B4", "Total Due After -DATE-: 40 dollars. " + PARA, "fix", "Total Due After the Due Date: 40 dollars. " + PARA),
    ("B4", "Price: NaN\n" + PARA, "fix", "Price:\n" + PARA),
    ("B4", "She called it'smart work' today. " + PARA, "fix", "She called it 'smart work' today. " + PARA),
    ("B4", PARA + " The text does not mention the price. " + PARA, "fix", PARA + " " + PARA),
    ("F1", PARA + "\nCall me on 555-867-5309 or write to ravi.kumar" + AT + "gmail.com.", "fix",
     PARA + "\nCall me on <PHONE> or write to <EMAIL>."),
    ("F1", PARA + "\nI live at 42 Elm Street, Springfield, IL 62704.", "fix", PARA + "\nI live at <ADDRESS>."),
]

# (code, a text that looks like the disease but is not: it must stay as it is)
LOOK_ALIKE = [
    ("A1", "A plain line with café and an em dash — here."),
    ("A1", "Hindi keeps its joiners: " + HINDI_ZWJ + " and " + HINDI_ZWNJ + "."),
    ("A2", "Tab\tseparated\nlines"),
    ("A3", "A café in São Paulo opens at nine. " + PARA),
    ("A5", "Café au lait"),
    ("B1", "AT&T and R&D work together."),
    ("B2", "Use the <p> tag to start a paragraph in HTML."),
    ("C3", PARA),
    ("C5", PARA + "\nThe tags on the bags were lost."),
    ("D4", "Pipes like a|b and braces {x} are fine. " + PARA),
    ("C1", PARA + "\nShare this story with your friends today.\n" + PARA),
    ("C2", "Subscribe to our newsletter\n" + PARA + "\nSubscribe to our newsletter"),
    ("D3", PARA + " He said спасибо to us."),
    ("B4", PARA + " Sets use { and } braces."),
    ("F1", PARA + "\nContact our office at info" + AT + "acme.com or call 1-800-555-0199."),
    ("F1", PARA + "\nThe years 1990 to 2005 saw 3,000 new farms."),
]

# joiners in every context a rule could touch; no line here is one a rule removes
JOINER_PROBES = dict(zip([
    "hindi-zwj", "hindi-zwnj", "malayalam-chillu", "persian-zwnj", "emoji-family", "emoji-flag", "beside-a1-junk",
    "crlf-and-control", "mojibake", "decomposed-accent", "html", "phone", "address", "long-paragraph", "joiner-in-tags"], [
    "The word " + HINDI_ZWJ + " is written with a half ka.",
    "The word " + HINDI_ZWNJ + " keeps the virama visible.",
    "Old Malayalam writes ന്‍ for the chillu n.",
    "In Persian, می‌خواهم means I want.",
    "Our family \U0001F468‍\U0001F469‍\U0001F467 went on a trip.",
    "Pride month \U0001F3F3️‍\U0001F308 starts in June.",
    "Mixed​‍﻿‌ junk­ and joiners here.",
    "Line one ‍\r\nLine two\x07 ‌ here.\r\n",
    "The cafÃ© sells " + HINDI_ZWJ + " tea, didnâ€™t it?",
    "Café and " + HINDI_ZWNJ + " together.",
    "Entities &amp; joiners ‍ inside <b>bold ‌</b> text.",
    "Call Ravi ‍ on 555-867-5309 tonight ‌ please.",
    "He lives at 42 Elm Street ‍, Springfield, IL 62704 ‌ now.",
    ("Hindi text uses " + HINDI_ZWJ + " and " + HINDI_ZWNJ + ". ") * 30,
    PARA + "\n" + "Tags" + ZWJ + ": not a tag line, the joiner is inside the word\n" + PARA,
]))
CLEANERS = {"spec_v1/clean_english.py": c, "scripts/clean_english.py": e}


def joiners(s):
    return s.count(ZWJ), s.count(ZWNJ)


@pytest.mark.parametrize("m", CLEANERS.values(), ids=CLEANERS.keys())
@pytest.mark.parametrize("code, text, action, after", SICK, ids=[f"{x[0]}-{i}" for i, x in enumerate(SICK)])
def test_treats_a_sick_document(m, code, text, action, after):
    a, new = m.RULES[code](en(text))
    assert a == action
    if action == "drop":
        assert new == text  # a drop hands back the document as it was
    else:
        assert new == after


@pytest.mark.parametrize("m", CLEANERS.values(), ids=CLEANERS.keys())
@pytest.mark.parametrize("code, text", LOOK_ALIKE, ids=[f"{x[0]}-{i}" for i, x in enumerate(LOOK_ALIKE)])
def test_leaves_a_look_alike(m, code, text):
    assert m.RULES[code](en(text)) == ("keep", text)


@pytest.mark.parametrize("code", list(c.RULES))
def test_every_function_leaves_plain_prose(code):
    text = PARA + "\n\n" + PARA
    assert c.RULES[code](en(text)) == ("keep", text)
    assert c.RULES[code](en(text, "eng")) == ("keep", text)


@pytest.mark.parametrize("text", [t for _, t, _, _ in SICK], ids=[f"{x[0]}-{i}" for i, x in enumerate(SICK)])
def test_a_row_of_another_language_passes_unchanged(text):
    for lang in OTHER_LANGS:
        doc = en(text, lang)
        assert all(fn(doc) == ("keep", text) for fn in c.RULES.values())
        assert c.clean(doc) == ("keep", text) and e.clean(doc) == ("keep", text)


@pytest.mark.parametrize("text", [t for _, t, a, _ in SICK if a == "fix"] + [PARA],
                         ids=[f"{x[0]}-{i}" for i, x in enumerate(SICK) if x[2] == "fix"] + ["plain"])
def test_clean_twice_is_clean_once(text):
    a, once = c.clean(en(text))
    if a != "drop":
        assert c.clean(en(once)) == ("keep", once)


# Keep ZWJ and ZWNJ in all text (DISEASES.md, A1: "ZWJ U+200D and ZWNJ U+200C are NOT diseases in Indic text").

@pytest.mark.parametrize("text", JOINER_PROBES.values(), ids=JOINER_PROBES.keys())
def test_no_function_and_not_clean_deletes_a_joiner(text):
    for fn in list(c.RULES.values()) + [c.clean, e.clean]:
        a, new = fn(en(text))
        assert a != "drop", fn.__name__
        assert joiners(new) == joiners(text), fn.__name__


def test_a1_takes_the_junk_and_leaves_the_joiners_beside_it():
    a, new = c.a1(en("Mixed​‍﻿‌ junk­ here."))
    assert (a, new) == ("fix", "Mixed‍‌ junk here.")


def test_d3_takes_a_joiner_only_with_a_whole_foreign_line():
    """D3 deletes a line whose letters are mostly not Latin, so a Hindi line in an English document goes with its
    joiners. That removes the line, not the joiner: a joiner in a line that stays is kept."""
    hindi_line = "यह " + HINDI_ZWJ + "त्रिय है और " + HINDI_ZWNJ + " भी।"
    english_line = "The half form " + HINDI_ZWJ + " appears in this English line."
    a, new = c.d3(en(PARA + "\n" + hindi_line + "\n" + english_line))
    assert (a, new) == ("fix", PARA + "\n" + english_line)
    assert joiners(new) == joiners(english_line)


# F1: DA-F1-005, written to the instructor's F1 ruling of 31 Oct, must never be left out.

def test_f1_on_english_is_the_instructor_rule():
    assert c.RULES["F1"] is c.f1
    assert c._OWN_F1["english"] is c._english_f1_005  # tools/build_clean.py kept the sheet's own F1
    assert not ({"en", "eng"} & c._F1_LANGS)           # the shared F1 does not run on English
    assert 'RULE_ID = "DA-F1-005"' in (ROOT / "clean_english.py").read_text(encoding="utf-8")
    assert e.RULES["F1"] is e.f1 and e._PIPELINES["english"][-1] is e._english_f1_005


@pytest.mark.parametrize("lang", ["en", "eng"])
def test_f1_tags_survive_a_second_clean(lang):
    text = PARA + "\nCall me on 555-867-5309 or write to ravi.kumar" + AT + "gmail.com.\nI live at 42 Elm Street, Springfield, IL 62704."
    a, once = c.clean(en(text, lang))
    assert a == "fix" and all(t in once for t in ("<PHONE>", "<EMAIL>", "<ADDRESS>"))
    assert c.clean(en(once, lang)) == ("keep", once)


def test_the_shared_f1_still_runs_on_code():
    """The code family keeps the shared rule: f1() hands a code row to it, as before English was added."""
    doc = {"doc_id": "x", "text": "package main\n", "url": "a/b.go", "lang_label": "go"}
    assert c.f1(doc) == c._shared_f1(doc)


# both cleaners are the sheet, packaged

def test_clean_english_was_built_from_the_current_sheet():
    assert e.SHEET_SHA256 == hashlib.sha256(SHEET.read_bytes()).hexdigest(), "rerun scripts/build_clean_english.py"


def test_both_cleaners_run_the_sheet_rules_in_the_sheet_order():
    want = [f"_english_{rid[3:].lower().replace('-', '_')}" for rid, _ in sheet()]
    assert [f.__name__ for f in c._PIPELINES["english"]] + [c._OWN_F1["english"].__name__] == want, "rerun tools/build_clean.py"
    assert [f.__name__ for f in e._PIPELINES["english"]] == want


@pytest.mark.parametrize("text", [t for _, t, _, _ in SICK] + [t for _, t in LOOK_ALIKE] + list(JOINER_PROBES.values()),
                         ids=[f"sick-{x[0]}-{i}" for i, x in enumerate(SICK)] + [f"look-alike-{x[0]}-{i}" for i, x in enumerate(LOOK_ALIKE)]
                         + [f"joiner-{k}" for k in JOINER_PROBES])
def test_clean_gives_what_the_sheet_gives(text):
    want = run_sheet(en(text))
    assert c.clean(en(text)) == want
    assert e.clean(en(text)) == want
