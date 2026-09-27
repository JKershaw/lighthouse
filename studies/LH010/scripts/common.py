"""LH010: shared helpers, copied from LH009's unchanged except for the study name, the user agent and the scratch directory. Every network read goes through here and is logged in
data/read_log.csv with its UTC time, the source, the endpoint, the HTTP status and the bytes read.
No key, token or credential is read from the environment; every source read is anonymous.
Clones are held in LH010_SCRATCH (default /tmp/claude-0/lh010-work), outside the repository.

Added in version 0.3 of the record (27 September 2026), for the offline replay (REPLAY.md): tables are written to
LH010_OUT when that environment variable names a directory, and to data/ otherwise (the behaviour every committed
table was made with); tables are always read from data/. `requests` is imported only if installed, so the scripts
that need no network (classes.py, analyse.py, reanalyse.py) run on the standard library alone; the collection
scripts still need it."""
import csv, datetime, json, os, re, subprocess, threading, time
try:
    import requests
except ImportError:  # offline replay: no network read is made
    requests = None

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
OUT = os.environ.get('LH010_OUT') or DATA
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = os.environ.get('LH010_SCRATCH', '/tmp/claude-0/lh010-work')
LOG_FIELDS = ['read_utc', 'source', 'label', 'method', 'endpoint', 'http_status', 'bytes', 'note']
UA = 'lighthouse-lh010-study (research; anonymous reads)'
S = requests.Session() if requests else None
if S is not None:
    S.headers['User-Agent'] = UA
FMT = '%Y-%m-%dT%H:%M:%SZ'


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime(FMT)


def ts(s):
    """Parse an ISO time (Z, offset or fractional seconds) to an aware UTC datetime."""
    s = s.strip().replace('Z', '+00:00')
    s = re.sub(r'\.\d+', '', s)
    d = datetime.datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc)


def iso(d):
    return d.astimezone(datetime.timezone.utc).strftime(FMT)


_LOCK = threading.Lock()


def log(**e):
    with _LOCK:
        new = not os.path.exists(LOG)
        with open(LOG, 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=LOG_FIELDS, lineterminator='\n')
            if new:
                w.writeheader()
            w.writerow({k: e.get(k, '') for k in LOG_FIELDS})


def http(source, label, url, method='GET', json_body=None, data=None, note=''):
    if requests is None:
        raise RuntimeError('the collection scripts need the requests package and the network')
    for attempt in range(4):
        t = now()
        try:
            r = S.request(method, url, json=json_body, data=data, timeout=120)
            if r.status_code in (429, 500, 502, 503, 504) and attempt < 3:
                log(read_utc=t, source=source, label=label, method=method, endpoint=url, http_status=r.status_code,
                    bytes=len(r.content), note='retried')
                time.sleep(3 * (attempt + 1))
                continue
            break
        except (requests.ConnectionError, requests.Timeout) as ex:
            log(read_utc=t, source=source, label=label, method=method, endpoint=url, http_status='', bytes='',
                note=f'connection error, retried: {type(ex).__name__}')
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    log(read_utc=t, source=source, label=label, method=method, endpoint=url, http_status=r.status_code,
        bytes=len(r.content), note=note)
    return r


def jget(source, label, url):
    r = http(source, label, url)
    return r.json() if r.status_code == 200 else None


EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')


def write_csv(name, rows, fields=None, keep_email=False):
    """Write a table. E-mail addresses are removed from every text field unless keep_email (never used for
    people's addresses; bot addresses are reduced to a class before writing)."""
    fields = fields or (list(rows[0].keys()) if rows else ['empty'])
    if not keep_email:
        rows = [{k: EMAIL.sub('<e-mail address removed>', v) if isinstance(v, str) else v for k, v in r.items()}
                for r in rows]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def git(args, cwd=None, check=True, timeout=900):
    p = subprocess.run(['git', '-c', 'credential.helper=', '-c', 'core.askPass=true'] + args, cwd=cwd,
                       capture_output=True, text=True, timeout=timeout, env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'},
                       errors='replace')
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: {p.stderr[:500]}')
    return p.stdout


def norm(n):
    """PEP 503 normalised name."""
    return re.sub(r'[-_.]+', '-', n).lower()
