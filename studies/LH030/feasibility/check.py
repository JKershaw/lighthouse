#!/usr/bin/env python3
"""One GET per structured tracker, all for the unrelated CVE-2024-4577."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

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
            response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=25)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       content_type=response.headers.get('Content-Type', ''), last_modified=response.headers.get('Last-Modified', ''),
                       bytes=len(body), sha256=sha256(body).hexdigest())
            if len(body) <= 1024 * 1024:
                (HERE / (name + '.raw')).write_bytes(body)
                row['file'] = name + '.raw'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'content_type', 'last_modified', 'error')}), flush=True)
(HERE / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
