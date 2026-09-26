"""LH006: shared helpers. Every network read goes through here and is logged in
data/read_log.csv with its UTC time, the source, the endpoint, the HTTP status and the bytes read.
No key, token or credential is read from the environment. The only tokens used are the anonymous
pull tokens that auth.docker.io and ghcr.io/token hand to any caller; they are held in memory and
never written to disk."""
import csv, datetime, json, os, subprocess, time
import requests

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = os.environ.get('LH006_SCRATCH', '/tmp/lh006-scratch')
LOG_FIELDS = ['read_utc', 'source', 'label', 'method', 'endpoint', 'http_status', 'bytes', 'note']
UA = 'lighthouse-lh006-study (research; anonymous reads)'
S = requests.Session()
S.headers['User-Agent'] = UA


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(**e):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS, lineterminator='\n')
        if new:
            w.writeheader()
        w.writerow({k: e.get(k, '') for k in LOG_FIELDS})


def http(source, label, url, method='GET', headers=None, note='', stream=False, params=None):
    """One logged request. Authorization headers are never logged."""
    t = now()
    r = S.request(method, url, headers=headers or {}, timeout=120, stream=stream, params=params,
                  allow_redirects=True)
    n = '' if stream else len(r.content)
    log(read_utc=t, source=source, label=label, method=method, endpoint=r.url if not stream else url,
        http_status=r.status_code, bytes=n, note=note)
    return r


def write_csv(name, rows, fields=None):
    fields = fields or list(rows[0].keys())
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
