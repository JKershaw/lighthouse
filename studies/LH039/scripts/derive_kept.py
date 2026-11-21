#!/usr/bin/env python3
"""Replace LH039's kept bodies from sites whose robots.txt refuses AI-training or archiving crawlers,
or all bots, with derived files (the keeper's decision of 21 November 2026,
notes/keeper/2026-11-21-robots-intent.md).

For each such body under data/raw-*/ it writes <name>.derived.json beside it, holding the URL, the read
time, HTTP status, size and SHA-256 from that read's readlog.csv, and only the facts the study's scripts
and records use:
  w3-*.body, cand-3, cand-4 (W3Techs details pages): the page's own dates and each diagram's rows
                                                       (label and percentage), plus the headline shares;
  w3h-*.body (W3Techs history pages):                  the monthly table (column dates, row labels, cells);
  stats-1 (api.wordpress.org branch shares):           the branch-to-share map;
  meta-1 (version-check):                              each offer's response and version;
  meta-4 (stable-check):                               the status of every release on branches 7.1, 7.0, 6.9;
  stats-2, stats-3, stats-4:                           nothing beyond the read's metadata (kept unread).
Bodies that are Lighthouse's own "not fetched" notes are not page bodies and are left alone.
It checks that tabulate.py reads the same values from the derived file as from the body, and stops if
not. It never deletes anything: the bodies are removed separately, after the outputs are compared.
Offline, standard library only. Usage: python3 -I studies/LH039/scripts/derive_kept.py
"""
import csv, glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
BRANCHES = ["7.1", "7.0", "6.9"]
W3 = ("cand-3", "cand-4", "w3-71", "w3-70", "w3-69")
W3H = ("w3h-71", "w3h-70", "w3h-69")
API = ("stats-1", "stats-2", "stats-3", "stats-4", "meta-1", "meta-4")
ROBOTS = {"w3techs.com": "A: AI-training token named and refused; * allows",
          "api.wordpress.org": "B: * refuses all bots (no AI token named)"}
USED = {
    "cand-3": "Candidate source before the brief (W3Techs's overall WordPress page), kept unread; context only.",
    "cand-4": "Candidate source before the brief (W3Techs's WordPress 7 page, which links the per-branch pages); context only.",
    "w3-": "Measure 1: W3Techs's per-release shares within the branch at this read (tabulate.py).",
    "w3h-": "Measure 1: W3Techs's monthly history points for the branch (tabulate.py, latest read).",
    "stats-1": "Measure 4 and before-the-brief: WordPress.org's per-branch shares (tabulate.py).",
    "stats-2": "Before-the-brief: PHP shares kept beside stats-1, unread; no figure used.",
    "stats-3": "Before-the-brief: MySQL shares kept beside stats-1, unread; no figure used.",
    "stats-4": "Before-the-brief: locale shares kept beside stats-1, unread; no figure used.",
    "meta-1": "Measure 5 and before-the-brief: releases the version-check API offers (tabulate.py).",
    "meta-4": "Measure 5 and before-the-brief: stable-check's status of each release on 7.1, 7.0, 6.9 (tabulate.py).",
}


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
    """W3Techs history_details page: the monthly table, as tabulate.py's w3_history reads it."""
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


def readlog(d):
    rows = list(csv.reader(open(os.path.join(d, "readlog.csv"))))
    out = {}
    if rows and rows[0][:1] == ["name"]:
        for r in rows[1:]:
            out[r[1]] = {"name": r[0], "url": r[1], "read_utc": r[2], "http_status": r[3], "content_type": r[4],
                         "bytes": int(r[5]), "sha256": r[6]}
    else:  # 7 November: url, start, "status content-type size", sha256 (no header)
        for r in rows:
            st, rest = r[2].split(" ", 1)
            ct, size = rest.rsplit(" ", 1)
            out[r[0]] = {"url": r[0], "read_utc": r[1], "http_status": st, "content_type": ct, "bytes": int(size), "sha256": r[3]}
    return out


URLS = {"cand-3": "https://w3techs.com/technologies/details/cm-wordpress",
        "cand-4": "https://w3techs.com/technologies/details/cm-wordpress/7",
        "stats-1": "https://api.wordpress.org/stats/wordpress/1.0/", "stats-2": "https://api.wordpress.org/stats/php/1.0/",
        "stats-3": "https://api.wordpress.org/stats/mysql/1.0/", "stats-4": "https://api.wordpress.org/stats/locale/1.0/",
        "meta-1": "https://api.wordpress.org/core/version-check/1.7/", "meta-4": "https://api.wordpress.org/core/stable-check/1.0/"}
for b in BRANCHES:
    k = b.replace(".", "")
    URLS["w3-" + k] = "https://w3techs.com/technologies/details/cm-wordpress/" + b
    URLS["w3h-" + k] = "https://w3techs.com/technologies/history_details/cm-wordpress/" + b


def extract(name, raw):
    if name in W3:
        return w3_details(raw)
    if name in W3H:
        return {"history": w3_history(raw)}
    if name == "stats-1":
        return {"shares": json.loads(raw)}
    if name == "meta-1":
        return {"offers": [{"response": o["response"], "version": o["version"]} for o in json.loads(raw)["offers"]]}
    if name == "meta-4":
        s = json.loads(raw)
        return {"stable_check": {k: v for k, v in s.items() if any(k == b or k.startswith(b + ".") for b in BRANCHES)}}
    return {}


def check(name, raw, ext):
    """The values tabulate.py takes from the body must equal those it takes from the derived file."""
    sys.path.insert(0, HERE)
    import tabulate as T
    if name.startswith("w3-"):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".body") as f:
            f.write(raw); f.flush()
            a = T.w3_release_shares(f.name)
        assert a == T.w3_release_shares_derived({"extracted": ext}), name
    elif name.startswith("w3h-"):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".body") as f:
            f.write(raw); f.flush()
            a = T.w3_history(f.name)
        h = ext["history"]
        assert a == (None if h is None else (h["columns"], [tuple(r) for r in h["rows"]])), name


def main():
    n = 0
    for d in sorted(glob.glob(os.path.join(DATA, "raw-*"))):
        log = readlog(d)
        for name in W3 + W3H + API:
            p = os.path.join(d, name + ".body")
            out = os.path.join(d, name + ".derived.json")
            if not os.path.exists(p):
                continue
            raw = open(p, "rb").read()
            if raw.startswith(b"not fetched"):
                continue  # Lighthouse's own note of a robots.txt refusal, not a page body
            url = URLS[name]
            meta = dict(log[url])
            meta.pop("name", None)
            ext = extract(name, raw)
            check(name, raw, ext)
            host = url.split("/")[2]
            rec = {"url": url, **{k: v for k, v in meta.items() if k != "url"},
                   "robots_class": ROBOTS[host], "body_removed": NOTE,
                   "used_for": USED.get(name, USED.get(name.split("-")[0] + "-")),
                   "extracted": ext}
            open(out, "w").write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
            n += 1
    print("derived files written:", n)


if __name__ == "__main__":
    main()
