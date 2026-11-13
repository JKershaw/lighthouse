#!/usr/bin/env python3
"""Offline retained-data counts for the LH052 reader-and-inference review."""
import collections
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
cases = list(csv.DictReader((root / 'cases.csv').open()))
measurements = list(csv.DictReader((root / 'operator-measurements.csv').open()))
logs = [json.loads(line) for i in (1, 2)
        for line in (root / f'reads-iteration-{i}.jsonl').read_text().splitlines()]
http = [row for row in logs if row['type'] == 'http_request']
sources = [source for i in (1, 2)
           for source in json.loads((root / f'sources-iteration-{i}.json').read_text())['sources']]
result = {
    'case_source_field_rows': len(cases),
    'distinct_outage_cases': len({row['case_id'] for row in cases}),
    'case_field_classifications': dict(collections.Counter(row['classification'] for row in cases)),
    'operator_measurement_rows': len(measurements),
    'readable_documents': sum(source['substantive_access'] == 'readable' for source in sources),
    'http_requests': len(http),
    'response_body_bytes': sum(row['bytes'] for row in http),
    'summed_http_elapsed_seconds': round(sum(row['elapsed_seconds'] for row in http), 3),
    'discovery_queries': sum(row.get('query_count', 0) for row in logs if row['type'] == 'discovery'),
    'interpretation': 'Coding and access counts only; no private telemetry or causal effect reproduced.',
}
print(json.dumps(result, indent=2))
