#!/usr/bin/env python3
"""A drop-in, robots.txt-gated urlopen for Lighthouse's older collectors (robots sweep, 9 November 2026).

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys robots.txt as its own agent
and as whatever runs it. Collectors written before that rule call urllib's urlopen directly; they now
import `urlopen` from here instead, which asks scripts/robots_gate.py first. A URL that robots.txt
disallows, or whose robots.txt cannot be read, is not requested: `NotFetched` is raised, and the
collector's own error handling logs it as a missing reading ("NotFetched: ..."), never a negative.

  from lh_fetch import urlopen, redacted, UA      (redacted(body) -> bytes; redact_bytes -> (bytes, count))

UA is Lighthouse's User-Agent with its robots token. redact_bytes withholds email addresses from a body
before it is saved (the keeper, 8 November 2026); a fetch log keeps the hash of the bytes received.
The provider is read from LIGHTHOUSE_PROVIDER; unset, every listed provider's tokens are obeyed.
"""
import os
import sys
import urllib.request
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from robots_gate import RobotsGate  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402,F401

UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
_GATE = RobotsGate(UA)


def redacted(body):
    """The body with email addresses withheld, as bytes (redact_bytes also returns the count)."""
    return redact_bytes(body)[0]


class NotFetched(Exception):
    """robots.txt disallows the URL, or could not be read: not requested in this run."""


def check(url, access=None):
    return _GATE.check(url, access)


def may_keep(url, access=None):
    """(keep, reason): may a body fetched from url be kept in the repository? (the keeper, 21 November
    2026: not where robots.txt refuses * or a training or archiving crawler). Pass the final URL after
    any redirect and the access mode it was read under. Also check
    robots_rules.page_reservation(body, headers) on the body itself."""
    return _GATE.may_keep(url, access)


def _require_allowed(url, access=None):
    ok, info = _GATE.check(url, access)
    if not ok:
        raise NotFetched("not fetched: %s (robots %s, status %s, group %s, rule %s, sha256 %s)" % (
            info.get("reason"), info.get("robots_url"), info.get("robots_status"),
            info.get("decided_by", ""), info.get("rule", ""), info.get("robots_sha256", "")[:16]))


class _RobotsCheckedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, access=None):
        super().__init__()
        self.access = access

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            parts = urlsplit(newurl)
            if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
                raise NotFetched("not fetched: invalid HTTP(S) redirect destination")
            _require_allowed(newurl, self.access)
        except (NotFetched, ValueError):
            fp.close()
            raise
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def urlopen(request, *args, check_redirects=False, access=None, **kwargs):
    """Check robots.txt before fetching, and before each redirect when requested. access='oneoff' for a
    one-off, targeted read; the default is the recurring-collection rule."""
    url = request.full_url if isinstance(request, urllib.request.Request) else request
    _require_allowed(url, access)
    if check_redirects:
        opener = urllib.request.build_opener(_RobotsCheckedRedirect(access))
        return opener.open(request, *args, **kwargs)
    return urllib.request.urlopen(request, *args, **kwargs)


def save_body(path, body, url, headers=None, access=None, gzip_body=None):
    """Save a fetched body only if it may be kept (the keeper, 21 November 2026). Returns
    (kept, reason). url is the final URL after any redirect; headers the response headers (for a
    page's own noai / TDM reservation). Where the body may not be kept, nothing is written: the
    caller logs URL, read time, status, size, the SHA-256 of the bytes received and the reason, and
    keeps only the facts its measures use; a later script that finds no body treats the reading as
    unavailable, never as zero. Email addresses are withheld from a kept body. gzip_body defaults to
    whether path ends in .gz."""
    import gzip as _gzip
    from robots_rules import page_reservation
    keep, why = may_keep(url, access)
    reserved = page_reservation(body, headers) if keep else None
    if not keep or reserved:
        return False, reserved or why
    data = redacted(body)
    if gzip_body is None:
        gzip_body = str(path).endswith('.gz')
    if gzip_body:
        data = _gzip.compress(data, mtime=0)
    with open(path, 'wb') as f:
        f.write(data)
    return True, why
