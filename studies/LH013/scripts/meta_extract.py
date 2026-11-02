#!/usr/bin/env python3
"""LH013: turns the 37 PyPI JSON bodies read on 2 November 2026 (kept in scratch space, their SHA-256 in
data/pypi_json_sha256.txt) into data/versions.csv, one row per version, with the columns of LH012's
data/versions.csv, as LH012's collect_meta.py built them. Usage: python3 meta_extract.py <raw dir>"""
import csv, json, os, sys
from packaging.version import Version, InvalidVersion

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = sys.argv[1]


def pre(v):
    try:
        x = Version(v)
        return x.is_prerelease or x.is_devrelease, 'ok'
    except InvalidVersion:
        return '', 'invalid'


rows = []
for fn in sorted(os.listdir(RAW)):
    if not fn.endswith('.json'):
        continue
    name = fn[:-5]
    d = json.load(open(os.path.join(RAW, fn)))
    for v, files in d['releases'].items():
        ups = sorted(f['upload_time_iso_8601'] for f in files)
        is_pre, parse = pre(v)
        rp = sorted({(f.get('requires_python') or '') for f in files})
        rows.append(dict(project=name, version=v, first_upload_utc=ups[0] if ups else '', is_prerelease=is_pre, parse=parse,
                         n_files=len(files), all_yanked=bool(files) and all(f.get('yanked') for f in files),
                         last_upload_utc=ups[-1] if ups else '', any_yanked=any(f.get('yanked') for f in files),
                         requires_python=' | '.join(rp), has_sdist=any(f['packagetype'] == 'sdist' for f in files),
                         n_wheels=sum(f['packagetype'] == 'bdist_wheel' for f in files)))
fields = ['project', 'version', 'first_upload_utc', 'is_prerelease', 'parse', 'n_files', 'all_yanked', 'last_upload_utc',
          'any_yanked', 'requires_python', 'has_sdist', 'n_wheels']
with open(os.path.join(STUDY, 'data', 'versions.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
print(len(rows), 'versions')
