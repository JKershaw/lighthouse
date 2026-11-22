#!/usr/bin/env python3
"""R-0114, evidence review of LH039 record 1.0: independent recomputation from retained files.

Written by the reviewer (Claude Code, Claude Opus 5.5), 22 November 2026. Offline; reads only
studies/LH039/data/ and studies/LH033/data/; imports nothing from the study's scripts.
Usage: python3 -I studies/LH039/review/R-0114_checks.py > studies/LH039/review/R-0114_checks.out.txt
"""
import datetime, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "data")
L33 = os.path.join(HERE, "..", "..", "LH033", "data")
E0 = datetime.date(2026, 10, 28)
E3 = datetime.datetime(2026, 11, 18, 17, 8, 59)
FIX = {"7.1": (7, 1, 4), "7.0": (7, 0, 8), "6.9": (6, 9, 11)}


def vt(s):
    return tuple(int(x) for x in s.split("."))


def pct(s):
    """'less than 0.1%' -> (0, 0.1); '38.3%' -> (38.3, 38.3)."""
    if s.startswith("less than"):
        return (0.0, 0.1)
    v = float(s.rstrip("%"))
    return (v, v)


def w3rows(path):
    j = json.load(open(path))["extracted"]
    for dg in j["diagrams"]:
        if dg["caption"].startswith("percentages of websites using various subversions"):
            return {r[0].replace("Version ", ""): pct(r[1]) for r in dg["rows"]}, j["page_dates"]
    raise SystemExit("no subversion diagram in " + path)


def share(rows, fixed, apart=()):
    """Range of fixed/(fixed+unfixed): low = fixed_lo/(fixed_lo+unfixed_hi), high = fixed_hi/(fixed_hi+unfixed_lo)."""
    fl = fh = ul = uh = 0.0
    for v, (lo, hi) in rows.items():
        if v in apart:
            continue
        if fixed(v):
            fl += lo; fh += hi
        else:
            ul += lo; uh += hi
    return 100 * fl / (fl + uh), 100 * fh / (fh + ul)


def f(r):
    return "%.2f%% to %.2f%%" % r


print("== 1. W3Techs fixed share, measure 1, every read from 9 November (7.1.5 apart before E3, fixed after) ==")
reads = sorted(os.path.basename(p)[4:] for p in glob.glob(os.path.join(D, "raw-2026-11-*")) if os.path.basename(p)[4:] >= "2026-11-09")
series = {b: [] for b in FIX}
for lab in reads:
    dt = datetime.datetime.strptime(lab, "%Y-%m-%dT%H%MZ")
    for b in FIX:
        rows, dates = w3rows(os.path.join(D, "raw-" + lab, "w3-%s.derived.json" % b.replace(".", "")))
        apart = ("7.1.5",) if (b == "7.1" and dt < E3) else ()
        r = share(rows, lambda v, b=b: vt(v) >= FIX[b], apart)
        series[b].append(r)
        extra = ""
        if b == "7.1" and lab == "2026-11-21T1411Z":
            extra = " | 7.1.5 apart: %s | 7.1.4 alone: %s | 7.1.5,7.1.6 apart: %s" % (
                f(share(rows, lambda v: vt(v) >= FIX[b], ("7.1.5",))),
                f(share(rows, lambda v: v == "7.1.4")), f(share(rows, lambda v: vt(v) >= FIX[b], ("7.1.5", "7.1.6"))))
        if b != "7.1" and lab == "2026-11-21T1411Z":
            r0 = "%d.%d.%d" % FIX[b]
            extra = " | %s alone: %s" % (r0, f(share(rows, lambda v, r0=r0: v == r0)))
        print("%s %s day %d page %s: %s%s" % (b, lab, (dt.date() - E0).days, dates[0], f(r), extra))
for b in FIX:
    s = series[b]
    up = all(s[i][0] > s[i - 1][1] for i in range(1, len(s)))
    print("%s: every read strictly above the previous one (low bound > previous high bound): %s" % (b, up))
# effect of counting the early 7.1.5 label as fixed, reads before E3
mx = 0
for lab in reads:
    dt = datetime.datetime.strptime(lab, "%Y-%m-%dT%H%MZ")
    if dt < E3:
        rows, _ = w3rows(os.path.join(D, "raw-" + lab, "w3-71.derived.json"))
        a = share(rows, lambda v: vt(v) >= (7, 1, 4), ("7.1.5",)); c = share(rows, lambda v: vt(v) >= (7, 1, 4))
        mx = max(mx, abs(c[0] - a[0]), abs(c[1] - a[1]))
print("largest change in either bound, first ten reads, 7.1.5 fixed vs apart: %.3f points" % mx)

print("\n== 2. W3Techs history, 1 November column, as on the 21 November history pages ==")
for b, r in (("71", "7.1.4"), ("70", "7.0.8"), ("69", "6.9.11"), ("71", "7.1.5")):
    h = json.load(open(os.path.join(D, "raw-2026-11-21T1411Z", "w3h-%s.derived.json" % b)))["extracted"]["history"]
    for name, cols in h["rows"]:
        if name == "version " + r:
            print(r, "1 Nov 2026:", cols.get("1 Nov 2026"))

print("\n== 3. Measure 2: LH033 PHP W3Techs pages, recomputed (share at or above fixed patch / all listed) ==")
php = {}
for lab, day in (("2026-11-02T1530Z", 12), ("2026-11-09T1427Z", 19), ("2026-11-16T1419Z", 26)):
    t = json.load(open(os.path.join(L33, "read-" + lab, "tables.json")))["m4_w3techs_within_minor"]
    for m in ("8.2", "8.3", "8.4", "8.5"):
        rows, _ = w3rows(os.path.join(L33, "read-" + lab, "w3techs-details-%s.derived.json" % m))
        fp = t[m]["fixed_patch"]
        r = share(rows, lambda v, fp=fp: vt(v)[2] >= fp)
        php[(day, m)] = (t[m]["share_at_or_above_fixed_pct"], r)
        print("PHP day %d %s: LH033 tabulated %.1f%%; recomputed %s" % (day, m, t[m]["share_at_or_above_fixed_pct"], f(r)))
wp14, wp24 = series["7.1"][reads.index("2026-11-11T1415Z")], series["7.1"][reads.index("2026-11-21T1411Z")]
for wp, day, lbl in ((wp14, 12, "WP day 14 vs PHP day 12"), (wp14, 19, "WP day 14 vs PHP day 19"), (wp24, 26, "WP day 24 vs PHP day 26"), (wp24, 19, "WP day 24 vs PHP day 19")):
    cmp = []
    for m in ("8.2", "8.3", "8.4", "8.5"):
        tab, rr = php[(day, m)]
        rel = "above" if wp[0] > max(tab, rr[1]) else "below" if wp[1] < min(tab, rr[0]) else "overlaps"
        cmp.append("%s %s" % (m, rel))
    print("%s (%s): %s" % (lbl, f(wp), ", ".join(cmp)))

print("\n== 4. Packagist, from the per-version files of the 21 November read ==")
def series_pk(pkg, b, read="packagist-2026-11-21T1415Z"):
    files = glob.glob(os.path.join(D, read, "%s-%s.*.json" % (pkg, b)))
    tot, fx, labels = {}, {}, None
    for p in files:
        v = os.path.basename(p)[len(pkg) + 1:-5]
        j = json.load(open(p)); labels = j["labels"]
        assert len(j["values"]) == 1, p  # x.y.0 is keyed "x.y" by Packagist
        vals = list(j["values"].values())[0]
        for d, n in zip(labels, vals):
            tot[d] = tot.get(d, 0) + n
            if vt(v) >= FIX[b]:
                fx[d] = fx.get(d, 0) + n
    return labels, tot, fx, sorted(os.path.basename(p)[len(pkg) + 1:-5] for p in files)
for pkg in ("roots", "johnpbloch"):
    for b in FIX:
        labels, tot, fx, vers = series_pk(pkg, b)
        days = [d for d in labels if d >= "2026-10-28"]
        sh = {d: fx.get(d, 0) / tot[d] for d in labels if tot[d]}
        first = next((d for d in days if sh[d] >= 0.5), None)
        half = [d for d in days if sh[d] >= 0.5]
        below_all = [d for d in days if sh[d] < 0.5]
        below_full = [d for d in days if sh[d] < 0.5 and d <= "2026-11-17"]
        pre = max(sh[d] for d in labels if d < "2026-10-28")
        print("%s %s: versions %s..%s (%d); last label %s; max share before 28 Oct %.3f" % (pkg, b, vers[0], vers[-1], len(vers), labels[-1], pre))
        print("  first day >= half: %s (%s)" % (first, "%.1f%%" % (100 * sh[first]) if first else "-"))
        print("  days >= half: %s" % half)
        print("  days below half 28 Oct-19 Nov: %d of %d; 28 Oct-17 Nov (full coverage): %d of %d" % (
            len(below_all), len(days), len(below_full), len([d for d in days if d <= "2026-11-17"])))
        for d in ("2026-11-17", "2026-11-18", "2026-11-19"):
            print("  %s: %d of %d = %.1f%%" % (d, fx.get(d, 0), tot[d], 100 * sh[d]))
        if b != "7.1":
            win = [tot[d] for d in labels if "2026-11-12" <= d <= "2026-11-19"]
            print("  daily totals 12-19 Nov: min %d max %d" % (min(win), max(win)))
        wk = []
        for d in labels:
            dd = datetime.date.fromisoformat(d)
            if dd.weekday() == 5:
                fri = (dd - datetime.timedelta(1)).isoformat(); mon = (dd + datetime.timedelta(2)).isoformat()
                sun = (dd + datetime.timedelta(1)).isoformat()
                if fri in tot and mon in tot:
                    wk.append("%s:%s" % (d[5:], max(tot[d], tot[sun]) < min(tot[fri], tot[mon])))
        print("  weekend (Sat and Sun both below Fri and Mon): %s" % ", ".join(wk))
# identical overlap between the two checkpoint reads
same = n = 0
for pkg in ("roots", "johnpbloch"):
    for b in FIX:
        l1, t1, f1, _ = series_pk(pkg, b, "packagist-2026-11-14T1415Z")
        l2, t2, f2, _ = series_pk(pkg, b, "packagist-2026-11-21T1415Z")
        for d in l1:
            if d in t2:
                n += 1; same += (t1[d] == t2[d] and f1.get(d, 0) == f2.get(d, 0))
print("package-branch-days held by both reads: %d; identical totals and fixed counts: %d" % (n, same))

print("\n== 5. WordPress.org per-branch download counter increments (measure 4 context) ==")
for b in ("71", "70", "69"):
    vals = []
    for lab in reads:
        p = os.path.join(D, "raw-" + lab, "dl-%s.body" % b)
        if os.path.exists(p):
            vals.append((lab, int(json.load(open(p)).replace(",", ""))))
    inc = [(vals[i][0], vals[i][1] - vals[i - 1][1]) for i in range(1, len(vals))]
    print(b, " ".join("%s:%d" % (l[5:10], v) for l, v in inc))

print("\n== 6. WordPress.org branch shares, 7 and 8 November ==")
for lab in ("2026-11-07T1418Z", "2026-11-08T1411Z"):
    s = json.load(open(os.path.join(D, "raw-" + lab, "stats-1.derived.json")))["extracted"]["shares"]
    below = sum(v for k, v in s.items() if vt(k) < (4, 7))
    print(lab, "7.1 %.3f; 7.1+7.0+6.9 %.3f; below 4.7 %.3f" % (s["7.1"], s["7.1"] + s["7.0"] + s["6.9"], below))

print("\n== 7. One-off read: hashes ==")
import csv, hashlib
o = os.path.join(D, "oneoff-2026-11-22T1514Z")
for r in csv.DictReader(open(os.path.join(o, "readlog.csv"))):
    p = os.path.join(o, r["name"] + ".body")
    held = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else "body not committed"
    print(r["name"], r["utc_start"], r["status"], r["size"], "log", r["sha256"][:16], "held", held[:16])
