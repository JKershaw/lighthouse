"""Summarise one LH048 read for its checkpoint: per CVE, the CNA's and any
CISA ADP container's metrics, NVD's status and metrics, the newest EPSS value,
any EPSS step (day-on-day factor of two or more) in the series held, and KEV.
Reads only retained bytes. Not the study's tabulator (which comes later and
implements measures 1 to 4 across reads); a checkpoint aid.
Usage: python3 -I studies/LH048/scripts/summarise_read.py <read dir>
"""
import gzip, json, sys
from pathlib import Path

d = Path(sys.argv[1])
sel = json.loads((d.parent.parent / 'selection.json').read_text())
role = {}
for u in sel['units']:
    for c in u['cves'] + u['candidates']:
        role.setdefault(c, []).append(f"{u['step']} ({u['class']})")
for c in sel['linked_set']:
    role.setdefault(c, ['linked set'])

def load(name):
    p = d / f'{name}.raw.gz'
    if not p.exists():
        return None
    try:
        return json.loads(gzip.open(p).read())
    except Exception:
        return None

def band(s):
    return 'Critical' if s >= 9 else 'High' if s >= 7 else 'Medium' if s >= 4 else 'Low' if s > 0 else 'None'

def metrics(container):
    out = []
    for m in container.get('metrics', []) or []:
        for k, v in m.items():
            if k.startswith('cvss'):
                out.append(f"{k} {v.get('baseScore')} {v.get('baseSeverity', band(v.get('baseScore', 0)))}")
            elif k == 'other':
                c = v.get('content', {})
                if c.get('id') or c.get('options'):
                    out.append('SSVC ' + json.dumps(c.get('options')))
    return out

kev = load('kev') or {}
kev_ids = {v['cveID']: v for v in kev.get('vulnerabilities', [])}
print(f"KEV catalogue {kev.get('catalogVersion')} released {kev.get('dateReleased')}, {kev.get('count')} entries")
epss = {}
for p in sorted(d.glob('epss_*.raw.gz')):
    for r in json.loads(gzip.open(p).read()).get('data', []):
        series = [(r['date'], float(r['epss']), float(r['percentile']))]
        for t in r.get('time-series', []):
            series.append((t['date'], float(t['epss']), float(t['percentile'])))
        epss[r['cve']] = sorted(set(series))

for c in role:
    print(f"\n{c}: {', '.join(role[c])}")
    rec = load(f'cve_org_{c}')
    if rec is None:
        print('  CVE record: none at this read')
    else:
        meta = rec.get('cveMetadata', {})
        cna = rec.get('containers', {}).get('cna', {})
        print(f"  CVE record: published {meta.get('datePublished')}, updated {meta.get('dateUpdated')}; CNA {meta.get('assignerShortName')}: {metrics(cna) or 'no metric'}")
        for adp in rec.get('containers', {}).get('adp', []):
            prov = adp.get('providerMetadata', {}).get('shortName')
            print(f"  ADP {prov}: {metrics(adp) or 'no metric'}")
    n = load(f'nvd_{c}')
    if n and n.get('vulnerabilities'):
        cv = n['vulnerabilities'][0]['cve']
        ms = []
        for k, arr in cv.get('metrics', {}).items():
            for m in arr:
                if 'cvssData' in m:
                    ms.append(f"{k} {m.get('source')} {m.get('type', 'no type')} {m['cvssData'].get('baseScore')}")
                elif 'ssvcData' in m:
                    ms.append(f"{k} {m.get('source')} {json.dumps(m['ssvcData'].get('options'))}")
        print(f"  NVD: {cv.get('vulnStatus')}, lastModified {cv.get('lastModified')}; {ms or 'no metric'}; cisaExploitAdd {cv.get('cisaExploitAdd')}")
    else:
        print('  NVD: no record at this read' if n is not None else '  NVD: unavailable')
    s = epss.get(c)
    if s:
        steps = [(s[i][0], s[i-1][1], s[i][1]) for i in range(1, len(s)) if s[i-1][1] > 0 and (s[i][1] / s[i-1][1] >= 2 or s[i][1] / s[i-1][1] <= 0.5)]
        print(f"  EPSS: {len(s)} dates {s[0][0]} to {s[-1][0]}; latest {s[-1][1]} (percentile {s[-1][2]}); max {max(x[1] for x in s)}; steps {steps or 'none'}")
    else:
        print('  EPSS: not scored at this read')
    k = kev_ids.get(c)
    print(f"  KEV: listed, dateAdded {k['dateAdded']}" if k else '  KEV: not listed at this read')
m = load('msrc_CVE-2026-33096')
if m is not None:
    v = (m.get('value') or [{}])[0]
    keys = ['severity', 'impact', 'baseScore', 'vectorString', 'exploited', 'publiclyDisclosed', 'releaseDate', 'latestRevisionDate']
    print('\nMSRC CVE-2026-33096: ' + json.dumps({k: v.get(k) for k in keys}))
