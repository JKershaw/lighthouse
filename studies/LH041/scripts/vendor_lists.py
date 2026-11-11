"""LH041, brief Amendment 2, analysis 1 (post hoc; written 11 November 2026, before
read 2's collection): vendors' package lists set beside OSV.

    python3 -I studies/LH041/scripts/vendor_lists.py --read <read label> [--out DIR]

For W04, W05, W10 and W11, packages printed on vendor or press pages already
retained under data/prebrief/web/ or review/web/ are matched by exact package
name to OSV's MAL- records of the given read. Reported per wave and per page:
packages in both, only in the vendor's list, and only in OSV's records. Writes
data/<read>/tables/amendment2/vendor_lists.csv and vendor_lists_names.csv (or
under DIR) and prints the summary. Needs scripts/tabulate.py to have been run
on the read first (it reads tables/records.csv and tables/posthoc/records.csv
for which records the brief joined to each wave). Makes no request: the
amendment allows gated re-reads, but this script reads retained pages only, and
a page that is not retained, or whose retained body is a wall or an error, is
reported as missing and that page's comparison as unknown.

Post hoc: the amendment was conceived after read 1's counts were seen. For W04,
W05 and W10 the vendor list is a second join route, counted apart from the
brief's joins and never summed with them. Vendor lists never assign a record to
a wave under the brief's rules. For W11, StepSecurity's page (w19) says its full
list is served by an authenticated enterprise endpoint, which is not used (no
account; a login is a wall); the comparison covers only what the public pages
print.

Rules fixed here where the amendment leaves a choice (fixed from the protocol
files and the pages' structure, before any match was computed):
  V1 Which pages. A wave's pages are those that scripts/waves.py (protocol 0.1,
     fixed before any record was read) names in that wave's `src`: W04, W05 and
     W10 -> w07 (Unit 42); W11 -> w19 (StepSecurity), w13 (Elastic), w18
     (Unit 42), w03 (BleepingComputer). No other retained page is attributed to
     a wave, since nothing fixed in advance says which wave its packages
     belong to.
  V2 Which copy. The copy under data/prebrief/web/ is read; if a page also has a
     copy under review/web/, the names are extracted from it too and the output
     says whether the two lists are identical (if they differ, both lists are
     written to vendor_lists_names.csv and the prebrief list is the one
     counted). A page whose prebrief fetch log status is not 200 and that has
     no review copy is missing.
  V3 Which part of a page. On a page named for more than one of the four waves
     (w07), a wave's part is the subsection of the page's "Indicators of
     Compromise" section whose heading contains the wave's vendor-clock date
     written as "<Month> <day>, <year>" (W04 April 22, 2026; W05 April 29,
     2026; W10 July 14, 2026), from that heading to the next h2 or h3 heading;
     the narrative sections are not read, because they discuss several waves
     together. On a page named for one wave, the part is the article: from the
     first h1 to the first later heading whose text begins with "Related",
     "Explore Related", "Tags", "Table of Contents", "Comments" or "You may
     also like" (site furniture), or to the end of the page.
  V4 How names are extracted. Within that part, a package is printed if it
     appears (i) as name@version in the visible text (scripts and styles
     removed, tags replaced by spaces, entities decoded), with an npm name,
     scoped or not, and a version beginning digit.digit.digit; or (ii) in the
     first column of an HTML table whose first header cell reads "Package";
     or (iii) as an entry of a data list embedded in the page's script for
     display, that is a quoted string made only of two or more ";"-separated
     entries of the form name@version or name@version|version... (StepSecurity
     renders its searchable "Package / Compromised Versions" table from such a
     list; the list is parsed as text, never run). Bare unscoped names in prose
     are not extracted, since they cannot be told from words. A page part that
     yields no names is reported as "no list printed" and its comparison as
     unknown, never as zero packages.
  V5 Matching. Exact, case-sensitive string equality of package names, against
     npm MAL- records only (all four waves and all their pages are npm), not
     withdrawn, in the read's osv-mal-index.csv.gz. Versions are not matched.
  V6 What is reported. For each wave, each page and the union of the wave's
     pages: vendor_listed; in_both_any_mal (vendor names with any npm MAL-
     record in the read), split into joined to this wave by the brief, joined
     to another wave, and joined to none (lineage, ambiguous, unassigned, or
     not selected); in_both_wave (vendor names among the packages the brief
     joined to this wave); only_vendor (vendor names with no npm MAL- record);
     only_osv (packages the brief joined to this wave that the page does not
     list). The brief's joins are taken in the indicator+window scope, in the
     brief's view and, separately, the post hoc view.
"""
import argparse, collections, csv, gzip, html, os, re, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import waves  # noqa: E402

W = {w["id"]: w for w in waves.WAVES}
WAVES = ["W04", "W05", "W10", "W11"]
PRE = os.path.join(HERE, "..", "data", "prebrief", "web")
REV = os.path.join(HERE, "..", "review", "web")
NAME = r"(?:@[A-Za-z0-9~][A-Za-z0-9._~-]*/)?[A-Za-z0-9~][A-Za-z0-9._~-]*"
VER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"
NV = re.compile(r"(?<![A-Za-z0-9._~/@-])(" + NAME + r")@(" + VER + r")")
FULLNAME = re.compile(r"^" + NAME + r"$")
ENTRY = re.compile(r"^(" + NAME + r")@" + VER + r"(?:\|" + VER + r")*$")
FURNITURE = ("related", "explore related", "tags", "table of contents", "comments", "you may also like")
HEAD = re.compile(r"<(h[1-4])\b[^>]*>(.*?)</\1\s*>", re.S | re.I)


def shown(path):
    """Path as printed: relative to the repository, or a placeholder for an --out outside it."""
    root = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
    path = os.path.realpath(path)
    return os.path.relpath(path, root) if path.startswith(root + os.sep) else "<--out directory>/" + os.path.basename(path)


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def pages_for(wid):
    return re.findall(r"\bw\d\d\b", W[wid]["src"])  # V1


def log_status():
    st = {}
    for r in csv.DictReader(open(os.path.join(HERE, "..", "data", "prebrief", "web-log.psv")), delimiter="|"):
        st[r["file"].split(".")[0]] = r["status"]
    return st


def part(doc, page, wid, multi):
    heads = [(m.start(), m.end(), m.group(1).lower(), text_of(m.group(2))) for m in HEAD.finditer(doc)]
    if multi:  # V3, dated subsection of Indicators of Compromise
        d = datetime.strptime(re.search(r"\d{4}-\d{2}-\d{2}", W[wid]["vendor_clock"]).group(0), "%Y-%m-%d")
        date = f"{d.strftime('%B')} {d.day}, {d.year}"
        ioc = [h for h in heads if h[2] == "h2" and h[3].lower().startswith("indicators of compromise")]
        if not ioc:
            return None, "no Indicators of Compromise section"
        i0 = ioc[0][0]
        nxt_h2 = min([h[0] for h in heads if h[2] == "h2" and h[0] > i0] + [len(doc)])
        sub = [h for h in heads if h[2] == "h3" and i0 < h[0] < nxt_h2 and date in h[3]]
        if not sub:
            return None, f"no Indicators of Compromise subsection dated {date}"
        s = sub[0][0]
        e = min([h[0] for h in heads if h[2] in ("h2", "h3") and h[0] > s] + [len(doc)])
        return doc[s:e], f"IOC subsection '{sub[0][3]}'"
    h1 = [h for h in heads if h[2] == "h1"]
    if not h1:
        return None, "no h1"
    s = h1[0][0]
    e = min([h[0] for h in heads if h[0] > s and h[3].lower().startswith(FURNITURE)] + [len(doc)])
    return doc[s:e], "article from h1"


def extract(fragment):
    names = set()
    for sc in re.findall(r"<script\b[^>]*>(.*?)</script\s*>", fragment, re.S | re.I):  # V4 (iii)
        for lit in re.findall(r"'([^'\n]*)'|\"([^\"\n]*)\"", sc):
            lit = lit[0] or lit[1]
            ent = [x for x in lit.split(";") if x]
            if len(ent) >= 2 and all(ENTRY.match(x) for x in ent):
                names.update(ENTRY.match(x).group(1) for x in ent)
    vis = re.sub(r"<(script|style|noscript)\b.*?</\1\s*>", " ", fragment, flags=re.S | re.I)
    for t in re.findall(r"<table\b.*?</table\s*>", vis, re.S | re.I):  # V4 (ii)
        trs = re.findall(r"<tr\b.*?</tr\s*>", t, re.S | re.I)
        if not trs:
            continue
        hdr = re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]\s*>", trs[0], re.S | re.I)
        if not hdr or text_of(hdr[0]).lower() != "package":
            continue
        for tr in trs[1:]:
            c = re.findall(r"<td\b[^>]*>(.*?)</td\s*>", tr, re.S | re.I)
            if c:
                n = text_of(c[0])
                n = re.sub(r"@" + VER + r"$", "", n)
                if FULLNAME.match(n):
                    names.add(n)
    for m in NV.finditer(text_of(vis)):  # V4 (i)
        names.add(m.group(1))
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True)
    ap.add_argument("--out", help="output directory (default data/<read>/tables/amendment2)")
    a = ap.parse_args()
    d = os.path.join(HERE, "..", "data", a.read)
    out = a.out or os.path.join(d, "tables", "amendment2")
    os.makedirs(out, exist_ok=True)

    mal = set()
    for r in csv.DictReader(gzip.open(os.path.join(d, "osv-mal-index.csv.gz"), "rt")):
        if r["ecosystem"] == "npm" and r["id"].startswith("MAL-") and not r["withdrawn"]:
            mal.add(r["package"])
    joined = {}
    for view in ("brief", "posthoc"):
        f = os.path.join(d, "tables", *(["posthoc"] if view == "posthoc" else []), "records.csv")
        if not os.path.exists(f):
            sys.exit(f"missing {f}: run scripts/tabulate.py --read {a.read} (and --posthoc) first")
        jw = collections.defaultdict(set)
        for r in csv.DictReader(open(f)):
            if r["wave"] and r["ecosystem"] == "npm" and r["join"] in ("indicator", "window"):
                jw[r["package"]].add(r["wave"])
        joined[view] = jw

    status = log_status()
    multi_pages = collections.Counter(p for w in WAVES for p in set(pages_for(w)))
    rows, name_rows, notes = [], [], []

    def compare(wid, page, names, how):
        row = dict(wave=wid, page=page, part=how, vendor_listed=len(names) if names else "")
        if not names:
            row.update(comparison="unknown (no list printed)" if names is not None else "unknown (missing)")
            rows.append(row)
            return
        both = names & mal
        row["comparison"] = "compared"
        row["in_both_any_mal"] = len(both)
        for view in ("brief", "posthoc"):
            jw = joined[view]
            wave_pk = {p for p, ws in jw.items() if wid in ws}
            row[f"{view}_in_both_joined_this_wave"] = sum(1 for p in both if wid in jw.get(p, ()))
            row[f"{view}_in_both_joined_other_wave_only"] = sum(1 for p in both if jw.get(p) and wid not in jw[p])
            row[f"{view}_in_both_joined_none"] = sum(1 for p in both if not jw.get(p))
            row[f"{view}_osv_wave_packages"] = len(wave_pk)
            row[f"{view}_only_osv"] = len(wave_pk - names)
        row["only_vendor"] = len(names - mal)
        rows.append(row)

    for wid in WAVES:
        union, any_list = set(), False
        for page in pages_for(wid):
            multi = multi_pages[page] > 1
            copies = {}
            for lab, base in (("prebrief", PRE), ("review", REV)):
                f = os.path.join(base, page + ".html.gz")
                if not os.path.exists(f) or (lab == "prebrief" and status.get(page) != "200"):
                    continue
                doc = gzip.open(f, "rt", encoding="utf-8", errors="replace").read()
                frag, how = part(doc, page, wid, multi)
                copies[lab] = (extract(frag) if frag is not None else set(), how)
            if not copies:
                compare(wid, page, None, f"not retained or not 200 (log status {status.get(page, 'none')})")
                continue
            lab = "prebrief" if "prebrief" in copies else "review"
            names, how = copies[lab]
            if len(copies) == 2:
                same = copies["prebrief"][0] == copies["review"][0]
                notes.append(f"{wid} {page}: prebrief and review copies give {'identical' if same else 'DIFFERENT'} lists "
                             f"({len(copies['prebrief'][0])} and {len(copies['review'][0])} names)")
            for l2, (nm, _) in copies.items():
                if l2 == lab or nm != names:
                    for n in sorted(nm):
                        name_rows.append([wid, page, l2, n, int(n in mal),
                                          ";".join(sorted(joined["brief"].get(n, ()))),
                                          ";".join(sorted(joined["posthoc"].get(n, ())))])
            compare(wid, page, names, f"{lab} copy; {how}")
            union |= names
            any_list = any_list or bool(names)
        compare(wid, "all pages", union if any_list else set(), "union of the wave's pages")

    fields = ["wave", "page", "part", "comparison", "vendor_listed", "in_both_any_mal",
              "brief_in_both_joined_this_wave", "brief_in_both_joined_other_wave_only", "brief_in_both_joined_none",
              "only_vendor", "brief_osv_wave_packages", "brief_only_osv",
              "posthoc_in_both_joined_this_wave", "posthoc_in_both_joined_other_wave_only", "posthoc_in_both_joined_none",
              "posthoc_osv_wave_packages", "posthoc_only_osv"]
    with open(os.path.join(out, "vendor_lists.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(out, "vendor_lists_names.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "page", "copy", "package", "has_npm_mal_record", "brief_joined_waves", "posthoc_joined_waves"])
        w.writerows(name_rows)

    print(f"LH041 Amendment 2, analysis 1 (post hoc), read {a.read}; written to "
          f"{shown(os.path.join(out, 'vendor_lists.csv'))} and vendor_lists_names.csv")
    print(f"npm MAL- records' packages in the read (not withdrawn): {len(mal)}")
    for n in notes:
        print("copy check:", n)
    w = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)


if __name__ == "__main__":
    main()
