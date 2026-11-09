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
received. Where the robots.txt governing a host (or a response header) carries a Content-Signal
asking for use=reference or use=immediate, a 2xx body is not kept (amendment of 9 November 2026,
scripts/content_signal.py): <n>.b holds a placeholder, <n>.withheld.json the sha256 of the bytes
received, the signal as read and a bounded extract (and, after --classify, the class and echoes
derived from the body), and <n>.b.withheld-local the whole body for this run only, ignored by git.
Everything is kept under data/<kind>-<LABEL>/: readlog.csv (one row per request), each response's
headers (<n>.h) and first 64 KiB of body (<n>.b), and the derived tables. LABEL is a UTC time,
for example 2026-11-08T2000Z. A label already held is refused, never overwritten (except
--classify, which only rewrites derived tables).

A wall is the observation. The collector never answers a challenge, runs no JavaScript, keeps no
cookies, sends no credentials, submits no form, and does not retry a refused request.

Which robots.txt rules are obeyed (amendment 5, the keeper's decision of 8 November 2026, in force
for every request from read 1): scripts/robots_rules.py, with the provider from LIGHTHOUSE_PROVIDER
('anthropic' or 'openai'; unset or anything else means every listed provider's tokens). A group
naming Lighthouse-research or one of that provider's tokens (scripts/robots_tokens.json) applies,
else '*'; the strictest applicable group wins. Every request this module makes, in --read,
--wayback, --httparchive and --statements, is decided that way; the provider is recorded in
services.json and summary.json.
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
                      CLASSIFIER_VERSION, version_for, complete_lines, AMENDMENT5_FROM)
import robots_rules  # noqa: E402  (scripts/robots_rules.py: amendment 5, the keeper's rule)
import content_signal  # noqa: E402  (scripts/content_signal.py: amendment of 9 November 2026, use=reference)
import re  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
END = datetime(2027, 2, 9, 23, 59, 59, tzinfo=timezone.utc)
PAUSE = 1.5
# Amendment 3 (8 November 2026, post hoc, from read 1): robots.txt redirects are followed, up to
# ROBOTS_MAX_REDIRECTS hops, same-site or cross-site, each hop a logged request; probes still
# follow none. No host gets more than HOST_CAP requests in a read (1 robots.txt + 5 redirects +
# 1 probe for a single service), enforced across all services.
ROBOTS_MAX_REDIRECTS = 5
HOST_CAP = 7
# Amendment 4 (8 November 2026, post hoc, from read 1): robots.txt is read up to 512 KiB (RFC 9309
# section 2.5 asks for at least 500 KiB); a file still cut at that size is robots_unreachable for
# the read (no probe), and its cut-off last line is never applied, even to measure 4.
ROBOTS_CAP = 512 * 1024
# Headers and body patterns that echo the client's address back (amendment 4, measure of route).
ECHO_HEADERS = re.compile(r'(?i)^(x-ip|x-client-ip|x-ratelimit-ip|x-real-ip|x-forwarded-for|x-originating-ip|'
                          r'cf-connecting-ip|true-client-ip|x-remote-addr|x-remote-ip|remote-addr|x-your-ip|'
                          r'x-client-address|x-visitor-ip)$')
IPV4 = r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])'
ECHO_BODY = re.compile(r'(?i)(?:\bipr?\b|client[_ -]?ip|remote[_ -]?addr(?:ess)?|your ip(?: address)?(?: is)?|'
                       r'ip[_ -]?address)["\'=:\s>/]{1,6}(' + IPV4 + r')')
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


def provider_label(provider):
    return provider or 'all'


def obey(groups, url, provider):
    """Amendment 5: may Lighthouse request url under these robots_rules groups? Returns the
    robots_rules Decision (allowed, decided_by, rule, line, ...)."""
    return robots_rules.decide_groups(groups or [], url, provider)


def why_disallowed(d):
    return 'by %s: %s (line %s; provider %s)' % (d.decided_by, d.rule, d.line, d.provider)


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
    def __init__(self, outdir, provider=None):
        self.dir = outdir
        self.dir.mkdir(parents=True)
        self.n = 0
        self.host_counts = {}
        # Amendment of 9 November 2026 (use=reference): the robots.txt body and request number that
        # governed each host in this run, set by the caller, so get() can read its Content-Signal.
        self.provider = provider
        self.robots_for = {}
        self.v03 = True   # set False only when re-creating a pre-amendment-4 read
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
        sig = {'withhold': False}
        if not kind.startswith('robots') and r['status'] and 200 <= r['status'] < 300:
            rb, rn = self.robots_for.get(h, (None, ''))
            sig = content_signal.decide(rb, r['headers'], self.provider)
        if sig['withhold']:
            # Amendment of 9 November 2026: the site asks for use=reference, so the body is not kept in
            # the repository; hash, headers and a bounded extract are, and the whole body is held for
            # this run only in <n>.b.withheld-local (git-ignored), for do_classify and the coder.
            content_signal.write_withheld(self.dir / ('%04d.b' % self.n), r['body'], {
                'file': '%04d.b' % self.n, 'by': 'scripts/collect.py', 'sha256_received': r['sha256'],
                'url': url, 'service': service,
                'kind': kind, 'fetched_utc': r['utc'], 'http_status': r['status'],
                'headers': '%04d.h' % self.n,
                'content_signal': {'line': sig['signal'], 'where': sig['where'],
                                   'as_read': ('robots.txt kept as %04d.b' % rn) if sig['where'] == 'robots.txt'
                                   else 'response header'},
                'extract': {'title': content_signal.title_of(body)}})
        else:
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
                    'text/plain, */*;q=0.5', cap=ROBOTS_CAP if rec.v03 else 65536)
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


def robots_outcome(res, version=CLASSIFIER_VERSION):
    """What a robots.txt response allows. Returns (state, groups, class, detail)."""
    if res['error']:
        return 'unreachable', None, 'robots_unreachable', res['error']
    st = res['status']
    cls, det = classify(st, None, res['headers'], res['body'], 'file', '', res['url'], version=version)
    if cls == 'unread_proxy':
        # this container's own refusal, e.g. a redirect onto github.com: not the origin's answer
        return 'unreachable', None, 'robots_unreachable', det
    if cls in ('challenge', 'rate_limited'):
        return 'wall', None, 'wall_at_robots', cls + ':' + det
    if 200 <= st < 300:
        truncated = str(res.get('truncated', False)) == 'True'
        if version >= '0.3' and truncated:
            return 'truncated', None, 'robots_unreachable', 'robots.txt longer than %d bytes' % ROBOTS_CAP
        # amendment 5: groups for scripts/robots_rules.py, complete lines only
        return 'parsed', robots_rules.parse(robots_rules.complete_text(res['body'], truncated)), '', ''
    if 300 <= st < 400:
        return 'redirect', None, 'robots_redirect', header(res, 'location')[:120]
    if 400 <= st < 500:
        return 'unavailable', [], '', ''   # RFC 9309: unavailable, crawling allowed
    return 'unreachable', None, 'robots_unreachable', str(st)


def do_read(label, provider=None):
    check_window()
    out = ROOT / 'data' / ('read-' + label)
    if out.exists():
        sys.exit('read %s already held' % label)
    print('robots.txt obeyed for Lighthouse-research and provider: %s' % provider_label(provider))
    panel = load_panel()
    holds = previous_holds(label)
    version = version_for(label)
    rec = Recorder(out, provider)
    rec.v03 = version >= '0.3'
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
        state, groups, pcls, pdet = robots_outcome(rr, version)
        row['robots_n'], row['robots_state'] = rr['n'], state
        if state == 'parsed':
            rec.robots_for[(u.hostname or '').lower()] = (rr['body'], rr['n'])
        if pcls:
            row.update({'pre_class': pcls, 'pre_detail': pdet})
            services.append(row)
            continue
        d = obey(groups, s['url'], provider)
        if not d.allowed:
            row.update({'pre_class': 'robots_disallowed', 'pre_detail': why_disallowed(d)})
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
                   'robots_rules': 'amendment 5 (scripts/robots_rules.py)',
                   'provider': provider_label(provider), 'services': services}, f, indent=1)
    do_classify(label)


def _load_resp(d, n):
    """A kept response. Where the body was withheld for use=reference (a <n>.withheld.json beside
    it), 'withheld' carries that record and 'body' is the run's local copy if this checkout still has
    it, else the record's extract; 'withheld_local' says which."""
    if not n:
        return None
    lines = (d / ('%04d.h' % int(n))).read_text().splitlines()
    st = lines[0].split(' ', 1)[1] if lines else 'None'
    headers = [tuple(x.split(': ', 1)) if ': ' in x else (x, '') for x in lines[1:] if x]
    bpath = d / ('%04d.b' % int(n))
    body, w, local = bpath.read_bytes(), content_signal.load_record(bpath), False
    if w is not None:
        lp = Path(str(bpath) + content_signal.LOCAL_SUFFIX)
        local = lp.exists()
        body = lp.read_bytes() if local else '\n'.join(str(v) for v in w.get('extract', {}).values()).encode()
    return {'status': None if st == 'None' else int(st), 'headers': headers, 'body': body,
            'withheld': w, 'withheld_local': local}


def _save_derived(d, n, **fields):
    """Keep what do_classify derived from a withheld body's local copy in its record, so a later
    re-classification without the copy reproduces it."""
    p = content_signal.record_path(d / ('%04d.b' % int(n)))
    rec = json.loads(p.read_text())
    rec.setdefault('derived', {}).update(fields)
    p.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')


def _derived(resp, version=None):
    """The kept derivation of a withheld body with no local copy, or None."""
    w = resp.get('withheld')
    if not w or resp.get('withheld_local'):
        return None
    dv = w.get('derived') or {}
    return dv if version is None or dv.get('classifier') == version else None


def scan_echoes(headers, body):
    """Addresses a response echoes back: named headers, any header whose whole value is an IPv4
    address, and addresses that follow an address-like key in the kept body."""
    out = []
    for k, v in headers:
        if ECHO_HEADERS.match(k.strip()) or re.fullmatch(IPV4, v.strip() or 'x'):
            for a in re.findall(IPV4, v):
                out.append(('header', k.strip().lower(), a))
    text = body.decode('utf-8', 'replace') if isinstance(body, bytes) else body
    for m in ECHO_BODY.finditer(text):
        out.append(('body', m.group(0).split(m.group(1))[0].strip()[:30], m.group(1)))
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def do_classify(label):
    d = ROOT / 'data' / ('read-' + label)
    meta = json.load(open(d / 'services.json'))
    log = {r['n']: r for r in csv.DictReader(open(d / 'readlog.csv'))}
    version = version_for(label)
    rows, robots_rows = [], []
    for s in meta['services']:
        cls, det, status, ra = s['pre_class'], s['pre_detail'], '', ''
        if s['robots_n'] and not s['probe_n'] and cls not in ('robots_disallowed', 'not_probed_host_cap') \
                and s['robots_state'] != 'host_cap':
            # re-read the kept robots.txt response with the current classifier
            rl = log[str(s['robots_n'])]
            rresp = _load_resp(d, s['robots_n'])
            rresp.update({'error': rl['error'] or None, 'url': rl['url'], 'truncated': rl['truncated']})
            state, _, pcls, pdet = robots_outcome(rresp, version)
            if pcls:
                cls, det = pcls, pdet
            else:
                cls, det = 'unprobed', 'robots.txt now reads as %s; no probe was sent at the read' % state
        if s['probe_n']:
            lr = log[str(s['probe_n'])]
            resp = _load_resp(d, s['probe_n'])
            err = lr['error'] or None
            dv = _derived(resp, version)
            if dv:   # body withheld for use=reference: the class derived from it when it was here
                cls, det = dv['class'], dv['detail']
            else:
                cls, det = classify(resp['status'] or 0, err, resp['headers'], resp['body'],
                                    s['surface'], s['marker'], s['url'], version=version)
            if resp['withheld_local']:
                text = resp['body'].decode('utf-8', 'replace')
                _save_derived(d, s['probe_n'], classifier=version, **{'class': cls}, detail=det,
                              marker_found=bool(s['marker']) and s['marker'] in text,
                              marker_in_context=content_signal.excerpt(text, s['marker'], 80) if s['marker'] else '')
            status = lr['status']
            if cls in ('rate_limited',):
                u = retry_after_until({'headers': resp['headers'], 'utc': lr['utc']})
                ra = u.isoformat() if u else ''
        rows.append({'id': s['id'], 'stratum': s['stratum'], 'class_group': s['class'], 'host': s['host'],
                     'surface': s['surface'], 'prior': s['prior'], 'robots_state': s['robots_state'],
                     'status': status, 'class': cls, 'detail': det,
                     'wall': 'yes' if cls in WALL_CLASSES else 'no', 'retry_after_until': ra,
                     'classifier': version,
                     'route': log[str(s['probe_n'] or s['robots_n'])]['route'] if (s['probe_n'] or s['robots_n']) else ''})
        if s['robots_n'] and s['robots_state'] == 'parsed':
            root = '%s://%s/' % (urlsplit(s['url']).scheme, urlsplit(s['url']).netloc)
            rbody = _load_resp(d, s['robots_n'])['body']
            rcut = log[str(s['robots_n'])]['truncated'] == 'True'
            if label >= AMENDMENT5_FROM:
                # amendment 5: scripts/robots_rules.py for measure 4 too (complete lines; each token's
                # own group, else '*'), plus the decision the read obeyed and which group made it
                g = robots_rules.parse(robots_rules.complete_text(rbody, rcut))
                allowed = robots_rules.token_allowed
                dec = obey(g, s['url'], None if meta.get('provider', 'all') == 'all' else meta['provider'])
            else:
                rtext = rbody.decode('utf-8', 'replace')
                if version >= '0.3':
                    rtext = complete_lines(rtext, rcut)
                g = parse_robots(rtext)
                allowed = robots_allowed
                dec = None
            rr = {'id': s['id'], 'host': s['host'],
                  'lighthouse_probe_allowed': allowed(g, ROBOTS_TOKEN, s['url']),
                  'star_root_allowed': allowed(g, '*', root),
                  'star_probe_allowed': allowed(g, '*', s['url'])}
            for t in AI_TOKENS:
                rr[t] = allowed(g, t, root)
            if dec is not None:
                rr['obeyed_probe_allowed'] = dec.allowed
                rr['obeyed_decided_by'] = dec.decided_by or ''
                rr['obeyed_provider'] = dec.provider
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
    summ = {'label': label, 'classifier': version, 'requests': len(log),
            'bytes_retained': sum(int(r['bytes']) for r in log.values()), 'by_stratum': {}}
    for r in rows:
        summ['by_stratum'].setdefault(r['stratum'], {}).setdefault(r['class'], 0)
        summ['by_stratum'][r['stratum']][r['class']] += 1
    if 'provider' in meta:   # reads made under amendment 5 name the rule and the provider they obeyed
        summ['robots_rules'], summ['provider'] = meta['robots_rules'], meta['provider']
    hosts = {}
    for r in log.values():
        h = urlsplit(r['url']).hostname
        hosts[h] = hosts.get(h, 0) + 1
    summ['max_requests_to_one_host'] = max(hosts.values()) if hosts else 0
    summ['routes'] = {}
    for r in log.values():
        summ['routes'][r['route']] = summ['routes'].get(r['route'], 0) + 1
    # tallies within route (amendment 4): the strata were read partly over different routes
    summ['by_stratum_route'] = {}
    for r in rows:
        k = '%s|%s' % (r['stratum'], r['route'] or 'none')
        summ['by_stratum_route'].setdefault(k, {}).setdefault(r['class'], 0)
        summ['by_stratum_route'][k][r['class']] += 1
    # addresses echoed back by responses, per route (amendment 4)
    echoes = []
    for n, r in sorted(log.items(), key=lambda kv: int(kv[0])):
        resp = _load_resp(d, n)
        dv = _derived(resp)
        if dv is not None and 'echoes' in dv:
            found = [tuple(e) for e in dv['echoes']]
        else:
            found = scan_echoes(resp['headers'], resp['body'])
            if resp['withheld_local']:
                _save_derived(d, n, echoes=[list(e) for e in found])
        for where, name, addr in found:
            echoes.append({'n': n, 'service': r['service'], 'route': r['route'], 'where': where,
                           'name': name, 'address': addr})
    with open(d / 'echoes.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['n', 'service', 'route', 'where', 'name', 'address'])
        w.writeheader()
        w.writerows(echoes)
    summ['egress_ip_echoed'] = {}
    summ['echoed_blocks_16'] = {}
    for e in echoes:
        summ['egress_ip_echoed'].setdefault(e['route'], set()).add(e['address'])
    for rt, addrs in list(summ['egress_ip_echoed'].items()):
        summ['egress_ip_echoed'][rt] = sorted(addrs)
        summ['echoed_blocks_16'][rt] = sorted({'.'.join(a.split('.')[:2]) + '.0.0/16' for a in addrs})
    with open(d / 'summary.json', 'w') as f:
        json.dump(summ, f, indent=1)
    print(json.dumps(summ, indent=1))


def do_wayback(label, provider=None):
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
    rec = Recorder(out, provider)
    state = {'used': 0, 'fails': 0, 'stopped': ''}
    results = []

    def get(sid, kind, url, cap=65536):
        if state['stopped'] or state['used'] >= WAYBACK_MAX:
            return None
        r = rec.get(sid, kind, url, UA_PLAIN, '*/*', cap=cap)
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

    rb = get('-', 'robots', 'https://web.archive.org/robots.txt', cap=ROBOTS_CAP)
    groups = None
    if rb and not rb['error'] and rb['status'] and 200 <= rb['status'] < 300:
        groups = robots_rules.parse(robots_rules.complete_text(rb['body'], rb['truncated']))
        rec.robots_for['web.archive.org'] = (rb['body'], rb['n'])
    elif rb and rb['status'] and 400 <= rb['status'] < 500 and rb['status'] != 429:
        groups = []
    if groups is None:
        state['stopped'] = state['stopped'] or 'robots.txt of web.archive.org unread'

    def cdx(sid, url):
        q = ('https://web.archive.org/cdx/search/cdx?url=%s&output=json&from=20240101'
             '&fl=timestamp,statuscode,digest,length&collapse=digest&limit=500' % quote(url, safe=''))
        if groups is not None and not obey(groups, q, provider).allowed:
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
        if groups is not None and not obey(groups, u, provider).allowed:
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
        json.dump({'label': label, 'provider': provider_label(provider), 'requests': state['used'],
                   'stopped': state['stopped'],
                   'walled': len(walled), 'checks': len(check)}, f, indent=1)
    print(json.dumps({'requests': state['used'], 'stopped': state['stopped'], 'walled': len(walled)}))


def do_httparchive(label, provider=None):
    check_window()
    out = ROOT / 'data' / ('httparchive-' + label)
    if out.exists():
        sys.exit('httparchive %s already held' % label)
    rec = Recorder(out, provider)
    rb, _, cut = fetch_robots(rec, '-', 'https://cdn.httparchive.org/robots.txt')
    state, groups, pcls, _ = robots_outcome(rb) if rb and not cut else ('unreachable', None, 'host_cap', '')
    if state == 'parsed':
        rec.robots_for['cdn.httparchive.org'] = (rb['body'], rb['n'])
    url = ('https://cdn.httparchive.org/v1/adoption?technology=%s&geo=ALL&rank=ALL&start=2024-01-01'
           % quote(','.join(HA_TECH), safe=','))
    if state in ('parsed', 'unavailable') and obey(groups, url, provider).allowed:
        rec.get('-', 'context', url, UA_PLAIN, 'application/json', cap=8 * 1024 * 1024)
    else:
        print('HTTP Archive not read: robots', state, pcls)
    rec.close()


def do_statements(label, listfile, provider=None):
    check_window()
    out = ROOT / 'data' / ('statements-' + label)
    if out.exists():
        sys.exit('statements %s already held' % label)
    rec = Recorder(out, provider)
    robots = {}
    for row in csv.DictReader(open(listfile)):
        u = urlsplit(row['url'])
        key = (u.scheme, u.netloc)
        if key not in robots:
            rb, _, cut = fetch_robots(rec, row['id'], '%s://%s/robots.txt' % key)
            robots[key] = robots_outcome(rb) if rb and not cut else ('unreachable', None, 'host_cap', '')
            if robots[key][0] == 'parsed':
                rec.robots_for[(u.hostname or '').lower()] = (rb['body'], rb['n'])
        state, groups, pcls, _ = robots[key]
        if state not in ('parsed', 'unavailable') or not obey(groups, row['url'], provider).allowed:
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
    provider = robots_rules.provider_from_env()   # amendment 5: LIGHTHOUSE_PROVIDER, else all providers
    if a.read:
        do_read(a.read, provider)
    elif a.classify:
        do_classify(a.classify)
    elif a.wayback:
        do_wayback(a.wayback, provider)
    elif a.httparchive:
        do_httparchive(a.httparchive, provider)
    elif a.statements:
        do_statements(*a.statements, provider=provider)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
