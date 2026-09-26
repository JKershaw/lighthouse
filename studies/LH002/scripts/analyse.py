#!/usr/bin/env python3
"""LH002 analysis: candidate propagation links and the ordinary explanations,
GH Archive's hour against git, pseudonymous author tables, and a routine check
on the one exact-pin dependent that moved in the window (R03), read from its
whole pin history. Reads the outputs of collect_git.py, collect_depsdev.py and
gharchive_hour.py. Publishes no name, handle or address.

Usage: python3 analyse.py <scratch_dir> <study_dir>
"""
import collections, csv, datetime as dt, json, os, re, subprocess, sys
S, STUDY = sys.argv[1:3]
DATA = os.path.join(STUDY, 'data'); CL = os.path.join(S, 'clones')
UTC = dt.timezone.utc
def ts(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(UTC)
W0, W1 = dt.datetime(2026, 3, 26, tzinfo=UTC), dt.datetime(2026, 4, 23, tzinfo=UTC)
E0 = ts('2026-04-02T14:48:07Z')  # mcp 1.27.0 publication on PyPI, per Open Source Insights
raw = json.load(open(os.path.join(S, 'commits_in_window_raw.json')))
authors = json.load(open(os.path.join(S, 'author_key_PRIVATE.json')))
dep = json.load(open(os.path.join(S, 'manifest_dependency_changes_PRIVATE.json')))
locks = list(csv.DictReader(open(os.path.join(DATA, 'lockfile_changes.csv'))))
rels = list(csv.DictReader(open(os.path.join(DATA, 'pypi_releases_in_window.csv'))))
pkg = json.load(open(os.path.join(S, 'raw', 'depsdev', 'pkg-mcp.json')))
stable = sorted((ts(v['publishedAt']), v['versionKey']['version']) for v in pkg['versions']
                if v.get('publishedAt') and re.fullmatch(r'\d+\.\d+\.\d+', v['versionKey']['version']))
def latest_mcp(t): return [v for p, v in stable if p <= t][-1]
by_hash = {c['h'][:10]: c for c in raw}
def author_of(commit10): c = by_hash[commit10]; return authors[(c['email'].lower() or c['name'].lower())]
def fmt_lag(t): h = (t - E0).total_seconds() / 3600; return round(h, 1)

def write(name, rows):
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# ---- 1. candidate propagation links from the release ----
cands = []
events = []
for r in dep:
    if r['repo'] != 'R00' and r['package'] == 'mcp':
        events.append(dict(repo=r['repo'], commit=r['commit'], t=ts(r['committed']), kind=f"manifest mcp {r['change']}",
                           before=r['before'], after=r['after'], file=r['file'], breadth=r['packages_changed_in_commit'],
                           msg=r['message_class']))
for r in locks:
    if r['repo'] != 'R00' and r['mcp_before'] != r['mcp_after']:
        events.append(dict(repo=r['repo'], commit=r['commit'], t=ts(r['committed']), kind='lockfile mcp moved',
                           before=r['mcp_before'], after=r['mcp_after'], file=r['file'], breadth=r['packages_moved'],
                           msg=next((d['message_class'] for d in dep if d['commit'] == r['commit']), 'not classed (no manifest change)')))
for e in sorted(events, key=lambda e: e['t']):
    a = author_of(e['commit'])
    own = sorted((ts(x['published']), x['version']) for x in rels if x['repo'] == e['repo'] and ts(x['published']) >= e['t'])
    nxt = own[0] if own else None
    after_release = e['t'] > E0
    admits = '1.27.0' in (e['after'] or '')
    cands.append(dict(
        repo=e['repo'], commit=e['commit'], committed_utc=e['t'].isoformat(), change=e['kind'], file=e['file'],
        before=e['before'], after=e['after'], after_release=after_release,
        lag_hours_from_release=fmt_lag(e['t']) if after_release else '',
        latest_stable_mcp_at_commit=latest_mcp(e['t']),
        candidate_link='yes' if after_release and admits else 'no',
        author_class=a['cls'], author_subclass=a['sub'],
        test_dependency_update_bot='bot author' if a['cls'] == 'bot' else 'not a bot author',
        message_class=e['msg'], packages_changed_same_commit=e['breadth'],
        own_pypi_release_next=f"{nxt[1]} after {round((nxt[0]-e['t']).total_seconds()/3600, 1)} h" if nxt else 'none in window',
        test_shared_maintainer_with_library='yes' if 'R00' in a['repos'] else 'no'))
# R04's GitHub history opens with the uptake already made (root commit, lockfile at 1.27.0)
root = subprocess.run(['git', '-C', os.path.join(CL, 'R04'), 'rev-list', '--max-parents=0', 'HEAD'], capture_output=True, text=True).stdout.split()[0]
rc = by_hash[root[:10]]; ra = authors[(rc['email'].lower() or rc['name'].lower())]
cands.append(dict(repo='R04', commit=root[:10], committed_utc=ts(rc['ct']).isoformat(), change='first commit on GitHub; lockfile already holds mcp',
                  file='uv.lock', before='(no earlier history on GitHub)', after='1.27.0', after_release=True,
                  lag_hours_from_release=fmt_lag(ts(rc['ct'])), latest_stable_mcp_at_commit=latest_mcp(ts(rc['ct'])),
                  candidate_link='uptake visible, change not visible', author_class=ra['cls'], author_subclass=ra['sub'],
                  test_dependency_update_bot='not a bot author' if ra['cls'] != 'bot' else 'bot author',
                  message_class='', packages_changed_same_commit='whole repository', own_pypi_release_next='none in window',
                  test_shared_maintainer_with_library='yes' if 'R00' in ra['repos'] else 'no'))
write('propagation_candidates.csv', cands)

# ---- 2. the library's own dependency changes in the window, and whether they reached PyPI or any dependent ----
lib_changes = [r for r in dep if r['repo'] == 'R00']
d126 = json.load(open(os.path.join(S, 'raw', 'depsdev', 'deps-mcp-1.26.0.json')))
d127 = json.load(open(os.path.join(S, 'raw', 'depsdev', 'deps-mcp-1.27.0.json')))
direct = lambda g: sorted(n['versionKey']['name'] for n in g['nodes'] if n['relation'] == 'DIRECT')
lib_rows = []
for r in lib_changes:
    followers = [d for d in dep if d['repo'] != 'R00' and d['package'] == r['package'] and ts(d['committed']) > ts(r['committed'])]
    lib_rows.append(dict(commit=r['commit'], committed_utc=ts(r['committed']).isoformat(), section=r['section'], package=r['package'],
                         change=r['change'], after=r['after'], on_default_branch=by_hash[r['commit']]['default'],
                         in_mcp_1_27_0_direct_requirements=r['package'] in direct(d127),
                         dependents_changing_same_package_later_in_window=len(followers)))
write('library_dependency_changes.csv', lib_rows)

# ---- 3. shared maintainers between the library and each dependent, over whole histories ----
shared = []
for rid in [f'R{i:02d}' for i in range(1, 10)]:
    hum = [a for a in authors.values() if rid in a['repos'] and 'R00' in a['repos'] and a['cls'] != 'bot']
    bots = [a for a in authors.values() if rid in a['repos'] and 'R00' in a['repos'] and a['cls'] == 'bot']
    shared.append(dict(repo=rid, non_bot_identities_also_in_library_history=len(hum), bot_identities_also_in_library_history=len(bots)))
write('shared_identities_with_library.csv', shared)

# ---- 4. pseudonymous authors with window commits ----
per = collections.defaultdict(lambda: dict(commits=0, days=set()))
for c in raw:
    k = (c['repo'], c['author'], c['cls'], c['sub']); per[k]['commits'] += 1; per[k]['days'].add(ts(c['ct']).date())
arows = [dict(repo=k[0], pseudonym=k[1], author_class=k[2], author_subclass=k[3], commits=v['commits'], active_days=len(v['days']))
         for k, v in sorted(per.items(), key=lambda kv: (kv[0][0], -kv[1]['commits']))]
write('authors_pseudonymous.csv', arows)
conc = []
for rid in sorted({r['repo'] for r in arows}):
    rr = [r for r in arows if r['repo'] == rid]; tot = sum(r['commits'] for r in rr)
    conc.append(dict(repo=rid, authors_in_window=len(rr), commits=tot, top_author_class=rr[0]['author_class'],
                     top_author_share=round(rr[0]['commits'] / tot, 3)))
write('author_concentration.csv', conc)
# where the added and deleted lines sit: top-level directory and file extension, per repository
where = collections.defaultdict(lambda: [0, 0, 0])
for c in raw:
    for add, dele, p in c.get('numstat', []):
        if add is None: continue
        top = p.split('/')[0] if '/' in p else '(root)'
        ext = os.path.splitext(p)[1].lower() or '(none)'
        for key in ((c['repo'], 'directory', top), (c['repo'], 'extension', ext)):
            where[key][0] += add; where[key][1] += dele; where[key][2] += 1
wrows = []
for rid in sorted({k[0] for k in where}):
    tot = sum(v[0] + v[1] for k, v in where.items() if k[0] == rid and k[1] == 'extension')
    for kind in ('directory', 'extension'):
        top5 = sorted(((k, v) for k, v in where.items() if k[0] == rid and k[1] == kind), key=lambda kv: -(kv[1][0] + kv[1][1]))[:5]
        for k, v in top5:
            wrows.append(dict(repo=rid, grouping=kind, value=k[2], additions=v[0], deletions=v[1], file_changes=v[2],
                              share_of_changed_lines=round((v[0] + v[1]) / tot, 3) if tot else ''))
write('changed_lines_by_location.csv', wrows)
trail = collections.Counter()
TOOL = re.compile(r'^(co-authored-by|generated[- ]with|generated[- ]by|assisted-by)\s*:?.*?\b(claude|copilot|cursor|codex|devin|gemini|aider|openhands|jules|chatgpt|windsurf|amp)\b', re.I | re.M)
for c in raw:
    tools = {m.group(2).lower() for m in TOOL.finditer(c['msg'])}
    for t in tools: trail[(c['repo'], t)] += 1
write('ai_tool_trailers.csv', [dict(repo=r, tool_named_in_trailer=t, commits=n) for (r, t), n in sorted(trail.items())] or [dict(repo='', tool_named_in_trailer='', commits=0)])

# ---- 5. GH Archive's hour against git ----
hour0 = dt.datetime(2026, 4, 2, 14, tzinfo=UTC); hour1 = hour0 + dt.timedelta(hours=1)
gha = json.load(open(os.path.join(S, 'gharchive_2026-04-02-14_cohort_events.json')))
hrows = []
for rid in [f'R{i:02d}' for i in range(10)]:
    git_commits = [c for c in raw if c['repo'] == rid and hour0 <= ts(c['ct']) < hour1]
    ev = [e for e in gha if e['repo'] == rid]
    pushes = [e for e in ev if e['type'] == 'PushEvent']
    pushed_commits, heads_reachable, heads_by_hash, heads_on_default = 0, 0, 0, 0
    window_hashes = {c['h'] for c in raw if c['repo'] == rid}
    repo = os.path.join(CL, rid)
    dflt = subprocess.run(['git', '-C', repo, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD'], capture_output=True, text=True).stdout.strip()
    for e in pushes:
        # reachable from a branch or tag of the clone, i.e. in the history git shows today
        reach = bool(subprocess.run(['git', '-C', repo, 'for-each-ref', '--contains', e['head'], '--format=x'], capture_output=True, text=True).stdout.strip())
        heads_reachable += reach
        # retrievable by hash: in a partial clone this fetches the object from GitHub on demand
        ok = subprocess.run(['git', '-C', repo, 'cat-file', '-e', e['head'] + '^{commit}'], capture_output=True).returncode == 0
        heads_by_hash += ok
        if ok:
            n = subprocess.run(['git', '-C', repo, 'rev-list', '--count', f"{e['before']}..{e['head']}"], capture_output=True, text=True).stdout.strip()
            pushed_commits += int(n or 0)
            heads_on_default += subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', e['head'], dflt]).returncode == 0
    hrows.append(dict(repo=rid, gharchive_events=len(ev), gharchive_push_events=len(pushes),
                      gharchive_other_events=';'.join(sorted({e['type'] for e in ev if e['type'] != 'PushEvent'})),
                      push_heads_reachable_from_refs=heads_reachable, push_heads_retrievable_by_hash=heads_by_hash, commits_in_pushes_per_git=pushed_commits,
                      push_heads_now_on_default_branch=heads_on_default,
                      git_commits_with_committer_time_in_hour=len(git_commits),
                      git_commits_in_hour_on_default_branch=sum(c['default'] for c in git_commits)))
write('gharchive_hour_vs_git.csv', hrows)

# ---- 6. routine check: R03's whole history of its exact mcp pin against mcp publication times ----
repo = os.path.join(CL, 'R03')
log = subprocess.run(['git', '-C', repo, 'log', '--first-parent', 'origin/HEAD', '--format=%H %cI', '--', 'pyproject.toml'],
                     capture_output=True, text=True).stdout.split('\n')
pins, prev = [], None
for line in reversed([l for l in log if l.strip()]):
    h, t = line.split()
    txt = subprocess.run(['git', '-C', repo, 'show', f'{h}:pyproject.toml'], capture_output=True, text=True).stdout
    m = re.search(r'"mcp(\[[^\]]*\])?\s*([=<>~!][^"]*)"', txt)
    spec = m.group(2).replace(' ', '') if m else ''
    if spec != prev:
        pv = spec[2:] if spec.startswith('==') else ''
        pub = next((p for p, v in stable if v == pv), None)
        pins.append(dict(commit=h[:10], committed_utc=ts(t).isoformat(), mcp_spec=spec,
                         pinned_version_published_utc=pub.isoformat() if pub else '',
                         lag_days_from_publication=round((ts(t) - pub).total_seconds() / 86400, 1) if pub else '',
                         latest_stable_mcp_at_commit=latest_mcp(ts(t)) if ts(t) >= stable[0][0] else ''))
        prev = spec
write('R03_mcp_pin_history.csv', pins)

for name, rows in (('candidates', cands), ('library', lib_rows), ('shared', shared), ('hour', hrows), ('R03 pins', pins)):
    print('==', name); [print({k: v for k, v in r.items()}) for r in rows]
print('== trailers', dict(trail)); print('== conc', conc)
lags = sorted(r['lag_days_from_publication'] for r in pins if r['lag_days_from_publication'] != '' and r['mcp_spec'] == '==' + r['latest_stable_mcp_at_commit'])
print('== R03 exact-pin moves to the then-latest release:', len(lags), 'lags (days)', lags, 'median', lags[len(lags)//2] if len(lags) % 2 else (lags[len(lags)//2-1]+lags[len(lags)//2])/2)
print('== top authors', [r for r in arows if r['commits'] >= 20])
