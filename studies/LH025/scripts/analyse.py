#!/usr/bin/env python3
"""Offline replay of LH025 raw bytes, digest links and per-tag daily summary."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
FIELDS = ('repository', 'tag', 'architecture', 'observed_at_utc', 'status', 'manifest_digest',
          'declared_php_version', 'platform_last_pushed', 'tag_last_pushed', 'evidence')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', required=True)
    args = parser.parse_args()
    out = ROOT / 'data' / ('snapshot-' + args.snapshot)
    log = list(csv.DictReader((out / 'read_log.csv').open()))
    assert len(log) <= 24
    assert sum(x['kind'] == 'manifest' for x in log) <= 5
    assert sum(int(x['bytes'] or 0) for x in log) <= 10 * 1024 * 1024
    bodies = {}
    for row in log:
        key = (row['kind'], row['repository'], row['tag'])
        assert key not in bodies
        if row['kind'] == 'auth':
            assert not row['sha256'] and row['file'] == '[anonymous bearer discarded]'
            continue
        body = (ROOT / row['file']).read_bytes()
        assert len(body) == int(row['bytes'])
        assert hashlib.sha256(body).hexdigest() == row['sha256']
        bodies[key] = body
    rows = []
    for item in PANEL:
        repo, tag = item['repository'], item['tag']
        key = (repo, tag)
        observed = next((x['utc'] for x in log if x['kind'] == 'hubtag' and (x['repository'], x['tag']) == key), '')
        row = dict(repository=repo, tag=tag, architecture='linux/amd64', observed_at_utc=observed,
                   status='unknown', manifest_digest='', declared_php_version='', platform_last_pushed='',
                   tag_last_pushed='', evidence='')
        names = [kind for kind in ('hubtag', 'manifest', 'config') if (kind, repo, tag) in bodies]
        row['evidence'] = '; '.join(str((Path('data') / out.name /
            (kind + '_' + repo + '_' + tag.replace('.', '_').replace('-', '_') + '.raw'))) for kind in names)
        try:
            hub = json.loads(bodies[('hubtag', repo, tag)])
            platform = next(x for x in hub['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
            digest = platform['digest']
            row.update(manifest_digest=digest, platform_last_pushed=platform.get('last_pushed', ''),
                       tag_last_pushed=hub.get('tag_last_pushed', ''), status='platform metadata only')
            manifest = bodies[('manifest', repo, tag)]
            assert hashlib.sha256(manifest).hexdigest() == digest.split(':', 1)[1]
            config_digest = json.loads(manifest)['config']['digest']
            config = bodies[('config', repo, tag)]
            assert hashlib.sha256(config).hexdigest() == config_digest.split(':', 1)[1]
            env = json.loads(config)['config'].get('Env') or []
            php = [x.split('=', 1)[1] for x in env if x.startswith('PHP_VERSION=')]
            row.update(declared_php_version=';'.join(php), status='manifest and config verified')
        except (KeyError, ValueError, StopIteration):
            pass
        rows.append(row)
    summary = ROOT / 'data' / ('summary-' + args.snapshot + '.csv')
    with summary.open('w', newline='') as f:
        writer = csv.DictWriter(f, FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print('Verified', len(rows), 'fixed tracks,', len(log), 'requests; summary:', summary.relative_to(ROOT))
    for row in rows:
        print(row['repository'] + ':' + row['tag'], row['status'], row['declared_php_version'] or 'unknown')


if __name__ == '__main__':
    main()
