#!/usr/bin/env python3
"""LH008 steps 2 to 4, by brief.md and its first amendment.

frame   Open Source Insights' direct dependents for the eight versions (the release before each fixed
        release and before each comparison release); SHA-256 order of the normalised name; the first 60
        per frame marked for screening. Writes data/frame_counts.csv and data/frame.csv. No repository
        is cloned.
screen  For each marked package: the repository (Open Source Insights v3, then PyPI's project URLs); a
        blobless clone in LH008_SCRATCH; the snapshot commit (last first-parent commit on the default
        branch at or before the release time); the pinning and locking files there and the version each
        holds. Writes data/screen.csv and data/snapshot_files.csv.
moves   For each kept repository: every first-parent commit after the snapshot that touches a pin or
        lock file, read in order to the first move (or removal, or the head); the moving commit's times
        and authorship. Writes data/moves.csv and data/move_steps.csv.

Usage: LH008_SCRATCH=/tmp/lh008 python3 collect.py frame|screen|moves"""
import hashlib, json, os, re, shutil, subprocess, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version, InvalidVersion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, jget, write_csv, read_csv, git, SCRATCH, now, log, ts, iso, norm

N_SCREEN = 60
CAP_BYTES = 3 * 1024 ** 3
MAX_COMMITS = 400
q = lambda s: urllib.parse.quote(s, safe='')


def V(s):
    try:
        return Version(s)
    except (InvalidVersion, TypeError):
        return None


def frames():
    """The eight frames: (frame id, library, kind, frame version, threshold version, release time)."""
    out = []
    for e in read_csv('events.csv'):
        if e['chosen'] != 'yes':
            continue
        out.append(dict(frame=f"{norm(e['library'])}:fix", library=e['library'], kind='fix',
                        frame_version=e['release_before_fix'], threshold=e['fixed_release'],
                        release_time=e['fixed_uploaded'], advisory_time=e['advisory_published']))
        out.append(dict(frame=f"{norm(e['library'])}:comparison", library=e['library'], kind='comparison',
                        frame_version=e['release_before_comparison'], threshold=e['comparison_release'],
                        release_time=e['comparison_uploaded'], advisory_time=''))
    return out


# ---------------------------------------------------------------- frame

def frame():
    rows, counts = [], []
    for f in frames():
        d = jget('Open Source Insights', f"deps.dev dependents {f['library']} {f['frame_version']}",
                 f"https://deps.dev/_/s/pypi/p/{q(norm(f['library']))}/v/{q(f['frame_version'])}/dependents")
        counts.append(dict(frame=f['frame'], library=f['library'], version=f['frame_version'],
                           total=d.get('totalCount', '') if d else 'not served',
                           direct=d.get('directCount', '') if d else '', indirect=d.get('indirectCount', '') if d else '',
                           direct_listed=len(d.get('directSample', [])) if d else 0, read_utc=now()))
        seen = {}
        for e in (d or {}).get('directSample', []):
            n = norm(e['package']['name'])
            if n not in seen:
                seen[n] = dict(frame=f['frame'], library=f['library'], package=e['package']['name'], norm=n,
                               sha256=hashlib.sha256(n.encode()).hexdigest(), listed_version=e['version'])
        fr = sorted(seen.values(), key=lambda r: r['sha256'])
        for i, r in enumerate(fr, 1):
            r['hash_rank'] = i
            r['screened'] = 'yes' if i <= N_SCREEN else 'no (beyond the screening limit)'
        rows += fr
    write_csv('frame_counts.csv', counts)
    write_csv('frame.csv', rows, ['frame', 'library', 'hash_rank', 'package', 'norm', 'sha256', 'listed_version', 'screened'])
    for c in counts:
        print(c)


# ---------------------------------------------------------------- repository

def repo_from_version(name, ver):
    v = jget('Open Source Insights', f'deps.dev version {name} {ver}',
             f'https://api.deps.dev/v3/systems/pypi/packages/{q(name)}/versions/{q(ver)}') or {}
    for rp in v.get('relatedProjects', []):
        if rp['relationType'] == 'SOURCE_REPO':
            return rp['projectKey']['id'].lower(), 'deps.dev relation'
    for l in v.get('links', []):
        u = l['url'].lower().rstrip('/')
        for host in ('github.com/', 'gitlab.com/'):
            if host in u and l['label'] in ('SOURCE_REPO', 'HOMEPAGE'):
                parts = u.split(host)[1].split('/')
                if len(parts) >= 2 and parts[1]:
                    return host + parts[0] + '/' + parts[1].removesuffix('.git'), 'deps.dev link'
    return None, None


def repo_from_pypi(pj):
    urls = list((pj['info'].get('project_urls') or {}).items()) + [('home_page', pj['info'].get('home_page') or '')]
    urls.sort(key=lambda kv: 0 if kv[0].lower() in ('source', 'repository', 'source code', 'code', 'github') else 1)
    for _, u in urls:
        u = (u or '').lower().rstrip('/')
        for host in ('github.com/', 'gitlab.com/'):
            if host in u:
                parts = u.split(host)[1].split('/')
                if len(parts) >= 2 and parts[1]:
                    return host + parts[0] + '/' + parts[1].removesuffix('.git').split('#')[0], 'PyPI project_urls'
    return None, None


_REPO = {}


def find_repo(pkg, ver):
    k = (pkg, ver)
    if k not in _REPO:
        r, via = repo_from_version(pkg, ver)
        if not r:
            pj = jget('PyPI JSON API', f'PyPI {pkg} {ver}', f'https://pypi.org/pypi/{q(pkg)}/{q(ver)}/json')
            if pj:
                r, via = repo_from_pypi(pj)
        if not r:
            pj = jget('PyPI JSON API', f'PyPI {pkg}', f'https://pypi.org/pypi/{q(pkg)}/json')
            if pj:
                r, via = repo_from_pypi(pj)
        _REPO[k] = (r or '', via or '')
    return _REPO[k]


def repo_dir(repo):
    return os.path.join(SCRATCH, 'repos', repo.replace('/', '__'))


def du(path):
    p = subprocess.run(['du', '-sb', path], capture_output=True, text=True)
    return int(p.stdout.split()[0]) if p.returncode == 0 and p.stdout else 0


import threading
_CLONE_LOCKS = {}
_GLOBAL = threading.Lock()


def clone(repo, pkg):
    d = repo_dir(repo)
    with _GLOBAL:
        lk = _CLONE_LOCKS.setdefault(repo, threading.Lock())
    with lk:
        if os.path.exists(os.path.join(d, 'HEAD')) or os.path.exists(os.path.join(d, '.git')):
            return 'already cloned'
        if du(os.path.join(SCRATCH, 'repos')) > CAP_BYTES:
            return 'not cloned: 3 GB ceiling reached'
        url = 'https://' + repo + '.git'
        t = now()
        try:
            git(['clone', '-q', '--filter=blob:none', '--no-checkout', url, d], timeout=900)
            st = 'cloned'
        except Exception as ex:
            st = 'failed: ' + str(ex)[:160].replace('\n', ' ')
            shutil.rmtree(d, ignore_errors=True)
        log(read_utc=t, source='git over HTTPS', label=f'clone {pkg}', method='git clone --filter=blob:none --no-checkout',
            endpoint=url, http_status='', bytes=du(d) if st == 'cloned' else '', note=st)
        return st


# ---------------------------------------------------------------- pins and locks

SKIP = re.compile(r'(?i)(^|/)(tests?|testing|test_[^/]*|[^/]*_tests?|examples?|[^/]*_examples?|docs?)/|(^|/)(\.venv|venv|site-packages|vendor|node_modules|third_party)/')


def candidate(path):
    if path.count('/') > 3 or SKIP.search(path):
        return None
    b = path.rsplit('/', 1)[-1]
    if b in ('uv.lock', 'poetry.lock', 'pdm.lock', 'Pipfile.lock'):
        return 'lockfile'
    if b in ('pyproject.toml', 'setup.py', 'setup.cfg', 'Pipfile'):
        return 'manifest'
    if re.search(r'(?i)requirements[^/]*\.txt$', b) or (re.search(r'(?i)(^|/)requirements/', path) and b.endswith('.txt')):
        return 'requirements'
    return None


GENERATED = re.compile(r'(?i)autogenerated by pip-compile|uv pip compile|this file was autogenerated by uv|uv export|pdm export|poetry export|generated by pip-compile')


def lib_re(lib):
    n = re.escape(norm(lib)).replace(r'\-', '[-_.]')
    return n


def versions_in(path, text, lib, kind):
    """(class, [versions]) the file holds for the library: 'lockfile' or 'exact pin', or (None, [])."""
    n = lib_re(lib)
    b = path.rsplit('/', 1)[-1]
    if kind == 'lockfile' and b != 'Pipfile.lock':
        vs = []
        for blk in re.split(r'\n\[\[package\]\]', '\n' + text):
            m = re.search(r'^name\s*=\s*"([^"]+)"', blk, re.M)
            if m and norm(m.group(1)) == norm(lib):
                mv = re.search(r'^version\s*=\s*"([^"]+)"', blk, re.M)
                if mv:
                    vs.append(mv.group(1))
        return ('lockfile', vs) if vs else (None, [])
    if b == 'Pipfile.lock':
        try:
            j = json.loads(text)
        except Exception:
            return (None, [])
        vs = [x.get('version', '').lstrip('=') for sec in ('default', 'develop') for k, x in (j.get(sec) or {}).items()
              if norm(k) == norm(lib) and isinstance(x, dict) and x.get('version', '').startswith('==')]
        return ('lockfile', vs) if vs else (None, [])
    pat = re.compile(r'(?i)(?<![\w.\-/])' + n + r'(\[[^\]]*\])?\s*===?\s*([0-9][^\s"\',;#\\)\]*]*)(?![*\w.])')
    vs = [m.group(2) for m in pat.finditer(text)]
    if b == 'pyproject.toml' or b == 'Pipfile':
        for m in re.finditer(r'(?im)^\s*"?' + n + r'"?\s*=\s*(?:\{[^}\n]*version\s*=\s*)?"(?:==)?([0-9][0-9A-Za-z.+!-]*)"', text):
            vs.append(m.group(1))
    vs = [v for v in vs if V(v)]
    if not vs:
        return (None, [])
    if kind == 'requirements' and GENERATED.search(text[:3000]):
        return ('lockfile', vs)
    return ('exact pin', vs)


def show(d, rev, path):
    try:
        return git(['show', f'{rev}:{path}'], cwd=d, timeout=300)
    except Exception:
        return None


def holdings(d, rev, paths, lib):
    """{path: (class, [versions])} for the candidate paths at rev that pin or lock the library."""
    out = {}
    for p in paths:
        k = candidate(p)
        if not k:
            continue
        txt = show(d, rev, p)
        if txt is None:
            continue
        c, vs = versions_in(p, txt, lib, k)
        if c:
            out[p] = (c, vs)
    return out


def fmt_hold(h):
    return '; '.join(f"{p} [{c}] {','.join(vs)}" for p, (c, vs) in sorted(h.items()))


# ---------------------------------------------------------------- screen

def screen_one(row, f):
    pkg = row['package']
    out = dict(frame=row['frame'], library=row['library'], hash_rank=row['hash_rank'], package=pkg,
               listed_version=row['listed_version'], repo='', repo_via='', clone='', default_branch='',
               release_time=f['release_time'], threshold=f['threshold'], snapshot_commit='', snapshot_time='',
               candidate_files=0, holdings='', pin_class='', held_min='', kept='no', reason='')
    r, via = find_repo(pkg, row['listed_version'])
    out['repo'], out['repo_via'] = r, via
    if not r:
        out['reason'] = 'no repository named'
        return out, []
    st = clone(r, pkg)
    out['clone'] = st.split(':')[0]
    if not (st.startswith('cloned') or st.startswith('already')):
        out['reason'] = 'repository not cloned: ' + st
        return out, []
    d = repo_dir(r)
    try:
        out['default_branch'] = git(['symbolic-ref', '--short', 'HEAD'], cwd=d).strip()
        snap = git(['rev-list', '-1', '--first-parent', f"--before={iso(ts(f['release_time']))}", 'HEAD'], cwd=d).strip()
    except Exception as ex:
        out['reason'] = 'git error: ' + str(ex)[:100]
        return out, []
    if not snap:
        out['reason'] = 'no commit on the default branch at or before the release time'
        return out, []
    out['snapshot_commit'] = snap[:12]
    out['snapshot_time'] = git(['show', '-s', '--format=%cI', snap], cwd=d).strip()
    paths = [p for p in git(['ls-tree', '-r', '--name-only', snap], cwd=d).splitlines() if candidate(p)]
    paths.sort(key=lambda p: (p.count('/'), p))
    out['candidate_files'] = len(paths)
    h = holdings(d, snap, paths[:80], row['library'])
    out['holdings'] = fmt_hold(h)
    classes = sorted({c for c, _ in h.values()})
    out['pin_class'] = ' and '.join(classes) if classes else 'not pinned'
    allv = [v for _, vs in h.values() for v in vs]
    thr = V(f['threshold'])
    below = [v for v in allv if V(v) < thr]
    out['held_min'] = min(allv, key=V) if allv else ''
    if not h:
        out['reason'] = 'no exact pin or lockfile holding the library at the snapshot'
    elif not below:
        out['reason'] = 'pinned or locked, but already at or above ' + f['threshold']
    else:
        out['kept'] = 'yes'
        out['reason'] = 'holds ' + ','.join(sorted(set(below), key=V)) + ' below ' + f['threshold']
    files = [dict(frame=row['frame'], package=pkg, repo=r, snapshot_commit=snap[:12], path=p, pin_class=c, versions=','.join(vs))
             for p, (c, vs) in sorted(h.items())]
    print(row['frame'], row['hash_rank'], pkg, r, out['pin_class'], out['kept'], flush=True)
    return out, files


def screen():
    os.makedirs(os.path.join(SCRATCH, 'repos'), exist_ok=True)
    F = {f['frame']: f for f in frames()}
    rows = [r for r in read_csv('frame.csv') if r['screened'] == 'yes']
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: screen_one(r, F[r['frame']]), rows))
    write_csv('screen.csv', [o for o, _ in res])
    write_csv('snapshot_files.csv', [x for _, fs in res for x in fs] or [dict(frame='')],
              ['frame', 'package', 'repo', 'snapshot_commit', 'path', 'pin_class', 'versions'])


# ---------------------------------------------------------------- moves

BOT = re.compile(r'(?i)\[bot\]|dependabot|renovate|pre-commit-ci|github-actions|snyk|pyup|mergify|depfu|whitesource|mend-bolt|'
                 r'(^|[\s._-])bot$|-bot\b|\bbot\b|^bot[-_]')
BOT_BRANCH = re.compile(r'(?i)\bfrom\s+[^/\s]+/(dependabot|renovate|pre-commit-ci|snyk|pyup|mergify|update-dependencies|deps-bot)[/\-]|'
                        r'\b(dependabot|renovate)/(pip|uv|poetry|pipenv|pip_requirements|pep621|python|lock|[a-z0-9_.-]+)')
SEC = re.compile(r'(?i)security|vulnerab|GHSA-[a-z0-9]{4}|CVE-\d{4}|PYSEC-\d{4}')
AI = re.compile(r'(?im)^co-authored-by:.*(claude|anthropic|copilot|cursor|codex|openai|devin|gemini|aider|sweep|jules|amp\b)')
BOTTRAILER = re.compile(r'(?im)^co-authored-by:.*\[bot\]')


def meta(d, c):
    raw = git(['show', '-s', '--format=%H%x00%P%x00%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%B', c], cwd=d)
    k = raw.split('\x00')
    return dict(sha=k[0], parents=k[1].split(), an=k[2], ae=k[3], at=k[4], cn=k[5], ce=k[6], ct=k[7], msg=k[8].strip())


def is_bot(name, email):
    return bool(BOT.search(name or '')) or bool(re.search(r'(?i)\[bot\]@|dependabot|renovate|github-actions', email or ''))


def authorship(d, m):
    first_line = m['msg'].splitlines()[0] if m['msg'] else ''
    info = dict(author_is_bot='yes' if is_bot(m['an'], m['ae']) else 'no', bot_name=m['an'] if is_bot(m['an'], m['ae']) else '',
                committer_class='GitHub web' if m['ce'].lower() == 'noreply@github.com' else ('bot' if is_bot(m['cn'], m['ce']) else 'person'),
                merge='yes' if len(m['parents']) > 1 else 'no', merged_tip_author_is_bot='', merged_tip_bot='',
                message_first_line=first_line[:160], security_word='', ai_coauthor='', bot_coauthor='')
    text = m['msg']
    if len(m['parents']) > 1:
        t = meta(d, m['parents'][1])
        info['merged_tip_author_is_bot'] = 'yes' if is_bot(t['an'], t['ae']) else 'no'
        info['merged_tip_bot'] = t['an'] if is_bot(t['an'], t['ae']) else ''
        info['merged_tip_first_line'] = (t['msg'].splitlines()[0] if t['msg'] else '')[:160]
        text += '\n' + t['msg']
    if info['author_is_bot'] == 'yes':
        cls = 'bot'
    elif info['merge'] == 'yes' and (info['merged_tip_author_is_bot'] == 'yes' or BOT_BRANCH.search(m['msg'])):
        cls = "person merging a bot's branch"
        info['bot_name'] = info['merged_tip_bot'] or (BOT_BRANCH.search(m['msg']).group(0) if BOT_BRANCH.search(m['msg']) else '')
    else:
        cls = 'person'
    sw = SEC.findall(text)
    info['security_word'] = ' '.join(sorted(set(s.lower() if s.isalpha() else s for s in sw)))[:120]
    info['ai_coauthor'] = 'yes' if AI.search(text) else ''
    info['bot_coauthor'] = 'yes' if BOTTRAILER.search(text) else ''
    info['authorship'] = cls
    return info


def moves_one(s, f):
    d = repo_dir(s['repo'])
    lib, thr = s['library'], V(f['threshold'])
    snap = git(['rev-parse', s['snapshot_commit']], cwd=d).strip()
    head = git(['rev-parse', 'HEAD'], cwd=d).strip()
    base = dict(frame=s['frame'], library=lib, kind=f['kind'], package=s['package'], repo=s['repo'],
                default_branch=s['default_branch'], snapshot_commit=s['snapshot_commit'], held=s['holdings'],
                held_min=s['held_min'], threshold=f['threshold'], release_time=f['release_time'],
                advisory_time=f['advisory_time'], head_commit=head[:12],
                head_time=git(['show', '-s', '--format=%cI', head], cwd=d).strip())
    steps = []
    fp = git(['rev-list', '--first-parent', '--reverse', f'{snap}..{head}'], cwd=d).split()
    # first parent of each first-parent commit is the previous one in the list (the snapshot for the first)
    prev = snap
    pairs = []
    for c in fp:
        pairs.append((c, prev))
        prev = c
    changed = {}
    if pairs:
        p = subprocess.run(['git', 'diff-tree', '--stdin', '-r', '--name-only', '--no-renames'], cwd=d,
                           input='\n'.join(f'{c} {pp}' for c, pp in pairs) + '\n', capture_output=True, text=True, errors='replace')
        cur = None
        for line in p.stdout.splitlines():
            if re.fullmatch(r'[0-9a-f]{40}( [0-9a-f]{40})?', line):
                cur = line.split()[0]
                changed[cur] = []
            elif cur and line:
                changed[cur].append(line)
    state = {p: (c, vs.split(',')) for p, c, vs in
             [(x['path'], x['pin_class'], x['versions']) for x in SNAP.get((s['frame'], s['package']), [])]}
    held_below = {p for p, (c, vs) in state.items() if any(V(v) < thr for v in vs)}
    outcome, mv, n = 'censored at the head as cloned', None, 0
    for c in fp:
        touched = [p for p in changed.get(c, []) if candidate(p)]
        if not touched:
            continue
        n += 1
        if n > MAX_COMMITS:
            outcome = f'not moved within the first {MAX_COMMITS} commits touching pin or lock files (cap)'
            break
        h = holdings(d, c, touched, lib)
        for p in touched:
            if p in h:
                state[p] = h[p]
            else:
                state.pop(p, None)
        atleast = {p for p, (cl, vs) in state.items() if vs and all(V(v) >= thr for v in vs)}
        still = {p for p, (cl, vs) in state.items() if any(V(v) < thr for v in vs)}
        moved_files = [p for p in sorted(held_below) if p in atleast]
        gone = [p for p in sorted(held_below) if p not in state]
        steps.append(dict(frame=s['frame'], package=s['package'], commit=c[:12], touched=' '.join(touched)[:300],
                          state=fmt_hold(state)[:500]))
        if moved_files or (gone and atleast):
            outcome, mv = 'moved', c
            base['moved_files'] = ' '.join(moved_files or sorted(atleast))
            base['moved_to'] = ','.join(sorted({v for p in (moved_files or atleast) for v in state[p][1]}, key=V))
            base['all_files_moved'] = 'yes' if not still else 'no: ' + ' '.join(sorted(still))
            break
        if gone and not still and not atleast:
            outcome, mv = 'removed: no file pins or locks the library', c
            break
    base['outcome'] = outcome
    base['commits_read'] = n
    if mv:
        m = meta(d, mv)
        base.update(move_commit=mv[:12], committer_time=iso(ts(m['ct'])), author_time=iso(ts(m['at'])))
        base.update(authorship(d, m))
    print(s['frame'], s['package'], outcome, base.get('committer_time', ''), base.get('authorship', ''), flush=True)
    return base, steps


SNAP = {}


def moves():
    F = {f['frame']: f for f in frames()}
    for x in read_csv('snapshot_files.csv'):
        SNAP.setdefault((x['frame'], x['package']), []).append(x)
    kept, seen = [], set()
    for s in sorted([s for s in read_csv('screen.csv') if s['kept'] == 'yes'], key=lambda s: (s['frame'], int(s['hash_rank']))):
        if (s['frame'], s['repo']) not in seen:
            seen.add((s['frame'], s['repo']))
            kept.append(s)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda s: moves_one(s, F[s['frame']]), kept))
    fields = ['frame', 'library', 'kind', 'package', 'repo', 'default_branch', 'snapshot_commit', 'held', 'held_min',
              'threshold', 'release_time', 'advisory_time', 'outcome', 'commits_read', 'move_commit', 'committer_time',
              'author_time', 'moved_files', 'moved_to', 'all_files_moved', 'authorship', 'bot_name', 'author_is_bot',
              'committer_class', 'merge', 'merged_tip_author_is_bot', 'merged_tip_bot', 'message_first_line',
              'merged_tip_first_line', 'security_word', 'ai_coauthor', 'bot_coauthor', 'head_commit', 'head_time']
    write_csv('moves.csv', [b for b, _ in res], fields)
    write_csv('move_steps.csv', [x for _, st in res for x in st] or [dict(frame='')],
              ['frame', 'package', 'commit', 'touched', 'state'])


if __name__ == '__main__':
    {'frame': frame, 'screen': screen, 'moves': moves}[sys.argv[1]]()
