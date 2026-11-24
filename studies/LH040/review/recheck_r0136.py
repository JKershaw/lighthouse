"""R-0136 recheck of LH040 1.1: independent recomputation of the passages 1.1 changed.
Index I(R) = S0(R) / (h(R)/24), from read 2's raw Q1/Q2 and L1's derived upload times,
with 1.107.0 newest from 11:39:51 UTC to each window end (R1, R8, R7). Installer tail from raw Q4.
No network. Run: python3 -I studies/LH040/review/recheck_r0136.py"""
import csv, json, os, statistics, collections
from datetime import datetime, timedelta, timezone
from packaging.version import Version
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
R2 = os.path.join(B, 'data/read-2026-11-23T1433Z')
L1 = json.load(open(os.path.join(B, 'data/pre-brief-2026-11-08T1414Z/pypi_project_json.derived.json')))['extracted']['first_upload_time_iso_8601']
COMP = ['1.103.2','1.104.0','1.104.1','1.104.2','1.105.0','1.105.1','1.106.0','1.106.1','1.106.2',
        '1.106.3','1.106.4','1.106.5','1.106.6','1.108.0','1.108.1','1.108.2','1.108.3']
tot = collections.Counter()
for r in csv.DictReader(open(os.path.join(R2, 'Q1_daily_totals.raw'))): tot[r['date']] += int(r['count'])
ver = collections.Counter()
for r in csv.DictReader(open(os.path.join(R2, 'Q2_daily_by_version_oct_nov.raw'))): ver[(r['date'], r['version'])] += int(r['count'])
def p(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
up = {}
for v, t in L1.items():
    try: V = Version(v)
    except Exception: continue
    if not V.is_prerelease and not V.is_devrelease: up[v] = p(t)
CASE_UP = datetime(2026, 10, 21, 11, 39, 51, tzinfo=timezone.utc)
def hours_newest(rel, day, end):
    """Hours of UTC day `day` during which rel is the highest final version available, 1.107.0 live CASE_UP..end."""
    d0 = datetime.fromisoformat(day).replace(tzinfo=timezone.utc); d1 = d0 + timedelta(days=1)
    events = sorted({d0, d1} | {t for t in up.values() if d0 < t < d1} | ({CASE_UP, end} if d0 < CASE_UP < d1 else set()))
    h = 0.0
    for a, b in zip(events, events[1:]):
        mid = a + (b - a) / 2
        avail = [Version(v) for v, t in up.items() if t <= mid]
        if CASE_UP <= mid < end: avail.append(Version('1.107.0'))
        if max(avail) == Version(rel): h += (b - a).total_seconds() / 3600
    return h
ends = {'13:23': datetime(2026,10,21,13,23,tzinfo=timezone.utc), '13:20': datetime(2026,10,21,13,20,tzinfo=timezone.utc),
        '12:47': datetime(2026,10,21,12,47,tzinfo=timezone.utc)}
for name, end in ends.items():
    I = {}
    for rel in COMP + ['1.107.0']:
        t = CASE_UP if rel == '1.107.0' else up[rel]
        day = t.date().isoformat(); S0 = ver[(day, rel)] / tot[day]
        h = hours_newest(rel, day, end); I[rel] = S0 / (h / 24)
    comp = sorted(I[r] for r in COMP); med = statistics.median(comp); c = I['1.107.0']
    rank = 1 + sum(v > c for v in comp)
    below = [r for r in COMP if I[r] < c]
    print(f"end {name}: case I {c:.4f}, h {hours_newest('1.107.0','2026-10-21',end):.4f}; comp min {comp[0]:.4f} med {med:.4f} max {comp[-1]:.4f}")
    print(f"  band {comp[0]/med:.3f} to {comp[-1]/med:.3f} x median; case {c/med:.3f} x median; rank {rank} of 18; below: {below}")
    print(f"  position in band {100*(c-comp[0])/(comp[-1]-comp[0]):.1f}%; max reduction from median still in band {100*(1-comp[0]/med):.1f}%")
    if name == '13:23':
        early = {r: round(I[r], 3) for r in COMP if up[r].hour < 13}
        print(f"  uploaded before 13:00 UTC: n={len(early)}, min {min(early.values())} max {max(early.values())}, case below all: {all(v > c for v in early.values())}")
        print(f"  1.108.1 h {hours_newest('1.108.1','2026-11-05',end):.3f}")
day0 = tot['2026-10-21']; C0 = ver[('2026-10-21','1.107.0')]
print(f"C0 {C0}, total {day0}, S0 {100*C0/day0:.3f}%")
q4 = collections.Counter(); uvdays = collections.Counter()
for r in csv.DictReader(open(os.path.join(R2, 'Q4_installer.raw'))):
    if r['version'] == '1.107.0' and '2026-10-22' <= r['date'] <= '2026-11-20':
        q4[r['installer'] or '(none)'] += int(r['count'])
        if r['installer'] == 'uv': uvdays[r['date']] += int(r['count'])
n = sum(q4.values())
print(f"tail days 1-30 by installer: {dict(q4)}; total {n}; none+Browser {q4['(none)']+q4['Browser']} = {100*(q4['(none)']+q4['Browser'])/n:.2f}%; pip {q4.get('pip',0)}")
print(f"uv days {len(uvdays)}: {dict(sorted(uvdays.items()))}")
q2tail = sum(v for (d, r), v in ver.items() if r == '1.107.0' and '2026-10-22' <= d <= '2026-11-20')
days = sum(1 for (d, r), v in ver.items() if r == '1.107.0' and '2026-10-22' <= d <= '2026-11-20')
print(f"Q2 tail days 1-30 {q2tail} on {days} days")
