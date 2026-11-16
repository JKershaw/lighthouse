#!/usr/bin/env python3
"""LH036 interim evidence review: signals (measures 1 to 3) recomputed from the raw read bodies,
independently of tabulate.py. Usage: python3 -I studies/LH036/review/check_signals.py"""
from pathlib import Path
import gzip, json
D = Path(__file__).resolve().parents[1] / 'data'
CVE = 'CVE-2026-98432'
reads = sorted(p for p in D.glob('read-*') if p.is_dir())
def raw(r, n):
    log = {x['name']: x for x in json.loads((r / 'read_log.json').read_text())}
    x = log.get(n)
    if not x or x.get('status') != 200: return None, x
    return gzip.decompress((r / x['file']).read_bytes()).decode('utf-8', 'replace'), x

print('== Measure 1: EPSS, each date from the earliest read holding it')
series, later_diff = {}, []
for r in reads:
    t, _ = raw(r, 'epss'); d = json.loads(t)['data'][0]
    pts = [{'date': d['date'], 'epss': d['epss'], 'percentile': d['percentile']}] + d.get('time-series', [])
    for p in pts:
        v = (float(p['epss']), float(p['percentile']))
        if p['date'] in series:
            if series[p['date']][0] != v: later_diff.append((r.name, p['date'], series[p['date']][0], v))
        else: series[p['date']] = (v, r.name)
dates = sorted(series)
print('dates', dates[0], 'to', dates[-1], 'count', len(dates), 'later reads differing in value:', later_diff)
prev = None
for dt in dates:
    (s, pc), rd = series[dt]
    f = s / prev if prev else None
    print(dt, s, round(pc, 5), 'factor %.3f' % f if f else 'first', 'STEP' if f and (f >= 2 or f <= 0.5) else '', rd)
    prev = s
print('overall factor %.3f' % (series[dates[-1]][0][0] / series[dates[0]][0][0]))

print('\n== Measure 2: KEV')
for r in reads:
    t, x = raw(r, 'kev'); k = json.loads(t)
    hit = [v for v in k['vulnerabilities'] if v['cveID'] == CVE]
    # also a plain substring search, in case of a malformed entry
    print(r.name, k.get('catalogVersion'), k.get('dateReleased'), 'entries', len(k['vulnerabilities']), 'listed' if hit else 'not listed', 'substring' if CVE in t else 'no substring')

print('\n== Measure 3: CVE record, NVD, OSV')
prev_refs = {}
for r in reads:
    c = json.loads(raw(r, 'cve_org')[0])
    cna = c['containers']['cna']
    adp = [(a['providerMetadata'].get('shortName'), a['providerMetadata'].get('dateUpdated')) for a in c['containers'].get('adp', [])]
    ssvc = [m for a in c['containers'].get('adp', []) for m in a.get('metrics', []) if 'other' in m]
    vec = [(m.get('cvssV3_1') or {}).get('vectorString') for m in cna.get('metrics', [])]
    sc = [(m.get('cvssV3_1') or {}).get('baseScore') for m in cna.get('metrics', [])]
    crefs = {x['url'] for x in cna.get('references', [])} | {x['url'] for a in c['containers'].get('adp', []) for x in a.get('references', [])}
    n = json.loads(raw(r, 'nvd')[0])['vulnerabilities'][0]['cve']
    nm = {k: [(m.get('type'), m.get('source'), m.get('cvssData', {}).get('baseScore')) for m in v] for k, v in n.get('metrics', {}).items()}
    o = json.loads(raw(r, 'osv')[0])
    orefs = {x['url'] for x in o.get('references', [])}
    print(r.name, 'cve dateUpdated', c['cveMetadata'].get('dateUpdated'), 'cna dateUpdated', cna['providerMetadata'].get('dateUpdated'),
          'vec', vec, sc, 'adp', adp, 'ssvc', len(ssvc))
    print('   NVD', n['vulnStatus'], n['lastModified'], nm, 'weaknesses', [(w.get('type'), [d['value'] for d in w['description']]) for w in n.get('weaknesses', [])],
          'config nodes', sum(len(nd.get('cpeMatch', [])) for cf in n.get('configurations', []) for nd in cf.get('nodes', [])))
    print('   refs cve', len(crefs), 'osv', len(orefs), 'osv related', len(o.get('related', [])), 'osv modified', o.get('modified'))
    for k, s in (('cve', crefs), ('osv', orefs)):
        if k in prev_refs:
            if s - prev_refs[k]: print('   new', k, sorted(s - prev_refs[k]))
            if prev_refs[k] - s: print('   removed', k, sorted(prev_refs[k] - s))
        prev_refs[k] = s
n = json.loads(raw(reads[-1], 'nvd')[0])['vulnerabilities'][0]['cve']
print('\nNVD configurations at the last read:')
for cf in n.get('configurations', []):
    for nd in cf['nodes']:
        for m in nd['cpeMatch']:
            print('  ', m['criteria'], m.get('versionStartIncluding'), m.get('versionEndExcluding'), m.get('vulnerable'))
o = json.loads(raw(reads[-1], 'osv')[0])
print('OSV related at last read, non-SUSE:', [x for x in o.get('related', []) if not x.startswith(('SUSE', 'openSUSE'))])
