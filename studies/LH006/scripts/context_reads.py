#!/usr/bin/env python3
"""LH006: context reads that are not part of the selection. (1) Docker Hub's repository search count
for the word "mcp", to size the wider population the brief excludes (no result's content read).
(2) The OCI referrers endpoint on ghcr.io for one serena image, to see whether the registry lists
anything attached to a digest. Writes data/context_reads.csv."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, write_csv, read_csv, now
import registry as R

rows = []
r = http('hub.docker.com v2 API', 'search mcp', 'https://hub.docker.com/v2/search/repositories/?query=mcp&page_size=1')
rows.append(dict(read_utc=now(), reading='Docker Hub repository search, query "mcp"', http_status=r.status_code,
                 value=r.json().get('count') if r.status_code == 200 else ''))
img = [x for x in read_csv('images.csv') if x['image'] == 'ghcr.io/oraios/serena' and x['tags'].startswith('1.2')][0]
tok = R.token('ghcr.io', 'oraios/serena')
r = http('ghcr.io registry API', 'referrers serena 1.2.0', f"https://ghcr.io/v2/oraios/serena/referrers/{img['index_digest']}",
         headers={'Authorization': f'Bearer {tok}', 'Accept': 'application/vnd.oci.image.index.v1+json'})
body = r.json() if r.headers.get('content-type', '').startswith('application/') and r.content else {}
rows.append(dict(read_utc=now(), reading='ghcr.io OCI referrers for serena 1.2.0 index', http_status=r.status_code,
                 value=len(body.get('manifests', [])) if isinstance(body, dict) and 'manifests' in body else (r.text[:120].replace('\n', ' '))))
write_csv('context_reads.csv', rows, ['read_utc', 'reading', 'http_status', 'value'])
print(rows)

# (3) Docker Hub repository records: pull_count (manifest requests, not runs), last_updated, date registered
for c in read_csv('candidates.csv'):
    if c['qualifies'] == 'yes' and c['image_repository'].startswith('docker.io/'):
        ns, repo = c['image_repository'][10:].split('/')
        r = http('hub.docker.com v2 API', f'repository {ns}/{repo}', f'https://hub.docker.com/v2/namespaces/{ns}/repositories/{repo}')
        j = r.json() if r.status_code == 200 else {}
        rows.append(dict(read_utc=now(), reading=f'Docker Hub repository record {ns}/{repo}: pull_count; date_registered; last_updated',
                         http_status=r.status_code, value=f"{j.get('pull_count')}; {j.get('date_registered')}; {j.get('last_updated')}"))
write_csv('context_reads.csv', rows, ['read_utc', 'reading', 'http_status', 'value'])
print(rows[2:])
