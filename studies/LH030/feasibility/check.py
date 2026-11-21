#!/usr/bin/env python3
"""One GET per structured tracker, all for the unrelated CVE-2024-4577.

The record of the feasibility check of 23 October 2026 (studies/LH030/sources.md); it is not run again.
From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) it fetches through
scripts/lh_fetch.py's urlopen with access='oneoff' (before, urllib's urlopen with no robots check), so a URL
robots.txt refuses is not requested and is logged as an error "NotFetched: ..."; and it saves a body only
through lh_fetch's save_body, which withholds email addresses (the 23 October bodies were saved as received);
where a body may not be kept nothing is written, the row has no `file` and gets body_kept "no: <reason>".
A kept body is otherwise saved under the same name as before.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH030/feasibility/check.py`.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from lh_fetch import urlopen, save_body  # noqa: E402  robots.txt gate and the one keep path (21 November 2026)

HERE = Path(__file__).resolve().parent
URLS = {
    'debian': 'https://security-tracker.debian.org/tracker/CVE-2024-4577',
    'ubuntu': 'https://ubuntu.com/security/cves/CVE-2024-4577.json',
    'redhat': 'https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2024-4577.json',
    'suse': 'https://www.suse.com/security/cve/CVE-2024-4577.html',
    'cve_org': 'https://cveawg.mitre.org/api/cve/CVE-2024-4577',
    'nvd': 'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-4577',
    'osv': 'https://api.osv.dev/v1/vulns/CVE-2024-4577',
}
assert not (HERE / 'read_log.json').exists()
rows = []
for name, url in URLS.items():
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        try:
            response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=25,
                               access='oneoff')
        except HTTPError as error:
            response = error
        with response:
            body = response.read(1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       content_type=response.headers.get('Content-Type', ''), last_modified=response.headers.get('Last-Modified', ''),
                       bytes=len(body), sha256=sha256(body).hexdigest())
            if len(body) <= 1024 * 1024:
                kept, why = save_body(HERE / (name + '.raw'), body, response.geturl() or url, response.headers)
                if kept:
                    row['file'] = name + '.raw'
                else:
                    row['body_kept'] = 'no: ' + why
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'content_type', 'last_modified', 'error')}), flush=True)
(HERE / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
