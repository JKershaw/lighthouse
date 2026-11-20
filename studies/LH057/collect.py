#!/usr/bin/env python3
"""LH057 outcome read, as fixed in studies/LH057/brief.md (protocol 0.1).

Run only under a schedule row (LH057-2026-11-21 to LH057-2026-12-03), once per UTC day, after the brief is committed.
A label already held is skipped, never overwritten.

One GET of https://php.events.greynoise.io/ per read, asked of scripts/robots_gate.py first through scripts/lh_fetch.py
(the keeper's rule of 8 November 2026; run with LIGHTHOUSE_PROVIDER=anthropic under Claude Code), redirects gated too.
Body read up to 4 MiB. One retry only on a timeout, a connection error or HTTP 500, 502 or 504; never after a refusal,
challenge, rate limit, 503 or NotFetched. Both attempts are logged.

No body is kept (brief, "What may be kept"): the bytes received are hashed, parsed in memory, and only derived counts
and dates are written to data/read-<label>/derived.json.gz, after scripts/redact_emails.py redact_bytes and after
address-like strings are stripped; the writer refuses to save if any address-like string remains. Nothing from the
page's command, process, session, user-agent, fingerprint or indicator columns is extracted; addresses are used only
to count distinct values in memory. No link in the page is followed. One line per attempt goes to fetchlog.csv.

Usage:
  LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH057/collect.py --read 2026-11-21T1400Z
  python3 -I studies/LH057/collect.py --selftest      (parses a small synthetic page; sends nothing)
"""
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
import argparse
import csv
import gzip
import json
import re
import socket
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))

URL = 'https://php.events.greynoise.io/'
CEILING = 4 * 1024 * 1024
RETRY_STATUSES = (500, 502, 504)
TRACKER_CVES = ['CVE-2026-109618', 'CVE-2026-109619']
FIELDS = ['utc_time', 'url', 'purpose', 'robots_url', 'robots_status', 'gate', 'status', 'bytes', 'sha256',
          'body_kept', 'note']

IPV4 = re.compile(r'(?<![0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![0-9.])')
IPV6 = re.compile(r'(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{1,4}:){2,7}[0-9A-Fa-f]{0,4}(?![0-9A-Fa-f:])'
                  r'|(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{0,4}:){1,7}:[0-9A-Fa-f]{0,4}(?![0-9A-Fa-f:])')
NUM = r'(\d[\d,]*)'


def strip_addresses(s):
    s = IPV4.sub('[address withheld]', s)
    # IPv6-like strings, but leave clock times such as 13:30 or 13:30:05 alone
    return IPV6.sub(lambda m: m.group(0) if re.fullmatch(r'\d{1,2}:\d{2}(:\d{2})?', m.group(0)) else
                    '[address withheld]', s)


def n(s):
    return int(s.replace(',', '')) if s is not None else None


class Page(HTMLParser):
    """Collects only what the brief's measures need. Cells of unwanted columns are never stored."""

    WANT = {  # table id -> {header text: key}
        't_success_det': {'Shell started (UTC)': 'start', 'Attacker IP': 'addr'},
        't_all': {'entry': 'entry'},
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.updated = None
        self.blocks = {}          # class -> text, for report-summary, report-stats, stat-outcome, stat-note
        self.open_blocks = []     # [class, tag, depth of that tag when opened]
        self.depth = {}
        self.timeline = []
        self.in_tl = None
        self.in_tl_label = False
        self.summaries = []       # details/summary headings
        self.in_summary = None
        self.tables = {}          # id -> {'rows': int, 'closed': bool, 'headers': [], 'cols': {key: [values]}}
        self.table = None
        self.in_th = None
        self.cell = None
        self.col = -1
        self.in_updated = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get('class') or '').split()
        self.depth[tag] = self.depth.get(tag, 0) + 1
        for b in self.open_blocks:
            self.blocks[b[0]] += ' '
        if 'report-updated' in cls:
            self.in_updated = True
        if tag == 'time' and self.in_updated and self.updated is None:
            self.updated = a.get('datetime')
        for c in ('report-summary', 'report-stats', 'stat-outcome', 'stat-note'):
            if c in cls:
                self.open_blocks.append([c, tag, self.depth[tag]])
                self.blocks.setdefault(c, '')
        if tag == 'li' and 'tl-ev' in cls:
            self.in_tl = {'label': '', 'datetime': None}
            self.timeline.append(self.in_tl)
        if self.in_tl is not None and tag == 'time' and self.in_tl['datetime'] is None:
            self.in_tl['datetime'] = a.get('datetime')
        if self.in_tl is not None and 'tl-label' in cls:
            self.in_tl_label = True
        if tag == 'summary':
            self.in_summary = ''
        if tag == 'table':
            tid = a.get('id') or 'table%d' % len(self.tables)
            self.table = tid
            self.tables[tid] = {'rows': 0, 'closed': False, 'headers': [], 'cols': {}}
        if self.table:
            t = self.tables[self.table]
            if tag == 'tr':
                self.col = -1
            if tag == 'th':
                self.in_th = ''
            if tag == 'td':
                self.col += 1
                if self.col == 0:
                    t['rows'] += 1
                hdr = t['headers'][self.col] if self.col < len(t['headers']) else None
                key = self.WANT.get(self.table, {}).get(hdr)
                self.cell = (key, '') if key else None

    def handle_endtag(self, tag):
        for b in self.open_blocks:
            self.blocks[b[0]] += ' '
        self.open_blocks = [b for b in self.open_blocks if not (b[1] == tag and b[2] == self.depth.get(tag, 0))]
        if self.depth.get(tag):
            self.depth[tag] -= 1
        if tag == 'div' and self.in_updated and self.updated is not None:
            self.in_updated = False
        if self.in_tl_label and tag in ('span', 'b', 'div', 'strong', 'p'):
            self.in_tl_label = False
        if tag == 'li' and self.in_tl is not None:
            self.in_tl = None
            self.in_tl_label = False
        if tag == 'summary' and self.in_summary is not None:
            self.summaries.append(' '.join(self.in_summary.split()))
            self.in_summary = None
        if self.table:
            t = self.tables[self.table]
            if tag == 'th' and self.in_th is not None:
                t['headers'].append(' '.join(self.in_th.split()))
                self.in_th = None
            if tag == 'td' and self.cell is not None:
                key, val = self.cell
                t['cols'].setdefault(key, []).append(' '.join(val.split()))
                self.cell = None
            if tag == 'table':
                t['closed'] = True
                self.table = None

    def handle_data(self, d):
        for b in self.open_blocks:
            self.blocks[b[0]] += d
        if self.in_tl_label and self.in_tl is not None:
            self.in_tl['label'] += d
        if self.in_summary is not None:
            self.in_summary += d
        if self.in_th is not None:
            self.in_th += d
        if self.cell is not None:
            self.cell = (self.cell[0], self.cell[1] + d)


def by_day(values):
    days = {}
    unparsed = 0
    for v in values:
        m = re.match(r'(\d{4}-\d{2}-\d{2})', v or '')
        if m:
            days[m.group(1)] = days.get(m.group(1), 0) + 1
        else:
            unparsed += 1
    return dict(sorted(days.items())), unparsed


def derive(body, truncated):
    text = body.decode('utf-8', 'replace')
    p = Page()
    p.feed(text)
    out = {'truncated_at_ceiling': truncated, 'last_updated': p.updated}
    summ = ' '.join(p.blocks.get('report-summary', '').split())
    stats = ' '.join(p.blocks.get('report-stats', '').split())
    note = ' '.join(p.blocks.get('stat-note', '').split())
    out['summary_cves'] = sorted(set(re.findall(r'CVE-\d{4}-\d+', summ)))
    out['summary_names_tracker_cves'] = out['summary_cves'] == TRACKER_CVES if summ else None

    def grab(pat, s):
        m = re.search(pat, s)
        return m.groups() if m else None

    g = grab(r'observed ' + NUM + r' new attacker IPs? in the last ' + NUM + r' hours and a total of ' + NUM +
             r' as of ([^.]+?)\.', summ)
    out['new_addresses'], out['new_addresses_hours'], out['addresses_total'], out['addresses_as_of'] = (
        (n(g[0]), n(g[1]), n(g[2]), g[3]) if g else (None, None, None, None))
    g = grab(r'confirmed ' + NUM + r' successful exploitations?, from ' + NUM + r' attacker IPs?', summ)
    out['successes_summary'], out['success_addresses_summary'] = (n(g[0]), n(g[1])) if g else (None, None)
    for key, label in (('sessions', 'Sessions observed'), ('attempts', 'Exploitation attempts'),
                       ('reconnaissance', 'Reconnaissance')):
        g = grab(re.escape(label) + r'\s*' + NUM, stats)
        out[key] = n(g[0]) if g else None
    g = grab(NUM + r'\s*confirmed successful exploitations? from ' + NUM + r' attacker IPs?', stats)
    out['successes_stats'], out['success_addresses_stats'] = (n(g[0]), n(g[1])) if g else (None, None)
    g = grab(r'sensors since ([^;]+?) UTC', note)
    out['sensors_since'] = g[0] if g else None
    out['timeline'] = [{'label': strip_addresses(' '.join(e['label'].split()))[:120], 'datetime': e['datetime']}
                       for e in p.timeline]
    out['sections'] = []
    for s in p.summaries:
        m = re.match(r'(.*?)\s*\((\d[\d,]*)(.*)\)\s*$', s)
        out['sections'].append({'heading': strip_addresses(m.group(1) if m else s)[:120],
                                'count': n(m.group(2)) if m else None,
                                'rest': strip_addresses(m.group(3))[:80] if m else None})
    out['tables'] = {tid: {'rows_with_cells': t['rows'], 'complete': t['closed']} for tid, t in p.tables.items()}
    sd = p.tables.get('t_success_det')
    if sd and 'start' in sd['cols']:
        out['successes_by_day'], out['successes_unparsed'] = by_day(sd['cols']['start'])
        out['success_table_complete'] = sd['closed']
        out['success_distinct_addresses'] = len(set(sd['cols'].get('addr', []))) if 'addr' in sd['cols'] else None
    else:
        out['successes_by_day'] = out['successes_unparsed'] = out['success_table_complete'] = None
        out['success_distinct_addresses'] = None
    ta = p.tables.get('t_all')
    if ta and 'entry' in ta['cols']:
        out['entries_by_day'], out['entries_unparsed'] = by_day(ta['cols']['entry'])
        out['entry_table_complete'] = ta['closed']
    else:
        out['entries_by_day'] = out['entries_unparsed'] = out['entry_table_complete'] = None
    out['chart_section_reached'] = 'c_activity' in text
    out['mentions_8_5_13_or_8_4_28'] = ('8.5.13' in text) or ('8.4.28' in text)
    return out


def safe_dump(obj):
    from redact_emails import redact_bytes
    raw = json.dumps(obj, indent=1, sort_keys=True).encode()
    raw, _ = redact_bytes(raw)
    s = strip_addresses(raw.decode())
    if IPV4.search(s):
        raise SystemExit('refusing to save: an address-like string remains in the derived data')
    return s.encode()


def log(row):
    path = ROOT / 'fetchlog.csv'
    new = not path.exists()
    with open(path, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def fetch_once(label, attempt):
    from lh_fetch import urlopen, UA, NotFetched, check
    t = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    ok, info = check(URL)
    base = {'utc_time': t, 'url': URL, 'purpose': 'outcome read %s, attempt %d' % (label, attempt),
            'robots_url': info.get('robots_url'), 'robots_status': info.get('robots_status'),
            'gate': '%s (%s)' % ('allowed' if ok else 'refused', info.get('reason')), 'body_kept': 'no'}
    req = urllib.request.Request(URL, headers={'User-Agent': UA})
    try:
        try:
            r = urlopen(req, timeout=90, check_redirects=True)
        except HTTPError as e:
            r = e
        with r:
            body = r.read(CEILING + 1)
            status, final = r.status, r.geturl()
    except NotFetched as e:
        log(dict(base, status='NotFetched', bytes='', sha256='', note=str(e)[:300]))
        return None, False
    except (URLError, socket.timeout, TimeoutError, ConnectionError) as e:
        log(dict(base, status='error', bytes='', sha256='', note=type(e).__name__))
        return None, True
    digest = sha256(body).hexdigest()
    truncated = len(body) > CEILING
    body = body[:CEILING]
    note = ('final URL %s; ' % strip_addresses(final) if final != URL else '') + \
           ('cut at the 4 MiB ceiling' if truncated else '')
    log(dict(base, status=status, bytes=len(body), sha256=digest, note=note))
    if status != 200:
        return None, status in RETRY_STATUSES
    return (body, truncated, digest, t), False


def read(label):
    outdir = ROOT / 'data' / ('read-' + label)
    if outdir.exists():
        print('label already held; not overwritten:', outdir)
        return
    got, retry = fetch_once(label, 1)
    if got is None and retry:
        got, _ = fetch_once(label, 2)
    if got is None:
        print('read unavailable; logged in fetchlog.csv (a missed read, never a zero)')
        return
    body, truncated, digest, t = got
    d = derive(body, truncated)
    del body
    d.update({'label': label, 'read_utc': t, 'sha256_received': digest, 'url': URL, 'protocol': '0.1'})
    outdir.mkdir(parents=True)
    with gzip.open(outdir / 'derived.json.gz', 'wb') as f:
        f.write(safe_dump(d))
    print('derived data written to', outdir / 'derived.json.gz')


SYNTHETIC = b"""<html><body><div class=report-updated>Last updated<time datetime=2000-01-02T03:04:00Z>x</time></div>
<p class=report-summary>GreyNoise is monitoring exploitation attempts against PHP vulnerabilities CVE-2026-109618 and
CVE-2026-109619. We have observed 1 new attacker IPs in the last 24 hours and a total of 3 as of 2 January 2000.
We have confirmed 2 successful exploitations, from 1 attacker IPs, against our vulnerable sensors.</p>
<aside class=report-stats>Sessions observed<span class=stat-big>10</span><ul><li>Exploitation attempts<b>7</b></li>
<li>Reconnaissance<b>3</b></li></ul><p class=stat-outcome><b>2</b>confirmed successful exploitations from 1 attacker IPs</p>
<p class=stat-note>GreyNoise sensors since 1 Jan 2000 UTC; benign sources excluded.</p></aside>
<ol class=tl><li class="tl-ev tl-attack"><span class=tl-gap>1d later</span><time datetime=2000-01-01T00:00:00Z>t</time>
<span class=tl-label>First successful exploitation observed</span><span class=tl-detail>NOT KEPT</span></li></ol>
<details><summary>Successful Exploitation (2)</summary><table id=t_success_det><thead><tr><th>Shell started (UTC)</th>
<th>Attacker IP</th><th>Commands run (in order)</th></tr></thead><tbody>
<tr><td>2000-01-01 10:00</td><td>192.0.2.1</td><td>NOT KEPT</td></tr>
<tr><td>2000-01-02 11:00</td><td>192.0.2.1</td><td>NOT KEPT</td></tr></tbody></table></details>
<details><summary>Observed Infrastructure (3)</summary><table id=t_all><tr><th>ip</th><th>entry</th></tr>
<tr><td>192.0.2.1</td><td>2000-01-01 09:00</td></tr><tr><td>2001:db8::1</td><td>2000-01-01 09:30</td></tr>
<tr><td>198.51.100.7</td><td>2000-01-02 08:00</td></tr></table></details><div id=c_activity></div></body></html>"""


def selftest():
    d = derive(SYNTHETIC, False)
    s = safe_dump(d).decode()
    assert 'NOT KEPT' not in s and '192.0.2.1' not in s and '2001:db8' not in s, 'unwanted content kept'
    assert d['successes_by_day'] == {'2000-01-01': 1, '2000-01-02': 1}, d['successes_by_day']
    assert d['entries_by_day'] == {'2000-01-01': 2, '2000-01-02': 1}, d['entries_by_day']
    assert d['success_distinct_addresses'] == 1
    assert (d['attempts'], d['reconnaissance'], d['sessions']) == (7, 3, 10), (d['attempts'], d['reconnaissance'])
    assert (d['successes_summary'], d['success_addresses_summary'], d['addresses_total']) == (2, 1, 3)
    assert (d['successes_stats'], d['success_addresses_stats']) == (2, 1)
    assert d['summary_names_tracker_cves'] is True and d['last_updated'] == '2000-01-02T03:04:00Z'
    assert d['timeline'][0]['label'] == 'First successful exploitation observed'
    assert d['sensors_since'] == '1 Jan 2000'
    print('selftest passed (synthetic page; nothing fetched)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--read')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.read:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{4}Z', a.read):
            raise SystemExit('label must look like 2026-11-21T1400Z')
        read(a.read)
    else:
        ap.print_help()
