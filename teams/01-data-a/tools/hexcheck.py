"""List only the unusual characters in one document, in the agreed Data A hex format.

Usage:
    python hexcheck.py <pack.parquet> <doc_id> [<doc_id> ...]

Skips ordinary spaces (U+0020), tabs (U+0009) and line breaks (U+000A). In an Indic
document it also skips the ordinary letters, signs and digits of the document's own script.
Covers the whole document (no 2,000-character limit).
Prints a ready-to-paste `hex` cell: `offset U+XXXX NAME`, `(Nx)` for repeats
(offset of the first one), entries separated by ` | `.
Also lists G-group candidates (G1 cut at a vowel sign, G2 misplaced joiner, G4 mixed digits
and characters NFKC would change) and, for documents labelled with an Indic language, G3 hints:
traces that text was dropped (low share of the expected script, runs of empty lines, empty
headings or list items, text ending mid-sentence). G3 has no hex cell. A missing joiner (G2)
and the dropped text itself cannot be seen from the characters: judge those by reading.
Reminder: the hex column is only for A and G codes, and always empty for F1 and E3.
"""
import re, sys, unicodedata
import pyarrow.parquet as pq

# Common names for control characters (Unicode gives them no official name)
CONTROL_NAMES = {
    0x00: "NULL", 0x07: "BELL", 0x08: "BACKSPACE", 0x0B: "LINE TABULATION", 0x0C: "FORM FEED",
    0x0D: "CARRIAGE RETURN", 0x1B: "ESCAPE", 0x7F: "DELETE", 0x85: "NEXT LINE",
}
SKIP = {0x09, 0x0A, 0x20}


def name(cp):
    if cp in CONTROL_NAMES:
        return CONTROL_NAMES[cp]
    n = unicodedata.name(chr(cp), "")
    return n or f"CONTROL U+{cp:04X}"


A1_SET = {0x200B, 0xFEFF, 0x00AD, *range(0x202A, 0x202F), *range(0x2066, 0x206A)}
SPACE_LIKE = {0x00A0, 0x2007, 0x202F, 0x2002, 0x2003, 0x2009, 0x200A, 0x3000}
MOJIBAKE = re.compile(r"(Ã[\x80-\xbf¡-ÿ]|â€[™œ\x9d“”˜¦]|Â[\xa0-\xbf]|à¤|à¦)")


def kind(text, off, cp):
    """A short hint of what this character might be, mapped to DISEASES.md codes."""
    ch = chr(cp)
    if cp == 0xFFFD:
        return "A4 replacement character: bytes already lost"
    if cp in A1_SET:
        return "A1 invisible junk"
    if cp in (0x200C, 0x200D):
        return "ZWJ/ZWNJ: part of Indic script, NOT a disease there; A1 only in non-Indic text"
    if unicodedata.category(ch) == "Cc" or 0x7F <= cp <= 0x9F:
        return "A2 control character"
    if 0xE000 <= cp <= 0xF8FF:
        return "private-use character: check for broken fonts or icons"
    if cp in SPACE_LIKE:
        return "special space: usually fine, check if deliberate"
    if MOJIBAKE.match(text, max(0, off - 1)) or MOJIBAKE.match(text, off):
        return "A3? possible mojibake"
    if unicodedata.combining(ch):
        return "combining mark: check A5 (NFC) or G1"
    if unicodedata.normalize("NFC", ch) != ch:
        return "A5? changes under NFC"
    # A6: a non-Latin letter inside a word that is otherwise Latin
    if ch.isalpha() and not unicodedata.name(ch, "").startswith("LATIN"):
        a, b = off, off + 1
        while a > 0 and text[a - 1].isalpha(): a -= 1
        while b < len(text) and text[b].isalpha(): b += 1
        word = text[a:b]
        if any(c.isascii() and c.isalpha() for c in word):
            return f"A6? mixed script in word '{word}'"
        return "letter from another script: usually real text"
    return "symbol or accented letter: usually fine"


# ---- G group: damage from earlier cleaning (mostly Indic) -----------------------
# Indic scripts from Devanagari to Malayalam each own one 128-code-point block.
INDIC_LO, INDIC_HI = 0x0900, 0x0D7F
SCRIPT_NAMES = {0x0900: "DEVANAGARI", 0x0980: "BENGALI", 0x0A00: "GURMUKHI", 0x0A80: "GUJARATI",
                0x0B00: "ORIYA", 0x0B80: "TAMIL", 0x0C00: "TELUGU", 0x0C80: "KANNADA", 0x0D00: "MALAYALAM"}
ZWNJ, ZWJ = 0x200C, 0x200D


def _block(cp):
    return (cp & ~0x7F) if INDIC_LO <= cp <= INDIC_HI else None


def _is_indic_mark(ch):
    return _block(ord(ch)) is not None and unicodedata.category(ch) in ("Mn", "Mc")


def _is_virama(ch):
    return _block(ord(ch)) is not None and "VIRAMA" in unicodedata.name(ch, "")


def _cell(off, cps, tail=""):
    return f"{off} " + " + ".join(f"U+{c:04X} {name(c)}" for c in cps) + (f" {tail}" if tail else "")


def g_candidates(text):
    """Return (code, offset, hex_cell, hint) for G-group candidates. Candidates only: verify in context."""
    out = []
    n = len(text)
    for i, ch in enumerate(text):
        cp = ord(ch)
        # G1: a dependent vowel sign, virama or nukta that is not attached to its own script
        if _is_indic_mark(ch):
            prev = text[i - 1] if i else ""
            if prev and ord(prev) in (ZWJ, ZWNJ):
                continue
            if prev and _block(ord(prev)) == _block(cp):
                continue
            if prev and prev.isspace() and i >= 2 and _block(ord(text[i - 2])) == _block(cp):
                out.append(("G1", i - 2, _cell(i - 2, [ord(text[i - 2]), ord(prev), cp]),
                            "word cut before a vowel sign or virama"))
            else:
                prev_desc = f"after U+{ord(prev):04X} {name(ord(prev))}" if prev else "at start of text"
                out.append(("G1?", i, _cell(i, [cp], f"({prev_desc})"),
                            "mark not attached to a letter of its script"))
        # G2: a joiner that is not right after a virama, inside Indic text
        if cp in (ZWJ, ZWNJ):
            prev = text[i - 1] if i else ""
            nxt = text[i + 1] if i + 1 < n else ""
            indic_context = (prev and _block(ord(prev))) or (nxt and _block(ord(nxt)))
            if indic_context and not (prev and _is_virama(prev)):
                out.append(("G2?", i, _cell(i, [cp], f"(after U+{ord(prev):04X} {name(ord(prev))}, expected after a virama)")
                            if prev else _cell(i, [cp]), "joiner in an unexpected place; check the conjunct renders right"))
    # G4: one number written with Indic and Latin digits mixed (e.g. Devanagari 1, Latin 0)
    for m in re.finditer(r"[0-9०-९০-৯੦-੯૦-૯୦-୯"
                         r"௦-௯౦-౯೦-೯൦-൯]+", text):
        tok = m.group(0)
        blocks = {_block(ord(c)) for c in tok if not c.isascii()}
        if blocks and any(c.isascii() for c in tok) and len(blocks) == 1:
            base = blocks.pop()
            for k, c in enumerate(tok):
                if c.isascii():
                    exp = base + 0x66 + int(c)
                    out.append(("G4", m.start() + k, _cell(m.start() + k, [ord(c)], f"(expected U+{exp:04X})"),
                                f"Latin digit inside a {SCRIPT_NAMES.get(base, 'Indic')} number"))
    # G4 risk: characters that an NFKC step would change (superscripts, ligatures, full-width, micro sign...)
    seen = set()
    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in seen or cp < 0x80:
            continue
        if unicodedata.normalize("NFKC", ch) != unicodedata.normalize("NFC", ch):
            seen.add(cp)
            to = " + ".join(f"U+{ord(c):04X}" for c in unicodedata.normalize("NFKC", ch))
            out.append(("G4 risk", i, _cell(i, [cp], f"(NFKC would make it {to})"),
                        "not damage yet; a medicine that uses NFKC would change this"))
    return out


# ---- G3 hints: Indic text dropped or damaged by an English-only cleaning step ------------
# G3 is missing text, so there is no character to point at and no hex cell. These are TRACES
# that such a step often leaves; each one only says "read this document closely".
LANG_BLOCK = {"hi": 0x0900, "mr": 0x0900, "sa": 0x0900, "ne": 0x0900, "kok": 0x0900, "mai": 0x0900,
              "bn": 0x0980, "as": 0x0980, "pa": 0x0A00, "gu": 0x0A80, "or": 0x0B00, "od": 0x0B00,
              "ta": 0x0B80, "te": 0x0C00, "kn": 0x0C80, "ml": 0x0D00}
LANG_NAMES = {"hindi": "hi", "marathi": "mr", "sanskrit": "sa", "nepali": "ne", "bengali": "bn", "bangla": "bn",
              "assamese": "as", "punjabi": "pa", "gujarati": "gu", "odia": "or", "oriya": "or", "tamil": "ta",
              "telugu": "te", "kannada": "kn", "malayalam": "ml"}
END_MARKS = ("।", "॥", ".", "?", "!", "\"", "'", ")", "”", "’", ":", ";")


def expected_block(lang_label):
    """Map a pack's lang_label (e.g. 'hi', 'hin_Deva', 'Hindi') to its Indic script block."""
    l = (lang_label or "").strip().lower()
    if l in LANG_NAMES:
        l = LANG_NAMES[l]
    for key in sorted(LANG_BLOCK, key=len, reverse=True):
        if l == key or l.startswith(key + "_") or l.startswith(key + "-"):
            return LANG_BLOCK[key]
    if l.startswith(("hin", "mar", "san", "nep")):
        return 0x0900
    for code3, b in (("ben", 0x0980), ("asm", 0x0980), ("pan", 0x0A00), ("guj", 0x0A80), ("ori", 0x0B00),
                     ("ory", 0x0B00), ("tam", 0x0B80), ("tel", 0x0C00), ("kan", 0x0C80), ("mal", 0x0D00)):
        if l.startswith(code3):
            return b
    return None


def g3_hints(text, lang_label):
    """Return (offset, hint) pairs. Only for documents whose label is an Indic language."""
    home = expected_block(lang_label)
    if home is None:
        return []
    out = []
    letters = [c for c in text if c.isalpha()]
    own = sum(1 for c in letters if _block(ord(c)) == home)
    latin = sum(1 for c in letters if c.isascii())
    if letters:
        share = own / len(letters)
        if share < 0.5:
            out.append((0, f"only {share:.0%} of letters are {SCRIPT_NAMES.get(home)}, {latin} Latin letters: "
                           f"Indic parts may have been removed (G3), or the label is wrong (D1)"))
    for m in re.finditer(r"\n[ \t]*\n[ \t]*\n[ \t]*\n", text):
        out.append((m.start(), "three or more empty lines in a row: a paragraph may have been cut out"))
    lines = text.split("\n")
    pos = 0
    for k, line in enumerate(lines):
        stripped = line.strip()
        nxt = next((l.strip() for l in lines[k + 1:] if l.strip()), "")
        is_heading = stripped.startswith("#") or (stripped.endswith(":") and len(stripped) < 60)
        is_item = re.match(r"^([0-9०-९]+[.)]|[-*•])\s*$", stripped)
        if is_item:
            out.append((pos, f"list marker '{stripped}' with no text after it"))
        elif is_heading and (not nxt or nxt.startswith("#")):
            out.append((pos, f"heading '{stripped[:40]}' with nothing under it"))
        pos += len(line) + 1
    tail = text.rstrip()
    if tail and own and not tail.endswith(END_MARKS) and _block(ord(tail[-1])) == home:
        out.append((len(tail) - 1, "text ends mid-sentence (no danda or full stop): check C3 truncation or G3"))
    return out[:20]


def main_script_block(text):
    """The Indic block most of the document's non-ASCII letters belong to, if any (> 50%)."""
    counts, total = {}, 0
    for ch in text:
        if ord(ch) > 127 and ch.isalpha():
            total += 1
            b = _block(ord(ch))
            if b is not None:
                counts[b] = counts.get(b, 0) + 1
    if total and counts:
        b, n = max(counts.items(), key=lambda kv: kv[1])
        if n > total / 2:
            return b
    return None


def unusual(text):
    """Characters worth a look. In an Indic document, the ordinary letters, marks and digits of
    its own script (and the danda) count as normal and are not listed; joiners still are."""
    home = main_script_block(text)
    found = {}  # code point -> [first offset, count]
    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in SKIP:
            continue
        if home is not None and (_block(cp) == home or cp in (0x0964, 0x0965)) \
                and unicodedata.category(ch)[0] in "LMNP":
            continue
        if cp > 127 or unicodedata.category(ch)[0] in "CZ":
            if cp in found:
                found[cp][1] += 1
            else:
                found[cp] = [i, 1]
    return sorted(found.items(), key=lambda kv: kv[1][0])


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    rows = {r["doc_id"]: r for r in pq.read_table(sys.argv[1]).to_pylist()}
    for did in sys.argv[2:]:
        r = rows.get(did)
        print("=" * 70)
        if not r:
            print(f"{did}: not in this pack"); continue
        t = r["text"]
        items = unusual(t)
        print(f"{did}  {r['lang_label']}  {len(t)} chars")
        if not items:
            print("No unusual characters. Nothing for the hex column.")
            for off, hint in g3_hints(t, r.get("lang_label")):
                print(f"  G3?      offset {off}: {hint}")
            continue
        print(f"{'offset':>7}  {'code':8} {'count':>5}  name / UTF-8 bytes / hint / context")
        cells = []
        for cp, (off, n) in items:
            ch = chr(cp)
            ctx = t[max(0, off - 15):off + 15].replace("\n", "⏎").replace("\r", "␍").replace(ch, "⟦" + f"U+{cp:04X}" + "⟧", 1)
            print(f"{off:7d}  U+{cp:04X}  {n:5d}  {name(cp)} / {ch.encode('utf-8').hex(' ').upper()} / {kind(t, off, cp)} / …{ctx}…")
            cells.append(f"{off} U+{cp:04X} {name(cp)}" + (f" ({n}x)" if n > 1 else ""))
        print("\nhex cell (paste only if the row has an A or G code; check the context first):")
        print(" | ".join(cells))
        g3 = g3_hints(t, r.get("lang_label"))
        if g3:
            print("\nG3 hints (text dropped by an English-only step; no hex cell, put a quote and offset in evidence):")
            for off, hint in g3:
                print(f"  G3?      offset {off}: {hint}")
        g = g_candidates(t)
        if g:
            print("\nG-group candidates (verify in context; G2 and G4 also need the expected form):")
            for code, off, cell, hint in g[:40]:
                print(f"  {code:8} {cell}   [{hint}]")
            if len(g) > 40:
                print(f"  ... {len(g) - 40} more")
            real = [cell for code, off, cell, hint in g if code in ("G1", "G2?", "G4")]
            if real:
                print("\nG hex cell (paste only after checking):")
                print(" | ".join(real[:10]))


if __name__ == "__main__":
    main()
