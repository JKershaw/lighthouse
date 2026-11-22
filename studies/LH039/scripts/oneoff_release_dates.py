#!/usr/bin/env python3
"""LH039, after collection stopped: one-off reads for the release dates of 7.1.5, 7.1.6, 7.0.9 and 6.9.12.

Written for the record (version 1.0), 22 November 2026. Supply metadata only (brief, E3 and measure 5):
whether and when WordPress published a later release on 7.1, 7.0 or 6.9. It reads no outcome and changes
no measured share. Each URL is read once, through scripts/lh_fetch.py with access='oneoff' (the keeper,
21 November 2026); a URL robots.txt refuses is not requested and is logged "NotFetched". A body is saved
only through save_body (keep_decision); where it may not be kept, a derived file (write_derived) holds
URL, time, status, size, SHA-256 and the facts used. Nothing downloaded is executed; the bodies are parsed
as text with regular expressions only.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH039/scripts/oneoff_release_dates.py <label>
  e.g. label 2026-11-22T1530Z (the UTC minute the script starts); writes data/oneoff-<label>/.
  A name already held in that folder is skipped, so a rerun fetches nothing twice.
"""
import csv, datetime, hashlib, html, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from lh_fetch import urlopen, save_body, write_derived, UA, NotFetched  # noqa: E402

URLS = [
    # WordPress's release feed, the brief's named instrument for E0 and E3 (meta-2 in the daily reads of 7 and 8 November)
    ("feed", "https://wordpress.org/news/category/releases/feed/"),
    # WordPress's release archive page, a second view of release dates
    ("archive", "https://wordpress.org/download/releases/"),
]
WANT = ["7.1.4", "7.1.5", "7.1.6", "7.0.8", "7.0.9", "6.9.11", "6.9.12"]


def strip(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def facts_feed(body):
    """Each feed item whose title names a WordPress release: title, pubDate, and which watched releases its
    title or description names (from the text, no markup)."""
    t = body.decode("utf-8", "replace")
    out = []
    for item in re.findall(r"<item>(.*?)</item>", t, flags=re.S):
        title = re.search(r"<title>(.*?)</title>", item, flags=re.S)
        pub = re.search(r"<pubDate>(.*?)</pubDate>", item, flags=re.S)
        link = re.search(r"<link>(.*?)</link>", item, flags=re.S)
        title = strip(re.sub(r"<!\[CDATA\[|\]\]>", "", title.group(1))).strip() if title else ""
        txt = strip(re.sub(r"<!\[CDATA\[|\]\]>", "", item))
        named = [v for v in WANT if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", txt)]
        security = bool(re.search(r"security", txt, flags=re.I))
        out.append({"title": title, "pubDate": pub.group(1).strip() if pub else "",
                    "link": link.group(1).strip() if link else "", "watched_releases_named": named,
                    "mentions_security": security})
    return {"items": out[:15], "items_in_feed": len(out)}


def facts_archive(body):
    """For each watched release, the first short stretch of the page's text that begins with it (a table row:
    version, date, links), cut at the next release number."""
    s = strip(body.decode("utf-8", "replace"))
    out = {}
    for v in WANT:
        m = re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d]).{0,60}", s)
        out[v] = m.group(0)[:80].strip() if m else None
    return {"rows_by_release": out}


def main():
    label = sys.argv[1]
    out = os.path.join(HERE, "..", "data", "oneoff-" + label)
    os.makedirs(out, exist_ok=True)
    log = os.path.join(out, "readlog.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256", "body_kept"])
        for name, url in URLS:
            path = os.path.join(out, name + ".body")
            dpath = os.path.join(out, name + ".derived.json")
            npath = os.path.join(out, name + ".notfetched.txt")
            if any(os.path.exists(p) for p in (path, dpath, npath)):
                print("held", name); continue
            t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            try:
                with urlopen(req, timeout=60, check_redirects=True, access="oneoff") as r:
                    body = r.read(16 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
                    final, hdrs = r.geturl() or url, r.headers
            except NotFetched as e:
                open(npath, "w").write(str(e) + "\n")
                w.writerow([name, url, t, "NotFetched", "", 0, "", "no: not requested"]); f.flush()
                print(name, "NotFetched", e); continue
            except urllib.error.HTTPError as e:
                body = e.read(); status = e.code; ct = e.headers.get("Content-Type", ""); final, hdrs = e.geturl() or url, e.headers
            except Exception as e:  # Lighthouse's own note of a failure, not a page body
                open(npath, "w").write(repr(e) + "\n")
                w.writerow([name, url, t, "error", "", 0, "", "no: failed"]); f.flush()
                print(name, "error", e); continue
            sha = hashlib.sha256(body).hexdigest()
            facts = facts_feed(body) if name == "feed" else facts_archive(body)
            kept, why = save_body(path, body, final, hdrs, access="oneoff")
            if not kept:
                write_derived(dpath, url, why, facts, read_utc=t, final_url=final, http_status=status,
                              content_type=ct, bytes=len(body), sha256=sha,
                              used_for="LH039 record 1.0: release dates of 7.1.5, 7.1.6, 7.0.9, 6.9.12 (E3), after collection stopped")
            else:  # kept; the facts are written beside it too, so the record cites one small file either way
                json.dump({"url": url, "final_url": final, "read_utc": t, "http_status": status, "sha256": sha,
                           "body_kept": "yes: " + str(why), "extracted": facts},
                          open(os.path.join(out, name + ".facts.json"), "w"), indent=1, ensure_ascii=False)
            w.writerow([name, url, t, status, ct, len(body), sha, ("yes: " if kept else "no: ") + str(why)]); f.flush()
            print(name, status, ct, len(body), "kept" if kept else "not kept: " + str(why))
            time.sleep(2)


if __name__ == "__main__":
    main()
