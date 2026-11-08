#!/usr/bin/env python3
"""A robots.txt gate for Lighthouse's collectors: may this URL be fetched, under the keeper's rule?

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys robots.txt as its own
agent and as whatever runs it. The rule itself is scripts/robots_rules.py with the tokens in
scripts/robots_tokens.json; this module only fetches each host's robots.txt once per run and asks.

  gate = RobotsGate(user_agent)            provider from LIGHTHOUSE_PROVIDER, else all providers
  ok, info = gate.check(url)               info: robots_url, robots_status, robots_sha256, decided_by, rule, reason

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
    def __init__(self, user_agent, provider="env", timeout=30):
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

    def check(self, url):
        rec = self._robots(url)
        info = {"robots_url": rec["robots_url"], "robots_status": rec.get("status"),
                "robots_sha256": rec.get("sha256", ""), "provider": self.provider or "all"}
        st = rec.get("status")
        if st == "error" or (isinstance(st, int) and st >= 500):
            info["reason"] = "robots.txt unreachable; not fetched in this run"
            return False, info
        if isinstance(st, int) and 400 <= st < 500:
            info["reason"] = "robots.txt answered %d: no rules" % st
            return True, info
        if rec.get("truncated"):
            info["reason"] = "robots.txt over 512 KiB; not fetched in this run"
            return False, info
        d = robots_rules.decide(rec["body"], url, provider=self.provider)
        info.update(decided_by=str(getattr(d, "decided_by", "")), rule=str(getattr(d, "rule", "")),
                    reason="allowed by robots.txt" if d.allowed else "disallowed by robots.txt")
        return bool(d.allowed), info


if __name__ == "__main__":
    # python3 -I scripts/robots_gate.py <url> [<url> ...]: may each URL be fetched now? (reads each host's robots.txt once)
    import json
    gate = RobotsGate("Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)")
    worst = 0
    for u in sys.argv[1:]:
        ok, info = gate.check(u)
        print(json.dumps({"url": u, "allowed": ok, **info}))
        worst = worst or (0 if ok else 2)
    sys.exit(worst)
