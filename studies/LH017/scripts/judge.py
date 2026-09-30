"""LH017: the writer's judgements of the jobs the script leaves ("to judge"), where the brief requires them (step 3).

python3 judge.py     writes data/judgements.csv

The writer read the files named at each snapshot (from the clones, 30 September 2026, 07:30 to 07:40 UTC) and recorded
one reading per group of jobs in READINGS below; each reading replaces the job's "judge" effects, and the brief's
precedence and override rules (ci.decide) then give the job's class. Only jobs that could change a pair's class or its
reading for the lock are judged (brief, "Classification and its check", 3); the others stay class 6, not judged.
"""
import collections
import csv
import os
import posixpath
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401
import ci as C  # noqa: E402
import classify as K  # noqa: E402

MADE = '2026-09-30, before the blind sample was drawn'

# (repository, pattern on the judge effect's reason) -> (reading id, function(B, effect, steps) -> list of effects)


def manifest_reads(tfile):
    def f(B, e, steps):
        # the manifest takes the project's dependencies from the T file at build time (LH015 amendment 1's reading)
        cands = sorted(t for t in B.T if posixpath.basename(t) == tfile)
        if not cands:
            return [C.eff('und', why='other', detail=f'manifest reads {tfile}, not in T for this pair')]
        return [C.eff('T', files=cands[:1], why=f'the manifest takes its dependencies from {cands[0]} (writer)')]
    return f


def manifest_does_not_read(B, e, steps):
    # the manifest names the T file's name but does not read it for dependencies; the project installs from the manifest
    mans = e.get('files') or []
    for m in mans:
        hold, vers = versions_in(m, '\n'.join(B.tree.lines(m) or []), B.L, 'manifest')
        if hold:
            return [C.eff('other_pin', files=[m], version=vers, overrides=not set(vers) & set(B.pinned),
                          why=f'{m} pins L (writer)')]
    return [C.eff('fresh', sub='other file', names_L=False, files=mans, why='project from its manifest, which reads no T file (writer)')]


def others(why):
    return lambda B, e, steps: [C.eff('others', why=why)]


def neutral(why):
    return lambda B, e, steps: [C.eff('neutral', why=why)]


def und(reason, why):
    return lambda B, e, steps: [C.eff('und', why=reason, detail=why)]


def other_pin_by_name(B, e, steps):
    # LH015 amendment 2's reading: a file not in T that pins L exactly, whose name LH008's rule does not read
    return [C.eff('other_pin', files=e.get('files') or [], version=e.get('version') or [], overrides=True,
                  why=f'{(e.get("files") or ["?"])[0]} pins L exactly; LH008 would not read it by name (writer)')]


HATCH_LOCKS = {'default': '.hatch/requirements.txt', 'docs': '.hatch/requirements-docs.txt',
               'lint': '.hatch/requirements-lint.txt', 'test': '.hatch/requirements-test.txt'}
HATCH_DETACHED = {'lint'}


def live_text(repo, commit, path):
    """The writer's own read of a file at the snapshot, from the clone (logged)."""
    import subprocess
    import time
    t0, when = time.time(), now()
    p = subprocess.run(['git', 'show', f'{commit}:{path}'], cwd=repo_dir(repo), capture_output=True, text=True)
    log(read_utc=when, source='git over HTTPS (blob fetched on demand)', repo=repo, commit=commit, path=path, method='git show',
        status='ok' if p.returncode == 0 else 'failed', bytes=len(p.stdout.encode()) if p.returncode == 0 else '',
        seconds=round(time.time() - t0, 2), note='the writer\'s judgement')
    return p.stdout if p.returncode == 0 else None


def hatch_pip_compile(B, e, steps):
    """hatch-pip-compile installs the environment's lock-filename into it and keeps it up to date (its README on PyPI,
    read 07:32 UTC), and the project unless the environment is detached (pyproject.toml at both snapshots)."""
    runs = '\n'.join(s.get('run') or '' for s in steps)
    envs = []
    for m in re.finditer(r'hatch\s+(?:-e\s+(\w+)\s+)?run\s+(?:(\w+):)?', runs):
        envs.append(m.group(1) or m.group(2) or 'default')
    removed = bool(re.search(r'rm\s+\.hatch/requirements\*\.txt', runs))
    out = []
    for env in dict.fromkeys(envs):
        lock = HATCH_LOCKS.get(env)
        if lock is None:
            out.append(C.eff('und', why='other', detail=f'hatch environment {env} not in pyproject.toml'))
            continue
        if removed:
            out.append(C.eff('fresh', sub='lock absent', names_L=None, overrides=True,
                             why=f'{lock} removed before hatch resolves the {env} environment afresh (writer)'))
            continue
        if lock in B.T:
            out.append(C.eff('T', files=[lock], may_relock=True, why=f'hatch-pip-compile installs {lock} (writer)'))
        else:
            ls = live_text(B.tree.repo, B.tree.commit, lock)
            hold, vers = versions_in(lock, ls or '', B.L, 'requirements') if ls is not None else (None, [])
            if hold:
                out.append(C.eff('other_pin', files=[lock], version=vers, why=f'{lock} pins L (writer)'))
            else:
                out.append(C.eff('fresh', sub='other file', names_L=False, files=[lock], why=f'{lock} does not name L (writer)'))
        if env not in HATCH_DETACHED:
            if 'pyproject.toml' in B.T:
                out.append(C.eff('T', files=['pyproject.toml'], why='hatch installs the project, pinned in the T manifest (writer)'))
    return out


READINGS = [
    ('github.com/aider-ai/aider', r'^manifest names T file requirements\.txt', 'A1', manifest_reads('requirements.txt')),
    ('github.com/tvick64889/forgepair', r'^manifest names T file requirements\.txt', 'A1', manifest_reads('requirements.txt')),
    ('github.com/asozialesnetzwerk/an-website', r'^manifest names T file pip-dev-requirements\.txt', 'A2',
     manifest_reads('pip-requirements.txt')),
    ('github.com/egnyte/cloudimized', r'^manifest names T file requirements\.txt', 'A3', manifest_reads('requirements.txt')),
    ('github.com/nucypher/nucypher', r'^manifest names T file dev-requirements\.txt', 'A4', manifest_reads('requirements.txt')),
    ('github.com/talkinglibrary/talklib', r'^manifest names T file requirements\.txt', 'A5', manifest_reads('requirements.txt')),
    ('github.com/vida-nyu/bdi-kit', r'^manifest names T file requirements\.txt', 'A6', manifest_reads('requirements.txt')),
    ('github.com/snowflakedb/snowflake-cli', r'^manifest names T file requirements\.txt', 'A7', manifest_does_not_read),
    ('github.com/alan-turing-institute/data-safe-haven', r'^hatch: hatch environment type pip-compile', 'B1', hatch_pip_compile),
    ('github.com/asozialesnetzwerk/an-website', r'^install inside docker run', 'B2',
     others('pytest plugins named from pip-constraints.txt, installed inside the image the job runs (writer)')),
    ('github.com/asozialesnetzwerk/an-website', r'^pin of L in pip-constraints\.txt', 'B3', other_pin_by_name),
    ('github.com/chaoss/grimoirelab', r'^wheel \./dist/\*whl from a downloaded artefact', 'B4',
     und('external', 'the wheel is built by the external action chaoss/grimoirelab-github-actions/build (writer)')),
    ('github.com/eth-brownie/brownie', r'^action BobTheBuidler/mypycify', 'B5',
     und('external', 'an external action builds the project; what it installs is not read (writer)')),
    ('github.com/mervinpraison/praisonai', r'^action actions/create-release', 'B6',
     neutral('the release body text names an install command; the action creates a release (writer)')),
    ('github.com/mervinpraison/praisonai', r'^poetry (install|lock) without a project found', 'B7',
     und('external', 'the job checks out another repository (a fork named by an input) at main (writer)')),
    ('github.com/steveyegge/beads', r'^action DeterminateSystems/update-flake-lock', 'B8',
     neutral('the action updates a Nix flake lock, not a Python install (writer)')),
]


def main():
    q, aux = K.load_stored()
    jobs, steps = K.load_jobs()
    fr, ff = K.frame_inputs()
    fmap = {r['pair_id']: r for r in fr}
    pr = {r['pair_id']: r for r in read_csv('pairs_read.csv')}
    jc = read_csv('job_classes.csv')
    bp = collections.defaultdict(list)
    for r in jc:
        bp[r['pair_id']].append(r)
    repo_pkgs = collections.defaultdict(set)
    for r in fr:
        if r.get('package'):
            repo_pkgs[r['repo']].add(norm(r['package']))
    out, missing = [], collections.Counter()
    for pid, rs in bp.items():
        has1 = any(x['script_class'] == '1' for x in rs)
        haslock = any(x['script_class'] == '1' and x['T_lock'] == 'yes' for x in rs)
        lockpair = fmap[pid]['pin_class'] in ('lockfile', 'both')
        for x in rs:
            if x['script_class'] != 'to judge' or not (not has1 or (lockpair and not haslock)):
                continue
            p = fmap[pid]
            commit = pr[pid]['snapshot']
            tree = K.StoredTree(p['repo'], commit, q, aux)
            tree.default_branch = p.get('default_branch', '')
            T = [f['path'] for f in ff[pid]]
            T_kind = {f['path']: f['pin_class'] for f in ff[pid]}
            pinned = sorted({v for f in ff[pid] for v in f['versions'].split(';') if v})
            import json as _j
            own = set(repo_pkgs[p['repo']]) | set(_j.loads(pr[pid].get('own_names') or '[]'))
            B = C.Job(steps[x['job_key']], tree, T, T_kind, p['library'], pinned, own, system=jobs[x['job_key']]['system'])
            effects = C.walk(B)
            new, used = [], []
            for e in effects:
                if e['kind'] != 'judge':
                    new.append(e)
                    continue
                rd = next((r for r in READINGS if r[0] == p['repo'] and re.search(r[1], e['why'])), None)
                if rd is None:
                    missing[(p['repo'], e['why'][:80])] += 1
                    new.append(e)
                    continue
                used.append(rd[2])
                new += rd[3](B, e, steps[x['job_key']])
            cls, sub, why, flags = C.decide(B, new)
            if cls == 'to judge':
                continue
            Ts = [e for e in new if e['kind'] == 'T']
            out.append({'pair_id': pid, 'job_key': x['job_key'], 'class': cls, 'sub_label': sub,
                        'reason': ('reading ' + ', '.join(dict.fromkeys(used)) + ': ' + why)[:300],
                        'T_files': '|'.join(sorted({f for e in Ts for f in e.get('files', [])})) if cls == 1 else '',
                        'T_lock': 'yes' if cls == 1 and any(T_kind.get(f) == 'lockfile' for e in Ts for f in e.get('files', [])) else 'no',
                        'flags': '; '.join(flags), 'readings': ' '.join(dict.fromkeys(used)), 'made': MADE})
    write_csv('judgements.csv', out, ['pair_id', 'job_key', 'class', 'sub_label', 'reason', 'T_files', 'T_lock', 'flags', 'readings',
                                     'made'])
    print(f'{len(out)} judgements;', dict(collections.Counter(r['class'] for r in out)))
    for k, v in missing.most_common():
        print('no reading for', v, k)


if __name__ == '__main__':
    main()
