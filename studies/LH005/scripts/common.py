"""LH005: shared helpers. Every network read goes through here, so that each one is logged in
data/read_log.csv with its UTC read time, the endpoint, the query text and what came back.
No key, token or credential is read or sent: ClickHouse's public demo user, pypistats.org and
pepy.tech's anonymous path are the only endpoints used."""
import csv, io, json, os, subprocess, time, datetime

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo'
LOG_FIELDS = ['read_utc', 'source', 'label', 'endpoint', 'query', 'http_status', 'rows_or_bytes', 'output']


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(entry):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow(entry)


def curl(url, data=None):
    """Return (status, body). curl is used because it reads the session's proxy settings."""
    cmd = ['curl', '-sS', '-w', '\n%{http_code}', url]
    if data is not None:
        cmd += ['--data-binary', '@-']
    p = subprocess.run(cmd, input=(data or '').encode(), capture_output=True, timeout=180)
    out = p.stdout.decode('utf-8', 'replace')
    body, _, status = out.rpartition('\n')
    return status.strip(), body


def clickhouse(label, sql, output):
    """Run one read-only aggregate query on ClickPy's public demo service and write CSV to data/.
    Setting LH005_ONLY=<label prefix> runs only the queries whose label starts with it."""
    if os.environ.get('LH005_ONLY') and not label.startswith(os.environ['LH005_ONLY']):
        return None
    sql = ' '.join(sql.split()) + ' FORMAT CSVWithNames'
    t = now()
    status, body = curl(CLICKHOUSE, sql)
    rows = list(csv.DictReader(io.StringIO(body))) if status == '200' else []
    log(dict(read_utc=t, source='ClickPy (ClickHouse public demo)', label=label, endpoint=CLICKHOUSE,
             query=sql, http_status=status, rows_or_bytes=len(rows), output=output))
    if status != '200':
        raise SystemExit(f'{label}: HTTP {status}: {body[:300]}')
    with open(os.path.join(DATA, output), 'w') as f:
        f.write(body if body.endswith('\n') else body + '\n')
    time.sleep(1)  # be gentle with a free public service
    return rows


def get_json(source, label, url, output=None):
    t = now()
    status, body = curl(url)
    log(dict(read_utc=t, source=source, label=label, endpoint=url, query='', http_status=status,
             rows_or_bytes=len(body), output=output or ''))
    time.sleep(1)
    if status != '200':
        return status, None
    return status, json.loads(body)


def write_csv(name, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))
