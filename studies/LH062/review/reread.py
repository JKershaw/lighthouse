#!/usr/bin/env python3
"""LH062 evidence review (R-0162), 27 November 2026: gated one-off rereads of URLs the fetchlog lists.

One GET per URL through scripts/lh_fetch.py, access='oneoff', check_redirects=True, under
LIGHTHOUSE_PROVIDER=anthropic. No body is kept in the repository: bytes and a text extraction go to a
working folder outside it (--work, the reviewer's scratchpad). Each attempt is logged in
studies/LH062/review/rereads.csv with URL, UTC time, status and SHA-256.
Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH062/review/reread.py --work <dir> --id <id> --url <url>
"""
import argparse, csv, datetime, hashlib, html, os, re, subprocess, sys, urllib.error, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from lh_fetch import urlopen, UA, NotFetched  # noqa: E402
LOG = os.path.join(HERE, "rereads.csv")
F = ["utc", "id", "url", "final_url", "status", "bytes", "sha256", "outcome", "note"]

def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=F)
        if new: w.writeheader()
        w.writerow({k: row.get(k, "") for k in F})

ap = argparse.ArgumentParser(); ap.add_argument("--work", required=True); ap.add_argument("--id", required=True); ap.add_argument("--url", required=True)
a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
try:
    req = urllib.request.Request(a.url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=90, check_redirects=True, access="oneoff") as r:
        status, final, body = r.status, r.geturl() or a.url, r.read(64 << 20)
except NotFetched as e:
    log(dict(utc=t, id=a.id, url=a.url, outcome="robots refusal (not requested)", note=str(e)[:200])); print("REFUSED", e); sys.exit()
except urllib.error.HTTPError as e:
    log(dict(utc=t, id=a.id, url=a.url, status=e.code, outcome="wall")); print("HTTP", e.code); sys.exit()
sha = hashlib.sha256(body).hexdigest()
if body[:5] == b"%PDF-":
    text = subprocess.run(["pdftotext", "-layout", "-", "-"], input=body, capture_output=True, timeout=300).stdout.decode("utf-8", "replace")
else:
    t2 = body.decode("utf-8", "replace"); t2 = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t2)
    text = html.unescape(re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>", "\n", t2))))
open(os.path.join(a.work, a.id + ".txt"), "w").write(text)
log(dict(utc=t, id=a.id, url=a.url, final_url=final, status=status, bytes=len(body), sha256=sha, outcome="ok",
         note="no body kept; text extracted to the reviewer's scratchpad only; %d characters" % len(text)))
print(status, len(body), sha)
