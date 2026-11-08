"""Fetch documentation pages once each, retaining body, status and hash.
Usage: python3 -I fetch_sources.py <outdir> <name> <url> [<name> <url> ...]
Appends to <outdir>/fetch-log.tsv: utc, status, bytes, sha256 (of bytes received), url, file.
Bodies are saved with email addresses withheld (scripts/redact_emails.py)."""
import hashlib, os, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from redact_emails import redact_bytes
UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
out = sys.argv[1]; args = sys.argv[2:]
os.makedirs(out, exist_ok=True)
log = open(os.path.join(out, "fetch-log.tsv"), "a")
for name, url in zip(args[0::2], args[1::2]):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read()
    except Exception as e:
        status, body = "ERR:" + type(e).__name__, b""
    h = hashlib.sha256(body).hexdigest()
    red, n = redact_bytes(body)
    with open(os.path.join(out, name), "wb") as f:
        f.write(red)
    log.write(f"{t}\t{status}\t{len(body)}\t{h}\t{url}\t{name}\n"); log.flush()
    print(t, status, len(body), url)
    time.sleep(2)
