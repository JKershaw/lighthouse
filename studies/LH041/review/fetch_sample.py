"""R-0057: re-read a sample of LH041's vendor pages live, keeping the bytes
gzipped (emails redacted) with URL, UTC time, status and sha256 of bytes received.
Checks robots.txt for each host first. Run from the repository root:
    python3 -I studies/LH041/review/fetch_sample.py
"""
import gzip, hashlib, os, sys, time, urllib.request, urllib.error, urllib.robotparser
from datetime import datetime, timezone
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from redact_emails import redact_bytes  # noqa: E402
UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
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
    host = url.split("/")[2]
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request("https://%s/robots.txt" % host, headers={"User-Agent": UA})
        rp.parse(urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace").splitlines())
        allowed = rp.can_fetch(UA, url)
    except Exception as e:
        allowed = "robots unread (%s)" % type(e).__name__
    if allowed is False:
        log.write("%s|%s|not fetched|%s|0||disallowed\n" % (k, url, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))); continue
    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60)
        body, st = r.read(), r.status
    except urllib.error.HTTPError as e:
        body, st = e.read(), e.code
    except Exception as e:
        body, st = b"", "error:" + type(e).__name__
    sha = hashlib.sha256(body).hexdigest()
    gzip.open(os.path.join(HERE, "web", k + ".html.gz"), "wb").write(redact_bytes(body)[0])
    log.write("%s|%s|%s|%s|%d|%s|%s\n" % (k, url, st, t, len(body), sha, allowed))
    log.flush()
    time.sleep(1)
