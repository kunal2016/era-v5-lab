"""The lab canary string (G9). One place for the string, the stamp and the search.

Every file that holds eval items (questions, answers, prompts) carries the lab canary line.
If the canary turns up in a training document, eval data reached the training data.
canary_scan.py looks for it, and so does decontam_check.py (through fpset.Fingerprints).

The canary is plain ASCII text, not a special token (TSAI, G10 chat, 29 Oct): a special
token never comes out of normal tokenization, so leaked text would not contain it.
ASCII also keeps it the same in JSON written with ensure_ascii=True.

Do not change LAB_CANARY. Files stamped with the old string would no longer be found.
"""

from pathlib import Path

# The searched-for marker. The ID part was made once with uuid.uuid4().
LAB_CANARY = "era-v5-lab:eval:43c1a566-5d44-4c5b-96ae-b53b4188b0ec"
LAB_CANARY_ID = "era-v5-lab"
# The line written into eval files, in the style of the BIG-bench, GPQA and HLE canaries.
LAB_CANARY_LINE = ("ERA V5 LAB EVALUATION DATA. IT MUST NEVER APPEAR IN TRAINING DATA. "
                   "canary GUID " + LAB_CANARY)
MARKDOWN_LINE = f"<!-- {LAB_CANARY_LINE} -->"


def stamp(record):
    """Return a copy of a dict with the canary line as its first key."""
    return {"canary": LAB_CANARY_LINE, **{k: v for k, v in record.items() if k != "canary"}}


def load_canaries(fingerprint_dir=None):
    """Canary string -> source ID: the lab canary, plus every benchmark canary
    (fingerprints/<version>/<benchmark>/canaries.txt, for example GPQA and HLE)."""
    canaries = {LAB_CANARY: LAB_CANARY_ID}
    if fingerprint_dir:
        for f in sorted(Path(fingerprint_dir).glob("*/canaries.txt")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    canaries.setdefault(line.strip(), f.parent.name)
    return canaries


def find(text, canaries):
    """Every occurrence of every canary in text, as (offset, canary), by offset."""
    out = []
    for c in canaries:
        i = text.find(c)
        while i != -1:
            out.append((i, c))
            i = text.find(c, i + 1)
    return sorted(out)
