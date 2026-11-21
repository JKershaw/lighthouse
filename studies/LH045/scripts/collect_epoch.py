#!/usr/bin/env python3
"""LH045 part B: weekly capture of Epoch AI's AI data-centre records, under brief.md (protocol 0.1, 8 November 2026).

Checks robots.txt first, through scripts/robots_gate.py (from 21 November 2026), and skips any URL it refuses. One GET per URL, about one a
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
from lh_fetch import save_body, UA  # noqa: E402  what may be kept (the keeper, 21 November 2026); Lighthouse's UA
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule of 8 November 2026
import argparse, csv, datetime, gzip, hashlib, html, json, os, re, sys, time
import urllib.error, urllib.request

# Brief amendment of 21 November 2026 (review R-0111): robots.txt is read once per run by scripts/robots_gate.py
# with Lighthouse's User-Agent (was "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)" and
# urllib.robotparser); a URL it refuses, or whose robots.txt answers 5xx or cannot be read, is not fetched.
GATE = RobotsGate(UA)
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
                return r.status, r.headers.get("Content-Type", ""), r.read(64 << 20), "", r.geturl() or url, r.headers
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Content-Type", ""), e.read() or b"", "http error", url, e.headers
        except Exception as e:  # one retry after a connection reset, as the brief allows
            if attempt == 2 or "reset" not in repr(e).lower():
                return "error", "", repr(e).encode(), "no response", url, None
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
    w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256", "note", "body_kept"])
    t = now(); rec = GATE._robots(ROBOTS)  # the gate's one read of robots.txt, kept and logged as before
    body = rec.get("body") or b""
    open(os.path.join(d, "robots.body"), "wb").write(redact_bytes(body)[0])
    w.writerow(["robots", ROBOTS, t, rec.get("status"), "", len(body), rec.get("sha256", ""),
                "read by scripts/robots_gate.py" + ("; " + rec["error"] if rec.get("error") else ""), ""])
    for name, url in URLS:
        time.sleep(1)
        t = now()
        ok, info = GATE.check(url)
        if not ok:  # not fetched: a missing reading, never a negative
            w.writerow([name, url, t, "not fetched", "", 0, "", "%s (robots %s, status %s, group %s, rule %s)" % (
                info.get("reason"), info.get("robots_url"), info.get("robots_status"), info.get("decided_by", ""),
                info.get("rule", "")), ""]); print(name, "not fetched (robots)"); continue
        s2, ct, body, note, final, hdrs = get(url)
        kept, why = save_body(os.path.join(d, name + ".body"), body, final, hdrs, gate=GATE)  # the keeper, 21 November 2026
        w.writerow([name, url, t, s2, ct, len(body), hashlib.sha256(body).hexdigest(), note, "" if kept else "no: " + why])
        log.flush()
        print(name, s2, len(body))
    log.close()
    print(derive(d))

if __name__ == "__main__":
    main()
