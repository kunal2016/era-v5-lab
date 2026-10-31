"""Check ../clean_english.py (the code and English sheets, as ../../tools/build_clean.py builds them) and clean_english.py
(the English sheet alone) against ../medicine_english.md on every document of the English packs.
Prints IDs and counts only, never text.

  python -I verify_clean_english.py <packs dir>

  1 each ../clean_english.py function gives what that code's English sheet blocks give, run in order; the code family's functions keep
  2 ../clean_english.py's clean(doc) gives what the whole sheet gives, run in order (the sheet as harm_test.py tests it)
  3 scripts/clean_english.py's clean(doc) gives the same as ../clean_english.py's
  4 harm_test.py's ALL IN ORDER runs the functions in RULES order: same result as clean(doc)? (both cleaners)
  5 clean(clean(doc)) == ("keep", clean(doc)): a second run changes nothing
  6 ZWJ U+200D and ZWNJ U+200C: clean() never deletes a joiner on its own

Writes ../results/verify_clean_english.json.
"""
import difflib
import importlib.util
import json
import re
import sys
import textwrap
from pathlib import Path

import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
SPEC = HERE.parent
PACKS_DIR = Path(sys.argv[1])
SHEET = SPEC / "medicine_english.md"
PACKS = ["en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"]
ZWJ, ZWNJ = chr(0x200D), chr(0x200C)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


c = load(SPEC / "clean_english.py", "clean_both")
e = load(HERE / "clean_english.py", "clean_english")


def sheet_blocks():
    out = []
    for b in re.findall(r"^```python\n(.*?)^```[ \t]*$", SHEET.read_text(encoding="utf-8"), re.S | re.M):
        if 'RULE_ID = "' in b:
            ns = {"__name__": "rules"}
            exec(textwrap.dedent(b), ns)  # each block in its own namespace, as harm_test.py runs it
            out.append((ns["RULE_ID"], ns["CODE"], ns["medicine"]))
    return out


def run(doc, medicines):
    d = dict(doc)
    for m in medicines:
        a, t = m(d)
        if a == "drop":
            return ("drop", doc["text"])
        d["text"] = t
    return ("fix" if d["text"] != doc["text"] else "keep", d["text"])


def joiners_lost(before, after):
    """Joiners deleted on their own, the text around them kept. A removed line takes its joiners with it: not counted."""
    lost = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if op in ("delete", "replace"):
            seg, new = before[i1:i2], after[j1:j2]
            n = sum(seg.count(j) - new.count(j) for j in (ZWJ, ZWNJ))
            if n > 0 and not any(ch.isalnum() for ch in seg):
                lost += n
    return lost


def main():
    blocks = sheet_blocks()
    sheet = [m for _, _, m in blocks]
    by_code = {}
    for _, code, m in blocks:
        by_code.setdefault(code, []).append(m)
    report = {"sheet": "teams/01-data-a/spec_v1/medicine_english.md", "rules": [rid for rid, _, _ in blocks], "packs": {}}
    for p in PACKS:
        path = PACKS_DIR / f"{p}.parquet"
        rows = pq.read_table(path, columns=[k for k in ("doc_id", "text", "url", "lang_label") if k in pq.read_schema(path).names]).to_pylist()
        fn_differ = {code: [] for code in c.RULES}
        sheet_differ, english_differ, order_c, order_e, again, lost, with_joiners = [], [], [], [], [], [], 0
        actions = {"keep": 0, "fix": 0, "drop": 0}
        for r in rows:
            for code, fn in c.RULES.items():
                if fn(r) != run(r, by_code.get(code, [])):  # a code-family function must keep an English doc
                    fn_differ[code].append(r["doc_id"])
            got = c.clean(r)
            actions[got[0]] += 1
            if got != run(r, sheet):
                sheet_differ.append(r["doc_id"])
            if got != e.clean(r):
                english_differ.append(r["doc_id"])
            if got != run(r, list(c.RULES.values())):
                order_c.append(r["doc_id"])
            if got != run(r, list(e.RULES.values())):
                order_e.append(r["doc_id"])
            if got[0] != "drop" and c.clean(dict(r, text=got[1])) != ("keep", got[1]):
                again.append(r["doc_id"])
            if ZWJ in r["text"] or ZWNJ in r["text"]:
                with_joiners += 1
                if got[0] != "drop" and joiners_lost(r["text"], got[1]):
                    lost.append(r["doc_id"])
        report["packs"][p] = dict(docs=len(rows), clean_actions=actions,
                                  function_vs_sheet_blocks={k: v for k, v in fn_differ.items() if v},
                                  clean_vs_sheet=sheet_differ, clean_vs_clean_english=english_differ,
                                  all_in_order_vs_clean=order_c, clean_english_all_in_order_vs_clean=order_e,
                                  second_run_changes=again, docs_with_joiners=with_joiners, joiners_lost_in_kept_lines=lost)
        print(f"{p}: {len(rows)} docs, clean() {actions} | functions vs sheet blocks differ {sum(map(len, fn_differ.values()))} | "
              f"clean() vs sheet {len(sheet_differ)} | vs scripts/clean_english.py {len(english_differ)} | RULES order vs clean(): "
              f"spec_v1/clean_english.py {len(order_c)} {order_c[:4]}, scripts/clean_english.py {len(order_e)} | second run changes {len(again)} {again[:4]} | "
              f"docs with a joiner {with_joiners}, joiners lost {len(lost)}")
    out = SPEC / "results" / "verify_clean_english.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    bad = any(v["function_vs_sheet_blocks"] or v["clean_vs_sheet"] or v["clean_vs_clean_english"] or v["second_run_changes"]
              or v["joiners_lost_in_kept_lines"] for v in report["packs"].values())
    print("wrote", out.relative_to(SPEC), "|", "PROBLEMS FOUND" if bad else "all checks pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
