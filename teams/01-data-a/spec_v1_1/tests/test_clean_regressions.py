"""Synthetic regressions for code-pack F1 dispatch and Sanskrit number preservation (#734)."""
import importlib.util
from pathlib import Path

import pytest

@pytest.fixture
def cleaner():
    path = Path(__file__).resolve().parents[1] / 'clean.py'
    spec = importlib.util.spec_from_file_location('regression_v1_1', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def document(pack, text, lang):
    return dict(doc_id='synthetic', text=text, url='', pack_id=pack, lang_label=lang)


@pytest.mark.parametrize('pack, lang, prefix, string_line', [
    ('code-cpp', 'cpp', '//', 'const char* owner = "{email}";'),
    ('code-go', 'go', '//', 'package main\nconst owner = "{email}"'),
    ('code-java', 'java', '//', 'class A {{ String owner = "{email}"; }}'),
    ('code-js-ts', 'typescript', '//', 'const owner: string = "{email}";'),
    ('code-python', 'python', '#', 'owner = "{email}"'),
    ('code-rust', 'rust', '//', 'const OWNER: &str = "{email}";'),
])
def test_generic_code_tag_masks_contacts_with_the_packs_parser(cleaner, pack, lang, prefix, string_line):
    c = cleaner
    pytest.importorskip('tree_sitter_language_pack')
    email = 'jordan' + '@' + 'mail.io'
    for text in (f'{prefix} by {email}\n', string_line.format(email=email) + '\n'):
        row = document(pack, text, 'code')
        original = dict(row)
        result = c.f1(row)
        assert result == c.f1(dict(row, lang_label=lang))
        assert result == ('fix', text.replace(email, '<EMAIL>'))
        assert c.f1(dict(row, text=result[1])) == ('keep', result[1])
        assert row == original


def test_generic_code_tag_preserves_arithmetic_and_runs_in_clean(cleaner):
    c = cleaner
    pytest.importorskip('tree_sitter_language_pack')
    text = 'package main\nvar x = 555-010-0199\n'
    assert c.f1(document('code-go', text, 'code')) == ('keep', text)
    text = 'package main // by jordan' + '@' + 'mail.io\n'
    assert c.clean(document('code-go', text, 'code')) == ('fix', 'package main // by <EMAIL>\n')


def test_explicit_code_language_is_preserved(cleaner, monkeypatch):
    c = cleaner
    seen = []
    def spans(text, lang):
        seen.append(lang)
        return [(0, len(text.encode('utf-8')))]
    monkeypatch.setattr(c, '_f1_text_spans', spans)
    c.f1(document('code-js-ts', '// by jordan' + '@' + 'mail.io\n', 'javascript'))
    assert seen == ['javascript']


def test_unknown_code_pack_does_not_guess_a_parser(cleaner):
    c = cleaner
    text = '// by jordan' + '@' + 'mail.io\n'
    assert c._shared_f1(document('code-unknown', text, 'code')) == ('keep', text)


@pytest.mark.parametrize('text', ['श्लोकः॥१०० अनन्तरम्।', 'श्लोकः॥100 अनन्तरम्।',
                                 'वर्षे १९९६तमे संवत्सरे।', 'वर्षे 1996तमे संवत्सरे।',
                                 'वर्षा१९९६तमे संवत्सरे।'])
def test_sanskrit_b4_preserves_numbers_and_removes_wiki_markup(cleaner, text):
    c = cleaner
    row = document('ind-sa-fw2', text, 'san_Deva')
    rule = c._RULE['DB-B4-004']()
    assert rule(row) == ('keep', text)
    marked = "{{template}}'''[[लेखः|" + text + "]]'''↩"
    assert rule(dict(row, text=marked)) == ('fix', text)
