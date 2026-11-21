"""R-0057: re-read a sample of LH041's vendor pages live, keeping the bytes
gzipped (emails redacted) with URL, UTC time, status and sha256 of bytes received.
Asks scripts/robots_gate.py first (robots sweep, 9 November 2026; it replaced urllib.robotparser checked
for this script's own User-Agent): a URL it disallows, or whose robots.txt cannot be read, is not fetched,
and the log's robots column gives the deciding group and rule.
From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md; the record of review
R-0057, not run again): the page is fetched with scripts/lh_fetch.py's urlopen, which asks the same cached
gate (rule and robots.txt reads unchanged), and saved only through lh_fetch's save_body; where it may not be
kept no .html.gz is written and the robots column ends "; body_kept: no: <reason>". A kept page is written
under the same name with the same decompressed bytes; the gzip header now has mtime 0 and no file name
(before, gzip.open's). Run from the repository root:
    python3 -I studies/LH041/review/fetch_sample.py

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH041/review/fetch_sample.py`.
"""
import hashlib, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from lh_fetch import check as robots_check, urlopen, save_body, UA  # noqa: E402  robots.txt rule (8 November), keep path (21 November)
PAGES = {
    "w19": "https://www.stepsecurity.io/blog/chaindrop-npm-worm",
    "w10": "https://snyk.io/blog/mini-shai-hulud-antv-npm-supply-chain-attack/",
    "w16": "https://unit42.paloaltonetworks.com/npm-supply-chain-attack/",
    "w14": "https://www.aikido.dev/blog/tensorlake-npm-package-compromised",
    "w13": "https://www.elastic.co/security-labs/shai-hulud-chaindrop-npm-supply-chain",
    "w07": "https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/",
}
log = open(os.path.join(HERE, "web", "log.psv"), "a")
if log.tell() == 0:
    log.write("file|url|status|read_utc|bytes|sha256_received|robots\n")
for k, url in PAGES.items():
    ok, info = robots_check(url)
    allowed = ("%s; group %s; rule %s" % (info.get("reason"), info.get("decided_by", ""), info.get("rule", ""))).replace("|", "/")
    if not ok:
        log.write("%s|%s|not fetched|%s|0||%s\n" % (k, url, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), allowed)); continue
    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60)
        body, st, final, hdrs = r.read(), r.status, r.geturl() or url, r.headers
    except urllib.error.HTTPError as e:
        body, st, final, hdrs = e.read(), e.code, e.geturl() or url, e.headers
    except Exception as e:
        body, st, final, hdrs = b"", "error:" + type(e).__name__, url, None
    sha = hashlib.sha256(body).hexdigest()
    kept, why = save_body(os.path.join(HERE, "web", k + ".html.gz"), body, final, hdrs)
    if not kept:
        allowed += ("; body_kept: no: " + why).replace("|", "/")
    log.write("%s|%s|%s|%s|%d|%s|%s\n" % (k, url, st, t, len(body), sha, allowed))
    log.flush()
    time.sleep(1)
