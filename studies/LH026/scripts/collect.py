#!/usr/bin/env python3
"""Read one exact PHP base variant; discard its anonymous registry bearer.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body (which withholds email addresses, as before); where it may
not be kept no .raw is written, `file` is empty and `error` ends "body_kept: no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH026/scripts/collect.py`."""
import csv
import hashlib
import json
import urllib.error
import urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/snapshot-2026-10-22'
OUT.mkdir(parents=True, exist_ok=False)
rows = []
retained = 0


def fetch(key, url, headers=None, ephemeral=False):
    global retained
    if len(rows) >= 4 or retained >= 2 * 1024 * 1024:
        raise RuntimeError('ceiling')
    at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    status, data, hdr, error = '', b'', {}, ''
    final = url
    cap = min(1024 * 1024, 2 * 1024 * 1024 - retained)
    try:
        request = urllib.request.Request(url, headers={'User-Agent': UA, **(headers or {})})
        with urlopen(request, timeout=25) as response:
            status, hdr = response.status, dict(response.headers)
            final = response.geturl() or url
            data = response.read(cap + 1)
            if len(data) > cap:
                data, error = data[:cap], 'response exceeded cap'
    except urllib.error.HTTPError as exc:
        status, hdr, data, error = exc.code, dict(exc.headers), exc.read(min(cap, 4096)), 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    kept, logged_error = True, error
    if not ephemeral:
        kept, why = save_body(OUT / (key + '.raw'), data, final, hdr)
        if not kept:
            logged_error = (error + '; ' if error else '') + 'body_kept: no: ' + why
        retained += len(data)
    remaining = hdr.get('Ratelimit-Remaining', hdr.get('RateLimit-Remaining', ''))
    rows.append(dict(utc=at, key=key, url=url, status=status,
                     bytes='' if ephemeral else len(data),
                     sha256='' if ephemeral else hashlib.sha256(data).hexdigest(),
                     file='[anonymous bearer discarded]' if ephemeral else (str(Path('data') / OUT.name / (key + '.raw')) if kept else ''),
                     ratelimit_remaining=remaining, error=logged_error))
    with (OUT / 'read_log.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, rows[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(key, status, len(data), logged_error, flush=True)
    return json.loads(data) if status == 200 and not error else None, remaining


tag, _ = fetch('hubtag', 'https://hub.docker.com/v2/namespaces/library/repositories/php/tags/8.3-fpm-trixie')
if tag:
    matches = [x for x in tag.get('images', []) if x.get('os') == 'linux' and x.get('architecture') == 'amd64']
    if matches:
        token, _ = fetch('auth', 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/php:pull', ephemeral=True)
        if token:
            h = {'Authorization': 'Bearer ' + token['token'], 'Accept': 'application/vnd.oci.image.manifest.v1+json'}
            manifest, remaining = fetch('manifest',
                'https://registry-1.docker.io/v2/library/php/manifests/' + matches[0]['digest'], h)
            if manifest and remaining and int(remaining.split(';')[0]) < 10:
                print('rate limit stop', remaining)
            elif manifest:
                fetch('config', 'https://registry-1.docker.io/v2/library/php/blobs/' + manifest['config']['digest'],
                      {'Authorization': 'Bearer ' + token['token']})
print('COMPLETE', len(rows), retained, 'retained bytes')
