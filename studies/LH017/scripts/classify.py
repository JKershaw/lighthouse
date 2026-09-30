"""LH017: the class of each CI job for each pair, replayed offline from the records collect.py kept, and the pair classes.

python3 classify.py     writes data/job_classes.csv, data/doc_classes.csv, data/pair_classes.csv and data/file_facts.csv

It reads data/jobs.csv and data/ci_lines.csv (each job's steps), data/tree_paths.csv and data/aux_lines.csv (every
query and relevant line the rules read at collection), data/frame.csv and data/frame_files.csv (L, T and pin class),
and data/judgements.csv (the writer's classes for jobs the script leaves, an input). The rules are in ci.py.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401
import ci as C  # noqa: E402


class Unrecorded(Exception):
    pass


class StoredTree:
    def __init__(self, repo, commit, q, aux):
        self.repo, self.commit = repo, commit
        self.repo_slug = repo.split('/', 1)[1] if '/' in repo else repo
        self.q = q.get((repo, commit), {})
        self.aux = aux.get((repo, commit), {})

    def exists(self, p):
        k = ('exists', p)
        if k not in self.q:
            if p == '':
                return True
            raise Unrecorded(f'{self.repo}@{self.commit}: exists {p}')
        return self.q[k] == 'yes'

    def read(self, p):
        raise Unrecorded('a whole file is not stored')

    def lines(self, p):
        k = ('lines', p, '')
        if k not in self.aux:
            raise Unrecorded(f'{self.repo}@{self.commit}: lines {p}')
        st, ls = self.aux[k]
        return ls if st == 'read' else None

    def struct(self, kind, p, key):
        k = (kind, p, key)
        if k not in self.aux:
            raise Unrecorded(f'{self.repo}@{self.commit}: {kind} {p} {key}')
        st, v = self.aux[k]
        return v if st == 'read' else None


def load_stored():
    q = collections.defaultdict(dict)
    for r in read_csv('tree_paths.csv'):
        q[(r['repo'], r['commit'])][(r['query'], r['path'])] = r['result']
    raw = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in read_csv('aux_lines.csv'):
        raw[(r['repo'], r['commit'])][(r['kind'], r['path'], r['key'])].append((int(r['line']), r['text']))
    aux = collections.defaultdict(dict)
    for rc, d in raw.items():
        for k, rows in d.items():
            rows.sort(key=lambda x: x[0])
            st = rows[0][1] if rows and rows[0][0] == 0 else 'read'
            body = [t for n, t in rows if n > 0]
            if k[0] == 'lines':
                aux[rc][k] = (st, body)
            else:
                aux[rc][k] = (st, json.loads(''.join(body)) if st == 'read' else None)
    return q, aux


def load_jobs():
    jobs = {r['job_key']: r for r in read_csv('jobs.csv')}
    steps = collections.defaultdict(list)
    cur = {}
    for r in read_csv('ci_lines.csv'):
        k = r['job_key']
        sk = (r['seq'], r['sub'])
        if r['field'] == 'step':
            if int(r['part']) == 0:
                steps[k].append({'_json': r['text'], '_run': collections.defaultdict(str), '_sk': sk})
            else:
                steps[k][-1]['_json'] += r['text']
        else:
            li = int(r['field'].split(':', 1)[1])
            steps[k][-1]['_run'][li] += r['text']
    out = {}
    for k, ss in steps.items():
        lst = []
        for s in ss:
            d = json.loads(s['_json'])
            if s['_run'] or d.get('origin') in ('run', 'action-run', 'gitlab'):
                d['run'] = '\n'.join(s['_run'][i] for i in sorted(s['_run']))
            lst.append(d)
        out[k] = lst
    for k in jobs:
        out.setdefault(k, [])
    return jobs, out


def frame_inputs():
    fr = read_csv('frame.csv')
    ff = collections.defaultdict(list)
    for r in read_csv('frame_files.csv'):
        ff[r['pair_id']].append(r)
    return fr, ff


PAIR_ORDER = ['reads the pin', 'does not read the pin', "nothing of the project's requirements", 'undetermined', 'no CI']


def pair_class(classes):
    cs = [c for c in classes]
    if not cs:
        return None
    if any(c == 1 for c in cs):
        return 'reads the pin'
    if any(c == 6 for c in cs):
        return 'undetermined'
    if any(c in (2, 3, 4) for c in cs):
        return 'does not read the pin'
    return "nothing of the project's requirements"


def lock_class(rows):
    """For the lock: reads the timed lock, does not, or undetermined (brief, "Pair class")."""
    cs = [r['final_class'] for r in rows]
    if any(r['final_class'] == 1 and r['T_lock'] == 'yes' for r in rows):
        return 'reads the timed lock'
    if any(c == 6 for c in cs):
        return 'undetermined'
    if any(c in (1, 2, 3, 4) for c in cs):
        return 'does not'
    return 'outside'


def main():
    q, aux = load_stored()
    jobs, steps = load_jobs()
    fr, ff = frame_inputs()
    pr = {r['pair_id']: r for r in read_csv('pairs_read.csv')}
    judg = {}
    jp = os.path.join(DATA, 'judgements.csv')
    if os.path.exists(jp):
        for r in read_csv('judgements.csv'):
            judg[(r['pair_id'], r['job_key'])] = r
    by_commit = collections.defaultdict(list)
    for k, j in jobs.items():
        by_commit[(j['repo'], j['commit'])].append(k)
    docs = collections.defaultdict(list)
    for r in read_csv('docs_lines.csv'):
        docs[(r['repo'], r['commit'])].append(r)
    cif = collections.defaultdict(list)
    for r in read_csv('ci_files.csv'):
        cif[(r['repo'], r['commit'])].append(r)
    repo_pkgs = collections.defaultdict(set)
    for r in fr:
        if r.get('package'):
            repo_pkgs[r['repo']].add(norm(r['package']))
    jrows, drows, prows, frows = [], [], [], []
    for p in fr:
        pid = p['pair_id']
        st = pr.get(pid, {}).get('status', 'not read')
        base = {'pair_id': pid, 'repo': p['repo'], 'library': p['library'], 'pin_class': p['pin_class'],
                'source_study': p['source_study'], 'status': st}
        if st != 'read':
            prows.append({**base})
            continue
        commit = pr[pid]['snapshot']
        tree = StoredTree(p['repo'], commit, q, aux)
        tree.default_branch = p.get('default_branch', '')
        T = [f['path'] for f in ff[pid]]
        T_kind = {f['path']: f['pin_class'] for f in ff[pid]}
        pinned = sorted({v for f in ff[pid] for v in f['versions'].split(';') if v})
        own = set(repo_pkgs[p['repo']]) | set(json.loads(pr[pid].get('own_names') or '[]'))
        rows = []
        C.FACTS = set()
        for k in by_commit.get((p['repo'], commit), []):
            j = jobs[k]
            B = C.Job(steps[k], tree, T, T_kind, p['library'], pinned, own, system=j['system'])
            (cls, sub, why, flags), info = C.classify_job(B)
            jd = judg.get((pid, k))
            final, fsub, how = cls, sub, 'script'
            if cls == 'to judge':
                if jd:
                    final, fsub, how = int(jd['class']), jd.get('sub_label', ''), 'judged'
                else:
                    final, fsub, how = 6, 'other', 'not judged'
            row = {'pair_id': pid, 'job_key': k, 'file': j['file'], 'system': j['system'], 'job': j['job'], 'variant': j['variant'],
                   'script_class': cls, 'script_sub': sub, 'script_reason': why, 'flags': '; '.join(flags),
                   'final_class': final, 'final_sub': fsub, 'decided_by': how, 'judge_reason': (jd or {}).get('reason', ''),
                   'T_lock': info['T_lock'] if cls == 1 else ((jd or {}).get('T_lock', 'no') if how == 'judged' else 'no'),
                   'T_files': info['T_files'] if cls == 1 else ((jd or {}).get('T_files', '') if how == 'judged' else ''),
                   'names_L': info['names_L'], 'spec': info['spec'], 'own_pkgs': info['own_pkgs'], 'own_spec': info['own_spec'],
                   'other_pin': info['other_pin'], 'container_build': info['container_build'], 'effects': info['effects'],
                   'T_tools': info['T_tools'], 'tools': info['tools'], 'triggers': j['triggers'],
                   'caller_triggers': j.get('caller_triggers', ''), 'cache': j['cache'], 'checkout': j['checkout']}
            rows.append(row)
        jrows += rows
        drow = []
        for r in docs.get((p['repo'], commit), []):
            B = C.Job([{'origin': 'doc', 'run': r['text'], 'wd': ''}], tree, T, T_kind, p['library'], pinned, own, system='gitlab')
            (cls, sub, why, flags), info = C.classify_job(B)
            drow.append({'pair_id': pid, 'path': r['path'], 'line': r['line'], 'text': r['text'][:200], 'class': cls, 'sub': sub,
                         'reason': why, 'T_lock': info['T_lock']})
        drows += drow
        frows += [{'pair_id': pid, 'path': f, 'read_as': kind, 'holds_L': hold, 'versions': vers}
                  for f, kind, hold, vers in sorted(C.FACTS)]
        C.FACTS = None
        files = cif.get((p['repo'], commit), [])
        n_ci = sum(1 for f in files if f['system'] in ('github', 'gitlab'))
        n_other = sum(1 for f in files if f['system'] == 'other')
        if not rows:
            pc = 'no CI'
            sub = 'other CI only' if n_other else 'none'
        else:
            pc = pair_class([r['final_class'] for r in rows])
            sub = ''
            if pc == 'reads the pin' and any(r['final_class'] in (2, 3, 4) for r in rows):
                sub = 'mixed'
        lk = lock_class(rows) if p['pin_class'] in ('lockfile', 'both') and rows else ''
        prows.append({**base, 'snapshot': commit, 'ci_files': n_ci, 'other_ci_files': n_other, 'jobs': len(rows),
                      'pair_class': pc, 'pair_sub': sub, 'lock_class': lk,
                      'classes': ' '.join(str(r['final_class']) for r in rows),
                      'n_class1': sum(1 for r in rows if r['final_class'] == 1),
                      'n_to_judge': sum(1 for r in rows if r['script_class'] == 'to judge'),
                      'n_not_judged': sum(1 for r in rows if r['decided_by'] == 'not judged'),
                      'docs_classes': ' '.join(sorted({str(d['class']) for d in drow}))})
    jf = ['pair_id', 'job_key', 'file', 'system', 'job', 'variant', 'script_class', 'script_sub', 'script_reason', 'flags',
          'final_class', 'final_sub', 'decided_by', 'judge_reason', 'T_lock', 'T_files', 'names_L', 'spec', 'own_pkgs', 'own_spec',
          'other_pin', 'container_build', 'T_tools', 'tools', 'triggers', 'caller_triggers', 'cache', 'checkout', 'effects']
    write_csv('job_classes.csv', jrows, jf)
    write_csv('doc_classes.csv', drows, ['pair_id', 'path', 'line', 'text', 'class', 'sub', 'reason', 'T_lock'])
    write_csv('file_facts.csv', frows, ['pair_id', 'path', 'read_as', 'holds_L', 'versions'])
    pf = ['pair_id', 'repo', 'library', 'pin_class', 'source_study', 'status', 'snapshot', 'ci_files', 'other_ci_files', 'jobs',
          'pair_class', 'pair_sub', 'lock_class', 'classes', 'n_class1', 'n_to_judge', 'n_not_judged', 'docs_classes']
    write_csv('pair_classes.csv', prows, pf)
    c = collections.Counter(r.get('pair_class', r['status']) for r in prows)
    print('pairs:', dict(c))
    print('jobs:', dict(collections.Counter(str(r['script_class']) for r in jrows)))


if __name__ == '__main__':
    main()
