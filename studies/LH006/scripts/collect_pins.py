#!/usr/bin/env python3
"""LH006: each qualifying project's own statement of which mcp it wants, to set beside its images.
(1) git: every commit from 2026-01-01 to 2026-06-30 on the default branch that touched a manifest or
lockfile holding mcp (pyproject.toml, uv.lock, requirements*.txt, setup.py, poetry.lock), with the mcp
requirement and locked version after it; (2) PyPI: requires_dist for mcp of every release published in
the same span. Writes data/project_mcp_pins_git.csv and data/project_mcp_pins_pypi.csv."""
import os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH, http

A, B = '2026-01-01T00:00:00Z', '2026-06-30T23:59:59Z'
FILES = re.compile(r'(^|/)(pyproject\.toml|uv\.lock|poetry\.lock|setup\.py|requirements[^/]*\.txt)$')


def parse(path, txt):
    if path.endswith(('uv.lock', 'poetry.lock')):
        m = re.search(r'\[\[package\]\]\s*\nname = "mcp"\s*\nversion = "([^"]+)"', txt)
        return ('lock', m.group(1)) if m else ('lock', '')
    m = re.search(r'''["']?\bmcp(\[[^\]]*\])?\s*((?:[=<>!~]=?|===)\s*[0-9][^"',;\s\]]*(?:\s*,\s*[=<>!~]=?\s*[0-9][^"',;\s\]]*)*)''', txt)
    if m:
        return ('requirement', m.group(2).replace(' ', ''))
    m = re.search(r'''["']mcp(\[[^\]]*\])?["']''', txt)
    return ('requirement', 'unversioned' if m else '')


def main():
    grows, prows = [], []
    for c in read_csv('candidates.csv'):
        if c['qualifies'] != 'yes':
            continue
        pkg = c['package']
        if c['repo']:
            d = os.path.join(SCRATCH, 'repos', c['repo'].replace('/', '__'))
            paths = [p for p in git(['ls-tree', '-r', '--name-only', 'HEAD'], cwd=d).splitlines()
                     if FILES.search(p) and p.count('/') <= 3]
            log = git(['log', '--first-parent', f'--since={A}', f'--until={B}', '--format=%H %cI', '--'] + paths, cwd=d).split('\n') if paths else []
            for line in reversed([l for l in log if l.strip()]):
                sha, when = line.split()
                for p in paths:
                    try:
                        txt = git(['show', f'{sha}:{p}'], cwd=d)
                    except RuntimeError:
                        continue
                    kind, val = parse(p, txt)
                    if val:
                        grows.append(dict(package=pkg, commit=sha[:10], committed_utc=when, file=p, kind=kind, mcp=val))
        pj = http('PyPI JSON API', f'PyPI {pkg}', f'https://pypi.org/pypi/{urllib.parse.quote(pkg)}/json').json()
        for ver, files in pj['releases'].items():
            if not files:
                continue
            t = min(f['upload_time_iso_8601'] for f in files)
            if not (A <= t <= B):
                continue
            vj = http('PyPI JSON API', f'PyPI {pkg} {ver}', f'https://pypi.org/pypi/{urllib.parse.quote(pkg)}/{ver}/json').json()
            req = [r for r in (vj['info'].get('requires_dist') or []) if re.match(r'mcp\b(?![-_.\w])', r)]
            prows.append(dict(package=pkg, version=ver, published_utc=t, requires_mcp=' | '.join(req) or 'none'))
    # keep one row per change in git: drop rows equal to the previous row for the same file
    out, last = [], {}
    for r in grows:
        k = (r['package'], r['file'])
        if last.get(k) != r['mcp']:
            out.append(r)
            last[k] = r['mcp']
    write_csv('project_mcp_pins_git.csv', out, ['package', 'commit', 'committed_utc', 'file', 'kind', 'mcp'])
    prows.sort(key=lambda r: (r['package'], r['published_utc']))
    write_csv('project_mcp_pins_pypi.csv', prows, ['package', 'version', 'published_utc', 'requires_mcp'])


if __name__ == '__main__':
    main()
