#!/usr/bin/env python3
"""Replay LH020 from retained bytes; keep distinct event and observation clocks."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'data' / 'snapshot-2026-10-21'
LH018 = ROOT.parent / 'LH018' / 'data' / 'snapshot-2026-10-21'
LH019 = ROOT.parent / 'LH019' / 'data' / 'snapshot-2026-10-21'
log = list(csv.DictReader((P / 'read_log.csv').open(newline='')))
assert len(log) <= 24
total = 0
raw = {}
for row in log:
    data = (ROOT / row['file']).read_bytes()
    assert len(data) == int(row['bytes']) and hashlib.sha256(data).hexdigest() == row['sha256'], row['key']
    assert row['status'] == '200' and not row['error'], row['key']
    total += len(data)
    raw[row['key']] = json.loads(data)
assert total <= 8 * 1024 * 1024

php = raw['php_pr_1694']
official = raw['official_pr_22541']
assert php['number'] == 1694 and official['number'] == 22541
assert len(raw['php_commits']) == 1 and len(raw['official_commits']) == 1
assert raw['php_commits'][0]['sha'] == php['head']['sha']
assert raw['official_commits'][0]['sha'] == official['head']['sha']
assert raw['php_checks']['total_count'] == len(raw['php_checks']['check_runs']) <= 100
assert raw['official_checks']['total_count'] == len(raw['official_checks']['check_runs']) <= 100
assert raw['official_run']['head_sha'] == official['head']['sha']
assert raw['official_run']['run_attempt'] == 2
assert raw['official_jobs']['total_count'] == len(raw['official_jobs']['jobs']) <= 100
assert all(job['conclusion'] == 'success' for job in raw['official_jobs']['jobs'])
for prefix, pr in [('php', php), ('official', official)]:
    assert any(e['event'] == 'merged' and e['created_at'] == pr['merged_at']
               for e in raw[prefix + '_events'])
    assert all(c['head_sha'] == pr['head']['sha'] for c in raw[prefix + '_checks']['check_runs'])

events = []


def add(boundary, event, value, source, precision='second', detail=''):
    if value:
        events.append(dict(boundary=boundary, event=event, source_time_utc=value,
                           precision=precision, evidence=source, detail=detail))


add('information', 'selected public issue opened', raw['php_issue_1693']['created_at'], 'php_issue_1693.raw',
    detail='first in this selected source set; readership unknown')
for prefix, pr in [('php', php), ('official', official)]:
    add('source' if prefix == 'php' else 'publisher', prefix + ' PR opened', pr['created_at'],
        prefix + '_pr_' + str(pr['number']) + '.raw')
    add('source' if prefix == 'php' else 'publisher', prefix + ' PR merged', pr['merged_at'],
        prefix + '_pr_' + str(pr['number']) + '.raw')
    for review in raw[prefix + '_reviews']:
        if review['state'] == 'APPROVED':
            add('review', prefix + ' approval', review['submitted_at'], prefix + '_reviews.raw')
for prefix in ('php', 'official'):
    checks = raw[prefix + '_checks']['check_runs']
    start = min((c['started_at'] for c in checks if c.get('started_at')), default='')
    end = max((c['completed_at'] for c in checks if c.get('completed_at')), default='')
    successes = sum(c['conclusion'] == 'success' for c in checks)
    add('CI', prefix + ' first selected-head check started', start, prefix + '_checks.raw',
        detail=f'{successes}/{len(checks)} check runs report success at retrieval')
    add('CI', prefix + ' last selected-head check completed', end, prefix + '_checks.raw',
        detail='across all returned check runs, not one workflow run')
for prefix in ('php', 'official'):
    if prefix + '_run' not in raw:
        continue
    run = raw[prefix + '_run']
    add('CI', prefix + ' selected run created', run['created_at'], prefix + '_run.raw',
        detail=f"attempt {run['run_attempt']}, conclusion {run['conclusion']}")
    add('CI', prefix + ' selected run started', run['run_started_at'], prefix + '_run.raw')
    jobs = raw[prefix + '_jobs']['jobs']
    add('CI', prefix + ' selected run last job completed',
        max((x['completed_at'] for x in jobs if x.get('completed_at')), default=''),
        prefix + '_jobs.raw', detail=f'{len(jobs)} jobs in retained page')

for tag in ('8.5.12-apache', '8.4.27-fpm', '8.3.36-cli', '8.2.35-fpm'):
    k = tag.replace('.', '_').replace('-', '_')
    d = json.loads((LH018 / ('hubtag_' + k + '.raw')).read_bytes())
    platform = next(x for x in d['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
    log18 = list(csv.DictReader((LH018 / 'read_log.csv').open(newline='')))
    read = next(x for x in log18 if x['kind'] == 'hubtag' and x['key'] == k)
    add('registry', tag + ' linux/amd64 platform pushed (Hub field)', platform['last_pushed'],
        'LH018/hubtag_' + k + '.raw', detail=platform['digest'])
    add('registry', tag + ' tag pushed (Hub field)', d['tag_last_pushed'],
        'LH018/hubtag_' + k + '.raw')
    add('observation', tag + ' first Lighthouse observation', read['observed_at_utc'],
        'LH018/read_log.csv')
for tag in ('8.5-apache', '8.4-fpm', '8.3-cli', '8.2-fpm'):
    k = tag.replace('.', '_').replace('-', '_')
    d = json.loads((LH019 / ('hubtag_' + k + '.raw')).read_bytes())
    read = next(x for x in csv.DictReader((LH019 / 'read_log.csv').open(newline=''))
                if x['kind'] == 'hubtag' and x['tag'] == tag)
    add('observation', tag + ' moving tag first Lighthouse observation', read['observed_at_utc'],
        'LH019/read_log.csv', detail=next(x['digest'] for x in d['images']
                                          if x.get('os') == 'linux' and x.get('architecture') == 'amd64'))

events.sort(key=lambda x: x['source_time_utc'])
with (ROOT / 'data' / 'events-2026-10-21.csv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=events[0].keys(), lineterminator='\n')
    writer.writeheader()
    writer.writerows(events)
print('Verified', len(log), 'API responses,', total, 'bytes;', len(events), 'timeline rows')
print('Checks:', raw['php_checks']['total_count'], 'PHP;', raw['official_checks']['total_count'], 'official')
print('Selected official run:', raw['official_run']['run_attempt'],
      raw['official_run']['conclusion'], raw['official_jobs']['total_count'], 'jobs')
