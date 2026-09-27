#!/usr/bin/env python3
"""LH010 steps 3b to 3d, copied from LH009's collect.py and changed only where LH010's brief says:
- the frames are data/frame_defs.csv's rows not reused from LH008 or LH009 (osv_ranges.py): the events read
  fresh and the within-library second fixes;
- the first 20 packages of each frame are screened (not 60), in the order of the events' download rank;
- one 8 GB ceiling on everything in LH010_SCRATCH (the clones stop at 7.5 GB, leaving room for clones in flight);
- the kept rule reads each frame's own advisory's ranges (event_advisory_ranges.csv, keyed by frame), and each
  kept pair's fix is the `fixed` version of the range holding its lowest affected version, with that version's
  first upload as the pair's release time (pair_fix, pair_release_time);
- a move needs a followed file to hold only unaffected versions at or above the pair's fix;
- the time each repository's clone was made is kept with the pair (clone_utc) as its end of observation, since
  a clone may be deleted and made again for a later frame;
- the Co-authored-by names that trailers.py read are taken here, while the clone is present (ai_or_bot_coauthors);
- `clean` deletes the dependents' clones once their readings are written.

frame   Open Source Insights' direct dependents of each frame's release before the fix; SHA-256 order of the
        normalised name; the first 20 marked. Writes data/frame_counts.csv and data/frame.csv.
screen  For each marked package: repository, clone, snapshot, pin and lock files, kept or not. Writes
        data/screen.csv and data/snapshot_files.csv.
moves   For each kept pair: first-parent commits after the snapshot touching pin or lock files, to the first move,
        removal or the head. Writes data/moves.csv and data/move_steps.csv.

Usage: LH010_SCRATCH=/tmp/claude-0/lh010-work python3 collect.py frame|screen|moves|clean"""
import hashlib, json, os, re, shutil, subprocess, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version, InvalidVersion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, jget, write_csv, read_csv, git, SCRATCH, now, log, ts, iso, norm

N_SCREEN = 20
CAP_BYTES = int(7.5 * 1024 ** 3)
MAX_COMMITS = 400
q = lambda s: urllib.parse.quote(s, safe='')


def V(s):
    try:
        return Version(s)
    except (InvalidVersion, TypeError):
        return None


def frames():
    """The frames read here: (frame id, library, kind, frame version, threshold (fixed release), release time,
    advisory time, rank), in download order, events before second fixes."""
    out = []
    for f in read_csv('frame_defs.csv'):
        if f['reused'] != 'no':
            continue
        out.append(dict(frame=f['frame'], library=f['library'], kind=f['kind'], frame_version=f['release_before_fix'],
                        threshold=f['fixed_release'], release_time=f['fixed_uploaded'], advisory_time=f['advisory_published'],
                        rank=int(f['rank'])))
    return sorted(out, key=lambda f: (f['kind'] != 'event', f['rank']))


_RANGES = None
_REL = None


def _ranges(frame):
    global _RANGES
    if _RANGES is None:
        _RANGES = {r['frame']: json.loads(r['ranges']) for r in read_csv('event_advisory_ranges.csv')
                   if norm(r['package']) == norm(r['library'])}
    return _RANGES[frame]


def range_fix(frame, v):
    """The `fixed` version of the first ECOSYSTEM range of the frame's advisory that holds v, or None."""
    x = V(v)
    if x is None:
        return None
    for evs in _ranges(frame):
        state, fx = False, None
        for e in evs:
            if 'introduced' in e and (e['introduced'] == '0' or x >= V(e['introduced'])):
                state = True
            elif 'fixed' in e and x >= V(e['fixed']):
                state = False
            elif 'last_affected' in e and x > V(e['last_affected']):
                state = False
        if state:
            fx = next((e['fixed'] for e in evs if 'fixed' in e and V(e['fixed']) > x), None)
            return fx or 'none'
    return None


def affected(frame, v):
    """True if the frame's advisory's OSV ECOSYSTEM ranges, for the package named like the library, hold v."""
    return range_fix(frame, v) is not None


def uploaded(lib, v):
    global _REL
    if _REL is None:
        _REL = {(r['library'], r['version']): r['uploaded'] for r in read_csv('releases.csv')}
    return _REL.get((lib, v), '')


# ---------------------------------------------------------------- frame

def frame():
    rows, counts = [], []
    for f in frames():
        d = jget('Open Source Insights', f"deps.dev dependents {f['library']} {f['frame_version']}",
                 f"https://deps.dev/_/s/pypi/p/{q(norm(f['library']))}/v/{q(f['frame_version'])}/dependents")
        counts.append(dict(frame=f['frame'], library=f['library'], kind=f['kind'], version=f['frame_version'],
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
            r['screened'] = 'yes' if i <= N_SCREEN else 'no (beyond the screening limit of 20)'
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
CLONE_T = {}
_GLOBAL = threading.Lock()


def clone(repo, pkg):
    d = repo_dir(repo)
    with _GLOBAL:
        lk = _CLONE_LOCKS.setdefault(repo, threading.Lock())
    with lk:
        if os.path.exists(os.path.join(d, 'HEAD')) or os.path.exists(os.path.join(d, '.git')):
            return 'already cloned'
        if du(SCRATCH) > CAP_BYTES:
            return 'not cloned: disk ceiling reached'
        url = 'https://' + repo + '.git'
        t = now()
        try:
            git(['clone', '-q', '--filter=blob:none', '--no-checkout', url, d], timeout=900)
            st = 'cloned'
            CLONE_T[repo] = t
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
               candidate_files=0, holdings='', pin_class='', held_min='', kept='no', reason='', pair_fix='',
               pair_release_time='', clone_utc='')
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
    out['clone_utc'] = CLONE_T.get(r, '')
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
    below = [v for v in allv if affected(row['frame'], v)]
    out['held_min'] = min(allv, key=V) if allv else ''
    if not h:
        out['reason'] = 'no exact pin or lockfile holding the library at the snapshot'
    elif not below:
        out['reason'] = 'pinned or locked, but no held version is affected (at or above ' + f['threshold'] + ', or below the range)'
    else:
        out['kept'] = 'yes'
        low = min(below, key=V)
        out['pair_fix'] = range_fix(row['frame'], low)
        out['pair_release_time'] = uploaded(row['library'], out['pair_fix'])
        out['reason'] = 'holds ' + ','.join(sorted(set(below), key=V)) + ', affected (fixed in ' + out['pair_fix'] + ')'
    files = [dict(frame=row['frame'], package=pkg, repo=r, snapshot_commit=snap[:12], path=p, pin_class=c, versions=','.join(vs))
             for p, (c, vs) in sorted(h.items())]
    print(row['frame'], row['hash_rank'], pkg, r, out['pin_class'], out['kept'], flush=True)
    return out, files


def screen():
    os.makedirs(os.path.join(SCRATCH, 'repos'), exist_ok=True)
    F = {f['frame']: f for f in frames()}
    rank = {f['frame']: (f['kind'] != 'event', f['rank']) for f in F.values()}
    rows = sorted([r for r in read_csv('frame.csv') if r['screened'] == 'yes'], key=lambda r: (rank[r['frame']], int(r['hash_rank'])))
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
    lib, thr, fr = s['library'], V(s['pair_fix']), s['frame']
    snap = git(['rev-parse', s['snapshot_commit']], cwd=d).strip()
    head = git(['rev-parse', 'HEAD'], cwd=d).strip()
    base = dict(frame=s['frame'], library=lib, kind=f['kind'], package=s['package'], repo=s['repo'],
                default_branch=s['default_branch'], snapshot_commit=s['snapshot_commit'], held=s['holdings'],
                held_min=s['held_min'], threshold=f['threshold'], release_time=f['release_time'],
                advisory_time=f['advisory_time'], pair_fix=s['pair_fix'], pair_release_time=s['pair_release_time'],
                clone_utc=s['clone_utc'], head_commit=head[:12],
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
    held_below = {p for p, (c, vs) in state.items() if any(affected(fr, v) for v in vs)}
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
        atleast = {p for p, (cl, vs) in state.items() if vs and all(V(v) and (thr is None or V(v) >= thr) and not affected(fr, v) for v in vs)}
        still = {p for p, (cl, vs) in state.items() if any(affected(fr, v) for v in vs)}
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
        names = []
        for rev in [mv] + ([mv + '^2'] if base['merge'] == 'yes' else []):
            for l in git(['log', '-1', '--format=%B', rev], cwd=d, check=False).splitlines():
                if l.lower().startswith('co-authored-by:'):
                    n = re.sub(r'<[^>]*>', '', l.split(':', 1)[1]).strip()
                    if TRAILER_AI.search(n) or '[bot]' in n:
                        names.append(n)
        base['ai_or_bot_coauthors'] = '; '.join(dict.fromkeys(names))
    print(s['frame'], s['package'], outcome, base.get('committer_time', ''), base.get('authorship', ''), flush=True)
    return base, steps


SNAP = {}
TRAILER_AI = re.compile(r'(?i)claude|anthropic|copilot|cursor|codex|openai|chatgpt|devin|gemini|aider|sweep|jules')


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
              'threshold', 'release_time', 'advisory_time', 'pair_fix', 'pair_release_time', 'clone_utc', 'outcome', 'commits_read', 'move_commit', 'committer_time',
              'author_time', 'moved_files', 'moved_to', 'all_files_moved', 'authorship', 'bot_name', 'author_is_bot',
              'committer_class', 'merge', 'merged_tip_author_is_bot', 'merged_tip_bot', 'message_first_line',
              'merged_tip_first_line', 'security_word', 'ai_coauthor', 'bot_coauthor', 'ai_or_bot_coauthors', 'head_commit', 'head_time']
    write_csv('moves.csv', [b for b, _ in res], fields)
    write_csv('move_steps.csv', [x for _, st in res for x in st] or [dict(frame='')],
              ['frame', 'package', 'commit', 'touched', 'state'])


def clean():
    shutil.rmtree(os.path.join(SCRATCH, 'repos'), ignore_errors=True)
    print('deleted', os.path.join(SCRATCH, 'repos'))


if __name__ == '__main__':
    {'frame': frame, 'screen': screen, 'moves': moves, 'clean': clean}[sys.argv[1]]()
