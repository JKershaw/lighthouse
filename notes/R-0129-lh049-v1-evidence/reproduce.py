"""Independent reproduction of LH049 record v1.0 figures (review R-0129).

Written from the brief's text, not from scripts/tabulate.py. Reads only the
retained bodies under studies/LH049/data/read-*/ and makes no request.
Run: python3 -I notes/R-0129-lh049-v1-evidence/reproduce.py
"""
import gzip, hashlib, json, statistics, sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "studies/LH049/data"
V = "13.3.0"

def load(rd, name):
    return gzip.open(rd / f"{name}.raw.gz").read()

reads = sorted(p for p in DATA.glob("read-*") if p.is_dir())
print(f"reads: {len(reads)}")
rows = []
for rd in reads:
    log = {e["name"]: e for e in json.load(open(rd / "read_log.json"))}
    statuses = {k: e["status"] for k, e in log.items()}
    hashes = {}
    for k, e in log.items():
        raw = load(rd, k)
        if e.get("emails_withheld", 0) == 0:
            hashes[k] = hashlib.sha256(raw).hexdigest() == e["sha256"]
        else:
            hashes[k] = f"withheld {e['emails_withheld']}"
    pb = json.loads(load(rd, "point_before")); pa = json.loads(load(rd, "point_after"))
    ver = json.loads(load(rd, "versions"))
    rng = json.loads(load(rd, "range"))
    pk = json.loads(load(rd, "packument"))
    osv = json.loads(load(rd, "osv"))
    dl = ver["downloads"]
    s = sum(dl.values())
    agree = (pb["start"], pb["end"], pb["downloads"]) == (pa["start"], pa["end"], pa["downloads"])
    end = date.fromisoformat(pb["end"]); start = date.fromisoformat(pb["start"])
    seven = (end - start).days == 6
    held = agree and seven and s == pb["downloads"]
    listed = set(pk["versions"].keys())
    rows.append(dict(label=rd.name[5:], statuses=statuses, hashes=hashes, start=start, end=end,
                     point=pb["downloads"], vsum=s, held=held, agree=agree, seven=seven,
                     v=dl.get(V), nkeys=len(dl), zeros=sum(1 for x in dl.values() if x == 0),
                     smallest=min(dl.values()), listed=listed, dl=dl, rng=rng, pk=pk, osv=osv,
                     verkeys=set(dl), other_fields=sorted(set(ver) - {"package", "downloads"})))

print("\n== Clock rule per read")
for r in rows:
    print(f"{r['label']} statuses={sorted(set(r['statuses'].values()))} window {r['start']}..{r['end']} "
          f"agree={r['agree']} seven={r['seven']} point={r['point']} vsum={r['vsum']} diff={r['vsum']-r['point']:+d} "
          f"held={r['held']} V(13.3.0)={r['v'] if r['v'] is not None else 'NO KEY'} versions-answer extra fields={r['other_fields']}")
    print(f"   hash checks: {r['hashes']}")
nhash = sum(1 for r in rows for v in r['hashes'].values() if v is True)
print(f"bodies with no email withheld whose SHA-256 matched: {nhash}; mismatches: "
      f"{sum(1 for r in rows for v in r['hashes'].values() if v is False)}")

# windows that contain 5 Nov vs excess
print("\n== Excess and whether window contains 2026-11-05")
for r in rows:
    print(f"  {r['end']}: contains 5 Nov={r['start'] <= date(2026,11,5) <= r['end']}, excess={r['vsum']-r['point']}")

# Which per-version entries carry the excess? (descriptive only)
print("\n== Descriptive: per-version entries in failing windows vs window ending 12 Nov (not used by any measure)")
w12 = next(r for r in rows if r['end'] == date(2026,11,12))
for r in rows[:3]:
    big = sorted(r['dl'].items(), key=lambda kv: -kv[1])[:5]
    print(f"  {r['end']} top5 {big}")
print(f"  {w12['end']} top5 {sorted(w12['dl'].items(), key=lambda kv: -kv[1])[:5]}")

# Package daily totals
print("\n== Package daily totals")
daily = {}; disagree = []
for r in rows:
    for e in r['rng']['downloads']:
        d = date.fromisoformat(e['day'])
        if d >= date.fromisoformat(r['label'][:10]):  # own UTC date: not yet loaded
            if e['downloads'] != 0:
                print(f"  NOTE own-date nonzero {r['label']} {d} {e['downloads']}")
            continue
        if d in daily and daily[d] != e['downloads']:
            disagree.append((d, daily[d], e['downloads'], r['label']))
        daily[d] = e['downloads']
print("  disagreements:", disagree or "none")
print("  " + ", ".join(f"{d.day}={n}" for d, n in sorted(daily.items())))
for r in rows:
    tot = sum(daily[r['start'] + timedelta(i)] for i in range(7))
    print(f"  window {r['start']}..{r['end']}: daily sum {tot} vs point {r['point']} equal={tot == r['point']}")

# Day counts by the brief's formulas
print("\n== Day counts (brief formulas; held windows only; no key = no record, not zero)")
Vh = {}
for r in rows:
    if r['held']:
        Vh[r['end']] = r['v']  # None = no record
def Vt(d):
    if d == date(2026,11,8): return 0
    return Vh.get(d, "unknown") if d in Vh else "unknown"
dd = {}
nov = lambda n: date(2026,11,n)
v9 = Vt(nov(9))
dd[9] = v9 if isinstance(v9, int) else "unknown"
for n in range(10, 16):
    a, b = Vt(nov(n)), Vt(nov(n-1))
    dd[n] = a - b if isinstance(a, int) and isinstance(b, int) else "unknown"
a, b = Vt(nov(16)), Vt(nov(15))
dd[16] = a - b + dd[9] if all(isinstance(x, int) for x in (a, b, dd[9])) else "unknown"
for n in range(9, 17):
    print(f"  d({n} Nov) = {dd[n]}")
print("  V held:", {str(k): (v if v is not None else 'no record') for k, v in sorted(Vh.items())})
print("  Sums formed: " + "; ".join(f"d(9..{t.day})={v}" for t, v in sorted(Vh.items()) if isinstance(v, int)))

# Measure 1
earliest = min((t for t, v in Vh.items() if isinstance(v, int)))
upper = Vh[earliest]
lower_formable = isinstance(Vt(nov(15)), int) and isinstance(Vt(nov(16)), int)
pkg9 = daily[nov(9)]
print(f"\n== Measure 1: earliest held window with value ends {earliest}; upper={upper}; brief lower formable={lower_formable}")
print(f"  package 9 Nov = {pkg9}; S0 upper = {upper}/{pkg9} = {upper/pkg9:.4f} ({100*upper/pkg9:.1f}%)")
# Measure 3
ms = 75.1 / 1440
print(f"== Measure 3: minutes share {ms:.5f}; I upper = {(upper/pkg9)/ms:.3f}")
# Measure 4
others = [daily[nov(n)] for n in range(2, 17) if n != 9 and nov(n) in daily]
mn = min((daily[nov(n)], n) for n in range(2,17) if n != 9); mx = max((daily[nov(n)], n) for n in range(2,17) if n != 9)
print(f"== Measure 4: n={len(others)} median={statistics.median(others)} min={mn} max={mx}")
t = [daily[nov(n)] for n in range(17, 24)]
print(f"  17..23 Nov: {t} min {min(t)} max {max(t)} sum {sum(t)}")
# Measure 2 tail
w23 = next(r for r in rows if r['end'] == nov(23))
print(f"== Measure 2 tail: window {w23['start']}..{w23['end']} held={w23['held']} point {w23['point']} vsum {w23['vsum']} V={'no record' if w23['v'] is None else w23['v']}")
# Measure 6
lo, hi = 0, upper
inside = 4 <= lo and hi <= 31; outside = hi < 4 or lo > 31
print(f"== Measure 6: bound [{lo},{hi}] wholly inside 4..31={inside}, wholly outside={outside} -> reading {'made' if inside or outside else 'not made'}")

# Outside protocol: 13.3.0 in every window, keys vs listed
print("\n== Outside the protocol (observation)")
for r in rows:
    absent = sorted(r['listed'] - r['verkeys']); notlisted = sorted(r['verkeys'] - r['listed'])
    print(f"  {r['end']}: V={r['v'] if r['v'] is not None else 'no key'} keys={r['nkeys']} zeros={r['zeros']} smallest={r['smallest']} "
          f"listed={len(r['listed'])} listed-without-key={len(absent)} keys-not-listed={notlisted}")

# Measure 5 and 7
print("\n== Measure 5 / 7")
prev = None
for r in rows:
    pk = r['pk']; tm = pk.get('time', {})
    after = sorted(k for k, v in tm.items() if k not in ('created', 'modified') and v >= '2026-11-09T00:00')
    qual = [k for k, v in tm.items() if k not in ('created','modified') and '-' not in k and k != V
            and '2026-11-10T00:00' <= v <= '2026-11-16T23:59:59.999Z']
    dep = [k for k, vv in pk['versions'].items() if vv.get('deprecated')]
    new = sorted(r['listed'] - prev) if prev is not None else None
    gone = sorted(prev - r['listed']) if prev is not None else None
    prev = r['listed']
    vulns = r['osv'].get('vulns', [])
    o = [(x['id'], x.get('aliases'), x.get('modified'), x.get('withdrawn'),
          [ (s.get('source') if isinstance(s, dict) else s) for s in x.get('database_specific', {}).get('malicious-packages-origins', [])]) for x in vulns]
    print(f"  {r['label']}: listed13.3.0={V in pk['versions']} time={tm.get(V)} latest={pk['dist-tags'].get('latest')} "
          f"deprecated={dep} unpublished={'unpublished' in tm} modified={tm.get('modified')} n={len(r['listed'])} new={new} gone={gone} "
          f"time entries >=9 Nov={after} qualifying={qual}")
    print(f"     osv {o}")
