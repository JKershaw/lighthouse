#!/usr/bin/env python3
"""LH039 checkpoint 2 (21 November 2026): measure 2 and the sensitivity tables, offline.

Reads only retained files; fetches nothing.
  Part A, measure 2 (brief, pre-set): W3Techs fixed share on 7.1 at the read nearest day 14 after E0
    (2026-11-11T1415Z) and at the last read (2026-11-21T1411Z, day 24), from LH039's own reads by
    tabulate.py's functions; beside LH033's W3Techs share at or above the fixed patch for PHP 8.2 to 8.5
    (PHP day 0 = 21 October 2026), at the LH033 W3Techs reads nearest PHP day 14 and day 24. LH033
    read W3Techs only on 25 and 26 October and 2, 9, 16 and 21 November (PHP days 4, 5, 12, 19, 26, 31),
    so no LH033 read falls on PHP day 14 or 24. Two forms of the PHP figure are given: LH033's own
    tabulated value (studies/LH033/data/read-*/tables.json, "less than 0.1%" counted as 0, sum of the
    shares at or above the fixed patch) and a recomputation from LH033's retained raw W3Techs pages by
    LH039's rule (fixed shares over the sum of listed shares, "less than 0.1%" as [0, 0.1)).
  Part B, post hoc (chosen after the reads were seen): the same-day matches that do exist, WordPress
    day 12 and 19 (9 and 16 November) beside PHP day 12 and 19 (2 and 9 November).
  Part C, post hoc sensitivity of measure 1 to the labels that appeared during the window
    (7.1.5 rising from 19 November, 7.1.6, 7.0.9, 6.9.12).
  Part D, observation: Packagist branch totals read per day, 12 to 19 November, to show where the
    per-version reads stop covering the branch (7.1.5, 7.0.9 and 6.9.12 were not among the releases read).
Usage: python3 -I studies/LH039/scripts/checkpoint2_extra.py
"""
import glob, gzip, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tabulate as T  # LH039's own committed tabulator, for its W3Techs parser and ratio rule  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LH033 = os.path.join(ROOT, "studies", "LH033", "data")
PHP_FIXED = {"8.2": 35, "8.3": 36, "8.4": 27, "8.5": 12}  # LH033 brief: 8.2.35, 8.3.36, 8.4.27, 8.5.12
PHP_DAY0 = (2026, 10, 21)
out = []


def p(s=""):
    out.append(s)


def wp_ratio(label, branch, apart=("7.1.5",), fixed=None):
    path = os.path.join(T.DATA, "raw-" + label, "w3-%s.body" % branch.replace(".", ""))
    rows, date = T.w3_release_shares(path)
    fx = fixed or T.FIXED[branch]
    nlo = nhi = olo = ohi = 0.0
    for v, lo, hi, _ in rows:
        if v in apart:
            continue
        if fx(v) if callable(fx) else T.vt(v) >= fx:
            nlo += lo; nhi += hi
        else:
            olo += lo; ohi += hi
    return nlo / (nlo + ohi), nhi / (nhi + olo), date


def php_raw(label, minor):
    t = gzip.open(os.path.join(LH033, "read-" + label, "w3techs-details-%s.raw.gz" % minor)).read().decode("utf8", "replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    part = t[t.find("Subversions of PHP " + minor):]
    part = part[part.find("How to read the diagram"):]
    part = part[part.find("%") + 1:]
    part = part[:part.find("W3Techs.com,")]
    date = re.search(r"W3Techs\.com, (\d+ \w+ \d{4})", t)
    nlo = nhi = olo = ohi = 0.0
    n = 0
    for m in re.finditer(r"Version " + re.escape(minor) + r"\.(\d+) (?:([\d.]+)%|(less than 0\.1%))", part):
        n += 1
        lo, hi = (0.0, 0.1) if m.group(3) else (float(m.group(2)),) * 2
        if int(m.group(1)) >= PHP_FIXED[minor]:
            nlo += lo; nhi += hi
        else:
            olo += lo; ohi += hi
    return nlo / (nlo + ohi), nhi / (nhi + olo), (date.group(1) if date else ""), n, nhi


def php_tab(label, minor):
    t = json.load(open(os.path.join(LH033, "read-" + label, "tables.json")))
    return t["m4_w3techs_within_minor"][minor]


def rng(lo, hi):
    a, b = 100 * lo, 100 * hi
    return "%.2f%%" % a if abs(a - b) < 0.005 else "%.2f%% to %.2f%%" % (a, b)


def php_block(label, day):
    p("  PHP, LH033 read %s (PHP day %d), files studies/LH033/data/read-%s/w3techs-details-8.x.raw.gz and tables.json:" % (label, day, label))
    for m in PHP_FIXED:
        lo, hi, date, n, _ = php_raw(label, m)
        tb = php_tab(label, m)
        p("    %s: LH033 tabulated %.1f%% (page date %s, %d rows); recomputed by LH039's rule %s" % (
            m, tb["share_at_or_above_fixed_pct"], tb["w3techs_date"], tb["listed_rows"], rng(lo, hi)))


p("LH039 checkpoint 2 extra tables. Offline; reads only retained files.")
p("")
p("== Part A: measure 2, the comparison named in advance ==")
for lab, day in (("2026-11-11T1415Z", 14), ("2026-11-21T1411Z", 24)):
    lo, hi, date = wp_ratio(lab, "7.1")
    p("WordPress 7.1, LH039 read %s (day %d after E0, page date %s): fixed share %s (7.1.5 apart, per brief)" % (lab, day, date, rng(lo, hi)))
PHP_READS = {"2026-10-25T0855Z": 4, "2026-10-26T0637Z": 5, "2026-11-02T1530Z": 12, "2026-11-09T1427Z": 19,
             "2026-11-16T1419Z": 26, "2026-11-21T1414Z": 31}
p("LH033 W3Techs reads held (label: PHP day): " + ", ".join("%s: %d" % kv for kv in PHP_READS.items()))
p("Nearest to PHP day 14: day 12 (2 Nov, 2 days early); next is day 19 (5 days late).")
p("Nearest to PHP day 24: day 26 (16 Nov, 2 days late); previous is day 19 (5 days early).")
for lab in ("2026-11-02T1530Z", "2026-11-09T1427Z", "2026-11-16T1419Z"):
    php_block(lab, PHP_READS[lab])
p("")
p("== Part B (post hoc, not pre-set; 2 comparisons): exact same-day matches that exist ==")
for lab, day in (("2026-11-09T1431Z", 12), ("2026-11-16T1418Z", 19)):
    lo, hi, date = wp_ratio(lab, "7.1")
    p("WordPress 7.1, LH039 read %s (day %d): %s" % (lab, day, rng(lo, hi)))
p("PHP at day 12 and 19: the LH033 reads 2026-11-02T1530Z and 2026-11-09T1427Z in Part A.")
p("")
p("== Part C (post hoc sensitivity, chosen after the reads were seen): measure 1 under other label treatments ==")
reads = sorted(os.path.basename(d)[4:] for d in glob.glob(os.path.join(T.DATA, "raw-2026-11-1[5-9]*")) + glob.glob(os.path.join(T.DATA, "raw-2026-11-2*")))
for lab in reads:
    a = wp_ratio(lab, "7.1")
    b = wp_ratio(lab, "7.1", apart=("7.1.5", "7.1.6"))
    c = wp_ratio(lab, "7.1", apart=())
    p("7.1 %s  tabulator (7.1.5 apart, 7.1.6 fixed) %s | 7.1.5 and 7.1.6 both apart %s | 7.1.5 and 7.1.6 counted fixed %s | 7.1.4 alone: %s" % (
        lab, rng(a[0], a[1]), rng(b[0], b[1]), rng(c[0], c[1]),
        rng(*wp_ratio(lab, "7.1", apart=(), fixed=lambda v: v == "7.1.4")[:2])))
for br, rel in (("7.0", "7.0.8"), ("6.9", "6.9.11")):
    for lab in reads:
        a = wp_ratio(lab, br, apart=())
        e = wp_ratio(lab, br, apart=(), fixed=lambda v, rel=rel: v == rel)
        p("%s %s  tabulator (any later release fixed) %s | %s alone %s" % (br, lab, rng(a[0], a[1]), rel, rng(e[0], e[1])))
p("")
p("== Part D (observation): Packagist branch downloads read per day, packagist-2026-11-21T1415Z ==")
p("Releases read: 7.1.0 to 7.1.4, 7.0.0 to 7.0.8, 6.9.0 to 6.9.11 (packagist.py VERSIONS; no --extra).")
d = os.path.join(T.DATA, "packagist-2026-11-21T1415Z")
for pkg in ("roots", "johnpbloch"):
    for br in T.BRANCHES:
        tot = {}
        for f in glob.glob(os.path.join(d, "%s-%s.*.json" % (pkg, br))):
            j = json.load(open(f))
            for day, v in zip(j["labels"], list(j["values"].values())[0]):
                tot[day] = tot.get(day, 0) + v
        days = [x for x in sorted(tot) if x >= "2026-11-12"]
        p("%s %s: %s" % (pkg, br, ", ".join("%s %d" % (x[5:], tot[x]) for x in days)))

txt = "\n".join(out) + "\n"
open(os.path.join(HERE, "..", "checkpoints", "2026-11-21-extra.txt"), "w").write(txt)
print(txt)
