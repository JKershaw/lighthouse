#!/usr/bin/env python3
"""LH044 collector, as fixed in studies/LH044/brief.md (protocol 0.1). Run only under a schedule
row. Stops working after END: the study's requests end on a fixed date.

  --read LABEL         the weekly panel read: for each service, its host's robots.txt (with up to
                       five redirects followed, amendment 3), then at most one probe if robots.txt
                       allows it. At most HOST_CAP (7) requests to any host in a read; no retries;
                       a probe's redirect is recorded, not followed.
  --classify LABEL     (offline) re-run the classifier over a read's retained responses.
  --wayback LABEL      Wayback Machine checks for that read's walled services (brief, measure 5).
  --httparchive LABEL  one request for HTTP Archive's monthly adoption counts (context, measure 6).
  --statements LABEL FILE   fetch operator statement pages listed in FILE (id,operator,url).

Email addresses in kept headers and text bodies are replaced with a placeholder before saving
(scripts/redact_emails.py, the keeper, 8 November 2026); readlog.csv's sha256 is of the bytes
received. Everything is kept under data/<kind>-<LABEL>/: readlog.csv (one row per request), each response's
headers (<n>.h) and first 64 KiB of body (<n>.b), and the derived tables. LABEL is a UTC time,
for example 2026-11-08T2000Z. A label already held is refused, never overwritten (except
--classify, which only rewrites derived tables).

A wall is the observation. The collector never answers a challenge, runs no JavaScript, keeps no
cookies, sends no credentials, submits no form, and does not retry a refused request.
"""
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit, quote, urljoin
from urllib.request import getproxies, proxy_bypass_environment
import argparse
import csv
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh044lib import fetch, header, UA_PLAIN, UA_COMPAT, ROBOTS_TOKEN, utcnow  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from redact_emails import redact_bytes  # noqa: E402  (the keeper, 8 November 2026: addresses withheld)
from classify import (classify, parse_robots, robots_allowed, AI_TOKENS, WALL_CLASSES,  # noqa: E402
                      CLASSIFIER_VERSION)

ROOT = Path(__file__).resolve().parents[1]
END = datetime(2027, 2, 9, 23, 59, 59, tzinfo=timezone.utc)
PAUSE = 1.5
# Amendment 3 (8 November 2026, post hoc, from read 1): robots.txt redirects are followed, up to
# ROBOTS_MAX_REDIRECTS hops, same-site or cross-site, each hop a logged request; probes still
# follow none. No host gets more than HOST_CAP requests in a read (1 robots.txt + 5 redirects +
# 1 probe for a single service), enforced across all services.
ROBOTS_MAX_REDIRECTS = 5
HOST_CAP = 7
ACCEPT = {
    'page': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
    'api': 'application/json, application/xml;q=0.9, */*;q=0.5',
    'file': '*/*',
}
WAYBACK_MAX = 60
WAYBACK_PAUSE = 4.0
WAYBACK_PER_SERVICE = 8
HA_TECH = ['Cloudflare Bot Management', 'Cloudflare Turnstile', 'Akamai Bot Manager', 'DataDome',
           'PerimeterX', 'Kasada', 'AntiBot.Cloud', 'AWS WAF Captcha', 'hCaptcha', 'reCAPTCHA',
           'Friendly Captcha']
LOG_FIELDS = ['n', 'service', 'kind', 'url', 'utc', 'status', 'error', 'error_detail', 'content_type',
              'bytes', 'truncated', 'sha256', 'elapsed_ms', 'ua', 'route']


def route(url):
    host = urlsplit(url).hostname or ''
    scheme = urlsplit(url).scheme
    if scheme == 'http':
        return 'direct-http'
    if proxy_bypass_environment(host) or 'https' not in getproxies():
        return 'direct'
    return 'egress-proxy'


def check_window():
    if utcnow() > END:
        sys.exit('LH044 ended on %s; the collector makes no more requests.' % END.isoformat())


def load_panel():
    rows = []
    for name in ('named.csv', 'drawn.csv'):
        p = ROOT / 'panel' / name
        for r in csv.DictReader(open(p)):
            r['stratum'] = 'named' if name == 'named.csv' else 'drawn'
            rows.append(r)
    return rows


class Recorder:
    def __init__(self, outdir):
        self.dir = outdir
        self.dir.mkdir(parents=True)
        self.n = 0
        self.host_counts = {}
        self.f = open(self.dir / 'readlog.csv', 'w', newline='')
        self.w = csv.DictWriter(self.f, fieldnames=LOG_FIELDS)
        self.w.writeheader()

    def get(self, service, kind, url, ua, accept, cap=65536):
        self.n += 1
        h = (urlsplit(url).hostname or '').lower()
        self.host_counts[h] = self.host_counts.get(h, 0) + 1
        r = fetch(url, ua=ua, accept=accept, cap=cap)
        # Email addresses are withheld from what is kept (the keeper, 8 November 2026); the
        # readlog's sha256 stays the hash of the bytes received. Classification reads the kept bytes.
        htext = 'HTTP %s\n' % r['status'] + ''.join('%s: %s\n' % kv for kv in r['headers'])
        (self.dir / ('%04d.h' % self.n)).write_bytes(redact_bytes(htext.encode('utf-8', 'replace'))[0])
        body = r['body'] if b'\x00' in r['body'][:4096] else redact_bytes(r['body'])[0]
        (self.dir / ('%04d.b' % self.n)).write_bytes(body)
        self.w.writerow({'n': self.n, 'service': service, 'kind': kind, 'url': url, 'utc': r['utc'],
                         'status': r['status'] if r['status'] is not None else '', 'error': r['error'] or '',
                         'error_detail': r['error_detail'], 'content_type': header(r, 'content-type'),
                         'bytes': len(r['body']), 'truncated': r['truncated'], 'sha256': r['sha256'],
                         'elapsed_ms': r['elapsed_ms'], 'ua': 'compat' if ua == UA_COMPAT else 'plain',
                         'route': route(url)})
        self.f.flush()
        r['n'] = self.n
        time.sleep(PAUSE)
        return r

    def close(self):
        self.f.close()


def retry_after_until(res):
    v = header(res, 'retry-after').strip()
    if not v:
        return None
    try:
        return datetime.strptime(res['utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) + \
            timedelta(seconds=int(v))
    except ValueError:
        try:
            return parsedate_to_datetime(v)
        except (TypeError, ValueError):
            return None


def previous_holds(label):
    """Retry-After times from the latest earlier read, so a service that asked to be left alone
    past this read is skipped (brief, 'Lighthouse's own requests')."""
    reads = sorted(p for p in (ROOT / 'data').glob('read-*') if p.name < 'read-' + label)
    if not reads:
        return {}
    p = reads[-1] / 'classes.csv'
    if not p.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(p)):
        if r.get('retry_after_until'):
            out[r['id']] = datetime.fromisoformat(r['retry_after_until'])
    return out


def host_full(rec, url):
    return rec.host_counts.get((urlsplit(url).hostname or '').lower(), 0) >= HOST_CAP


def fetch_robots(rec, sid, url):
    """robots.txt with its redirects followed (amendment 3): at most ROBOTS_MAX_REDIRECTS hops,
    each logged as kind robots-redirect-<k>. Returns (final response or None, chain of request
    numbers, cut) where cut is '' or 'host_cap'. A chain that is still redirecting after the
    last allowed hop ends on that redirect, which robots_outcome reads as robots_redirect."""
    chain, cur, r = [], url, None
    for hop in range(ROBOTS_MAX_REDIRECTS + 1):
        if host_full(rec, cur):
            return r, chain, 'host_cap'
        r = rec.get(sid, 'robots' if hop == 0 else 'robots-redirect-%d' % hop, cur, UA_PLAIN,
                    'text/plain, */*;q=0.5')
        chain.append(r['n'])
        if r['error'] or not r['status'] or not (300 <= r['status'] < 400):
            break
        loc = header(r, 'location').strip()
        nxt = urljoin(cur, loc) if loc else ''
        if urlsplit(nxt).scheme not in ('http', 'https'):
            break
        if hop == ROBOTS_MAX_REDIRECTS:
            break
        cur = nxt
    return r, chain, ''


def robots_outcome(res):
    """What a robots.txt response allows. Returns (state, groups, class, detail)."""
    if res['error']:
        return 'unreachable', None, 'robots_unreachable', res['error']
    st = res['status']
    cls, det = classify(st, None, res['headers'], res['body'], 'file', '', res['url'])
    if cls == 'unread_proxy':
        # this container's own refusal, e.g. a redirect onto github.com: not the origin's answer
        return 'unreachable', None, 'robots_unreachable', det
    if cls in ('challenge', 'rate_limited'):
        return 'wall', None, 'wall_at_robots', cls + ':' + det
    if 200 <= st < 300:
        return 'parsed', parse_robots(res['body'].decode('utf-8', 'replace')), '', ''
    if 300 <= st < 400:
        return 'redirect', None, 'robots_redirect', header(res, 'location')[:120]
    if 400 <= st < 500:
        return 'unavailable', [], '', ''   # RFC 9309: unavailable, crawling allowed
    return 'unreachable', None, 'robots_unreachable', str(st)


def do_read(label):
    check_window()
    out = ROOT / 'data' / ('read-' + label)
    if out.exists():
        sys.exit('read %s already held' % label)
    panel = load_panel()
    holds = previous_holds(label)
    rec = Recorder(out)
    services = []
    t0 = utcnow()
    for s in panel:
        sid = s['id']
        row = dict(s)
        row.update({'robots_n': '', 'robots_chain': [], 'robots_state': '', 'probe_n': '', 'pre_class': '',
                    'pre_detail': ''})
        hold = holds.get(sid)
        if hold and hold > utcnow():
            row.update({'pre_class': 'skipped_retry_after', 'pre_detail': hold.isoformat()})
            services.append(row)
            continue
        u = urlsplit(s['url'])
        robots_url = '%s://%s/robots.txt' % (u.scheme, u.netloc)
        rr, chain, cut = fetch_robots(rec, sid, robots_url)
        row['robots_chain'] = chain
        if rr is None or cut:
            row.update({'robots_n': chain[-1] if chain else '', 'robots_state': 'host_cap',
                        'pre_class': 'robots_unreachable', 'pre_detail': 'host cap reached'})
            services.append(row)
            continue
        state, groups, pcls, pdet = robots_outcome(rr)
        row['robots_n'], row['robots_state'] = rr['n'], state
        if pcls:
            row.update({'pre_class': pcls, 'pre_detail': pdet})
            services.append(row)
            continue
        if not robots_allowed(groups, ROBOTS_TOKEN, s['url']):
            row.update({'pre_class': 'robots_disallowed', 'pre_detail': ''})
            services.append(row)
            continue
        if host_full(rec, s['url']):
            row.update({'pre_class': 'not_probed_host_cap', 'pre_detail': ''})
            services.append(row)
            continue
        ua = UA_COMPAT if s['surface'] == 'page' else UA_PLAIN
        pr = rec.get(sid, 'probe', s['url'], ua, ACCEPT[s['surface']])
        row['probe_n'] = pr['n']
        services.append(row)
    rec.close()
    t1 = utcnow()
    with open(out / 'services.json', 'w') as f:
        json.dump({'label': label, 'started': t0.isoformat(), 'finished': t1.isoformat(),
                   'services': services}, f, indent=1)
    do_classify(label)


def _load_resp(d, n):
    if not n:
        return None
    lines = (d / ('%04d.h' % int(n))).read_text().splitlines()
    st = lines[0].split(' ', 1)[1] if lines else 'None'
    headers = [tuple(x.split(': ', 1)) if ': ' in x else (x, '') for x in lines[1:] if x]
    return {'status': None if st == 'None' else int(st), 'headers': headers,
            'body': (d / ('%04d.b' % int(n))).read_bytes()}


def do_classify(label):
    d = ROOT / 'data' / ('read-' + label)
    meta = json.load(open(d / 'services.json'))
    log = {r['n']: r for r in csv.DictReader(open(d / 'readlog.csv'))}
    rows, robots_rows = [], []
    for s in meta['services']:
        cls, det, status, ra = s['pre_class'], s['pre_detail'], '', ''
        if s['robots_n'] and not s['probe_n'] and cls not in ('robots_disallowed', 'not_probed_host_cap') \
                and s['robots_state'] != 'host_cap':
            # re-read the kept robots.txt response with the current classifier
            rl = log[str(s['robots_n'])]
            rresp = _load_resp(d, s['robots_n'])
            rresp.update({'error': rl['error'] or None, 'url': rl['url']})
            state, _, pcls, pdet = robots_outcome(rresp)
            if pcls:
                cls, det = pcls, pdet
            else:
                cls, det = 'unprobed', 'robots.txt now reads as %s; no probe was sent at the read' % state
        if s['probe_n']:
            lr = log[str(s['probe_n'])]
            resp = _load_resp(d, s['probe_n'])
            err = lr['error'] or None
            cls, det = classify(resp['status'] or 0, err, resp['headers'], resp['body'],
                                s['surface'], s['marker'], s['url'])
            status = lr['status']
            if cls in ('rate_limited',):
                u = retry_after_until({'headers': resp['headers'], 'utc': lr['utc']})
                ra = u.isoformat() if u else ''
        rows.append({'id': s['id'], 'stratum': s['stratum'], 'class_group': s['class'], 'host': s['host'],
                     'surface': s['surface'], 'prior': s['prior'], 'robots_state': s['robots_state'],
                     'status': status, 'class': cls, 'detail': det,
                     'wall': 'yes' if cls in WALL_CLASSES else 'no', 'retry_after_until': ra,
                     'classifier': CLASSIFIER_VERSION})
        if s['robots_n'] and s['robots_state'] == 'parsed':
            g = parse_robots(_load_resp(d, s['robots_n'])['body'].decode('utf-8', 'replace'))
            root = '%s://%s/' % (urlsplit(s['url']).scheme, urlsplit(s['url']).netloc)
            rr = {'id': s['id'], 'host': s['host'],
                  'lighthouse_probe_allowed': robots_allowed(g, ROBOTS_TOKEN, s['url']),
                  'star_root_allowed': robots_allowed(g, '*', root),
                  'star_probe_allowed': robots_allowed(g, '*', s['url'])}
            for t in AI_TOKENS:
                rr[t] = robots_allowed(g, t, root)
            robots_rows.append(rr)
    with open(d / 'classes.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    if robots_rows:
        with open(d / 'robots.csv', 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(robots_rows[0].keys()))
            w.writeheader()
            w.writerows(robots_rows)
    # summary
    summ = {'label': label, 'classifier': CLASSIFIER_VERSION, 'requests': len(log),
            'bytes_retained': sum(int(r['bytes']) for r in log.values()), 'by_stratum': {}}
    for r in rows:
        summ['by_stratum'].setdefault(r['stratum'], {}).setdefault(r['class'], 0)
        summ['by_stratum'][r['stratum']][r['class']] += 1
    hosts = {}
    for r in log.values():
        h = urlsplit(r['url']).hostname
        hosts[h] = hosts.get(h, 0) + 1
    summ['max_requests_to_one_host'] = max(hosts.values()) if hosts else 0
    summ['routes'] = {}
    for r in log.values():
        summ['routes'][r['route']] = summ['routes'].get(r['route'], 0) + 1
    xip = set()
    for n, r in log.items():
        resp = _load_resp(d, n)
        for k, v in resp['headers']:
            if k.lower() == 'x-ip':
                xip.add(v)
    summ['egress_ip_echoed'] = sorted(xip)
    with open(d / 'summary.json', 'w') as f:
        json.dump(summ, f, indent=1)
    print(json.dumps(summ, indent=1))


def do_wayback(label):
    """For each service walled at read LABEL: the Wayback Machine's CDX list of captures of the
    probe URL since 2024-01-01, then archived captures read (raw, id_) by bisection to bracket when
    the wall first appears. A fixed check set (every tenth open service by id) gets a CDX listing
    only, as a check of the archive's coverage. At most WAYBACK_MAX requests; stops for the read
    at the first 429 or after two network failures in a row."""
    check_window()
    src = ROOT / 'data' / ('read-' + label)
    out = ROOT / 'data' / ('wayback-' + label)
    if out.exists():
        sys.exit('wayback %s already held' % label)
    classes = list(csv.DictReader(open(src / 'classes.csv')))
    panel = {s['id']: s for s in load_panel()}
    walled = [r for r in classes if r['wall'] == 'yes' and r['class'] != 'wall_at_robots']
    opened = [r for r in classes if r['class'] == 'open']
    check = opened[::10]
    rec = Recorder(out)
    state = {'used': 0, 'fails': 0, 'stopped': ''}
    results = []

    def get(sid, kind, url):
        if state['stopped'] or state['used'] >= WAYBACK_MAX:
            return None
        r = rec.get(sid, kind, url, UA_PLAIN, '*/*')
        state['used'] += 1
        time.sleep(WAYBACK_PAUSE - PAUSE)
        if r['status'] == 429:
            state['stopped'] = '429 at request %d' % r['n']
        elif r['error']:
            state['fails'] += 1
            if state['fails'] >= 2:
                state['stopped'] = 'two network failures in a row (%s)' % r['error']
        else:
            state['fails'] = 0
        return r

    rb = get('-', 'robots', 'https://web.archive.org/robots.txt')
    groups = None
    if rb and not rb['error'] and rb['status'] and 200 <= rb['status'] < 300:
        groups = parse_robots(rb['body'].decode('utf-8', 'replace'))
    elif rb and rb['status'] and 400 <= rb['status'] < 500 and rb['status'] != 429:
        groups = []
    if groups is None:
        state['stopped'] = state['stopped'] or 'robots.txt of web.archive.org unread'

    def cdx(sid, url):
        q = ('https://web.archive.org/cdx/search/cdx?url=%s&output=json&from=20240101'
             '&fl=timestamp,statuscode,digest,length&collapse=digest&limit=500' % quote(url, safe=''))
        if groups is not None and not robots_allowed(groups, ROBOTS_TOKEN, q):
            return None, 'robots_disallowed'
        r = get(sid, 'cdx', q)
        if r is None:
            return None, 'not read: ' + (state['stopped'] or 'cap')
        if r['error'] or r['status'] != 200:
            return None, 'cdx %s' % (r['error'] or r['status'])
        try:
            rows = json.loads(r['body'].decode('utf-8', 'replace') or '[]')
        except ValueError:
            return None, 'cdx unparsable (truncated?)'
        return [x for x in rows[1:]], ''

    def capture_class(sid, s, ts, st):
        u = 'https://web.archive.org/web/%sid_/%s' % (ts, s['url'])
        if groups is not None and not robots_allowed(groups, ROBOTS_TOKEN, u):
            return None
        r = get(sid, 'capture', u)
        if r is None or r['error']:
            return None
        hdrs = [(k[len('x-archive-orig-'):], v) for k, v in r['headers'] if k.lower().startswith('x-archive-orig-')]
        stc = int(st) if str(st).isdigit() else (r['status'] or 0)
        cls, _ = classify(stc, None, hdrs, r['body'], s['surface'], s['marker'], s['url'])
        return cls

    for r in walled:
        s = panel[r['id']]
        caps, why = cdx(r['id'], s['url'])
        res = {'id': r['id'], 'kind': 'walled', 'class_now': r['class'], 'captures': '', 'last_open': '',
               'first_wall': '', 'note': why}
        if caps is not None:
            res['captures'] = len(caps)
            if caps:
                lo, hi = 0, len(caps) - 1
                c_hi = capture_class(r['id'], s, caps[hi][0], caps[hi][1])
                c_lo = capture_class(r['id'], s, caps[lo][0], caps[lo][1])
                fetched = 2
                if c_lo is None or c_hi is None:
                    res['note'] = 'captures unread'
                elif c_lo in WALL_CLASSES:
                    res['first_wall'] = caps[lo][0]
                    res['note'] = 'walled at the earliest capture read since 2024-01-01'
                elif c_hi not in WALL_CLASSES:
                    res['last_open'] = caps[hi][0]
                    res['note'] = 'latest capture not walled (%s)' % c_hi
                else:
                    while hi - lo > 1 and fetched < WAYBACK_PER_SERVICE:
                        mid = (lo + hi) // 2
                        c = capture_class(r['id'], s, caps[mid][0], caps[mid][1])
                        fetched += 1
                        if c is None:
                            break
                        if c in WALL_CLASSES:
                            hi = mid
                        else:
                            lo = mid
                    res['last_open'], res['first_wall'] = caps[lo][0], caps[hi][0]
                    res['note'] = 'bracket' if hi - lo == 1 else 'bracket, not narrowed to adjacent captures'
        results.append(res)
    for r in check:
        s = panel[r['id']]
        caps, why = cdx(r['id'], s['url'])
        results.append({'id': r['id'], 'kind': 'coverage-check', 'class_now': r['class'],
                        'captures': '' if caps is None else len(caps), 'last_open': '', 'first_wall': '',
                        'note': why})
    rec.close()
    with open(out / 'dating.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['id', 'kind', 'class_now', 'captures', 'last_open', 'first_wall', 'note'])
        w.writeheader()
        w.writerows(results)
    with open(out / 'summary.json', 'w') as f:
        json.dump({'label': label, 'requests': state['used'], 'stopped': state['stopped'],
                   'walled': len(walled), 'checks': len(check)}, f, indent=1)
    print(json.dumps({'requests': state['used'], 'stopped': state['stopped'], 'walled': len(walled)}))


def do_httparchive(label):
    check_window()
    out = ROOT / 'data' / ('httparchive-' + label)
    if out.exists():
        sys.exit('httparchive %s already held' % label)
    rec = Recorder(out)
    rb, _, cut = fetch_robots(rec, '-', 'https://cdn.httparchive.org/robots.txt')
    state, groups, pcls, _ = robots_outcome(rb) if rb and not cut else ('unreachable', None, 'host_cap', '')
    url = ('https://cdn.httparchive.org/v1/adoption?technology=%s&geo=ALL&rank=ALL&start=2024-01-01'
           % quote(','.join(HA_TECH), safe=','))
    if state in ('parsed', 'unavailable') and robots_allowed(groups, ROBOTS_TOKEN, url):
        rec.get('-', 'context', url, UA_PLAIN, 'application/json', cap=8 * 1024 * 1024)
    else:
        print('HTTP Archive not read: robots', state, pcls)
    rec.close()


def do_statements(label, listfile):
    check_window()
    out = ROOT / 'data' / ('statements-' + label)
    if out.exists():
        sys.exit('statements %s already held' % label)
    rec = Recorder(out)
    robots = {}
    for row in csv.DictReader(open(listfile)):
        u = urlsplit(row['url'])
        key = (u.scheme, u.netloc)
        if key not in robots:
            rb, _, cut = fetch_robots(rec, row['id'], '%s://%s/robots.txt' % key)
            robots[key] = robots_outcome(rb) if rb and not cut else ('unreachable', None, 'host_cap', '')
        state, groups, pcls, _ = robots[key]
        if state not in ('parsed', 'unavailable') or not robots_allowed(groups, ROBOTS_TOKEN, row['url']):
            print('not read (robots %s %s): %s' % (state, pcls, row['url']))
            continue
        rec.get(row['id'], 'statement', row['url'], UA_PLAIN, ACCEPT['page'], cap=2 * 1024 * 1024)
    rec.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read')
    ap.add_argument('--classify')
    ap.add_argument('--wayback')
    ap.add_argument('--httparchive')
    ap.add_argument('--statements', nargs=2, metavar=('LABEL', 'FILE'))
    a = ap.parse_args()
    if a.read:
        do_read(a.read)
    elif a.classify:
        do_classify(a.classify)
    elif a.wayback:
        do_wayback(a.wayback)
    elif a.httparchive:
        do_httparchive(a.httparchive)
    elif a.statements:
        do_statements(*a.statements)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
