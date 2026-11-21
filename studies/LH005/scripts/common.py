"""LH005: shared helpers. Every network read goes through here, so that each one is logged in
data/read_log.csv with its UTC read time, the endpoint, the query text and what came back.
No key, token or credential is read or sent: ClickHouse's public demo user, pypistats.org and
pepy.tech's anonymous path are the only endpoints used.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH005/scripts/common.py`."""
import csv, io, json, os, subprocess, time, datetime
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
import hashlib, urllib.error, urllib.request  # noqa: E402
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body, write_derived, keep_decision  # noqa: E402  robots.txt gate (8 November 2026); one keep path (21 November)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies

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


LAST = {}  # the latest response's final URL and headers, for save_body (21 November 2026)


def curl(url, data=None):
    """Return (status, body). Until 21 November 2026 this ran the curl command; it now requests through
    scripts/lh_fetch.py's urlopen (the keeper's decision of that day, notes/keeper/2026-11-21-robots-intent.md:
    one gated fetch path for every collector). The robots.txt gate is asked first, as before, and urlopen asks
    the same cached gate, so robots.txt is read once. Return values are as before: the status as text ('000'
    where no response came, curl's code), and the body as text (the header block is not returned here).
    One difference: curl here did not follow redirects; urllib follows them, each checked against robots.txt first
    (check_redirects=True), and a refused redirect returns "not fetched: ..."."""
    # The robots.txt gate first (the keeper, 8 November 2026): a URL it does not allow, or whose robots.txt
    # cannot be read, is not requested; the status returned, and so logged, is "not fetched: ..." with the
    # deciding group and rule, a missing reading and never a negative.
    ok, info = robots_check(url)
    if not ok:
        return ('not fetched: %s (robots %s, status %s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
                info.get('robots_status'), info.get('decided_by', ''), info.get('rule', ''))), ''
    req = urllib.request.Request(url, data=None if data is None else data.encode(),
                                 headers={'User-Agent': UA})
    LAST.clear()
    LAST.update(final=url, headers=None)
    try:
        try:
            resp = urlopen(req, timeout=180, check_redirects=True)
        except urllib.error.HTTPError as e:
            resp = e
        with resp:
            raw = resp.read()
            LAST.update(final=resp.geturl() or url, headers=resp.headers)
            status = str(resp.status)
            head = 'HTTP/1.1 %s %s\r\n%s\r\n' % (resp.status, getattr(resp, 'reason', ''),
                                                 ''.join('%s: %s\r\n' % kv for kv in resp.headers.items()))
    except NotFetched as e:  # a redirect robots.txt refuses: not requested, logged as not fetched
        return 'not fetched: ' + str(e).replace('not fetched: ', '', 1), ''
    except Exception:  # no response (curl reported 000)
        return '000', ''
    return status, raw.decode('utf-8', 'replace')

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
    _save_query(os.path.join(DATA, output), body, t, status, sql, rows)
    time.sleep(1)  # be gentle with a free public service
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
