#!/usr/bin/env python3
"""LH007 step 1b: an aid to the qualification decision, no network. For each screened package with a
cloned repository, read its CI workflows at the two commits screened and list the image names they
push (build-push-action `tags:`/`images:`, `docker push`, `--push -t`), with `${{ github.repository }}`,
`env.REGISTRY`/`env.IMAGE_NAME` style variables resolved from the same file where they are literal.
Writes data/candidate_images.csv. The decision itself is made in classify_candidates.py."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH

PUSH = re.compile(r'build-push-action|docker\s+push|--push|buildx\s+bake|docker/bake-action|ko\s+publish|jib', re.I)
IMG = re.compile(r'((?:ghcr\.io|docker\.io|quay\.io|registry\.gitlab\.com|public\.ecr\.aws|[a-z0-9.-]+\.azurecr\.io|[a-z0-9-]+-docker\.pkg\.dev)/[A-Za-z0-9_.${}\-/ ]+)', re.I)


def resolve(s, env, repo):
    owner_repo = '/'.join(repo.split('/')[1:3])
    s = re.sub(r'\$\{\{\s*github\.repository\s*\}\}', owner_repo, s)
    s = re.sub(r'\$\{\{\s*github\.repository_owner\s*\}\}', owner_repo.split('/')[0], s)
    s = re.sub(r'\$\{\{\s*github\.event\.repository\.name\s*\}\}', owner_repo.split('/')[1], s)
    for _ in range(3):
        s = re.sub(r'\$\{\{\s*env\.([A-Za-z_]+)\s*\}\}|\$\{?([A-Z_]+)\}?', lambda m: env.get(m.group(1) or m.group(2), m.group(0)), s)
    return s.lower()


def main():
    rows = []
    for f in read_csv('candidate_frame.csv'):
        if f['clone'] not in ('cloned', 'already cloned') or not f['repo']:
            continue
        d = os.path.join(SCRATCH, 'repos', f['repo'].replace('/', '__'))
        found = {}
        for label in ('head', 'period_end'):
            c = f[f'{label}_commit']
            if not c:
                continue
            paths = [p for p in git(['ls-tree', '-r', '--name-only', c], cwd=d).splitlines()
                     if p.startswith('.github/workflows/') and p.endswith(('.yml', '.yaml'))]
            for p in paths:
                try:
                    txt = git(['show', f'{c}:{p}'], cwd=d)
                except Exception:
                    continue
                if not PUSH.search(txt):
                    continue
                env = {}
                for m in re.finditer(r'^\s*([A-Z_]+)\s*:\s*["\']?([^"\'\n#]+?)["\']?\s*$', txt, re.M):
                    env.setdefault(m.group(1), m.group(2).strip())
                names = set()
                for m in re.finditer(r'(?:images|tags|image)\s*:\s*[|>]?\s*\n?((?:\s+[^\n]+\n?){0,6})', txt):
                    for line in m.group(1).splitlines()[:6]:
                        line = line.strip().strip('-').strip()
                        if '/' in line or '$' in line:
                            names.add(resolve(line.split(',')[0].split(':')[0] if not line.startswith(('ghcr', 'docker', 'quay')) else line, env, f['repo']))
                for m in re.finditer(r'(?:docker\s+push|-t|--tag)\s+["\']?([^\s"\']+)', txt):
                    names.add(resolve(m.group(1), env, f['repo']))
                for m in IMG.finditer(txt):
                    names.add(resolve(m.group(1).strip(), env, f['repo']))
                for n in names:
                    n = re.sub(r'(:|@).*$', '', n.split()[0]) if n.split() else ''
                    if n and not re.search(r'astral-sh|library/|postgres|redis|actions/', n):
                        found.setdefault(n, set()).add(f'{label}:{p.rsplit("/", 1)[-1]}')
        for n, where in sorted(found.items()):
            rows.append(dict(hash_rank=f['hash_rank'], package=f['package'], repo=f['repo'], image_name=n,
                             where=';'.join(sorted(where))))
    write_csv('candidate_images.csv', rows, ['hash_rank', 'package', 'repo', 'image_name', 'where'])
    for r in rows:
        print(r['hash_rank'], r['package'], r['image_name'], r['where'][:60])


if __name__ == '__main__':
    main()
