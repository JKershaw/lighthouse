#!/usr/bin/env python3
"""One gated GET for LH038's SUSE clocks read (brief, amendment of 20 November 2026).

  LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH038/scripts/suse_clocks.py <read dir> <name> <url>

Asks scripts/robots_gate.py (through scripts/lh_fetch.py) immediately before the fetch; a refused URL
is logged "not fetched" with the deciding group and rule. Reads at most 4 MiB, withholds email
addresses with redact_bytes before saving, keeps the body gzipped as <read dir>/<name>.raw.gz (through lh_fetch.save_body: not where robots.txt
refuses `*`, an AI-training or archiving crawler, or the page reserves itself, the keeper's decision of
21 November 2026; the note then says "body_kept: no: <reason>") and
appends a row to <read dir>/readlog.csv: URL, UTC start, status, Last-Modified, Date, length and the
SHA-256 of the bytes received. No retry. Refuses to run once the read has used 30 GETs, counting one
robots.txt per host as the gate fetches it. The driver chooses each URL from the indexes as the
amendment says; this script follows no link itself.
"""
import csv
import datetime
import hashlib
import os
import sys
import urllib.error
from urllib.parse import urlsplit

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
import urllib.request  # noqa: E402
from lh_fetch import urlopen, NotFetched, redact_bytes, UA, save_body  # noqa: E402

CEILING = 30
LIMIT = 4 * 1024 * 1024
FIELDS = ["name", "url", "utc_start", "status", "last_modified", "date", "bytes", "sha256", "emails_withheld", "note"]


def main(d, name, url):
    os.makedirs(d, exist_ok=True)
    log = os.path.join(d, "readlog.csv")
    rows = list(csv.DictReader(open(log))) if os.path.exists(log) else []
    if any(r["name"] == name for r in rows):
        sys.exit("already read: %s" % name)
    hosts = {urlsplit(r["url"]).hostname for r in rows} | {urlsplit(url).hostname}
    used = len(rows) + 1 + len(hosts)  # content GETs including this one, plus one robots.txt per host
    if used > CEILING:
        sys.exit("ceiling: this GET would make %d of %d" % (used, CEILING))
    start = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = dict(name=name, url=url, utc_start=start, status="", last_modified="", date="", bytes="",
               sha256="", emails_withheld="", note="")
    body, final, hdrs = None, url, None
    try:
        with urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60, check_redirects=True) as r:
            body, final, hdrs = r.read(LIMIT + 1), r.geturl() or url, r.headers
            row.update(status=r.status, last_modified=r.headers.get("Last-Modified", ""),
                       date=r.headers.get("Date", ""))
    except NotFetched as e:
        row.update(status="not fetched", note=str(e))
    except urllib.error.HTTPError as e:
        row.update(status=e.code, note="HTTP error; wall recorded, not retried")
    except Exception as e:  # noqa: BLE001
        row.update(status="error", note="%s: %s" % (type(e).__name__, e))
    if body is not None:
        if len(body) > LIMIT:
            body = body[:LIMIT]
            row["note"] = "cut at 4 MiB"
        row.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        row["emails_withheld"] = redact_bytes(body)[1]
        kept, why = save_body(os.path.join(d, name + ".raw.gz"), body, final, hdrs)  # the keeper, 21 November 2026
        if not kept:  # nothing kept where robots.txt or the page refuses it
            row["note"] = (row["note"] + "; " if row["note"] else "") + "body_kept: no: " + why
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow(row)
    print(row["status"], row["bytes"], row["last_modified"], row["note"], "(GETs used: %d)" % used)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
