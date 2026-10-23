#!/usr/bin/env python3
"""Offline source integrity and evidence-marker index; no external calls."""
import csv
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip, self.text = 0, []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg') and self.skip:
            self.skip -= 1

    def handle_data(self, value):
        if not self.skip and value.strip():
            self.text.append(' '.join(value.split()))


oai = next(r for r in json.loads((ROOT / 'studies/LH028/data/snapshot-2026-10-23T1600Z/read_log.json').read_text()) if r['source'] == 'openai')
google = next(r for r in csv.DictReader((ROOT / 'studies/LH024/data/snapshot-2026-10-23/read_log.csv').open()) if r['key'] == 'google_cloud_0')
wiz = json.loads((HERE / 'read_log.json').read_text())
packed = (HERE / wiz['file']).read_bytes()
assert hashlib.sha256(packed).hexdigest() == wiz['sha256_gzip']
sources = [
    ('openai', ROOT / 'studies/LH028/data/snapshot-2026-10-23T1600Z/openai.raw', oai['bytes'], oai['sha256'], None,
     ['Calif', 'GPT', 'Wiz', 'maintainers', 'coordinate']),
    ('google', ROOT / 'studies/LH024/data/snapshot-2026-10-23/google_cloud_0.raw', int(google['bytes_retained']), google['sha256_retained'], None,
     ['Wiz', 'Gemini 4 Argon', 'exploit development', 'validation']),
    ('wiz', HERE / wiz['file'], wiz['retained_bytes'], wiz['sha256_retained'], gzip.decompress,
     ['Wiz Atlas', 'Gemini 4 Argon', 'GPT-5.6 Sol', 'August 19, 2026', 'August 24, 2026']),
]
index = []
for name, path, size, sha, decode, markers in sources:
    raw = path.read_bytes()
    if decode:
        raw = decode(raw)
    assert len(raw) == size
    assert hashlib.sha256(raw).hexdigest() == sha
    parser = Visible()
    parser.feed(raw.decode('utf-8', 'replace'))
    joined = ' '.join(parser.text)
    assert all(marker in joined for marker in markers), (name, markers)
    index.append({'source': name, 'sha256': sha, 'verified_bytes': size,
                  'markers_present': markers})
print(json.dumps(index, indent=1))
