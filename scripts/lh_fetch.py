#!/usr/bin/env python3
"""How every Lighthouse collector fetches and saves: a robots.txt-gated urlopen, and the one place
the rule on keeping a body is applied.

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys robots.txt as its own agent
and as whatever runs it. Collectors written before that rule call urllib's urlopen directly; they now
import `urlopen` from here instead, which asks scripts/robots_gate.py first. A URL that robots.txt
disallows, or whose robots.txt cannot be read, is not requested: `NotFetched` is raised, and the
collector's own error handling logs it as a missing reading ("NotFetched: ..."), never a negative.

  from lh_fetch import urlopen, redacted, UA      (redacted(body) -> bytes; redact_bytes -> (bytes, count))
  urlopen(req, access='oneoff')                    a one-off, targeted read (the keeper, 21 November 2026)
  save_body(path, body, url, headers, gate=, robots_body=) -> (kept, reason)
                                                  writes a body only where it may be kept
  keep_decision(url, body, headers, ...)          the keep rule itself: robots.txt and the page's reservation
  write_derived(path, url, reason, extracted, **meta)   the record that stands in for a body not kept

The keeper, 21 November 2026 (notes/keeper/2026-11-21-robots-intent.md): no body is kept where
robots.txt refuses *, an AI-training or archiving crawler, or the page reserves itself from AI use.
Every collector saves bodies only through save_body (notes/keeper/robots-intent-2026-11-21/
collectors_wired.md); where it says no, the collector logs body_kept = "no: <reason>" and, where its
measures need facts from the page, writes them with write_derived.

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



NOT_KEPT_NOTE = ("Body not kept under the keeper's decision of 21 November 2026 (notes/keeper/2026-11-21-robots-intent.md): "
                 "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, or the page reserves itself "
                 "from AI use, so Lighthouse keeps the URL, read time, status, SHA-256 of the bytes received and the facts "
                 "its records use, not the page.")


_UNSET = object()


def keep_decision(url, body=None, headers=None, access=None, gate=None, robots_body=_UNSET):
    """(keep, reason) for a body fetched from url (the final URL after any redirect): robots.txt
    (robots_rules.may_keep, through the gate's cached file) and, when body or headers are given, the
    page's own noai / TDM reservation (robots_rules.page_reservation). gate: a collector's own
    RobotsGate, so robots.txt is read once per run; defaults to this module's gate. robots_body: the
    site's robots.txt already read by the caller (bytes), or None where it answered 4xx (no rules);
    then no gate is consulted. The one place the keep rule is applied; save_body and collectors
    that store bodies in their own form use it."""
    from robots_rules import page_reservation, may_keep as _may_keep_rules
    if robots_body is _UNSET:
        keep, why = (gate or _GATE).may_keep(url, access)
    elif robots_body is None:
        keep, why = True, 'robots.txt gave no rules'
    else:
        keep, why = _may_keep_rules(robots_body, url)
    if not keep:
        return False, why
    reserved = page_reservation(body, headers) if (body is not None or headers is not None) else None
    return (False, reserved) if reserved else (True, why)


def save_body(path, body, url, headers=None, access=None, gzip_body=None, gate=None, robots_body=_UNSET):
    """Save a fetched body only if it may be kept (keep_decision). Returns (kept, reason). Where it
    may not be kept, nothing is written: the caller logs body_kept = "no: <reason>" with URL, read
    time, status, size and the SHA-256 of the bytes received, and writes a derived file
    (write_derived) where its measures need facts from the page; a later script that finds no body
    treats the reading as unavailable, never as zero. Email addresses are withheld from a kept body.
    gzip_body defaults to whether path ends in .gz."""
    import gzip as _gzip
    keep, why = keep_decision(url, body, headers, access, gate, robots_body)
    if not keep:
        return False, why
    data = redacted(body)
    if gzip_body is None:
        gzip_body = str(path).endswith('.gz')
    if gzip_body:
        data = _gzip.compress(data, mtime=0)
    with open(path, 'wb') as f:
        f.write(data)
    return True, why


def write_derived(path, url, reason, extracted, **meta):
    """Write the derived file that stands in for a body not kept: URL, the reason, the facts a study
    uses (extracted), and any metadata given (read_utc, finish_utc, http_status, content_type, bytes,
    sha256, used_for ...), with the standard note. JSON, UTF-8, one indent."""
    import json as _json
    rec = {'url': url, **meta, 'body_kept': 'no: ' + str(reason), 'body_removed': NOT_KEPT_NOTE,
           'extracted': extracted}
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    return path
