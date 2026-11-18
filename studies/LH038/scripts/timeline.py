"""LH038 record: extract each event's clock from the retained read of
2026-11-17T1419Z and compute elapsed UTC calendar days against the policy
intervals the brief names. Standard library only; reads retained bodies,
fetches nothing.

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
print(f"T1 -> T3: {days(t1, t3)} days")
print(f"T1 -> first stable: {days(t1, first_stable)} days; T1 -> last stable: {days(t1, last_stable)} days")
fs, fsd = min(suse.items(), key=lambda kv: kv[1])
fr = min(rh.values())
print(f"first stable -> earliest followed SUSE ({fsd:%Y-%m-%d}): {days(first_stable, fsd)} days; last stable -> it: {days(last_stable, fsd)} days")
print(f"first stable -> earliest followed Red Hat ({fr}): {days(first_stable, fr)} days; last stable -> it: {days(last_stable, fr)} days")
print(f"T6 post -> earliest followed SUSE: {days(t6, fsd)} days; -> earliest followed Red Hat: {days(t6, fr)} days")
print("T0 (report) unknown: no pair with T0 computed. P4 (linux-distros 14 days): no use known, not computed.")
