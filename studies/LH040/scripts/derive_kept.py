#!/usr/bin/env python3
"""Replace LH040's kept pre-brief responses from pypi.org's JSON and simple APIs and from api.deps.dev with derived
files (the keeper's decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md: both sites'
robots.txt refuse all bots under `*` for these paths).

Each derived file (<name>.derived.json beside the body) holds the URL, read time, HTTP status, size and SHA-256
from that directory's readlog.csv, and only what the study uses:
  pypi_project_json (L1): the first upload time of every final release with files, as PyPI gives it
                          (upload_time_iso_8601), which tabulate.py uses for h(R); the release names it lists
                          and its last serial (sources.md, L1);
  pypi_simple_json (L4):  its last serial, project status and the 1.107.0 versions its files name (sources.md, L4);
  pypi_1.107.0_json (L2): its HTTP 404 message; pypi_1.106.7_json, pypi_1.108.0_json (L3): version, yanked flag,
                          file count and first upload time (added 21 November after the sweep; pypi.org's robots.txt
                          refuses /pypi/ paths);
  depsdev_requests_version, depsdev_requests_dependents: read before the brief for the shape of the response
                          only; nothing beyond the read's metadata is kept.
It never deletes anything. Offline, standard library only. Usage: python3 -I studies/LH040/scripts/derive_kept.py
"""
from datetime import datetime
from pathlib import Path
import csv, json

DATA = Path(__file__).resolve().parents[1] / 'data'
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
TARGETS = [
    ('pre-brief-2026-11-08T1414Z', 'pypi_project_json', "L1: first upload time of each final litellm release, for h(R) (tabulate.py); the releases listed (sources.md)."),
    ('pre-brief-2026-11-08T1414Z', 'pypi_simple_json', "L4: PyPI's simple index for litellm: last serial, project status, no final 1.107.0 file (sources.md)."),
    ('pre-brief-2026-11-08T1414Z', 'pypi_1.107.0_json', "L2: PyPI's version record for 1.107.0; HTTP 404 with the message 'Not Found' (sources.md)."),
    ('pre-brief-2026-11-08T1414Z', 'pypi_1.106.7_json', "L3: PyPI's version record for 1.106.7, a neighbour's metadata (sources.md); no script reads it."),
    ('pre-brief-2026-11-08T1414Z', 'pypi_1.108.0_json', "L3: PyPI's version record for 1.108.0, a neighbour's metadata (sources.md); no script reads it."),
    ('pre-brief-2026-11-08T1416Z', 'depsdev_requests_version', "Before the brief: shape of deps.dev's version record (for requests 2.32.3); no figure used."),
    ('pre-brief-2026-11-08T1416Z', 'depsdev_requests_dependents', "Before the brief: shape of deps.dev's dependents count (for requests 2.32.3); no figure used."),
]


def is_final(v):  # as tabulate.py
    return all(p.isdigit() for p in v.split('.'))


def main():
    n = 0
    for d, name, used in TARGETS:
        p = DATA / d / (name + '.raw')
        if not p.exists():
            continue
        row = next(r for r in csv.DictReader(open(DATA / d / 'readlog.csv')) if r['name'] == name)
        ext = {}
        if name == 'pypi_project_json':
            first = {}
            for v, files in json.loads(p.read_bytes())['releases'].items():
                if files and is_final(v):
                    first[v] = min((f['upload_time_iso_8601'] for f in files),
                                   key=lambda s: datetime.fromisoformat(s.replace('Z', '+00:00')))
            j = json.loads(p.read_bytes())
            ext = {'first_upload_time_iso_8601': first, 'last_serial': j.get('last_serial'),
                   'releases_listed': list(j['releases']), 'lists_1.107.0': '1.107.0' in j['releases']}
        if name == 'pypi_simple_json':
            j = json.loads(p.read_bytes())
            fam = sorted({f['filename'].split('-')[1].removesuffix('.tar.gz') for f in j['files'] if f['filename'].startswith('litellm-1.107.0')})
            ext = {'last_serial': j['meta'].get('_last-serial'), 'project_status': (j.get('project-status') or {}).get('status'),
                   'versions_named_in_1.107.0_files': fam, 'lists_final_1.107.0_file': '1.107.0' in fam}
        if name.startswith('pypi_1.'):
            j = json.loads(p.read_bytes())
            if row['status'] != '200':
                ext = {'message': j.get('message')}
            else:
                ext = {'version': j['info']['version'], 'yanked': j['info'].get('yanked'), 'files': len(j.get('urls', [])),
                       'first_upload_time_iso_8601': min((f['upload_time_iso_8601'] for f in j.get('urls', [])),
                                                         key=lambda s: datetime.fromisoformat(s.replace('Z', '+00:00')), default=None)}
        rec = {'url': row['url'], 'read_utc': row['utc_start'], 'http_status': row['status'], 'content_type': row['content_type'],
               'bytes': int(row['size']), 'sha256': row['sha256'], 'robots_class': 'B: * refuses all bots (no AI token named)',
               'body_removed': NOTE, 'used_for': used, 'extracted': ext}
        (DATA / d / (name + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
        n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()
