"""Read runnable medicines out of medicine.md files.

Convention (one per medicine section in medicine.md). Either function shape is accepted:
    def medicine(text) -> (new_text, "keep" | "fix" | "drop")
    def apply_rule(text, metadata) -> (new_text or None, dropped)   # spec v1 contract


    ## Medicine <N>: <CODE> <title>
    ...
    ```python medicine
    def medicine(text):
        ...
        return new_text, "fix"      # "keep" | "fix" | "drop"
    ```

Usage as a script (loads the blocks and lists them; runs nothing on pack data):
    python extract_medicines.py <medicine.md> [<medicine.md> ...]

Warning: loading a medicine RUNS its code. Read the blocks of other people's
files before you load them.
"""
import os, re, sys, textwrap

HEADING = re.compile(r"(?m)^## Medicine \d+:\s*(\S+)(.*)$")
BLOCK = re.compile(r"(?ms)^[ \t]*```python medicine[ \t]*\n(.*?)^[ \t]*```[ \t]*$")
VALID_ACTIONS = {"keep", "fix", "drop"}


def owner_of(path):
    """Name a file's author: the folder above medicine.md (the GitHub handle), else the file name."""
    parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
    return parent if os.path.basename(path) == "medicine.md" else os.path.splitext(os.path.basename(path))[0]


def load(path):
    """Return a list of (name, code, function, problem) for every medicine section in one file."""
    text = open(path, encoding="utf-8").read()
    who = owner_of(path)
    heads = list(HEADING.finditer(text))
    found = []
    for i, h in enumerate(heads):
        code = h.group(1).strip()
        section = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        name = f"{who}/{code}"
        m = BLOCK.search(section)
        if not m:
            found.append((name, code, None, "no ```python medicine block in this section"))
            continue
        src = textwrap.dedent(m.group(1))
        ns = {}
        try:
            exec(compile(src, f"{path}:{code}", "exec"), ns)
        except Exception as e:  # report, do not crash the whole run
            found.append((name, code, None, f"code does not run: {type(e).__name__}: {e}"))
            continue
        fn = ns.get("medicine")
        if not callable(fn) and callable(ns.get("apply_rule")):
            fn = _from_apply_rule(ns["apply_rule"])
        if not callable(fn):
            found.append((name, code, None, "block defines neither medicine(text) nor apply_rule(text, metadata)"))
            continue
        found.append((name, code, _checked(fn, name), None))
    return found


def _from_apply_rule(apply_rule):
    """Adapt the spec v1 contract apply_rule(text, metadata) -> (new_text | None, dropped)."""
    def run(text, metadata=None):
        new, dropped = apply_rule(text, metadata or {})
        if dropped:
            return text, "drop"
        new = text if new is None else new
        return new, ("fix" if new != text else "keep")
    return run


def _checked(fn, name):
    """Wrap a medicine so a wrong return shape is reported clearly."""
    def run(text):
        out = fn(text)
        if not (isinstance(out, tuple) and len(out) == 2 and isinstance(out[0], str) and out[1] in VALID_ACTIONS):
            raise ValueError(f"{name}: medicine must return (str, 'keep'|'fix'|'drop'), got {type(out).__name__}")
        return out
    return run


def load_many(paths):
    meds, problems = {}, []
    for p in paths:
        for name, code, fn, problem in load(p):
            if problem:
                problems.append(f"{name}: {problem}")
            else:
                meds[name] = (code, fn)
    return meds, problems


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    meds, problems = load_many(sys.argv[1:])
    for name, (code, _) in meds.items():
        print(f"OK       {name}")
    for p in problems:
        print(f"PROBLEM  {p}")
