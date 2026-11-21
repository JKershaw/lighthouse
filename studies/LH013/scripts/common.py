"""LH013: shared helpers. Every network read goes through here and is logged in data/read_log.csv
with its UTC read time, the endpoint, the query text, the HTTP status, the rows returned and, for
ClickPy, the rows and bytes read as ClickHouse's own X-ClickHouse-Summary header reports them.
No key, token or credential is read or sent: ClickHouse's public `demo` user and PyPI's JSON API are
the only endpoints, both anonymous. BigQuery is not read.

Adapted from studies/LH012/scripts/common.py. What changed: paths and the scratch directory are this
study's; the ceilings are LH013's brief's (300 ClickPy queries, 30 billion rows read, 300 PyPI JSON
requests); the phase gate has two settings, LH013_PHASE=dates (the default), which refuses any query
on the pypi database that can return a download count (only min, max or DISTINCT of project and date,
and the system database), and LH013_PHASE=counts, set only after the eligibility check, the days-held
listing, the W0 baseline check and the PyPI metadata read; every query of the pypi database carries
SETTINGS read_overflow_mode = 'throw' (amendment 1) and result_overflow_mode = 'throw', so a query cut
short by a limit fails rather than returning a partial answer; a body that carries a ClickHouse
exception is treated as failed even under HTTP 200.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH013/scripts/common.py`."""
import csv, io, json, os, re, subprocess, time, datetime
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
import hashlib, urllib.error, urllib.request  # noqa: E402
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body, write_derived, keep_decision  # noqa: E402  robots.txt gate (8 November 2026); one keep path (21 November)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = '/tmp/claude-0/-home-user-lighthouse/d3ec6ea6-80c0-5ef0-b532-d48fc65fef6b/scratchpad/LH013'
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo'
LOG_FIELDS = ['read_utc', 'source', 'stage', 'label', 'endpoint', 'query', 'http_status', 'rows_returned',
              'read_rows', 'read_bytes', 'elapsed_ns', 'output', 'note']
MAX_QUERIES, MAX_ROWS_READ, MAX_PYPI = 300, 30_000_000_000, 300
PHASE = os.environ.get('LH013_PHASE', 'dates')
os.makedirs(SCRATCH, exist_ok=True)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(entry):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS, lineterminator='\n')
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


def curl(url, data=None):
    """Return (status, body, headers). Until 21 November 2026 this ran the curl command; it now requests through
    scripts/lh_fetch.py's urlopen (the keeper's decision of that day, notes/keeper/2026-11-21-robots-intent.md:
    one gated fetch path for every collector). The robots.txt gate is asked first, as before, and urlopen asks
    the same cached gate, so robots.txt is read once. Return values are as before: the status as text ('000'
    where no response came, curl's code), the body as text, and the response's header block as text.
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
                                 headers={'User-Agent': UA})
    LAST.clear()
    LAST.update(final=url, headers=None)
    try:
        try:
            resp = urlopen(req, timeout=170, check_redirects=True)
        except urllib.error.HTTPError as e:
            resp = e
        with resp:
            raw = resp.read()
            LAST.update(final=resp.geturl() or url, headers=resp.headers)
            status = str(resp.status)
            head = 'HTTP/1.1 %s %s\r\n%s\r\n' % (resp.status, getattr(resp, 'reason', ''),
                                                 ''.join('%s: %s\r\n' % kv for kv in resp.headers.items()))
    except NotFetched as e:  # a redirect robots.txt refuses: not requested, logged as not fetched
        return 'not fetched: ' + str(e).replace('not fetched: ', '', 1), '', ''
    except Exception:  # no response (curl reported 000)
        return '000', '', ''
    return status, raw.decode('utf-8', 'replace'), head

def summary(headers):
    for line in headers.splitlines():
        if line.lower().startswith('x-clickhouse-summary:'):
            try:
                return json.loads(line.split(':', 1)[1])
            except ValueError:
                return {}
    return {}


def dates_allowed(sql):
    """True for a query that cannot return a download count: one on the system database without the pypi
    database in its FROM, or one whose select list is only project, date, DISTINCT, and min()/max() of a date."""
    s = ' '.join(sql.split())
    if re.search(r'\bFROM system\.', s, re.I) and not re.search(r'\bFROM pypi\.', s, re.I):
        return not re.search(r'\b(rows|bytes\w*|data_\w*)\b', s, re.I)
    m = re.match(r'SELECT (DISTINCT )?(.*?) FROM ', s, re.I)
    if not m:
        return False
    items = [x.strip() for x in re.split(r',(?![^()]*\))', m.group(2))]
    ok = all(re.fullmatch(r'(project|date|(min|max)\(date\))( AS \w+)?', x, re.I) for x in items)
    return ok and not re.search(r'\b(count|sum|uniq|avg|quantile)\w*\(', s, re.I)


def clickhouse(stage, label, sql, output=None, note=''):
    """Run one read-only query on ClickPy's public demo service and return its rows (a list of dicts).
    Raises SystemExit at a ceiling or a phase refusal; returns None when the query failed (HTTP error, an
    exception in the body, or a limit), after logging it, so the caller can split it."""
    if PHASE == 'dates' and not dates_allowed(sql):
        raise SystemExit(f'{label}: refused in the dates phase, since it could return a download count: {sql[:200]}')
    q, r, _ = spent()
    if q >= MAX_QUERIES or r >= MAX_ROWS_READ:
        raise SystemExit(f'ceiling reached: {q} queries, {r} rows read')
    sql = ' '.join(sql.split())
    if re.search(r'\bFROM pypi\.', sql):
        sql += " SETTINGS read_overflow_mode = 'throw', result_overflow_mode = 'throw'"
    sql += ' FORMAT CSVWithNames'
    t = now()
    status, body, headers = curl(CLICKHOUSE, sql)
    s = summary(headers)
    failed = status != '200' or 'DB::Exception' in body or '__exception__' in body or 'Code: ' in body[:200]
    rows = [] if failed else list(csv.DictReader(io.StringIO(body)))
    log(dict(read_utc=t, source='ClickPy (ClickHouse public demo)', stage=stage, label=label, endpoint=CLICKHOUSE,
             query=sql, http_status=status + (' (exception in body)' if failed and status == '200' else ''),
             rows_returned=len(rows), read_rows=s.get('read_rows', ''), read_bytes=s.get('read_bytes', ''),
             elapsed_ns=s.get('elapsed_ns', ''), output=output or '', note=(note + ' ' + (body[:300].replace('\n', ' ') if failed else '')).strip()))
    time.sleep(0.5)  # be gentle with a free public service
    if failed:
        print(f'   failed: {label}: HTTP {status}: {body[:300]}')
        return None
    if output:
        path = os.path.join(DATA, output)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _save_query(path, body, t, status, sql, rows)
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


def get_json(stage, label, url, output=''):
    if spent()[2] >= MAX_PYPI:
        raise SystemExit('PyPI request ceiling reached')
    t = now()
    status, body, _ = curl(url)
    log(dict(read_utc=t, source='PyPI JSON API', stage=stage, label=label, endpoint=url, http_status=status,
             read_bytes=len(body.encode()), output=output))
    time.sleep(0.2)
    if status != '200':
        return status, None, body
    return status, json.loads(body), body


def write_csv(path, rows, fields=None):
    fields = fields or list(rows[0].keys())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))
