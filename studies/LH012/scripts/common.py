"""LH012: shared helpers. Every network read goes through here and is logged in data/read_log.csv
with its UTC read time, the endpoint, the query text, the HTTP status, the rows returned and, for
ClickPy, the rows and bytes read as ClickHouse's own X-ClickHouse-Summary header reports them.
No key, token or credential is read or sent: ClickHouse's public `demo` user, PyPI's JSON API,
files.pythonhosted.org and a few documentation pages are the only endpoints used, all anonymously.

Adapted from studies/LH011/scripts/common.py. What changed: paths, the scratch directory and the
environment switch (LH012_ONLY) are this study's; the ceilings are this brief's (900 ClickPy queries,
40 billion rows read, 4,000 PyPI requests); a phase gate refuses, while LH012_PHASE is 1 (the
default), any ClickPy query that could return a download count: in phase 1 only queries on the
`system` database, or queries whose select list is limited to min(...) and max(...) of a date, run;
`get_text` logs a read of a documentation page; `get_json` counts PyPI requests against the ceiling
and records the byte length of every body; pypistats is not used.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH012/scripts/common.py`."""
import csv, io, json, os, re, subprocess, time, datetime
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
import hashlib, urllib.error, urllib.request  # noqa: E402
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body, write_derived, keep_decision  # noqa: E402  robots.txt gate (8 November 2026); one keep path (21 November)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = '/tmp/claude-0/-home-user-lighthouse/a4c176a2-2216-4535-ad2d-2da5b8411bad/scratchpad/LH012'
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo'
LOG_FIELDS = ['read_utc', 'source', 'label', 'endpoint', 'query', 'http_status', 'rows_returned',
              'read_rows', 'read_bytes', 'output']
MAX_QUERIES, MAX_ROWS_READ, MAX_PYPI = 900, 40_000_000_000, 4000
PHASE = os.environ.get('LH012_PHASE', '1')
os.makedirs(SCRATCH, exist_ok=True)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(entry):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: entry.get(k, '') for k in LOG_FIELDS})


def spent():
    """(ClickPy queries, ClickPy rows read, PyPI requests) so far, from the log."""
    if not os.path.exists(LOG):
        return 0, 0, 0
    q = r = p = 0
    for e in csv.DictReader(open(LOG)):
        if e['source'].startswith('ClickPy'):
            q += 1
            r += int(e['read_rows'] or 0)
        elif e['source'].startswith('PyPI'):
            p += 1
    return q, r, p


LAST = {}  # the latest response's final URL and headers, for save_body (21 November 2026)


def curl(url, data=None, binary_out=None, accept=None):
    """Return (status, body, headers). Until 21 November 2026 this ran the curl command; it now requests through
    scripts/lh_fetch.py's urlopen (the keeper's decision of that day, notes/keeper/2026-11-21-robots-intent.md:
    one gated fetch path for every collector). The robots.txt gate is asked first, as before, and urlopen asks
    the same cached gate, so robots.txt is read once. Return values are as before: the status as text ('000'
    where no response came, curl's code), the body as text (for binary_out, the bytes, which the caller saves), and the response's header block as text.
    Redirects are followed as curl -L did, each now checked against robots.txt first (check_redirects=True); a
    refused redirect returns "not fetched: ..."."""
    # The robots.txt gate first (the keeper, 8 November 2026): a URL it does not allow, or whose robots.txt
    # cannot be read, is not requested; the status returned, and so logged, is "not fetched: ..." with the
    # deciding group and rule, a missing reading and never a negative.
    ok, info = robots_check(url)
    if not ok:
        return ('not fetched: %s (robots %s, status %s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
                info.get('robots_status'), info.get('decided_by', ''), info.get('rule', ''))), '', ''
    req = urllib.request.Request(url, data=None if data is None else data.encode(),
                                 headers={'User-Agent': UA, **({'Accept': accept} if accept else {})})
    LAST.clear()
    LAST.update(final=url, headers=None)
    try:
        try:
            resp = urlopen(req, timeout=300, check_redirects=True)
        except urllib.error.HTTPError as e:
            resp = e
        with resp:
            raw = resp.read()
            LAST.update(final=resp.geturl() or url, headers=resp.headers)
            status = str(resp.status)
            head = 'HTTP/1.1 %s %s\r\n%s\r\n' % (resp.status, getattr(resp, 'reason', ''),
                                                 ''.join('%s: %s\r\n' % kv for kv in resp.headers.items()))
    except NotFetched as e:  # a redirect robots.txt refuses: not requested, logged as not fetched
        return 'not fetched: ' + str(e).replace('not fetched: ', '', 1), (b'' if binary_out else ''), ''
    except Exception:  # no response (curl reported 000)
        return '000', (b'' if binary_out else ''), ''
    return status, (raw if binary_out else raw.decode('utf-8', 'replace')), head

def summary(headers):
    for line in headers.splitlines():
        if line.lower().startswith('x-clickhouse-summary:'):
            return json.loads(line.split(':', 1)[1])
    return {}


def phase1_allowed(sql):
    """True for a query that cannot return a download count: one on the system database, or one whose
    select list is only min() and max() of a date column."""
    s = ' '.join(sql.split())
    if re.search(r'\bFROM system\.', s, re.I) and 'pypi.' not in s.replace("database = 'pypi'", '').replace("database='pypi'", ''):
        return True
    m = re.match(r'SELECT (.*?) FROM ', s, re.I)
    if not m:
        return not re.search(r'\bFROM\b', s, re.I)  # SELECT version(), getSetting(...) and the like
    items = [x.strip() for x in re.split(r',(?![^()]*\))', m.group(1))]
    ok = all(re.fullmatch(r'(project|(min|max)\((min_date|max_date|date)\))( AS \w+)?', x, re.I) for x in items)
    return ok and not re.search(r'\b(count|sum|uniq|avg|quantile)\w*\(', s, re.I)


def clickhouse(label, sql, output=None):
    """Run one read-only aggregate query on ClickPy's public demo service; write CSV to data/<output>
    (or return rows only when output is None). Setting LH012_ONLY=<label prefix> runs only matching labels."""
    if os.environ.get('LH012_ONLY') and not label.startswith(os.environ['LH012_ONLY']):
        return None
    if PHASE == '1' and not phase1_allowed(sql):
        raise SystemExit(f'{label}: refused in phase 1, since it could return a download count: {sql[:200]}')
    q, r, _ = spent()
    if q >= MAX_QUERIES or r >= MAX_ROWS_READ:
        raise SystemExit(f'ceiling reached: {q} queries, {r} rows read')
    sql = ' '.join(sql.split()) + ' FORMAT CSVWithNames'
    t = now()
    status, body, headers = curl(CLICKHOUSE, sql)
    s = summary(headers)
    rows = list(csv.DictReader(io.StringIO(body))) if status == '200' else []
    log(dict(read_utc=t, source='ClickPy (ClickHouse public demo)', label=label, endpoint=CLICKHOUSE,
             query=sql, http_status=status, rows_returned=len(rows), read_rows=s.get('read_rows', ''),
             read_bytes=s.get('read_bytes', ''), output=output or ''))
    if status != '200':
        raise SystemExit(f'{label}: HTTP {status}: {body[:400]}')
    if output:
        _save_query(os.path.join(DATA, output), body, t, status, sql, rows)
    time.sleep(0.5)  # be gentle with a free public service
    return rows


def _save_query(path, body, t, status, sql, rows):
    """Write a ClickPy query's CSV only through lh_fetch's save_body (21 November 2026); where it may not be
    kept, write path.derived.json (write_derived) with the read's metadata and the rows the study uses."""
    data = (body if body.endswith('\n') else body + '\n').encode()
    kept, why = save_body(path, data, LAST.get('final') or CLICKHOUSE, LAST.get('headers'))
    if not kept:
        write_derived(path + '.derived.json', LAST.get('final') or CLICKHOUSE, why, {'rows': rows}, read_utc=t,
                      http_status=status, query=sql, bytes=len(body.encode()),
                      sha256=hashlib.sha256(body.encode()).hexdigest())
        print('body_kept: no:', why, path)
    return kept


def get_json(source, label, url, output='', pause=0.2):
    if source.startswith('PyPI') and spent()[2] >= MAX_PYPI:
        raise SystemExit('PyPI request ceiling reached')
    t = now()
    status, body, _ = curl(url)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             rows_returned='', read_bytes=len(body), output=output))
    time.sleep(pause)
    if status != '200':
        return status, None
    return status, json.loads(body)


def get_text(source, label, url, path):
    """A documentation page, saved to scratch space (not retained) and logged."""
    t = now()
    status, body, _ = curl(url)
    body = redact_bytes(body.encode())[0].decode()
    kept, why = save_body(path, body.encode(), LAST.get('final') or url, LAST.get('headers'))  # 21 November 2026
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             read_bytes=len(body), output=path if kept else 'body_kept: no: ' + why))
    return status, body


def download(source, label, url, path):
    """A binary archive (a source distribution) into the scratchpad. From 21 November 2026 it is written only
    where lh_fetch's keep_decision allows; it is not passed through save_body, whose email redaction would
    corrupt an archive (curl -o wrote it unredacted before, too). Where it may not be kept, nothing is
    written, the log's output column says "body_kept: no: <reason>" and the status is returned as before."""
    t = now()
    status, raw, _ = curl(url, binary_out=path)
    out = path
    if raw:
        kept, why = keep_decision(LAST.get('final') or url, raw, LAST.get('headers'))
        if kept:
            with open(path, 'wb') as f:
                f.write(raw)
        else:
            out = 'body_kept: no: ' + why
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             read_bytes=os.path.getsize(path) if os.path.exists(path) else '', output=out))
    return status


def write_csv(name, rows, fields=None):
    """Writes under data/, or under $LH012_OUT when set (the replay's temporary directory)."""
    fields = fields or list(rows[0].keys())
    base = os.environ.get('LH012_OUT', DATA)
    os.makedirs(os.path.dirname(os.path.join(base, name)), exist_ok=True)
    with open(os.path.join(base, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))
