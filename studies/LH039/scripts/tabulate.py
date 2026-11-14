#!/usr/bin/env python3
"""Tabulate LH039's measures 1, 3, 4 and 5 from retained reads, as brief.md (protocol 0.1) defines them.

Reads only files already kept under studies/LH039/data/; fetches nothing.
  Measure 1: W3Techs fixed share within 7.1, 7.0 and 6.9 at each daily read (data/raw-*/w3-*.body),
             "less than 0.1%" carried as [0, 0.1) and the ratio given as a range; 7.1.5 reported
             apart and left out of numerator and denominator; monthly history points (w3h-*.body).
  Measure 3: Packagist fixed share within each branch per UTC day (data/packagist-<label>/*.json).
  Measure 4: WordPress.org branch shares (stats-1.body) and per-branch download counter increments
             (dl-*.body), where fetched.
  Measure 5: release named by stable-check (meta-4) and version-check (meta-1), where fetched.
A read whose body is missing or was not fetched is reported as missing, never as zero.
Usage: python3 -I studies/LH039/scripts/tabulate.py --packagist 2026-11-14T1415Z [--until 2026-11-14T1412Z]
"""
import argparse, csv, datetime, glob, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
BRANCHES = ["7.1", "7.0", "6.9"]
FIXED = {"7.1": (7, 1, 4), "7.0": (7, 0, 8), "6.9": (6, 9, 11)}  # brief: fixed = these or later
UNEXPLAINED = {"7.1.5"}  # brief, Missing evidence: reported separately while WordPress publishes none
E0 = datetime.date(2026, 10, 28)


def vt(v):
    p = [int(x) for x in v.split(".")]
    return tuple(p + [0] * (3 - len(p)))


def text(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def status_of(readdir, name):
    p = os.path.join(readdir, "readlog.csv")
    if not os.path.exists(p):
        return None
    rows = list(csv.reader(open(p)))
    if rows and rows[0][:1] == ["name"]:
        for r in rows[1:]:
            if r[0] == name:
                return r[3]
    return None


def body_note(readdir, name):
    p = os.path.join(readdir, name + ".body")
    if not os.path.exists(p):
        return "not requested on this read (URL not in this read's list)"
    b = open(p, "rb").read()
    if b.startswith(b"not fetched"):
        return "NotFetched: " + b.decode("utf-8", "replace").strip()
    return "status %s" % status_of(readdir, name)


def w3_release_shares(path):
    s = text(path)
    i = s.find("Subversions of WordPress")
    seg = s[i:] if i >= 0 else s
    j = seg.find("Percentages of websites using various subversions")
    seg = seg[:j] if j >= 0 else seg
    date = re.search(r"W3Techs\.com, (\d+ \w+ \d{4})", seg)
    # Skip the "How to read the diagram" sentence, which repeats the first row.
    seg = re.sub(r"How to read the diagram:.*?version \d+\.\d+\.\s", " ", seg, flags=re.S)
    rows = re.findall(r"Version (\d+\.\d+\.\d+) (less than 0\.1%|[\d.]+%)", seg)
    out = []
    for v, val in rows:
        if val.startswith("less"):
            out.append((v, 0.0, 0.1, "less than 0.1%"))
        else:
            x = float(val.rstrip("%"))
            out.append((v, x, x, val))
    return out, (date.group(1) if date else "")


def fixed_ratio(branch, rows):
    fx = FIXED[branch]
    num_lo = num_hi = oth_lo = oth_hi = 0.0
    sep = []
    for v, lo, hi, _ in rows:
        if v in UNEXPLAINED:
            sep.append((v, _)); continue
        if vt(v) >= fx:
            num_lo += lo; num_hi += hi
        else:
            oth_lo += lo; oth_hi += hi
    rlo = num_lo / (num_lo + oth_hi) if num_lo + oth_hi else None
    rhi = num_hi / (num_hi + oth_lo) if num_hi + oth_lo else None
    return rlo, rhi, sep


def w3_history(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<table class=hist>(.*?)</table>", t, flags=re.S)
    if not m:
        return None
    rows = re.split(r"<tr>", m.group(1))
    head = [html.unescape(re.sub(r"<[^>]+>", " ", c)).split() for c in re.split(r"<td>", rows[1])[2:]]
    cols = [" ".join(h[1:] + h[:1]) for h in head]
    out = []
    for r in rows[2:]:
        name = re.search(r"<th>(.*?)<", r)
        cells = [html.unescape(c).strip() for c in re.split(r"<td>", r)[1:]]  # one cell per dated column
        out.append((name.group(1) if name else "?", dict(zip(cols, cells))))
    return cols, out


def pct(x, nd=1):
    return "n/a" if x is None else "%.*f%%" % (nd, 100 * x)


def measure1(reads, lines):
    lines.append("== Measure 1: W3Techs fixed share within a branch (fixed = 7.1.4, 7.0.8, 6.9.11 or later) ==")
    lines.append("Shares as W3Techs gives them (percent of that branch's sites). 'less than 0.1%' carried as [0, 0.1).")
    lines.append("7.1.5 reported apart and excluded from numerator and denominator (brief, Missing evidence).")
    for b in BRANCHES:
        lines.append("")
        lines.append("-- branch %s --" % b)
        for rd in reads:
            lab = os.path.basename(rd)[4:]
            p = os.path.join(rd, "w3-%s.body" % b.replace(".", ""))
            if not os.path.exists(p) or status_of(rd, "w3-%s" % b.replace(".", "")) not in ("200",):
                lines.append("%s  missing: %s" % (lab, body_note(rd, "w3-%s" % b.replace(".", ""))))
                continue
            rows, date = w3_release_shares(p)
            lo, hi, sep = fixed_ratio(b, rows)
            rng = pct(lo, 2) if lo is not None and hi is not None and abs(hi - lo) < 1e-12 else "%s to %s" % (pct(lo, 2), pct(hi, 2))
            given = "; ".join("%s %s" % (v, g) for v, _, _, g in rows)
            listed = sum(1 for _ in rows)
            lines.append("%s  page date %s  fixed share %s  (%d releases listed)  separate: %s" % (
                lab, date or "not shown", rng, listed, ", ".join("%s %s" % s for s in sep) or "none"))
            lines.append("    as given: %s" % given)
    lines.append("")
    lines.append("-- W3Techs monthly history points (history_details pages, latest read; only releases above 1% shown by W3Techs) --")
    last = reads[-1]
    for b in BRANCHES:
        p = os.path.join(last, "w3h-%s.body" % b.replace(".", ""))
        h = w3_history(p) if os.path.exists(p) else None
        if not h:
            lines.append("%s: no history table" % b); continue
        cols, rows = h
        lines.append("%s (read %s): columns %s" % (b, os.path.basename(last)[4:], " | ".join(cols)))
        for name, cells in rows:
            lines.append("    %s: %s" % (name, " | ".join(cells.get(c, "") or "(blank)" for c in cols)))
        fx = FIXED[b]
        for c in cols:
            vals = {n.replace("version ", ""): cells.get(c, "") for n, cells in rows}
            fixed = [v for v in vals if vals[v] and vt(v) >= fx and v not in UNEXPLAINED]
            if c.endswith("Nov 2026") and c.startswith("1 "):
                lines.append("    1 Nov 2026 fixed releases shown: %s" % (
                    ", ".join("%s %s" % (v, vals[v]) for v in fixed) or "none above 1%"))


def measure3(label, lines, csv_path):
    d = os.path.join(DATA, "packagist-" + label)
    lines.append("")
    lines.append("== Measure 3: Packagist fixed share within a branch, per UTC day (read %s) ==" % label)
    log = list(csv.DictReader(open(os.path.join(d, "readlog.csv"))))
    bad = [r["name"] for r in log if r["status"] != "200"]
    lines.append("requests: %d, HTTP 200: %d, other: %s" % (len(log), len(log) - len(bad), ", ".join(bad) or "none"))
    rows_out = []
    for pkg in ["roots", "johnpbloch"]:
        for b in BRANCHES:
            series = {}
            labels = None
            for f in sorted(glob.glob(os.path.join(d, "%s-%s.*.json" % (pkg, b)))):
                v = os.path.basename(f)[len(pkg) + 1:-5]
                if status_of_pk(log, os.path.basename(f)[:-5]) != "200":
                    continue
                j = json.load(open(f))
                labels = j["labels"]
                vals = list(j["values"].values())[0]
                series[v] = dict(zip(labels, vals))
            fixed = [v for v in series if vt(v) >= FIXED[b] and v not in UNEXPLAINED]
            lines.append("")
            lines.append("-- %s %s: releases read %d, fixed releases %s, days %s to %s --" % (
                pkg, b, len(series), ",".join(fixed), labels[0], labels[-1]))
            first_half = None
            for day in labels:
                tot = sum(series[v].get(day, 0) for v in series)
                fx = sum(series[v].get(day, 0) for v in fixed)
                sh = fx / tot if tot else None
                dd = (datetime.date.fromisoformat(day) - E0).days
                rows_out.append([pkg, b, day, dd, fx, tot, "" if sh is None else "%.4f" % sh])
                if sh is not None and sh >= 0.5 and first_half is None:
                    first_half = (day, dd, sh)
                if dd >= -1:
                    lines.append("    %s (day %d): fixed %d of %d = %s" % (day, dd, fx, tot, pct(sh)))
            lines.append("    first day fixed release took half of branch downloads: %s" % (
                "%s (day %d, %s)" % (first_half[0], first_half[1], pct(first_half[2])) if first_half else "none in series"))
            lines.append("    last day in Packagist's series: %s" % labels[-1])
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["package", "branch", "utc_day", "days_since_E0", "fixed_downloads", "branch_downloads", "fixed_share"])
        w.writerows(rows_out)


def status_of_pk(log, name):
    for r in log:
        if r["name"] == name:
            return r["status"]
    return None


def measure4(reads, lines):
    lines.append("")
    lines.append("== Measure 4: context ==")
    lines.append("-- WordPress.org branch shares (api.wordpress.org/stats/wordpress/1.0/) --")
    for rd in reads:
        lab = os.path.basename(rd)[4:]
        p = os.path.join(rd, "stats-1.body")
        b = open(p, "rb").read() if os.path.exists(p) else b""
        try:
            s = json.loads(b)
        except Exception:
            lines.append("%s  missing: %s" % (lab, body_note(rd, "stats-1"))); continue
        below = sum(v for k, v in s.items() if vt(k) < (4, 7, 0))
        three = sum(s.get(k, 0) for k in BRANCHES)
        lines.append("%s  7.1 %s, 7.0 %s, 6.9 %s; sum 7.1+7.0+6.9 = %.3f; sum below 4.7 = %.3f; all keys sum %.3f" % (
            lab, s.get("7.1"), s.get("7.0"), s.get("6.9"), three, below, sum(s.values())))
    lines.append("-- WordPress.org per-branch download counters (wordpress.org/wp-json/wporg/v1/core-downloads/<branch>) --")
    lines.append("   downloads of that branch's package; whether automatic updates are counted: unknown")
    prev = {}
    for rd in reads:
        lab = os.path.basename(rd)[4:]
        parts = []
        for b in BRANCHES:
            n = "dl-%s" % b.replace(".", "")
            p = os.path.join(rd, n + ".body")
            if not os.path.exists(p) or status_of(rd, n) != "200":
                parts.append("%s missing (%s)" % (b, body_note(rd, n))); prev.pop(b, None); continue
            c = int(json.loads(open(p).read()).replace(",", ""))
            if b in prev:
                pl, pc = prev[b]
                hrs = (lab_dt(lab) - lab_dt(pl)).total_seconds() / 3600
                parts.append("%s %d (+%d since %s, %.1f h)" % (b, c, c - pc, pl, hrs))
            else:
                parts.append("%s %d" % (b, c))
            prev[b] = (lab, c)
        lines.append("%s  %s" % (lab, "; ".join(parts)))


def lab_dt(lab):
    return datetime.datetime.strptime(lab, "%Y-%m-%dT%H%MZ")


def measure5(reads, lines):
    lines.append("")
    lines.append("== Measure 5: supply (stable-check 'latest'/'outdated' per branch; version-check offers) ==")
    for rd in reads:
        lab = os.path.basename(rd)[4:]
        out = []
        try:
            s = json.load(open(os.path.join(rd, "meta-4.body")))
            for b in BRANCHES:
                named = [k for k, v in s.items() if (k == b or k.startswith(b + ".")) and v in ("latest", "outdated")]
                out.append("stable-check %s: %s" % (b, ", ".join("%s %s" % (k, s[k]) for k in named) or "none"))
        except Exception:
            out.append("stable-check missing (%s)" % body_note(rd, "meta-4"))
        try:
            m = json.load(open(os.path.join(rd, "meta-1.body")))
            offers = sorted({(o["response"], o["version"]) for o in m["offers"] if vt(o["version"])[:2] in [vt(b)[:2] for b in BRANCHES]})
            out.append("version-check offers on 7.1/7.0/6.9: %s" % ", ".join("%s %s" % o for o in offers))
        except Exception:
            out.append("version-check missing (%s)" % body_note(rd, "meta-1"))
        lines.append("%s  %s" % (lab, "; ".join(out)))
    lines.append("-- Supplementary, not the brief's instrument: Packagist package version lists (cand-5, cand-6) --")
    for rd in reads:
        lab = os.path.basename(rd)[4:]
        out = []
        for n, pkg in (("cand-5", "roots"), ("cand-6", "johnpbloch")):
            try:
                j = json.load(open(os.path.join(rd, n + ".body")))
                vs = [v for v in j.get("versions", []) if re.fullmatch(r"\d+\.\d+(\.\d+)?", v)]
                hi = {b: max((v for v in vs if vt(v)[:2] == vt(b)[:2]), key=vt, default="none") for b in BRANCHES}
                out.append("%s highest %s" % (pkg, ", ".join(hi[b] for b in BRANCHES)))
            except Exception:
                out.append("%s missing" % pkg)
        lines.append("%s  %s" % (lab, "; ".join(out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packagist", required=True, help="label of the checkpoint's Packagist read")
    ap.add_argument("--until", default=None, help="last daily read label to include")
    ap.add_argument("--out", default=None, help="output stem; default checkpoints/<date of --packagist>")
    a = ap.parse_args()
    reads = sorted(d for d in glob.glob(os.path.join(DATA, "raw-*")) if os.path.isdir(d))
    if a.until:
        reads = [d for d in reads if os.path.basename(d)[4:] <= a.until]
    stem = a.out or os.path.join(HERE, "..", "checkpoints", a.packagist[:10])
    os.makedirs(os.path.dirname(stem), exist_ok=True)
    lines = ["LH039 tabulation, brief protocol 0.1. Daily reads: %s. Packagist read: %s." % (
        ", ".join(os.path.basename(r)[4:] for r in reads), a.packagist), ""]
    measure1(reads, lines)
    measure3(a.packagist, lines, stem + "-packagist.csv")
    measure4(reads, lines)
    measure5(reads, lines)
    open(stem + "-tabulation.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
