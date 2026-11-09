"""LH009: shared helpers, copied from LH008's (which were adapted from LH007's). Every network read goes through here and is logged in
data/read_log.csv with its UTC time, the source, the endpoint, the HTTP status and the bytes read.
No key, token or credential is read from the environment; every source read is anonymous.
Clones are held in LH009_SCRATCH (default /tmp/claude-0/lh009-work), outside the repository."""
import csv, datetime, json, os, re, subprocess, threading, time
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies
import requests

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = os.environ.get('LH009_SCRATCH', '/tmp/claude-0/lh009-work')
LOG_FIELDS = ['read_utc', 'source', 'label', 'method', 'endpoint', 'http_status', 'bytes', 'note']
# UA: Lighthouse's User-Agent with its robots token, from scripts/lh_fetch.py (was 'lighthouse-lh009-study (research; anonymous reads)')
S = requests.Session()
S.headers['User-Agent'] = UA

_request = S.request


def _gated_request(method, url, *args, **kwargs):
    """Every request through the session asks the robots.txt gate first (the keeper, 8 November 2026).
    A URL it does not allow, or whose robots.txt cannot be read, is not requested: the read log gets a
    "not fetched" row with the deciding group and rule, and NotFetched stops the step (a missing reading,
    never a negative)."""
    ok, info = robots_check(url)
    if not ok:
        why = 'not fetched: %s (robots %s, status %s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
              info.get('robots_status'), info.get('decided_by', ''), info.get('rule', ''))
        log(read_utc=now(), source='robots.txt gate', label='', method=method, endpoint=url.split('?')[0],
            http_status='not fetched', bytes='', note=why)
        raise NotFetched(why)
    return _request(method, url, *args, **kwargs)


S.request = _gated_request

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
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


_ORIGIN_OK = {}


def _git_env(args, cwd):
    """The robots.txt gate for git over HTTPS (the keeper, 8 November 2026). A clone's https URL is checked
    first, and a clone it does not allow is not made (RuntimeError "not fetched: ..."). In an existing partial
    clone, which fetches missing objects from its origin on demand, the origin is checked once; if it is not
    allowed, git is told not to fetch (GIT_NO_LAZY_FETCH), so a missing object is an error, not a request."""
    if 'clone' in args:
        for a in args:
            if a.startswith('https://'):
                ok, info = robots_check(a)
                if not ok:
                    raise RuntimeError('not fetched: %s (robots %s, status %s, group %s, rule %s)' % (
                        info.get('reason'), info.get('robots_url'), info.get('robots_status'),
                        info.get('decided_by', ''), info.get('rule', '')))
        return None
    if cwd:
        if cwd not in _ORIGIN_OK:
            o = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], cwd=cwd, capture_output=True, text=True).stdout.strip()
            _ORIGIN_OK[cwd] = robots_check(o)[0] if o.startswith('https://') else True
        if not _ORIGIN_OK[cwd]:
            return dict(os.environ, GIT_NO_LAZY_FETCH='1')
    return None


def git(args, cwd=None, check=True, timeout=900):
    p = subprocess.run(['git', '-c', 'credential.helper=', '-c', 'core.askPass=true'] + args, cwd=cwd,
                       capture_output=True, text=True, timeout=timeout,
                       env={**os.environ, 'GIT_TERMINAL_PROMPT': '0', **(_git_env(args, cwd) or {})},
                       errors='replace')
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: {p.stderr[:500]}')
    return p.stdout


def norm(n):
    """PEP 503 normalised name."""
    return re.sub(r'[-_.]+', '-', n).lower()
