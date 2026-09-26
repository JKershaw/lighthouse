#!/usr/bin/env python3
"""LH002 git readings for the cohort over the fixed window.

Usage: python3 collect_git.py <scratch_dir> <study_dir>
Expects blobless clones at <scratch_dir>/clones/Rnn (see brief.md for the list), made with
  git clone --filter=blob:none --no-checkout https://github.com/OWNER/REPO.git Rnn
and optionally Rnn-full, a shallow clone with contents
  git clone --no-checkout --shallow-since=2026-03-01 --no-single-branch URL Rnn-full
Personal identifiers (names, addresses) are written only under <scratch_dir>.
Published tables go to <study_dir>/data/ and hold counts, classes and pseudonyms.
"""
import csv, collections, datetime as dt, json, os, re, subprocess, sys, tomllib

S, STUDY = sys.argv[1], sys.argv[2]
CL = os.path.join(S, 'clones')
DATA = os.path.join(STUDY, 'data'); os.makedirs(DATA, exist_ok=True)
W0 = dt.datetime(2026, 3, 26, tzinfo=dt.timezone.utc)
W1 = dt.datetime(2026, 4, 23, tzinfo=dt.timezone.utc)  # exclusive end
DAYS = [(W0 + dt.timedelta(days=i)).date() for i in range(28)]
REPOS = [l.split() for l in open(os.path.join(S, 'repos.txt')) if l.strip()]

LOCKS = ('uv.lock', 'poetry.lock', 'pipfile.lock', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'pdm.lock')
VENDOR = re.compile(r'(^|/)(vendor|_vendor|vendored|third_party)/')
MANIFEST = re.compile(r'(^|/)(pyproject\.toml|setup\.py|setup\.cfg|pipfile|[^/]*requirements[^/]*\.txt)$', re.I)
PYLOCK = re.compile(r'(^|/)(uv\.lock|poetry\.lock|pdm\.lock)$', re.I)
BOT = re.compile(r'\[bot\]|dependabot|renovate|github-actions|pre-commit-ci|mergify|snyk-bot|semantic-release|allcontributors|actions-user|github-merge-queue', re.I)
DEPBOT = re.compile(r'dependabot|renovate|snyk-bot|pyup', re.I)
AGENTBOT = re.compile(r'copilot|claude|cursor|devin|codex|openhands|jules|sweep|codegen|gemini|aider', re.I)
AITRAILER = re.compile(r'^(co-authored-by|generated[- ]with|generated[- ]by|assisted-by)\s*:?.*\b(claude|copilot|cursor|codex|devin|gemini|aider|openhands|jules|chatgpt|windsurf|amp)\b', re.I | re.M)

def git(repo, *args, check=True):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, errors='replace')
    if check and r.returncode:
        raise RuntimeError(f'git {args[:2]} in {repo}: {r.stderr[:300]}')
    return r.stdout

def author_class(name, email):
    s = f'{name} {email}'
    if BOT.search(s) or (AGENTBOT.search(name) and 'noreply' in email.lower() and '[bot]' in s.lower()):
        if DEPBOT.search(s): return 'bot', 'dependency-update bot'
        if AGENTBOT.search(s): return 'bot', 'AI coding tool identity'
        return 'bot', 'other bot'
    if re.search(r'(cursoragent@cursor\.com|noreply@anthropic\.com|devin-ai-integration|\+copilot@users\.noreply\.github\.com)', email, re.I):
        return 'bot', 'AI coding tool identity'
    if email.lower().endswith('@users.noreply.github.com'):
        return 'human account', 'GitHub noreply address, not marked as bot'
    return 'unknown', 'no bot marker, not a GitHub noreply address'

def ts(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(dt.timezone.utc)

# ---------- requirement parsing ----------
NAME = re.compile(r'^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(\[[^\]]*\])?\s*(.*)$')
def norm(n): return re.sub(r'[-_.]+', '-', n).lower()
def split_req(s):
    s = s.split(';')[0].strip() if ';' in s else s.strip()
    m = NAME.match(s)
    if not m: return None
    return norm(m.group(1)), re.sub(r'\s+', '', m.group(3))

def reqs_from_text(path, text):
    out = {}
    low = path.lower()
    try:
        if low.endswith('pyproject.toml'):
            t = tomllib.loads(text)
            p = t.get('project', {})
            for r in p.get('dependencies', []) or []:
                x = split_req(r); x and out.__setitem__(('project', x[0]), x[1])
            for g, rs in (p.get('optional-dependencies') or {}).items():
                for r in rs:
                    x = split_req(r); x and out.__setitem__((f'extra:{g}', x[0]), x[1])
            for g, rs in (t.get('dependency-groups') or {}).items():
                for r in rs:
                    if isinstance(r, str):
                        x = split_req(r); x and out.__setitem__((f'group:{g}', x[0]), x[1])
            for r in (t.get('tool', {}).get('uv', {}).get('dev-dependencies') or []):
                x = split_req(r); x and out.__setitem__(('uv-dev', x[0]), x[1])
            po = t.get('tool', {}).get('poetry', {})
            groups = {'poetry': po.get('dependencies') or {}}
            for g, gd in (po.get('group') or {}).items():
                groups[f'poetry:{g}'] = gd.get('dependencies') or {}
            for g, deps in groups.items():
                for n, v in deps.items():
                    if norm(n) == 'python': continue
                    out[(g, norm(n))] = json.dumps(v, sort_keys=True) if not isinstance(v, str) else v
        elif low.endswith('pipfile'):
            t = tomllib.loads(text)
            for g in ('packages', 'dev-packages'):
                for n, v in (t.get(g) or {}).items():
                    out[(g, norm(n))] = v if isinstance(v, str) else json.dumps(v, sort_keys=True)
        elif low.endswith('.txt'):
            for line in text.splitlines():
                line = line.split('#')[0].strip()
                if not line or line.startswith('-'): continue
                x = split_req(line); x and out.__setitem__(('req', x[0]), x[1])
        elif low.endswith('setup.cfg'):
            m = re.search(r'install_requires\s*=\s*\n((?:[ \t]+.*\n?)+)', text)
            if m:
                for line in m.group(1).splitlines():
                    x = split_req(line.strip()); x and out.__setitem__(('install_requires', x[0]), x[1])
        elif low.endswith('setup.py'):
            m = re.search(r'install_requires\s*=\s*\[(.*?)\]', text, re.S)
            if m:
                for r in re.findall(r'["\']([^"\']+)["\']', m.group(1)):
                    x = split_req(r); x and out.__setitem__(('install_requires', x[0]), x[1])
    except Exception as e:
        out[('PARSE-ERROR', type(e).__name__)] = str(e)[:80]
    return out

def locked_versions(text):
    out = {}
    for m in re.finditer(r'\[\[package\]\]\s*\nname\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', text):
        out[norm(m.group(1))] = m.group(2)
    return out

def show(repo, rev, path):
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True, text=True, errors='replace')
    return r.stdout if r.returncode == 0 else None

# ---------- main ----------
authors = {}          # email -> dict(pseudonym, class, sub)  [scratch only]
pseudo_count = collections.Counter()
raw_commits = []
day_rows, dep_rows, lock_rows, state_rows, tag_rows, summary = [], [], [], [], [], []

def pseudonym(name, email):
    key = email.lower() or name.lower()
    if key not in authors:
        c, sub = author_class(name, email)
        pfx = {'bot': 'B', 'human account': 'H', 'unknown': 'U'}[c]
        pseudo_count[pfx] += 1
        authors[key] = dict(p=f'{pfx}{pseudo_count[pfx]:02d}', cls=c, sub=sub, name=name, email=email, repos=set())
    return authors[key]

for rid, slug in REPOS:
    repo = os.path.join(CL, rid)
    # A '-full' shallow clone with file contents, where present, serves line counts and
    # manifests (same commit hashes); the blobless clone serves history. Used for R06, whose
    # 1,482 window commits made lazy per-commit blob fetches impractical.
    crepo = os.path.join(CL, rid + '-full') if os.path.isdir(os.path.join(CL, rid + '-full')) else repo
    default = git(repo, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD').strip()
    fmt = '%H%x1f%P%x1f%an%x1f%ae%x1f%aI%x1f%cn%x1f%ce%x1f%cI%x1f%B%x1e'
    allc = {}
    for rec in git(repo, 'log', '--all', f'--format={fmt}').split('\x1e'):
        rec = rec.strip('\n')
        if not rec: continue
        f = rec.split('\x1f')
        allc[f[0]] = dict(h=f[0], parents=f[1].split(), an=f[2], ae=f[3], at=f[4], cn=f[5], ce=f[6], ct=f[7], msg=f[8])
    on_default = set(git(repo, 'rev-list', default).split())
    # every author in the repository's whole history, for the shared-maintainer test [scratch only]
    for c in allc.values():
        a = pseudonym(c['an'], c['ae']); a['repos'].add(rid)
    first = min(ts(c['ct']) for c in allc.values())
    win = sorted((c for c in allc.values() if W0 <= ts(c['ct']) < W1), key=lambda c: c['ct'])
    by_author_date = sum(1 for c in allc.values() if W0 <= ts(c['at']) < W1)
    hashes = [c['h'] for c in win if len(c['parents']) <= 1]
    numstat = {}
    if hashes:
        out = git(crepo, 'show', '--no-renames', '--numstat', '--format=@@%H', *hashes)
        cur = None
        for line in out.splitlines():
            if line.startswith('@@'): cur = line[2:]; numstat[cur] = []; continue
            parts = line.split('\t')
            if len(parts) == 3 and cur:
                a, d, p = parts
                numstat[cur].append((None if a == '-' else int(a), None if d == '-' else int(d), p))
    days = {d: collections.Counter() for d in DAYS}
    day_auth = {d: {'bot': set(), 'human account': set(), 'unknown': set()} for d in DAYS}
    for c in win:
        d = ts(c['ct']).date(); k = days[d]
        a = authors[(c['ae'].lower() or c['an'].lower())]
        k['commits'] += 1
        k['commits_default_branch'] += c['h'] in on_default
        k['merge_commits'] += len(c['parents']) > 1
        k[f"commits_{a['cls'].replace(' ', '_')}"] += 1
        k['commits_with_ai_tool_trailer'] += bool(AITRAILER.search(c['msg']))
        day_auth[d][a['cls']].add(a['p'])
        files = numstat.get(c['h'], [])
        for add, dele, p in files:
            if add is None: k['binary_file_changes'] += 1; continue
            col = 'lock' if p.lower().rsplit('/', 1)[-1] in LOCKS else 'vendored' if VENDOR.search(p) else 'other'
            k[f'additions_{col}'] += add; k[f'deletions_{col}'] += dele
        raw_commits.append(dict(repo=rid, h=c['h'], ct=c['ct'], at=c['at'], author=a['p'], cls=a['cls'], sub=a['sub'],
                                name=c['an'], email=c['ae'], parents=len(c['parents']), msg=c['msg'],
                                files=[p for _, _, p in files], numstat=files, default=c['h'] in on_default))
        # dependency changes: manifests and python lockfiles touched by a non-merge commit
        if len(c['parents']) == 1:
            for _, _, p in files:
                if MANIFEST.search(p):
                    before = reqs_from_text(p, show(crepo, c['parents'][0], p) or '')
                    after = reqs_from_text(p, show(crepo, c['h'], p) or '')
                    for key in sorted(set(before) | set(after)):
                        if before.get(key) != after.get(key):
                            kind = 'added' if key not in before else 'removed' if key not in after else 'changed'
                            dep_rows.append(dict(repo=rid, commit=c['h'][:10], committed=c['ct'], author_class=a['cls'],
                                                 author_subclass=a['sub'], file=p, section=key[0], package=key[1], change=kind,
                                                 before=before.get(key, ''), after=after.get(key, ''),
                                                 packages_changed_in_commit=None, message_first_line=None))
                    k['manifest_dependency_changes'] += sum(1 for key in set(before) | set(after) if before.get(key) != after.get(key))
                    k['mcp_requirement_changes'] += sum(1 for key in set(before) | set(after) if key[1] == 'mcp' and before.get(key) != after.get(key))
                elif PYLOCK.search(p):
                    b = locked_versions(show(crepo, c['parents'][0], p) or '')
                    af = locked_versions(show(crepo, c['h'], p) or '')
                    moved = sorted(n for n in set(b) | set(af) if b.get(n) != af.get(n))
                    k['lockfile_package_changes'] += len(moved)
                    if b.get('mcp') != af.get('mcp'):
                        k['lockfile_mcp_changes'] += 1
                    lock_rows.append(dict(repo=rid, commit=c['h'][:10], committed=c['ct'], author_class=a['cls'],
                                          author_subclass=a['sub'], file=p, packages_moved=len(moved),
                                          mcp_before=b.get('mcp', ''), mcp_after=af.get('mcp', '')))
    for r in dep_rows:
        if r['repo'] == rid and r['packages_changed_in_commit'] is None:
            r['packages_changed_in_commit'] = sum(1 for x in dep_rows if x['repo'] == rid and x['commit'] == r['commit'])
            msg = next(c['msg'] for c in win if c['h'].startswith(r['commit']))
            r['message_first_line'] = re.sub(r'\s+', ' ', msg.splitlines()[0])[:100] if msg else ''
            m = msg.lower()
            r['message_class'] = ('dependency-update wording' if re.search(r'\b(bump|deps?|dependenc|upgrade|update|lock)', m)
                                  else 'release wording' if re.search(r'\b(release|version|v\d+\.\d+)', m) else 'other')
    for d in DAYS:
        k = days[d]
        observed = d >= first.date()
        row = dict(repo=rid, date=d.isoformat(), status='observed' if observed else 'before first commit')
        for col in ('commits', 'commits_default_branch', 'merge_commits', 'commits_bot', 'commits_human_account',
                    'commits_unknown', 'commits_with_ai_tool_trailer', 'additions_other', 'deletions_other',
                    'additions_lock', 'deletions_lock', 'additions_vendored', 'deletions_vendored', 'binary_file_changes',
                    'manifest_dependency_changes', 'mcp_requirement_changes', 'lockfile_package_changes', 'lockfile_mcp_changes'):
            row[col] = k[col] if observed else ''
        for cls in ('bot', 'human account', 'unknown'):
            row[f"authors_{cls.replace(' ', '_')}"] = len(day_auth[d][cls]) if observed else ''
        day_rows.append(row)
    # mcp requirement and locked version at window start and end, on the default branch
    for label, t in (('start', W0), ('end', W1)):
        rev = git(repo, 'rev-list', '-1', f'--before={t.isoformat()}', default).strip()
        if not rev:
            state_rows.append(dict(repo=rid, at=label, commit='', manifests='', mcp_requirements='', locked_mcp='')); continue
        paths = git(crepo, 'ls-tree', '-r', '--name-only', rev).splitlines()
        mans = [p for p in paths if MANIFEST.search(p)]
        locks = [p for p in paths if PYLOCK.search(p)]
        reqs = []
        for p in mans:
            for key, v in reqs_from_text(p, show(crepo, rev, p) or '').items():
                if key[1] == 'mcp': reqs.append(f'{p}[{key[0]}]: mcp{v}')
        lk = [f'{p}: {locked_versions(show(crepo, rev, p) or "").get("mcp", "absent")}' for p in locks]
        state_rows.append(dict(repo=rid, at=label, commit=rev[:10], manifests=len(mans), mcp_requirements='; '.join(reqs),
                               locked_mcp='; '.join(lk)))
    for line in git(repo, 'for-each-ref', 'refs/tags', '--format=%(refname:short)%09%(creatordate:iso-strict)%09%(objecttype)').splitlines():
        name, when, typ = line.split('\t')
        if W0 <= ts(when) < W1:
            tag_rows.append(dict(repo=rid, tag=name, created=ts(when).isoformat(), tag_object=typ))
    wa = collections.Counter(authors[(c['ae'].lower() or c['an'].lower())]['cls'] for c in win)
    wauth = {cls: len({authors[(c['ae'].lower() or c['an'].lower())]['p'] for c in win
                        if authors[(c['ae'].lower() or c['an'].lower())]['cls'] == cls}) for cls in ('bot', 'human account', 'unknown')}
    obs_days = sum(1 for d in DAYS if d >= first.date())
    act = sum(1 for d in DAYS if days[d]['commits'])
    summary.append(dict(repo=rid, first_commit=first.date().isoformat(), commits_in_history=len(allc),
                        observed_days=obs_days, active_days=act, commits=len(win),
                        commits_by_author_date=by_author_date,
                        commits_per_observed_day=round(len(win) / obs_days, 2) if obs_days else '',
                        additions_other=sum(days[d]['additions_other'] for d in DAYS),
                        deletions_other=sum(days[d]['deletions_other'] for d in DAYS),
                        additions_lock=sum(days[d]['additions_lock'] for d in DAYS),
                        deletions_lock=sum(days[d]['deletions_lock'] for d in DAYS),
                        additions_vendored=sum(days[d]['additions_vendored'] for d in DAYS),
                        commits_bot=wa['bot'], commits_human_account=wa['human account'], commits_unknown=wa['unknown'],
                        authors_bot=wauth['bot'], authors_human_account=wauth['human account'], authors_unknown=wauth['unknown'],
                        commits_with_ai_tool_trailer=sum(days[d]['commits_with_ai_tool_trailer'] for d in DAYS),
                        tags=sum(1 for t in tag_rows if t['repo'] == rid),
                        manifest_dependency_changes=sum(days[d]['manifest_dependency_changes'] for d in DAYS),
                        lockfile_mcp_changes=sum(days[d]['lockfile_mcp_changes'] for d in DAYS)))

def write(name, rows):
    if not rows: open(os.path.join(DATA, name), 'w').write(''); return
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

write('repo_day.csv', day_rows)
write('repo_summary.csv', summary)
json.dump(dep_rows, open(os.path.join(S, 'manifest_dependency_changes_PRIVATE.json'), 'w'), indent=0)
write('manifest_dependency_changes.csv', [{k: v for k, v in r.items() if k != 'message_first_line'} for r in dep_rows])
write('lockfile_changes.csv', lock_rows)
write('mcp_state_window_start_end.csv', state_rows)
write('tags_in_window.csv', tag_rows)
# scratch only: raw commits with identities, and the pseudonym key
json.dump(raw_commits, open(os.path.join(S, 'commits_in_window_raw.json'), 'w'), indent=0)
json.dump({k: dict(v, repos=sorted(v['repos'])) for k, v in authors.items()},
          open(os.path.join(S, 'author_key_PRIVATE.json'), 'w'), indent=0)
for r in summary: print(r)
