#!/usr/bin/env python3
"""Independent pinned LH032 review; does not import the production analyser.

Usage: python3 studies/LH032/review/check_source.py CLONE OUTPUT.json
Reads only git objects at the original source revision. OUTPUT must not exist.
"""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

PIN = '2fdc314ded280d18868d13d2f33d092a15e5a231'
CVES = ('CVE-2026-109618', 'CVE-2026-109619')
MAPPING = {'underInvestigationFor': 'Investigation', 'affects': 'Vulnerable',
           'fixedIn': 'Fix', 'doesNotAffect': 'Not vuln'}
CLONE = Path(sys.argv[1])
OUT = Path(sys.argv[2])
assert not OUT.exists(), 'Keep earlier review output; choose a new output name'


def git(*args):
    return subprocess.check_output(['git', '-C', str(CLONE), *args])


def projected(value):
    value = str(value or '').strip()
    for old, new in {'\u00a0': ' ', '\u2013': '-', '\u2014': '-', '\u2018': "'",
                     '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2192': '->'}.items():
        value = value.replace(old, new)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()
    return value.replace('\\', '\\\\').replace('|', '\\|')


def cells(line):
    """Scan separators, accounting for odd/even preceding backslash runs."""
    parts, text, escapes = [], '', 0
    for char in line:
        if char == '|' and escapes % 2 == 0:
            parts.append(text.strip())
            text = ''
        else:
            text += char
        escapes = escapes + 1 if char == '\\' else 0
    parts.append(text.strip())
    assert not parts[0] and not parts[-1], 'Expected outer table pipes'
    return parts[1:-1]


def markdown(sha):
    paths = git('ls-tree', '-r', '--name-only', sha).decode().splitlines()
    selected = [p for p in paths if re.fullmatch(r'software/software_list_[0-9a-z-]+\.md', p)]
    if not selected and 'software/software_list.md' in paths:
        selected = ['software/software_list.md']
    entries = {}
    for path in selected:
        for line in git('show', sha + ':' + path).decode().splitlines():
            if not line.startswith('|'):
                continue
            row = cells(line)
            if row[0].lower() == 'supplier' or re.fullmatch(r'[-: ]+', row[0]):
                continue
            assert len(row) == 7, (sha, path, row)
            key = tuple(row[:2])
            assert key not in entries, ('duplicate identity', sha, key)
            entries[key] = {'statuses': row[3:5], 'links': row[6]}
    return entries


paths = git('ls-tree', '-r', '--name-only', PIN).decode().splitlines()
fragments = [p for p in paths if re.fullmatch(r'software/spdx/(shared|segments)/.+\.json', p)]
source, hashes = {}, {}
for path in fragments:
    raw = git('show', PIN + ':' + path)
    hashes[path] = hashlib.sha256(raw).hexdigest()
    for element in json.loads(raw)['@graph']:
        key = element.get('spdxId') or element['@id']
        assert key not in source
        source[key] = element
compiled = json.loads(git('show', PIN + ':software/spdx/PHP_Downstream_Inventory.spdx3.json'))['@graph']
assert len(compiled) == len(source)
assert {e.get('spdxId') or e['@id']: e for e in compiled} == source
orgs = {k: e['name'] for k, e in source.items() if e['type'] == 'Organization'}
vulns = {k: e['name'] for k, e in source.items() if e['type'] == 'security_Vulnerability'}
statuses = collections.defaultdict(dict)
for element in source.values():
    if element['type'].startswith('security_Vex'):
        cve, status = vulns[element['from']], MAPPING[element['relationshipType']]
        for target in element['to']:
            assert statuses[target].get(cve, status) == status
            statuses[target][cve] = status
packages = {}
for key, element in source.items():
    if element['type'] != 'software_Package':
        continue
    name = (projected(orgs[element['suppliedBy']]), projected(element['name']))
    assert name not in packages
    urls, advisory_urls = [], []
    for ref in element.get('externalRef', []):
        locators = ref.get('locator', [])
        if isinstance(locators, str):
            locators = [locators]
        urls.extend(locators)
        if ref.get('externalRefType') == 'securityAdvisory':
            advisory_urls.extend(locators)
    packages[name] = {'statuses': [statuses[key].get(c, '') for c in CVES],
                      'url': any(u.startswith(('http://', 'https://')) for u in urls),
                      'advisory_url': any(u.startswith(('http://', 'https://')) for u in advisory_urls)}
head = markdown(PIN)
assert set(head) == set(packages)
for key, entry in head.items():
    assert entry['statuses'] == packages[key]['statuses']
    assert bool(re.search(r'https?://', entry['links'])) == packages[key]['url']

commits = [row.split(' ', 1) for row in git('log', '--first-parent', '--reverse', '--format=%H %cI', PIN).decode().splitlines()]
first, resolved, transitions, prior = {}, {}, collections.Counter(), {}
for sha, at in commits:
    current = markdown(sha)
    for key, entry in current.items():
        first.setdefault(key, at)
        if any(s in ('Fix', 'Not vuln') for s in entry['statuses']):
            resolved.setdefault(key, at)
        if entry['statuses'] != prior.get(key, {}).get('statuses'):
            transitions[key] += 1
    prior = current
release = datetime.datetime(2026, 10, 21, 13, 30, tzinfo=datetime.timezone.utc)
bins = collections.Counter()
for key in head:
    if key not in resolved:
        continue
    hours = (datetime.datetime.fromisoformat(resolved[key]) - release).total_seconds() / 3600
    label = 'before_release' if hours < 0 else '0_to_12' if hours < 12 else '12_to_24' if hours < 24 else '24_to_36' if hours < 36 else '36_to_48' if hours < 48 else '48_or_more'
    bins[label] += 1
root = Path(__file__).resolve().parents[1]
baseline = json.loads((root / 'data/read-2026-10-23T1850Z/entries.json').read_text())
url_corrections = []
first_clock_differences = resolved_clock_differences = 0
for row in baseline:
    key = (row['supplier'], row['product'])
    if row['links_vendor'] != packages[key]['url']:
        url_corrections.append({'supplier': key[0], 'product': key[1],
                                'original_url_flag': row['links_vendor'], 'source_url_flag': packages[key]['url']})
    first_clock_differences += row['first_listed'] != first[key]
    resolved_clock_differences += row['first_fix_or_not_vuln'] != resolved.get(key)
report = {'source_revision': PIN, 'source_fragments': len(fragments), 'source_elements': len(source),
          'source_fragment_hashes': hashes, 'source_matches_compiled': True,
          'identities_and_per_entry_statuses_and_url_presence_match_markdown': True,
          'entries': len(packages), 'entries_with_url': sum(e['url'] for e in packages.values()),
          'entries_with_advisory_typed_url': sum(e['advisory_url'] for e in packages.values()),
          'statuses': {c: dict(collections.Counter(e['statuses'][i] for e in packages.values())) for i, c in enumerate(CVES)},
          'mainline_commits': len(commits), 'first_resolution_bins_hours': dict(bins),
          'first_listed_clock_differences': first_clock_differences,
          'first_resolution_clock_differences': resolved_clock_differences,
          'surviving_entries_with_status_changes': sum(transitions[k] > 1 for k in head),
          'url_corrections': url_corrections}
OUT.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('source_fragment_hashes', 'url_corrections')}, indent=2))
