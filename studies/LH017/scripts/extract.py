"""LH017: from CI files to jobs and their steps, and from task-runner files to the install commands they run.

Run by collect.py against the live tree (full files are read into the scratchpad only). What it returns is stored:
each job's steps in data/ci_lines.csv, and each task-runner reading (tox, nox, hatch, make, just, scripts) as JSON in
data/aux_lines.csv, so that classify.py can replay the classification offline. The brief's sections "What counts as
CI" and "Steps, files and working directories" fix what is read here.
"""
import ast
import configparser
import itertools
import json
import posixpath
import re
import shlex
import tomllib

import yaml

from ci import UNK, WS, J, commands, parse_cmd

# ================================================================ expressions

EXPR = re.compile(r'\$\{\{\s*(.*?)\s*\}\}', re.S)


def _lookup(root, path):
    cur = root
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur


def strkeys(v):
    """YAML may give booleans or numbers as mapping keys; JSON with sorted keys needs strings."""
    if isinstance(v, dict):
        return {str(k): strkeys(x) for k, x in v.items()}
    if isinstance(v, list):
        return [strkeys(x) for x in v]
    return v


def _fmt(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (dict, list)):
        return json.dumps(v)
    return str(v)


def eval_expr(e, ctx):
    """The value of a simple expression: matrix.*, inputs.*, env.*, github.workspace, a literal, or a || chain."""
    e = e.strip()
    parts = [p.strip() for p in re.split(r'\|\|', e)] if '||' in e else [e]
    for p in parts:
        v = _eval1(p, ctx)
        if v is None:
            return None
        if v != '':
            return v
    return ''


def _eval1(p, ctx):
    m = re.fullmatch(r"'([^']*)'", p)
    if m:
        return m.group(1)
    if re.fullmatch(r'-?\d+(\.\d+)?', p):
        return p
    if p in ('true', 'false'):
        return p
    if p == 'github.workspace':
        return WS
    m = re.fullmatch(r"(matrix|inputs|env)((?:\.[A-Za-z_][\w-]*|\[\s*'[^']+'\s*\])+)", p)
    if m:
        keys = re.findall(r"\.([A-Za-z_][\w-]*)|\[\s*'([^']+)'\s*\]", m.group(2))
        keys = [a or b for a, b in keys]
        src = ctx.get(m.group(1))
        if src is None:
            return None
        v = _lookup(src, keys)
        if v is None:
            return '' if m.group(1) == 'inputs' and keys and keys[0] in (ctx.get('_declared_inputs') or ()) else None
        if isinstance(v, str) and UNK in v:
            return None
        return _fmt(v)
    return None


def subst(s, ctx):
    if s is None:
        return None
    s = str(s)

    def rep(m):
        v = eval_expr(m.group(1), ctx)
        return v if v is not None else UNK + m.group(1)[:60] + '⟩'
    return EXPR.sub(rep, s)


# ================================================================ matrices (G2)

def matrix_combos(m):
    """[(combo dict, unknown keys)] under GitHub's include and exclude rules; None if the matrix is an expression."""
    if m is None:
        return [({}, set())]
    if not isinstance(m, dict):
        return None
    unk = set()
    base = {}
    for k, v in m.items():
        if k in ('include', 'exclude'):
            continue
        if isinstance(v, list):
            base[k] = v
        else:
            unk.add(k)
    keys = list(base)
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*[base[k] for k in keys])] if keys else []
    ex = m.get('exclude') if isinstance(m.get('exclude'), list) else []
    combos = [c for c in combos if not any(isinstance(x, dict) and all(c.get(k) == v for k, v in x.items()) for x in ex)]
    inc = m.get('include')
    if isinstance(inc, str):
        unk.add('include')
        inc = []
    for x in inc or []:
        if not isinstance(x, dict):
            continue
        added = False
        for c in combos:
            if all(c.get(k) == v for k, v in x.items() if k in base):
                for k, v in x.items():
                    if k not in base:
                        c[k] = v
                added = True
        if not added:
            combos.append(dict(x))
    if not combos:
        combos = [{}]
    return [(c, unk) for c in combos]


# ================================================================ YAML

def load_yaml(text):
    d = yaml.safe_load(text)
    if isinstance(d, dict) and True in d and 'on' not in d:
        d['on'] = d.pop(True)
    return strkeys(d)


def triggers_of(d):
    on = d.get('on') if isinstance(d, dict) else None
    if isinstance(on, str):
        return [on]
    if isinstance(on, list):
        return [str(x) for x in on]
    if isinstance(on, dict):
        return [str(k) for k in on]
    return []


def call_inputs_decl(d):
    on = d.get('on') if isinstance(d, dict) else None
    if isinstance(on, dict) and isinstance(on.get('workflow_call'), dict):
        inp = on['workflow_call'].get('inputs') or {}
        return {k: (v or {}).get('default') for k, v in inp.items()} if isinstance(inp, dict) else {}
    return None


def dispatch_inputs_decl(d):
    on = d.get('on') if isinstance(d, dict) else None
    if isinstance(on, dict) and isinstance(on.get('workflow_dispatch'), dict):
        inp = on['workflow_dispatch'].get('inputs') or {}
        return {k: (v or {}).get('default') for k, v in inp.items()} if isinstance(inp, dict) else {}
    return {}


KEEP_RUN = re.compile(r'(?i)\b(pip3?|pip3\.\d+|uv|uvx|poetry|pipenv|pdm|pipx|conda|mamba|micromamba|pip-sync|pip-compile|tox|nox|'
                      r'hatch|make|gmake|just|docker|podman|buildah|docker-compose|pre-commit|prek|setup\.py|cd|pushd|popd|'
                      r'export|source|bash|sh|GITHUB_ENV|python3?(\.\d+)?\s+-m)\b|\./|\.sh\b|^\s*[A-Za-z_][A-Za-z0-9_]*=')


def keep_run(text):
    """The run text's install-relevant lines, with continuations joined (brief, data/ci_lines.csv)."""
    out = []
    for line in re.sub(r'\\\r?\n', ' ', text or '').split('\n'):
        if KEEP_RUN.search(line):
            out.append(line.rstrip())
    return '\n'.join(out)


def norm_env(env, ctx):
    out = {}
    if isinstance(env, dict):
        for k, v in env.items():
            vv = subst(_fmt(v), {**ctx, 'env': {**(ctx.get('env') or {}), **out}})
            out[str(k)] = vv if vv is not None else ''
    return out


def github_jobs(tree, path, d, callers):
    """Jobs of one workflow file: [{'job', 'variant', 'values', 'steps', 'meta'}]."""
    out = []
    wenv_raw = d.get('env') if isinstance(d.get('env'), dict) else {}
    wdef = ((d.get('defaults') or {}).get('run') or {}).get('working-directory') if isinstance(d.get('defaults'), dict) else None
    trig = triggers_of(d)
    decl = call_inputs_decl(d)
    input_sets = []
    caller_trig = {}
    if decl is not None:
        for w, ctrig in callers.get(path, []):
            input_sets.append(('call', {**decl, **w}))
            caller_trig[len(input_sets) - 1] = sorted(ctrig)
        if not input_sets or any(t != 'workflow_call' for t in trig):
            input_sets.append(('defaults', dict(decl)))
    else:
        input_sets.append(('dispatch', dispatch_inputs_decl(d)))
    jobs = d.get('jobs') if isinstance(d.get('jobs'), dict) else {}
    for jid, job in jobs.items():
        if not isinstance(job, dict):
            continue
        if 'uses' in job and 'steps' not in job:
            u = str(job.get('uses') or '')
            if u.startswith('./'):
                continue
            out.append({'job': str(jid), 'variant': 'external call', 'values': {}, 'meta': {'call': u, 'triggers': trig},
                        'steps': [{'origin': 'external-call', 'uses': u}]})
            continue
        if not isinstance(job.get('steps'), list):
            continue
        strat = job.get('strategy') if isinstance(job.get('strategy'), dict) else {}
        mat = strat.get('matrix') if strat else None
        combos = matrix_combos(mat)
        jdef = ((job.get('defaults') or {}).get('run') or {}).get('working-directory') if isinstance(job.get('defaults'), dict) else None
        seen = {}
        for si, (how, inputs) in enumerate(input_sets):
            for combo, unk in (combos if combos is not None else [({}, {'*'})]):
                mctx = dict(combo)
                for k in unk:
                    mctx[k] = UNK + 'matrix.' + k + '⟩'
                if combos is None:
                    mctx = None
                ctx = {'matrix': mctx if mctx is not None else {}, 'inputs': inputs, '_declared_inputs': set(inputs)}
                if mctx is None:
                    ctx['matrix'] = _AnyUnknown('matrix')
                wenv = norm_env(wenv_raw, ctx)
                ctx['env'] = wenv
                jenv = norm_env(job.get('env'), ctx)
                ctx['env'] = {**wenv, **jenv}
                steps = []
                container = job.get('container')
                image = container if isinstance(container, str) else (container or {}).get('image') if isinstance(container, dict) else ''
                for i, s in enumerate(job['steps']):
                    if not isinstance(s, dict):
                        continue
                    senv = norm_env(s.get('env'), ctx)
                    sctx = {**ctx, 'env': {**ctx['env'], **senv}}
                    st = {'seq': i, 'if': 'if' in s, 'env': senv}
                    if 'uses' in s:
                        u = subst(s.get('uses'), sctx) or ''
                        w = {str(k): subst(_fmt(v), sctx) for k, v in (s.get('with') or {}).items()} if isinstance(s.get('with'), dict) else {}
                        st.update({'origin': 'uses', 'uses': u, 'with': w})
                        if u.startswith('./'):
                            steps += local_action(tree, u, w, sctx, i, wdef, jdef)
                            continue
                    elif 'run' in s:
                        wd = s.get('working-directory') or jdef or wdef
                        st.update({'origin': 'run', 'run': keep_run(subst(_fmt(s.get('run')), sctx)),
                                   'wd': subst(_fmt(wd), sctx) if wd else ''})
                    else:
                        continue
                    steps.append(st)
                key = json.dumps([{k: v for k, v in s.items() if k != 'seq'} for s in steps], sort_keys=True)
                if key in seen:
                    continue
                vals = {k: combo.get(k) for k in combo} if combos is not None else {'matrix': 'expression'}
                seen[key] = True
                meta = {'triggers': trig, 'inputs_from': how, 'caller_triggers': caller_trig.get(si, []), 'container': _fmt(image) or '', 'runs_on': _fmt(job.get('runs-on')) or '',
                        'job_if': 'if' in job, 'needs': job.get('needs') if isinstance(job.get('needs'), list) else
                        ([job['needs']] if isinstance(job.get('needs'), str) else [])}
                out.append({'job': str(jid), 'variant': str(len(seen)), 'values': vals, 'steps': steps, 'meta': meta})
                if len(seen) >= 64:
                    break
            if len(seen) >= 64:
                break
    # artefacts: a job that downloads an artefact is told which projects the jobs it needs build (brief, "Hard cases")
    built = {}
    for j in out:
        built.setdefault(j['job'], set()).update(built_projects(j['steps']))
    for j in out:
        needs = (j.get('meta') or {}).get('needs') or []
        projs = sorted({p for n in needs for p in built.get(str(n), set())} | built.get(j['job'], set()))
        for s in j['steps']:
            if (s.get('uses') or '').lower().startswith('actions/download-artifact'):
                s.setdefault('with', {})['__projects__'] = projs
    return out


class _AnyUnknown(dict):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __contains__(self, k):
        return True

    def __getitem__(self, k):
        return UNK + self.name + '.' + str(k) + '⟩'


BUILD_CMD = re.compile(r'(?:^|\s)(?:python3?(?:\.\d+)?\s+-m\s+build|pyproject-build|uv\s+build|poetry\s+build|hatch\s+build|'
                       r'pdm\s+build|flit\s+build|pip3?\s+wheel|python3?\s+setup\.py\s+(?:sdist|bdist_wheel))\b([^;&|\n]*)')


def built_projects(steps):
    """Workspace directories whose project a job's steps build into a wheel or sdist."""
    out = []
    for s in steps:
        u = (s.get('uses') or '').lower()
        if u.startswith(('pypa/cibuildwheel', 'hynek/build-and-inspect-python-package')):
            w = s.get('with') or {}
            out.append(J(w.get('package-dir') or w.get('path') or '.'))
            continue
        run = s.get('run') or ''
        for line in run.split('\n'):
            cd = re.match(r'^\s*cd\s+([\w./-]+)\s*(?:&&|;)', line)
            m = BUILD_CMD.search(line)
            if not m:
                continue
            args = [a for a in m.group(1).split() if not a.startswith('-')]
            base = J(s.get('wd') or '', cd.group(1) if cd else '')
            src = args[0] if args and not args[0].startswith(('dist', '/', '$')) and 'whl' not in args[0] else '.'
            out.append(J(base, src) if src not in ('.', '') else base)
    return sorted(set(out))


def local_action(tree, uses, with_, ctx, i, wdef, jdef):
    """A local composite action's steps, read one level with its inputs substituted (G3)."""
    base = J(uses[2:].split('@', 1)[0])
    meta = None
    for n in ('action.yml', 'action.yaml'):
        p = J(base, n)
        if tree.exists(p):
            txt = tree.read(p)
            if txt is None:
                return [{'seq': i, 'origin': 'unreadable', 'note': f'local action {p} unreadable'}]
            try:
                meta = load_yaml(txt)
            except Exception:
                return [{'seq': i, 'origin': 'unreadable', 'note': f'local action {p} does not parse'}]
            break
    if meta is None:
        return [{'seq': i, 'origin': 'judge', 'note': f'local action {uses} without action.yml at the snapshot'}]
    runs = meta.get('runs') if isinstance(meta, dict) else None
    if not isinstance(runs, dict) or str(runs.get('using', '')).lower() != 'composite':
        return [{'seq': i, 'origin': 'judge', 'note': f'local action {uses} is not composite ({(runs or {}).get("using", "")})'}]
    decl = meta.get('inputs') if isinstance(meta.get('inputs'), dict) else {}
    inputs = {k: (v or {}).get('default') if isinstance(v, dict) else None for k, v in decl.items()}
    for k, v in with_.items():
        inputs[k] = v
    actx = {**ctx, 'inputs': {k: (_fmt(v) if v is not None else '') for k, v in inputs.items()}, '_declared_inputs': set(inputs)}
    out = []
    for j, s in enumerate(runs.get('steps') or []):
        if not isinstance(s, dict):
            continue
        senv = norm_env(s.get('env'), actx)
        sctx = {**actx, 'env': {**(actx.get('env') or {}), **senv}}
        st = {'seq': i, 'sub': j, 'if': 'if' in s, 'env': senv, 'action': base}
        if 'uses' in s:
            u = subst(s.get('uses'), sctx) or ''
            w = {str(k): subst(_fmt(v), sctx) for k, v in (s.get('with') or {}).items()} if isinstance(s.get('with'), dict) else {}
            if u.startswith('./'):
                out.append({**st, 'origin': 'nested-action', 'uses': u})
                continue
            st.update({'origin': 'action-uses', 'uses': u, 'with': w})
        elif 'run' in s:
            wd = s.get('working-directory')
            st.update({'origin': 'action-run', 'run': keep_run(subst(_fmt(s.get('run')), sctx)),
                       'wd': subst(_fmt(wd), sctx) if wd else ''})
        else:
            continue
        out.append(st)
    return out


def local_calls(docs):
    """Inputs that callers in the repository give each local reusable workflow."""
    calls = {}
    for path, d in docs.items():
        if not isinstance(d, dict) or not isinstance(d.get('jobs'), dict):
            continue
        for jid, job in d['jobs'].items():
            if isinstance(job, dict) and isinstance(job.get('uses'), str) and job['uses'].startswith('./'):
                tgt = J(job['uses'][2:].split('@', 1)[0])
                strat = job.get('strategy') if isinstance(job.get('strategy'), dict) else {}
                combos = matrix_combos(strat.get('matrix')) if strat else [({}, set())]
                for combo, unk in (combos or [({}, set())]):
                    mctx = dict(combo)
                    for k in unk:
                        mctx[k] = UNK + 'matrix.' + k + '⟩'
                    ctx = {'matrix': mctx, 'inputs': {}, 'env': {}}
                    w = {str(k): subst(_fmt(v), ctx) for k, v in (job.get('with') or {}).items()} if isinstance(job.get('with'), dict) else {}
                    lst = calls.setdefault(tgt, [])
                    hit = next((x for x in lst if x[0] == w), None)
                    if hit is None:
                        lst.append((w, set(triggers_of(d))))
                    else:
                        hit[1].update(triggers_of(d))
    return calls


GITLAB_GLOBAL = {'default', 'include', 'stages', 'variables', 'workflow', 'image', 'services', 'before_script', 'after_script',
                 'cache', 'spec'}


def gitlab_jobs(tree, path):
    txt = tree.read(path)
    if txt is None:
        return None, 'unreadable'
    try:
        d = load_yaml(txt)
    except Exception:
        return None, 'does not parse'
    if not isinstance(d, dict):
        return None, 'does not parse'
    notes = []
    inc = d.get('include')
    incs = inc if isinstance(inc, list) else ([inc] if inc else [])
    for x in incs:
        p = x.get('local') if isinstance(x, dict) else (x if isinstance(x, str) and not x.startswith('http') else None)
        if p:
            p = J(p.lstrip('/'))
            t2 = tree.read(p) if tree.exists(p) else None
            try:
                d2 = load_yaml(t2) if t2 else None
            except Exception:
                d2 = None
            if isinstance(d2, dict):
                for k, v in d2.items():
                    d.setdefault(k, v)
            else:
                notes.append(f'include {p} not read')
        else:
            notes.append('external include')
    gvars = {str(k): _fmt(v if not isinstance(v, dict) else v.get('value')) for k, v in (d.get('variables') or {}).items()} \
        if isinstance(d.get('variables'), dict) else {}
    default = d.get('default') if isinstance(d.get('default'), dict) else {}
    gbefore = default.get('before_script', d.get('before_script'))
    out = []
    for name, job in d.items():
        if name in GITLAB_GLOBAL or str(name).startswith('.') or not isinstance(job, dict):
            continue
        ext = job.get('extends')
        merged = {}
        for e in ([ext] if isinstance(ext, str) else ext if isinstance(ext, list) else []):
            if isinstance(d.get(e), dict):
                merged.update(d[e])
        merged.update(job)
        if 'script' not in merged:
            continue
        before = merged.get('before_script', gbefore)

        def lines(x):
            if isinstance(x, str):
                return [x]
            if isinstance(x, list):
                return [y for z in x for y in lines(z)]
            return []
        jvars = {str(k): _fmt(v if not isinstance(v, dict) else v.get('value')) for k, v in (merged.get('variables') or {}).items()} \
            if isinstance(merged.get('variables'), dict) else {}
        env = {**gvars, **jvars}
        text = '\n'.join(lines(before) + lines(merged.get('script')))
        par = merged.get('parallel')
        combos = [{}]
        if isinstance(par, dict) and isinstance(par.get('matrix'), list):
            combos = []
            for m in par['matrix']:
                if isinstance(m, dict):
                    ks = list(m)
                    vs = [m[k] if isinstance(m[k], list) else [m[k]] for k in ks]
                    combos += [dict(zip(ks, v)) for v in itertools.product(*vs)]
        seen = set()
        for c in combos:
            e2 = {**env, **{k: _fmt(v) for k, v in c.items()}}
            t = keep_run(text)
            key = json.dumps([t, e2], sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            avail = (e2.get('GIT_STRATEGY') or '').lower() != 'none'
            out.append({'job': str(name), 'variant': str(len(seen)), 'values': c,
                        'meta': {'triggers': ['gitlab'], 'container': _fmt(merged.get('image', d.get('image'))) or '',
                                 'gitlab_avail': avail, 'notes': notes},
                        'steps': [{'seq': 0, 'origin': 'gitlab', 'run': t, 'wd': '', 'env': e2, 'if': bool(merged.get('rules') or
                                                                                                         merged.get('only'))}]})
    return out, '; '.join(notes)


# ================================================================ task runners (one level)

def script_struct(text):
    return {'lines': [l for l in keep_run(text).split('\n') if l.strip()][:400]}


def make_struct(text, targets):
    """The recipe lines of the targets named (else the default), with their prerequisites and the targets their recipes
    call with make, one level each; Makefile variables substituted where literal."""
    text = re.sub(r'\\\r?\n', ' ', text)
    var = {}
    rules, order = {}, []
    cur = None
    for line in text.split('\n'):
        if line.startswith('\t'):
            if cur is not None:
                for c in cur:
                    rules[c]['lines'].append(line[1:].strip())
            continue
        s = line.split('#', 1)[0].rstrip()
        if not s.strip():
            continue
        m = re.match(r'^\s*(?:export\s+|override\s+)?([A-Za-z_][A-Za-z0-9_.-]*)\s*(\?=|:=|::=|\+=|=|!=)\s*(.*)$', s)
        if m and ':' not in m.group(1):
            k, op, v = m.groups()
            if op == '+=':
                var[k] = (var.get(k, '') + ' ' + v).strip()
            elif op == '?=':
                var.setdefault(k, v.strip())
            elif op == '!=':
                var[k] = UNK + 'shell⟩'
            else:
                var[k] = v.strip()
            cur = None
            continue
        m = re.match(r'^([^:=\t][^:=]*?)\s*::?\s*(?!=)(.*)$', s)
        if m:
            names = m.group(1).split()
            rest = m.group(2)
            recipe_inline = None
            if ';' in rest:
                rest, recipe_inline = rest.split(';', 1)
            deps = [x for x in rest.split() if not x.startswith('|')]
            cur = []
            for n in names:
                if n.startswith('.') and n not in order:
                    if n in ('.PHONY', '.DEFAULT_GOAL', '.SILENT', '.ONESHELL', '.EXPORT_ALL_VARIABLES', '.NOTPARALLEL'):
                        cur = None
                        continue
                rules.setdefault(n, {'deps': [], 'lines': []})
                rules[n]['deps'] += deps
                if recipe_inline:
                    rules[n]['lines'].append(recipe_inline.strip())
                order.append(n)
                cur.append(n)
            continue
        cur = None

    def expand(s, depth=0):
        def rep(m):
            k = m.group(1) or m.group(2)
            if k in ('MAKE',):
                return 'make'
            if k in var and depth < 5:
                return expand(var[k], depth + 1)
            if k.startswith('shell ') or k.startswith('wildcard ') or ' ' in k:
                return UNK + 'make⟩'
            return m.group(0)
        return re.sub(r'\$\(([^()]+)\)|\$\{([^{}]+)\}', rep, s)
    goal = var.get('.DEFAULT_GOAL')
    tlist = targets.split() if targets else ([goal] if goal else [n for n in order if not n.startswith('.') and '%' not in n][:1])
    if not tlist:
        return {'error': 'no target'}
    out = []
    for t in tlist:
        if t not in rules:
            pat = next((n for n in order if '%' in n and re.fullmatch(re.escape(n).replace('%', '(.+)'), t)), None)
            if pat is None:
                return {'error': f'target {t} not found'}
            stem = re.fullmatch(re.escape(pat).replace('%', '(.+)'), t).group(1)
            rules[t] = {'deps': [d.replace('%', stem) for d in rules[pat]['deps']],
                        'lines': [l.replace('$*', stem).replace('$@', t) for l in rules[pat]['lines']]}
        seq = []
        for dep in rules[t]['deps']:
            if dep in rules and dep != t:
                seq.append((dep, rules[dep]['lines']))
        seq.append((t, rules[t]['lines']))
        for name, ls in seq:
            lines = []
            for l in ls:
                l2 = expand(l).lstrip('@-+ ')
                m = re.match(r'^make\s+(?:-[A-Za-z]\s+)*([A-Za-z0-9_.-]+)\s*$', l2)
                if m and m.group(1) in rules and m.group(1) != name:
                    lines += [expand(x).lstrip('@-+ ') for x in rules[m.group(1)]['lines']]
                else:
                    lines.append(l2)
            out.append({'name': name, 'lines': [x for x in lines if keep_run(x)][:200]})
    return {'targets': out}


def just_struct(text, recipe):
    rules, order, cur = {}, [], None
    for line in text.replace('\r\n', '\n').split('\n'):
        if line.startswith((' ', '\t')) and cur:
            rules[cur]['lines'].append(line.strip())
            continue
        m = re.match(r'^@?([A-Za-z0-9_-]+)(\s+[^:]*)?:\s*(.*)$', line)
        if m and not line.startswith(('set ', 'export ', 'alias ', 'import ', 'mod ')) and ':=' not in line:
            cur = m.group(1)
            rules[cur] = {'deps': m.group(3).split(), 'lines': []}
            order.append(cur)
            continue
        cur = None if line.strip() else cur
    t = recipe or (order[0] if order else None)
    if t not in rules:
        return {'error': f'recipe {t} not found'}
    out = []
    for dep in rules[t]['deps']:
        if dep in rules:
            out.append({'name': dep, 'lines': [x.lstrip('@-') for x in rules[dep]['lines'] if keep_run(x)]})
    out.append({'name': t, 'lines': [x.lstrip('@-') for x in rules[t]['lines'] if keep_run(x)]})
    return {'targets': out}


def _tox_lines(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [x.strip() for x in str(v).split('\n') if x.strip()]


def _strip_factor(line):
    m = re.match(r'^[!A-Za-z0-9_.,{}-]+\s*:\s+(.*)$', line)
    return m.group(1) if m and not re.match(r'^(https?|git\+|file):', line) else line


def tox_struct(tree, d, envs):
    """tox's configuration at directory d or its nearest ancestor with one, for the environments named (T1, T2)."""
    cand = None
    p = d
    while True:
        for n in ('tox.ini', 'tox.toml', 'pyproject.toml', 'setup.cfg'):
            f = J(p, n)
            if tree.exists(f):
                txt = tree.read(f)
                if txt is None:
                    continue
                if n == 'tox.ini' or (n == 'setup.cfg' and '[tox:tox]' in txt) or n == 'tox.toml' or \
                        (n == 'pyproject.toml' and re.search(r'^\[tool\.tox', txt, re.M)):
                    cand = (f, n, txt)
                    break
        if cand or p == '':
            break
        p = posixpath.dirname(p)
    if not cand:
        return None
    f, n, txt = cand
    root = posixpath.dirname(f)
    base, named, env_list, labels = {}, {}, [], {}
    try:
        if n in ('tox.ini', 'setup.cfg'):
            cp = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
            cp.read_string(txt)
            top = 'tox' if n == 'tox.ini' else 'tox:tox'
            if cp.has_section(top):
                env_list = [x.strip() for x in re.split(r'[,\n]', cp.get(top, 'envlist', fallback=cp.get(top, 'env_list', fallback='')))
                            if x.strip()]
            for sec in cp.sections():
                sname = sec[len('testenv'):] if sec.startswith('testenv') else None
                if n == 'setup.cfg' and sec.startswith('testenv'):
                    sname = sec[len('testenv'):]
                if sname is None:
                    continue
                data = {k: cp.get(sec, k) for k in cp.options(sec)}
                if sname == '':
                    base = data
                elif sname.startswith(':'):
                    named[sname[1:]] = data
        else:
            t = tomllib.loads(txt)
            if n == 'pyproject.toml':
                t = (t.get('tool') or {}).get('tox') or {}
                if 'legacy_tox_ini' in t:
                    cp = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
                    cp.read_string(t['legacy_tox_ini'])
                    env_list = [x.strip() for x in re.split(r'[,\n]', cp.get('tox', 'envlist', fallback='')) if x.strip()] \
                        if cp.has_section('tox') else []
                    for sec in cp.sections():
                        if sec == 'testenv':
                            base = {k: cp.get(sec, k) for k in cp.options(sec)}
                        elif sec.startswith('testenv:'):
                            named[sec[8:]] = {k: cp.get(sec, k) for k in cp.options(sec)}
                    t = {}
            env_list = env_list or [str(x) for x in (t.get('env_list') or t.get('envlist') or [])]
            if isinstance(t.get('env_run_base'), dict):
                base = t['env_run_base']
            for k, v in (t.get('env') or {}).items():
                if isinstance(v, dict):
                    named[k] = v
    except Exception as ex:
        return {'error': f'tox configuration {f} does not parse ({type(ex).__name__})', 'file': f}
    if envs == 'ALL_DEFAULT' or not envs:
        want = env_list or (list(named) if named else ['py'])
    else:
        want = envs.split(',')
    out = []
    for e in want:
        if e.upper() == 'ALL':
            return {'error': 'tox -e ALL', 'file': f}
        if '{' in e:
            e2 = e
        else:
            e2 = e
        cfg = dict(base)
        if e2 in named:
            cfg.update(named[e2])
        for k in list(cfg):
            cfg[k.replace('-', '_')] = cfg[k]
        deps = [_strip_factor(x) for x in _tox_lines(cfg.get('deps'))]
        deps = [x.replace('{toxinidir}', '.').replace('{tox_root}', '.') for x in deps]
        deps = [re.sub(r'\{\[testenv\]deps\}', ' '.join(_tox_lines(base.get('deps'))), x) for x in deps]
        cons = [x.replace('{toxinidir}', '.').replace('{tox_root}', '.') for x in _tox_lines(cfg.get('constraints'))]
        runner = str(cfg.get('runner') or '').strip()
        skip = str(cfg.get('skip_install', 'false')).strip().lower() in ('true', '1', 'yes')
        package = str(cfg.get('package') or '').strip().lower()
        if str(cfg.get('usedevelop', cfg.get('use_develop', 'false'))).strip().lower() in ('true', '1', 'yes'):
            package = 'editable'
        if skip:
            package = 'skip'
        extras = [_strip_factor(x) for x in _tox_lines(cfg.get('extras'))]
        cmds = []
        if runner == 'uv-venv-lock-runner':
            cmds.append('uv sync' + ''.join(f' --extra {shlex.quote(x)}' for x in extras if x))
        else:
            args = []
            for x in deps:
                if any(ch in x for ch in '{}'):
                    args.append(UNK + 'tox:' + x[:40] + '⟩')
                    continue
                args += shlex.split(x) if x.startswith('-') else [x]
            for c in cons:
                args += ['-c', c]
            if args:
                cmds.append('pip install ' + ' '.join(shlex.quote(a) for a in args))
            if package not in ('skip', 'external'):
                tgt = '.' + (f'[{",".join(x for x in extras if x)}]' if any(extras) else '')
                cmds.append('pip install ' + ('-e ' if package in ('editable', 'editable-legacy') else '') + shlex.quote(tgt))
            elif package == 'external':
                cmds.append(UNK + 'tox external package⟩')
        for key in ('commands_pre', 'commands'):
            for x in _tox_lines(cfg.get(key)):
                x = _strip_factor(x) if not isinstance(cfg.get(key), list) else x
                if isinstance(x, str) and keep_run(x):
                    cmds.append(x.replace('{toxinidir}', '.').replace('{tox_root}', '.').replace('{posargs}', ''))
            if isinstance(cfg.get(key), list):
                for x in cfg.get(key):
                    if isinstance(x, list):
                        s = ' '.join(shlex.quote(str(y)) for y in x)
                        if keep_run(s):
                            cmds.append(s)
        cd = ''
        facs = set(re.split(r'[-,]', e))
        for x in _tox_lines(cfg.get('changedir') or cfg.get('change_dir')):
            m = re.match(r'^([!A-Za-z0-9_.,{}-]+)\s*:\s+(.*)$', x)
            if m:
                fs = set(m.group(1).split(','))
                if any((f[1:] not in facs) if f.startswith('!') else (f in facs) for f in fs):
                    cd = m.group(2).strip()
            else:
                cd = x.strip()
        cd = cd.replace('{toxinidir}', '.').replace('{tox_root}', '.')
        out.append({'name': e, 'commands': cmds, 'changedir': J(root, cd) if cd and '{' not in cd else ''})
    return {'root': root, 'file': f, 'envs': out}


INSTALLERS = ('pip', 'uv', 'poetry', 'pdm', 'pipenv', 'conda', 'mamba', 'micromamba', 'python', 'python3')


def nox_struct(text, sessions):
    """Sessions of a noxfile: the install commands of session.install, run_install, run and conda_install (N1)."""
    try:
        tree = ast.parse(text)
    except Exception:
        return {'error': 'noxfile does not parse'}
    defaults = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Attribute) and t.attr == 'sessions' and
                                                isinstance(t.value, ast.Attribute) and t.value.attr == 'options'
                                                for t in node.targets):
            if isinstance(node.value, (ast.List, ast.Tuple)) and all(isinstance(e, ast.Constant) for e in node.value.elts):
                defaults = [e.value for e in node.value.elts]
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        name = None
        for dec in node.decorator_list:
            d = dec.func if isinstance(dec, ast.Call) else dec
            dn = d.attr if isinstance(d, ast.Attribute) else d.id if isinstance(d, ast.Name) else ''
            if dn == 'session':
                name = node.name
                if isinstance(dec, ast.Call):
                    for kw in dec.keywords:
                        if kw.arg == 'name' and isinstance(kw.value, ast.Constant):
                            name = kw.value.value
        if not name:
            continue
        cmds, unparsed = [], []
        for sub in ast.walk(node):
            if not (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)):
                continue
            meth = sub.func.attr
            if meth not in ('install', 'run_install', 'run', 'conda_install', 'run_always'):
                continue
            args = []
            ok = True
            for a in sub.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    args.append(a.value)
                elif isinstance(a, ast.Starred):
                    ok = False
                    args.append(UNK + 'nox:*⟩')
                else:
                    ok = False
                    args.append(UNK + 'nox:' + ast.unparse(a)[:30] + '⟩')
            if meth == 'install':
                cmds.append('pip install ' + ' '.join(shlex.quote(x) for x in args))
            elif meth == 'conda_install':
                if any(names for names in args):
                    cmds.append('conda install ' + ' '.join(shlex.quote(x) for x in args))
            else:
                if args and args[0] in INSTALLERS or (args and args[0].startswith(UNK)):
                    s = ' '.join(shlex.quote(x) for x in args)
                    if keep_run(s) or args[0].startswith(UNK):
                        cmds.append(s)
            if not ok and meth in ('install', 'run_install'):
                unparsed.append(ast.unparse(sub)[:80])
        found[name] = {'name': name, 'commands': cmds, 'unparsed': '; '.join(unparsed)}
    want = sessions.split(',') if sessions and sessions != 'DEFAULT' else (defaults or list(found))
    out = []
    for s in want:
        base = s.split('(')[0].split('-')[0] if s not in found else s
        if s in found:
            out.append(found[s])
        elif base in found:
            out.append(found[base])
        else:
            return {'error': f'session {s} not found'}
    return {'sessions': out}


def uv_member(tree, root, name):
    """Amendment 3: the directory of the uv workspace member named `name` under `root` (the pyproject.toml whose
    [project] name matches, after PEP 503 normalisation), and of the workspace members it lists with
    `{ workspace = true }` in [tool.uv.sources], one level."""
    from common import norm
    import fnmatch
    if name == '*':
        # every member of the workspace rooted at `root`, by its [tool.uv.workspace] members and exclude globs
        rt = tree.read(J(root, 'pyproject.toml')) if tree.exists(J(root, 'pyproject.toml')) else None
        try:
            ws = (((tomllib.loads(rt).get('tool') or {}).get('uv') or {}).get('workspace') or {}) if rt else {}
        except Exception:
            ws = {}
        mem, exc = ws.get('members') or [], ws.get('exclude') or []
        dirs = sorted({posixpath.dirname(f) for f in tree.files if f.endswith('pyproject.toml')
                       and posixpath.dirname(f) != root
                       and any(fnmatch.fnmatch(posixpath.relpath(posixpath.dirname(f), root or '.'), g) for g in mem)
                       and not any(fnmatch.fnmatch(posixpath.relpath(posixpath.dirname(f), root or '.'), g) for g in exc)})
        return {'dirs': dirs}
    found = {}
    for f in sorted(tree.files):
        if not f.endswith('pyproject.toml') or not (root == '' or f.startswith(root + '/')):
            continue
        txt = tree.read(f)
        if not txt:
            continue
        try:
            t = tomllib.loads(txt)
        except Exception:
            continue
        nm = ((t.get('project') or {}).get('name') or '')
        if nm:
            found[norm(nm)] = (posixpath.dirname(f), t)
    hit = found.get(norm(name))
    if not hit:
        return {'dirs': []}
    d, t = hit
    dirs = [d]
    srcs = (((t.get('tool') or {}).get('uv') or {}).get('sources') or {})
    for k, v in srcs.items():
        if isinstance(v, dict) and v.get('workspace') and norm(k) in found:
            dirs.append(found[norm(k)][0])
    return {'dirs': dirs}


def hatch_struct(tree, proj, env):
    """A hatch environment's install (H1, H2): the project in development mode unless skip-install or dev-mode false,
    its dependencies and features, and pre- and post-install commands; a locked environment is judged."""
    cfg_all = {}
    for n in ('hatch.toml', 'pyproject.toml'):
        f = J(proj, n)
        if tree.exists(f):
            txt = tree.read(f)
            if txt is None:
                return {'error': f'{f} unreadable'}
            try:
                t = tomllib.loads(txt)
            except Exception:
                return {'error': f'{f} does not parse'}
            envs = t.get('envs') if n == 'hatch.toml' else ((t.get('tool') or {}).get('hatch') or {}).get('envs')
            for k, v in (envs or {}).items():
                if isinstance(v, dict):
                    cfg_all.setdefault(k, {}).update(v)
    base_env = env.split('.')[0]
    chain, seen = [], set()
    cur = base_env
    while cur and cur not in seen:
        seen.add(cur)
        c = cfg_all.get(cur, {})
        chain.append(c)
        if cur == 'default':
            break
        cur = c.get('template', 'default' if cur not in ('hatch-test', 'hatch-static-analysis', 'hatch-build') else None)
    cfg = {}
    for c in reversed(chain):
        cfg.update(c)
    if cfg.get('type') not in (None, 'virtual'):
        return {'error': f'hatch environment type {cfg.get("type")}'}
    if cfg.get('locked'):
        return {'error': 'hatch locked environment'}
    cmds = []
    for x in cfg.get('pre-install-commands') or []:
        if keep_run(str(x)):
            cmds.append(str(x))
    if not cfg.get('skip-install', False):
        feats = cfg.get('features') or []
        tgt = '.' + (f'[{",".join(feats)}]' if feats else '')
        cmds.append('pip install ' + ('' if cfg.get('dev-mode', True) is False else '-e ') + shlex.quote(tgt))
    deps = list(cfg.get('dependencies') or []) + list(cfg.get('extra-dependencies') or [])
    if deps:
        cmds.append('pip install ' + ' '.join(shlex.quote(str(x)) for x in deps))
    for x in cfg.get('post-install-commands') or []:
        if keep_run(str(x)):
            cmds.append(str(x))
    return {'commands': cmds, 'env': env}


# ================================================================ documented install commands (S5)

DOC_CMD = re.compile(r'^\s*(?:\$|%|>|!)?\s*((?:sudo\s+)?(?:python3?\s+-m\s+)?(?:pip3?|uv|uvx|poetry|pipenv|pdm|pipx|conda|mamba|'
                     r'micromamba|pip-sync|make|tox|nox|hatch)\b.*)$')


def doc_commands(text):
    """Install commands in fenced or indented code blocks, or after a shell prompt, of a README or CONTRIBUTING file."""
    out = []
    fence = False
    for i, line in enumerate(text.replace('\r\n', '\n').split('\n')):
        s = line.rstrip()
        if re.match(r'^\s*(```|~~~)', s):
            fence = not fence
            continue
        code = fence or line.startswith(('    ', '\t')) or re.match(r'^\s*[$%]\s', s)
        if not code:
            continue
        m = DOC_CMD.match(s)
        if m:
            out.append((i + 1, m.group(1)[:400]))
    return out[:200]
