"""LH007: shared helpers. Every network read goes through here and is logged in
data/read_log.csv with its UTC time, the source, the endpoint, the HTTP status and the bytes read.
No key, token or credential is read from the environment. The only tokens used are the anonymous
pull tokens that auth.docker.io and ghcr.io/token hand to any caller; they are held in memory and
never written to disk."""
import csv, datetime, json, os, re, subprocess, threading, time
import requests
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LOG = os.path.join(DATA, 'read_log.csv')
SCRATCH = os.environ.get('LH007_SCRATCH', '/tmp/claude-0/lh007-scratch')
LOG_FIELDS = ['read_utc', 'source', 'label', 'method', 'endpoint', 'http_status', 'bytes', 'note']
# UA: Lighthouse's User-Agent with its robots token, from scripts/lh_fetch.py (was 'lighthouse-lh007-study (research; anonymous reads)')
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


def git(args, cwd=None, check=True):
    p = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True, timeout=900, env=_git_env(args, cwd))
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: {p.stderr[:500]}')
    return p.stdout
