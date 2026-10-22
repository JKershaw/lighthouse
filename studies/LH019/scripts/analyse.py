#!/usr/bin/env python3
"""Verify one retained LH019 run and reconstruct its four-track summary offline."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTERPART = ROOT.parent / 'LH018' / 'data' / 'snapshot-2026-10-21'
TRACKS = (
    ('8.5-apache', '8.5.12-apache', '8.5.12'),
    ('8.4-fpm', '8.4.27-fpm', '8.4.27'),
    ('8.3-cli', '8.3.36-cli', '8.3.36'),
    ('8.2-fpm', '8.2.35-fpm', '8.2.35'),
)


def key(tag):
    return tag.replace('.', '_').replace('-', '_')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', default='2026-10-21')
    args = parser.parse_args()
    folder = ROOT / 'data' / ('snapshot-' + args.snapshot)
    log = list(csv.DictReader((folder / 'read_log.csv').open(newline='')))
    assert len(log) <= 20
    assert sum(row['kind'] == 'manifest' for row in log) <= 4
    total = 0
    for row in log:
        if row['kind'] == 'auth':
            assert row['file'] == '[anonymous bearer discarded]'
            continue
        raw = (ROOT / row['file']).read_bytes()
        assert len(raw) == int(row['bytes']) and digest(raw) == row['sha256'], row['file']
        total += len(raw)
    assert total <= 10 * 1024 * 1024

    rows = []
    for tag, fixed, version in TRACKS:
        k = key(tag)
        selected = [r for r in log if r['tag'] == tag]
        hub = next(r for r in selected if r['kind'] == 'hubtag')
        row = dict(tag=tag, architecture='linux/amd64', observed_at_utc=hub['observed_at_utc'],
                   status='unknown', manifest_digest='', fixed_counterpart_digest='',
                   matches_fixed_counterpart='', declared_php_version='',
                   platform_last_pushed='', tag_last_pushed='',
                   evidence='; '.join(r['file'] for r in selected if r['kind'] != 'auth'))
        if any(r['status'] != '200' for r in selected):
            row['status'] = 'incomplete HTTP read'
            rows.append(row)
            continue
        if {r['kind'] for r in selected} != {'hubtag', 'auth', 'manifest', 'config'}:
            row['status'] = 'incomplete source fields'
            rows.append(row)
            continue
        hub_data = json.loads((folder / ('hubtag_' + k + '.raw')).read_bytes())
        platform = next((x for x in hub_data['images'] if x.get('os') == 'linux' and
                         x.get('architecture') == 'amd64'), None)
        if platform is None:
            row['status'] = 'linux/amd64 absent'
            rows.append(row)
            continue
        raw_manifest = (folder / ('manifest_' + k + '.raw')).read_bytes()
        raw_config = (folder / ('config_' + k + '.raw')).read_bytes()
        manifest = json.loads(raw_manifest)
        config = json.loads(raw_config)
        assert platform['digest'] == 'sha256:' + digest(raw_manifest), tag
        assert manifest['config']['digest'] == 'sha256:' + digest(raw_config), tag
        env = config['config']['Env']
        declared = next((x.split('=', 1)[1] for x in env if x.startswith('PHP_VERSION=')), '')
        assert 'PHP_URL=https://www.php.net/distributions/php-' + declared + '.tar.xz' in env, tag
        fixed_data = json.loads((COUNTERPART / ('hubtag_' + key(fixed) + '.raw')).read_bytes())
        fixed_platform = next(x for x in fixed_data['images'] if x.get('os') == 'linux' and
                              x.get('architecture') == 'amd64')
        row.update(status='manifest and config verified', manifest_digest=platform['digest'],
                   fixed_counterpart_digest=fixed_platform['digest'],
                   matches_fixed_counterpart=str(platform['digest'] == fixed_platform['digest']).lower(),
                   declared_php_version=declared, platform_last_pushed=platform.get('last_pushed', ''),
                   tag_last_pushed=hub_data.get('tag_last_pushed', ''))
        assert declared == version, tag
        rows.append(row)

    output = ROOT / 'data' / ('summary-' + args.snapshot + '.csv')
    with output.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print('Verified', len(rows), 'tracks,', len(log), 'HTTP observations,', total,
          'retained bytes; summary:', output.relative_to(ROOT))
    for row in rows:
        print(row['tag'], row['status'], row['declared_php_version'], row['matches_fixed_counterpart'])


if __name__ == '__main__':
    main()
