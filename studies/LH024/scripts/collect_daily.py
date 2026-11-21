#!/usr/bin/env python3
"""Daily LH024 read: the selection file for one UTC date, once, preserving primary bytes and media metadata.
A dated copy of collect.py, which stays as it read 22 October; usage: collect_daily.py YYYY-MM-DD.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body (which withholds email addresses, as before); where it may
not be kept no .raw is written, raw_retained is False and `error` ends "body_kept: no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH024/scripts/collect_daily.py`."""
import csv
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PANEL = {x['id']: x for x in json.loads((ROOT / 'panel.json').read_text())}
DATE = sys.argv[1]
datetime.strptime(DATE, '%Y-%m-%d')
SELECTED = json.loads((ROOT / ('selection-' + DATE + '.json')).read_text())
OUT = ROOT / ('data/snapshot-' + DATE)
OUT.mkdir(parents=True, exist_ok=False)
assert len(SELECTED) == 13 and sum(len(x['urls']) for x in SELECTED) <= 30
CAP = 512 * 1024


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.title = ''
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            k = a.get('property', a.get('name', '')).lower()
            if k in ('article:published_time', 'article:modified_time', 'date', 'datepublished',
                     'datemodified', 'og:title', 'author'):
                self.meta.setdefault(k, a.get('content', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.meta['canonical'] = a.get('href', '')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def fetch(item):
    key, url, role = item
    started = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    status, data, hdr, final, error = '', b'', {}, '', ''
    try:
        request = urllib.request.Request(url, headers={'User-Agent': UA,
                                                       'Accept': 'text/html,application/xhtml+xml'})
        with urlopen(request, timeout=22) as response:
            status, hdr, final = response.status, dict(response.headers), response.url
            data = response.read(CAP + 1)
    except urllib.error.HTTPError as exc:
        status, hdr, final, data = exc.code, dict(exc.headers), exc.url, exc.read(min(CAP + 1, 4096))
        error = 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    truncated = len(data) > CAP
    data = data[:CAP]
    if truncated:
        error = 'response exceeded 512 KiB; SHA-256 is of retained prefix only'
    metadata = Metadata()
    try:
        metadata.feed(data.decode('utf-8', 'replace'))
    except Exception:
        pass
    kept = role != 'media'
    if kept:
        kept, why = save_body(OUT / (key + '.raw'), data, final or url, hdr)
        if not kept:
            error = (error + '; ' if error else '') + 'body_kept: no: ' + why
    row = dict(observed_at_utc=started, key=key, role=role, url=url, final_url=final,
               status=status, bytes_retained=len(data), sha256_retained=hashlib.sha256(data).hexdigest(),
               raw_retained=kept, title=html.unescape(metadata.meta.get('og:title') or metadata.title.strip())[:250],
               canonical=metadata.meta.get('canonical', ''), published=metadata.meta.get('article:published_time', metadata.meta.get('datepublished', metadata.meta.get('date', ''))),
               modified=metadata.meta.get('article:modified_time', metadata.meta.get('datemodified', '')),
               author=metadata.meta.get('author', ''), http_date=hdr.get('Date', ''),
               last_modified=hdr.get('Last-Modified', ''), etag=hdr.get('ETag', ''), error=error)
    return row


items = [(f"{x['id']}_{i}", url, PANEL[x['id']]['role']) for x in SELECTED for i, url in enumerate(x['urls'])]
with ThreadPoolExecutor(max_workers=4) as executor:
    rows = list(executor.map(fetch, items))
assert sum(int(x['bytes_retained']) for x in rows) <= 12 * 1024 * 1024
with (OUT / 'read_log.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, rows[0].keys(), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print(json.dumps({'attempts': len(rows), 'status': {str(s): sum(x['status'] == s for x in rows)
             for s in {x['status'] for x in rows}}, 'retained_bytes': sum(x['bytes_retained'] for x in rows)}, sort_keys=True))
