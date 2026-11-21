"""Fetch documentation pages once each, retaining body, status and hash.
Usage: python3 -I fetch_sources.py <outdir> <name> <url> [<name> <url> ...]
Appends to <outdir>/fetch-log.tsv: utc, status, bytes, sha256 (of bytes received), url, file, and from
21 November 2026 body_kept (empty, or "no: <reason>").
Bodies are saved with email addresses withheld, through scripts/lh_fetch.py's save_body, which keeps
nothing where robots.txt refuses `*`, an AI-training or archiving crawler, or the page reserves itself
(the keeper, 21 November 2026). From 21 November 2026 (review R-0111) each fetch is gated by scripts/lh_fetch.py's
urlopen under the keeper's robots.txt rule of 8 November 2026, with Lighthouse's User-Agent, and save_body
decides from the same gate's copy of robots.txt, so robots.txt is read once per host; a refused URL is logged
"not fetched". Before, this script read no robots.txt at all."""
import hashlib, os, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from lh_fetch import save_body, urlopen, NotFetched, UA  # noqa: E402
out = sys.argv[1]; args = sys.argv[2:]
os.makedirs(out, exist_ok=True)
log = open(os.path.join(out, "fetch-log.tsv"), "a")
for name, url in zip(args[0::2], args[1::2]):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urlopen(req, timeout=60, check_redirects=True) as r:
            status, body, final, hdrs = r.status, r.read(), r.geturl() or url, r.headers
    except urllib.error.HTTPError as e:
        status, body, final, hdrs = e.code, e.read(), url, e.headers
    except NotFetched as e:
        log.write(f"{t}\tnot fetched\t0\t\t{url}\t{name}\t{e}\n"); log.flush(); print(t, "not fetched", url); continue
    except Exception as e:
        status, body, final, hdrs = "ERR:" + type(e).__name__, b"", url, None
    h = hashlib.sha256(body).hexdigest()
    kept, why = save_body(os.path.join(out, name), body, final, hdrs)
    log.write(f"{t}\t{status}\t{len(body)}\t{h}\t{url}\t{name}\t{'' if kept else 'no: ' + why}\n"); log.flush()
    print(t, status, len(body), url)
    time.sleep(2)
