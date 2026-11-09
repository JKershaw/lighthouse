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


def check(url):
    return _GATE.check(url)


def urlopen(request, *args, **kwargs):
    url = request.full_url if isinstance(request, urllib.request.Request) else request
    ok, info = _GATE.check(url)
    if not ok:
        raise NotFetched("not fetched: %s (robots %s, status %s, group %s, rule %s, sha256 %s)" % (
            info.get("reason"), info.get("robots_url"), info.get("robots_status"),
            info.get("decided_by", ""), info.get("rule", ""), info.get("robots_sha256", "")[:16]))
    return urllib.request.urlopen(request, *args, **kwargs)
