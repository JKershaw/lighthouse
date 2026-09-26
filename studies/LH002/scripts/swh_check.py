#!/usr/bin/env python3
"""LH002: Software Heritage coverage of the cohort (anonymous API).

For each repository: whether a GitHub origin is archived (URL as given, then the
package's own original-case URL). For each archived origin: whether the
default-branch head at window end, as read from git, exists as a revision. For
R00 only: the visit history around the window, and whether the visit snapshots
hold the release tag v1.27.0 and the v1.x branch.

Usage: python3 swh_check.py <scratch_dir> <study_dir>
"""
import csv, json, os, subprocess, sys, time, urllib.request, urllib.error
S, STUDY = sys.argv[1:3]
API = 'https://archive.softwareheritage.org/api/1'
RAW = os.path.join(S, 'raw', 'swh'); os.makedirs(RAW, exist_ok=True)
CASE = {'R01': 'saigontechnology/AgentCrew', 'R03': 'oOo0oOo/lean-lsp-mcp', 'R06': 'eddmpython/dartlab',
        'R08': 'Drakkar-Software/OctoBot'}  # original-case URLs from each package's own links (deps.dev)

def get(url, name):
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                body = {'_status': r.status, 'data': json.load(r)}
        except urllib.error.HTTPError as e:
            body = {'_status': e.code, 'data': None}
        json.dump(body, open(path, 'w')); time.sleep(0.5)
    return json.load(open(path))

state = {r['repo']: r for r in csv.DictReader(open(os.path.join(STUDY, 'data', 'mcp_state_window_start_end.csv'))) if r['at'] == 'end'}
rows = []
for line in open(os.path.join(S, 'repos.txt')):
    if not line.strip(): continue
    rid, slug = line.split()
    urls = [f'https://github.com/{slug}'] + ([f'https://github.com/{CASE[rid]}'] if rid in CASE else [])
    found = None
    for i, u in enumerate(urls):
        o = get(f'{API}/origin/{u}/get/', f'origin-{rid}-{i}.json')
        if o['_status'] == 200: found = u; break
    head = state[rid]['commit']
    full = subprocess.run(['git', '-C', os.path.join(S, 'clones', rid), 'rev-parse', head], capture_output=True, text=True).stdout.strip() if head else ''
    rev_status = ''
    if found and full:
        rev_status = get(f'{API}/revision/{full}/', f'revision-{rid}-{full[:10]}.json')['_status']
    rows.append(dict(repo=rid, github_origin_archived='yes' if found else 'no', origin_lookups=len(urls),
                     window_end_head=head, window_end_head_in_archive={200: 'yes', 404: 'no'}.get(rev_status, '')))

# R00 visit history and tag presence
v = get(f'{API}/origin/https://github.com/modelcontextprotocol/python-sdk/visits/?per_page=200', 'visits-R00-full.json')['data']
visits = []
for x in sorted(v, key=lambda x: x['date']):
    if not ('2026-02-01' <= x['date'][:10] <= '2026-06-01'): continue
    snap = x.get('snapshot')
    tag = branch = ''
    if snap:
        s = get(f'{API}/snapshot/{snap}/?branches_from=refs/tags/v1.27.0&branches_count=1', f'snap-{snap[:12]}-tag.json')['data'] or {}
        tag = 'yes' if 'refs/tags/v1.27.0' in (s.get('branches') or {}) else 'no'
        s2 = get(f'{API}/snapshot/{snap}/?branches_from=refs/heads/v1.x&branches_count=1', f'snap-{snap[:12]}-v1x.json')['data'] or {}
        b = (s2.get('branches') or {}).get('refs/heads/v1.x')
        branch = (b or {}).get('target', '')[:10] if b else 'absent'
    visits.append(dict(visit_date=x['date'], status=x['status'], type=x.get('type'), snapshot=(snap or '')[:12],
                       has_tag_v1_27_0=tag, v1x_branch_head=branch))
rel = subprocess.run(['git', '-C', os.path.join(S, 'clones', 'R00'), 'rev-parse', 'v1.27.0^{commit}'], capture_output=True, text=True).stdout.strip()
relrev = get(f'{API}/revision/{rel}/', f'revision-R00-release.json')
out = dict(read_at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), repositories=rows, r00_visits_feb_to_may_2026=visits,
           r00_visits_total=len(v), r00_first_visit=min(x['date'] for x in v), r00_last_visit=max(x['date'] for x in v),
           release_commit=rel[:10], release_commit_in_archive={200: 'yes', 404: 'no'}.get(relrev['_status'], str(relrev['_status'])))
json.dump(out, open(os.path.join(STUDY, 'data', 'software_heritage_coverage.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
