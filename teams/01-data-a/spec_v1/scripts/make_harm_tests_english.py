"""Run each function of ../clean_english.py, and each English medicine, on each English gold set with the team's harm_test.py,
and write ../harm_tests_english.md. The English counterpart of ../../tools/make_harm_tests.py, which writes ../harm_tests.md.

  python -I make_harm_tests_english.py <g1-harm-test checkout> <packs dir> <gold dir with the disputed docs left in>

harm_test.py is run as it is, never changed. Five runs per pack, reports in ../results/ (IDs and digests only):
  clean_<pack>_harm.json           ../clean_english.py --rule all, official gold: each function, then ALL IN ORDER in RULES order
  clean_stress_<pack>_harm.json    the same, with the disputed docs left in
  clean_english_<pack>_harm.json   clean_english.py --rule all, official gold: its RULES order is the sheet's order
  <pack>_harm.json                 ../medicine_english.md --rule all, official gold: each medicine, then the sheet
  stress_<pack>_harm.json          the same, with the disputed docs left in
Section 5 of harm_tests_english.md comes from ../results/verify_clean_english.json: run verify_clean_english.py first.
"""
import csv
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE.parent
CHECKOUT, PACKS_DIR, STRESS = (Path(a).resolve() for a in sys.argv[1:4])
TEAM = CHECKOUT / "teams" / "01-data-a"
HARM = TEAM / "tools" / "harm_test.py"
CLEAN, ENGLISH, SHEET = SPEC / "clean_english.py", HERE / "clean_english.py", SPEC / "medicine_english.md"
OUT = SPEC / "results"
PACKS = ["en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"]
SHORT = {"en-dclm": "dclm", "en-fineweb-edu": "fineweb-edu", "en-nemotroncc": "nemotroncc", "en-nemotroncc-synth": "synth"}
IN_REPO = {CLEAN: "teams/01-data-a/spec_v1/clean_english.py", ENGLISH: "teams/01-data-a/spec_v1/scripts/clean_english.py",
           SHEET: "teams/01-data-a/spec_v1/medicine_english.md"}


def gold_rows(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def harm(pack, rules, gold, report):
    if not gold_rows(gold):
        return None  # harm_test.py says NOT TESTABLE (exit code 2) and writes no report
    report.unlink(missing_ok=True)
    r = subprocess.run([sys.executable, "-I", str(HARM), "--pack", str(PACKS_DIR / f"{pack}.parquet"), "--gold", str(gold),
                        "--rules", str(rules), "--rule", "all", "--report", str(report)], capture_output=True, text=True)
    if not report.exists():
        sys.exit(f"harm_test.py could not run {rules.name} on {pack}: {(r.stderr or r.stdout).strip()}")
    d = json.loads(report.read_text(encoding="utf-8"))
    d["rules"] = IN_REPO[rules]  # the path it has in the repo, not this machine's
    report.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8", newline="\n")
    return d


def res(rep, name):
    return next(x for x in rep["results"] if x["rule"] == name)


def cell(rep, name):
    """As ../harm_tests.md: changed + dropped, and the result only when it is not a PASS."""
    if rep is None:
        return "NOT TESTABLE"
    r = res(rep, name)
    return f"{r['changed'] + r['dropped']}" + ("" if r["result"] == "PASS" else f" **{r['result']}**")


def ids(rep, name):
    return [i for i in res(rep, name)["affected_ids"]]


def main():
    ver = json.loads((OUT / "verify_clean_english.json").read_text(encoding="utf-8"))
    fn, fn_s, en, sh, sh_s = {}, {}, {}, {}, {}
    for p in PACKS:
        gold, stress = TEAM / "gold" / f"{p}_gold.csv", STRESS / f"{p}_gold.csv"
        fn[p] = harm(p, CLEAN, gold, OUT / f"clean_{p}_harm.json")
        fn_s[p] = harm(p, CLEAN, stress, OUT / f"clean_stress_{p}_harm.json")
        en[p] = harm(p, ENGLISH, gold, OUT / f"clean_english_{p}_harm.json")
        sh[p] = harm(p, SHEET, gold, OUT / f"{p}_harm.json")
        sh_s[p] = harm(p, SHEET, stress, OUT / f"stress_{p}_harm.json")
        print(p, " ".join(f"{k} {v['status']}" for k, v in (("spec_v1/clean_english.py", fn[p]), ("stress", fn_s[p]), ("scripts/clean_english.py", en[p]),
                                                           ("sheet", sh[p]), ("sheet-stress", sh_s[p]))))
    sys.path.insert(0, str(HERE))
    import clean_english as e
    by_code = {}
    for f in e._PIPELINES["english"]:
        rid = "DA-" + f.__name__[len("_english_"):].upper().replace("_", "-")
        by_code.setdefault(rid.split("-")[1], []).append(rid)
    english_codes = list(by_code)
    rule_ids = [rid for v in by_code.values() for rid in v]
    head = "| {} | " + " | ".join(SHORT[p] for p in PACKS) + " |"
    rule = "|---|" + "---:|" * len(PACKS)
    goldrow = lambda runs: "| gold docs (limit) | " + " | ".join("0: NOT TESTABLE" if runs[p] is None else
                                                                f"{runs[p]['gold_count']} ({runs[p]['limit_documents']})" for p in PACKS) + " |"
    funcs = [c for c in (r["rule"] for r in fn[PACKS[0]]["results"]) if c in english_codes or c == "ALL IN ORDER"]
    o = ["# Spec v1 harm tests: English", "",
         "DRAFT. Each cell: gold docs changed + dropped, for that function or medicine on that pack's gold set. Limit: "
         "`max(1, floor(1% of gold))`, that is `max(1 document, 1%)` (TSAI decision); each pack on its own gold set, never pooled; "
         "an empty gold set is NOT TESTABLE (exit code 2), never a PASS. A result other than PASS is shown after the count. "
         f"Made by `scripts/make_harm_tests_english.py` on {date.today():%d %b %Y} with the team's `harm_test.py`, run as it is "
         f"(sha256 `{hashlib.sha256(HARM.read_bytes()).hexdigest()[:12]}`, `g1-harm-test` at `bae5163`, the same file as PR 140's head). "
         "The code packs are in `harm_tests.md`.", "",
         "## 1. Each function of clean_english.py on the English packs", "",
         f"`clean_english.py`: the code and English sheets, as `tools/build_clean.py` builds them (`clean.py` holds the code sheet only). The {len(english_codes)} functions with English rules; "
         "the other functions hold code rules only, which keep every English document (section 5).", "",
         head.format("function"), rule, goldrow(fn)]
    o += [f"| {c} | " + " | ".join(cell(fn[p], c) for p in PACKS) + " |" for c in funcs]
    o += ["", "`ALL IN ORDER` is `harm_test.py` running every function of `clean_english.py` one after another, in `RULES` order. "
          "Section 5 shows whether that gives the same as `clean()`, which runs the English rules in the sheet's order and F1 last.", "",
          "## 2. The same, with the disputed docs left in the gold sets", "", head.format("function"), rule, goldrow(fn_s)]
    o += [f"| {c} | " + " | ".join(cell(fn_s[p], c) for p in PACKS) + " |" for c in funcs]
    o += ["", "## 3. Each medicine on its own, on the English packs", "",
          "`medicine_english.md --rule all`: each of the 20 medicines alone, then the whole sheet in its order.", "",
          "| medicine | function | " + " | ".join(SHORT[p] for p in PACKS) + " | with the disputed docs left in |",
          "|---|---|" + "---:|" * len(PACKS) + "---|",
          "| gold docs (limit) | | " + " | ".join(f"{sh[p]['gold_count']} ({sh[p]['limit_documents']})" for p in PACKS) + " | "
          + ", ".join(f"{SHORT[p]} {sh_s[p]['gold_count']} ({sh_s[p]['limit_documents']})" for p in PACKS) + " |"]
    for rid in rule_ids + ["ALL IN ORDER"]:
        o.append(f"| {'`' + rid + '`' if rid != 'ALL IN ORDER' else 'ALL IN ORDER'} | {rid.split('-')[1] if rid != 'ALL IN ORDER' else 'the sheet'} | "
                 + " | ".join(cell(sh[p], rid) for p in PACKS) + " | " + ", ".join(cell(sh_s[p], rid) for p in PACKS) + " |")
    o += ["", "## 4. scripts/clean_english.py, the English cleaner on its own", "",
          "`scripts/clean_english.py --rule all`. Its `RULES` follow the sheet's order, so its `ALL IN ORDER` is `clean()`.", "",
          head.format("function"), rule, goldrow(en)]
    o += [f"| {c} | " + " | ".join(cell(en[p], c) for p in PACKS) + " |" for c in [r["rule"] for r in en[PACKS[0]]["results"]]]
    pk = ver["packs"]
    vcell = lambda v: "0" if not v else f"**{len(v)}** ({', '.join(f'`{i}`' for i in v[:3])})"
    o += ["", "## 5. Checks on every document of the English packs", "",
          "From `scripts/verify_clean_english.py` (`results/verify_clean_english.json`). Each cell: documents where the check fails.", "",
          head.format("check"), rule,
          "| documents | " + " | ".join(str(pk[p]["docs"]) for p in PACKS) + " |",
          "| a `clean_english.py` function differs from its English medicines run in order (a code function must keep) | "
          + " | ".join(vcell([i for v in pk[p]["function_vs_sheet_blocks"].values() for i in v]) for p in PACKS) + " |",
          "| `clean()` differs from the sheet run in order | " + " | ".join(vcell(pk[p]["clean_vs_sheet"]) for p in PACKS) + " |",
          "| `clean_english.py` and `scripts/clean_english.py` differ | " + " | ".join(vcell(pk[p]["clean_vs_clean_english"]) for p in PACKS) + " |",
          "| `ALL IN ORDER` of `clean_english.py` (RULES order) differs from `clean()` | " + " | ".join(vcell(pk[p]["all_in_order_vs_clean"]) for p in PACKS) + " |",
          "| `ALL IN ORDER` of `scripts/clean_english.py` differs from `clean()` | " + " | ".join(vcell(pk[p]["clean_english_all_in_order_vs_clean"]) for p in PACKS) + " |",
          "| a second `clean()` changes the text again | " + " | ".join(vcell(pk[p]["second_run_changes"]) for p in PACKS) + " |",
          "| documents with a ZWJ or ZWNJ | " + " | ".join(str(pk[p]["docs_with_joiners"]) for p in PACKS) + " |",
          "| a ZWJ or ZWNJ deleted on its own | " + " | ".join(vcell(pk[p]["joiners_lost_in_kept_lines"]) for p in PACKS) + " |"]
    f1_path = OUT / "f1_eval_english.json"
    if f1_path.exists():  # made by f1_eval_english.py, the English counterpart of tools/f1_eval.py
        f1 = json.loads(f1_path.read_text(encoding="utf-8"))
        o += ["", "## 6. F1 on the English packs", "",
              "From `scripts/f1_eval_english.py` (`results/f1_eval_english.json`). `DA-F1-005` is the F1 that `clean_english.py` runs on English; the "
              "shared `tools/f1_rule.py` is switched on for `en` and `eng` in memory only, to show what that would do. Each cell: docs F1 "
              "changes or drops after the other English rules, then the gold docs among them.", "",
              head.format("F1 rule"), rule]
        for name in ("DA-F1-005", "shared F1 (in memory)"):
            o.append(f"| {name} | " + " | ".join(
                f"{f1['real'][p][name]['fixed'] + f1['real'][p][name]['dropped']}, gold {len(f1['real'][p][name]['gold_touched'])}"
                + ("" if len(f1['real'][p][name]['gold_touched']) <= f1['real'][p][name]['limit'] else " **over**") for p in PACKS) + " |")
        o += ["", "A second `clean()` leaves every F1 tag as it is: " + ", ".join(
            f"{SHORT[p]} {len(f1['second_run'][p]['changed_again'])} of {f1['second_run'][p]['docs_with_new_tags']}" for p in PACKS)
            + " docs change again. Planted made-up values: `decisions_english.md`, F1."]
    touched = {(p, k): ids(r[p], "ALL IN ORDER") for k, r in (("official", fn), ("stress", fn_s)) for p in PACKS}
    o += ["", "## Gold docs touched", "",
          "| pack | official gold | with the disputed docs left in |", "|---|---|---|"]
    o += [f"| {SHORT[p]} | {', '.join(f'`{i}`' for i in touched[(p, 'official')]) or '-'} | "
          f"{', '.join(f'`{i}`' for i in touched[(p, 'stress')]) or '-'} |" for p in PACKS]
    o += ["", "Affected gold IDs are in `results/clean_<pack>_harm.json`, `results/clean_stress_<pack>_harm.json` and "
          "`results/<pack>_harm.json`. No document text is kept.", "",
          "## Not run", "", "| family | pack | gold docs | why |", "|---|---|---:|---|"]
    not_run = [(SHORT[p], p) for p in PACKS if fn[p] is None]
    o += [f"| English | {p} | 0 | gold set is empty: NOT TESTABLE |" for _, p in not_run] or ["| - | - | - | every English pack ran |"]
    runs = [r for d in (fn, fn_s, en, sh, sh_s) for r in d.values() if r]
    passed = sum(r["status"] == "PASS" for r in runs)
    o += ["", f"Overall: {passed} of {len(runs)} runs PASS" + ("." if passed == len(runs) else f", {len(runs) - passed} not.")]
    (SPEC / "harm_tests_english.md").write_text("\n".join(o) + "\n", encoding="utf-8", newline="\n")
    print("wrote harm_tests_english.md |", f"{passed}/{len(runs)} PASS")


if __name__ == "__main__":
    main()
