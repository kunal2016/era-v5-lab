"""Run the full shard check on many training shards in one command (G9).

    python check_shards.py --tokenizer <p1536>/tokenizer.json --work <dir> --shards <folder>
    python check_shards.py --tokenizer <p1536>/tokenizer.json --work <dir> --links shard_links.tsv \
        --only code-cpp-train-000000 ind-gu-fw2-train-000000
    python check_shards.py ... --compare ../results/decontam_shards.md

For each shard this runs the same chain as results/decontam_shards.md, with the scripts unchanged:
decode_shard.py (checks the shard against its manifest) -> decontam_check.py (full set: no --benchmarks, --tags or
--exclude) -> canary_scan.py. decontam_check.py and canary_scan.py run at the same time on the decoded file.

  --links    TSAI's shard_links.tsv (columns file, url). Files missing under <work>/shards are downloaded first
             (.bin, .idx.npy, .docs.parquet, .json; no quality report). decode_shard.py checks each file's sha256
             against the manifest, so a broken download fails the shard and is not counted.
  --jobs     shards checked at the same time (default 3). Peak memory is about 20 bytes per token per shard for the
             decode, plus one fingerprint set per running decontam_check.py.
  --compare  a markdown file with a shard table (shard_id, payload_sha256, docs, tokens). Each checked shard must
             match its row there; a mismatch or a missing row is reported and makes the exit code 1.

Results go to <work>/results/<shard_id>.json, one file per shard, written only when all three steps finish. A second
run skips a shard that already has a result for the same tokenizer, fingerprint set and payload (resume after a
stop). Use --force to check again. The decoded text is deleted after the checks unless --keep-text is given.

At the end it prints a markdown table in the format of results/decontam_shards.md, plus the fingerprint set_sha256
and the canary count. Exit code: 0 when every shard passed with 0 flagged and 0 canary hits and matched --compare;
1 when a shard failed a step, has a hit or does not match; 2 for a usage error. It never prints document text.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARD_EXTS = (".bin", ".idx.npy", ".docs.parquet", ".json")
SET_LINE = re.compile(r"^fingerprints (\S+) set_sha256 ([0-9a-f]{64}) \((.+)\)$", re.M)
DECONTAM_LINE = re.compile(r"^docs (\d+) flagged (\d+) ", re.M)
CANARY_COUNT = re.compile(r"^canaries (\d+) from (.+)$", re.M)
CANARY_LINE = re.compile(r"^docs (\d+) with_canary (\d+) hits (\d+)", re.M)
ROW = re.compile(r"^\|[^|]*\|\s*`?([a-z0-9-]+-\d{6})`?\s*\|\s*`?([0-9a-f]{64})`?\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|")


class CheckError(Exception):
    pass


def read_links(path):
    """{file name: url} from shard_links.tsv (lines starting with # are comments; header row 'file url')."""
    links = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2 or parts[0] == "file":
            continue
        links[parts[0]] = parts[1]
    return links


def shard_ids_from_links(links):
    ids = set()
    for name in links:
        if name.endswith(".bin"):
            ids.add(name[: -len(".bin")])
    return sorted(ids)


def download(url, dest, tries=3):
    tmp = dest.with_name(dest.name + ".part")
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            os.replace(tmp, dest)
            return
        except Exception as e:  # network error or expired link: retry, then report
            tmp.unlink(missing_ok=True)
            if attempt == tries:
                raise CheckError(f"download of {dest.name} failed: {type(e).__name__}: {e}") from None
            time.sleep(2 * attempt)


def fetch_shard(shard_id, links, shard_dir):
    for ext in SHARD_EXTS:
        name = shard_id + ext
        dest = shard_dir / name
        if dest.exists():
            continue
        if name not in links:
            raise CheckError(f"{name} is not in the links file")
        download(links[name], dest)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def check_one(shard_id, a, tok_sha):
    """Decode one shard, run both checks, return the result dict (never document text)."""
    shard_dir = a.work / "shards"
    text_dir = a.work / "text"
    bin_path = shard_dir / f"{shard_id}.bin"
    t0 = time.time()
    if a.links_map is not None:
        fetch_shard(shard_id, a.links_map, shard_dir)
    if not bin_path.exists():
        raise CheckError(f"{bin_path} not found")

    code, out, err = run([sys.executable, str(HERE / "decode_shard.py"), str(bin_path),
                          "--tokenizer", str(a.tokenizer), "--out", str(text_dir)])
    if code != 0:
        raise CheckError(f"decode_shard.py failed: {err.strip().splitlines()[0] if err.strip() else code}")
    summary = json.loads(out.strip().splitlines()[-1])
    text_path = Path(summary["out"])

    cmd_d = [sys.executable, str(HERE / "decontam_check.py"), str(text_path)]
    cmd_c = [sys.executable, str(HERE / "canary_scan.py"), str(text_path)]
    if a.fingerprints:
        cmd_d += ["--fingerprints", str(a.fingerprints)]
        cmd_c += ["--fingerprints", str(a.fingerprints)]
    with ThreadPoolExecutor(2) as ex:
        fd, fc = ex.submit(run, cmd_d), ex.submit(run, cmd_c)
        (code_d, out_d, err_d), (code_c, out_c, err_c) = fd.result(), fc.result()
    if not a.keep_text:
        text_path.unlink(missing_ok=True)

    m_set, m_dec = SET_LINE.search(err_d), DECONTAM_LINE.search(err_d)
    if code_d != 0 or not m_set or not m_dec:
        raise CheckError(f"decontam_check.py failed (exit {code_d}): {err_d.strip()[-300:]}")
    m_cc, m_can = CANARY_COUNT.search(err_c), CANARY_LINE.search(err_c)
    if code_c not in (0, 1) or not m_cc or not m_can:  # 1 = hits (counted below), 2 = a file was skipped
        raise CheckError(f"canary_scan.py failed (exit {code_c}): {err_c.strip()[-300:]}")
    if int(m_dec.group(1)) != summary["docs"] or int(m_can.group(1)) != summary["docs"]:
        raise CheckError(f"document counts differ: decode {summary['docs']}, decontam {m_dec.group(1)}, "
                         f"canary {m_can.group(1)}")

    flagged_ids = [json.loads(line)["doc_id"] for line in out_d.splitlines() if line.strip()]
    canary_hits = [json.loads(line) for line in out_c.splitlines() if line.strip()]
    return {
        "shard_id": shard_id,
        "payload_sha256": summary["payload_sha256"],
        "docs": summary["docs"],
        "tokens": summary["tokens"],
        "dataset_version": summary["dataset_version"],
        "split": summary["split"],
        "tokenizer_sha256": tok_sha,
        "fingerprints_version": m_set.group(1),
        "set_sha256": m_set.group(2),
        "scope": m_set.group(3),
        "flagged": int(m_dec.group(2)),
        "flagged_doc_ids": flagged_ids,
        "canaries_checked": int(m_cc.group(1)),
        "canary_hits": int(m_can.group(3)),
        "canary_hit_list": [{"canary": h["canary"], "doc_id": h["doc_id"], "offset": h["offset"]} for h in canary_hits],
        "seconds": round(time.time() - t0, 1),
    }


def read_reference(path):
    """{shard_id: (payload_sha256, docs, tokens)} from the rows of a markdown shard table."""
    ref = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            ref.setdefault(m.group(1), (m.group(2), int(m.group(3).replace(",", "")),
                                        int(m.group(4).replace(",", ""))))
    return ref


def compare(result, ref):
    """List of mismatch strings (empty when the shard matches its row)."""
    row = ref.get(result["shard_id"])
    if row is None:
        return ["no row in the --compare file"]
    issues = []
    for name, want, got in (("payload_sha256", row[0], result["payload_sha256"]),
                            ("docs", row[1], result["docs"]), ("tokens", row[2], result["tokens"])):
        if want != got:
            issues.append(f"{name} {got} != {want}")
    return issues


def table(results, ref):
    lines = ["| # | shard_id | payload_sha256 | docs | tokens | flagged | canary hits |"
             + (" matches --compare |" if ref is not None else ""),
             "|---:|---|---|---:|---:|---:|---:|" + ("---|" if ref is not None else "")]
    for n, r in enumerate(results, 1):
        line = (f"| {n} | `{r['shard_id']}` | `{r['payload_sha256']}` | {r['docs']:,} | {r['tokens']:,} | "
                f"{r['flagged']} | {r['canary_hits']} |")
        if ref is not None:
            issues = compare(r, ref)
            line += " yes |" if not issues else f" NO: {'; '.join(issues)} |"
        lines.append(line)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizer", type=Path, required=True, help="the frozen tokenizer.json the shards name")
    ap.add_argument("--work", type=Path, required=True,
                    help="work folder: shards/, text/ (deleted after use) and results/ (holds text while running: "
                         "never commit it)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--shards", type=Path, help="a folder with the shard files (all four per shard)")
    src.add_argument("--links", type=Path, help="TSAI's shard_links.tsv: download missing files to <work>/shards")
    ap.add_argument("--only", nargs="+", metavar="SHARD_ID", help="check only these shards")
    ap.add_argument("--fingerprints", type=Path, help="fingerprint set folder (default: the scripts' default, v2)")
    ap.add_argument("--jobs", type=int, default=3, help="shards at the same time (default 3)")
    ap.add_argument("--compare", type=Path, help="markdown shard table to check payload_sha256, docs and tokens")
    ap.add_argument("--keep-text", action="store_true", help="keep <work>/text/<shard_id>.text.parquet")
    ap.add_argument("--force", action="store_true", help="check again shards that already have a result")
    a = ap.parse_args(argv)

    if a.jobs < 1:
        ap.error("--jobs must be 1 or more")
    if not a.tokenizer.is_file():
        ap.error(f"{a.tokenizer} not found")
    tok_sha = sha256_file(a.tokenizer)
    for sub in ("shards", "text", "results"):
        (a.work / sub).mkdir(parents=True, exist_ok=True)

    a.links_map = None
    if a.links:
        a.links_map = read_links(a.links)
        ids = shard_ids_from_links(a.links_map)
    else:
        if a.shards.resolve() != (a.work / "shards").resolve():
            for ext in SHARD_EXTS:  # link the given folder's files into <work>/shards, no copy
                for f in a.shards.glob(f"*{ext}"):
                    dest = a.work / "shards" / f.name
                    if not dest.exists():
                        dest.symlink_to(f.resolve())
        ids = sorted(p.name[: -len(".bin")] for p in (a.work / "shards").glob("*.bin"))
    if a.only:
        missing = sorted(set(a.only) - set(ids))
        if missing:
            ap.error(f"not found: {' '.join(missing)}")
        ids = [i for i in ids if i in set(a.only)]
    if not ids:
        ap.error("no shards to check")
    ref = read_reference(a.compare) if a.compare else None

    def result_path(shard_id):
        return a.work / "results" / f"{shard_id}.json"

    def task(shard_id):
        rp = result_path(shard_id)
        if rp.exists() and not a.force:
            old = json.loads(rp.read_text())
            if old.get("tokenizer_sha256") == tok_sha:
                print(f"{shard_id}: result kept from an earlier run (use --force to check again)", file=sys.stderr)
                return old
        try:
            r = check_one(shard_id, a, tok_sha)
        except CheckError as e:
            print(f"{shard_id}: FAILED: {e}", file=sys.stderr)
            return None
        tmp = rp.with_name(rp.name + ".tmp")
        tmp.write_text(json.dumps(r, indent=1) + "\n")
        os.replace(tmp, rp)
        print(f"{shard_id}: docs {r['docs']} tokens {r['tokens']} flagged {r['flagged']} "
              f"canary hits {r['canary_hits']} ({r['seconds']} s)", file=sys.stderr)
        return r

    t0 = time.time()
    with ThreadPoolExecutor(a.jobs) as ex:
        out = list(ex.map(task, ids))
    results = [r for r in out if r is not None]
    failed = [i for i, r in zip(ids, out) if r is None]

    print(table(results, ref))
    sets = sorted({(r["fingerprints_version"], r["set_sha256"], r["scope"]) for r in results})
    for version, sha, scope in sets:
        print(f"\nFingerprint set: {version}, set_sha256 `{sha}`, scope `{scope}`")
    canaries = sorted({r["canaries_checked"] for r in results})
    print(f"Canaries checked per shard: {', '.join(map(str, canaries))}")
    print(f"Tokenizer sha256: `{tok_sha}`")
    total_docs = sum(r["docs"] for r in results)
    total_tokens = sum(r["tokens"] for r in results)
    print(f"Total: {len(results)} shards, {total_docs:,} docs, {total_tokens:,} tokens, "
          f"{sum(r['flagged'] for r in results)} flagged, {sum(r['canary_hits'] for r in results)} canary hits")
    print(f"checked {len(results)} of {len(ids)} shard(s) in {time.time() - t0:.0f} s"
          + (f"; FAILED: {' '.join(failed)}" if failed else ""), file=sys.stderr)

    bad = bool(failed) or len(sets) > 1
    bad |= any(r["flagged"] or r["canary_hits"] for r in results)
    bad |= ref is not None and any(compare(r, ref) for r in results)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
