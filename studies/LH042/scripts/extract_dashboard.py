#!/usr/bin/env python3
"""LH042: append one row per recurring read to data/dashboard_reads.csv.

Usage: python3 -I studies/LH042/scripts/extract_dashboard.py data/<label>

Reads <label>/readlog.csv and the saved body of https://declawed.io/api/stats.
Fields kept (fixed in the brief before any value was read): last_sync (the
dashboard's own clock), total_hits (the page's "Total Instances", every
instance discovered so far, a cumulative count), active_count (the page's
"Active"), inactive = total_hits - active_count (the page's own arithmetic),
variant_counts (openclaw, moltbot, clawdbot), unique_ips, vulnerable_count,
rce_count; plus the HTTP status of Shadowserver's dashboard. No other field is
analysed.
"""
import csv, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "data" / "dashboard_reads.csv"
FIELDS = ["label", "declawed_status", "fetched_utc", "last_sync", "total_hits", "active_count",
          "inactive", "openclaw", "moltbot", "clawdbot", "unique_ips", "vulnerable_count",
          "rce_count", "body_sha256", "shadowserver_status", "shadowserver_error"]


def main(d):
    d = pathlib.Path(d)
    if not d.is_absolute():
        d = HERE.parent / d
    log = list(csv.DictReader(open(d / "readlog.csv")))
    row = {k: "" for k in FIELDS}
    row["label"] = d.name
    for r in log:
        if r["url"] == "https://declawed.io/api/stats":
            row["declawed_status"] = r["http_status"] or r["error"]
            row["fetched_utc"] = r["start_utc"]
            row["body_sha256"] = r["sha256_saved"]
            if r["http_status"] == "200":
                s = json.loads((d / f"{int(r['n']):03d}.body").read_text())
                for k in ["last_sync", "total_hits", "active_count", "unique_ips", "vulnerable_count", "rce_count"]:
                    row[k] = s.get(k, "")
                if isinstance(s.get("total_hits"), int) and isinstance(s.get("active_count"), int):
                    row["inactive"] = s["total_hits"] - s["active_count"]
                vc = s.get("variant_counts") or {}
                for k in ["openclaw", "moltbot", "clawdbot"]:
                    row[k] = vc.get(k, "")
        if r["url"].startswith("https://dashboard.shadowserver.org"):
            row["shadowserver_status"] = r["http_status"]
            row["shadowserver_error"] = r["error"]
    new = not OUT.exists()
    with open(OUT, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(row)


if __name__ == "__main__":
    main(sys.argv[1])
