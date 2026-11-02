"""Write studies/LH035/searchlog.md from the raw search logs (written before any
result was opened) and the list of results opened afterwards.
Run from the repository root: python3 studies/LH035/scripts/searchlog.py"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
OPENED = {
    ("L1a", 7): "site opened at its root (https://interconnection.cs.uchicago.edu/), not this URL; it redirected to imp.cablelabs.com (row I04)",
    ("L2a", 6): "OPENED: 302 to downloads.pch.net (row I07)",
    ("L3a", 4): "OPENED (candidate ISI ANT, undetermined)",
    ("L4b", 12): "OPENED (candidate DNS Coffee, undetermined)",
    ("L5b", 7): "OPENED (row I12)",
    ("L5b", 14): "OPENED (candidate Netlas, undetermined)",
    ("L8a", 6): "OPENED (row I36)",
    ("L10b", 3): "OPENED (candidate ITSA, excluded)",
    ("L10b", 11): "OPENED (candidate public IXP compilation, excluded)",
    ("P1", 4): "OPENED (paper L01)",
    ("P1", 8): "OPENED (paper L02)",
    ("P2", 7): "OPENED (paper L03)",
    ("P3", 2): "OPENED as its arXiv abstract and HTML pages (paper L07)",
    ("P3", 4): "OPENED (paper L11)",
    ("P3", 6): "OPENED: HTTP 503, not read (L04)",
    ("P4", 8): "OPENED (paper L06)",
    ("P5", 1): "OPENED as its arXiv abstract and HTML pages (paper L05)",
    ("P6", 5): "OPENED (paper L08)",
    ("P7", 4): "OPENED (paper L09)",
    ("P8", 3): "OPENED (paper L10)",
}

def annotate(text):
    out, sid = [], None
    for line in text.splitlines():
        m = re.match(r"## (\w+) ", line)
        if m:
            sid = m.group(1)
            line = "#" + line
        m = re.match(r"(\d+)\. ", line)
        if m and sid:
            note = OPENED.get((sid, int(m.group(1))), "not opened (lead only)")
            line = f"{line} | {note}"
        out.append(line)
    return "\n".join(out)

head = """# LH035 search log

Read on 2 November 2026 with WebSearch (standard mode). The twenty survey searches (L1a to L10b, two per layer, in the brief's fixed form) and the eight literature searches (P1 to P8) were run, and every result's title and URL written down (data/search_raw.md, data/lit_raw.md), before any result was opened. Each result below is marked as opened or not. An unopened result is a lead only: nothing in the table rests on it. The search tool also returned a model-written summary of each search; those summaries are leads too, and they suggested several candidates whose own documentation was then read directly (each row in sources.md says which search named it). Instruments read directly at a different URL from a result are not marked as opening that result.

"""
body = annotate((D / "data/search_raw.md").read_text().split("\n", 2)[2])
lit = annotate((D / "data/lit_raw.md").read_text().split("\n", 2)[2])
(D / "searchlog.md").write_text(head + "## Survey searches\n" + body + "\n\n## Literature searches\n" + lit + "\n")
print("written")
