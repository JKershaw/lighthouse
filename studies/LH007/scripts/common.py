"""LH007: shared helpers. Every network read goes through here and is logged in
data/read_log.csv with its UTC time, the source, the endpoint, the HTTP status and the bytes read.
No key, token or credential is read from the environment. The only tokens used are the anonymous
pull tokens that auth.docker.io and ghcr.io/token hand to any caller; they are held in memory and
never written to disk."""
import csv, datetime, json, os, re, subprocess, threading, time
import requests

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = os.environ.get('LH007_SCRATCH', '/tmp/claude-0/lh007-scratch')
LOG_FIELDS = ['read_utc', 'source', 'label', 'method', 'endpoint', 'http_status', 'bytes', 'note']
UA = 'lighthouse-lh007-study (research; anonymous reads)'
S = requests.Session()
S.headers['User-Agent'] = UA


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


_LOCK = threading.Lock()


def log(**e):
    with _LOCK:
        _log(**e)


def _log(**e):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS, lineterminator='\n')
        if new:
            w.writeheader()
        w.writerow({k: e.get(k, '') for k in LOG_FIELDS})


SIGNED = re.compile(r'sig=|signature|x-amz-|token=|se=20|hmac=', re.I)


def clean(u):
    """A logged endpoint without a signed query string (registries redirect blobs to signed URLs)."""
    return u.split('?')[0] + '?<signed query removed>' if '?' in u and SIGNED.search(u.split('?', 1)[1]) else u


def http(source, label, url, method='GET', headers=None, note='', stream=False, params=None):
    """One logged request. Authorization headers are never logged."""
    for attempt in range(4):
        t = now()
        try:
            r = S.request(method, url, headers=headers or {}, timeout=120, stream=stream, params=params,
                          allow_redirects=True)
            break
        except (requests.ConnectionError, requests.Timeout) as ex:
            log(read_utc=t, source=source, label=label, method=method, endpoint=url.split('?')[0], http_status='',
                bytes='', note=f'connection error, retried: {type(ex).__name__}')
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    n = '' if stream else len(r.content)
    log(read_utc=t, source=source, label=label, method=method, endpoint=clean(r.url if not stream else url),
        http_status=r.status_code, bytes=n, note=note)
    return r


EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')


def write_csv(name, rows, fields=None):
    """Write a table; e-mail addresses found in any text (READMEs, workflow labels) are removed."""
    fields = fields or list(rows[0].keys())
    rows = [{k: EMAIL.sub('<e-mail address removed>', v) if isinstance(v, str) else v for k, v in r.items()} for r in rows]
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def git(args, cwd=None, check=True):
    p = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True, timeout=900)
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: {p.stderr[:500]}')
    return p.stdout
