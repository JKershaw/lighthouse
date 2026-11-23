"""LH047 re-audit of ISO week 2026-W47 (16 November 2026 00:00 UTC to 22 November 2026 24:00 UTC):
gather every request with a UTC time inside the week from the logs listed in logs.csv into one table,
requests.csv (brief, Amendment 2). Offline: reads git objects of the population commit, never the
working copy, so the table is the same whatever has been committed since.

Run from the repository root:
  python3 -I studies/LH047/data/reaudit-2026-W47/code/normalise.py <population-commit> [<later-commit>]

One row per request. Columns:
  log, practice, study, run, kind (page | robots), method, url, host, utc, utc_precision
  (second | minute-approx | not logged), status, sent (yes | no: refused by the gate | implicit
  robots read), provider, ua_class, ua, robots_logged_status, robots_logged_sha256, gate_reason,
  body_kept, note.

Robots.txt reads that a gated collector made without a logged row are added from the code, one per
host per run (brief section 3; Amendment 2): the collector file named in logs.csv is read at the
latest commit at or before the run's first logged request (or, where the file was first committed
after that, its first committed version, flagged), and the read is added only if that version goes
through scripts/lh_fetch.py's gated urlopen/check or scripts/robots_gate.py. Their time is not logged:
utc is set to the first request to that host in the run and utc_precision says "not logged (at or
before)".

With a later commit, the same logs are read there too and any week row present there but not at the
population commit is written to requests-later-only.csv (Amendment 2: logs committed after 22
November that record requests inside the week are included and named).
"""
import csv, gzip, io, json, os, re, subprocess, sys
from datetime import datetime, timezone
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
LO, HI = '2026-11-16T00:00:00', '2026-11-23T00:00:00'
GATED = re.compile(r'from lh_fetch import[^\n]*\b(urlopen|check)\b|robots_gate|RobotsGate|lh_fetch\.(urlopen|check)')
LH_TOKEN = 'Lighthouse-research'
# every robots.txt gate in the repository (scripts/robots_gate.py through lh_fetch, or a collector's RobotsGate(UA)) sends a
# User-Agent carrying Lighthouse's token; the CLI and lh_fetch send this one
GATE_UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, check=True).stdout


def show(commit, path):
    try:
        b = git('show', '%s:%s' % (commit, path))
    except subprocess.CalledProcessError:
        return None
    return gzip.decompress(b) if path.endswith('.gz') else b


def iso(s):
    """Normalise a logged time to YYYY-MM-DDTHH:MM:SSZ (UTC)."""
    s = s.strip()
    if not s:
        return ''
    s2 = s.replace('Z', '+00:00')
    try:
        d = datetime.fromisoformat(s2)
    except ValueError:
        m = re.match(r'(\d{4}-\d\d-\d\d)T(\d\d):?(\d\d):?(\d\d)?', s)
        if not m:
            return ''
        return '%sT%s:%s:%sZ' % (m.group(1), m.group(2), m.group(3), m.group(4) or '00')
    if d.tzinfo:
        d = d.astimezone(timezone.utc)
    return d.strftime('%Y-%m-%dT%H:%M:%SZ')


def in_week(u):
    return bool(u) and LO <= u[:19] < HI


def host_of(url):
    return (urlsplit(url).hostname or '').lower()


# ------------------------------------------------------------------ readers, one per log format

def r_read_log_json(b, log):
    for e in json.loads(b):
        rob = e.get('robots') if isinstance(e.get('robots'), dict) else {}
        err = str(e.get('error') or '')
        refused = e.get('status') in (None, '') and ('not fetched' in err.lower() or 'notfetched' in err.lower())
        yield dict(url=e.get('url', ''), utc=e.get('start_utc', ''), status='' if e.get('status') is None else str(e['status']),
                   method=e.get('method') or 'GET', sent='no: refused by the gate' if refused else 'yes',
                   robots_logged_status=str(rob.get('robots_status', '')), robots_logged_sha256=rob.get('robots_sha256', ''),
                   robots_url=rob.get('robots_url', ''), gate_reason=rob.get('reason', '') or (err[:160] if refused else ''),
                   provider=rob.get('provider', ''), access=rob.get('access', ''), final_url=e.get('final_url', ''),
                   body_kept=str(e.get('body_kept', '')), file=e.get('file', '') or '', note=err[:160] if not refused else '')


def r_readlog_csv(b, log):
    for r in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
        url = r.get('url', '')
        st = r.get('status', '') or ('error:' + r['error'] if r.get('error') else '')
        kind = r.get('kind', '')
        yield dict(url=url, utc=r.get('utc_start') or r.get('utc', ''), status=st, method='GET', sent='yes',
                   kind_hint=kind, ua_hint=r.get('ua', ''), truncated=r.get('truncated', ''), n=r.get('n', ''),
                   file=('%04d.b' % int(r['n'])) if r.get('n') else ((r.get('name', '') + '.body') if r.get('name') else ''),
                   body_kept=r.get('body_kept', ''), note=(r.get('note', '') or r.get('error_detail', ''))[:160],
                   gate_reason='read by scripts/robots_gate.py' if 'robots_gate' in r.get('note', '') else '')


def r_fetch_log_jsonl(b, log):
    for line in b.decode('utf-8', 'replace').splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        url = e.get('url') or e.get('requested_url', '')
        utc = e.get('observed_at') or e.get('started', '')
        st = e.get('status')
        outcome = str(e.get('outcome', '') or e.get('access_status', ''))
        refused = (e.get('robots_ok') is False) or ('robots' in outcome and st in (None, ''))
        yield dict(url=url, utc=utc, status='' if st is None else str(st), method='GET',
                   sent='no: refused by the gate' if refused and st in (None, '') else 'yes',
                   ua_hint=e.get('user_agent', ''), provider=e.get('provider', ''), robots_ref=e.get('robots_ref', ''),
                   final_url=e.get('final_url', ''), body_kept='yes' if (e.get('retained_body') or e.get('retained_path')) else '',
                   file=e.get('retained_path') or e.get('retained_body') or '',
                   note=('outcome=' + outcome)[:160])


def r_fetchlog_csv(b, log):
    for r in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
        rob = r.get('robots', '') or r.get('gate', '')
        m = re.search(r'robots sha256 ([0-9a-f]{64})', rob)
        refused = (r.get('status', '') in ('', 'not fetched') and 'disallow' in rob.lower()) or r.get('status', '') == 'NotFetched'
        yield dict(url=r['url'], utc=r.get('utc_start') or r.get('utc_time', ''), status=r.get('status', ''),
                   method=r.get('method') or 'GET', sent='no: refused by the gate' if refused else 'yes',
                   robots_logged_status=r.get('robots_status', ''), robots_logged_sha256=m.group(1) if m else '',
                   robots_url=r.get('robots_url', ''), gate_reason=rob[:200], body_kept=r.get('body_kept', ''), file=r.get('file', ''),
                   provider='anthropic' if 'provider anthropic' in rob else '', note=(r.get('note', '') or r.get('purpose', ''))[:160])


def r_lh051_tsv(b, log):
    for line in b.decode('utf-8', 'replace').splitlines():
        t = line.split('\t')
        if len(t) < 8:
            continue
        yield dict(url=t[3], utc=t[1], status=t[4], method='GET', sent='yes', gate_reason=t[7],
                   robots_logged_status='', note=(t[8] if len(t) > 8 else '')[:160])


def r_lh013_csv(b, log):
    for r in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
        yield dict(url=r['endpoint'], utc=r['read_utc'], status=r['http_status'], method='POST', sent='yes',
                   note=('%s %s' % (r['stage'], r['label']))[:160])


def r_lh056_probe(b, log):
    kv = {}
    for row in csv.reader(io.StringIO(b.decode('utf-8', 'replace'))):
        if len(row) >= 2:
            kv[row[0]] = row[1]
    # the endpoint is not written in the log; LH056's collector and this probe use ClickPy's public SQL endpoint
    yield dict(url='https://sql-clickhouse.clickhouse.com/', utc=kv.get('utc_start', ''), status=kv.get('status', ''),
               method='POST', sent='yes', note='endpoint not in the log; ClickPy public SQL (LH056 sources.md)')


def r_horizon_requests(b, log):
    for r in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
        tool, url = r['tool'], r['url_or_query']
        base = dict(utc=r['tool_call_utc'], status='', method='GET', note='scout %s; %s' % (r['scout'], tool),
                    scout=r['scout'], tool=tool)
        if tool == 'WebSearch':
            yield dict(base, url='', sent='search (not a request to a site)')
        elif tool == 'Bash(robots_gate)':
            u = urlsplit(url)
            yield dict(base, url='%s://%s/robots.txt' % (u.scheme, u.netloc), sent='yes', kind_hint='robots',
                       note=base['note'] + '; gate check of ' + url[:120])
        else:
            yield dict(base, url=url, sent='yes')


MS_ROW = re.compile(r'^\|\s*(https?://\S+)\s*\|[^|]*\|\s*(\d\d:\d\d(?::\d\d)?)\s*\|([^|]*)\|')


def r_ms_reading(b, log):
    day = re.search(r'(2026-11-\d\d)\.md$', log).group(1)
    text = b.decode('utf-8', 'replace')
    for line in text.splitlines():
        m = MS_ROW.match(line)
        if not m:
            continue
        url, hhmm, access = m.group(1), m.group(2), m.group(3)
        st = re.search(r'HTTP (\d{3})', access) or re.search(r'(?:;|^)\s*(\d{3})\b', access)
        yield dict(url=url, utc='%sT%s%sZ' % (day, hhmm, '' if hhmm.count(':') == 2 else ':00'), status=st.group(1) if st else '',
                   method='GET', sent='yes', gate_reason=access.strip()[:200], note='hand-parsed from the reading table')
    # URLs refused by the gate and not requested (the gate read their robots.txt)
    for line in text.splitlines():
        if re.search(r'[Rr]efused by robots\.txt|not requested', line) and not line.startswith('|'):
            for u in re.findall(r'https?://[^\s)\]`,]+', line):
                yield dict(url=u.rstrip('.'), utc='%sT14:00:00Z' % day, utc_precision='not logged (day only)', status='',
                           method='GET', sent='no: refused by the gate', note='refusal named in prose')


def r_handcoded(b, log):
    for r in csv.DictReader(io.StringIO(b.decode('utf-8', 'replace'))):
        yield dict(r)


READERS = dict(read_log_json=r_read_log_json, readlog_csv=r_readlog_csv, fetch_log_jsonl=r_fetch_log_jsonl,
               fetchlog_csv=r_fetchlog_csv, lh051_tsv=r_lh051_tsv, lh013_csv=r_lh013_csv, lh056_probe=r_lh056_probe,
               horizon_requests=r_horizon_requests, ms_reading=r_ms_reading)


# ------------------------------------------------------------------ code version of a collector

def code_at(path, when, commit):
    """(version commit, text, flag) of path at the latest commit <= when reachable from commit."""
    out = git('log', '--format=%H %cI', commit, '--', path).decode().split('\n')
    revs = [l.split() for l in out if l.strip()]
    if not revs:
        return '', '', 'collector file not found'
    before = [h for h, t in revs if iso(t) <= when]
    if before:
        h, flag = before[0], ''
    else:
        h, flag = revs[-1][0], 'first committed after the run (version committed with or after its data)'
    try:
        txt = git('show', '%s:%s' % (h, path)).decode('utf-8', 'replace')
    except subprocess.CalledProcessError:
        txt, flag = '', 'file absent at its last commit before the run'
    return h[:12], txt, flag


def ua_class(ua):
    """Amendment 1, R8."""
    if not ua:
        return 'unknown'
    if LH_TOKEN.lower() in ua.lower():
        return 'complies'
    if re.match(r'^(curl|Wget|Python-urllib|python-requests)/', ua):
        return 'complies (unlabelled)'
    if ua.startswith('Mozilla/5.0') and 'compatible;' not in ua:
        return 'does not comply (browser)'
    return 'does not comply (unattributed)'


def main():
    P = sys.argv[1]
    later = sys.argv[2] if len(sys.argv) > 2 else None
    logs = list(csv.DictReader(open(os.path.join(OUT, 'logs.csv'), newline='')))
    rows, later_rows, report = [], [], []
    for L in logs:
        if L['include'] != 'yes':
            continue
        path = L['path']
        b = (open(os.path.join(os.getcwd(), path), 'rb').read() if L['format'] == 'handcoded' else show(P, path))
        if b is None:
            report.append((path, 'absent at population commit'))
            continue
        reader = r_handcoded if L['format'] == 'handcoded' else READERS[L['format']]
        got = []
        for r in reader(b, path):
            r['utc'] = iso(r.get('utc', ''))
            if not in_week(r['utc']):
                continue
            # a collector that writes the gate's refusal as an error body (LH039): not sent
            if L['format'] == 'readlog_csv' and r.get('status') == 'error' and r.get('file'):
                eb = show(P, os.path.dirname(path) + '/' + r['file']) or b''
                if eb.startswith(b'not fetched'):
                    r['sent'] = 'no: refused by the gate'
                    r['gate_reason'] = eb[:200].decode('utf-8', 'replace')
            got.append(r)
        # code: is the collector gated, and what User-Agent does it send?
        first = min((r['utc'] for r in got), default='')
        ver, txt, flag = ('', '', '')
        if L['collector']:
            ver, txt, flag = code_at(L['collector'], first or HI, P)
        gated = bool(GATED.search(txt)) if txt else False
        oneoff = bool(re.search(r"access=['\"]oneoff['\"]", txt)) if txt else False
        ua_code = L['ua']
        if not ua_code and txt:
            if 'Lighthouse-research' in txt or re.search(r'from lh_fetch import[^\n]*\bUA\b', txt):
                ua_code = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)' \
                    if re.search(r'from lh_fetch import[^\n]*\bUA\b', txt) or 'compatible; Lighthouse-research' in txt \
                    else 'Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)'
        hosts_with_robots_row = set()
        for r in got:
            url = r.get('url', '')
            kind = 'robots' if (r.get('kind_hint', '').startswith('robots') or urlsplit(url).path == '/robots.txt') else 'page'
            if r.get('sent', 'yes').startswith('search'):
                kind = 'search'
            ua = r.get('ua_hint', '')
            if ua in ('plain', 'compat'):
                ua = {'plain': 'Lighthouse-research/1.0 (+https://lighthouse.harbour.cat/...)',
                      'compat': 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat/...)'}[ua]
            if ua == 'webfetch':
                ua = ''  # WebFetch: the User-Agent sent is not visible (R8 unknown)
            elif r.get('tool') == 'Bash(robots_gate)' or (kind == 'robots' and 'gate check' in r.get('note', '')):
                ua = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'  # scripts/robots_gate.py CLI
            else:
                ua = ua or ua_code
            if kind == 'robots' and r.get('sent', 'yes') == 'yes':
                hosts_with_robots_row.add(host_of(url))
            rows.append(dict(log=path, practice=r.get('practice') or L['practice'], study=r.get('study') or L['study'], run=L['run'], kind=kind,
                             method=r.get('method', 'GET'), url=url, host=host_of(url), utc=r['utc'],
                             utc_precision=r.get('utc_precision') or L.get('utc_precision') or 'second',
                             status=r.get('status', ''), sent=r.get('sent', 'yes'),
                             provider=r.get('provider') or L['provider'], ua_class=ua_class(ua) if kind != 'search' else '',
                             ua=ua, robots_logged_status=r.get('robots_logged_status', ''),
                             robots_logged_sha256=r.get('robots_logged_sha256', '') or (re.search(r'robots sha256 ([0-9a-f]{64})', r.get('gate_reason', '')) or [None, ''])[1], gate_reason=r.get('gate_reason', ''),
                             access=r.get('access', '') or ('oneoff (from code)' if oneoff and kind == 'page' else ''), final_url=r.get('final_url', ''), truncated=r.get('truncated', ''),
                             n=r.get('n', ''), body_kept=r.get('body_kept', ''), file=r.get('file', ''), robots_ref=r.get('robots_ref', ''),
                             note=r.get('note', ''), collector=L['collector'], collector_version=ver, collector_flag=flag,
                             gated_in_code='yes' if gated else ('n/a' if not L['collector'] else 'no')))
        # implicit gate robots reads: one per host per run (per log), where the collector is gated and the
        # log has no robots row of its own for that host. Prose logs mark implicit reads in logs.csv.
        implicit = L.get('implicit_robots', '')
        if (gated and implicit != 'no') or implicit == 'yes':
            firsts = {}
            for r in rows:
                if r['log'] != path or r['kind'] != 'page' or not r['url']:
                    continue
                if not (r['sent'] == 'yes' or r['sent'].startswith('no: refused')):
                    continue
                if r['practice'] != L['practice']:
                    continue
                h = r['host']
                if h in hosts_with_robots_row:
                    continue
                u = urlsplit(r['url'])
                key = '%s://%s' % (u.scheme, u.netloc)
                if key not in firsts or r['utc'] < firsts[key][0]:
                    firsts[key] = (r['utc'], r)
            for key, (t, r0) in sorted(firsts.items()):
                rows.append(dict(r0, kind='robots', method='GET', url=key + '/robots.txt', host=host_of(key), utc=t,
                                 ua=GATE_UA, ua_class=ua_class(GATE_UA),
                                 utc_precision='not logged (at or before)', status=r0['robots_logged_status'],
                                 sent='implicit robots read', gate_reason='', access='', final_url='', truncated='',
                                 n='', body_kept='', file='', robots_ref='',
                                 note='robots.txt read by the gate (counted from code: %s at %s)' % (
                                     L['collector'] or 'logs.csv', ver or 'n/a')))
        report.append((path, '%d week rows; collector %s at %s%s; gated=%s' % (
            len(got), L['collector'] or '-', ver or '-', (' [' + flag + ']') if flag else '', gated)))
        if later and L['format'] != 'handcoded':
            b2 = show(later, path)
            if b2 is not None and b2 != b:
                have = {(r.get('url', ''), iso(r.get('utc', ''))) for r in got}
                reader2 = READERS[L['format']]
                for r in reader2(b2, path):
                    u = iso(r.get('utc', ''))
                    if in_week(u) and (r.get('url', ''), u) not in have:
                        later_rows.append(dict(log=path, url=r.get('url', ''), utc=u, status=r.get('status', '')))
    # one robots_gate CLI call reads each host's robots.txt once: horizon gate rows of one scout for one host at
    # the same second are one read
    seen = set()
    for r in rows:
        if r['log'].startswith('notes/horizon/') and r['kind'] == 'robots' and r['sent'] == 'yes':
            k = (r['note'].split(';')[0], r['host'], r['utc'])
            if k in seen:
                r['sent'] = 'no: same gate call (robots.txt read once)'
            seen.add(k)
    # a signed URL's signature is withheld from what this audit keeps (AGENTS.md: no token in the repository)
    for r in rows:
        for k in ('url', 'final_url'):
            r[k] = re.sub(r'([?&](?:sig|signature|X-Amz-Signature|token)=)[^&]+', r'\1[withheld by Lighthouse]', r.get(k, ''))
    rows.sort(key=lambda r: (r['utc'], r['log'], r['url']))
    for i, r in enumerate(rows, 1):
        r['id'] = 'W%05d' % i
    fields = ['id', 'log', 'practice', 'study', 'run', 'kind', 'method', 'url', 'host', 'utc', 'utc_precision', 'status', 'sent',
              'provider', 'ua_class', 'ua', 'robots_logged_status', 'robots_logged_sha256', 'gate_reason', 'access', 'final_url',
              'truncated', 'n', 'body_kept', 'file', 'robots_ref', 'note', 'collector', 'collector_version', 'collector_flag', 'gated_in_code']
    with open(os.path.join(OUT, 'requests.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, 'requests-later-only.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['log', 'url', 'utc', 'status'])
        w.writeheader()
        w.writerows(later_rows)
    with open(os.path.join(OUT, 'normalise-report.txt'), 'w') as f:
        f.write('population commit %s; later commit %s\n' % (P, later or '-'))
        for p, s in report:
            f.write('%s\t%s\n' % (p, s))
    from collections import Counter
    print('rows', len(rows), Counter((r['kind'], r['sent']) for r in rows))
    print('later-only week rows', len(later_rows))


if __name__ == '__main__':
    main()
