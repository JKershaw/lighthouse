"""R-0091: independent check of studies/LH038/LH038.md version 0.1 against the
retained bodies. Written by the evidence reviewer without reusing timeline.py's
code. Standard library only; reads retained files, fetches nothing.

Replay (from the repository root):
  python3 -I studies/LH038/review/r0091_check.py > studies/LH038/review/r0091_check_output.txt
"""
import datetime as dt
import email.utils
import gzip
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
S = ROOT / "studies" / "LH038"
READ = S / "data" / "read-2026-11-17T1419Z"
POL = S / "data"
L36 = ROOT / "studies" / "LH036" / "data" / "read-2026-11-16T1419Z"
UTC = dt.timezone.utc
CVE = "CVE-2026-98432"
checks = []


def ok(label, cond, detail=""):
    checks.append((label, bool(cond)))
    print(("PASS " if cond else "FAIL ") + label + (f"  [{detail}]" if detail else ""))


def raw(path):
    return gzip.open(path).read().decode("utf-8", "replace")


def text(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    h = h.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", h).strip()


def norm(q):
    return re.sub(r"\s+", " ", q.replace("\u2019", "'")).strip()


def days(a, b):
    return (b - a).days


# 1. Counts from the read log
print("== 1. read log counts")
log = json.load(open(READ / "read_log.json"))
by = {r["name"]: r for r in log}
st = [r.get("status") for r in log]
n200 = sum(1 for s in st if s == 200)
# A body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md) is
# counted as kept through the <name>.derived.json that replaced it (scripts/derive_kept.py).
files = sorted({p.name for p in READ.glob("*.raw.gz")} | {p.name[:-len(".derived.json")] + ".raw.gz" for p in READ.glob("*.derived.json")})
kept200 = [r["name"] for r in log if r.get("status") == 200 and ((READ / f"{r['name']}.raw.gz").exists() or (READ / f"{r['name']}.derived.json").exists())]
not_fetched = [r for r in log if r.get("status") is None]
print("targets", len(log), "status 200", n200, "status 403", st.count(403), "not fetched", len(not_fetched),
      "raw files on disk", len(files), "200 bodies kept", len(kept200))
ok("80 targets", len(log) == 80)
ok("51 answered HTTP 200", n200 == 51)
ok("50 HTTP-200 bodies kept (7.3 over ceiling)", len(kept200) == 50 and "changelog_7.3" not in kept200)
empty = []
for n in kept200:
    if not (READ / f"{n}.raw.gz").exists():
        if json.load(open(READ / f"{n}.derived.json"))["extracted"].get("challenge_page"):
            empty.append(n)
        continue
    t = raw(READ / f"{n}.raw.gz")
    if "I Challenge Thee" in t or (n == "ref_nvd_detail" and "NVD - Home" in t and CVE not in t):
        empty.append(n)
print("no source content:", empty)
ok("46 of 50 hold source content (3 Debian challenges, NVD shell)", len(kept200) - len(empty) == 46 and len(empty) == 4)
ok("10 bodies kept from HTTP 403 as well (60 files in all)", len(files) == 60)
reasons = {}
for r in not_fetched:
    reasons.setdefault(r["robots"]["reason"], []).append(r["name"])
for k, v in reasons.items():
    print(" not fetched:", k, len(v), v[:3], "...")
gh = raw(READ / "upstream_e3f33b0a1d89.raw.gz")
ok("GitHub 403 body is the session's access layer, not GitHub", "not enabled for this session" in gh)
fol = json.load(open(S / "follow.json"))
ub = [k for k in fol if k.startswith("ubuntu_")]
ub_usn = [k for k in ub if "USN" in k]
print("follow.json entries", len(fol), "ubuntu", len(ub), "of which USNs", len(ub_usn))
ok("follow.json has 52 entries", len(fol) == 52)
ok("Ubuntu followed = 14 notices + 1 blog post (record says '15 notices')", len(ub_usn) == 14 and len(ub) == 15)

# 2. the follow rule's 244 from LH036's read of 16 November
print("== 2. follow rule total from LH036's read of 16 November")
rh = json.loads(gzip.open(L36 / "redhat.raw.gz").read())
rh_ids = sorted({a["advisory"] for a in rh.get("affected_release", []) if a.get("advisory")})
su = raw(L36 / "suse.raw.gz").lower()
su_ids = sorted(set(re.findall(r"suse-su-\d+-\d+", su)))
lib = sorted(set(re.findall(r"suse-liberty-linux-updates/[^\"<> ]+", raw(L36 / "suse.raw.gz"))))
ubj = json.loads(gzip.open(L36 / "ubuntu.raw.gz").read())
usn = [x if isinstance(x, str) else x.get("id") for x in ubj.get("notices", [])]
blog = 1 if "proposed-pocket" in raw(L36 / "ubuntu.raw.gz") else 0
refs = [k for k in fol if k.startswith("ref_")]
tot = len(rh_ids) + len(su_ids) + len(lib) + len(usn) + blog + len(refs)
print("RH", len(rh_ids), "SUSE-SU", len(su_ids), "Liberty", len(lib), "USN", len(usn), "blog", blog, "refs", len(refs), "total", tot)
ok("rule names 244", tot == 244)
nf_su = len(su_ids) + len(lib) - sum(1 for k in fol if k.startswith("suse_"))
nf_rh = len(rh_ids) - sum(1 for k in fol if k.startswith("redhat_"))
nf_ub = len(usn) + blog - len(ub)
print("not followed: SUSE", nf_su, "Red Hat", nf_rh, "Ubuntu", nf_ub, "total", nf_su + nf_rh + nf_ub)
ok("192 not followed = 174 SUSE + 12 Red Hat + 6 Ubuntu", (nf_su, nf_rh, nf_ub) == (174, 12, 6))

# 3. T1 and T4 from the changelogs, parsed by a different route
print("== 3. T1/T4 changelogs")
rel = {}
fixes = set()
for p in sorted(READ.glob("changelog_*.raw.gz")):
    ver = p.name[len("changelog_"):-len(".raw.gz")]
    t = raw(p)
    # release commit: the block whose message body is exactly 'Linux <ver>'
    m = re.search(r"^commit ([0-9a-f]{40})\nAuthor:[^\n]*\nDate:\s+([^\n]+)\n\n\s+Linux " + re.escape(ver) + r"\n", t, re.M)
    rd = email.utils.parsedate_to_datetime(
        re.sub(r"^(\w+) (\w+) +(\d+) (\S+) (\d+) (\S+)$", r"\1, \3 \2 \5 \4 \6", m.group(2).strip())).astimezone(UTC)
    blocks = t.split("\ncommit ")
    fb = [b for b in blocks if "commit e3f33b0a1d89d738e2b913dab519226eaf76e15b upstream." in b]
    fd = re.search(r"^Date:\s+([^\n]+)", fb[0], re.M).group(1).strip()
    fdt = dt.datetime.strptime(fd, "%a %b %d %H:%M:%S %Y %z").astimezone(UTC)
    rb = re.search(r"^\s+Reported-by:([^\n]*)", fb[0], re.M)
    has_date = bool(re.search(r"\d{4}-\d\d-\d\d|20\d\d", rb.group(1))) if rb else None
    fixes.add(fdt)
    rel[ver] = rd
    print(f"{ver}: release {rd:%Y-%m-%d %H:%M:%S} UTC; fix blocks {len(fb)}; fix author {fdt:%Y-%m-%d %H:%M:%S} UTC; "
          f"Reported-by present {bool(rb)}, carries a date {has_date}; Last-Modified {by['changelog_'+ver]['last_modified']}")
ok("seven changelogs read, one fix author date 2026-10-01 22:12:53Z",
   len(rel) == 7 and fixes == {dt.datetime(2026, 10, 1, 22, 12, 53, tzinfo=UTC)})
exp = {"6.18.56": "2026-10-11 13:26", "7.2.10": "2026-10-11 13:27", "6.12.113": "2026-10-15 09:56",
       "5.10.272": "2026-10-15 12:13", "5.15.223": "2026-10-15 12:14", "6.1.190": "2026-10-15 12:15",
       "6.6.159": "2026-10-15 12:16"}
ok("release-commit times as the record states", all(f"{rel[v]:%Y-%m-%d %H:%M}" == exp[v] for v in exp))
print("7.3:", by["changelog_7.3"]["status"], by["changelog_7.3"]["bytes"], "bytes, no body:", not (READ / "changelog_7.3.raw.gz").exists())
t3 = dt.datetime(2026, 10, 15, 12, 8, 22, tzinfo=UTC)
lm_old = [email.utils.parsedate_to_datetime(by[f"changelog_{v}"]["last_modified"]) for v in ("5.10.272", "5.15.223", "6.1.190", "6.6.159")]
print("older four Last-Modified minus T3 (minutes):", sorted(round((x - t3).total_seconds() / 60, 1) for x in lm_old))
ok("CVE published before each older changelog's Last-Modified", all(x > t3 for x in lm_old))

# 4. T5
print("== 4. T5 advisories")
suse = {}
for p in sorted(READ.glob("suse_suse_su_*.raw.gz")):
    tx = text(raw(p))
    d = re.search(r"Release Date:\s*(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)", tx).group(1)
    kernel = "Security update for the Linux Kernel" in tx or "Linux Kernel" in tx[:5000]
    ncve = len(set(re.findall(r"CVE-\d{4}-\d+", tx)))
    suse[p.name] = dt.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    print(f"{p.name[:-7]}: Release Date {d}; names {CVE}: {CVE in tx}; distinct CVEs on page {ncve}; kernel title {kernel}")
ok("12 SUSE advisories, all name the CVE", len(suse) == 12)
d24 = sorted(k for k, v in suse.items() if v.date() == dt.date(2026, 10, 24))
ok("four SUSE advisories dated 24 October, eight 2 November",
   len(d24) == 4 and sum(1 for v in suse.values() if v.date() == dt.date(2026, 11, 2)) == 8)
for p in sorted(READ.glob("suse_liberty_*.raw.gz")):
    h = raw(p)
    print(p.name[:-7], re.search(r"<I>([^<]+)</I>", h).group(1).strip(), "| equivalent of RHSA:", "functional equivalent of RHSA" in h, "| names CVE:", CVE in h)
rhd = {}
for p in sorted(READ.glob("redhat_*.raw.gz")):
    h = raw(p)
    m = re.search(r"<dl class=\"details\">\s*<dt>[^<]*</dt>\s*<dd>(\d{4}-\d\d-\d\d)</dd>\s*<dt>[^<]*</dt>\s*<dd>(\d{4}-\d\d-\d\d)</dd>", h)
    rhd[p.name[:-7]] = (m.group(1), m.group(2))
    print(p.name[:-7], "issued", m.group(1), "updated", m.group(2), "| names CVE:", CVE in h)
first_rh = min(dt.date.fromisoformat(v[0]) for v in rhd.values())
ok("15 Red Hat errata; earliest issued 1 November (four of them)", len(rhd) == 15 and first_rh == dt.date(2026, 11, 1)
   and sum(1 for v in rhd.values() if v[0] == "2026-11-01") == 4)
ok("latest update read is 13 November (RHSA-2026:95416)", max(v[1] for v in rhd.values()) == "2026-11-13")

# 5. T6 the post
print("== 5. T6 the post")
ph = raw(READ / "anthropic_post.raw.gz")
pub = re.search(r'"datePublished"\s*:\s*"([^"]+)"', ph).group(1)
mod = re.search(r'"dateModified"\s*:\s*"([^"]+)"', ph).group(1)
print("datePublished", pub, "dateModified", mod)
ok("datePublished midnight 27 Oct; dateModified 30 Oct 15:24:16Z",
   pub.startswith("2026-10-27T00:00:00") and mod.startswith("2026-10-30T15:24:16"))
print("tags in whole page: pre", len(re.findall(r"<pre\b", ph)), "code", len(re.findall(r"<code\b", ph)),
      "img/figure/video in Linux section:", end=" ")
a = ph.find("remote code execution in Linux")
z = ph.find("What we learned", a)
print(re.findall(r"<(img|figure|video|svg|pre|code)\b", ph[a:z]))
pt = text(ph)
for q in ["We reported each vulnerability to the affected vendor under our coordinated vulnerability disclosure",
          "gives developers 90 days to patch and a further 45 days before we discuss details beyond what is already included in a public advisory",
          "a remote attacker to send packets to Linux servers with a multipath TCP listener to run arbitrary commands as root",
          "In our proof of concept, it takes 48 minutes to leak a kernel pointer and another five minutes to reach the shell command execution",
          "was patched upstream and backported to all maintained stable kernel branches"]:
    ok("post quote verbatim: " + q[:60] + "...", norm(q) in pt)
i = pt.find("a remote attacker to send packets")
print("post continues:", pt[i - 40:i + 160])
ok("post section names no report date for this flaw", not re.search(r"reported (it |this )?(on|in) ", pt[pt.find("remote code execution in Linux While"):pt.find("What we learned")]))

# 6. T7 oss-security
print("== 6. T7 oss-security")
for p in sorted(READ.glob("ref_oss_security_*.raw.gz")):
    h = html.unescape(raw(p))
    hdrs = re.findall(r"^Date:\s*(.+)$", h, re.M)
    u = email.utils.parsedate_to_datetime(hdrs[0].strip()).astimezone(UTC)
    print(p.name[:-7], "| first Date:", hdrs[0].strip(), "=", f"{u:%Y-%m-%d %H:%M}", "UTC | inner Date headers:", [x.strip() for x in hdrs[1:]],
          "| links the post:", "discovering-vulnerabilities-with-claude" in h)
matches = []
for mon in ("09", "10", "11"):
    h = raw(READ / f"oss_security_2026_{mon}.raw.gz")
    items = re.findall(r'<li><a href="(\d+/\d+)">(.*?)</a>', h, re.S)
    hit = [(k, re.sub(r"\s+", " ", v)) for k, v in items if re.search(r"CVE-2026-98432|MPTCP|multipath", v, re.I)]
    print(f"2026/{mon}: {len(items)} messages; matches {hit}")
    matches += [f"{mon}/{k}" for k, _ in hit]
    ok(f"2026/{mon}: no {CVE} anywhere in the index except matched subjects",
       h.count(CVE) == sum(1 for _, v in hit if CVE in v))
ok("exactly four matches: 10/30/1, 10/30/6, 10/31/5, 11/03/1", matches == ["10/30/1", "10/30/6", "10/31/5", "11/03/1"])
if (READ / "openwall_distros_stats.raw.gz").exists():
    stt = text(raw(READ / "openwall_distros_stats.raw.gz"))
    ok("distros stats page read is an index, Last modified 2026/02/09, no CVE", "Last modified: 2026/02/09" in stt and CVE not in stt)
else:  # body removed 21 November 2026; the derived file keeps the Last modified line and whether the CVE appears
    e = json.load(open(READ / "openwall_distros_stats.derived.json"))["extracted"]
    ok("distros stats page read is an index, Last modified 2026/02/09, no CVE", e["last_modified_line"] == "Last modified: 2026/02/09" and not e["names_" + CVE])

# 7. policy quotations
print("== 7. policy quotations against retained bodies")
cvd = text(raw(POL / "policies-2026-11-04T1415Z" / "anthropic_cvd.raw.gz"))
sec = text(raw(POL / "policies-2026-11-04T1416Z" / "kernel_security_bugs_docs.raw.gz"))
cve = text(raw(POL / "policies-2026-11-04T1416Z" / "kernel_cve_docs.raw.gz"))
ubu = text(raw(POL / "policies-2026-11-04T1415Z" / "ubuntu_disclosure.raw.gz"))
for src, q in [(cvd, "we would generally wait 45 days before publishing full technical details"),
               (cvd, "if the details are already publicly known through other channels, or if earlier publication would materially help defenders"),
               (cvd, "Last updated Mar 6, 2026"),
               (sec, "from the start of the release process"),
               (sec, "If you resorted to AI assistance to identify a bug, you must treat it as public"),
               (cve, "after a fix is available and applied to a stable kernel tree"),
               (ubu, "held private for at least one week after fixes are published")]:
    ok("policy quote verbatim: " + q[:70], norm(q) in src)
j = cvd.find("materially help defenders")
print("P1 shortening clause continues:", repr(cvd[j:j + 70]))
k = cvd.find("after 90 days")
print("P1 90-day sentence:", repr(cvd[k - 60:k + 60]))
m = cve.find("after a fix is available")
print("P3 sentence:", repr(cve[m - 60:m + 60]))

# 8. elapsed days and +45/+90
print("== 8. elapsed UTC calendar days")
t6 = dt.date(2026, 10, 27)
t1 = dt.date(2026, 10, 1)
fs, ls = dt.date(2026, 10, 11), dt.date(2026, 10, 15)
suse1 = min(suse.values()).date()
for lab, d, want in [("T1 fix author", t1, (26, "2026-11-15", "2026-12-30")),
                     ("first stable 6.18.56", fs, (16, "2026-11-25", "2027-01-09")),
                     ("last stable 6.6.159", ls, (12, "2026-11-29", "2027-01-13")),
                     ("CVE published", t3.date(), (12, "2026-11-29", "2027-01-13"))]:
    got = (days(d, t6), str(d + dt.timedelta(45)), str(d + dt.timedelta(90)))
    print(lab, d, "->", got)
    ok("table row " + lab, got == want)
ok("T1->first stable 10; T1->CVE 14", days(t1, fs) == 10 and days(t1, t3.date()) == 14)
ok("first stable->SUSE 13; last stable->SUSE 9; SUSE->post 3", (days(fs, suse1), days(ls, suse1), days(suse1, t6)) == (13, 9, 3))
ok("first stable->Red Hat 21; post->Red Hat 5", (days(fs, first_rh), days(t6, first_rh)) == (21, 5))
ok("post 12 to 16 days after the stable releases", (days(ls, t6), days(fs, t6)) == (12, 16))
ok("first stable 4 days before CVE", days(fs, t3.date()) == 4)
p1 = dt.date(2026, 10, 30)
print("first oss-security message (UTC 30 Oct) after the post:", days(t6, p1), "days; 29 Oct local:", days(t6, dt.date(2026, 10, 29)))
print("Candidate the brief names but the record omits: earliest followed distribution fix (SUSE)", suse1,
      "-> post", days(suse1, t6), "days; +45 =", suse1 + dt.timedelta(45), "; +90 =", suse1 + dt.timedelta(90))
print("Red Hat earliest", first_rh, ": post precedes it by", days(t6, first_rh), "days")

print()
print(f"{sum(c for _, c in checks)} of {len(checks)} checks pass")
for lab, c in checks:
    if not c:
        print("FAILED:", lab)
