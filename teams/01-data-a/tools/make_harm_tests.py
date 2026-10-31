"""Task 4: run each clean.py function on each gold set with the team's harm_test.py, and write spec_v1/harm_tests.md.

  python make_harm_tests.py <checkout> <packs dir>

A pack with no file in <packs dir> is listed as not run. Reports are IDs and digests only.
"""
import csv, json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1] / "spec_v1"
WT, PACKS = Path(sys.argv[1]), Path(sys.argv[2])
TEAM = WT / "teams" / "01-data-a"
CLEAN = HERE / "clean.py"
OUT = HERE / "results"; OUT.mkdir(exist_ok=True)
FAMILIES = {"code": ["code-go", "code-rust", "code-js-ts", "code-java", "code-cpp", "code-python"],
            "English": ["en-dclm", "en-fineweb-edu", "en-nemotroncc", "en-nemotroncc-synth"], "math": ["math-finemath", "math-megamath"], "science": ["sci-finepdfs"]}
lines = ["# Spec v1 harm tests", "",
         "DRAFT. Each cell: gold docs changed + dropped, for that function on that pack's gold set. Limit: `max(1, floor(1% of gold))`. Made by `tools/make_harm_tests.py` with the team's `harm_test.py`.", ""]
ran, missing = {}, []
for fam, packs in FAMILIES.items():
    for pack in packs:
        gold = TEAM / "gold" / f"{pack}_gold.csv"; n = sum(1 for _ in csv.DictReader(open(gold, encoding="utf-8"))) if gold.exists() else 0
        parquet = PACKS / f"{pack}.parquet"
        if not parquet.exists() or not n:
            missing.append((fam, pack, n, "gold set is empty: NOT TESTABLE" if not n else "pack not on this machine: NOT RUN")); continue
        report = OUT / f"clean_{pack}_harm.json"
        rc = subprocess.run([sys.executable, str(TEAM / "tools" / "harm_test.py"), "--pack", str(parquet), "--gold", str(gold), "--rules", str(CLEAN), "--rule", "all", "--report", str(report)], capture_output=True, text=True)
        d = json.loads(report.read_text(encoding="utf-8")); d["rules"] = "teams/01-data-a/spec_v1/clean.py"
        report.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8", newline="\n")
        ran[pack] = d
packs = list(ran); codes = [r["rule"] for r in next(iter(ran.values()))["results"]]
lines += ["| function | " + " | ".join(p.replace("code-", "") for p in packs) + " |", "|---|" + "---:|" * len(packs)]
lines.append("| gold docs (limit) | " + " | ".join(f"{ran[p]['gold_count']} ({ran[p]['limit_documents']})" for p in packs) + " |")
for code in codes:
    cells = []
    for p in packs:
        r = next(x for x in ran[p]["results"] if x["rule"] == code)
        cells.append(f"{r['changed'] + r['dropped']}" + ("" if r["result"] == "PASS" else f" **{r['result']}**"))
    lines.append(f"| {code} | " + " | ".join(cells) + " |")
lines += ["", "Affected gold IDs are in `results/clean_<pack>_harm.json`. No document text is kept.", "", "## Not run", "", "| family | pack | gold docs | why |", "|---|---|---:|---|"]
lines += [f"| {f} | {p} | {n} | {w} |" for f, p, n, w in missing]
(HERE / "harm_tests.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
for p in packs: print(p, ran[p]["status"], [(r["rule"], r["changed"], r["dropped"], r["errors"]) for r in ran[p]["results"] if r["changed"] or r["dropped"] or r["errors"]])
print("not run:", [m[1] for m in missing])
