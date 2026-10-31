"""F1 on prose packs (math, science): the prose path of tools/f1_rule.py. Every value is made up (555-01xx numbers,
example names and domains); none comes from a pack.

  python -m pytest spec_v1/tests
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clean as c

AT = "@"  # made-up addresses are joined at run time, like test_clean.py


def sci(text): return {"doc_id": "x", "text": text, "url": "http://a/b.pdf", "lang_label": "eng_Latn", "pack_id": "sci-finepdfs"}
def math(text): return {"doc_id": "x", "text": text, "url": "http://a/b", "lang_label": "en", "pack_id": "math-megamath"}


@pytest.mark.parametrize("text, expect", [
    ("Call me.\nHome: 312-555-0142\n", "Call me.\nHome: <PHONE>\n"),
    ("Reach Pat on 312-555-0177 (cell) after six.", "Reach Pat on <PHONE> (cell) after six."),
    (f"Written by jordan.sample{AT}mailhost.net; questions to info{AT}mailhost.net or someone{AT}example.org",
     f"Written by <EMAIL>; questions to info{AT}mailhost.net or someone{AT}example.org"),
])
def test_private_values_get_their_tag(text, expect):
    assert c.f1(sci(text)) == ("fix", expect)


def test_contact_card_phone_and_address():
    a, new = c.f1(sci("Jordan Sample\n12 Maple Lane\nSpringfield, IL 62701\n217-555-0123\n"))
    assert a == "fix" and "<PHONE>" in new and "<ADDRESS>" in new and "555-0123" not in new and "Maple" not in new


def test_people_table():
    a, new = c.f1(sci("| Name | Telephone | Fax |\n|---|---|---|\n| Jordan Sample | 44 20 5550 0123 | 44 20 5550 0124 |\n"))
    assert a == "fix" and new.count("<PHONE>") == 2 and "5550" not in new


def test_mailing_list_at_form_on_math():
    a, new = c.f1(math("Re: patch\nJordan Sample\njsample at mail.example-uni.net\nThu Oct 1 2009\n"))
    assert a == "fix" and "jsample at" not in new and "<EMAIL>" in new


def test_listing_of_individuals_is_dropped():
    rows = "".join(f"SAMPLE, Jordan Lee, {30 + i}, {i} Maple Lane, Springfield, Clerk. Order made.\n" for i in range(8))
    assert c.f1(sci(rows))[0] == "drop"


@pytest.mark.parametrize("text", [
    "County Clerk's Office\n100 Main Street\nPhone: 312-555-0100\n",                        # public office
    "Call 1-800-555-0199 for help.",                                                         # toll free
    "**Food Pantry Network**\n- Address: 22 Oak Street, Springfield, IL 62701\n- Phone: 217-555-0188\n"
    "- Website: https://pantry.example.org/\n",                                              # a directory of organisations
    f"Contact us\n\nsales.team.lead{AT}company-mail.net",                                    # an organisation's mailbox
    "The data set is available at data.example-archive.net under CC0.",                     # "at" in prose is not an email
    "We set $x = 312-555$ and n = 1.000.0000 in Table 3, page 555-0123 of the appendix.",  # numbers that look alike
])
def test_organisations_and_look_alikes_are_kept(text):
    assert c.f1(sci(text)) == ("keep", text)


@pytest.mark.parametrize("row", [
    {"doc_id": "x", "text": "Home: 312-555-0142", "lang_label": "en"},                                   # no pack_id
    {"doc_id": "x", "text": "Home: 312-555-0142", "lang_label": "en", "pack_id": "en-dclm"},            # English: not harm-tested
    {"doc_id": "x", "text": "Home: 312-555-0142", "lang_label": "en", "pack_id": "sci-finepdfs"},       # wrong tag for that pack
])
def test_prose_path_runs_only_on_harm_tested_packs(row):
    assert c.f1(row) == ("keep", row["text"])


def test_clean_twice_is_clean_once_on_prose():
    row = sci(f"Jordan Sample\n12 Maple Lane\nSpringfield, IL 62701\nHome: 217-555-0123\njordan.s{AT}mailhost.net\n")
    a, once = c.clean(row)
    assert a == "fix"
    assert c.clean(dict(row, text=once)) == ("keep", once)
