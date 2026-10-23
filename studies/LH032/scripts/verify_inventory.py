#!/usr/bin/env python3
"""Independently reconcile generated Markdown with pinned SPDX source fragments.

No upstream code is imported or executed. Historical reads without SPDX are left
for the Markdown history reader; this check requires SPDX at the selected head.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

CVES = ('CVE-2026-109618', 'CVE-2026-109619')
STATUS = {'underInvestigationFor': 'Investigation', 'affects': 'Vulnerable',
          'fixedIn': 'Fix', 'doesNotAffect': 'Not vuln'}


def git(clone, *args):
    return subprocess.check_output(['git', '-C', str(clone), *args])


def text_cell(value):
    """Match the published table's documented ASCII/Markdown representation."""
    text = str(value or '').strip()
    for old, new in {'\u00a0': ' ', '\u2013': '-', '\u2014': '-', '\u2018': "'",
                     '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2192': '->'}.items():
        text = text.replace(old, new)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return re.sub(r'\r?\n+', '<br>', text.replace('\\', '\\\\').replace('|', '\\|')).strip()


def table_cells(line):
    """Split only unescaped pipes (an even preceding backslash run)."""
    parts, start, slashes = [], 0, 0
    for i, char in enumerate(line.strip()):
        if char == '|' and slashes % 2 == 0:
            parts.append(line.strip()[start:i].strip())
            start = i + 1
        slashes = slashes + 1 if char == chr(92) else 0
    parts.append(line.strip()[start:].strip())
    if parts[0] or parts[-1]:
        raise ValueError('expected table boundary delimiters')
    return parts[1:-1]


def markdown_entries(clone, commit):
    result = {}
    files = git(clone, 'ls-tree', '-r', '--name-only', commit).decode().splitlines()
    for name in files:
        if not re.fullmatch(r'software/software_list(_[0-9a-z-]+)?\.md', name):
            continue
        header = None
        for line in git(clone, 'show', f'{commit}:{name}').decode().splitlines():
            if not line.startswith('|'):
                continue
            cells = table_cells(line)
            if cells[0].lower() == 'supplier':
                header = [c.lower() for c in cells]
                continue
            if header is None or set(''.join(cells)) <= set(':- '):
                continue
            if len(cells) != len(header):
                raise ValueError(f'malformed table row at {commit}:{name}')
            row = dict(zip(header, cells))
            key = (row['supplier'], row['product'])
            value = {'status': tuple(row.get('status ' + c.lower(), '') for c in CVES),
                     'version': row.get('version (see status)', row.get('version', '')),
                     'links': row.get('links', ''), 'notes': row.get('notes', '')}
            if key in result and result[key] != value:
                raise ValueError(f'conflicting table identity {key} at {commit}')
            result[key] = value
    return result


def verify(clone, commit):
    names = git(clone, 'ls-tree', '-r', '--name-only', commit).decode().splitlines()
    source_paths = [p for p in names if re.fullmatch(r'software/spdx/(segments|shared)/.+\.json', p)]
    if not source_paths:
        raise ValueError('No authoritative SPDX fragments at selected head; review schema before proceeding')
    graph, hashes = {}, {}
    for path in source_paths:
        raw = git(clone, 'show', f'{commit}:{path}')
        hashes[path] = hashlib.sha256(raw).hexdigest()
        for element in json.loads(raw)['@graph']:
            id_ = element.get('spdxId', element.get('@id'))
            assert id_, 'element has no identifier'
            if id_ in graph:
                raise ValueError(f'duplicate SPDX ID {id_}')
            graph[id_] = element
    compiled_path = 'software/spdx/PHP_Downstream_Inventory.spdx3.json'
    compiled_raw = git(clone, 'show', f'{commit}:{compiled_path}')
    compiled = json.loads(compiled_raw)['@graph']
    assert len(compiled) == len(graph)
    assert {e.get('spdxId', e.get('@id')): e for e in compiled} == graph, 'compiled inventory differs from source fragments'
    hashes[compiled_path] = hashlib.sha256(compiled_raw).hexdigest()
    orgs = {k: e['name'] for k, e in graph.items() if e['type'] == 'Organization'}
    vulnerabilities = {k: e['name'] for k, e in graph.items() if e['type'] == 'security_Vulnerability'}
    assert set(vulnerabilities.values()) == set(CVES), 'CVE panel/schema changed; review before proceeding'
    statuses = defaultdict(dict)
    for e in graph.values():
        if not e.get('type', '').startswith('security_Vex'):
            continue
        cve = vulnerabilities[e['from']]
        status = STATUS[e['relationshipType']]
        for target in e['to']:
            assert target in graph
            assert statuses[target].get(cve, status) == status, 'conflicting VEX status'
            statuses[target][cve] = status
    packages = {}
    source_rows = []
    for id_, e in graph.items():
        if e['type'] != 'software_Package':
            continue
        key = (text_cell(orgs[e['suppliedBy']]), text_cell(e['name']))
        assert key not in packages, 'supplier/product identity collision'
        value = {'status': tuple(statuses[id_].get(c, '') for c in CVES),
                 'version': text_cell(e.get('software_packageVersion'))}
        urls, advisories = [], []
        for ref in e.get('externalRef', []):
            locators = ref.get('locator', [])
            locators = [locators] if isinstance(locators, str) else locators
            urls.extend(locators)
            if ref.get('externalRefType') == 'securityAdvisory':
                advisories.extend(locators)
        packages[key] = value
        source_rows.append({'id': id_, 'supplier': key[0], 'product': key[1],
                            'status': list(value['status']), 'urls': list(dict.fromkeys(urls)),
                            'advisory_urls': list(dict.fromkeys(advisories))})
    md = markdown_entries(clone, commit)
    assert set(md) == set(packages), 'Markdown/source product sets differ'
    for key, row in packages.items():
        assert row['status'] == md[key]['status'], f'status mismatch {key}'
        assert row['version'] == md[key]['version'], f'version mismatch {key}'
    return {'commit': commit, 'source_fragment_count': len(source_paths),
            'source_element_count': len(graph), 'source_packages': len(packages),
            'markdown_products': len(md), 'source_sha256': hashes,
            'status_counts': {c: dict(Counter(v['status'][i] for v in packages.values()))
                              for i, c in enumerate(CVES)},
            'entries_with_advisory_typed_url': sum(bool(r['advisory_urls']) for r in source_rows),
            'entries_with_external_url': sum(any(re.match(r'https?://', u) for u in r['urls'])
                                             for r in source_rows)}, sorted(source_rows, key=lambda r: (r['supplier'], r['product']))
