"""LH011: shared helpers. Every network read goes through here and is logged in data/read_log.csv
with its UTC read time, the endpoint, the query text, the HTTP status, the rows returned and, for
ClickPy, the rows and bytes read as ClickHouse's own X-ClickHouse-Summary header reports them.
No key, token or credential is read or sent: ClickHouse's public `demo` user, PyPI's JSON API,
files.pythonhosted.org and pypistats.org are the only endpoints used, all anonymously.

Adapted from studies/LH005/scripts/common.py. What changed: curl also dumps the response headers so
that ClickHouse's read_rows and read_bytes are logged for every query (the brief's row ceiling is
counted in them); the log has columns read_rows and read_bytes; a running total of queries and rows
read is checked against the brief's ceilings (600 queries, 60 billion rows) before each query;
setting LH011_ONLY replaces LH005_ONLY; a binary download helper for the installers' source
distributions was added; pepy.tech is not used."""
import csv, io, json, os, subprocess, time, datetime

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = '/tmp/claude-0/-home-user-lighthouse/1d316742-ad44-59e1-a3b5-6a3527addf23/scratchpad/LH011'
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo'
LOG_FIELDS = ['read_utc', 'source', 'label', 'endpoint', 'query', 'http_status', 'rows_returned',
              'read_rows', 'read_bytes', 'output']
MAX_QUERIES, MAX_ROWS_READ = 600, 60_000_000_000


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
    """(ClickPy queries so far, ClickPy rows read so far) from the log."""
    if not os.path.exists(LOG):
        return 0, 0
    q = r = 0
    for e in csv.DictReader(open(LOG)):
        if e['source'].startswith('ClickPy'):
            q += 1
            r += int(e['read_rows'] or 0)
    return q, r


def curl(url, data=None, binary_out=None):
    """Return (status, body, headers). curl is used because it reads the session's proxy settings."""
    hdr = os.path.join(SCRATCH, '.headers')
    cmd = ['curl', '-sS', '-D', hdr, '-w', '\n%{http_code}', url]
    if binary_out:
        cmd = ['curl', '-sS', '-L', '-D', hdr, '-o', binary_out, '-w', '%{http_code}', url]
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


def clickhouse(label, sql, output=None):
    """Run one read-only aggregate query on ClickPy's public demo service; write CSV to data/<output>
    (or return rows only when output is None). Setting LH011_ONLY=<label prefix> runs only matching labels."""
    if os.environ.get('LH011_ONLY') and not label.startswith(os.environ['LH011_ONLY']):
        return None
    q, r = spent()
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


def get_json(source, label, url, output=''):
    t = now()
    status, body, _ = curl(url)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             rows_returned='', read_bytes=len(body), output=output))
    time.sleep(0.5)
    if status != '200':
        return status, None
    return status, json.loads(body)


def download(source, label, url, path):
    t = now()
    status, _, _ = curl(url, binary_out=path)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, http_status=status,
             read_bytes=os.path.getsize(path) if os.path.exists(path) else '', output=path))
    return status


def write_csv(name, rows, fields=None):
    """Writes under data/, or under $LH011_OUT when set (the replay's temporary directory)."""
    fields = fields or list(rows[0].keys())
    base = os.environ.get('LH011_OUT', DATA)
    os.makedirs(os.path.dirname(os.path.join(base, name)), exist_ok=True)
    with open(os.path.join(base, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))
