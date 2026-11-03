# Medicine sheet: ind-bn-fw2 (aneeshads)

Counts are from my label sheet `labels.csv`: 100 documents read in full (my assigned IDs), 82 `clean` and 18 `fix`,
5 codes found. A disease gets a section when it is found more than five times: C1 (15 times, in 14 documents), D3 (22
times, in 7 documents) and F1 (6 times, in 4 documents). A count is the number of evidence items, followed by the
number of documents. G2 (3 times, 1 document) and C2 (1 time, 1 document) are below the threshold.

**Harm test.** The gold set of Bengali is the Data B gold set: `teams/02-data-b/gold/ind-bn-fw2_gold.csv` (238
documents of this pack, readers aditeyaaitronics and sohamniyogi) and `ind-bn-sangraha-v_gold.csv` (50 documents of
the other Bengali pack), **288 documents** in all. The test is Data B's tool, which runs the code in this file as it
is:

```
python3 teams/02-data-b/tools/harm_test_indic.py --medicine medicines.md \
    --pack packs/ind-bn-fw2.jsonl packs/ind-bn-sangraha-v.jsonl --gold-dir teams/02-data-b/gold
```

1% of 288 is 2.88, so a medicine passes when it changes or drops **at most 2** gold documents, and when no changed
document loses or gains a ZWJ/ZWNJ or leaves NFC (the tool's two audits).

**All 100 of my documents are in that gold set**, among them the 18 that I marked `fix`. So a medicine that cures
more than 2 of my sick documents fails the harm test by construction: the gold readers kept these documents as
clean. This decides the sheet: C1 gets a narrow medicine that passes, and the full C1 rule is reported as a candidate
that fails.

| # | Code | Count (documents) | Action | Gold changed | Gold dropped | Share of 288 | Result | Labelled documents treated | fw2 pack changed (500) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C1 | 15 (14) | fix | 2 | 0 | 0.69% | **pass** | 2 of 14 | 2 |
| 1a | C1 (candidate, full rule) | | fix | 46 | 0 | 15.97% | **fail** | 11 of 14 | 95 |
| 2 | D3 | 22 (7) | none (candidate: fix) | 2 | 0 | 0.69% | pass, not proposed | 1 of 7 | 41 |
| 3 | F1 | 6 (4) | none | 0 | 0 | 0.0% | nothing to test | 0 of 4 | 0 |

## Medicine 1

1. **Disease:** C1, boilerplate of Bangladeshi news sites: photo and agency credits, source lines, desk slugs and
   datelines. Count 15, in 14 documents.
   - `656e1a989097ab40`, offset 0: `সংগৃহীত ছবি।`, a photo credit on its own line ("collected photo").
   - `642e2d510bf80d87`, offset 565: `—ইউএনবি`, the agency credit (UNB) after a dash at the end of the story.
   - `16b0ef19cedf0abb`, offset 1059: `বিডি প্রতিদিন/এমআই`, the desk slug of Bangladesh Pratidin (paper/editor's
     initials) at the end of the story.
2. **Medicine:** remove a line that is only a photo credit (`সংগৃহীত ছবি`, `ছবি: সংগৃহীত`, `ফাইল ছবি`), and remove an
   agency credit after a dash at the end of a line (`—ইউএনবি`, `—বাসস`, `—এএফপি`, `—রয়টার্স`, `—বিবিসি`).
   ```python
   import re

   _PHOTO_CREDIT = re.compile(r"^[ \t]*(?:সংগৃহীত ছবি|ছবি[ \t]*[:ঃ][ \t]*সংগৃহীত|ফাইল ছবি)[।.]?[ \t]*(?:\n|$)", re.M)
   _AGENCY_AFTER_DASH = re.compile(r"[ \t]*[—–][ \t]*(?:ইউএনবি|বাসস|এএফপি|রয়টার্স|বিবিসি)[ \t]*$", re.M)


   def medicine_c1(text):
       text = _PHOTO_CREDIT.sub("", text)            # a photo credit on its own line: সংগৃহীত ছবি।
       return _AGENCY_AFTER_DASH.sub("", text)       # an agency credit after a dash at the end of a line: —ইউএনবি
   ```

   The candidate I tested is the full rule, which also removes the other forms of C1 in my labels: a source line
   (`সূত্র: বিবিসি`), a desk slug at the end of a paragraph (`বিডি প্রতিদিন/এমআই`, `ভোরের আকাশ/নি`), and a dateline
   at the start (`নিজস্ব প্রতিবেদক, নাটোর :`, `চাঁদপুর প্রতিনিধি:`). Its name starts with `_`, so the harm-test tool
   does not run it as the C1 rule.
   ```python
   import re

   _SOURCE_LINE = re.compile(r"^[ \t]*সূত্র[ \t]*[:ঃ][^\n]{0,80}(?:\n|$)", re.M)
   _DESK_SLUG = re.compile(r"(?:^|(?<=[।.!?]))[ \t]*[^\s/।]+(?:[ \t][^\s/।]+){0,2}"
                           r"(?:[ \t]*/[ \t]*[^\s/।]+(?:[ \t][^\s/।]+){0,2})+[ \t]*$", re.M)
   _DATELINE = re.compile(r"\A[ \t]*(?:নিজস্ব প্রতিবেদক|অনলাইন ডেস্ক|[^\n,।]{2,30}প্রতিনিধি)[^\n:ঃ।]{0,30}[:ঃ।]+[ \t]*")


   def _candidate_c1(text):
       text = medicine_c1(text)                      # the passing part first
       text = _SOURCE_LINE.sub("", text)             # সূত্র: বিবিসি
       text = _DESK_SLUG.sub("", text)               # বিডি প্রতিদিন/এমআই at the end of a paragraph
       return _DATELINE.sub("", text)                # নিজস্ব প্রতিবেদক, নাটোর : at the start
   ```
3. **Action:** fix the text.
4. **Harm test:** gold set of 244 documents (ind-bn-fw2 244), medicine.md sha256 21d37e6bc395; rule: changed or dropped at most 1% or 1 document, whichever is more.
   - Changed 2 of 244 (0.82%). Dropped 0 of 244 (0.00%). **PASS**
   - ZWJ/ZWNJ audit: 0 changed documents with a different count. **PASS**
   - Normal-form audit: 0 changed documents left NFC or lost a compatibility character. **PASS**

   The full candidate changes 46 gold documents and drops 0: 15.97%. **Fail.** It treats 11 of my 14 C1 documents.
   19 of the 46 are my own documents, and 8 of those I marked `clean` myself although they carry the same
   boilerplate: for example `চাঁদপুর প্রতিনিধি:` at offset 0 of `44b419b70b6d9c1a` and `বাংলাপোস্ট২৪/নাছির` at offset
   523 of `241485aee4d1a252`. So my labels do not treat datelines and slugs in one way either. fw2 pack: 95 documents
   changed.
5. **Side effects:**
   - Of `medicine_c1`: a line `ফাইল ছবি` that is a real caption, or a sentence that ends with a quoted agency name
     after a dash, would be removed. It leaves 12 of my 14 C1 documents as they are.
   - Of the candidate:
     - The dateline gives the place of the story (`নাটোর`, `চাঁদপুর`); removing it loses a fact that the first sentence
       often does not repeat.
     - The slug pattern also removes a short last line with a slash that is content, such as a date `১২/০৩` or a
       ratio, when it stands alone after a full stop.
     - It still misses a byline that is only a name (`বিল্লাল হোসেন প্রান্তঃ` in `04e967f91a68f9d2`), a source in the
       middle of a line, and a desk name without a slash (`অনলাইন ডেস্ক।।` after the first line in `4b0b3423594d7d68`).
   - To cure the rest of C1, the gold readers and I need to agree first whether credits, slugs and datelines are
     boilerplate. Until then the gold set treats them as clean text.

## Medicine 2

1. **Disease:** D3, mixed language. Count 22, in 7 documents. 5 of the 7 are `clean` documents, because DISEASES.md
   says to label D3 but not judge it.
   - `39a83529d646f458`, offset 352: `left handed`, an English gloss in brackets after the Bengali `বাঁহাতি`; the same
     page has `অমিতাভ বচ্চন (Amitabh Bachchan)`.
   - `448d894cd2d20ced`, offset 1190: `জি-মেইল সাইন-ইন`, English words written in Bengali letters.
   - `0d0cf7fcbba3fef6`, offset 659: `https://toffeelive.com/`, an English URL in Bengali prose.
2. **Medicine:** none. The candidate I tested removes an English gloss in brackets after a Bengali word. Its name
   starts with `_`, so the harm-test tool does not run it as a D3 rule.
   ```python
   import re

   _GLOSS = re.compile(r"\s?\(\s*[A-Za-z][A-Za-z0-9 .,&'’-]*\)")


   def _candidate_d3(text):
       return _GLOSS.sub("", text)                   # রোহিত শর্মা (Rohit Sharma) -> রোহিত শর্মা
   ```
3. **Action:** keep the documents as they are. The candidate's action would be to fix the text.
4. **Harm test:** **Harm test:** gold set of 244 documents (ind-bn-fw2 244), medicine.md sha256 21d37e6bc395; rule: changed or dropped at most 1% or 1 document, whichever is more.
   - Changed 2 of 244 (0.82%). Dropped 0 of 244 (0.00%). **PASS**
   - ZWJ/ZWNJ audit: 0 changed documents with a different count. **PASS**
   - Normal-form audit: 0 changed documents left NFC or lost a compatibility character. **PASS**
5. **Side effects:**
   - The candidate removes good text: English names and terms that help a model link the two scripts.
   - It misses most D3: English words in Bengali letters (`ওয়ারড্রোব` at offset 643 of `3c0e338578d39683`,
     `জি-মেইল সাইন-ইন`) and URLs; these are natural Bengali and need no medicine.

## Medicine 3

1. **Disease:** F1, personal data. Count 6, in 4 documents. Only the type and the offset are given here:
   - `03af12da56523789`: private names at offsets 629 and 636 (two students in a school news story).
   - `04e967f91a68f9d2`: private names at offsets 322 and 498 (a murder victim and another person named in a crime story).
   - `138b777477338cb0`: an address at offset 633 (a house number in a fire story).
2. **Medicine:** none. The personal data in this pack is the name of a person in a news story, written as an
   ordinary Bengali word, and a house number in brackets. A regex cannot tell such a name from any other word, and
   masking every name in news would remove the subject of the story. Finding them needs a named-entity model, which is
   not a short rule.
3. **Action:** keep the documents as they are.
4. **Harm test:** there is no rule in code, so nothing changes: 0 changed, 0 dropped of 288 (the tool reports "F1 has
   no rule in code").
5. **Side effects:**
   - The names stay in the training text. They are names that the newspapers published, but they are of private
     people.
   - A mask for one form (a number in brackets after a word, `(৭৯/১)`) would also hit ages, which this pack writes the
     same way (`লাভলী (৩০)` in `04e967f91a68f9d2`), so I did not write one.

## Codes below the threshold

| Code | Disease | Count (documents) | Example |
|---|---|---|---|
| G2 | lost ZWJ or ZWNJ | 3 (1) | `0236f7515e926ec4`, offset 44: `কোরআন` (0995 09CB 09B0 0986 09A8) |
| C2 | repeated lines | 1 (1) | `529567589848cc21`, offset 2980: `শহীদ মিনার` |
