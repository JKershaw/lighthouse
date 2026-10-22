#!/usr/bin/env python3
"""One immutable, bounded observation of four official PHP moving tags."""
import argparse
import csv
import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAGS = ('8.5-apache', '8.4-fpm', '8.3-cli', '8.2-fpm')
AUTH_URL = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/php:pull'
FIELDS = ('observed_at_utc', 'kind', 'tag', 'url', 'status', 'bytes', 'sha256',
          'file', 'last_modified', 'etag', 'ratelimit_remaining', 'error')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', required=True, help='unique YYYY-MM-DD run label in UTC')
    args = parser.parse_args()
    datetime.strptime(args.snapshot, '%Y-%m-%d')
    out = ROOT / 'data' / ('snapshot-' + args.snapshot)
    if out.exists():
        raise SystemExit('snapshot already exists; refusing to overwrite evidence')
    out.mkdir(parents=True)
    log = out / 'read_log.csv'
    rows = []
    calls = retained = manifests = 0
    ceiling = 10 * 1024 * 1024

    def save(kind, tag, url, headers=None, ephemeral=False):
        nonlocal calls, retained, manifests
        if calls >= 20 or retained >= ceiling:
            raise RuntimeError('run ceiling reached')
        if kind == 'manifest':
            if manifests >= 4:
                raise RuntimeError('manifest GET ceiling reached')
            manifests += 1
        calls += 1
        started = now()
        status = ''
        hdr = {}
        data = b''
        error = ''
        cap = min(1024 * 1024, ceiling - retained)
        try:
            request = urllib.request.Request(url, headers={
                'User-Agent': 'Lighthouse-LH019/0.1', **(headers or {})})
            with urllib.request.urlopen(request, timeout=22) as response:
                status = response.status
                hdr = dict(response.headers)
                data = response.read(cap + 1)
                if len(data) > cap:
                    error = 'response exceeded cap; retained truncated prefix'
                    data = data[:cap]
        except urllib.error.HTTPError as exc:
            status = exc.code
            hdr = dict(exc.headers)
            data = exc.read(min(cap, 4096))
            error = 'HTTP error'
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        path = out / (kind + '_' + tag.replace('.', '_').replace('-', '_') + '.raw')
        if not ephemeral:
            path.write_bytes(data)
            retained += len(data)
        rows.append(dict(observed_at_utc=started, kind=kind, tag=tag, url=url,
                         status=status, bytes=len(data) if not ephemeral else '',
                         sha256=hashlib.sha256(data).hexdigest() if not ephemeral else '',
                         file=path.relative_to(ROOT).as_posix() if not ephemeral else '[anonymous bearer discarded]',
                         last_modified=hdr.get('Last-Modified', ''), etag=hdr.get('ETag', ''),
                         ratelimit_remaining=hdr.get('Ratelimit-Remaining', hdr.get('RateLimit-Remaining', '')),
                         error=error))
        with log.open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        print(kind, tag, status, len(data), error, flush=True)
        return status, data, hdr

    for tag in TAGS:
        status, body, _ = save('hubtag', tag,
                              'https://hub.docker.com/v2/namespaces/library/repositories/php/tags/' + tag)
        if status != 200:
            continue
        try:
            obj = json.loads(body)
            platform = next(image for image in obj['images']
                            if image.get('os') == 'linux' and image.get('architecture') == 'amd64')
            digest = platform['digest']
            if not digest.startswith('sha256:'):
                raise ValueError('invalid platform digest')
        except (ValueError, KeyError, StopIteration) as exc:
            print('Missing linux/amd64 digest', tag, str(exc), flush=True)
            continue
        auth_status, auth_body, _ = save('auth', tag, AUTH_URL, ephemeral=True)
        if auth_status != 200:
            continue
        try:
            token = json.loads(auth_body)['token']
        except (ValueError, KeyError):
            print('Anonymous token unavailable', tag, flush=True)
            continue
        headers = {'Authorization': 'Bearer ' + token,
                   'Accept': 'application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json'}
        manifest_status, manifest_body, manifest_headers = save(
            'manifest', tag,
            'https://registry-1.docker.io/v2/library/php/manifests/' + digest, headers)
        remaining = manifest_headers.get('Ratelimit-Remaining', '')
        if manifest_status == 429:
            print('Stopping at registry rate limit', flush=True)
            break
        if manifest_status == 200:
            try:
                config = json.loads(manifest_body)['config']['digest']
                if not config.startswith('sha256:'):
                    raise ValueError('invalid config digest')
                save('config', tag,
                     'https://registry-1.docker.io/v2/library/php/blobs/' + config,
                     {'Authorization': 'Bearer ' + token})
            except (ValueError, KeyError) as exc:
                print('Missing configuration', tag, str(exc), flush=True)
        if remaining:
            try:
                if int(remaining.split(';')[0]) < 10:
                    print('Stopping with fewer than ten registry pulls remaining', flush=True)
                    break
            except ValueError:
                pass
    print('COMPLETE', now(), 'requests', calls, 'retained bytes', retained, flush=True)


if __name__ == '__main__':
    main()
