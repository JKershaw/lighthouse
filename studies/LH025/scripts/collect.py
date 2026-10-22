#!/usr/bin/env python3
"""One bounded five-tag registry snapshot with immutable raw evidence."""
import argparse
import csv
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
FIELDS = ('utc', 'kind', 'repository', 'tag', 'url', 'status', 'bytes', 'sha256', 'file',
          'etag', 'ratelimit_remaining', 'error')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', required=True)
    args = parser.parse_args()
    datetime.strptime(args.snapshot, '%Y-%m-%d')
    out = ROOT / 'data' / ('snapshot-' + args.snapshot)
    out.mkdir(parents=True, exist_ok=False)
    rows, auth = [], {}
    retained = manifests = 0

    def save(kind, repo, tag, url, headers=None, ephemeral=False):
        nonlocal retained, manifests
        if len(rows) >= 24 or retained >= 10 * 1024 * 1024:
            raise RuntimeError('request or retained byte ceiling')
        if kind == 'manifest':
            if manifests >= 5:
                raise RuntimeError('manifest GET ceiling')
            manifests += 1
        status, data, hdr, error = '', b'', {}, ''
        at = now()
        cap = min(1024 * 1024, 10 * 1024 * 1024 - retained)
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH025/0.1', **(headers or {})})
            with urllib.request.urlopen(request, timeout=25) as response:
                status, hdr = response.status, dict(response.headers)
                data = response.read(cap + 1)
                if len(data) > cap:
                    data, error = data[:cap], 'response exceeded byte cap; retained prefix only'
        except urllib.error.HTTPError as exc:
            status, hdr, data, error = exc.code, dict(exc.headers), exc.read(min(cap, 4096)), 'HTTP error'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        filename = f'{kind}_{repo}_{tag.replace(".", "_").replace("-", "_")}.raw'
        path = out / filename
        if not ephemeral:
            path.write_bytes(data)
            retained += len(data)
        limit = hdr.get('Ratelimit-Remaining', hdr.get('RateLimit-Remaining', ''))
        row = dict(utc=at, kind=kind, repository=repo, tag=tag, url=url, status=status,
                   bytes='' if ephemeral else len(data), sha256='' if ephemeral else hashlib.sha256(data).hexdigest(),
                   file='[anonymous bearer discarded]' if ephemeral else path.relative_to(ROOT).as_posix(),
                   etag=hdr.get('ETag', ''), ratelimit_remaining=limit, error=error)
        rows.append(row)
        with (out / 'read_log.csv').open('w', newline='') as f:
            w = csv.DictWriter(f, FIELDS, lineterminator='\n')
            w.writeheader()
            w.writerows(rows)
        print(kind, repo, tag, status, len(data), error, flush=True)
        return status, data, limit

    for item in PANEL:
        repo, tag = item['repository'], item['tag']
        status, body, _ = save('hubtag', repo, tag,
            f'https://hub.docker.com/v2/namespaces/library/repositories/{repo}/tags/{tag}')
        if status != 200:
            continue
        try:
            platform = next(x for x in json.loads(body)['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
            digest = platform['digest']
            assert digest.startswith('sha256:')
        except (ValueError, KeyError, StopIteration, AssertionError) as exc:
            print('missing linux/amd64 digest', repo, tag, exc, flush=True)
            continue
        if repo not in auth:
            status, token, _ = save('auth', repo, tag,
                f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/{repo}:pull',
                ephemeral=True)
            if status != 200:
                continue
            try:
                auth[repo] = json.loads(token)['token']
            except (ValueError, KeyError):
                continue
        h = {'Authorization': 'Bearer ' + auth[repo], 'Accept': 'application/vnd.oci.image.manifest.v1+json'}
        status, manifest, limit = save('manifest', repo, tag,
            f'https://registry-1.docker.io/v2/library/{repo}/manifests/{digest}', h)
        if status == 429 or (limit and int(limit.split(';')[0]) < 10):
            print('stopped at registry allowance', limit, flush=True)
            break
        if status != 200 or hashlib.sha256(manifest).hexdigest() != digest.split(':')[1]:
            continue
        try:
            config = json.loads(manifest)['config']['digest']
        except (ValueError, KeyError):
            continue
        status, _, limit = save('config', repo, tag,
            f'https://registry-1.docker.io/v2/library/{repo}/blobs/{config}',
            {'Authorization': 'Bearer ' + auth[repo]})
        if status == 429 or (limit and int(limit.split(';')[0]) < 10):
            print('stopped at registry allowance', limit, flush=True)
            break
    print('COMPLETE', now(), len(rows), 'requests', retained, 'retained bytes')


if __name__ == '__main__':
    main()
