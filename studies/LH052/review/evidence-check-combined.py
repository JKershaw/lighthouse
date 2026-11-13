#!/usr/bin/env python3
"""Replay LH052 retained coding/footprint arithmetic without network access.

Temporary cached sources, when available, permit byte identification only.
This program does not fetch sources, emit their bodies or reproduce private data.
"""
import collections
import csv
import hashlib
import json
import sys
from pathlib import Path

p = Path('studies/LH052')
sys.path.insert(0, 'scripts')
from redact_emails import redact_bytes
inputs = [p / 'brief.md', p / 'cases.csv', p / 'operator-measurements.csv']
result = {'iterations': {}, 'review_footprint': {
    'cached_substantive_verification_documents': 7,
    'new_http_requests': 0,
    'new_discovery_queries': 0,
    'remaining_substantive_verification_allowance': 1,
}}
all_http = []
source_ids = set()
all_endpoints = set()
for iteration, cache_dir in ((1, '/tmp/lh051-iteration1'), (2, '/tmp/lh051-iteration-2')):
    source_file = p / f'sources-iteration-{iteration}.json'
    log_file = p / f'reads-iteration-{iteration}.jsonl'
    inputs.extend([source_file, log_file, p / f'iteration-{iteration}.md'])
    sources = json.loads(source_file.read_text())['sources']
    log = [json.loads(line) for line in log_file.read_text().splitlines()]
    http = [row for row in log if row['type'] == 'http_request']
    all_http.extend(http)
    substantive = [row for row in http if row['request_kind'] == 'substantive']
    all_endpoints.update(row['url'] for row in substantive)
    source_ids.update(row['id'] for row in sources)
    item = {
        'http_requests': len(http),
        'request_kinds': dict(collections.Counter(row['request_kind'] for row in http)),
        'response_body_bytes': sum(row['bytes'] for row in http),
        'summed_http_elapsed_seconds': round(sum(row['elapsed_seconds'] for row in http), 3),
        'source_access_counts': dict(collections.Counter(row['substantive_access'] for row in sources)),
        'unique_substantive_endpoints': len({row['url'] for row in substantive}),
        'logged_redirects': sum(bool(row.get('redirect_to')) for row in http),
        'discovery_queries': sum(row.get('query_count', 0) for row in log if row['type'] == 'discovery'),
        'cached_source_identification': {},
    }
    for source in sources:
        suffix = '.pdf' if source['id'] == 'I2-S04' else '.html'
        cache = Path(cache_dir) / (source['id'] + suffix)
        if not cache.exists():
            item['cached_source_identification'][source['id']] = {'available': False}
            continue
        raw = cache.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        item['cached_source_identification'][source['id']] = {
            'available': True,
            'observed_cache_sha256': digest,
            'recorded_original_sha256': source['sha256_raw'],
            'matches_original_hash': digest == source['sha256_raw'],
            'matches_recorded_redacted_cache': digest == source.get('cache_correction', {}).get('sha256_redacted_cache'),
            'observed_cache_bytes': len(raw),
            'recorded_original_bytes': source['bytes'],
        }
        if suffix == '.html':
            item['cached_source_identification'][source['id']]['remaining_text_email_pattern_matches'] = redact_bytes(raw)[1]
        extracted = Path(cache_dir) / (source['id'] + '.txt')
        if extracted.exists():
            item['cached_source_identification'][source['id']]['extracted_text_email_pattern_matches'] = redact_bytes(extracted.read_bytes())[1]
    result['iterations'][str(iteration)] = item

rows = list(csv.DictReader((p / 'cases.csv').open()))
measurement_rows = list(csv.DictReader((p / 'operator-measurements.csv').open()))
result['outage_coding'] = {
    'rows': len(rows),
    'classification_counts': dict(collections.Counter(row['classification'] for row in rows)),
    'distinct_cases': len({row['case_id'] for row in rows}),
}
result['measurement_coding'] = {
    'rows': len(measurement_rows),
    'status_counts': dict(collections.Counter(row['status'] for row in measurement_rows)),
    'duplicate_row_ids': len(measurement_rows) - len({row['row_id'] for row in measurement_rows}),
    'words_by_source': {},
    'locator_row_set_matches_matrix': {},
}
for f in sorted((p / 'data/iteration-1').glob('*evidence.json')):
    inputs.append(f)
for f in sorted((p / 'data/iteration-2').glob('*evidence.json')):
    inputs.append(f)
    evidence = json.loads(f.read_text())
    sid = evidence['source_id']
    matching = [row for row in measurement_rows if row['source_id'] == sid]
    count = sum(len(row['measurement_or_limit'].split()) for row in matching)
    result['measurement_coding']['words_by_source'][sid] = {
        'recomputed_whitespace_words': count,
        'recorded_words': evidence['paraphrase_words'],
        'matches': count == evidence['paraphrase_words'],
        'at_most_150': count <= 150,
    }
    result['measurement_coding']['locator_row_set_matches_matrix'][sid] = (
        {row['row_id'] for row in matching} == {row['row_id'] for row in evidence['evidence_rows']})
result['combined_analyst_footprint'] = {
    'http_requests': len(all_http),
    'response_body_bytes': sum(row['bytes'] for row in all_http),
    'summed_http_elapsed_seconds': round(sum(row['elapsed_seconds'] for row in all_http), 3),
    'source_ids_attempted': len(source_ids),
    'unique_substantive_endpoints_attempted': len(all_endpoints),
    'readable_substantive_documents': sum(item['source_access_counts'].get('readable', 0) for item in result['iterations'].values()),
    'discovery_queries': sum(item['discovery_queries'] for item in result['iterations'].values()),
}
for f in (p / 'LH052.md', p / 'synthesis.md'):
    if f.exists():
        inputs.append(f)
for f in (Path('investigations/ai-cost-and-spread.md'), Path('programme.md'), Path('proposals.md')):
    if f.exists():
        inputs.append(f)
result['reviewed_input_sha256'] = {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs if f.exists()}
print(json.dumps(result, indent=2))
