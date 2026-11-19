#!/usr/bin/env python3
"""LH054 tables from every retained read: measures 1 to 5 of the brief, written to data/tables.json.

Adapted after the baseline read of 19 November 2026 from studies/LH036/scripts/tabulate.py. Changes: the CVE and
events (F, E0, D); KEV is read from LH036's catalogue body of the same read day (brief, Overlap), never fetched here;
the page measured is the oss-security post; the CNA score is kept with its base score; SUSE products are also
summarised by the states of their main kernel packages (kernel-default, kernel-source, kernel-rt, kernel-64kb),
live patches left out, as measure 4 fixes in advance.

Usage: python3 studies/LH054/scripts/tabulate.py
Reads data/read-*/ in label order (the credit-check directory is not a read under the protocol and is skipped).
Offline, standard library only. A body that is a refusal, a challenge or under 200 bytes is 'unavailable'.
"""
from hashlib import sha256
from html import unescape
from pathlib import Path
import gzip
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CVE = 'CVE-2026-99288'
EVENTS = {'F': '2026-11-03', 'E0': '2026-11-10', 'D': '2026-11-15'}
LH036_DATA = ROOT.parent / 'LH036' / 'data'
MAIN_KERNEL = ('kernel-default', 'kernel-source', 'kernel-rt', 'kernel-64kb')


def body(read, name):
    log = {r['name']: r for r in json.loads((read / 'read_log.json').read_text())}
    row = log.get(name)
    if not row or row.get('status') != 200 or not row.get('file'):
        return None, (row or {}).get('status')
    raw = gzip.decompress((read / row['file']).read_bytes())
    text = raw.decode('utf-8', 'replace')
    if len(raw) < 200 or "not a bot" in text[:2000]:
        return None, 'unavailable (challenge or short body)'
    return text, 200


def text_of(html):
    html = re.sub(r'(?s)<(script|style).*?</\1>', '', html)
    s = unescape(re.sub(r'<[^>]+>', '\n', html))
    s = re.sub(r'[ \t\r]+', ' ', s)
    return [line.strip() for line in s.split('\n') if line.strip()]


def epss(read):
    t, st = body(read, 'epss')
    if t is None:
        return None
    d = json.loads(t)['data']
    if not d:
        return {}
    d = d[0]
    series = {d['date']: (float(d['epss']), float(d['percentile']))}
    for x in d.get('time-series', []):
        series.setdefault(x['date'], (float(x['epss']), float(x['percentile'])))
    return series


def kev(read):
    """KEV from LH036's read of the same UTC day (brief, Overlap); missing there means unavailable here."""
    day = read.name[5:15]
    same = sorted(p for p in LH036_DATA.glob('read-' + day + 'T*') if p.is_dir())
    if not same:
        return {'state': 'unavailable', 'status': 'no LH036 read on ' + day}
    t, st = body(same[-1], 'kev')
    if t is None:
        return {'state': 'unavailable', 'status': st, 'source': 'LH036/data/' + same[-1].name}
    k = json.loads(t)
    hit = [v for v in k['vulnerabilities'] if v['cveID'] == CVE]
    out = {'source': 'LH036/data/' + same[-1].name, 'state': 'listed' if hit else 'not listed', 'catalogVersion': k.get('catalogVersion'), 'dateReleased': k.get('dateReleased')}
    if hit:
        out.update({f: hit[0].get(f) for f in ('dateAdded', 'dueDate', 'knownRansomwareCampaignUse', 'notes')})
    return out


def record(read):
    out = {}
    t, st = body(read, 'cve_org')
    if t is not None:
        c = json.loads(t)
        cna = c['containers']['cna']
        out['cve_dateUpdated'] = c['cveMetadata'].get('dateUpdated')
        out['cna_dateUpdated'] = cna['providerMetadata'].get('dateUpdated')
        out['cna_cvss'] = [(m.get('cvssV3_1', m.get('cvssV4_0', {})).get('vectorString'), m.get('cvssV3_1', m.get('cvssV4_0', {})).get('baseScore')) for m in cna.get('metrics', []) if 'cvssV3_1' in m or 'cvssV4_0' in m]
        out['adp'] = []
        refs = {r['url'] for r in cna.get('references', [])}
        for a in c['containers'].get('adp', []):
            entry = {'provider': a['providerMetadata'].get('shortName'), 'dateUpdated': a['providerMetadata'].get('dateUpdated')}
            for m in a.get('metrics', []):
                if 'cvssV3_1' in m:
                    entry['cvss'] = (m['cvssV3_1'].get('vectorString'), m['cvssV3_1'].get('baseScore'))
                other = m.get('other', {})
                if other.get('type') == 'ssvc':
                    entry['ssvc'] = {list(o)[0]: list(o.values())[0] for o in other['content'].get('options', [])}
            out['adp'].append(entry)
            refs |= {r['url'] for r in a.get('references', [])}
        out['cve_refs'] = sorted(refs)
    else:
        out['cve_org'] = st
    t, st = body(read, 'nvd')
    if t is not None:
        v = json.loads(t)['vulnerabilities']
        if v:
            v = v[0]['cve']
            out['nvd_vulnStatus'] = v.get('vulnStatus')
            out['nvd_lastModified'] = v.get('lastModified')
            out['nvd_metrics'] = [(k, m.get('source'), m.get('type'), m.get('cvssData', {}).get('vectorString')) for k, ms in v.get('metrics', {}).items() for m in ms]
        else:
            out['nvd_vulnStatus'] = 'no record'
    else:
        out['nvd'] = st
    t, st = body(read, 'osv')
    if t is not None:
        o = json.loads(t)
        out['osv_modified'] = o.get('modified')
        out['osv_related'] = sorted(o.get('related', []))
        out['osv_refs'] = sorted(r['url'] for r in o.get('references', []))
    else:
        out['osv'] = st
    return out


def debian(read):
    t, st = body(read, 'debian')
    if t is None:
        return st
    lines = text_of(t)
    i = lines.index('Source Package')
    j = next(k for k in range(i, len(lines)) if lines[k].startswith('The information below'))
    cells = lines[i + 4:j]
    rows, pkg = [], None
    k = 0
    while k < len(cells):
        if k + 1 < len(cells) and cells[k + 1] == '(' and cells[k + 2] == 'PTS' and cells[k + 3] == ')':
            pkg = cells[k]
            k += 4
            continue
        if k + 2 < len(cells) and cells[k + 2] in ('fixed', 'vulnerable', 'not affected', 'undetermined'):
            rows.append({'package': pkg, 'release': cells[k], 'version': cells[k + 1], 'status': cells[k + 2]})
            k += 3
            continue
        k += 1
    return rows


def ubuntu(read):
    t, st = body(read, 'ubuntu')
    if t is None:
        return st
    u = json.loads(t)
    out = {'priority': u.get('priority'), 'linux': {}}
    for p in u.get('packages', []):
        if p['name'] == 'linux':
            out['linux'] = {s['release_codename']: [s['status'], s.get('description', '')] for s in p['statuses']}
    out['notices'] = sorted(n.get('id') for n in u.get('notices', []) if isinstance(n, dict))
    return out


def redhat(read):
    t, st = body(read, 'redhat')
    if t is None:
        return st
    r = json.loads(t)
    return {'threat_severity': r.get('threat_severity'), 'cvss3': r.get('cvss3'),
            'package_state': sorted((p['product_name'], p['package_name'], p['fix_state']) for p in r.get('package_state', [])),
            'affected_release': sorted((a.get('product_name'), a.get('package'), a.get('advisory'), a.get('release_date')) for a in r.get('affected_release', []))}


def suse(read):
    t, st = body(read, 'suse')
    if t is None:
        return st
    lines = text_of(t)
    out = {}
    for line in lines:
        if line.startswith('Overall state of this security issue:'):
            out['overall'] = line.split(':', 1)[1].strip()
    i = next(k for k, l in enumerate(lines) if l.startswith('Status of this issue by product and package'))
    i = next(k for k in range(i, len(lines)) if lines[k] == 'State') + 1
    rows, k = [], i
    end = next((m for m in range(i, len(lines)) if lines[m].startswith(('SUSE Timeline', 'Timeline', 'SUSE Bugzilla', 'Bugzilla entry'))), len(lines))
    while k + 2 < end:
        if lines[k].startswith('Products ') or lines[k].endswith('.'):
            k += 1
            continue
        rows.append((lines[k], lines[k + 1], lines[k + 2]))
        k += 3
    out['states'] = rows
    products = {}
    for product, package, state in rows:
        if package in MAIN_KERNEL:
            products.setdefault(product, []).append(state)
    out['main_kernel_summary'] = {p: sorted(set(v)) for p, v in sorted(products.items())}
    return out


def page(read, name):
    log = {r['name']: r for r in json.loads((read / 'read_log.json').read_text())}
    row = log.get(name, {})
    t, st = body(read, name)
    out = {'status': st if t is None else 200, 'sha256': row.get('sha256')}
    if t is not None:
        m = re.search(r'"dateModified"\s*:\s*"([^"]+)"', t)
        out['dateModified'] = m.group(1) if m else None
        # Pages carry markup that changes between fetches; the text's hash is what says the words changed.
        out['text_sha256'] = sha256('\n'.join(text_of(t)).encode()).hexdigest()
    return out


reads = sorted(p for p in DATA.glob('read-*') if p.is_dir())
tables = {'reads': [p.name[5:] for p in reads], 'events': EVENTS, 'per_read': {}, 'epss_series': {}}
for read in reads:
    label = read.name[5:]
    s = epss(read)
    if s:
        for d, v in s.items():
            tables['epss_series'].setdefault(d, {'epss': v[0], 'percentile': v[1], 'first_read': label})
    tables['per_read'][label] = {
        'kev': kev(read), 'record': record(read), 'debian': debian(read), 'ubuntu': ubuntu(read),
        'redhat': redhat(read), 'suse': suse(read),
        'pages': {n: page(read, n) for n in ('oss_security_post',)},
    }
series = sorted(tables['epss_series'].items())
steps = []
for (d0, a), (d1, b) in zip(series, series[1:]):
    if a['epss'] and (b['epss'] / a['epss'] >= 2 or a['epss'] / b['epss'] >= 2):
        from datetime import date
        days = {e: (date.fromisoformat(d1) - date.fromisoformat(v)).days for e, v in EVENTS.items()}
        steps.append({'date': d1, 'from': a['epss'], 'to': b['epss'], 'days_after_event': days})
tables['epss_first_date'] = series[0][0] if series else None
tables['epss_steps'] = steps
(DATA / 'tables.json').write_text(json.dumps(tables, indent=1) + '\n')
print(json.dumps({'reads': tables['reads'], 'epss_first_date': tables['epss_first_date'], 'epss_steps': steps}, indent=1))
