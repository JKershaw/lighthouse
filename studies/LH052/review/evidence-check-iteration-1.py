#!/usr/bin/env python3
"""Offline LH052 evidence-review arithmetic and cached provenance check.

Run from the repository root. No network calls. Cached bodies are optional,
temporary inputs, not retained source replay. Never emit source bodies.
"""
import collections
import csv
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = attrs.get('property', attrs.get('name'))
        if tag == 'meta' and key in ('article:published_time', 'article:modified_time'):
            self.values[key] = attrs.get('content')


p = Path('studies/LH052')
rows = list(csv.DictReader((p / 'cases.csv').open()))
log = [json.loads(line) for line in (p / 'reads-iteration-1.jsonl').read_text().splitlines()]
http = [row for row in log if row['type'] == 'http_request']
sources = json.loads((p / 'sources-iteration-1.json').read_text())['sources']
result = {
    'case_field_rows': len(rows),
    'classification_counts': dict(collections.Counter(row['classification'] for row in rows)),
    'distinct_cases': len({row['case_id'] for row in rows}),
    'distinct_source_ids': len({row['source_id'] for row in rows}),
    'field_rows_by_source': dict(collections.Counter(row['source_id'] for row in rows)),
    'duplicate_case_source_fields': len(rows) - len({(row['case_id'], row['source_id'], row['field']) for row in rows}),
    'http_requests': len(http),
    'http_request_kinds': dict(collections.Counter(row['request_kind'] for row in http)),
    'http_bytes': sum(row['bytes'] for row in http),
    'http_elapsed_seconds_sum': round(sum(row['elapsed_seconds'] for row in http), 3),
    'search_request_count': sum(row['request_count'] for row in log if row['type'] == 'discovery'),
    'search_query_count': sum(row['query_count'] for row in log if row['type'] == 'discovery'),
    'source_access_counts': dict(collections.Counter(row['substantive_access'] for row in sources)),
}
evidence_ids = set()
result['evidence_files'] = {}
for f in sorted((p / 'data/iteration-1').glob('*-evidence.json')):
    d = json.loads(f.read_text())
    count = sum(len(item['paraphrase'].split()) for item in d['evidence'])
    evidence_ids.update(item['id'] for item in d['evidence'])
    result['evidence_files'][f.name] = {
        'recorded_words': d['paraphrase_word_count'],
        'recomputed_whitespace_words': count,
        'matches': count == d['paraphrase_word_count'],
        'below_150': count <= 150,
    }
result['missing_referenced_evidence_ids'] = sorted({ref for row in rows for ref in row['evidence_ids'].split(';') if ref} - evidence_ids)
reviewed_inputs = [p / 'brief.md', p / 'iteration-1.md', p / 'cases.csv', p / 'sources-iteration-1.json', p / 'reads-iteration-1.jsonl']
reviewed_inputs += sorted((p / 'data/iteration-1').glob('*-evidence.json'))
result['reviewed_input_sha256'] = {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in reviewed_inputs}
result['cached_sources'] = {}
for source in sources:
    body = Path('/tmp/lh051-iteration1') / (source['id'] + '.html')
    if not body.exists():
        result['cached_sources'][source['id']] = {'available_for_this_replay': False}
        continue
    raw = body.read_bytes()
    parser = Metadata()
    parser.feed(raw.decode(errors='replace'))
    digest = hashlib.sha256(raw).hexdigest()
    result['cached_sources'][source['id']] = {
        'sha256': digest,
        'matches_recorded_original_hash': digest == source['sha256_raw'],
        'bytes': len(raw),
        'matches_recorded_bytes': len(raw) == source['bytes'],
        'publication_metadata': parser.values,
        'site_unavailable_placeholder': b'<title>Site Unavailable</title>' in raw,
    }
print(json.dumps(result, indent=2))
