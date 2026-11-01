"""Unit tests for the scope table at the top of clean.py (SCOPE) and for tools/build_clean.py, which writes it from specv1.md.
Every text here is made up; none comes from a pack.

  python -m pytest spec_v1/tests
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

SPEC = Path(__file__).resolve().parents[1]
BUILD = SPEC / "tools" / "build_clean.py"
sys.path.insert(0, str(SPEC))
import clean as c

FAMILIES = {"code": {"code-cpp", "code-go", "code-java", "code-js-ts", "code-python", "code-rust"},
            "english": {"en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"},
            "math": {"math-finemath", "math-megamath"}, "sci": {"sci-finepdfs"}}
PACKS = sorted(set().union(*FAMILIES.values()))
SHEET = (SPEC / "sheets" / "specv1.md").read_text(encoding="utf-8")
SECTIONS = re.findall(r"^## Medicine \d+ — (\w+) / \w+ / `(DA-[A-H]\d-\d{3})`", SHEET, re.M)


def doc(pack, text, lang): return {"doc_id": "x", "text": text, "url": "http://a/b", "lang_label": lang, "pack_id": pack}


def test_every_rule_has_one_scope_entry_in_sheet_order():
    assert list(c.SCOPE) == list(c._RULE) == [rid for _, rid in SECTIONS] + ["f1_rule.py"]
    assert all(isinstance(packs, frozenset) and packs for packs in c.SCOPE.values())


def test_each_pack_is_in_exactly_one_family():
    assert {f: {p for p, g in c._FAMILY.items() if g == f} for f in FAMILIES} == FAMILIES
    for fam, rid in SECTIONS:
        assert c.SCOPE[rid] <= FAMILIES[fam]


def test_each_family_runs_its_rules_in_sheet_order():
    assert {f: [c._ID[make] for make in rules] for f, rules in c._PIPELINES.items()} == {f: [rid for g, rid in SECTIONS if g == f] for f in FAMILIES}


def test_the_f1_rules_cover_their_whole_family():
    assert c.SCOPE["DA-F1-005"] == FAMILIES["english"]  # the instructor's F1 rule, never left out
    assert c.SCOPE["DA-F1-006"] == FAMILIES["sci"]
    assert c.SCOPE["f1_rule.py"] == FAMILIES["code"]  # the shared F1


def test_a_math_rule_takes_the_packs_of_its_origin():
    assert c.SCOPE["DA-A1-005"] == {"math-finemath"} and c.SCOPE["DA-C5-001"] == {"math-megamath"}
    assert c.SCOPE["DA-A3-001"] == FAMILIES["math"]


@pytest.mark.parametrize("rid, text, lang", [
    ("DA-A1-001", "\ufeffpackage main\n", "go"),                          # code A1: a BOM
    ("DA-A1-004", "The river\u200b rises in the hills.\n", "en"),         # English A1: a zero-width space
    ("DA-A1-005", "Area\u200b of a circle is pi r squared.\n", "en"),      # math A1, finemath only
    ("DA-B4-013", "Call FUN and <function name> in the text.\n", "en"),   # science B4: a converter label
])
@pytest.mark.parametrize("pack", PACKS)
def test_a_rule_acts_only_on_the_packs_of_its_scope(rid, text, lang, pack):
    expect = "fix" if pack in c.SCOPE[rid] else "keep"
    assert c._RULE[rid]()(doc(pack, text, lang))[0] == expect  # the rule's own guard, which reads SCOPE
    assert c._run(doc(pack, text, lang), c._RULE[rid])[0] == expect  # and _run, which checks SCOPE before any rule


def test_the_scope_table_decides(monkeypatch):
    text = "\ufeffpackage main\n"
    assert c.a1(doc("code-go", text, "go"))[0] == "fix"
    monkeypatch.setitem(c.SCOPE, "DA-A1-001", frozenset({"code-cpp"}))
    assert c.a1(doc("code-go", text, "go")) == ("keep", text)


@pytest.mark.parametrize("pack", [None, "en-unknown"])
def test_no_rule_runs_without_a_known_pack(pack):
    row = {k: v for k, v in doc(pack, "\ufeffArea\u200b of <b>a</b> circle.\n", "en").items() if v is not None}
    assert c.clean(row) == ("keep", row["text"])
    assert all(c._run(row, make) == ("keep", row["text"]) for make in c._RULE.values())


def build(tmp_path, sheet=SHEET):
    (tmp_path / "specv1.md").write_text(sheet, encoding="utf-8", newline="\n")
    return subprocess.run([sys.executable, "-I", str(BUILD), "--sheet", str(tmp_path / "specv1.md"), "--out", str(tmp_path / "clean.py")],
                          capture_output=True, text=True)


def with_packs(rid, packs):
    """specv1.md with the SPEC_PACKS line of one rule changed."""
    start = SHEET.index(f"/ `{rid}`")
    end = SHEET.index("\n## Medicine ", start)
    section = re.sub(r"^SPEC_PACKS = .*$", f"SPEC_PACKS = {packs!r}", SHEET[start:end], count=1, flags=re.M)
    return SHEET[:start] + section + SHEET[end:]


def test_the_build_writes_this_clean_py(tmp_path):
    r = build(tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "clean.py").read_bytes() == (SPEC / "clean.py").read_bytes()


@pytest.mark.parametrize("rid, packs, error", [
    ("DA-A1-004", set(), "applies to no pack"),
    ("DA-A1-004", FAMILIES["english"] | {"math-finemath"}, "in two families"),
    ("DA-F1-005", {"en-dclm"}, "DA-F1-005 must be in the sheet"),
])
def test_the_build_stops_on_a_bad_scope(tmp_path, rid, packs, error):
    r = build(tmp_path, with_packs(rid, packs))
    assert r.returncode != 0 and error in r.stderr
    assert not (tmp_path / "clean.py").exists()
