#!/usr/bin/env python3
"""Verify the retained first consumer snapshot and reconstruct a small feasibility table."""
import base64
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'data' / 'snapshot-2026-10-21'
log = list(csv.DictReader((P / 'read_log.csv').open(newline='')))
selection = json.loads((P / 'selection.json').read_text())
assert len(log) <= 36 and len(selection) == 3
raw = {}
total = 0
for row in log:
    data = (ROOT / row['file']).read_bytes()
    assert len(data) == int(row['bytes']) and hashlib.sha256(data).hexdigest() == row['sha256'], row['key']
    assert row['status'] == '200' and not row['error'], row['key']
    total += len(data)
    raw[row['key']] = json.loads(data)
assert total <= 12 * 1024 * 1024

rows = []
for item in selection:
    name = item['repo']
    key = name.replace('/', '_')
    repo = raw[key + '_repo']
    commit = raw[key + '_commit']
    tree = raw[key + '_tree']
    assert repo['full_name'] == name and commit['sha'] == item['head_sha']
    assert not tree['truncated'] and tree['sha'] == commit['commit']['tree']['sha']
    entries = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    chosen_docker = sorted(p for p in entries if p.rsplit('/', 1)[-1].startswith('Dockerfile'))[:4]
    chosen_workflow = sorted(p for p in entries if p.startswith('.github/workflows/')
                             and p.endswith(('.yml', '.yaml')))[:2]
    assert item['dockerfiles'] == chosen_docker and item['workflows'] == chosen_workflow
    bases = []
    unresolved = []
    for i, path in enumerate(chosen_docker + chosen_workflow):
        blob = raw[key + '_blob_' + str(i)]
        data = base64.b64decode(blob['content'])
        git_hash = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\x00' + data).hexdigest()
        assert git_hash == entries[path]['sha'] == blob['sha'], (name, path)
        if i < len(chosen_docker):
            for line in data.decode('utf-8', errors='replace').splitlines():
                match = re.match(r'^\s*FROM\s+(\S+)', line, re.I)
                if not match:
                    continue
                image = match.group(1)
                if image.startswith('php:') and re.fullmatch(r'php:[A-Za-z0-9_.-]+', image):
                    bases.append(path + ': ' + image)
                else:
                    unresolved.append(path + ': ' + image)
    run_list = raw[key + '_runs']
    runs = run_list['workflow_runs']
    assert len(runs) <= 10
    matched = [r for r in runs if r['head_sha'] == item['head_sha']]
    rows.append(dict(repo=name, head_sha=item['head_sha'], sampled_dockerfiles=len(chosen_docker),
                     sampled_workflows=len(chosen_workflow), literal_php_bases='; '.join(bases),
                     other_or_templated_bases='; '.join(unresolved),
                     recent_runs_returned=len(runs), runs_at_head=len(matched),
                     successful_runs_at_head=sum(r['conclusion'] == 'success' for r in matched),
                     run_times_at_head='; '.join(r['created_at'] for r in matched),
                     evidence=key + '_tree.raw; ' + key + '_runs.raw; ' +
                     '; '.join(key + '_blob_' + str(i) + '.raw' for i in range(len(chosen_docker + chosen_workflow)))))

with (ROOT / 'data' / 'summary-2026-10-21.csv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print('Verified', len(log), 'responses,', total, 'retained bytes')
for r in rows:
    print(r['repo'], 'literal PHP bases', r['literal_php_bases'].count('php:'),
          'runs at sampled head', r['runs_at_head'])
