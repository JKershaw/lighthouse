"""Shared HTTP code for LH044 (the closing web). Every request Lighthouse makes in this study goes
through fetch() below, so every request is labelled the same way, logged, capped and paced.

What a request looks like to the operator (brief, "Lighthouse's own requests"):
  - User-Agent UA_PLAIN for machine probes, robots.txt and instruments, and UA_COMPAT for page
    probes. Both name Lighthouse and the study page; neither claims to be a browser.
  - No cookies, no JavaScript, no retries inside a read, no email address, no key or token.
  - Redirects are not followed automatically: fetch() returns the first response; the collector
    follows at most two same-host redirects itself, each one a counted request.
Bodies: at most CAP bytes are read (decompressed if gzip), retained raw, and hashed (sha256 of the
retained bytes; `truncated` says whether the body went on).
"""
from datetime import datetime, timezone
from hashlib import sha256
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler, ProxyHandler
import os
import socket
import ssl
import time
import zlib

STUDY_URL = 'https://lighthouse.harbour.cat/studies/LH044/'
UA_PLAIN = 'Lighthouse-research/1.0 (+%s)' % STUDY_URL
UA_COMPAT = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +%s)' % STUDY_URL
ROBOTS_TOKEN = 'Lighthouse-research'
CAP = 65536
TIMEOUT = 25
CA = '/root/.ccr/ca-bundle.crt'
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = build_opener(ProxyHandler(), HTTPSHandler(context=CTX), _NoRedirect())


def utcnow():
    return datetime.now(timezone.utc)


def _read_capped(resp, cap):
    raw = b''
    truncated = False
    enc = (resp.headers.get('Content-Encoding') or '').lower().strip()
    if enc == 'gzip':
        d = zlib.decompressobj(16 + zlib.MAX_WBITS)
        while len(raw) < cap:
            chunk = resp.read(16384)
            if not chunk:
                break
            try:
                raw += d.decompress(chunk, cap - len(raw) + 1)
            except zlib.error:
                break
        if len(raw) > cap or resp.read(1):
            truncated = True
        raw = raw[:cap]
    else:
        raw = resp.read(cap + 1)
        if len(raw) > cap:
            truncated = True
            raw = raw[:cap]
    return raw, truncated, enc


def classify_error(exc):
    """A network-level failure, as a short class. A refusal by this container's own egress proxy
    is 'proxy_refused' and is never a wall: the origin was not reached."""
    s = repr(exc)
    reason = getattr(exc, 'reason', exc)
    rs = repr(reason)
    if 'Tunnel connection failed' in s or 'Tunnel connection failed' in rs:
        return 'proxy_refused'
    if isinstance(reason, socket.gaierror) or 'Name or service not known' in rs or 'gaierror' in rs:
        return 'dns'
    if isinstance(reason, (socket.timeout, TimeoutError)) or 'timed out' in rs:
        return 'timeout'
    if isinstance(reason, ssl.SSLError) or 'SSL' in rs or 'CERTIFICATE' in rs:
        return 'tls'
    if 'reset' in rs.lower() or 'ConnectionReset' in rs:
        return 'reset'
    if 'refused' in rs.lower():
        return 'conn_refused'
    if 'RemoteDisconnected' in rs or 'closed' in rs.lower():
        return 'closed'
    return 'other'


def fetch(url, ua=UA_PLAIN, accept='*/*', cap=CAP):
    """One GET. Returns a dict: url, utc, status (int or None), error (None or class), headers
    (list of pairs), body (bytes, at most cap), truncated, sha256, elapsed_ms, ua, accept."""
    req = Request(url, headers={
        'User-Agent': ua,
        'Accept': accept,
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en',
    }, method='GET')
    t0 = time.monotonic()
    out = {'url': url, 'utc': utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 'ua': ua, 'accept': accept,
           'status': None, 'error': None, 'error_detail': '', 'headers': [], 'body': b'',
           'truncated': False, 'encoding': ''}
    try:
        resp = _OPENER.open(req, timeout=TIMEOUT)
        out['status'] = resp.status
        out['headers'] = list(resp.headers.items())
        out['body'], out['truncated'], out['encoding'] = _read_capped(resp, cap)
        resp.close()
    except HTTPError as e:
        out['status'] = e.code
        out['headers'] = list(e.headers.items()) if e.headers else []
        try:
            out['body'], out['truncated'], out['encoding'] = _read_capped(e, cap)
        except Exception as e2:  # body unreadable after an error status
            out['error_detail'] = 'body: ' + repr(e2)[:200]
    except (URLError, OSError, ValueError) as e:
        out['error'] = classify_error(e)
        out['error_detail'] = repr(e)[:300]
    except Exception as e:  # anything else is recorded, never raised
        out['error'] = 'other'
        out['error_detail'] = repr(e)[:300]
    out['elapsed_ms'] = int((time.monotonic() - t0) * 1000)
    out['sha256'] = sha256(out['body']).hexdigest()
    return out


def header(res, name):
    name = name.lower()
    for k, v in res['headers']:
        if k.lower() == name:
            return v
    return ''


def host_of(url):
    return urlsplit(url).hostname or ''
