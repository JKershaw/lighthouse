#!/usr/bin/env python3
"""LH039 record 1.0 to 1.2 (22 November 2026): measure 1 and measure 2 with E3 settled, and the post hoc treatments.

Offline: reads only retained files under studies/LH039/data/ (and LH033's tables.json for measure 2);
fetches nothing. Uses tabulate.py's parser and branch rule.

E3, from the one-off read after collection stopped (data/oneoff-2026-11-22T1514Z/feed.facts.json and
archive.facts.json): WordPress published 7.1.5 at 2026-11-18T17:08:59Z (release feed pubDate), and 7.0.9
and 6.9.12 on 18 November 2026 (release archive, date only). No 7.1.6 on either page as read.

  Part A, measure 1 as the brief wrote it, with E3 settled: fixed = 7.1.4, 7.0.8, 6.9.11 or later; the
    W3Techs 7.1.5 label held apart "while it does not" resolve to a published release, so apart at every
    read taken before 2026-11-18T17:08:59Z (reads to 2026-11-18T1415Z) and fixed from the read of
    2026-11-19T1417Z; 7.1.6 counted fixed, since the brief's exception names only 7.1.5.
  Part B, post hoc treatments, chosen after the reads were seen (6 in all: 4 on 7.1, 1 each on 7.0 and 6.9):
    7.1 (i) 7.1.6 also held apart, by analogy with the brief's 7.1.5 rule; (ii) 7.1.5 apart at every read
    (checkpoint 2's figure); (iii) 7.1.5 counted fixed at every read, the earlier labels included;
    (iv) 7.1.4 alone. 7.0 and 6.9: the E0 release alone (7.0.8, 6.9.11).
  Part C, measure 2 with Part A's 7.1 figure at day 14 and day 24, beside LH033's tabulated W3Techs shares
    for PHP 8.2 to 8.5 at its reads of PHP day 12, 19 and 26 (reuse disclosed; recomputation by LH039's
    rule is in checkpoints/2026-11-21-extra.txt, Part A).
  Part D, Packagist (measure 3) on 18 and 19 November from the checkpoint CSV, with the coverage note.
Usage: python3 -I studies/LH039/scripts/record_measures.py   (writes studies/LH039/record-1.2-output.txt; record 1.0's and 1.1's outputs are in git history)
"""
import csv, datetime, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tabulate as T  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LH033 = os.path.join(ROOT, "studies", "LH033", "data")
ONEOFF = os.path.join(T.DATA, "oneoff-2026-11-22T1514Z")
out = []


def p(s=""):
    out.append(s)


def rows_of(label, branch):
    rd = os.path.join(T.DATA, "raw-" + label)
    n = "w3-%s" % branch.replace(".", "")
    path = os.path.join(rd, n + ".body")
    return T.w3_release_shares(path) if os.path.exists(path) else T.w3_release_shares_derived(T.derived(rd, n))


def ratio(rows, is_fixed, apart=()):
    nlo = nhi = olo = ohi = 0.0
    for v, lo, hi, _ in rows:
        if v in apart:
            continue
        if is_fixed(v):
            nlo += lo; nhi += hi
        else:
            olo += lo; ohi += hi
    return nlo / (nlo + ohi), nhi / (nhi + olo)


def rng(r):
    a, b = 100 * r[0], 100 * r[1]
    return "%.2f%%" % a if abs(a - b) < 0.005 else "%.2f%% to %.2f%%" % (a, b)


def later(branch):
    return lambda v: T.vt(v) >= T.FIXED[branch]


feed = json.load(open(os.path.join(ONEOFF, "feed.facts.json")))
arch = json.load(open(os.path.join(ONEOFF, "archive.facts.json")))
rel = [i for i in feed["extracted"]["items"] if i["title"].startswith("WordPress 7.1.5")]
E3 = datetime.datetime(2026, 11, 18, 17, 8, 59)
p("LH039 record 1.0, offline tables. Reads only retained files.")
p("")
p("== E3 (supply), one-off read after collection stopped, %s and %s ==" % (feed["read_utc"], arch["read_utc"]))
p("release feed item: %s, pubDate %s, link %s" % (rel[0]["title"], rel[0]["pubDate"], rel[0]["link"]))
for v, r in arch["extracted"]["rows_by_release"].items():
    p("release archive %s: %s" % (v, r if r else "not on the page"))
p("E3 used here: 2026-11-18T17:08:59Z (7.1.5, feed); 7.0.9 and 6.9.12 dated 18 November 2026 by the archive (no time).")
p("Day of E3 after E0 (28 October): %d" % (E3.date() - datetime.date(2026, 10, 28)).days)

reads = sorted(os.path.basename(d)[4:] for d in glob.glob(os.path.join(T.DATA, "raw-2026-11-*"))
               if os.path.basename(d)[4:] >= "2026-11-09")
p("")
p("== Part A: measure 1 as the brief wrote it, E3 settled (7.1.5 apart before E3, fixed after; 7.1.6 fixed) ==")
A = {}
for b in T.BRANCHES:
    for lab in reads:
        rows, date = rows_of(lab, b)
        before = T.lab_dt(lab) < E3
        apart = ("7.1.5",) if (b == "7.1" and before) else ()
        A[(b, lab)] = ratio(rows, later(b), apart)
        given = "; ".join("%s %s" % (v, g) for v, _, _, g in rows if v in ("7.1.5", "7.1.6", "7.0.9", "6.9.12"))
        p("%s %s (day %d, page date %s): %s%s%s" % (
            b, lab, (T.lab_dt(lab).date() - T.E0).days, date, rng(A[(b, lab)]),
            "  [7.1.5 apart: read before E3]" if apart else "", ("  labels after E0 release: " + given) if given else ""))

p("")
p("== Part B: post hoc treatments (chosen after the reads were seen; 6 in all) ==")
for lab in reads:
    rows, _ = rows_of(lab, "7.1")
    before = T.lab_dt(lab) < E3
    i = ratio(rows, later("7.1"), ("7.1.5", "7.1.6") if before else ("7.1.6",))
    ii = ratio(rows, later("7.1"), ("7.1.5",))
    iii = ratio(rows, later("7.1"), ())
    iv = ratio(rows, lambda v: v == "7.1.4", ())
    p("7.1 %s  brief %s | (i) 7.1.6 apart %s | (ii) 7.1.5 apart throughout %s | (iii) 7.1.5 fixed throughout %s | (iv) 7.1.4 alone %s" % (
        lab, rng(A[("7.1", lab)]), rng(i), rng(ii), rng(iii), rng(iv)))
for b, r0 in (("7.0", "7.0.8"), ("6.9", "6.9.11")):
    for lab in reads:
        rows, _ = rows_of(lab, b)
        p("%s %s  brief %s | %s alone %s" % (b, lab, rng(A[(b, lab)]), r0, rng(ratio(rows, lambda v, r0=r0: v == r0, ()))))

p("")
p("== Part C: measure 2, the comparison named in advance (LH033 reuse disclosed) ==")
for lab, day in (("2026-11-11T1415Z", 14), ("2026-11-21T1411Z", 24)):
    p("WordPress 7.1, read %s (day %d): brief, E3 settled %s; checkpoint 2 (7.1.5 apart throughout) %s" % (
        lab, day, rng(A[("7.1", lab)]), rng(ratio(rows_of(lab, "7.1")[0], later("7.1"), ("7.1.5",)))))
for lab, day in (("2026-11-02T1530Z", 12), ("2026-11-09T1427Z", 19), ("2026-11-16T1419Z", 26)):
    t = json.load(open(os.path.join(LH033, "read-" + lab, "tables.json")))["m4_w3techs_within_minor"]
    p("PHP, LH033 read %s (PHP day %d), tabulated share at or above the fixed patch: %s" % (
        lab, day, ", ".join("%s %.1f%%" % (m, t[m]["share_at_or_above_fixed_pct"]) for m in ("8.2", "8.3", "8.4", "8.5"))))

p("")
p("== Part D: Packagist (measure 3), 17 to 19 November, from checkpoints/2026-11-21-packagist.csv ==")
p("7.1.5, 7.0.9 and 6.9.12 were not among the releases read; WordPress published them on 18 November (7.1.5 at 17:08:59Z),")
p("so 18 November's shares cover about 17 of its 24 hours fully and are a lower bound after that, and 19 November's are a lower bound.")
cs = list(csv.DictReader(open(os.path.join(HERE, "..", "checkpoints", "2026-11-21-packagist.csv"))))
for r in cs:
    if r["utc_day"] in ("2026-11-17", "2026-11-18", "2026-11-19"):
        p("%s %s %s (day %s): fixed %s of %s = %.1f%%" % (r["package"], r["branch"], r["utc_day"], r["days_since_E0"],
          r["fixed_downloads"], r["branch_downloads"], 100 * float(r["fixed_share"])))

p("")
p("== Part E (added in record 1.1, 22 November 2026): measure 2 position, WordPress 7.1 against each PHP branch ==")
p("above = WordPress's lower bound above PHP's tabulated value; below = WordPress's upper bound below it")
PHP = {}
for lab, day in (("2026-11-02T1530Z", 12), ("2026-11-09T1427Z", 19), ("2026-11-16T1419Z", 26)):
    t = json.load(open(os.path.join(LH033, "read-" + lab, "tables.json")))["m4_w3techs_within_minor"]
    PHP[day] = {m: t[m]["share_at_or_above_fixed_pct"] for m in ("8.2", "8.3", "8.4", "8.5")}
for wlab, wday, pdays in (("2026-11-09T1431Z", 12, (12,)), ("2026-11-16T1418Z", 19, (19,)),
                          ("2026-11-11T1415Z", 14, (12, 19)), ("2026-11-21T1411Z", 24, (19, 26))):
    lo, hi = (100 * x for x in A[("7.1", wlab)])
    for pd in pdays:
        pos = ", ".join("%s %s" % (m, "above" if lo > v else "below" if hi < v else "overlaps")
                        for m, v in PHP[pd].items())
        p("WordPress day %d (%s) vs PHP day %d: %s" % (wday, rng(A[("7.1", wlab)]), pd, pos))

p("")
p("== Part F (added in record 1.1): Packagist days below half, counting only days with full coverage (to 17 November) ==")
for pk in ("roots", "johnpbloch"):
    for b in T.BRANCHES:
        d = [r for r in cs if r["package"] == pk and r["branch"] == b and 0 <= int(r["days_since_E0"]) and r["utc_day"] <= "2026-11-17"]
        below = sum(1 for r in d if float(r["fixed_share"]) < 0.5)
        p("%s %s, 28 October to 17 November: below half on %d of %d days" % (pk, b, below, len(d)))
p("Weekend dips (both Saturday and Sunday branch totals below the Friday and the Monday), 5 weekends from 17 October:")
for pk in ("roots", "johnpbloch"):
    for b in T.BRANCHES:
        s = {r["utc_day"]: int(r["branch_downloads"]) for r in cs if r["package"] == pk and r["branch"] == b}
        res = []
        for sat in ("2026-10-17", "2026-10-24", "2026-10-31", "2026-11-07", "2026-11-14"):
            d0 = datetime.date.fromisoformat(sat)
            f, su, m = (str(d0 + datetime.timedelta(k)) for k in (-1, 1, 2))
            res.append("%s %s" % (sat[5:], "dip" if max(s[sat], s[su]) < min(s[f], s[m]) else "no dip"))
        p("%s %s: %s" % (pk, b, ", ".join(res)))

p("")
p("== Part G (added in record 1.2, after R-0118; all post hoc, chosen after the reads were seen) ==")
p("G1. Least-squares line through the E0 release's share of its branch as W3Techs gives it (0.1-point precision),")
p("    reads of days 12 to 21 (9 to 18 November, before the second release); the day at which the line crosses zero.")
first = [lab for lab in reads if T.lab_dt(lab) < E3]
for b, r0 in (("7.1", "7.1.4"), ("7.0", "7.0.8"), ("6.9", "6.9.11")):
    xs, ys = [], []
    for lab in first:
        rows, _ = rows_of(lab, b)
        v = [hi for (rv, lo, hi, g) in rows if rv == r0]
        xs.append((T.lab_dt(lab).date() - T.E0).days); ys.append(v[0])
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    ic = my - sl * mx
    res = max(abs(y - (ic + sl * x)) for x, y in zip(xs, ys))
    p("    %s: values %s; slope %.2f points a day, intercept %.2f, zero at day %.1f, largest residual %.2f; line at day 4: %.1f" % (
        r0, ", ".join("%.1f" % y for y in ys), sl, ic, -ic / sl, res, ic + 4 * sl))
p("G2. W3Techs history pages, read 21 November: releases the fix replaced, 1 November -> 21 November (share of branch)")
for b in T.BRANCHES:
    h = T.history_of(os.path.join(T.DATA, "raw-2026-11-21T1411Z"), "w3h-%s" % b.replace(".", ""))
    cols, hrows = h
    for name, cells in hrows:
        v = name.replace("version ", "")
        if T.vt(v)[:2] == T.vt(b)[:2] and T.vt(v) < T.FIXED[b]:
            first_col = next((c for c in cols if cells.get(c)), "")
            p("    %s: 1 Nov %s -> 21 Nov %s (first column with a value: %s)" % (
                v, cells.get("1 Nov 2026") or "(blank)", cells.get("21 Nov 2026") or "(blank)", first_col))
p("G3. Branch-matched comparison with PHP (LH033 tabulated): each WordPress branch at each pairing, 9 comparisons")
p("    (WordPress day 12 v PHP day 12, day 19 v day 19, day 24 v day 26), plus 7.1 v 8.5 at the record's other pairings")
pairs = (("2026-11-09T1431Z", 12, 12), ("2026-11-16T1418Z", 19, 19), ("2026-11-21T1411Z", 24, 26))
for lab, wd, pd in pairs:
    for b in T.BRANCHES:
        lo, hi = (100 * x for x in A[(b, lab)])
        below = [m for m, v in PHP[pd].items() if hi < v]
        above = [m for m, v in PHP[pd].items() if lo > v]
        p("    WordPress %s day %d (%s) v PHP day %d: below %s; above %s; v 8.5: %+.1f to %+.1f points" % (
            b, wd, rng(A[(b, lab)]), pd, ",".join(below) or "none", ",".join(above) or "none",
            lo - PHP[pd]["8.5"], hi - PHP[pd]["8.5"]))
for lab, wd, pd in (("2026-11-11T1415Z", 14, 12), ("2026-11-11T1415Z", 14, 19), ("2026-11-21T1411Z", 24, 19)):
    lo, hi = (100 * x for x in A[("7.1", lab)])
    p("    WordPress 7.1 day %d v PHP 8.5 day %d: %+.2f to %+.2f points" % (wd, pd, lo - PHP[pd]["8.5"], hi - PHP[pd]["8.5"]))
p("G4. Within-branch movements on 7.0 between the reads of 9 and 21 November (W3Techs as given)")
r9 = {v: g for v, lo, hi, g in rows_of("2026-11-09T1431Z", "7.0")[0]}
r21 = {v: g for v, lo, hi, g in rows_of("2026-11-21T1411Z", "7.0")[0]}
for v in ("7.0.4", "7.0.6", "7.0.7"):
    a, z = float(r9[v].rstrip("%")), float(r21[v].rstrip("%"))
    p("    %s: %s -> %s (factor %.2f)" % (v, r9[v], r21[v], z / a))

txt = "\n".join(out) + "\n"
open(os.path.join(HERE, "..", "record-1.2-output.txt"), "w").write(txt)
print(txt)
