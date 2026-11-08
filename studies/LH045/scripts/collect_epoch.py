#!/usr/bin/env python3
"""LH045 part B: weekly capture of Epoch AI's AI data-centre records, under brief.md (protocol 0.1, 8 November 2026).

Checks robots.txt first and skips any URL it disallows. One GET per URL, about one a
second; bodies kept raw under data/epoch/raw-<label>/ with readlog.csv (name, url, UTC
start, status, content type, size, SHA-256, note). Then derives updates.csv from the
update log page's embedded data. Idempotent: a label already held is not fetched again;
--derive-only rebuilds the derived table from the kept bodies.
Epoch AI's data is CC BY 4.0: credit Epoch AI, 'AI data centers', published online at epoch.ai.
Usage: python3 -I studies/LH045/scripts/collect_epoch.py --read 2026-11-08T1930Z
"""
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from redact_emails import redact_bytes  # noqa: E402
import argparse, csv, datetime, gzip, hashlib, html, json, os, re, sys, time
import urllib.error, urllib.request, urllib.robotparser

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
ROBOTS = "https://epoch.ai/robots.txt"
URLS = [
    ("hub", "https://epoch.ai/data/data-centers"),
    ("updates", "https://epoch.ai/data/ai-data-centers/updates"),
    ("documentation", "https://epoch.ai/data/data-centers-documentation"),
    ("all-zip", "https://epoch.ai/data/data_centers/data_centers.zip"),
    ("data-centers-csv", "https://epoch.ai/data/data_centers/data_centers.csv"),
    ("timelines-csv", "https://epoch.ai/data/data_centers/data_center_timelines.csv"),
    ("chip-quantities-csv", "https://epoch.ai/data/data_centers/data_centers_chip_quantities.csv"),
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read(64 << 20), ""
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Content-Type", ""), e.read() or b"", "http error"
        except Exception as e:  # one retry after a connection reset, as the brief allows
            if attempt == 2 or "reset" not in repr(e).lower():
                return "error", "", repr(e).encode(), "no response"
            time.sleep(5)

def unzip_body(b):
    return gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b

def derive(d):
    p = os.path.join(d, "updates.body")
    if not os.path.exists(p):
        return "no updates body"
    s = unzip_body(open(p, "rb").read()).decode("utf-8", "replace")
    props = re.findall(r'<astro-island[^>]*props="([^"]*)"', s)
    if not props:
        return "partial: no embedded data found"
    raw = html.unescape(max(props, key=len))
    try:
        data = json.loads(raw)
    except ValueError:
        return "partial: embedded data not JSON"

    # Astro serialises values as [type, value]; type 0 is plain, 1 is an array.
    def un(v):
        if isinstance(v, list) and len(v) == 2 and isinstance(v[0], int):
            t, x = v
            if t == 1:
                return [un(i) for i in x]
            return un(x)
        if isinstance(v, dict):
            return {k: un(x) for k, x in v.items()}
        return v

    data = un(data)
    rows = []

    def walk(o):
        if isinstance(o, dict):
            if "date" in o and "sections" in o:
                for sec in o.get("sections") or []:
                    for it in sec.get("items") or []:
                        ch = it.get("change")
                        changes = ch if isinstance(ch, list) else [ch]
                        extra = it.get("newlyOperational") or it.get("note") or ""
                        for c in changes:
                            rows.append([o.get("date"), sec.get("type", ""), it.get("name", ""), it.get("url", ""),
                                         c if c is not None else "", extra])
                return
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(data)
    with open(os.path.join(d, "updates.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "section", "site", "url", "change", "note"])
        w.writerows(rows)
    dates = sorted({r[0] for r in rows if r[0]})
    return f"updates.csv: {len(rows)} rows, {len(dates)} dates, {dates[0] if dates else '-'} to {dates[-1] if dates else '-'}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True, help="UTC label YYYY-MM-DDTHHMMZ, the minute the collector starts")
    ap.add_argument("--derive-only", action="store_true")
    a = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d{4}Z", a.read):
        sys.exit("label must look like 2026-11-08T1930Z")
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.normpath(os.path.join(here, "..", "data", "epoch", "raw-" + a.read))
    if a.derive_only:
        print(derive(d)); return
    if os.path.exists(d):
        print("already held:", d); return
    os.makedirs(d)
    log = open(os.path.join(d, "readlog.csv"), "w", newline="")
    w = csv.writer(log)
    w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256", "note"])
    t = now(); st, ct, body, note = get(ROBOTS)
    open(os.path.join(d, "robots.body"), "wb").write(redact_bytes(body)[0])
    w.writerow(["robots", ROBOTS, t, st, ct, len(body), hashlib.sha256(body).hexdigest(), note])
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "replace").splitlines() if st == 200 else [])
    for name, url in URLS:
        time.sleep(1)
        t = now()
        if st == 200 and not rp.can_fetch(UA, url):
            w.writerow([name, url, t, "skipped", "", 0, "", "disallowed by robots.txt"]); print(name, "skipped (robots)"); continue
        s2, ct, body, note = get(url)
        open(os.path.join(d, name + ".body"), "wb").write(redact_bytes(body)[0])
        w.writerow([name, url, t, s2, ct, len(body), hashlib.sha256(body).hexdigest(), note])
        log.flush()
        print(name, s2, len(body))
    log.close()
    print(derive(d))

if __name__ == "__main__":
    main()
