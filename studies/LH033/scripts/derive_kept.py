#!/usr/bin/env python3
"""Replace LH033's kept W3Techs bodies with derived files (the keeper's decision of 21 November 2026,
notes/keeper/2026-11-21-robots-intent.md: W3Techs's robots.txt refuses AI-training and archiving crawlers).

For each data/read-*/w3techs-details-<minor>.raw.gz and w3techs-history_details-<minor>.raw.gz it writes
<name>.derived.json beside it, holding the URL, read times, HTTP status, size and SHA-256 from that read's
read_log.json, and only the facts the study uses:
  details pages: the page's own dates, the headline share and each version diagram's rows (label, percentage),
                 from which tabulate.py takes measure 4;
  history pages: the monthly table (column dates, row labels, cells), for measure 6 (amendment 1).
It never deletes anything. Offline, standard library only.
Usage: python3 -I studies/LH033/scripts/derive_kept.py
"""
import glob, gzip, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
ROBOTS = "A: AI-training token named and refused; * allows"
USED = {"details": "Measure 4: W3Techs's share within the minor at or above the fixed patch (tabulate.py, m4_w3techs_within_minor).",
        "history_details": "Measure 6 (amendment 1): W3Techs's monthly points within the minor; no script reads it yet."}


def page_text(raw):
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


EXAMPLE = re.compile(r"(?:Version [\d.]+?|WordPress|PHP) is used by [\d.]+% of all the websites"
                     r"(?: who use (?:WordPress|PHP)(?: version [\d.]+?)?)?\.(?= )")


def w3_details(raw):
    """W3Techs details page: headline shares and each version diagram's dated rows (label, percentage)."""
    s = page_text(raw)
    out = {"page_dates": re.findall(r"W3Techs\.com, (\d+ \w+ \d{4})", s), "headline": None, "diagrams": []}
    h = re.search(r"is used by ([\d.]+%) of all the websites whose (.+?) we know\.(?: This is ([\d.]+%) of all websites)?", s)
    if h:
        out["headline"] = {"share_of_known": h.group(1), "of": h.group(2), "share_of_all_websites": h.group(3)}
    for m in re.finditer(r"(?:This|The) diagram shows the (percentages? of websites using .*?)\. How to read the diagram: (.*?) "
                         r"W3Techs\.com, (\d+ \w+ \d{4})", s):
        cap, body, date = m.groups()
        if "subtechnologies" in cap:
            continue  # product names, not versions; no script or record uses them
        rows = re.findall(r"(Version [\d.]+|WordPress|PHP) (less than 0\.1%|[\d.]+%)", EXAMPLE.sub(" ", body))
        out["diagrams"].append({"caption": cap, "date": date, "rows": [list(r) for r in rows]})
    return out


def w3_history(raw):
    """W3Techs history_details page: the monthly table, as LH039's tabulate.py reads such a table."""
    t = raw.decode("utf-8", "replace")
    m = re.search(r"<table class=hist>(.*?)</table>", t, flags=re.S)
    if not m:
        return None
    rows = re.split(r"<tr>", m.group(1))
    head = [html.unescape(re.sub(r"<[^>]+>", " ", c)).split() for c in re.split(r"<td>", rows[1])[2:]]
    cols = [" ".join(h[1:] + h[:1]) for h in head]
    out = []
    for r in rows[2:]:
        name = re.search(r"<th>(.*?)<", r)
        cells = [html.unescape(c).strip() for c in re.split(r"<td>", r)[1:]]
        out.append([name.group(1) if name else "?", dict(zip(cols, cells))])
    return {"columns": cols, "rows": out}


def main():
    n = 0
    for d in sorted(glob.glob(os.path.join(DATA, "read-*"))):
        logp = os.path.join(d, "read_log.json")
        if not os.path.exists(logp):
            continue
        for row in json.load(open(logp)):
            src = row.get("source", "")
            if not src.startswith("w3techs-") or not row.get("file"):
                continue
            p = os.path.join(d, row["file"])
            if not os.path.exists(p):
                continue
            raw = gzip.decompress(open(p, "rb").read())
            kind = src.split("-")[1]
            ext = w3_details(raw) if kind == "details" else {"history": w3_history(raw)}
            rec = {"url": row["url"], "read_utc": row.get("start_utc"), "finish_utc": row.get("finish_utc"),
                   "http_status": row.get("status"), "content_type": row.get("content_type"), "bytes": row.get("bytes"),
                   "sha256": row.get("sha256"), "robots_class": ROBOTS, "body_removed": NOTE, "used_for": USED[kind],
                   "extracted": ext}
            open(os.path.join(d, src + ".derived.json"), "w").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
            n += 1
    print("derived files written:", n)


if __name__ == "__main__":
    main()
