#!/usr/bin/env python3
"""LH007 step 5, adapted from LH006: each sampled project's own statement of which mcp it wants.
(1) git: every first-parent commit on the default branch from 2026-04-01 to 2026-08-15 that touched a
manifest or lockfile (pyproject.toml, uv.lock, poetry.lock, setup.py, requirements*.txt, at most three
directories deep), with the mcp requirement or locked version after it, one row per change;
(2) PyPI: requires_dist for mcp of every release published in the same span, for each sampled package
and for the packages two images install from PyPI by name (mcp-proxy-for-aws, mcp-mesh).
Writes data/project_mcp_pins_git.csv and data/project_mcp_pins_pypi.csv."""
import os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH, http
from collect_builds import REPO, mcp_spec, lock_version

A, B = '2026-04-01T00:00:00Z', '2026-08-15T23:59:59Z'
FILES = re.compile(r'(^|/)(pyproject\.toml|uv\.lock|poetry\.lock|setup\.py|requirements[^/]*\.txt)$')
EXTRA_PYPI = ['mcp-proxy-for-aws', 'mcp-mesh']


def main():
    grows, prows = [], []
    repos = sorted({r for r, _ in REPO.values()})
    for repo in repos:
        d = os.path.join(SCRATCH, 'repos', repo.replace('/', '__'))
        if not os.path.exists(d):
            continue
        paths = [p for p in git(['ls-tree', '-r', '--name-only', 'HEAD'], cwd=d).splitlines()
                 if FILES.search(p) and p.count('/') <= 3 and 'test' not in p.lower() and 'example' not in p.lower()]
        log = git(['log', '--first-parent', f'--since={A}', f'--until={B}', '--format=%H %cI', '--'] + paths, cwd=d).split('\n') if paths else []
        last = {}
        for line in reversed([l for l in log if l.strip()]):
            sha, when = line.split()
            changed = set(git(['diff-tree', '--no-commit-id', '--name-only', '-r', '-m', '--first-parent', sha], cwd=d).split())
            for p in paths:
                if p not in changed and p in last:
                    continue
                try:
                    txt = git(['show', f'{sha}:{p}'], cwd=d)
                except RuntimeError:
                    continue
                if p.endswith(('uv.lock', 'poetry.lock')):
                    kind, val = 'lock', lock_version(txt)
                else:
                    kind, val = 'requirement', mcp_spec(txt)
                if val and last.get(p) != val:
                    grows.append(dict(repo=repo, commit=sha[:10], committed_utc=when, file=p, kind=kind, mcp=val))
                    last[p] = val
        print(repo, sum(1 for g in grows if g['repo'] == repo), flush=True)
    pkgs = list(dict.fromkeys([c['package'] for c in read_csv('sample.csv')] + EXTRA_PYPI))
    for pkg in pkgs:
        r = http('PyPI JSON API', f'PyPI {pkg}', f'https://pypi.org/pypi/{urllib.parse.quote(pkg)}/json')
        if r.status_code != 200:
            continue
        for ver, files in r.json()['releases'].items():
            if not files:
                continue
            t = min(f['upload_time_iso_8601'] for f in files)
            if not (A <= t <= B):
                continue
            vj = http('PyPI JSON API', f'PyPI {pkg} {ver}', f'https://pypi.org/pypi/{urllib.parse.quote(pkg)}/{ver}/json').json()
            req = [x for x in (vj['info'].get('requires_dist') or []) if re.match(r'(mcp|fastmcp)\b(?![-_.\w])', x)]
            prows.append(dict(package=pkg, version=ver, published_utc=t[:19] + 'Z', requires_mcp=' | '.join(req) or 'none'))
        print(pkg, sum(1 for p in prows if p['package'] == pkg), flush=True)
    write_csv('project_mcp_pins_git.csv', grows, ['repo', 'commit', 'committed_utc', 'file', 'kind', 'mcp'])
    prows.sort(key=lambda r: (r['package'], r['published_utc']))
    write_csv('project_mcp_pins_pypi.csv', prows, ['package', 'version', 'published_utc', 'requires_mcp'])


if __name__ == '__main__':
    main()
