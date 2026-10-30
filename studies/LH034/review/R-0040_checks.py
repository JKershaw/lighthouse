#!/usr/bin/env python3
"""R-0040 reviewer checks (reader review of 'A week after two fixes').
Reads retained data only. Usage: python3 -I studies/LH034/review/R-0040_checks.py"""
import gzip, json
from pathlib import Path
from datetime import date
ROOT = Path(__file__).resolve().parents[3]
D0 = date(2026, 10, 21)
snap = json.loads(gzip.decompress((ROOT/'studies/LH033/data/read-2026-10-29T0635Z/censys.raw.gz').read_bytes()))['snapshot']
print('snapshot keys:', sorted(snap.keys()))
print('branch_history row keys:', sorted(snap['branch_history'][0].keys()))
rows = {}
for r in snap['branch_history']:
    d = (date.fromisoformat(r['day']) - D0).days
    if 0 <= d <= 7 and r['branch'] in ('8.2','8.3','8.4','8.5'):
        rows.setdefault(r['branch'], {})[d] = r
print('\n== A. Per branch: targets, patched, unpatched (targets-patched), in thousands; day-on-day changes')
for b, v in sorted(rows.items()):
    print(f'branch {b}')
    prev = None
    for d in sorted(v):
        r = v[d]; t, p = r['targets'], r['patched']; u = t - p
        line = f'  d{d}: targets {t/1e3:8.0f}  patched {p/1e3:8.0f}  unpatched {u/1e3:8.0f}  share {p/t*100:5.1f}%'
        if prev:
            pt, pp = prev; line += f'   d_targets {(t-pt)/1e3:+7.0f}  d_patched {(p-pp)/1e3:+7.0f}  d_unpatched {((t-p)-(pt-pp))/1e3:+7.0f}'
        print(line + '   ' + json.dumps({k: r[k] for k in r if k not in ('day','branch','targets','patched')}))
        prev = (t, p)
    t0, p0 = v[0]['targets'], v[0]['patched']; t7, p7 = v[7]['targets'], v[7]['patched']
    print(f'  d0->d7: targets {(t7-t0)/1e3:+.0f}k, patched {(p7-p0)/1e3:+.0f}k, unpatched {((t7-p7)-(t0-p0))/1e3:+.0f}k;'
          f' share if targets held at d0 and every new patched were an upgrade: {min(p7,t0)/t0*100:.1f}%;'
          f' share counting only fall in unpatched as upgrades: {((t0-p0)-(t7-p7)+p0)/t0*100:.1f}%')
# Node.js: day-7 share of fixed release alone vs at-or-newer (from R-0039 output, recomputed here)
print('\n== B. Node.js July vs October, line 26, as the record reports (LH034.md tables): July d7 89.0, Oct d7 64.7; posting-aligned July d8 89.4')

print('\n== C. Censys current snapshot (29 Oct 06:15, part of day 8) beside branch_history day 7')
cur = {}
for r in snap['branch_versions']:
    cur.setdefault(r['branch'], 0); cur[r['branch']] += r['targets']
fixed = {'8.2': '8.2.35', '8.3': '8.3.36', '8.4': '8.4.27', '8.5': '8.5.12'}
for b in ('8.2', '8.3', '8.4', '8.5'):
    fx = sum(r['targets'] for r in snap['branch_versions'] if r['version'] == fixed[b])
    t7, p7 = rows[b][7]['targets'], rows[b][7]['patched']
    print(f'  {b}: branch_history d7 targets {t7/1e6:.2f}M patched {p7/1e6:.2f}M | current branch_versions total {cur[b]/1e6:.2f}M, on fixed release {fx/1e6:.2f}M ({fx/cur[b]*100:.1f}%)')
nofix = [r for r in snap['top_versions'] if r['status'] == 'affected_nofix']
t74 = sum(r['targets'] for r in snap['branches'] if r['branch'] == '7.4')
v7433 = sum(r['targets'] for r in snap['top_versions'] if r['version'] == '7.4.33')
print(f'  branch 7.4 current {t74/1e6:.2f}M, of which 7.4.33 (the last upstream 7.4 release) {v7433/1e6:.2f}M = {v7433/t74*100:.1f}%')
print('  largest affected_nofix versions:', [(r['version'], round(r['targets']/1e6, 2)) for r in sorted(nofix, key=lambda r: -r['targets'])[:6]])
