"""LH038 record: extract each event's clock from the retained read of
2026-11-17T1419Z and compute elapsed UTC calendar days against the policy
intervals the brief names. From version 0.4 (21 November 2026) it also applies
the decision rule of the brief's amendment of 20 November per SUSE advisory,
from the retained SUSE clocks read (data/suse-clocks-2026-11-21T1420Z/) and
LH036's retained SUSE CVE page of 16 November (reuse); the output up to that
section is unchanged from version 0.3. Standard library only; reads retained
bodies, fetches nothing.

Replay: python3 -I studies/LH038/scripts/timeline.py > studies/LH038/scripts/timeline_output.txt
"""
import datetime as dt
import email.utils
import gzip
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent
READ = HERE / "data" / "read-2026-11-17T1419Z"
FIX = "e3f33b0a1d89d738e2b913dab519226eaf76e15b"


def body(name):
    return gzip.open(READ / name).read().decode("utf-8", "replace")


def git_date(s):
    return dt.datetime.strptime(s.strip(), "%a %b %d %H:%M:%S %Y %z").astimezone(dt.timezone.utc)


log = {r["name"]: r for r in json.load(open(READ / "read_log.json"))}
print("read log entries:", len(log))
statuses = {}
for r in log.values():
    statuses[str(r.get("status"))] = statuses.get(str(r.get("status")), 0) + 1
print("status counts:", dict(sorted(statuses.items())))
print()

# T1 and T4: stable changelogs
print("== T1/T4 from stable changelogs")
rel, fixdates = {}, set()
for name in sorted(n for n in log if n.startswith("changelog_")):
    ver = name[len("changelog_"):]
    if not (READ / (name + ".raw.gz")).exists():
        print(f"{ver}: no body retained (status {log[name].get('status')}, bytes {log[name].get('bytes')}, Last-Modified {log[name].get('last_modified')})")
        continue
    t = body(name + ".raw.gz")
    commits = re.split(r"^commit [0-9a-f]{40}\n", t, flags=re.M)[1:]
    first = commits[0]
    rdate = git_date(re.search(r"^Date:(.*)$", first, re.M).group(1))
    assert re.search(r"^\s+Linux " + re.escape(ver) + r"\s*$", first, re.M), ver
    fx = [c for c in commits if f"commit {FIX} upstream" in c]
    assert len(fx) == 1, (ver, len(fx))
    fdate = git_date(re.search(r"^Date:(.*)$", fx[0], re.M).group(1))
    fixdates.add(fdate)
    rel[ver] = rdate
    print(f"{ver}: release commit author {rdate:%Y-%m-%d %H:%M} UTC; commits in changelog {len(commits)}; "
          f"fix author {fdate:%Y-%m-%d %H:%M:%S} UTC; Last-Modified {log[name].get('last_modified')}")
print("distinct fix author dates:", sorted(str(d) for d in fixdates))
t1 = min(fixdates)
print()

# T5: SUSE and Red Hat
print("== T5 SUSE (Release Date)")
suse = {}
for name in sorted(n for n in log if n.startswith("suse_suse_su_")):
    t = body(name + ".raw.gz")
    m = re.search(r"Release Date:</th>\s*<td>([^<]+)</td>", t)
    d = dt.datetime.strptime(m.group(1).strip(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    suse[name] = d
    print(f"{name}: {d:%Y-%m-%d %H:%M:%S}Z; names the CVE {t.count('CVE-2026-98432')} times")
print("== T5 SUSE Liberty list posts")
for name in sorted(n for n in log if n.startswith("suse_liberty_")):
    t = body(name + ".raw.gz")
    print(f"{name}: {re.search(r'<I>([^<]+)</I>', t).group(1).strip()}; names the CVE {t.count('CVE-2026-98432')} times")
print("== T5 Red Hat (Issued / Updated; dd after the first two dt)")
rh = {}
for name in sorted(n for n in log if n.startswith("redhat_")):
    t = body(name + ".raw.gz")
    dds = re.findall(r"<dt>[^<]*</dt>\s*<dd>(\d{4}-\d{2}-\d{2})</dd>", t)
    rh[name] = dt.date.fromisoformat(dds[0])
    print(f"{name}: issued {dds[0]}, updated {dds[1] if len(dds) > 1 else ''}; names the CVE {t.count('CVE-2026-98432')} times")
print()

# T6: the post
print("== T6 Anthropic post")
t = body("anthropic_post.raw.gz")
pub = re.search(r'"datePublished":"([^"]+)"', t).group(1)
mod = re.search(r'"dateModified":"([^"]+)"', t).group(1)
print("datePublished", pub, "dateModified", mod)
t6 = dt.date.fromisoformat(pub[:10])
print()

# T7: oss-security messages
print("== T7 oss-security messages (Date header)")
for name in sorted(n for n in log if n.startswith("ref_oss_security_")):
    t = body(name + ".raw.gz")
    ds = re.findall(r"^Date:\s*(.+)$", t, re.M)
    first = ds[0].strip()
    u = email.utils.parsedate_to_datetime(first).astimezone(dt.timezone.utc)
    print(f"{name}: {first}  = {u:%Y-%m-%d %H:%M} UTC")
print()


def days(a, b):
    a = a.date() if isinstance(a, dt.datetime) else a
    b = b.date() if isinstance(b, dt.datetime) else b
    return (b - a).days


t3 = dt.datetime(2026, 10, 15, 12, 8, 22, tzinfo=dt.timezone.utc)  # CVE record, recorded in the brief
first_stable = min(rel.values())
last_stable = max(rel.values())
fv = min(rel, key=rel.get)
lv = max(rel, key=rel.get)
print("== Elapsed UTC calendar days")
cands = [("T1 fix author date", t1), (f"T4 first stable release ({fv})", first_stable),
         (f"T4 last stable release ({lv})", last_stable), ("T3 CVE published", t3)]
for label, d in cands:
    print(f"{label} {d:%Y-%m-%d %H:%M} UTC -> T6 post {t6}: {days(d, t6)} days; "
          f"+7 = {(d.date() + dt.timedelta(7))}; +45 = {(d.date() + dt.timedelta(45))}; +90 = {(d.date() + dt.timedelta(90))}")
fs0, fsd0 = min(suse.items(), key=lambda kv: kv[1])
print(f"Earliest followed distribution fix (SUSE Release Date, {fs0}) {fsd0:%Y-%m-%d %H:%M} UTC -> T6 post {t6}: {days(fsd0, t6)} days; "
      f"+7 = {(fsd0.date() + dt.timedelta(7))}; +45 = {(fsd0.date() + dt.timedelta(45))}; +90 = {(fsd0.date() + dt.timedelta(90))}")
print("(version 0.2: the distribution-fix candidate added after R-0091; the T3 row was added after the read, post hoc)")
print(f"T1 -> T3: {days(t1, t3)} days")
print(f"T1 -> first stable: {days(t1, first_stable)} days; T1 -> last stable: {days(t1, last_stable)} days")
fs, fsd = min(suse.items(), key=lambda kv: kv[1])
fr = min(rh.values())
print(f"first stable -> earliest followed SUSE ({fsd:%Y-%m-%d}): {days(first_stable, fsd)} days; last stable -> it: {days(last_stable, fsd)} days")
print(f"first stable -> earliest followed Red Hat ({fr}): {days(first_stable, fr)} days; last stable -> it: {days(last_stable, fr)} days")
print(f"T6 post -> earliest followed SUSE: {days(t6, fsd)} days; -> earliest followed Red Hat: {days(t6, fr)} days")
print("T0 (report) unknown: no pair with T0 computed. P4 (linux-distros 14 days): no use known, not computed.")
print()

# Version 0.4 (21 November 2026): the amendment of 20 November, its decision rule applied per advisory.
# Three SUSE dates for each followed advisory, all from retained bodies:
#   Release Date: the advisory page of the read of 17 November (parsed above, `suse`);
#   CVE-page stamp: SUSE's CVE page as retained by LH036's read of 16 November (reuse, post hoc);
#   list message: the archive's date for the message on sle-security-updates, read 21 November.
# OSV's published and modified are printed beside them, classed as SUSE's data relayed by OSV,
# and are never used in the rule. The rule compares UTC calendar days only, and the post's date
# plays no part in it.
print("== T5 SUSE: the amendment of 20 November, decision rule per advisory (version 0.4)")
LH036_SUSE = HERE.parent / "LH036" / "data" / "read-2026-11-16T1419Z" / "suse.raw.gz"
CLOCKS = HERE / "data" / "suse-clocks-2026-11-21T1420Z"
page = gzip.open(LH036_SUSE).read().decode("utf-8", "replace")
OFF = {"CET": 1, "CEST": 2, "UTC": 0}
stamp = {}
for ident, s, tz, yr in re.findall(
        r">([A-Z]+-[A-Z0-9:-]+)</a>, published (\w{3} \w{3} +\d+ [\d:]+) (CET|CEST|UTC) (\d{4})", page):
    d = dt.datetime.strptime(re.sub(" +", " ", s) + " " + yr, "%a %b %d %H:%M:%S %Y") - dt.timedelta(hours=OFF[tz])
    stamp.setdefault(ident, []).append(d.replace(tzinfo=dt.timezone.utc))
lm = {}
import csv  # noqa: E402
for row in csv.DictReader(open(CLOCKS / "readlog.csv")):
    lm[row["name"]] = row["last_modified"]
groups, rows = {}, []
for name in sorted(suse):
    num = int(re.search(r"suse_su_2026(\d{5})_1", name).group(1))
    ident = f"SUSE-SU-2026:{num}-1"
    rd = suse[name]
    assert len(stamp.get(ident, [])) == 1, ident
    cp = stamp[ident][0]
    m = gzip.open(CLOCKS / f"msg-{num}.raw.gz").read().decode("utf-8", "replace")
    arch = re.findall(r"<I>([^<]*\d{4})</I>", m)
    arch_dt = [dt.datetime.strptime(" ".join(x.split()), "%a %b %d %H:%M:%S UTC %Y").replace(tzinfo=dt.timezone.utc)
               for x in arch]
    rel_in_msg = re.findall(r"Release Date:\s*(\S+)", m)
    assert rel_in_msg and rel_in_msg[0] == f"{rd:%Y-%m-%dT%H:%M:%SZ}", (ident, rel_in_msg)
    refs = m.split("<PRE>", 1)[1].split("CVSS scores", 1)[0]
    listed = "listed in References" if "* CVE-2026-98432" in refs else ("appears" if "CVE-2026-98432" in m else "not shown")
    lmd = email.utils.parsedate_to_datetime(lm[f"msg-{num}"]).astimezone(dt.timezone.utc)
    o = json.loads(gzip.open(CLOCKS / f"osv-{num}.raw.gz").read())
    days_shown = {d.date() for d in arch_dt}
    if len(days_shown) != 1:
        verdict = "unclassed (archive dates on more than one UTC day)"
    else:
        ld = days_shown.pop()
        r, c = ld == rd.date(), ld == cp.date()
        verdict = ("supports Release Date" if r and not c else "supports CVE-page stamp" if c and not r
                   else "agrees with neither: all three kept" if not (r or c) else "agrees with both")
    group = "24 October" if rd.date() == dt.date(2026, 10, 24) else "2 November"
    groups.setdefault(group, {}).setdefault(verdict, 0)
    groups[group][verdict] += 1
    rows.append((ident, rd, cp, arch_dt[0], group))
    print(f"{ident} [{group}]: Release Date {rd:%Y-%m-%d %H:%M:%S}Z (same in message); CVE-page stamp {cp:%Y-%m-%d %H:%M:%S}Z; "
          f"list message (archive) {'; '.join(f'{d:%Y-%m-%d %H:%M:%S}Z' for d in arch_dt)} "
          f"(page Last-Modified {lmd:%Y-%m-%d %H:%M:%S}Z); CVE-2026-98432 {listed}; "
          f"OSV published {o.get('published')} modified {o.get('modified')} (SUSE's data relayed, not used) -> {verdict}; "
          f"Release Date to list message {(arch_dt[0] - rd).total_seconds() / 86400:.2f} days")
osv_src = set()
for name in suse:
    num = int(re.search(r"suse_su_2026(\d{5})_1", name).group(1))
    o = json.loads(gzip.open(CLOCKS / f"osv-{num}.raw.gz").read())
    osv_src |= {(af.get("database_specific") or {}).get("source", "").split("/pub/")[0] for af in o.get("affected", [])}
print("OSV records' stated source hosts (affected[].database_specific.source):", sorted(osv_src))
print("counts by group:", {g: v for g, v in groups.items()})
gaps = [(r[2] - r[3]).total_seconds() / 3600 for r in rows]
print(f"CVE-page stamp minus list message, hours (all twelve): min {min(gaps):.2f}, max {max(gaps):.2f}; "
      f"list message before stamp in {sum(g > 0 for g in gaps)} of {len(gaps)}")
print()
print("== Elapsed UTC calendar days, with the list's announcement day (version 0.4)")
for group in ("24 October", "2 November"):
    gr = [r for r in rows if r[4] == group]
    first_list = min(r[3] for r in gr)
    last_list = max(r[3] for r in gr)
    rdmin = min(r[1] for r in gr)
    print(f"{group} group: list messages {first_list:%Y-%m-%d %H:%M}Z to {last_list:%Y-%m-%d %H:%M}Z; "
          f"post {t6} -> list day: {days(t6, first_list)} days; Release Date {rdmin:%Y-%m-%d} -> post: {days(rdmin, t6)} days")
earliest_list = min(r[3] for r in rows)
print(f"Earliest followed SUSE announcement on the list {earliest_list:%Y-%m-%d %H:%M}Z -> T6 post {t6}: {days(earliest_list, t6)} days; "
      f"+7 = {(earliest_list.date() + dt.timedelta(7))}; +45 = {(earliest_list.date() + dt.timedelta(45))}; "
      f"+90 = {(earliest_list.date() + dt.timedelta(90))}")
print(f"first stable -> earliest list announcement: {days(first_stable, earliest_list)} days; "
      f"last stable -> it: {days(last_stable, earliest_list)} days")
print("No clock is chosen by its distance from the post: the rule above compares the list day with the two SUSE clocks only.")
