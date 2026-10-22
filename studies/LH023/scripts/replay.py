#!/usr/bin/env python3
"""Offline hash, Git blob and OCI digest replay of the retained LH023 snapshot."""
import base64
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/snapshot-2026-10-22'
for row in csv.DictReader((OUT / 'read_log.csv').open()):
    if row['key'] == 'auth':
        assert row['sha256'] == '' and not (OUT / 'auth.raw').exists()
        continue
    body = (OUT / (row['key'] + '.raw')).read_bytes()
    assert len(body) == int(row['bytes'])
    assert hashlib.sha256(body).hexdigest() == row['sha256']
    assert str(row['status']) == '200' and not row['error']

for label in ('pre', 'head', 'production'):
    obj = json.loads((OUT / (label + '_recipe.raw')).read_text())
    content = base64.b64decode(obj['content'])
    gitsha = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    assert gitsha == obj['sha']
    assert b'FROM php:8.3-fpm-trixie\n' in content

tag = json.loads((OUT / 'derived_tag.raw').read_text())
amd64 = next(x for x in tag['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
manifest = (OUT / 'manifest.raw').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == amd64['digest'].split(':')[1]
config_digest = json.loads(manifest)['config']['digest']
config = (OUT / 'config.raw').read_bytes()
assert hashlib.sha256(config).hexdigest() == config_digest.split(':')[1]
versions = [x for x in json.loads(config)['config']['Env'] if x.startswith('PHP_VERSION=')]
assert versions == ['PHP_VERSION=8.3.36']
print('verified 3 Git blobs, amd64 manifest, config, all retained response hashes')
print('derived digest', amd64['digest'], 'platform pushed', amd64['last_pushed'])
