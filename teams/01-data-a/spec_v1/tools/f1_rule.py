# TSAI decision on F1, 31 Oct: a typed placeholder for a private person's details, drop a personal listing, keep organisations.
# In code, a value is replaced only inside a comment or a string, found with tree-sitter. So `x = 555-010-0199` stays. Prose has no tree.
from bisect import bisect_right

_F1_TREE = {"cpp", "go", "java", "javascript", "python", "rust", "typescript"}
_F1_LANGS = set(_F1_TREE)  # families with a harm test so far. Prose families go here after theirs; prose has no tree, so regex alone decides
_F1_EMAIL = re.compile(r"(?<![\w.+%-])([A-Za-z0-9._%+-]+)@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})(?![\w-])")
_F1_ROLE = re.compile(r"(?i)^(info|contact|contacts|support|help|helpdesk|admin|administrator|sales|office|press|media|hello|enquiries|inquiries|"
                      r"webmaster|postmaster|noreply|no-reply|donotreply|service|services|customerservice|billing|careers|jobs|hr|legal|security|abuse|team|git|root)$")
_F1_SAFE_DOMAIN = re.compile(r"(?i)(^|\.)(example\.(com|org|net)|localhost|test|invalid|users\.noreply\.github\.com)$|(^|\.)(gov|mil)(\.[a-z]{2})?$")
_F1_FILE_END = re.compile(r"(?i)\.(js|ts|py|go|rs|java|c|h|cpp|hpp|css|html|md|json|png|jpg|svg|gif)$")  # npm scopes and retina image names
_F1_PHONE = re.compile(r"(?<![\w.+/#=-])(?:(?:\+\d{1,3}[ .-]?)?(?:\(?\d{2,5}\)?[ .-]){1,3}\d{3,5}|\+?\d{10,13})(?![\w/-]|\.\d)")
_F1_PHONE_WORD = re.compile(r"(?i)\b(tel|telephone|phone|mobile|cell|fax|whatsapp|call me)\b[^\n]{0,30}$")
_F1_ADDRESS = re.compile(r"\b\d{1,5}[A-Za-z]?\s+(?:[A-Z][A-Za-z]*\.?\s+){1,4}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl|Terrace|Crescent|Nagar|Marg|Colony)\b\.?")
_F1_ORG = re.compile(r"(?i)\b(inc|ltd|llc|corp|corporation|company|university|college|school|hospital|clinic|department|dept|ministry|council|office|"
                     r"embassy|police|bank|library|museum|hotel|restaurant|customer service|support|helpline|hotline|toll[- ]free|headquarters|hq|reception|sales)\b")


@cache
def _f1_parser(lang):
    from tree_sitter_language_pack import get_parser  # no silent fallback: without the parser a hit in code raises, and the harm test shows it
    return get_parser(lang)


def _f1_text_spans(text, lang):
    """Sorted (start byte, end byte) of the comments and strings of a code file."""
    out, stack = [], [_f1_parser(lang).parse(text.encode("utf-8", "replace")).root_node]
    while stack:
        n = stack.pop()
        if "comment" in n.type or "string" in n.type or n.type == "jsx_text":
            out.append((n.start_byte, n.end_byte))
        else:
            stack.extend(n.children)
    return sorted(out)


def _f1_is_phone(m, line):
    digits = sum(c.isdigit() for c in m.group())
    if not 10 <= digits <= 13:
        return False
    if m.group().startswith("+") or _F1_PHONE_WORD.search(line[:m.start()]):
        return True
    return bool(re.fullmatch(r"\(?\d{3}\)?[ -]\d{3}-\d{4}", m.group()))  # the plain US form; digit groups alone are too common in data


def _f1_hits(line, previous):
    """(start, end, tag) of a private person's details on one line. An organisation on this line or the one above keeps its phone and address."""
    out = [(m.start(), m.end(), "<EMAIL>") for m in _F1_EMAIL.finditer(line)
           if not (_F1_ROLE.match(m.group(1)) or _F1_SAFE_DOMAIN.search(m.group(2)) or _F1_FILE_END.search(m.group(2)))]
    if not (_F1_ORG.search(line) or _F1_ORG.search(previous)):
        for rx, tag in ((_F1_PHONE, "<PHONE>"), (_F1_ADDRESS, "<ADDRESS>")):
            for m in rx.finditer(line):
                if (tag != "<PHONE>" or _f1_is_phone(m, line)) and not any(s < m.end() and m.start() < e for s, e, _ in out):
                    out.append((m.start(), m.end(), tag))
    return sorted(out)


def f1(doc):
    """F1: <PHONE>, <EMAIL>, <ADDRESS> for a private person. Drop when lines with such details hold most of the text."""
    text, lang = doc["text"], doc.get("lang_label")
    if lang not in _F1_LANGS:
        return ("keep", text)
    out, hit_lines, hit_chars, previous, pos, spans = [], 0, 0, "", 0, None
    for line in text.split("\n"):
        new, last = [], 0
        for s, e, tag in _f1_hits(line, previous):
            if lang in _F1_TREE:
                if spans is None:
                    spans = _f1_text_spans(text, lang)
                    starts = [a for a, _ in spans]
                b = len(text[:pos + s].encode("utf-8", "replace"))
                i = bisect_right(starts, b) - 1
                if i < 0 or b >= spans[i][1]:
                    continue  # in code, not in a comment or a string
            new += [line[last:s], tag]
            last = e
        if new:
            hit_lines += 1
            hit_chars += len(line.strip())
        out.append("".join(new) + line[last:])
        previous = line
        pos += len(line) + 1
    if hit_lines >= 5 and hit_chars > 0.5 * sum(len(l.strip()) for l in text.split("\n")):
        return ("drop", text)
    new = "\n".join(out)
    return ("fix" if new != text else "keep", new)
