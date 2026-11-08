#!/usr/bin/env python3
"""LH040 pre-brief read: the event's own records (PyPI metadata, OSV, the reporters' posts, PyPI's
blog and status feed) and ClickPy's table definitions, each URL once, before the brief is fixed.

No download count for litellm is read here. The ClickPy queries ask only for the list of tables,
the column definitions of the per-day tables, and the last day held for an unrelated package
(requests), which returns a date and no count.

Bodies are kept raw under data/pre-brief-<UTC label>/ with readlog.csv
(name, url, utc_start, status, content_type, size, sha256, method, request_body).
The label is the UTC minute the read starts. User-Agent "Lighthouse-research/1.0". No key, token
or credential is read or sent.

Stage 2 follows every vulnerability id the OSV query returns (GET /v1/vulns/<id>), once each,
besides the two ids named below for the March 2026 compromise.

Usage: python3 -I studies/LH040/scripts/collect_prebrief.py [--second | --third]
The first read (2026-11-08T1414Z) used PANEL. --second (2026-11-08T1415Z) reads PANEL_2, the sources the first read
pointed to (LiteLLM's own incident posts, PyPI's report on the March compromise, and OSV's full list
of records for litellm, to check "the second compromise of 2026"); it follows no OSV ids. --third reads PANEL_3: the column definitions of two more ClickPy per-day
tables, and deps.dev's version and dependents endpoints for an unrelated package (requests 2.32.3),
to see whether they answer; nothing for litellm.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import csv
import json
import os
import ssl

ROOT = Path(__file__).resolve().parents[1]
UA = 'Lighthouse-research/1.0'
CEILING = 8 * 1024 * 1024
CA = '/root/.ccr/ca-bundle.crt'
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
CLICKHOUSE = 'https://sql-clickhouse.clickhouse.com/?user=demo&default_format=TabSeparatedWithNames'
OSV_QUERY = json.dumps({'package': {'name': 'litellm', 'ecosystem': 'PyPI'}, 'version': '1.107.0'})

# (name, url, method, body, extra headers)
PANEL = [
    ('pypi_project_json', 'https://pypi.org/pypi/litellm/json', 'GET', None, {}),
    ('pypi_1.107.0_json', 'https://pypi.org/pypi/litellm/1.107.0/json', 'GET', None, {}),
    ('pypi_1.106.7_json', 'https://pypi.org/pypi/litellm/1.106.7/json', 'GET', None, {}),
    ('pypi_1.108.0_json', 'https://pypi.org/pypi/litellm/1.108.0/json', 'GET', None, {}),
    ('pypi_simple_json', 'https://pypi.org/simple/litellm/', 'GET', None,
     {'Accept': 'application/vnd.pypi.simple.v1+json'}),
    ('pypi_project_page_1.107.0', 'https://pypi.org/project/litellm/1.107.0/', 'GET', None, {}),
    ('pypi_project_page', 'https://pypi.org/project/litellm/', 'GET', None, {}),
    ('osv_query_1.107.0', 'https://api.osv.dev/v1/query', 'POST', OSV_QUERY,
     {'Content-Type': 'application/json'}),
    ('osv_MAL-2026-2144', 'https://api.osv.dev/v1/vulns/MAL-2026-2144', 'GET', None, {}),
    ('osv_PYSEC-2026-2', 'https://api.osv.dev/v1/vulns/PYSEC-2026-2', 'GET', None, {}),
    ('cloudsmith', 'https://cloudsmith.com/blog/litellm-1-107-0-compromised-on-pypi', 'GET', None, {}),
    ('aikido', 'https://www.aikido.dev/blog/litellm-compromised-infostealer-rat', 'GET', None, {}),
    ('aikido_index', 'https://www.aikido.dev/blog', 'GET', None, {}),
    ('datadog', 'https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-docker/', 'GET', None, {}),
    ('stepsecurity', 'https://www.stepsecurity.io/blog/litellm-1-107-0-compromised-pypi-backdoored-wheels-credential-stealer',
     'GET', None, {}),
    ('pypi_blog', 'https://blog.pypi.org/', 'GET', None, {}),
    ('pypi_blog_feed', 'https://blog.pypi.org/feed_rss_created.xml', 'GET', None, {}),
    ('python_status_history', 'https://status.python.org/history.rss', 'GET', None, {}),
    ('litellm_docs_blog', 'https://docs.litellm.ai/blog', 'GET', None, {}),
    ('clickpy_tables', CLICKHOUSE, 'POST', 'SHOW TABLES FROM pypi', {}),
    ('clickpy_describe_per_day_by_version', CLICKHOUSE, 'POST',
     'DESCRIBE TABLE pypi.pypi_downloads_per_day_by_version', {}),
    ('clickpy_describe_pypi', CLICKHOUSE, 'POST', 'DESCRIBE TABLE pypi.pypi', {}),
    ('clickpy_last_day_requests', CLICKHOUSE, 'POST',
     "SELECT max(date) AS last_day FROM pypi.pypi_downloads_per_day_by_version WHERE project = 'requests'", {}),
]

OSV_ALL = json.dumps({'package': {'name': 'litellm', 'ecosystem': 'PyPI'}})
PANEL_2 = [
    ('litellm_incident_oct21', 'https://docs.litellm.ai/blog/security-incident-oct-21-2026', 'GET', None, {}),
    ('litellm_incident_oct21_attack_chain', 'https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain',
     'GET', None, {}),
    ('litellm_changes_after_oct21', 'https://docs.litellm.ai/blog/security-changes-after-oct-21-2026', 'GET', None, {}),
    ('litellm_update_march2026', 'https://docs.litellm.ai/blog/security-update-march-2026', 'GET', None, {}),
    ('pypi_incident_report_march2026',
     'https://blog.pypi.org/posts/2026-04-02-incident-report-litellm-telnyx-supply-chain-attack/', 'GET', None, {}),
    ('pypi_docs_quarantine', 'https://docs.pypi.org/using-pypi/pypi-basics/', 'GET', None, {}),
    ('osv_query_all_litellm', 'https://api.osv.dev/v1/query', 'POST', OSV_ALL, {'Content-Type': 'application/json'}),
]

PANEL_3 = [
    ('clickpy_describe_installer_by_type', CLICKHOUSE, 'POST',
     'DESCRIBE TABLE pypi.pypi_downloads_per_day_by_version_by_installer_by_type', {}),
    ('clickpy_describe_file_type', CLICKHOUSE, 'POST',
     'DESCRIBE TABLE pypi.pypi_downloads_per_day_by_version_by_file_type', {}),
    ('clickpy_describe_system', CLICKHOUSE, 'POST',
     'DESCRIBE TABLE pypi.pypi_downloads_per_day_by_version_by_system', {}),
    ('depsdev_requests_version', 'https://api.deps.dev/v3/systems/pypi/packages/requests/versions/2.32.3', 'GET', None, {}),
    ('depsdev_requests_dependents',
     'https://api.deps.dev/v3alpha/systems/pypi/packages/requests/versions/2.32.3:dependents', 'GET', None, {}),
]


def fetch(name, url, method, body, headers, out, rows):
    row = {'name': name, 'url': url, 'utc_start': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'method': method, 'request_body': body or ''}
    data = body.encode() if body is not None else None
    req = Request(url, data=data, method=method, headers={'User-Agent': UA, **headers})
    payload = b''
    try:
        try:
            resp = urlopen(req, timeout=60, context=CTX)
        except HTTPError as err:
            resp = err
        with resp:
            payload = resp.read(CEILING + 1)
            row.update(status=resp.status, content_type=resp.headers.get('Content-Type', ''))
    except Exception as err:  # network failure: recorded, nothing invented
        row.update(status='error: ' + type(err).__name__ + ': ' + str(err)[:200], content_type='')
    row.update(size=len(payload), sha256=sha256(payload).hexdigest() if payload else '')
    if payload:
        (out / (name + '.raw')).write_bytes(payload[:CEILING])
    rows.append(row)
    print(json.dumps({k: row[k] for k in ('name', 'status', 'size')}), flush=True)
    return payload


def main():
    label = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%MZ')
    out = ROOT / 'data' / ('pre-brief-' + label)
    assert not out.exists(), 'label already held; not overwritten'
    out.mkdir(parents=True)
    import sys
    rows = []
    follow = []
    for name, url, method, body, headers in (PANEL_2 if '--second' in sys.argv else PANEL_3 if '--third' in sys.argv else PANEL):
        payload = fetch(name, url, method, body, headers, out, rows)
        if name == 'osv_query_1.107.0' and payload:
            try:
                ids = [v['id'] for v in json.loads(payload).get('vulns', [])]
            except ValueError:
                ids = []
            follow = [i for i in ids if i not in ('MAL-2026-2144', 'PYSEC-2026-2')]
    for vid in follow:
        fetch('osv_' + vid, 'https://api.osv.dev/v1/vulns/' + vid, 'GET', None, {}, out, rows)
    fields = ['name', 'url', 'utc_start', 'status', 'content_type', 'size', 'sha256', 'method', 'request_body']
    with open(out / 'readlog.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(out)


if __name__ == '__main__':
    main()
