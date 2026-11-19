# Spec v1.2 proposal — G5 Emptied by cleaning (`DA-G5-001`), from dedup's `empty_documents.csv`

**From:** Kunal Sinha (Data A dedup), for task 8 (Aneesha Das's spec v1.2 collation). **Status:** PROPOSED; needs the
team's agreement, an entry in `diagnosis/DISEASES.md` and in the build's `CODE_ORDER`.

## 1. Disease

**G5 — Emptied by cleaning** (group G, damage from earlier cleaning; next free code after G1–G4). A cleaning fix removes
everything a document had, and the row is kept with empty or whitespace-only text instead of being dropped.

**Found by dedup, not by reading.** `overlap.py` scores documents by word 5-gram shingles, and these documents have none.
`dedup.py` lists them in `empty_documents.csv` and sets aside the matches between them, so they are never removed as
duplicates of each other (`README_dedup.md`). Both cleanings had the same 7, all code, all train:

| pack | part | row_in_part | doc_id | text after cleaning |
|---|---|---:|---|---|
| code-cpp | code-cpp/part-00001.parquet | 1499 | `79fa36f8339f9ebd` | empty |
| code-java | code-java/part-00000.parquet | 42665 | `d5d0b4192775579c` | 1 whitespace character |
| code-java | code-java/part-00000.parquet | 45786 | `4a67489226159c57` | empty |
| code-java | code-java/part-00001.parquet | 5993 | `8a07c8e5f95eee27` | 1 whitespace character |
| code-java | code-java/part-00001.parquet | 21846 | `91f4b8de1c11bf4b` | 1 whitespace character |
| code-js-ts | code-js-ts/part-00000.parquet | 12129 | `a2ffa5d828d9e9ab` | empty |
| code-js-ts | code-js-ts/part-00000.parquet | 56860 | `fff1410ec5527f29` | empty |

Sources: `empty_documents.csv` of the 5 Nov run and of TSAI's dedup run #547 on the #244 cleaning (identical, 7 rows);
lengths checked on the local 5 Nov cleaned parts. 7 of 1,414,996 documents (0.0005%).

**Why it happens.** In `spec_v1_1/clean.py`, the shared wrapper `_std` drops a rule's empty result ("An empty result is
a drop"), but not every rule goes through it: the code rules return `("fix", new)` directly (for example `DA-E4-005`,
licence headers), and `_run` passes any fixed text on, empty or not. All 7 are code files, so the likely cause is a
code rule that removed the whole file (a file that was only a licence header or only comments). **To confirm:** run the
7 raw documents through `clean.py` rule by rule and record which rule emptied each one.

**Harm of leaving it.** An empty row is counted as a kept document in the cleaning reports and the ledger, goes into the
shards as a zero-token document, and has to be special-cased by dedup (`empty_documents.csv`).

## 2. Medicine

Drop a document whose text is empty or whitespace-only **after all of its family's rules**, as the last step before F1.
One check in `_run` covers every rule, including ones added later:

```python
RULE_ID = "DA-G5-001"
CODE = "G5"  # proposed new code: emptied by cleaning (group G)
ACTION = "drop"
STAGE = "99"  # last, after every fix of the family, before the shared F1
STATUS = "PROPOSED"
ORIGIN = "code-cpp, code-java, code-js-ts"  # packs where dedup found it
PACKS = "every pack"  # a guard: an empty document carries nothing, in any family
SOURCE = "dedup empty_documents.csv (5 Nov run; #547)"
AUTHOR = "kunal2016"


def _run(doc, *factories):
    """Run the rules in order: a drop ends the document, a fix passes its text on. A rule runs only on the packs SCOPE gives it.
    G5: a document that the rules leave empty or whitespace-only is dropped, never kept as a fix."""
    d = dict(doc)
    for make in factories:
        if doc.get("pack_id") not in SCOPE[_ID[make]]:
            continue
        action, text = make()(d)
        if action == "drop":
            return ("drop", doc["text"])
        d["text"] = text
    if not d["text"].strip():                    # DA-G5-001
        return ("drop", doc["text"])
    return ("fix" if d["text"] != doc["text"] else "keep", d["text"])
```

A document that was already empty in the raw data is dropped too (it carries nothing); the cleaning report should count
those separately from documents emptied by a rule.

## 3. Harm test and checks

- **Gold harm:** 0 expected on every gold set — a gold (reviewed clean) document is never empty. Run `harm_test.py` on
  all real gold sets as for every rule; any gold document dropped by G5 means a rule upstream is wrong.
- **Unit tests:** `""`, `"\n"`, `"  \t\n"` → drop; `"x"` → keep; a code file that is only a licence header, cleaned by
  `DA-E4-005`, → drop; a file with a licence header and code → fix, not drop.
- **On the sample:** exactly the 7 documents above are dropped (5 Nov and #244 cleanings); no other document changes,
  so every other output of `clean.py` is byte-identical.
- **Dedup afterwards:** the next overlap and dedup run should list 0 rows in `empty_documents.csv`; dedup keeps the
  listing as a check.

## 4. Spec v1.2 entry (short form for the collation)

| code | disease | family | packs (docs) | rule ID | action, stage | medicine |
|---|---|---|---|---|---|---|
| **G5** | Emptied by cleaning: a fix leaves empty or whitespace-only text and the row is kept | code (found); guard for all | code-cpp (1), code-java (4), code-js-ts (2) | `DA-G5-001` | drop, last (99) | written; tests and harm run to do |
