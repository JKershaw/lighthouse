#!/usr/bin/env python3
"""R-0035 evidence review: parse LH031's retained CISA KEV feed bodies with the
standard library only and print what the reviewed surfaces claim about them.

Usage: python3 -I studies/LH031/review/feed_check.py  (from the repository root)
Reads only retained bytes under studies/LH031/data/. Makes no network request.
"""
import datetime as dt
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "studies" / "LH031" / "data"
CVES = ["CVE-2026-109618", "CVE-2026-109619", "CVE-2026-115560"]
FIELDS = ["cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
          "dueDate", "forensicTriage", "knownRansomwareCampaignUse", "shortDescription",
          "requiredAction", "notes", "cwes"]


def load(read_dir):
    raw = (read_dir / "feed.raw").read_bytes()
    log = json.loads((read_dir / "read_log.json").read_text())
    return raw, log


def summarise(read_dir):
    raw, log = load(read_dir)
    sha = hashlib.sha256(raw).hexdigest()
    feed = json.loads(raw)
    vulns = feed.get("vulnerabilities", [])
    ids = [v.get("cveID") for v in vulns]
    print(f"== {read_dir.name}")
    for r in log:
        print(f"  read_log: start {r['start_utc']} status {r['status']} bytes {r['bytes']} sha256 {r['sha256'][:16]}...")
        print(f"  file:     bytes {len(raw)} sha256 {sha[:16]}... "
              f"(log matches: {r['bytes'] == len(raw) and r['sha256'] == sha})")
    print(f"  top-level keys: {sorted(feed.keys())}")
    print(f"  title: {feed.get('title')!r}")
    print(f"  catalogVersion {feed.get('catalogVersion')!r} dateReleased {feed.get('dateReleased')!r} "
          f"count field {feed.get('count')} entries parsed {len(vulns)} "
          f"(count == len: {feed.get('count') == len(vulns)}) duplicate ids {len(ids) - len(set(ids))}")
    for c in CVES:
        present = c in ids
        in_bytes = c.encode() in raw
        print(f"  {c}: parsed entry present {present}; byte string present {in_bytes}")
    return feed, ids, raw


def main():
    print("Retained reads, in order:")
    reads = sorted(DATA.glob("read-*"))
    for d in reads:
        raw, log = load(d)
        feed = json.loads(raw)
        ids = {v.get("cveID") for v in feed["vulnerabilities"]}
        hit = [c for c in CVES if c in ids]
        print(f"  {d.name}: start {log[0]['start_utc']} version {feed['catalogVersion']} "
              f"released {feed['dateReleased']} count {feed['count']} listed {hit or 'none'}")

    print()
    print("Previous read (should lack all three):")
    prev_feed, prev_ids, prev_raw = summarise(DATA / "read-2026-10-26T1830Z")
    print()
    print("Read under review (should hold the first two, lack the third):")
    feed, ids, raw = summarise(DATA / "read-2026-10-27T0633Z")

    print()
    print("Fields of the two entries, from the parsed 27 October body:")
    by_id = {v["cveID"]: v for v in feed["vulnerabilities"]}
    for c in CVES[:2]:
        v = by_id[c]
        print(f"  {c}:")
        for f in FIELDS:
            print(f"    {f}: {v.get(f)!r}")
        extra = sorted(set(v.keys()) - set(FIELDS))
        print(f"    (other fields: {extra})")
    a, b = by_id[CVES[0]], by_id[CVES[1]]
    same = [f for f in FIELDS if a.get(f) == b.get(f)]
    print(f"  fields identical across the two entries: {same}")

    print()
    print("Entries added in the 27 October body that the 26 October 18:34 body lacked:")
    added = [v for v in feed["vulnerabilities"] if v["cveID"] not in prev_ids]
    for v in added:
        print(f"  {v['cveID']} {v['vendorProject']} / {v['product']} dateAdded {v['dateAdded']} dueDate {v['dueDate']}")
    removed = [c for c in prev_ids if c not in ids]
    print(f"  removed: {removed or 'none'}; count difference {feed['count'] - prev_feed['count']}")
    others = [v for v in feed["vulnerabilities"] if v["dateAdded"] == "2026-10-26"]
    print(f"  entries with dateAdded 2026-10-26: {[v['cveID'] for v in others]}")

    print()
    print("Date arithmetic (calendar dates only; dateAdded is a day):")
    php_fix = dt.date(2026, 10, 21)
    added_d = dt.date.fromisoformat(a["dateAdded"])
    due_d = dt.date.fromisoformat(a["dueDate"])
    print(f"  PHP fixes 2026-10-21 -> dateAdded {added_d}: {(added_d - php_fix).days} days")
    print(f"  dateAdded {added_d} -> dueDate {due_d}: {(due_d - added_d).days} days")
    rel = dt.datetime.fromisoformat(feed["dateReleased"].replace("Z", "+00:00"))
    print(f"  dateReleased parsed: {rel.isoformat()} (UTC day {rel.date()})")
    prev_start = dt.datetime.fromisoformat(json.loads((DATA / 'read-2026-10-26T1830Z' / 'read_log.json').read_text())[0]['start_utc'])
    this_start = dt.datetime.fromisoformat(json.loads((DATA / 'read-2026-10-27T0633Z' / 'read_log.json').read_text())[0]['start_utc'])
    print(f"  previous read start {prev_start.isoformat()} < dateReleased {rel.isoformat()} < this read start {this_start.isoformat()}: "
          f"{prev_start < rel < this_start}")

    print()
    print("What the feed itself says about who the directive binds (top-level text and the entries' own text):")
    for k in ("title", "notes", "description"):
        if k in feed:
            print(f"  feed.{k}: {feed[k]!r}")
    for word in ("federal", "Federal", "agencies", "agency", "binding", "BOD", "directive", "Directive"):
        n = raw.count(word.encode())
        print(f"  byte count of {word!r} in the 27 October body: {n}")
    for c in CVES[:2]:
        v = by_id[c]
        text = " ".join(str(v.get(f, "")) for f in ("requiredAction", "notes", "shortDescription"))
        hits = [w for w in ("federal", "Federal", "agenc", "civilian", "FCEB") if w in text]
        print(f"  {c} entry text mentions: {hits or 'none of federal/agenc/civilian/FCEB'}")

    print()
    print("Compare the stored extract (result.json) with this parse:")
    stored = json.loads((DATA / "read-2026-10-27T0633Z" / "result.json").read_text())
    ok = (stored["catalogVersion"] == feed["catalogVersion"] and stored["dateReleased"] == feed["dateReleased"]
          and stored["count"] == feed["count"] and stored["entries"][CVES[2]] is None
          and all(stored["entries"][c] == by_id[c] for c in CVES[:2]))
    print(f"  extract matches parse: {ok}")


if __name__ == "__main__":
    main()
