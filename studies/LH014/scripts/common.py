"""LH014: shared helpers. Every network read goes through here and is logged in data/read_log.csv
with its UTC read time, the endpoint, the query text, the HTTP status, the rows returned and, for
ClickPy, the rows and bytes read as ClickHouse's own X-ClickHouse-Summary header reports them.
No key, token or credential is read or sent: ClickHouse's public `demo` user, PyPI's JSON API and a
few documentation pages are the only endpoints used, all anonymously.

Adapted from studies/LH012/scripts/common.py. What changed: paths, the scratch directory and the
environment switches (LH014_ONLY, LH014_PHASE, LH014_OUT) are this study's; the ceilings are this
brief's (800 ClickPy queries, 60 billion rows read, 400 PyPI JSON requests, 5 documentation reads);
the phase gate is stricter than LH012's: while LH014_PHASE is 1 (the default) only queries on the
`system` database, or with no FROM clause, run, so no table of the `pypi` database is read at all;
in phase 2 (the frame) the August monthly sums, dates held and installer names may also be read, and
nothing that counts; from phase 3, set only after amendment 1 is snapshotted, any query runs that
bounds its dates at or before 2026-09-27, the brief's cut (checked in phases 2 and 3 alike);
a ClickPy body that begins with HTTP 200 but carries a ClickHouse exception is treated as failed
(LH012, amendment 2); every query that reads the `pypi` database carries
`SETTINGS read_overflow_mode = 'throw'`, because the `demo` user's default is 'break', which returns a
partial result without error once a query passes the read limit, and a query whose reported rows or
bytes read reach that limit is treated as failed whatever it returned; `get_text` counts
documentation reads against the ceiling."""
import csv, io, json, os, re, subprocess, time, datetime

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = '/tmp/claude-0/-home-user-lighthouse/e0b16c49-af19-40c8-8a58-f38ee3e4b335/scratchpad/LH014'
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo'
LOG_FIELDS = ['read_utc', 'source', 'label', 'endpoint', 'query', 'http_status', 'rows_returned',
              'read_rows', 'read_bytes', 'output']
MAX_QUERIES, MAX_ROWS_READ, MAX_PYPI, MAX_DOCS = 800, 60_000_000_000, 400, 5
READ_LIMIT_ROWS, READ_LIMIT_BYTES = 1_000_000_000, 50_000_000_000   # the demo user's per-query read limits
PHASE = os.environ.get('LH014_PHASE', '1')
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
    """(ClickPy queries, ClickPy rows read, PyPI JSON requests, documentation reads) so far, from the log."""
    if not os.path.exists(LOG):
        return 0, 0, 0, 0
    q = r = p = d = 0
    for e in csv.DictReader(open(LOG)):
        if e['source'].startswith('ClickPy'):
            q += 1
            r += int(e['read_rows'] or 0)
        elif e['source'].startswith('PyPI JSON'):
            p += 1
        elif e['source'].startswith('Documentation'):
            d += 1
    return q, r, p, d


def curl(url, data=None, accept=None):
    """Return (status, body, headers). curl is used because it reads the session's proxy settings."""
    hdr = os.path.join(SCRATCH, '.headers')
    cmd = ['curl', '-sS', '-L', '-D', hdr, '-w', '\n%{http_code}', url]
    if accept:
        cmd[1:1] = ['-H', 'Accept: ' + accept]
    if data is not None:
        cmd += ['--data-binary', '@-']
    p = subprocess.run(cmd, input=(data or '').encode(), capture_output=True, timeout=300)
    out = p.stdout.decode('utf-8', 'replace')
    body, _, status = out.rpartition('\n')
    headers = open(hdr).read() if os.path.exists(hdr) else ''
    return status.strip(), body, headers


def summary(headers):
    for line in headers.splitlines():
        if line.lower().startswith('x-clickhouse-summary:'):
            return json.loads(line.split(':', 1)[1])
    return {}


CUT = '2026-09-27'   # the brief's cut: no download on a later day is read


def phase1_allowed(sql):
    """True only for a query that reads no table of the `pypi` database: every FROM names a `system`
    table, or there is no FROM (SELECT version(), getSetting(...) and the like)."""
    s = ' '.join(sql.split())
    froms = re.findall(r'\bFROM\s+([\w.`"]+)', s, re.I)
    return all(f.strip('`"').lower().startswith('system.') for f in froms) and not re.search(r'\bpypi\.', s, re.I)


def cut_respected(sql):
    """True when every date literal in the query is on or before the cut and, for a query on a per-day
    table or `pypi.pypi`, the date is bounded (BETWEEN, <=, < or IN)."""
    s = ' '.join(sql.split())
    dates = re.findall(r"'(\d{4}-\d{2}-\d{2})'", s)
    if any(d > CUT for d in dates):
        return False
    daily = re.search(r'\bpypi\.(pypi\b|pypi_downloads_per_day)', s, re.I)
    return not daily or (bool(dates) and bool(re.search(r'\bdate\s*(BETWEEN\b|<=|<|IN\b)', s, re.I)))


def phase2_allowed(sql):
    """Phase 2 (the frame, before amendment 1 is snapshotted): phase 1's reads; the August monthly sums
    (the frame); and queries whose select list is only project, installer or min()/max() of a date,
    with no aggregate that counts and no mention of the count column (dates held, installer names).
    Every one must respect the cut."""
    s = ' '.join(sql.split())
    if phase1_allowed(s):
        return True
    if not cut_respected(s):
        return False
    froms = [f.strip('`"').lower() for f in re.findall(r'\bFROM\s+([\w.`"]+)', s, re.I)]
    if froms and all(f == 'pypi.pypi_downloads_per_month' for f in froms) and "month = '2026-08-01'" in s:
        return True
    if re.search(r'\bcount\b|\bHAVING\b|\b(sum|uniq|avg|quantile|any|groupArray|topK|argMax|argMin)\w*\s*\(', s, re.I):
        return False
    m = re.match(r'SELECT (?:DISTINCT )?(.*?) FROM ', s, re.I)
    if not m:
        return False
    items = [x.strip() for x in re.split(r',(?![^()]*\))', m.group(1))]
    return all(re.fullmatch(r'(project|installer|(min|max)\((min_date|max_date|date)\))( AS \w+)?', x, re.I) for x in items)


def clickhouse(label, sql, output=None):
    """Run one read-only query on ClickPy's public demo service; write CSV to data/<output> (or return
    rows only when output is None). Setting LH014_ONLY=<label prefix> runs only matching labels."""
    if os.environ.get('LH014_ONLY') and not label.startswith(os.environ['LH014_ONLY']):
        return None
    if PHASE == '1' and not phase1_allowed(sql):
        raise SystemExit(f'{label}: refused in phase 1, since it reads the pypi database: {sql[:200]}')
    if PHASE == '2' and not phase2_allowed(sql):
        raise SystemExit(f'{label}: refused in phase 2, since it could return a count other than the frame: {sql[:200]}')
    if PHASE not in ('1', '2') and not cut_respected(sql):
        raise SystemExit(f'{label}: refused, since it could read a day after {CUT}: {sql[:200]}')
    q, r, _, _ = spent()
    if q >= MAX_QUERIES or r >= MAX_ROWS_READ:
        raise SystemExit(f'ceiling reached: {q} queries, {r} rows read')
    sql = ' '.join(sql.split())
    if re.search(r'\bpypi\.', sql, re.I) and 'read_overflow_mode' not in sql:
        # the demo user's read_overflow_mode is 'break' (data/clickpy_server.csv): past the read limit a
        # query returns a partial result without error. 'throw' makes it fail instead (brief, Resource ceiling).
        sql += (", " if re.search(r'\bSETTINGS\b', sql, re.I) else " SETTINGS ") + "read_overflow_mode = 'throw'"
    sql += ' FORMAT CSVWithNames'
    t = now()
    status, body, headers = curl(CLICKHOUSE, sql)
    s = summary(headers)
    failed = status != '200' or 'DB::Exception' in body or body.startswith('Code: ')
    # second guard: a query that reports reading the per-query limit may be partial, whatever the setting
    failed = failed or int(s.get('read_rows') or 0) >= READ_LIMIT_ROWS or int(s.get('read_bytes') or 0) >= READ_LIMIT_BYTES
    rows = [] if failed else list(csv.DictReader(io.StringIO(body)))
    log(dict(read_utc=t, source='ClickPy (ClickHouse public demo)', label=label, endpoint=CLICKHOUSE,
             query=sql, http_status=status + (' (exception in body)' if failed and status == '200' else ''),
             rows_returned=len(rows), read_rows=s.get('read_rows', ''), read_bytes=s.get('read_bytes', ''),
             output=output or ''))
    if failed:
        raise SystemExit(f'{label}: HTTP {status}: {body[:400]}')
    if output:
        with open(os.path.join(DATA, output), 'w') as f:
            f.write(body if body.endswith('\n') else body + '\n')
    time.sleep(0.5)  # be gentle with a free public service
    return rows


def get_json(source, label, url, output='', pause=0.2):
    if source.startswith('PyPI JSON') and spent()[2] >= MAX_PYPI:
        raise SystemExit('PyPI request ceiling reached')
    t = now()
    status, body, _ = curl(url)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             rows_returned='', read_bytes=len(body), output=output))
    time.sleep(pause)
    if status != '200':
        return status, None
    return status, json.loads(body)


def get_text(label, url, path):
    """A documentation page, saved to scratch space (not retained) and logged."""
    if spent()[3] >= MAX_DOCS:
        raise SystemExit('documentation read ceiling reached')
    t = now()
    status, body, _ = curl(url)
    with open(path, 'w') as f:
        f.write(body)
    log(dict(read_utc=t, source='Documentation', label=label, endpoint=url, http_status=status,
             read_bytes=len(body), output=path))
    return status, body


def write_csv(name, rows, fields=None):
    """Writes under data/, or under $LH014_OUT when set (the replay's temporary directory)."""
    fields = fields or list(rows[0].keys())
    base = os.environ.get('LH014_OUT', DATA)
    os.makedirs(os.path.dirname(os.path.join(base, name)), exist_ok=True)
    with open(os.path.join(base, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))
