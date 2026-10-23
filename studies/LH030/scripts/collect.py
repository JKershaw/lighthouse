#!/usr/bin/env python3
"""One LH030 read: every panel URL once, raw bytes up to 1 MiB, one read log per UTC read label."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label of this read, e.g. 2026-10-23T1730Z')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists; do not overwrite'
OUT.mkdir(parents=True)
targets = [('reference', 'php', 0, PANEL['reference']['php'][0])]
targets += [('records', key, 0, url) for key, url in PANEL['records'].items()]
targets += [('notices', key, i, url) for key, urls in PANEL['notices'].items() for i, url in enumerate(urls)]
assert len(targets) <= 20
rows = []
for group, key, index, url in targets:
    name = f'{key}_{index}'
    row = {'group': group, 'source': key, 'name': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        try:
            response = urlopen(request, timeout=25)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       last_modified=response.headers.get('Last-Modified', ''), bytes=len(body),
                       sha256=sha256(body).hexdigest())
            if len(body) <= 1024 * 1024:
                (OUT / (name + '.raw')).write_bytes(body)
                row['file'] = name + '.raw'
            else:
                row['error'] = 'over 1 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
