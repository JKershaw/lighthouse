#!/usr/bin/env python3
"""A robots.txt gate for Lighthouse's collectors: may this URL be fetched, under the keeper's rule?

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys robots.txt as its own
agent and as whatever runs it. The rule itself is scripts/robots_rules.py with the tokens in
scripts/robots_tokens.json; this module only fetches each host's robots.txt once per run and asks.

  gate = RobotsGate(user_agent)            provider from LIGHTHOUSE_PROVIDER, else all providers
  ok, info = gate.check(url)               info: robots_url, robots_status, robots_sha256, decided_by, rule, reason,
                                           access, keep_body, keep_reason
  gate.check(url, access='oneoff')         a one-off, targeted read (the keeper, 21 November 2026): obeys
                                           Lighthouse's token and the provider's user-triggered fetcher, else *

keep_body says whether a fetched body may be kept in the repository (robots_rules.may_keep): False
where robots.txt refuses the URL to *, a training crawler or an archiving crawler. A collector that
gets keep_body False keeps the URL, read time, status, hash and the facts it uses, not the body. A
collector should also check robots_rules.page_reservation(body, headers) before keeping a body.

RFC 9309 handling of the robots.txt fetch: up to 512 KiB, complete lines only; redirects followed
(urllib follows them; RFC 9309 asks for at least five); HTTP 4xx means no rules (allowed); 5xx,
a network failure or a body cut at the limit means the URL is not fetched in this run (treated as
disallowed, and recorded so the reading is "not fetched", never a negative).
"""
import hashlib
import os
import sys
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import robots_rules  # noqa: E402

LIMIT = 512 * 1024


class RobotsGate:
    def __init__(self, user_agent, provider="env", timeout=30, access="recurring"):
        if access not in robots_rules.ACCESS:
            raise ValueError("access must be one of %s" % (robots_rules.ACCESS,))
        self.access = access
        self.ua = user_agent
        self.provider = robots_rules.provider_from_env() if provider == "env" else provider
        self.timeout = timeout
        self.cache = {}

    def _robots(self, url):
        p = urlsplit(url)
        robots_url = "%s://%s/robots.txt" % (p.scheme, p.netloc)
        if robots_url in self.cache:
            return self.cache[robots_url]
        rec = {"robots_url": robots_url}
        try:
            req = Request(robots_url, headers={"User-Agent": self.ua})
            try:
                resp = urlopen(req, timeout=self.timeout)
            except HTTPError as e:
                resp = e
            with resp:
                body = resp.read(LIMIT + 1)
                rec.update(status=resp.status, sha256=hashlib.sha256(body).hexdigest(),
                           truncated=len(body) > LIMIT, body=body[:LIMIT])
        except Exception as e:  # unreachable: do not fetch in this run
            rec.update(status="error", error=type(e).__name__ + ": " + str(e))
        self.cache[robots_url] = rec
        return rec

    def check(self, url, access=None):
        access = access or self.access
        rec = self._robots(url)
        info = {"robots_url": rec["robots_url"], "robots_status": rec.get("status"),
                "robots_sha256": rec.get("sha256", ""), "provider": self.provider or "all", "access": access,
                "keep_body": False, "keep_reason": "not fetched"}
        st = rec.get("status")
        if st == "error" or (isinstance(st, int) and st >= 500):
            info["reason"] = "robots.txt unreachable; not fetched in this run"
            return False, info
        if isinstance(st, int) and 400 <= st < 500:
            info["reason"] = "robots.txt answered %d: no rules" % st
            info.update(keep_body=True, keep_reason="robots.txt answered %d: no rules" % st)
            return True, info
        if rec.get("truncated"):
            info["reason"] = "robots.txt over 512 KiB; not fetched in this run"
            return False, info
        d = robots_rules.decide(rec["body"], url, provider=self.provider, access=access)
        keep, why = robots_rules.may_keep(rec["body"], url)
        info.update(decided_by=str(getattr(d, "decided_by", "")), rule=str(getattr(d, "rule", "")),
                    reason="allowed by robots.txt" if d.allowed else "disallowed by robots.txt")
        if d.allowed:
            info.update(keep_body=keep, keep_reason=why)
        return bool(d.allowed), info

    def may_keep(self, url, access=None):
        """(keep, reason) for a body fetched from url, from the cached robots.txt. Pass the access
        mode the URL was read under, and the final URL after any redirect."""
        ok, info = self.check(url, access)
        return info["keep_body"], info["keep_reason"]


if __name__ == "__main__":
    # python3 -I scripts/robots_gate.py [--oneoff] <url> [<url> ...]: may each URL be fetched now, and may its
    # body be kept? (reads each host's robots.txt once)
    import json
    args = sys.argv[1:]
    access = "oneoff" if "--oneoff" in args else "recurring"
    gate = RobotsGate("Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)",
                      access=access)
    worst = 0
    for u in [a for a in args if a != "--oneoff"]:
        ok, info = gate.check(u)
        print(json.dumps({"url": u, "allowed": ok, **info}))
        worst = worst or (0 if ok else 2)
    sys.exit(worst)
