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
and records the byte length of every body; pypistats is not used."""
import csv, io, json, os, re, subprocess, time, datetime

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


def curl(url, data=None, binary_out=None, accept=None):
    """Return (status, body, headers). curl is used because it reads the session's proxy settings."""
    hdr = os.path.join(SCRATCH, '.headers')
    cmd = ['curl', '-sS', '-L', '-D', hdr, '-w', '\n%{http_code}', url]
    if binary_out:
        cmd = ['curl', '-sS', '-L', '-D', hdr, '-o', binary_out, '-w', '%{http_code}', url]
    if accept:
        cmd[1:1] = ['-H', 'Accept: ' + accept]
    if data is not None:
        cmd += ['--data-binary', '@-']
    p = subprocess.run(cmd, input=(data or '').encode(), capture_output=True, timeout=300)
    out = p.stdout.decode('utf-8', 'replace')
    if binary_out:
        body, status = '', out.strip()
    else:
        body, _, status = out.rpartition('\n')
    headers = open(hdr).read() if os.path.exists(hdr) else ''
    return status.strip(), body, headers


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
        with open(os.path.join(DATA, output), 'w') as f:
            f.write(body if body.endswith('\n') else body + '\n')
    time.sleep(0.5)  # be gentle with a free public service
    return rows


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
    with open(path, 'w') as f:
        f.write(body)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             read_bytes=len(body), output=path))
    return status, body


def download(source, label, url, path):
    t = now()
    status, _, _ = curl(url, binary_out=path)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             read_bytes=os.path.getsize(path) if os.path.exists(path) else '', output=path))
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
