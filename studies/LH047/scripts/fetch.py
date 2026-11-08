"""LH047's own collector. Reads each URL once with an honest User-Agent, after reading the
host's whole robots.txt and evaluating it under RFC 9309 (robots9309.py) for the token
Lighthouse-research and, as LH047's own stricter rule, for every Anthropic token in
ANTHROPIC_TOKENS: a URL any of them disallows is not fetched. A robots.txt answering 5xx
or not at all means complete disallow (RFC 9309 2.3.1.4). Redirects of robots.txt are
followed up to five hops (2.3.1.2); page redirects are followed by urllib (counted as one
logged request, final URL recorded). Refuses any host in data/audited-hosts.txt except for
its /robots.txt (the brief: no other request to an audited site).

Usage: python3 -I studies/LH047/scripts/fetch.py <label> <url-file>
Writes studies/LH047/data/reads/<label>/NNN.body (email addresses withheld), robots copies,
and readlog.csv (n, url, utc, robots_verdict, status, bytes, sha256 of bytes received,
final_url, content_type, note). Two seconds between requests.
"""
import csv, hashlib, os, sys, time, ssl, urllib.request, urllib.error
from datetime import datetime, timezone
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'scripts'))
import robots9309  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402

UA = 'Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)'
TOKEN = 'Lighthouse-research'
ANTHROPIC_TOKENS = ['anthropic-ai', 'ClaudeBot', 'Claude-Web', 'Claude-User', 'Claude-SearchBot', 'Claude-Code', 'Claude-Agent']
CA = '/root/.ccr/ca-bundle.crt'
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
DATA = os.path.join(HERE, '..', 'data')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def get(url, follow=True, cap=30_000_000):
    handlers = [urllib.request.HTTPSHandler(context=CTX)]
    if not follow:
        handlers.append(NoRedirect())
    op = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    try:
        with op.open(req, timeout=40) as r:
            return r.status, r.headers, r.read(cap), r.geturl(), ''
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read(cap) if e.fp else b'', url, ''
    except Exception as e:
        return None, None, b'', url, '%s: %s' % (type(e).__name__, e)


def audited():
    p = os.path.join(DATA, 'audited-hosts.txt')
    if not os.path.exists(p):
        return set()
    return {l.strip() for l in open(p) if l.strip() and not l.startswith('#')}


def robots_for(scheme_host, outdir, log):
    url = scheme_host + '/robots.txt'
    for hop in range(6):
        t = now()
        st, hd, body, final, err = get(url, follow=False)
        safe = urlsplit(url).netloc.replace(':', '_')
        with open(os.path.join(outdir, 'robots-%s-%d.txt' % (safe, hop)), 'wb') as f:
            f.write(redact_bytes(body)[0])
        log.writerow(['', url, t, 'robots.txt', st or err, len(body), hashlib.sha256(body).hexdigest(), url,
                      (hd.get('content-type') if hd else ''), 'robots hop %d' % hop])
        time.sleep(2)
        if st in (301, 302, 303, 307, 308) and hd and hd.get('location'):
            url = urllib.parse.urljoin(url, hd.get('location'))
            continue
        if st is None or st >= 500:
            return 'disallow-all', None
        if 400 <= st < 500:
            return 'allow-all', None
        if 200 <= st < 300:
            return 'parsed', body.decode('utf-8', 'replace')
        return 'disallow-all', None
    return 'allow-all', None  # more than five redirects: RFC 9309 2.3.1.2 allows treating as unavailable


def main(label, urlfile):
    outdir = os.path.join(DATA, 'reads', label)
    os.makedirs(outdir, exist_ok=True)
    aud = audited()
    urls = [l.strip() for l in open(urlfile) if l.strip() and not l.startswith('#')]
    cache = {}
    with open(os.path.join(outdir, 'readlog.csv'), 'a', newline='') as f:
        log = csv.writer(f)
        if f.tell() == 0:
            log.writerow(['n', 'url', 'utc', 'robots_verdict', 'status', 'bytes', 'sha256_received', 'final_url', 'content_type', 'note'])
        for n, url in enumerate(urls, 1):
            u = urlsplit(url)
            if u.hostname in aud:
                log.writerow([n, url, now(), 'not sent: audited host', '', '', '', '', '', '']); continue
            sh = '%s://%s' % (u.scheme, u.netloc)
            if sh not in cache:
                cache[sh] = robots_for(sh, outdir, log)
            state, text = cache[sh]
            path = (u.path or '/') + ('?' + u.query if u.query else '')
            verdict = 'allowed'
            if state == 'disallow-all':
                verdict = 'disallowed (robots.txt unreachable)'
            elif state == 'parsed':
                r = robots9309.evaluate(text, TOKEN, path)
                if not r['allowed']:
                    verdict = 'disallowed for %s by %s' % (TOKEN, r['rule'])
                else:
                    g = robots9309.parse(text)
                    for tok in ANTHROPIC_TOKENS:
                        ap, how = robots9309.groups_for(g, tok, fallback=False)
                        if how == 'token' and not robots9309.decide(ap, path)[0]:
                            verdict = 'disallowed for %s' % tok
                            break
            if verdict != 'allowed':
                log.writerow([n, url, now(), verdict, '', '', '', '', '', 'not sent']); continue
            t = now()
            st, hd, body, final, err = get(url)
            with open(os.path.join(outdir, '%03d.body' % n), 'wb') as b:
                b.write(redact_bytes(body)[0])
            log.writerow([n, url, t, verdict, st or err, len(body), hashlib.sha256(body).hexdigest(), final,
                          (hd.get('content-type') if hd else ''), ''])
            print(n, st or err, len(body), url)
            time.sleep(2)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
