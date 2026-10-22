#!/usr/bin/env python3
"""One bounded direct snapshot of the fixed LH028 source panel."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
URLS = {
    'amazon': 'https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/',
    'cloudflare': 'https://blog.cloudflare.com/php-vulnerabilities-waf-protection/',
    'openai': 'https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/',
}
parser = argparse.ArgumentParser()
parser.add_argument('--snapshot', required=True, help='UTC slot, e.g. 2026-10-22T1600Z')
args = parser.parse_args()
datetime.strptime(args.snapshot, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('snapshot-' + args.snapshot)
assert not OUT.exists(), 'snapshot already exists; do not overwrite'
OUT.mkdir(parents=True)
rows = []
for name, url in URLS.items():
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        try:
            response = urlopen(request, timeout=18)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       bytes=len(body), sha256=sha256(body).hexdigest())
            if len(body) <= 1024 * 1024:
                (OUT / (name + '.raw')).write_bytes(body)
                row['file'] = str((OUT / (name + '.raw')).relative_to(ROOT))
            else:
                row['error'] = 'over 1 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps(row), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
