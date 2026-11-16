#!/usr/bin/env python3
"""LH048 tabulator: measures 1 to 4 of the brief (studies/LH048/brief.md, protocol 0.1), offline.

Written 16 November 2026, after the baseline read (read-2026-11-10T1418Z) and the Monday read of 16 November
(read-2026-11-16T1420Z) were held. It reads only retained bytes under studies/LH048/data/ and selection.json; it
fetches nothing and changes nothing in the protocol. It implements the brief's measures as written and adds no
comparison; it writes no finding.

Usage:
  python3 -I studies/LH048/scripts/tabulate.py                 # every held read; writes data/tables.json
  python3 -I studies/LH048/scripts/tabulate.py --until 2026-11-10T1418Z --out -   # baseline only, to stdout

Output: one JSON document, keys sorted, no clock time, so a replay over the same bytes is byte-identical.
`as_of` holds the measures computed through each held read in turn ("the last read" being that read), so the
baseline's tabulation sits beside the latest.

Classes of missing evidence (brief, Missing evidence), kept distinct and never turned into a negative:
  unavailable at this read   body under 200 bytes, refusal, robots gate refusal, timeout, non-404 error status,
                             or a JSON source whose body does not parse (a challenge page, for instance)
  no record at this read     404 from the CVE record or NVD (or NVD answering with no vulnerability)
  not scored at this read    EPSS answered but held nothing for the CVE
  not given at this read     the record was read but lacks the field
  not listed at this read    absent from a KEV catalogue that was read
  not read at this read      the read's design did not request it (the linked set's CVE record and NVD on a
                             Monday read); added here, since the brief's classes assume the source was asked
  unknown                    unidentified and no-identifier units in every measure; any part that rests on one
                             of the classes above
"""
from datetime import date
from pathlib import Path
import argparse
import gzip
import html
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# --- the brief's fixed numbers -------------------------------------------------------------------------------
MIN_BODY = 200            # Missing evidence: a body under 200 bytes is unavailable
STEP_FACTOR = 2.0         # Measure 2: a day-on-day change by a factor of two or more, up or down
PCT_THRESHOLD = 0.5       # Measures 2 and 4: percentile above 0.5 / at or below 0.5
E2 = '2026-10-27'         # the post's datePublished (a day without a time)
# V, the vendor's own release date for the fix: the Chrome note's date and the Apple note's date as read at the
# discovery read (selection.json notes), LH036's E0 for Linux; Microsoft's is its releaseDate, read per read.
V_FIXED = {'chrome': '2026-10-20', 'safari': '2026-06-29', 'linux': '2026-10-15'}
VENDOR_HIGH_WORDS = {'High', 'Critical'}   # vendor words taken as given; Microsoft's 'Important' is not mapped

UNAVAILABLE = 'unavailable at this read'
NO_RECORD = 'no record at this read'
NOT_SCORED = 'not scored at this read'
NOT_GIVEN = 'not given at this read'
NOT_LISTED = 'not listed at this read'
NOT_READ = 'not read at this read'
UNKNOWN = 'unknown'
MISSING = {UNAVAILABLE, NOT_READ}          # states that are not a reading of the source at all


def is_missing(x):
    return isinstance(x, str) and x in MISSING

CLASSES = ('named', 'identified', 'ambiguous', 'unidentified', 'no identifier')
MSRC_FIELDS = ('severity', 'impact', 'baseScore', 'vectorString', 'exploited', 'publiclyDisclosed',
               'releaseDate', 'latestRevisionDate')
MSRC_RATING_FIELDS = ('severity', 'impact', 'baseScore', 'vectorString')


# --- thresholds as functions (tested in test_tabulate.py) ----------------------------------------------------
def cvss_band(score):
    """CVSS v3/v4 qualitative band: None 0.0, Low 0.1-3.9, Medium 4.0-6.9, High 7.0-8.9, Critical 9.0-10.0."""
    if score is None:
        return None
    s = float(score)
    if s >= 9.0:
        return 'Critical'
    if s >= 7.0:
        return 'High'
    if s >= 4.0:
        return 'Medium'
    if s > 0.0:
        return 'Low'
    return 'None'


def is_step(prev, cur):
    """A step: day-on-day change in score by a factor of two or more, up or down."""
    if prev is None or cur is None:
        return False
    if prev == 0 and cur == 0:
        return False
    if prev == 0 or cur == 0:
        return True
    return cur / prev >= STEP_FACTOR or prev / cur >= STEP_FACTOR


def above_threshold(pct):
    return pct > PCT_THRESHOLD


def body_state(row, file_exists, signal_with_records):
    """Classify one read_log row: 'ok', or one of the missing-evidence classes."""
    if row is None:
        return NOT_READ
    status = row.get('status')
    if not isinstance(status, int):
        return UNAVAILABLE                      # refusal by the gate, timeout, connection error
    if status == 404 and signal_with_records:
        return NO_RECORD
    if status != 200:
        return UNAVAILABLE
    if (row.get('bytes') or 0) < MIN_BODY or not file_exists:
        return UNAVAILABLE
    return 'ok'


# --- selection classes ---------------------------------------------------------------------------------------
def check_selection(sel):
    """Check every unit's class against the brief's definitions; raise on a contradiction. Returns notes."""
    notes = []
    units = sel['units']
    assert sel.get('rule_applied_at'), 'selection rule not applied'
    cand_steps = {}
    for u in units:
        for c in u.get('candidates', []):
            cand_steps.setdefault(c, []).append(u['step'])
    for u in units:
        cls, cves, cands = u['class'], u.get('cves', []), u.get('candidates', [])
        assert cls in CLASSES, (u['step'], cls)
        if cls == 'named':
            assert cves and not cands and u['chain'] in ('windows', 'linux'), u['step']
        elif cls == 'identified':
            assert len(cves) == 1 and not cands, u['step']
        elif cls == 'ambiguous':
            assert not cves and cands, u['step']
            if len(cands) == 1:
                # "more than one entry meets it" does not hold; the C1/C2 clause ("to both as ambiguous if it
                # matches either") must be what makes the unit ambiguous.
                shared = [s for s in cand_steps[cands[0]] if s != u['step']]
                assert u['step'] in ('C1', 'C2') and shared, u['step']
                notes.append('%s: one candidate, ambiguous by the C1/C2 sharing clause (shared with %s)'
                             % (u['step'], ', '.join(shared)))
        elif cls == 'unidentified':
            assert not cves and not cands, u['step']
        elif cls == 'no identifier':
            assert not cves and not cands and u['chain'] == 'android', u['step']
    chain_cves = {c for u in units for c in u.get('cves', []) + u.get('candidates', [])}
    overlap = chain_cves & set(sel.get('linked_set', []))
    assert not overlap, 'linked set overlaps the chains: %s' % sorted(overlap)
    return notes


def roles(sel):
    """Map each CVE to its group ('named_identified', 'ambiguous_candidate', 'linked_set'), units and chain."""
    out = {}
    for u in sel['units']:
        if u['class'] in ('named', 'identified'):
            for c in u['cves']:
                r = out.setdefault(c, {'group': 'named_identified', 'chain': u['chain'], 'units': []})
                r['units'].append('%s (%s)' % (u['step'], u['class']))
        elif u['class'] == 'ambiguous':
            for c in u['candidates']:
                r = out.setdefault(c, {'group': 'ambiguous_candidate', 'chain': u['chain'], 'units': []})
                assert r['group'] == 'ambiguous_candidate', c
                r['units'].append('%s (ambiguous)' % u['step'])
    for c in sel.get('linked_set', []):
        out[c] = {'group': 'linked_set', 'chain': 'chrome', 'units': ['linked set']}
    return out


# --- reading retained bytes ----------------------------------------------------------------------------------
class Read:
    def __init__(self, path):
        self.path = Path(path)
        self.label = self.path.name.split('-', 1)[1]
        rows = json.loads((self.path / 'read_log.json').read_text())
        self.log = {r['name']: r for r in rows}

    def raw(self, name, signal_with_records=False):
        row = self.log.get(name)
        f = self.path / (row.get('file') or '') if row and row.get('file') else None
        state = body_state(row, bool(f and f.exists()), signal_with_records)
        if state != 'ok':
            return state, None
        return 'ok', gzip.open(f).read()

    def json(self, name, signal_with_records=False):
        state, body = self.raw(name, signal_with_records)
        if state != 'ok':
            return state, None
        try:
            return 'ok', json.loads(body)
        except ValueError:
            return UNAVAILABLE, None

    def text(self, name):
        state, body = self.raw(name)
        if state != 'ok':
            return state, None
        return 'ok', body.decode('utf-8', 'replace')


def visible_text(h):
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    t = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    return re.sub(r'[ \t ]+', ' ', t)


CHROME_ENTRY = re.compile(r'\]\s*(Critical|High|Medium|Low)\s+(CVE-\d{4}-\d+):')


def chrome_words(page_html):
    words = {}
    for w, c in CHROME_ENTRY.findall(visible_text(page_html)):
        words.setdefault(c, set()).add(w)
    return words


def chrome_word(words, cve):
    w = words.get(cve)
    if not w:
        return NOT_GIVEN                        # the entry is not on the copy read
    if len(w) > 1:
        return 'conflicting on the page: ' + ', '.join(sorted(w))
    return next(iter(w))


APPLE_RATING = re.compile(r'(?i)\b(severity|rating|cvss)\b[^\n]*')


def apple_rating(page_html, cve):
    """Apple's rating for the entry, if its entry block gives one; else 'no vendor rating given' (a reading)."""
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', page_html)
    i = h.find(cve + ':')
    if i < 0:
        return NOT_GIVEN
    start = h.rfind('<h3', 0, i)
    end = h.find('</p>', i)
    block = visible_text(h[max(start, 0):end if end > 0 else i + 200])
    m = APPLE_RATING.search(block)
    return m.group(0).strip() if m else 'no vendor rating given'


def container_metrics(container):
    out = {}
    for m in container.get('metrics', []) or []:
        for k, v in m.items():
            if k.startswith('cvss') and isinstance(v, dict):
                key = k
                n = 2
                while key in out:
                    key = '%s#%d' % (k, n)
                    n += 1
                out[key] = {'score': v.get('baseScore'), 'vector': v.get('vectorString'),
                            'baseSeverity_given': v.get('baseSeverity', NOT_GIVEN),
                            'band': cvss_band(v.get('baseScore'))}
            elif k == 'other' and isinstance(v, dict):
                typ = v.get('type', 'other')
                content = v.get('content', {})
                key = 'other:' + typ
                out[key] = {'options': content.get('options', content)}
    return out


def read_cve_record(rd, cve):
    state, rec = rd.json('cve_org_' + cve, signal_with_records=True)
    if state != 'ok':
        return state
    meta = rec.get('cveMetadata', {})
    cons = rec.get('containers', {})
    cna = cons.get('cna', {})
    out = {'datePublished': meta.get('datePublished', NOT_GIVEN), 'dateUpdated': meta.get('dateUpdated', NOT_GIVEN),
           'cna': {'shortName': cna.get('providerMetadata', {}).get('shortName', meta.get('assignerShortName')),
                   'orgId': cna.get('providerMetadata', {}).get('orgId'),
                   'dateUpdated': cna.get('providerMetadata', {}).get('dateUpdated', NOT_GIVEN),
                   'metrics': container_metrics(cna)},
           'adp': {}}
    for a in cons.get('adp', []) or []:
        pm = a.get('providerMetadata', {})
        out['adp'][pm.get('shortName', pm.get('orgId', '?'))] = {
            'orgId': pm.get('orgId'), 'dateUpdated': pm.get('dateUpdated', NOT_GIVEN), 'metrics': container_metrics(a)}
    return out


def read_nvd(rd, cve, orgs):
    state, n = rd.json('nvd_' + cve, signal_with_records=True)
    if state != 'ok':
        return state
    vulns = n.get('vulnerabilities') or []
    if not vulns:
        return NO_RECORD
    cv = vulns[0].get('cve', {})
    metrics = []
    for k, arr in sorted((cv.get('metrics') or {}).items()):
        for m in arr:
            src = m.get('source', NOT_GIVEN)
            entry = {'key': k, 'source': src, 'source_name': orgs.get(src, src), 'type': m.get('type', NOT_GIVEN)}
            if 'cvssData' in m:
                s = m['cvssData'].get('baseScore')
                entry.update(score=s, vector=m['cvssData'].get('vectorString'), band=cvss_band(s))
            elif 'ssvcData' in m:
                entry.update(options=m['ssvcData'].get('options'))
            metrics.append(entry)
    cisa = {k: v for k, v in cv.items() if k.startswith('cisa')}
    return {'vulnStatus': cv.get('vulnStatus', NOT_GIVEN), 'lastModified': cv.get('lastModified', NOT_GIVEN),
            'metrics': metrics, 'cisaExploitAdd_fields': cisa or NOT_GIVEN}


def read_msrc(rd, cve):
    state, m = rd.json('msrc_' + cve)
    if state != 'ok':
        return state
    vals = m.get('value') or []
    if not vals:
        return NO_RECORD
    v = vals[0]
    return {k: v.get(k, NOT_GIVEN) for k in MSRC_FIELDS}


def read_kev(rd):
    state, k = rd.json('kev')
    if state != 'ok' or not isinstance(k.get('vulnerabilities'), list):
        return UNAVAILABLE if state == 'ok' else state, None
    cat = {'catalogVersion': k.get('catalogVersion', NOT_GIVEN), 'dateReleased': k.get('dateReleased', NOT_GIVEN),
           'count': k.get('count', NOT_GIVEN)}
    entries = {v.get('cveID'): v for v in k['vulnerabilities']}
    return cat, entries


def read_epss(rd):
    """{cve: {date: (epss, percentile)}}, and whether every EPSS batch of the read was readable."""
    names = sorted(n for n in rd.log if n.startswith('epss_'))
    if not names:
        return {}, NOT_READ
    out, all_ok = {}, True
    for n in names:
        state, d = rd.json(n)
        if state != 'ok' or not isinstance(d.get('data'), list):
            all_ok = False
            continue
        for r in d['data']:
            s = out.setdefault(r['cve'], {})
            s[r['date']] = (float(r['epss']), float(r['percentile']))
            for t in r.get('time-series', []) or []:
                s.setdefault(t['date'], (float(t['epss']), float(t['percentile'])))
    return out, ('ok' if all_ok else UNAVAILABLE)


# --- per-read state for one flaw -----------------------------------------------------------------------------
def vendor_source(chain):
    return {'chrome': 'chrome_release', 'safari': 'apple_note', 'windows': 'msrc', 'linux': 'kernel CNA'}[chain]


def snapshot(rd, cve, chain, cache):
    rec = read_cve_record(rd, cve)
    orgs = {}
    if isinstance(rec, dict):
        if rec['cna'].get('orgId'):
            orgs[rec['cna']['orgId']] = rec['cna']['shortName']
        for short, a in rec['adp'].items():
            if a.get('orgId'):
                orgs[a['orgId']] = short
    nvd = read_nvd(rd, cve, orgs)
    if chain == 'chrome':
        if ('chrome', rd.label) not in cache:
            st, h = rd.text('chrome_release')
            cache[('chrome', rd.label)] = chrome_words(h) if st == 'ok' else st
        w = cache[('chrome', rd.label)]
        vendor = {'chrome_word': w if isinstance(w, str) else chrome_word(w, cve)}
    elif chain == 'safari':
        st, h = rd.text('apple_note')
        vendor = {'apple_rating': apple_rating(h, cve) if st == 'ok' else st}
    elif chain == 'windows':
        vendor = {'msrc': read_msrc(rd, cve)}
    else:
        vendor = {'kernel_cna': 'the CNA container of the CVE record (see cve_record.cna)'}
    return {'vendor': vendor, 'cve_record': rec, 'nvd': nvd}


def flatten(snap):
    """(rating keys, other keys) per source group: {group: dict or missing-state}."""
    rating, other = {}, {}
    v = snap['vendor']
    if 'chrome_word' in v:
        rating['vendor'] = v['chrome_word'] if is_missing(v['chrome_word']) else {'chrome_word': v['chrome_word']}
    elif 'apple_rating' in v:
        rating['vendor'] = v['apple_rating'] if is_missing(v['apple_rating']) else {'apple_rating': v['apple_rating']}
    elif 'msrc' in v:
        m = v['msrc']
        if isinstance(m, dict):
            rating['vendor'] = {'msrc:' + k: m[k] for k in MSRC_RATING_FIELDS}
            other['vendor'] = {'msrc:' + k: m[k] for k in MSRC_FIELDS if k not in MSRC_RATING_FIELDS}
        else:
            rating['vendor'] = other['vendor'] = m if is_missing(m) else {'msrc': m}
    rec = snap['cve_record']
    if isinstance(rec, dict):
        r, o = {}, {'datePublished': rec['datePublished'], 'dateUpdated': rec['dateUpdated'],
                    'cna:%s:dateUpdated' % rec['cna']['shortName']: rec['cna']['dateUpdated']}
        for k, m in rec['cna']['metrics'].items():
            r['cna:%s:%s' % (rec['cna']['shortName'], k)] = m
        for short, a in rec['adp'].items():
            o['adp:%s:dateUpdated' % short] = a['dateUpdated']
            o['adp:%s:present' % short] = True
            for k, m in a['metrics'].items():
                r['adp:%s:%s' % (short, k)] = m
        rating['cve_record'], other['cve_record'] = r, o
    else:
        rating['cve_record'] = other['cve_record'] = rec if is_missing(rec) else {'record': rec}
    nvd = snap['nvd']
    if isinstance(nvd, dict):
        r = {}
        for m in nvd['metrics']:
            k = '%s:%s:%s' % (m['key'], m['source_name'], m['type'])
            r[k] = {x: m[x] for x in ('score', 'vector', 'band', 'options') if x in m}
        rating['nvd'] = r
        other['nvd'] = {'vulnStatus': nvd['vulnStatus'], 'lastModified': nvd['lastModified'],
                        'cisaExploitAdd_fields': nvd['cisaExploitAdd_fields']}
    else:
        rating['nvd'] = other['nvd'] = nvd if is_missing(nvd) else {'record': nvd}
    return rating, other


def changes(labels, per_read):
    """Every change of a key's value between successive reads at which its source was read, with the interval:
    after the last read that did not show it, at or before the first that did."""
    out = []
    groups = sorted({g for lab in labels for g in per_read[lab]})
    for g in groups:
        keys = sorted({k for lab in labels if isinstance(per_read[lab].get(g), dict) for k in per_read[lab][g]})
        for k in keys:
            last = None
            for lab in labels:
                cur = per_read[lab].get(g, NOT_READ)
                if not isinstance(cur, dict):
                    continue                    # a missed read stays missed; the interval widens
                val = cur.get(k, NOT_GIVEN)
                if last is not None and val != last[1]:
                    out.append({'source': g, 'key': k, 'from': last[1], 'to': val,
                                'after_read': last[0], 'at_or_before_read': lab})
                last = (lab, val)
    return out


def bands(snap):
    """CVSS bands by side: vendor or CNA; NVD (its own, Primary) or CISA (ADP container)."""
    side_a, side_b, all_high = [], [], []
    v = snap['vendor']
    m = v.get('msrc')
    if isinstance(m, dict) and m.get('baseScore') not in (None, NOT_GIVEN, ''):
        side_a.append({'source': 'Microsoft (Security Update Guide baseScore)', 'score': float(m['baseScore']),
                       'band': cvss_band(m['baseScore'])})
    rec = snap['cve_record']
    if isinstance(rec, dict):
        for k, x in sorted(rec['cna']['metrics'].items()):
            if 'band' in x:
                side_a.append({'source': 'CNA %s %s' % (rec['cna']['shortName'], k), 'score': x['score'],
                               'band': x['band']})
        for short, a in sorted(rec['adp'].items()):
            if short == 'CISA-ADP':
                for k, x in sorted(a['metrics'].items()):
                    if 'band' in x:
                        side_b.append({'source': 'CISA-ADP %s' % k, 'score': x['score'], 'band': x['band']})
    nvd = snap['nvd']
    if isinstance(nvd, dict):
        for x in nvd['metrics']:
            if 'band' in x and x['type'] == 'Primary':
                side_b.append({'source': 'NVD %s (Primary)' % x['key'], 'score': x['score'], 'band': x['band']})
    return side_a, side_b


def agreement(side_a, side_b, snap):
    if not side_a or not side_b:
        missing = []
        if not side_a:
            missing.append('no vendor or CNA CVSS band')
        if not side_b:
            missing.append('no NVD (Primary) or CISA ADP CVSS band')
        unread = [g for g in ('cve_record', 'nvd') if is_missing(snap[g])]
        if unread:
            return UNKNOWN + ' (%s: %s)' % (', '.join(unread), ', '.join(snap[g] for g in unread))
        return 'not comparable: ' + '; '.join(missing)
    a, b = {x['band'] for x in side_a}, {x['band'] for x in side_b}
    return 'agree' if a == b and len(a) == 1 else 'differ'


def high_or_critical(snap):
    """Sources rating the flaw High or Critical at this read, and whether any rating source was missing."""
    hits, missing = [], []
    v = snap['vendor']
    for key in ('chrome_word', 'apple_rating'):
        if key in v:
            if is_missing(v[key]):
                missing.append('vendor page: ' + v[key])
            elif v[key] in VENDOR_HIGH_WORDS:
                hits.append('vendor word %s' % v[key])
    if 'msrc' in v:
        m = v['msrc']
        if is_missing(m):
            missing.append('msrc: ' + m)
        elif isinstance(m, dict):
            if m.get('severity') in VENDOR_HIGH_WORDS:
                hits.append('Microsoft severity %s' % m['severity'])
    a, b = bands(snap)
    for x in a + b:
        if x['band'] in VENDOR_HIGH_WORDS:
            hits.append('%s %s %s' % (x['source'], x['score'], x['band']))
    nvd = snap['nvd']
    if isinstance(nvd, dict):
        for x in nvd['metrics']:
            if 'band' in x and x['type'] != 'Primary' and x['band'] in VENDOR_HIGH_WORDS:
                hits.append('NVD-listed %s from %s (%s) %s %s' % (x['key'], x['source_name'], x['type'],
                                                                   x['score'], x['band']))
    for g in ('cve_record', 'nvd'):
        if is_missing(snap[g]):
            missing.append('%s: %s' % (g, snap[g]))
    return hits, missing


# --- EPSS ----------------------------------------------------------------------------------------------------
def merge_epss(labels, epss_by_read, cve):
    """Each date's value from the earliest read holding it; later reads' differing values listed."""
    series, later = {}, []
    for lab in labels:
        data, _ = epss_by_read[lab]
        for d, (e, p) in sorted(data.get(cve, {}).items()):
            if d not in series:
                series[d] = {'epss': e, 'percentile': p, 'from_read': lab}
            elif (series[d]['epss'], series[d]['percentile']) != (e, p):
                later.append({'date': d, 'held': [series[d]['epss'], series[d]['percentile']],
                              'later_read': lab, 'later_value': [e, p]})
    return series, later


def days(a, b):
    return (date.fromisoformat(a) - date.fromisoformat(b)).days


def epss_measure(labels, epss_by_read, cve, events, P=None):
    series, later = merge_epss(labels, epss_by_read, cve)
    per_read = {}
    for lab in labels:
        data, state = epss_by_read[lab]
        s = data.get(cve)
        read_day = '%s-%s-%s' % (lab[0:4], lab[5:7], lab[8:10])
        if s:
            newest = max(s)
            per_read[lab] = {'newest_date_returned': newest, 'epss': s[newest][0], 'percentile': s[newest][1],
                             'on_read_date': ({'epss': series[read_day]['epss'],
                                               'percentile': series[read_day]['percentile'],
                                               'from_read': series[read_day]['from_read']}
                                              if read_day in series else
                                              NOT_GIVEN + ' (no value dated the read day is held)')}
        else:
            per_read[lab] = NOT_SCORED if state == 'ok' else state
    if not series:
        return {'per_read': per_read, 'series': [], 'first_date_scored': UNKNOWN, 'highest': UNKNOWN,
                'percentile_ever_above_0_5': UNKNOWN, 'steps': UNKNOWN, 'last_date_held': UNKNOWN,
                'later_read_differences': later}
    dates = sorted(series)
    steps, gaps = [], []
    for i in range(1, len(dates)):
        d0, d1 = dates[i - 1], dates[i]
        e0, e1 = series[d0]['epss'], series[d1]['epss']
        if not is_step(e0, e1):
            continue
        rec = {'date': d1, 'from': e0, 'to': e1, 'direction': 'up' if e1 > e0 else 'down',
               'factor': round(max(e0, e1) / min(e0, e1), 6) if min(e0, e1) > 0 else 'infinite'}
        if days(d1, d0) != 1:
            rec['note'] = 'previous date held is %s, not the day before: not day-on-day, so not a step' % d0
            gaps.append(rec)
            continue
        for name, ev in sorted(events.items()):
            rec['days_from_' + name] = days(d1, ev[:10]) if re.match(r'^\d{4}-\d{2}-\d{2}', str(ev)) else ev
        steps.append(rec)
    hi = max(dates, key=lambda d: (series[d]['epss'], d))
    first_hi = min(d for d in dates if series[d]['epss'] == series[hi]['epss'])
    p = P
    return {
        'per_read': per_read,
        'series': [dict(date=d, **series[d]) for d in dates],
        'series_note': ('from P (%s)' % p if p and dates[0] <= p[:10] else
                        'from the earliest date returned (%s); P is %s' % (dates[0], p)),
        'first_date_scored': dates[0],
        'highest': {'epss': series[hi]['epss'], 'first_date': first_hi},
        'percentile_ever_above_0_5': any(above_threshold(series[d]['percentile']) for d in dates),
        'steps': steps,
        'factor_two_changes_across_missing_dates': gaps,
        'last_date_held': {'date': dates[-1], 'epss': series[dates[-1]]['epss'],
                           'percentile': series[dates[-1]]['percentile']},
        'later_read_differences': later,
    }


# --- KEV -----------------------------------------------------------------------------------------------------
def kev_measure(labels, kev_by_read, cve):
    per_read, first_listed, last_not = {}, None, None
    for lab in labels:
        cat, entries = kev_by_read[lab]
        if entries is None:
            per_read[lab] = cat
            continue
        e = entries.get(cve)
        if e:
            per_read[lab] = {'listed': True, 'catalog': cat,
                             **{k: e.get(k, NOT_GIVEN) for k in ('dateAdded', 'dueDate',
                                                                 'knownRansomwareCampaignUse', 'notes')}}
            if first_listed is None:
                first_listed = lab
        else:
            per_read[lab] = {'listed': False, 'state': NOT_LISTED, 'catalog': cat}
            if first_listed is None:
                last_not = lab
    out = {'per_read': per_read}
    if first_listed:
        out['K'] = per_read[first_listed]['dateAdded']
        out['interval'] = {'after_read': last_not or 'no earlier read', 'at_or_before_read': first_listed}
    else:
        out['K'] = 'no K: not listed at any read held'
    return out


# --- assembly ------------------------------------------------------------------------------------------------
def tabulate_flaw(cve, role, labels, snaps, epss_by_read, kev_by_read):
    last = labels[-1]
    rating, other = {}, {}
    for lab in labels:
        rating[lab], other[lab] = flatten(snaps[lab])
    kev = kev_measure(labels, kev_by_read, cve)
    rec_last = next((snaps[l]['cve_record'] for l in reversed(labels) if isinstance(snaps[l]['cve_record'], dict)),
                    None)
    P = rec_last['datePublished'] if rec_last else UNKNOWN
    if role['chain'] == 'windows':
        m = next((snaps[l]['vendor']['msrc'] for l in reversed(labels)
                  if isinstance(snaps[l]['vendor'].get('msrc'), dict)), None)
        V = m['releaseDate'][:10] if m and m.get('releaseDate') not in (None, NOT_GIVEN) else UNKNOWN
    else:
        V = V_FIXED[role['chain']]
    K = kev['K'] if not str(kev['K']).startswith('no K') else 'no K (not listed at any read held)'
    epss = epss_measure(labels, epss_by_read, cve, {'E2': E2, 'V': V, 'K': K}, P)
    a, b = bands(snaps[last])
    hits, missing = high_or_critical(snaps[last])
    part1 = True if hits else (UNKNOWN if missing else False)
    ldh = epss.get('last_date_held')
    part2 = (ldh['percentile'] <= PCT_THRESHOLD) if isinstance(ldh, dict) else UNKNOWN
    kl = kev['per_read'][last]
    part3 = (not kl['listed']) if isinstance(kl, dict) else UNKNOWN
    parts = [part1, part2, part3]
    meets = False if False in parts else (UNKNOWN if UNKNOWN in parts else True)
    return {
        'units': role['units'],
        'chain': role['chain'],
        'events': {'E2': E2, 'P': P, 'V': V, 'K': K, 'V_source': vendor_source(role['chain'])},
        'measure1_severity': {
            'per_read': {lab: snaps[lab] for lab in labels},
            'bands_at_last_read': {'vendor_or_cna': a, 'nvd_or_cisa': b},
            'agreement_at_last_read': agreement(a, b, snaps[last]),
            'rating_changes': changes(labels, rating),
            'other_changes': changes(labels, other),
        },
        'measure2_epss': epss,
        'measure3_kev': kev,
        'measure4_gap_parts': {
            'rated_high_or_critical': part1, 'rated_by': hits, 'rating_sources_missing': missing,
            'epss_percentile_at_or_below_0_5_on_last_date_held': part2,
            'epss_last_date_held': ldh if isinstance(ldh, dict) else UNKNOWN,
            'not_in_kev_at_last_read': part3,
            'meets_all_three': meets,
        },
    }


def tabulate(data_dir, sel, until=None):
    notes = check_selection(sel)
    reads = sorted((Read(p) for p in Path(data_dir).glob('read-*') if (p / 'read_log.json').exists()),
                   key=lambda r: r.label)
    if until:
        reads = [r for r in reads if r.label <= until]
    assert reads, 'no read held'
    disc = sorted(Path(data_dir).glob('discover-*'))
    role = roles(sel)
    cache = {}
    snaps = {c: {r.label: snapshot(r, c, role[c]['chain'], cache) for r in reads} for c in role}
    epss_by_read = {r.label: read_epss(r) for r in reads}
    kev_by_read = {r.label: read_kev(r) for r in reads}
    disc_words = {}
    if disc:
        st, h = Read(disc[-1]).text('chrome_release')
        if st == 'ok':
            w = chrome_words(h)
            disc_words = {c: chrome_word(w, c) for c in role if role[c]['chain'] == 'chrome'}
    labels_all = [r.label for r in reads]
    as_of = {}
    for i in range(len(labels_all)):
        labels = labels_all[:i + 1]
        groups = {'named_identified': {}, 'ambiguous_candidates': {}, 'linked_set': {}}
        key = {'named_identified': 'named_identified', 'ambiguous_candidate': 'ambiguous_candidates',
               'linked_set': 'linked_set'}
        for c in sorted(role):
            t = tabulate_flaw(c, role[c], labels, snaps[c], epss_by_read, kev_by_read)
            if c in disc_words:
                t['measure1_severity']['chrome_word_on_discovery_copy'] = {
                    'read': disc[-1].name, 'word': disc_words[c],
                    'note': 'the discovery read is not a signals read; shown beside, never substituted'}
            groups[key[role[c]['group']]][c] = t
        m4 = {g: {c: groups[g][c]['measure4_gap_parts']['meets_all_three'] for c in sorted(groups[g])}
              for g in groups}
        chains = {}
        for u in sel['units']:
            ch = chains.setdefault(u['chain'], {'units': []})
            ent = {'step': u['step'], 'class': u['class']}
            if u['class'] in ('named', 'identified'):
                ent['flaws'] = {c: groups['named_identified'][c]['measure4_gap_parts']['meets_all_three']
                                for c in u['cves']}
            elif u['class'] == 'ambiguous':
                ent['candidates_reported_apart'] = u['candidates']
            else:
                ent['signals'] = UNKNOWN
            ch['units'].append(ent)
        for ch in chains.values():
            ch['has_named_or_identified_flaw'] = any('flaws' in e for e in ch['units'])
        as_of[labels[-1]] = {
            'reads': labels,
            'last_read': labels[-1],
            'flaws': groups,
            'measure4_gap': {
                'named_identified': m4['named_identified'],
                'ambiguous_candidates_reported_apart': m4['ambiguous_candidates'],
                'linked_set_described_apart': m4['linked_set'],
                'note': ('measure 4 is defined for identified or named flaws; the parts are computed for the '
                         'ambiguous candidates and the linked set too, and kept in their own lists, never pooled'),
            },
            'chains_side_by_side': chains,
        }
    unknown_units = [{'chain': u['chain'], 'step': u['step'], 'class': u['class'],
                      'all_measures': UNKNOWN} for u in sel['units'] if u['class'] in ('unidentified', 'no identifier')]
    return {
        '_about': ('LH048 tables: measures 1 to 4 of brief.md (protocol 0.1), tabulated offline from retained bytes '
                   'by scripts/tabulate.py, written 16 November 2026 after the baseline and the 16 November read '
                   'were held. A tabulation, not a finding.'),
        'brief': 'studies/LH048/brief.md',
        'selection_rule_applied_at': sel['rule_applied_at'],
        'selection_checks': notes,
        'thresholds': {'min_body_bytes': MIN_BODY, 'epss_step_factor': STEP_FACTOR,
                       'percentile_threshold': PCT_THRESHOLD,
                       'cvss_bands': 'None 0.0; Low 0.1-3.9; Medium 4.0-6.9; High 7.0-8.9; Critical 9.0-10.0',
                       'vendor_words_counted_high_or_critical': sorted(VENDOR_HIGH_WORDS)},
        'units_unknown_in_every_measure': unknown_units,
        'reads_held': labels_all,
        'as_of': as_of,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default=str(ROOT / 'data'))
    ap.add_argument('--selection', default=str(ROOT / 'selection.json'))
    ap.add_argument('--until', help='last read label to include, e.g. 2026-11-10T1418Z')
    ap.add_argument('--out', default=str(ROOT / 'data' / 'tables.json'), help="path, or '-' for stdout")
    a = ap.parse_args(argv)
    sel = json.loads(Path(a.selection).read_text())
    out = json.dumps(tabulate(a.data, sel, a.until), indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    if a.out == '-':
        sys.stdout.write(out)
    else:
        Path(a.out).write_text(out)


if __name__ == '__main__':
    main()
