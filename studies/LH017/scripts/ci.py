"""LH017: the class of each CI job for a pair, by the brief's rules ("Steps, files and working directories", "How
installers treat a pinned or locked file", "Classes of a job for a pair").

Shared by collect.py, which runs it against the live tree and records every query and every relevant line it reads
(data/tree_paths.csv, data/aux_lines.csv), and classify.py, which replays those records offline. The installer rules
(pip_args, pip_like, package, req_file, project, lock_step, uv, compile_or_sync, poetry, pipenv, pdm, decide) are
LH015's (studies/LH015/scripts/classify.py), with a CI job's checkout and working directory in place of a recipe's
build context, and with the brief's changes: a later step the rules cannot read does not undo class 1 (it is flagged),
and class 5 has the sub-label "container build only".
"""
import json
import os
import posixpath
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401
from packaging.requirements import Requirement, InvalidRequirement  # noqa: E402

UNK = '⟨EXPR:'          # a value the rules cannot substitute
WS = '/__ws__'          # the workspace root (GITHUB_WORKSPACE, ${{ github.workspace }}, CI_PROJECT_DIR)
OUT = '/__out__'        # a working directory outside the workspace (a literal absolute path elsewhere)
AMEND1 = os.environ.get('LH017_NO_A1') != '1'   # amendment 1 (studies/LH017/amendments.md)
AMEND2 = os.environ.get('LH017_NO_A2') != '1'   # amendment 2


def J(*parts):
    ps = [p for p in parts if p not in ('', None, '.')]
    if not ps:
        return ''
    p = posixpath.normpath(posixpath.join(*ps))
    return '' if p == '.' else p


def eff(kind, **kw):
    kw['kind'] = kind
    return kw


def truthy(v):
    return (v or '').strip().lower() not in ('', '0', 'false', 'no', 'off')


# ================================================================ shell text

KEYWORDS = {'if', 'then', 'else', 'elif', 'fi', 'do', 'done', 'while', 'until', 'for', 'case', 'esac', '!', '{', '}', 'in'}


def join_continuations(s):
    return re.sub(r'\\\r?\n', ' ', s or '')


def commands(s, depth=0):
    """Simple commands of a shell text as token lists (LH015's); `sh -c '...'` is opened; redirections kept."""
    out = []
    for line in join_continuations(s).split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            lx = shlex.shlex(line, posix=True, punctuation_chars=True)
            lx.whitespace_split = True
            lx.commenters = '#'
            toks = list(lx)
        except ValueError:
            toks = line.split()
        cur = []
        for t in toks:
            if t and set(t) <= set(';&|()'):
                if cur:
                    out.append(cur)
                cur = []
            elif not cur and t in KEYWORDS:
                continue
            else:
                cur.append(t)
        if cur:
            out.append(cur)
    res = []
    for c in out:
        b = posixpath.basename(c[0]) if c else ''
        if b in ('sh', 'bash', 'dash', 'zsh', 'ash') and '-c' in c[1:3] and depth < 2:
            k = c.index('-c')
            if k + 1 < len(c):
                res.extend(commands(c[k + 1], depth + 1))
                continue
        res.append(c)
    return res


def strip_prefix(c):
    env, i = {}, 0
    while i < len(c):
        t, b = c[i], posixpath.basename(c[i])
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', t):
            k, _, v = t.partition('=')
            env[k] = v
        elif b in ('sudo', 'exec', 'time', 'nice', 'nohup', 'command', 'eval', 'env', 'xvfb-run', 'retry'):
            pass
        elif b in ('timeout',):
            i += 1
        elif t == '--' or (i > 0 and t.startswith('-') and posixpath.basename(c[i - 1]) in ('env', 'sudo', 'xvfb-run')):
            pass
        else:
            break
        i += 1
    return env, c[i:]


def redirect_out(c):
    out, res, i = None, [], 0
    while i < len(c):
        t = c[i]
        if t in ('>', '>>', '>|'):
            if i + 1 < len(c):
                out = c[i + 1]
            i += 2
            continue
        if t in ('<', '>&', '<&', '2>', '&>') or re.fullmatch(r'\d?>&?\d?', t):
            i += 2 if t in ('<', '>&', '<&', '&>') else 1
            continue
        res.append(t)
        i += 1
    return res, out


PYTHON = re.compile(r'^(python|pypy|py)(\d(\.\d+)?)?(\.exe)?$')
TOOLS = ('uv', 'poetry', 'pipenv', 'pdm', 'pipx', 'conda', 'mamba', 'micromamba', 'pip-sync', 'pip-compile', 'make', 'gmake',
         'just', 'nox', 'tox', 'hatch', 'uvx', 'pre-commit', 'prek', 'docker', 'podman', 'docker-compose', 'buildah')
MODULES = {'pip': 'pip', 'uv': 'uv', 'pipx': 'pipx', 'pipenv': 'pipenv', 'poetry': 'poetry', 'pdm': 'pdm', 'piptools': 'piptools',
           'build': 'build', 'tox': 'tox', 'nox': 'nox', 'hatch': 'hatch', 'pre_commit': 'pre-commit'}


def parse_cmd(c):
    """{'fam', 'args', 'env', 'out', 'argv0'} for an installer, task runner, make target, script call, cd or container
    build; None otherwise."""
    env, c = strip_prefix(c)
    c, out = redirect_out(c)
    if not c:
        return None
    b = posixpath.basename(c[0])
    r = {'env': env, 'out': out, 'args': c[1:], 'argv0': c[0]}
    if b in ('cd', 'pushd', 'popd'):
        r['fam'] = b
    elif b == 'export':
        r['fam'] = 'export'
    elif b == 'echo' and out and re.search(r'GITHUB_ENV', out):
        r['fam'] = 'github_env'
    elif re.fullmatch(r'pip(\d(\.\d+)?)?(\.exe)?', b):
        r['fam'] = 'pip'
    elif PYTHON.match(b) or b.endswith('/python') or b.endswith('/python3'):
        j = 1
        while j < len(c) and c[j].startswith('-') and c[j] not in ('-m', '-c'):
            j += 1
        if j + 1 < len(c) and c[j] == '-m':
            mod = c[j + 1]
            r['args'] = c[j + 2:]
            if mod not in MODULES:
                return None
            r['fam'] = MODULES[mod]
        elif j < len(c) and c[j].endswith('setup.py'):
            r['fam'], r['script'], r['args'] = 'setup.py', c[j], c[j + 1:]
        else:
            return None
    elif b in TOOLS:
        r['fam'] = b
    elif b in ('sh', 'bash', 'dash', 'zsh', 'ash', 'source', '.'):
        a = [x for x in c[1:] if not x.startswith('-')]
        if not a:
            return None
        r['fam'], r['script'], r['args'] = ('source' if b in ('source', '.') else 'call'), a[0], a[1:]
    elif (c[0].startswith(('./', '../', WS)) or b.endswith('.sh')) and re.fullmatch(r'[\w./@+~-]+', c[0].replace(WS, '/ws')):
        r['fam'], r['script'] = 'call', c[0]
    else:
        return None
    return r


def sub_and_flags(args, valued):
    """Subcommand words and flags of uv, poetry, pdm, pipenv, conda or hatch; valued flags take the next word (LH015)."""
    subs, flags, vals, pos, i = [], set(), {}, [], 0
    while i < len(args):
        a = args[i]
        if a.startswith('-'):
            k, eq, v = a.partition('=')
            if k in valued:
                if not eq:
                    v = args[i + 1] if i + 1 < len(args) else ''
                    i += 1
                vals.setdefault(k, []).append(v)
            else:
                flags.add(k)
        elif len(subs) < 2 and not pos and re.fullmatch(r'[a-z][a-z-]*', a) and (not subs or subs[0] in ('pip', 'tool', 'env', 'self')):
            subs.append(a)
        else:
            pos.append(a)
        i += 1
    return subs, flags, vals, pos


PIP_VALUED = {'-r', '--requirement', '-c', '--constraint', '-e', '--editable', '-i', '--index-url', '--extra-index-url', '-f',
              '--find-links', '--upgrade-strategy', '-t', '--target', '--prefix', '--root', '--src', '--no-binary', '--only-binary',
              '--platform', '--python-version', '--implementation', '--abi', '--trusted-host', '--cache-dir', '--log', '--timeout',
              '--retries', '--proxy', '--cert', '--client-cert', '--progress-bar', '--root-user-action', '-C', '--config-settings',
              '--global-option', '--install-option', '--python', '-p', '--index-strategy', '--extra', '--group', '--resolution',
              '--prerelease', '--exclude-newer', '--link-mode', '--keyring-provider', '--report', '--override', '--overrides',
              '--build-constraint', '--build-constraints', '-b', '--config-file', '--python-platform', '--torch-backend',
              '--default-index', '--index', '--refresh-package', '-P', '--upgrade-package', '--reinstall-package', '--exclude',
              '-w', '--wheel-dir', '--use-feature', '--no-build-package', '--no-binary-package', '--only-binary-package', '-o',
              '--output-file', '--python-preference', '--directory', '--project', '--package', '--suffix', '--pip-args', '--spec',
              '--with', '--from', '--cache', '--annotation-style', '--resolver', '--extra-index', '-x', '-d', '--dest'}


def pip_args(args):
    """LH015's reading of pip's (and uv pip's) arguments."""
    r = {'req': [], 'con': [], 'paths': [], 'pkgs': [], 'remote': [], 'upgrade': False, 'eager': False, 'force': False,
         'no_deps': False, 'upgrade_pkgs': [], 'wheel_dir': None, 'out': None, 'unk': []}
    i = 0
    while i < len(args):
        a, v = args[i], None
        k = a
        if a.startswith('--') and '=' in a:
            k, v = a.split('=', 1)
        elif re.match(r'^-[rce][^-]', a):
            k, v = a[:2], a[2:]
        if k in PIP_VALUED and v is None:
            v = args[i + 1] if i + 1 < len(args) else ''
            i += 1
        if k in ('-r', '--requirement'):
            r['req'].append(v)
        elif k in ('-c', '--constraint'):
            r['con'].append(v)
        elif k in ('-e', '--editable'):
            (r['remote'] if re.match(r'^[a-z+]+://|^git\+', v) else r['paths']).append(v)
        elif k in ('-U', '--upgrade'):
            r['upgrade'] = True
        elif k == '--upgrade-strategy':
            r['eager'] = v == 'eager'
        elif k in ('--force-reinstall', '--reinstall'):
            r['force'] = True
        elif k in ('-P', '--upgrade-package'):
            r['upgrade_pkgs'].append(v)
        elif k == '--no-deps':
            r['no_deps'] = True
        elif k in ('-w', '--wheel-dir'):
            r['wheel_dir'] = v
        elif k in ('-o', '--output-file'):
            r['out'] = v
        elif k.startswith('-'):
            pass
        elif re.match(r'^(git\+|hg\+|svn\+|bzr\+|https?://|file:)', a) and not a.startswith('file:.'):
            r['remote'].append(a)
        elif (UNK in a or '$' in a) and not re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]*\])?\s*(==|>=|<=|~=|!=|<|>)', a):
            r['unk'].append(a)
        elif a in ('.', '..') or a.startswith(('.', '/', '~')) or '/' in a.split('[')[0] or \
                re.search(r'\.(whl|tar\.gz|zip|tgz)$', a) or a.startswith('file:'):
            r['paths'].append(a[5:] if a.startswith('file:') else a)
        else:
            r['pkgs'].append(a)
        i += 1
    return r


def spec_of(lines, lib):
    """PEP 508 specifiers of the library found in the lines (LH015's)."""
    out = []
    for t in lines:
        s = t.split('#', 1)[0].strip()
        if not names_lib(s, lib):
            continue
        cands = re.findall(r'["\']([^"\']+)["\']', s) or [s]
        found = False
        for x in cands:
            try:
                rq = Requirement(x.strip().rstrip(','))
            except InvalidRequirement:
                continue
            if norm(rq.name) == norm(lib):
                out.append(str(rq.specifier) + (f'; {rq.marker}' if rq.marker else ''))
                found = True
        if not found:
            m = re.match(r'^\s*"?' + lib_re(lib) + r'"?\s*=\s*(?:\{[^}]*version\s*=\s*)?"([^"]+)"', s, re.I)
            out.append('poetry:' + m.group(1) if m else '?')
    return out


def includes(lines):
    out = []
    for t in lines:
        s = t.split(' #', 1)[0].strip()
        m = re.match(r'^(-r|--requirement|-c|--constraint)\s*=?\s*(\S+)', s)
        if m:
            out.append((m.group(1).lstrip('-')[0], m.group(2)))
    return out


def req_paths(lines):
    """Local project installs inside a requirements file (`-e .`, `.`, `./x`, `file:.`), read as pip reads them."""
    out = []
    for t in lines:
        s = t.split(' #', 1)[0].strip()
        m = re.match(r'^(?:-e|--editable)\s*=?\s*(\S+)', s)
        x = m.group(1) if m else s
        if re.match(r'^(\.|\.\.|\./|\.\./|file:\.)', x) and not x.startswith(('-', '..py')):
            out.append(x[5:] if x.startswith('file:') else x)
    return out


# ================================================================ a job's walk

class Job:
    """One job variant for one pair: its steps, the pair's T and L, and the tree at the snapshot."""

    def __init__(self, steps, tree, T, T_kind, L, pinned, own, system='github', base_env=None):
        self.steps, self.tree = steps, tree
        self.T, self.T_kind, self.L, self.pinned = set(T), T_kind, L, pinned
        self.own = {norm(x) for x in own if x}
        self.system = system
        self.base_env = dict(base_env or {})
        self.effects, self.notes, self.tool_specs, self.flags = [], [], {}, set()


class State:
    def __init__(self, J_):
        self.avail = J_.system == 'gitlab'     # repository files available (after a checkout)
        self.prefix = ''                       # where the repository sits in the workspace
        self.cwd = ''                          # workspace-relative
        self.env = dict(J_.base_env)
        self.gen, self.wheels, self.artefacts = {}, {}, {}
        self.relocked = set()
        self.step = None
        self.depth = 0
        self.dirstack = []


def ws_path(st, p):
    """A path as written in a command, as a workspace-relative path; None if outside the workspace; UNK if unknown."""
    p = p.strip()
    if UNK in p or '$' in p or '`' in p:
        return UNK
    if p.startswith(WS):
        p = p[len(WS):].lstrip('/')
        return J(p)
    if p.startswith('~') or p.startswith('/'):
        return None
    if st.cwd == UNK:
        return UNK
    if st.cwd == OUT:
        return None
    return J(st.cwd, p)


def resolve(B, st, p):
    """('repo', rp) | ('missing', rp) | ('gen', idx) | ('wheelsrc', dir) | ('artefact', dir) | ('outside', p) |
    ('nocheckout', p) | ('unknown', p)."""
    w = ws_path(st, p)
    if w == UNK:
        return ('unknown', p)
    if w is None or w.startswith('../') or w == '..':
        return ('outside', p)
    for g, idx in st.gen.items():
        if w == g:
            return ('gen', idx)
    for a in st.artefacts:
        if w == a or w.startswith(a + '/'):
            return ('artefact', a)
    if not st.avail:
        return ('nocheckout', p)
    if st.prefix and not (w == st.prefix or w.startswith(st.prefix + '/')):
        return ('outside', p)
    rp = w[len(st.prefix):].lstrip('/') if st.prefix else w
    if B.tree.exists(rp):
        return ('repo', rp)
    return ('missing', rp)


def run_text(B, st, text, origin):
    for c in commands(run_text_prep(text)):
        step_command(B, st, c, origin)


LS_GLOB = re.compile(r'\$\(\s*(?:\(\s*cd\s+[\w./-]+\s*&&\s*)?ls\s+(?:-\w+\s+)*([\w./*?\[\]-]+)\s*\)?\s*\)|'
                     r'`\s*(?:\(\s*cd\s+[\w./-]+\s*&&\s*)?ls\s+(?:-\w+\s+)*([\w./*?\[\]-]+)\s*\)?\s*`')


def run_text_prep(text):
    """Amendment 1: a command substitution that lists files by a literal pattern (with or without a `cd` into the
    directory first) is read as that pattern."""
    return LS_GLOB.sub(lambda m: m.group(1) or m.group(2), text) if AMEND1 else text


def subst_env(st, toks):
    out = []
    for t in toks:
        if '$' in t:
            def rep(m):
                k = m.group(1) or m.group(2)
                if k in ('GITHUB_WORKSPACE', 'CI_PROJECT_DIR'):
                    return WS
                if k in ('RUNNER_TEMP', 'HOME', 'RUNNER_TOOL_CACHE', 'TMPDIR'):
                    return OUT
                if k == 'PWD':
                    return WS + ('/' + st.cwd if st.cwd else '')
                if k in st.env and '$' not in st.env[k]:
                    return st.env[k]
                return m.group(0)
            t = re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)', rep, t)
        out.append(t)
    return out


def step_command(B, st, c, origin):
    c = subst_env(st, c)
    if AMEND1 and c and all(re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', t) for t in c):
        for t in c:
            k, _, v = t.partition('=')
            st.env[k] = v
        return
    p = parse_cmd(c)
    if not p:
        return
    fam = p['fam']
    if fam in ('cd', 'pushd'):
        a = [x for x in p['args'] if not x.startswith('-')]
        if fam == 'pushd':
            st.dirstack.append(st.cwd)
        if not a:
            st.cwd = ''
            return
        w = ws_path(st, a[0])
        if w is None and a[0].startswith(('/', '~')) and not a[0].startswith(WS) and '$' not in a[0] and UNK not in a[0]:
            st.cwd = OUT
            return
        st.cwd = w if w not in (None, UNK) else UNK
        return
    if fam == 'popd':
        st.cwd = st.dirstack.pop() if st.dirstack else st.cwd
        return
    if fam == 'export':
        for a in p['args']:
            if '=' in a:
                k, _, v = a.partition('=')
                st.env[k] = v
        return
    if fam == 'github_env':
        for a in p['args']:
            if '=' in a and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', a):
                k, _, v = a.partition('=')
                st.env[k] = v
        return
    installer(B, st, p, origin)


def installer(B, st, p, origin):
    n0 = len(B.effects)
    try:
        return _installer(B, st, p, origin)
    finally:
        fam = p['fam']
        if fam == 'uv' and p['args'][:1] == ['pip']:
            fam = 'uv pip'
        for e in B.effects[n0:]:
            e.setdefault('tool', fam)


def _installer(B, st, p, origin):
    fam, a, env = p['fam'], p['args'], {**st.env, **p['env']}
    if p.get('out'):
        env['__out'] = p['out']
    if fam in ('call', 'source'):
        if fam == 'source' and re.search(r'activate(\.sh)?$', p['script']):
            return
        return call_script(B, st, p, origin)
    if fam in ('make', 'gmake'):
        return make_call(B, st, p, origin)
    if fam == 'just':
        return just_call(B, st, p, origin)
    if fam == 'tox':
        return tox_call(B, st, a, origin)
    if fam == 'nox':
        return nox_call(B, st, a, origin)
    if fam == 'hatch':
        return hatch_call(B, st, a, origin)
    if fam in ('pre-commit', 'prek'):
        B.effects.append(eff('others', why='pre-commit hooks'))
        return
    if fam in ('docker', 'podman', 'docker-compose', 'buildah'):
        s = [x for x in a if not x.startswith('-')]
        if fam == 'buildah' and s[:1] in (['bud'], ['build']):
            B.effects.append(eff('container', why='container build'))
        elif s[:1] == ['build'] or s[:2] in (['buildx', 'build'], ['compose', 'build'], ['image', 'build']) or \
                (fam == 'docker-compose' and s[:1] == ['build']) or (s[:2] == ['compose', 'up'] and '--build' in a):
            B.effects.append(eff('container', why='container build'))
        elif s[:1] == ['run'] and re.search(r'\b(pip3?|uv|poetry|pipenv|pdm|tox|nox|hatch)\b.*\b(install|sync)\b|\btox\b|\bnox\b',
                                            ' '.join(a)):
            B.effects.append(eff('judge', why='install inside docker run'))
            B.flags.add('install in docker run')
        return
    if fam == 'uvx':
        return tool_run(B, st, a, env, origin)
    if fam == 'build':
        out = next((a[i + 1] for i, t in enumerate(a[:-1]) if t in ('--outdir', '-o')), None) or \
            next((t.split('=', 1)[1] for t in a if t.startswith('--outdir=')), None)
        src = next((t for t in a if not t.startswith('-') and t != out), '.')
        w = ws_path(st, src)
        if w not in (None, UNK):
            st.wheels[J(w, out) if out and not out.startswith('/') else J(w, 'dist')] = w
        return
    if fam == 'setup.py':
        if a[:1] and a[0] in ('install', 'develop'):
            return project(B, st, posixpath.dirname(p['script']) or '.', {'no_deps': False})
        if a[:1] and a[0] in ('bdist_wheel', 'sdist', 'build'):
            w = ws_path(st, posixpath.dirname(p['script']) or '.')
            if w not in (None, UNK):
                st.wheels[J(w, 'dist')] = w
        return
    if fam == 'pip':
        sub = next((x for x in a if not x.startswith('-')), '')
        rest = a[a.index(sub) + 1:] if sub else []
        if sub in ('install', 'download'):
            return pip_like(B, st, pip_args(rest), env, 'pip', sub)
        if sub == 'wheel':
            r = pip_args(rest)
            for x in r['paths']:
                w = ws_path(st, x)
                if w not in (None, UNK):
                    st.wheels[J(st.cwd, r['wheel_dir']) if r['wheel_dir'] else st.cwd] = w
            return
        return
    if fam == 'pipx':
        subs, flags, vals, pos = sub_and_flags(a, PIP_VALUED)
        if subs[:1] == ['run']:
            return tool_run(B, st, a[a.index('run') + 1:], env, origin)
        if subs[:1] in (['install'], ['inject']):
            return pip_like(B, st, pip_args(pos[1:] if subs[:1] == ['inject'] else pos), env, 'pipx', 'install')
        return
    if fam == 'piptools':
        sub = a[0] if a else ''
        fam, a = ('pip-compile' if sub == 'compile' else 'pip-sync'), a[1:]
    if fam == 'uv':
        return uv(B, st, a, env, origin)
    if fam in ('pip-compile', 'pip-sync'):
        return compile_or_sync(B, st, fam, a, env)
    if fam == 'poetry':
        return poetry(B, st, a, env, origin)
    if fam == 'pipenv':
        return pipenv(B, st, a, env)
    if fam == 'pdm':
        return pdm(B, st, a, env, origin)
    if fam in ('conda', 'mamba', 'micromamba'):
        subs, flags, vals, pos = sub_and_flags(a, {'-f', '--file', '-n', '--name', '-p', '--prefix', '-c', '--channel'})
        files = vals.get('-f', []) + vals.get('--file', [])
        if files:
            for f in files:
                env_file(B, st, f)
        elif subs[:1] in (['install'], ['create']):
            names = [norm(re.split(r'[=<>!~ ]', x)[0]) for x in pos]
            if norm(B.L) in names:
                B.effects.append(eff('judge', why='conda-level L'))
            elif names:
                B.effects.append(eff('others', why=f'{fam} packages'))
        return


def tool_run(B, st, a, env, origin):
    """uvx or pipx run: a tool in its own environment; tox, nox, hatch and the lock tools are dispatched."""
    i = 0
    frm = None
    while i < len(a) and a[i].startswith('-'):
        if a[i] in ('--from', '--with', '--python', '-p', '--spec', '--index-url', '--with-requirements'):
            if a[i] in ('--from', '--spec'):
                frm = a[i + 1] if i + 1 < len(a) else None
            i += 2
            continue
        i += 1
    if i >= len(a):
        return
    tool = re.split(r'[=<>@\[]', a[i])[0]
    rest = a[i + 1:]
    if tool in ('tox', 'nox', 'hatch', 'poetry', 'pdm', 'pipenv', 'pre-commit'):
        return installer(B, st, {'fam': tool, 'args': rest, 'env': {}, 'argv0': tool}, origin)
    if frm and (frm.startswith('.') or '/' in frm):
        return project(B, st, frm, {'no_deps': False})
    nm = norm(tool)
    if nm == norm(B.L):
        B.effects.append(eff('fresh', sub='inline', names_L=True, spec='any', overrides=False, why=f'L run as a tool {tool}'))
    else:
        B.effects.append(eff('others', pkg=nm, why=f'tool {nm}'))


def pip_like(B, st, r, env, tool, sub):
    up = r['upgrade'] or truthy(env.get('PIP_UPGRADE'))
    reqs = r['req'] + ([env['PIP_REQUIREMENT']] if env.get('PIP_REQUIREMENT') else [])
    cons = list(r['con'])
    if env.get('PIP_CONSTRAINT'):
        cons = cons + env['PIP_CONSTRAINT'].split()
    if env.get('UV_CONSTRAINT'):
        cons = cons + env['UV_CONSTRAINT'].split()
    for f in reqs:
        if f == '-':
            if st.gen.get('__stdin__') is not None:
                B.effects.append(eff('neutral', why='installs what the piped export wrote', gen=st.gen['__stdin__']))
            else:
                B.effects.append(eff('judge', why='requirements from standard input'))
            continue
        B.effects.append(req_file(B, st, f, up, r['force'], False))
    for f in cons:
        e = req_file(B, st, f, up, r['force'], True)
        if e['kind'] == 'fresh':
            e = eff('neutral', why='constraints file without L pin')
        B.effects.append(e)
    for x in r['paths']:
        project(B, st, x, r)
    for x in r['unk']:
        B.effects.append(eff('und', why='build argument', detail=x))
    for x in r['remote']:
        nm = re.sub(r'(\.git)?(@.*)?$', '', re.split(r'#egg=', x)[-1].rstrip('/').rsplit('/', 1)[-1]).split('[')[0]
        if x.startswith('file:') or norm(nm) in B.own:
            B.effects.append(eff('judge', why=f'remote install {x[:60]}'))
        else:
            B.effects.append(eff('others', pkg=norm(nm), why=f'named package {norm(nm)} from a URL'))
    for x in r['pkgs']:
        package(B, x, up or norm(B.L) in [norm(y) for y in r['upgrade_pkgs']], r['force'], r['eager'])


def package(B, spec, up, force, eager):
    """A package named on the command line (LH015's), with the brief's class 4 for an exact inline pin of L."""
    try:
        rq = Requirement(spec)
    except InvalidRequirement:
        m = re.match(r'^([A-Za-z0-9][A-Za-z0-9._-]*)(\[[^\]]*\])?(?=[=<>!~ ]|$)', spec)
        if not m:
            B.effects.append(eff('judge', why=f'unparsed package argument {spec[:60]}'))
            return
        nm = norm(m.group(1))
        if nm == norm(B.L):
            B.effects.append(eff('judge', why=f'L named with an unparsed specifier {spec[:60]}'))
        elif nm in B.own:
            B.effects.append(eff('index_own', pkg=nm, spec='', why=f'own package {nm} from the index (specifier not parsed)'))
        else:
            B.effects.append(eff('others', pkg=nm, why=f'named package {nm}'))
        return
    nm = norm(rq.name)
    if nm in ('poetry', 'pipenv', 'pdm', 'uv', 'pip', 'setuptools', 'wheel', 'pip-tools', 'tox', 'nox', 'hatch'):
        B.tool_specs[nm] = str(rq.specifier)
    if nm == norm(B.L):
        sp = rq.specifier
        vs = [v for v in B.pinned if V(v)]
        admits_pin = any(sp.contains(v, prereleases=True) for v in vs) if vs else True
        exact = [s for s in sp if s.operator in ('==', '===') and '*' not in s.version]
        if exact:
            B.effects.append(eff('other_pin', files=[], version=[exact[0].version], inline=True,
                                 overrides=not admits_pin or force, why=f'L pinned inline {sp}'))
            return
        B.effects.append(eff('fresh', sub='upgrade' if up else 'inline', names_L=True, spec=str(sp) or 'any',
                             overrides=up or force or not admits_pin, why=f'L inline {sp}'))
    elif nm in B.own:
        B.effects.append(eff('index_own', pkg=nm, spec=str(rq.specifier), why=f'own package {nm} from the index',
                             overrides=eager))
    else:
        B.effects.append(eff('others', pkg=nm, why=f'named package {nm}', eager=eager))


def req_file(B, st, f, up, force, constraint, level=0, base=None):
    if UNK in f or '$' in f:
        return eff('und', why='build argument', detail=f)
    if f.startswith(('http://', 'https://')):
        return eff('judge', why=f'requirements from a URL {f[:60]}')
    st2 = st
    if base is not None:
        st2 = State.__new__(State)
        st2.__dict__.update(st.__dict__)
        st2.cwd = base
    r = resolve(B, st2, f)
    k, v = r
    if k == 'gen':
        return eff('neutral', why='installs a file generated in the job', gen=v)
    if k == 'artefact':
        return eff('und', why='external', detail=f'{f} from a downloaded artefact')
    if k == 'unknown':
        return eff('und', why='build argument', detail=v)
    if k == 'nocheckout':
        return eff('und', why='would not run', detail=f'{f} without a checkout')
    if k == 'outside':
        return eff('und', why='external', detail=f'{f} outside the repository')
    if k == 'missing':
        return eff('und', why='would not run', detail=f'{v} absent at the snapshot')
    rp = v
    if rp in B.T:
        return eff('T', files=[rp], why=f'{"-c" if constraint else "-r"} {rp}')
    lines = B.tree.lines(rp)
    if lines is None:
        return eff('und', why='unreadable', detail=rp)
    subs = []
    if level < 2:
        for how, inc in includes(lines):
            subs.append(req_file(B, st, inc, up, force, how == 'c', level + 1, base=posixpath.dirname(J(st2.prefix, rp))))
    for e in subs:
        if e['kind'] == 'T':
            return eff('T', files=[rp] + e['files'], why=f'{rp} includes {e["files"][-1]}')
    for e in subs:
        if e['kind'] in ('und', 'judge'):
            return e
    text = '\n'.join(lines)
    hold, vers = versions_in(rp, text, B.L, 'requirements')
    named = names_lib(text, B.L) or any(e.get('names_L') for e in subs)
    spec = spec_of(lines, B.L) + [s for e in subs for s in (e.get('spec_list') or [])]
    if hold:
        if kind_of(rp) is None:
            return eff('judge', why=f'pin of L in {rp}, a file LH008 would not read by name', files=[rp], version=vers)
        return eff('other_pin', files=[rp], version=vers, why=f'{rp} {hold} {",".join(vers)}',
                   overrides=not set(vers) & set(B.pinned))
    for e in subs:
        if e['kind'] == 'other_pin':
            return e
    if not constraint:
        for x in req_paths(lines):
            project(B, st, x, {'no_deps': False})
    return eff('fresh', sub='upgrade' if (up and named) else 'other file', names_L=named, spec='; '.join(spec) or None,
               spec_list=spec, files=[rp], overrides=named and (up or force), why=f'{rp}')


def project(B, st, x, r):
    """Installing a local project (a directory, or a wheel or sdist built from one)."""
    x0 = re.sub(r'\[[^\]]*\]$', '', x)
    if UNK in x0 or '$' in x0:
        B.effects.append(eff('und', why='build argument', detail=x))
        return
    w = ws_path(st, x0)
    if w == UNK:
        B.effects.append(eff('und', why='build argument', detail=f'{x} in a directory not substituted'))
        return
    if w is None:
        nm = norm(re.split(r'[-_]\d', posixpath.basename(x0.rstrip('/')))[0]) if x0 else ''
        if nm in B.own:
            B.effects.append(eff('judge', why=f'own project from outside the repository {x0[:60]}'))
        else:
            B.effects.append(eff('others', pkg=nm, why=f'package from outside the repository {x0[:60]}'))
        return
    if re.search(r'\.(whl|tar\.gz|zip|tgz)$', x0) or '*' in x0:
        d = posixpath.dirname(w)
        for g, pdir in st.wheels.items():
            if d == g or d.startswith(g + '/'):
                return project(B, repo_state(B, st), WS + '/' + J(pdir[len(st.prefix):].lstrip('/') if st.prefix and
                                                                 pdir.startswith(st.prefix) else pdir) if pdir else WS, r)
        for a, projs in st.artefacts.items():
            if d == a or d.startswith(a + '/') or a == '':
                if len(set(projs)) == 1:
                    return project(B, repo_state(B, st), WS + ('/' + projs[0] if projs[0] else ''), r)
                B.effects.append(eff('judge', why=f'wheel {x0} from a downloaded artefact' +
                                     (f' built from {len(set(projs))} projects' if projs else '')))
                return
        B.effects.append(eff('judge', why=f'wheel {x0} of unknown origin'))
        return
    k, v = resolve(B, st, x0)
    if k == 'nocheckout':
        B.effects.append(eff('und', why='would not run', detail=f'{x} without a checkout'))
        return
    if k in ('outside', 'unknown'):
        B.effects.append(eff('und', why='external' if k == 'outside' else 'build argument', detail=x))
        return
    if k == 'artefact':
        B.effects.append(eff('judge', why=f'project {x} from a downloaded artefact'))
        return
    if k == 'missing':
        B.effects.append(eff('und', why='would not run', detail=f'{x} absent at the snapshot'))
        return
    base = v if k == 'repo' else None
    if base is None:
        B.effects.append(eff('judge', why=f'project {x} generated in the job'))
        return
    mans = [J(base, m) for m in ('pyproject.toml', 'setup.py', 'setup.cfg') if B.tree.exists(J(base, m))]
    if not mans:
        B.effects.append(eff('judge', why=f'no manifest found for {x} at {base or "the root"}'))
        return
    if any(m in B.T for m in mans):
        B.effects.append(eff('T', files=[m for m in mans if m in B.T], why=f'project {x} with manifest in T'))
        return
    lines = []
    for m in mans:
        ls = B.tree.lines(m)
        if ls is None:
            B.effects.append(eff('und', why='unreadable', detail=m))
            return
        lines += ls
    text = '\n'.join(lines)
    reads = sorted(t for t in B.T if posixpath.basename(t) in text and posixpath.dirname(t).startswith(posixpath.dirname(mans[0])))
    if reads:
        how = bool(re.search(r'open\(|read_text|readlines|parse_req|\.read\(|file\s*=|file:|requirements_txt|-r ', text))
        B.effects.append(eff('judge', why=f'manifest names T file {posixpath.basename(reads[0])} (read pattern '
                                          f'{"yes" if how else "no"})', files=mans))
        return
    if not r.get('no_deps'):
        for m in mans:
            hold, vers = versions_in(m, '\n'.join(B.tree.lines(m) or []), B.L, 'manifest')
            if hold:
                B.effects.append(eff('other_pin', files=[m], version=vers, overrides=not set(vers) & set(B.pinned),
                                     why=f'project {x}: {m} pins L {",".join(vers)}'))
                return
    named = names_lib(text, B.L)
    B.effects.append(eff('fresh', sub='other file', names_L=named and not r.get('no_deps'), spec_list=spec_of(lines, B.L),
                         files=mans, why=f'project {x} ({",".join(posixpath.basename(m) for m in mans)} not in T)'))


def repo_state(B, st):
    """A state that reads the repository at the snapshot from its root: the manifest a wheel or sdist was built from."""
    st2 = State.__new__(State)
    st2.__dict__.update(st.__dict__)
    st2.avail, st2.prefix, st2.cwd, st2.artefacts, st2.gen = True, '', '', {}, {}
    return st2


def nearest_project(B, st, start, marker='pyproject.toml'):
    """The directory of the nearest `marker` at or above the workspace directory `start`, as a repository path."""
    k, v = resolve(B, st, WS + ('/' + start if start else ''))
    if k not in ('repo', 'missing'):
        return None
    d = v
    while True:
        if B.tree.exists(J(d, marker)):
            return d
        if d == '':
            return None
        d = posixpath.dirname(d)


def uv_workspace_root(B, d):
    """The uv workspace root of a project directory, if its pyproject.toml is a member of one (nearest ancestor with
    [tool.uv.workspace])."""
    p = posixpath.dirname(d) if d else None
    while p is not None:
        f = J(p, 'pyproject.toml')
        if B.tree.exists(f):
            ls = B.tree.lines(f) or []
            if any(re.match(r'^\s*\[tool\.uv\.workspace\]', t) for t in ls):
                return p
        if p == '':
            break
        p = posixpath.dirname(p)
    return None


def lock_step(B, st, proj, lockname, frozen, up, reader, relock=False, out=None, requires_lock=False):
    """A lock-reading command at the repository directory proj (LH015's rule, with the CI checkout)."""
    if proj is None:
        B.effects.append(eff('judge', why=f'{reader} without a project found'))
        return
    if not st.avail:
        B.effects.append(eff('und', why='would not run', detail=f'{reader} without a checkout'))
        return
    lock = J(proj, lockname)
    man_name = 'Pipfile' if lockname == 'Pipfile.lock' else 'pyproject.toml'
    man = J(proj, man_name)
    man_ok = B.tree.exists(man)
    man_T = man_ok and man in B.T
    if out:
        st.gen[J(st.cwd, out) if out != '__stdin__' else '__stdin__'] = len(B.effects)
    if B.tree.exists(lock):
        if lock not in B.T:
            ls = B.tree.lines(lock)
            if ls is None:
                B.effects.append(eff('und', why='unreadable', detail=lock))
                return
            hold, vers = versions_in(lock, '\n'.join(ls), B.L, 'lockfile')
            if hold:
                B.effects.append(eff('other_pin', files=[lock], version=vers, why=f'{reader} lock {lock} not in T locks L',
                                     overrides=not set(vers) & set(B.pinned)))
            else:
                B.effects.append(eff('fresh', sub='other file', names_L=False, files=[lock], overrides=True,
                                     why=f'{reader} lock {lock} not in T, without L'))
            return
        if up:
            B.effects.append(eff('T', files=[man], why=f'{reader} upgrade, pinned in T manifest') if man_T else
                             eff('fresh', sub='upgrade', names_L=None, overrides=True, why=f'{reader} re-resolves'))
        else:
            B.effects.append(eff('T', files=[lock], may_relock=relock and not frozen, why=f'{reader} with lock {lock}'))
        return
    if frozen or requires_lock:
        B.effects.append(eff('und', why='would not run', detail=f'{reader} requires {lockname}, absent at {proj or "the root"}'))
        return
    if not man_ok:
        B.effects.append(eff('judge', why=f'{reader} without {lockname} or manifest at {proj or "the root"}'))
        return
    if man_T:
        B.effects.append(eff('T', files=[man], why=f'{reader} without lock; manifest in T'))
        return
    ls = B.tree.lines(man)
    if ls is None:
        B.effects.append(eff('und', why='unreadable', detail=man))
        return
    hold, vers = versions_in(man, '\n'.join(ls), B.L, 'manifest')
    if hold:
        B.effects.append(eff('other_pin', files=[man], version=vers, overrides=not set(vers) & set(B.pinned),
                             why=f'{reader} without the lock: {man} pins L {",".join(vers)}'))
        return
    has_T_lock = any(B.T_kind.get(t) == 'lockfile' for t in B.T)
    B.effects.append(eff('fresh', sub='lock absent' if has_T_lock else 'other file', names_L=names_lib('\n'.join(ls), B.L),
                         spec_list=spec_of(ls, B.L), files=[man], overrides=True,
                         why=f'{reader} without the lock resolves {man}'))


UV_VALUED = PIP_VALUED | {'--out-dir', '--cache-dir', '--config-file', '--color', '--allow-insecure-host', '--native-tls', '--env-file',
                          '--only-group', '--no-group', '--extra', '--group', '--package', '--python', '-p', '--with',
                          '--with-requirements', '--with-editable', '--script', '--no-install-package', '--prune', '--format',
                          '--all-groups'}


def uv(B, st, a, env, origin):
    subs, flags, vals, pos = sub_and_flags(a, UV_VALUED)
    s = subs[0] if subs else ''
    start = st.cwd
    for k in ('--directory', '--project'):
        for v in vals.get(k, []):
            w = ws_path(st, v)
            if w in (None, UNK):
                B.effects.append(eff('und', why='build argument', detail=f'uv {k} {v}'))
                return
            start = w
    frozen = '--frozen' in flags or '--locked' in flags or truthy(env.get('UV_FROZEN')) or truthy(env.get('UV_LOCKED'))
    ups = [norm(x) for x in vals.get('--upgrade-package', []) + vals.get('-P', [])]
    up = '--upgrade' in flags or '-U' in flags or norm(B.L) in ups
    if s == 'pip':
        s2 = subs[1] if len(subs) > 1 else ''
        if s2 == 'install':
            return pip_like(B, st, pip_args(a[a.index('install') + 1:]), env, 'uv', 'install')
        if s2 in ('sync', 'compile'):
            return compile_or_sync(B, st, 'pip-sync' if s2 == 'sync' else 'pip-compile', a[a.index(s2) + 1:], env)
        return
    if s == 'tool' and subs[1:2] == ['install']:
        return pip_like(B, st, pip_args(pos), env, 'uv', 'install')
    if s == 'tool' and subs[1:2] == ['run']:
        return tool_run(B, st, a[a.index('run') + 1:], env, origin)
    if s in ('sync', 'run', 'export', 'lock'):
        if s == 'run' and ('--no-sync' in flags or truthy(env.get('UV_NO_SYNC')) or '--no-project' in flags or
                           '--script' in vals or '--isolated' in flags or truthy(env.get('UV_NO_PROJECT'))):
            if s == 'run' and pos[:1] and pos[0] in ('tox', 'nox', 'hatch', 'pip', 'poetry', 'pre-commit'):
                return installer(B, st, {'fam': pos[0], 'args': pos[1:], 'env': {}, 'argv0': pos[0]}, origin)
            return
        if s == 'run' and pos[:1] and pos[0].endswith('.py') and not pos[0].startswith('-'):
            B.flags.add('uv run of a .py file')
        if s == 'lock' and ('--check' in flags or '--check-exists' in flags):
            return
        proj = nearest_project(B, st, start)
        if proj is not None:
            root = uv_workspace_root(B, proj)
            if root is not None:
                proj = root
        out = (vals.get('-o') or vals.get('--output-file') or [None])[0] if s == 'export' else None
        if s == 'export' and not out and env.get('__out'):
            out = env['__out']
        lock_step(B, st, proj, 'uv.lock', frozen, up, f'uv {s}', relock=True, out=out)
        if s == 'run' and pos[:1] and pos[0] in ('tox', 'nox', 'hatch', 'pip', 'poetry', 'pre-commit'):
            installer(B, st, {'fam': pos[0], 'args': pos[1:], 'env': {}, 'argv0': pos[0]}, origin)
        return
    if s in ('add', 'remove'):
        B.effects.append(eff('judge', why=f'uv {s}'))
    if s == 'build':
        w = st.cwd
        st.wheels[J(w, (vals.get('-o') or vals.get('--out-dir') or ['dist'])[0])] = w


def compile_or_sync(B, st, fam, a, env):
    r = pip_args(a)
    files = r['paths'] + r['pkgs']
    up = r['upgrade'] or bool(r['upgrade_pkgs']) or '-U' in a or '--upgrade' in a
    if fam == 'pip-sync':
        for f in files or ['requirements.txt']:
            e = req_file(B, st, f, False, False, False)
            if e['kind'] in ('fresh', 'other_pin'):
                e['overrides'] = True
            B.effects.append(e)
        return
    out = r['out'] or (os.path.splitext(files[0])[0] + '.txt' if files and files[0].endswith('.in') else 'requirements.txt')
    rr = resolve(B, st, out)
    st.gen[J(st.cwd, out)] = len(B.effects)
    if rr[0] == 'repo' and rr[1] in B.T and not up:
        B.effects.append(eff('T', files=[rr[1]], why=f'{fam} keeps the pins of {rr[1]}'))
        return
    ins = [req_file(B, st, f, False, False, False) for f in files if not f.endswith('.toml')]
    named = any(e.get('names_L') for e in ins)
    B.effects.append(eff('fresh', sub='upgrade' if up else 'other file', names_L=named, overrides=True,
                         spec_list=[s for e in ins for s in (e.get('spec_list') or [])], why=f'{fam} resolves afresh'))


POETRY_VALUED = {'-C', '--directory', '-P', '--project', '--only', '--with', '--without', '-E', '--extras', '-o', '--output', '-f',
                 '--format', '--lock'}


def poetry(B, st, a, env, origin):
    subs, flags, vals, pos = sub_and_flags(a, POETRY_VALUED)
    s = subs[0] if subs else ''
    start = st.cwd
    for k in ('-C', '--directory', '-P', '--project'):
        for v in vals.get(k, []):
            w = ws_path(st, v)
            if w in (None, UNK):
                B.effects.append(eff('und', why='build argument', detail=f'poetry {k} {v}'))
                return
            start = w
    proj = nearest_project(B, st, start)
    if AMEND2 and s in ('add', 'update', 'remove') and ('--lock' in flags or '--lock' in vals):
        if s == 'update' or s == 'add':
            st.relocked.add(proj)
        B.notes.append(f'poetry {s} --lock updates the lock without installing')
        return
    if s in ('install', 'sync', 'export'):
        out = (vals.get('-o') or vals.get('--output') or [None])[0] if s == 'export' else None
        if s == 'export' and not out and env.get('__out'):
            out = env['__out']
        if AMEND2 and proj in st.relocked:
            B.effects.append(eff('fresh', sub='upgrade', names_L=None, overrides=True,
                                 why=f'poetry {s} reads a lock re-resolved earlier in the job'))
            return
        return lock_step(B, st, proj, 'poetry.lock', False, False, f'poetry {s}', out=out)
    if s == 'lock':
        spec = B.tool_specs.get('poetry', '') + ' ' + env.get('POETRY_VERSION', '')
        if re.search(r'(^|[=<~ ])1\.', spec) or '<2' in spec:
            B.effects.append(eff('judge', why='poetry lock with Poetry older than 2 (installer version)'))
            return
        if '--regenerate' in flags:
            return lock_step(B, st, proj, 'poetry.lock', False, True, 'poetry lock --regenerate')
        return lock_step(B, st, proj, 'poetry.lock', False, False, 'poetry lock', relock=True)
    if s == 'update':
        return lock_step(B, st, proj, 'poetry.lock', False, True, 'poetry update')
    if s in ('add', 'remove'):
        B.effects.append(eff('judge', why=f'poetry {s}'))
    if s == 'run' and pos[:1] and pos[0] in ('pip', 'pip3', 'tox', 'nox', 'python', 'python3'):
        return step_command(B, st, pos, origin)
    if s == 'build':
        st.wheels[J(start, 'dist')] = start


def pipenv(B, st, a, env):
    subs, flags, vals, pos = sub_and_flags(a, {'--python', '--pypi-mirror', '--categories'})
    s = subs[0] if subs else ''
    start = st.cwd
    if env.get('PIPENV_PIPFILE'):
        w = ws_path(st, env['PIPENV_PIPFILE'])
        if w in (None, UNK):
            B.effects.append(eff('und', why='build argument', detail='PIPENV_PIPFILE'))
            return
        start = posixpath.dirname(w)
    proj = nearest_project(B, st, start, 'Pipfile')
    if s == 'sync' or (s == 'install' and '--deploy' in flags and not pos):
        return lock_step(B, st, proj, 'Pipfile.lock', True, False, f'pipenv {s}')
    if s == 'requirements':
        return lock_step(B, st, proj, 'Pipfile.lock', True, False, 'pipenv requirements', out=env.get('__out'))
    if s == 'install' and not pos:
        old = re.search(r'(==|<=?)\s*20(1\d|2[0-3])\.', B.tool_specs.get('pipenv', ''))
        if old:
            return lock_step(B, st, proj, 'Pipfile.lock', False, True, 'pipenv install (Pipenv before 2024)')
        return lock_step(B, st, proj, 'Pipfile.lock', False, False, 'pipenv install', relock=True)
    if s in ('install', 'update', 'lock', 'upgrade'):
        B.effects.append(eff('judge', why=f'pipenv {s} {" ".join(pos)[:40]}'))


def pdm(B, st, a, env, origin):
    subs, flags, vals, pos = sub_and_flags(a, {'-p', '--project', '-G', '--group', '-o', '--output', '-L', '--lockfile'})
    s = subs[0] if subs else ''
    start = st.cwd
    for v in vals.get('-p', []) + vals.get('--project', []):
        w = ws_path(st, v)
        if w in (None, UNK):
            B.effects.append(eff('und', why='build argument', detail=f'pdm -p {v}'))
            return
        start = w
    proj = nearest_project(B, st, start)
    if s in ('install', 'sync', 'export'):
        out = (vals.get('-o') or vals.get('--output') or [None])[0] if s == 'export' else None
        return lock_step(B, st, proj, 'pdm.lock', '--frozen-lockfile' in flags, False, f'pdm {s}',
                         requires_lock=(s == 'sync'), out=out, relock=(s == 'install' and '--frozen-lockfile' not in flags))
    if s == 'update':
        return lock_step(B, st, proj, 'pdm.lock', False, True, 'pdm update')
    if s in ('add', 'remove', 'lock'):
        B.effects.append(eff('judge', why=f'pdm {s}'))
    if s == 'build':
        st.wheels[J(start, 'dist')] = start


def env_file(B, st, f):
    """A conda environment file: its pip section read as pip requirements; a conda-level L is judged."""
    k, v = resolve(B, st, f)
    if k != 'repo':
        B.effects.append(eff('und', why={'unknown': 'build argument', 'nocheckout': 'would not run', 'missing': 'would not run'}
                             .get(k, 'external'), detail=f'environment file {f} ({k})'))
        return
    ls = B.tree.lines(v)
    if ls is None:
        B.effects.append(eff('und', why='unreadable', detail=v))
        return
    if v in B.T:
        B.effects.append(eff('T', files=[v], why=f'environment file {v} in T'))
        return
    pip_items, conda_L = [], False
    in_pip = False
    for t in ls:
        m = re.match(r'^(\s*)-\s*pip\s*:\s*$', t)
        if m:
            in_pip = True
            continue
        m = re.match(r'^\s*-\s*(.+?)\s*$', t)
        if not m:
            continue
        item = m.group(1).strip('"\'')
        if in_pip and re.match(r'^\s{4,}-', t):
            pip_items.append(item)
        else:
            in_pip = False
            if re.match(r'^' + lib_re(B.L) + r'([=<>!~ ]|$)', item, re.I):
                conda_L = True
    if conda_L:
        B.effects.append(eff('judge', why=f'conda-level L in {v}'))
    st2 = State.__new__(State)
    st2.__dict__.update(st.__dict__)
    st2.cwd = posixpath.dirname(J(st.prefix, v))
    args = []
    for it in pip_items:
        args += shlex.split(it) if it.startswith('-') else [it]
    if args:
        pip_like(B, st2, pip_args(args), st.env, 'conda-pip', 'install')
    elif not conda_L:
        B.effects.append(eff('others', why=f'conda environment {v}'))


# ---------------------------------------------------------------- scripts, make, just, tox, nox, hatch (one level)

NOT_SHELL = re.compile(r'(?i)\.(py|pyz|pyw|js|mjs|ts|rb|pl|go|jar|exe|ps1|bat|cmd|R|jl|php|lua|json|toml|ya?ml|txt|md|css|html?)$')


def call_script(B, st, p, origin):
    """A shell script in the repository, read one level (brief, "Install step" (c)). A path that is not a repository
    file at the snapshot (made or downloaded in the job, or outside the workspace) is not a repository script; a Python
    or other non-shell program is not read (a limit); an environment file sourced sets variables only."""
    path = p['script']
    base = posixpath.basename(path)
    if NOT_SHELL.search(base) or (p['fam'] == 'source' and re.search(r'(?i)(^|[./])env([._-]|$)|\.env', base)):
        return
    k, v = resolve(B, st, path)
    if k == 'missing':
        B.notes.append(f'called {path}, not a repository file at the snapshot')
        return
    if k == 'outside':
        if re.search(r'(?i)install|setup|deps|requirement|bootstrap', base):
            B.effects.append(eff('und', why='script not read', detail=f'script {path} outside the repository'))
        return
    if k != 'repo':
        B.effects.append(eff('und', why='script not read' if k == 'unknown' else 'would not run', detail=f'script {path} ({k})'))
        return
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail=f'{path} called at depth {st.depth + 1}'))
        return
    data = B.tree.struct('script', v, '')
    if data is None:
        B.effects.append(eff('und', why='unreadable', detail=v))
        return
    text = '\n'.join(data.get('lines', []))
    if AMEND1:
        text = script_dirs(text, v, st)
    st.depth += 1
    try:
        run_text(B, st, text, f'script {v}')
    finally:
        st.depth -= 1


def script_dirs(text, path, st):
    """Amendment 1: the script-directory idioms a shell resolves from the script's own path, as literal paths."""
    here = WS + '/' + J(st.prefix, posixpath.dirname(path)) if posixpath.dirname(path) else WS + ('/' + st.prefix if st.prefix else '')
    here = here.rstrip('/')
    zero = r'(?:"?\$0"?|"?\$\{0\}"?|"?\$\{BASH_SOURCE(?:\[0\])?\}"?|"?\$BASH_SOURCE"?)'
    dn = r'\$\(\s*dirname\s+' + zero + r'\s*\)'
    text = re.sub(r'\$\(\s*cd\s+"?' + dn + r'"?(/\.\.)?"?\s*(?:>\s*/dev/null\s*(?:2>&1)?\s*)?&&\s*pwd(?:\s+-P)?\s*\)',
                  lambda m: posixpath.dirname(here) if m.group(1) else here, text)
    text = re.sub(dn, here, text)
    text = re.sub(r'\$\{0%/\*\}', here, text)
    text = re.sub(r'\$\(\s*git\s+rev-parse\s+--show-toplevel\s*\)', WS + ('/' + st.prefix if st.prefix else ''), text)
    return text


def make_call(B, st, p, origin):
    a = p['args']
    d = st.cwd
    subs = [x for x in a if not x.startswith('-') and '=' not in x]
    if '-C' in a and a.index('-C') + 1 < len(a):
        w = ws_path(st, a[a.index('-C') + 1])
        if w in (None, UNK):
            B.effects.append(eff('und', why='build argument', detail='make -C'))
            return
        d = w
        subs = [x for x in subs if x != a[a.index('-C') + 1]]
    f = a[a.index('-f') + 1] if '-f' in a and a.index('-f') + 1 < len(a) else None
    if f:
        subs = [x for x in subs if x != f]
    st2 = State.__new__(State)
    st2.__dict__.update(st.__dict__)
    st2.cwd = d
    mk = None
    for x in ([f] if f else ['GNUmakefile', 'makefile', 'Makefile']):
        k, v = resolve(B, st2, x)
        if k == 'repo':
            mk = v
            break
        if k == 'outside':
            return
        if k in ('nocheckout', 'unknown'):
            B.effects.append(eff('und', why='would not run' if k == 'nocheckout' else 'build argument', detail=f'make ({k})'))
            return
    if mk is None:
        B.effects.append(eff('und', why='would not run', detail=f'no Makefile at {d or "the root"}'))
        return
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail='make called at depth 2'))
        return
    if any(UNK in x or '$' in x for x in subs):
        B.effects.append(eff('und', why='build argument', detail='make target ' + ' '.join(subs)[:60]))
        return
    data = B.tree.struct('make', mk, ' '.join(subs))
    if data is None:
        B.effects.append(eff('und', why='unreadable', detail=mk))
        return
    if data.get('error'):
        B.effects.append(eff('judge', why=f'make: {data["error"]} in {mk}'))
        return
    st.depth += 1
    old = st.cwd
    try:
        st.cwd = d
        for tgt in data.get('targets', []):
            for line in tgt.get('lines', []):
                st.cwd = d
                run_text(B, st, line, f'make {mk}:{tgt["name"]}')
    finally:
        st.depth -= 1
        st.cwd = old


def just_call(B, st, p, origin):
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail='just called at depth 2'))
        return
    subs = [x for x in p['args'] if not x.startswith('-')]
    jf = None
    for x in ('justfile', 'Justfile', '.justfile'):
        k, v = resolve(B, st, x)
        if k == 'repo':
            jf = v
            break
    if jf is None:
        B.effects.append(eff('und', why='would not run', detail='no justfile'))
        return
    data = B.tree.struct('just', jf, ' '.join(subs[:1]))
    if data is None or data.get('error'):
        B.effects.append(eff('judge', why=f'just: {(data or {}).get("error", "unreadable")} in {jf}'))
        return
    st.depth += 1
    old = st.cwd
    try:
        for tgt in data.get('targets', []):
            for line in tgt.get('lines', []):
                run_text(B, st, line, f'just {jf}:{tgt["name"]}')
    finally:
        st.depth -= 1
        st.cwd = old


def tox_call(B, st, a, origin):
    """tox: the environments named (else env_list) install deps, constraints and the project, or uv.lock with tox-uv's
    lock runner (T1, T2)."""
    envs, i, sel = [], 0, None
    subs = [x for x in a if not x.startswith('-')]
    while i < len(a):
        t = a[i]
        if t in ('-e', '--env') and i + 1 < len(a):
            envs += a[i + 1].split(',')
            i += 2
            continue
        if t.startswith('-e') and len(t) > 2 and not t.startswith('--'):
            envs += t[2:].split(',')
        if t.startswith('--env='):
            envs += t.split('=', 1)[1].split(',')
        if t in ('-m', '--labels', '-f', '--factors') and i + 1 < len(a):
            sel = t
        i += 1
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail='tox called at depth 2'))
        return
    if any(UNK in e or '$' in e for e in envs):
        B.effects.append(eff('und', why='build argument', detail='tox -e ' + ','.join(envs)))
        return
    if sel:
        B.effects.append(eff('judge', why=f'tox {sel} selection'))
        return
    k, v = resolve(B, st, '.')
    if k != 'repo':
        B.effects.append(eff('und', why='would not run' if k == 'nocheckout' else 'build argument', detail=f'tox ({k})'))
        return
    conf = B.tree.struct('tox', v, ','.join(envs) or 'ALL_DEFAULT')
    if conf is None:
        B.effects.append(eff('und', why='would not run', detail=f'no tox configuration at {v or "the root"}'))
        return
    if conf.get('error'):
        B.effects.append(eff('judge', why=f'tox: {conf["error"]}'))
        return
    st.depth += 1
    old = st.cwd
    try:
        root = conf.get('root', v)
        for e in conf.get('envs', []):
            st.cwd = J(st.prefix, root)
            for c in e.get('commands', []):
                st.cwd = J(st.prefix, root)
                if e.get('changedir'):
                    st.cwd = J(st.prefix, e['changedir'])
                run_text(B, st, c, f'tox {e["name"]}')
    finally:
        st.depth -= 1
        st.cwd = old


def nox_call(B, st, a, origin):
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail='nox called at depth 2'))
        return
    sessions, i, sel = [], 0, None
    nf = 'noxfile.py'
    while i < len(a):
        t = a[i]
        if t in ('-s', '--session', '--sessions', '-e') :
            j = i + 1
            while j < len(a) and not a[j].startswith('-'):
                sessions.append(a[j])
                j += 1
            i = j
            continue
        if t.startswith('--session=') or t.startswith('--sessions='):
            sessions += t.split('=', 1)[1].split(',')
        if t in ('-f', '--noxfile') and i + 1 < len(a):
            nf = a[i + 1]
            i += 2
            continue
        if t in ('-k', '--keywords', '-t', '--tags', '-p', '--python'):
            sel = t
        i += 1
    if any(UNK in s or '$' in s for s in sessions):
        B.effects.append(eff('und', why='build argument', detail='nox -s ' + ' '.join(sessions)))
        return
    if sel in ('-k', '--keywords', '-t', '--tags'):
        B.effects.append(eff('judge', why=f'nox {sel} selection'))
        return
    k, v = resolve(B, st, nf)
    if k != 'repo':
        B.effects.append(eff('und', why='would not run' if k in ('nocheckout', 'missing') else 'build argument',
                             detail=f'noxfile ({k})'))
        return
    conf = B.tree.struct('nox', v, ','.join(sessions) or 'DEFAULT')
    if conf is None:
        B.effects.append(eff('und', why='unreadable', detail=v))
        return
    if conf.get('error'):
        B.effects.append(eff('judge', why=f'nox: {conf["error"]}'))
        return
    st.depth += 1
    old = st.cwd
    try:
        for s in conf.get('sessions', []):
            for c in s.get('commands', []):
                st.cwd = J(st.prefix, posixpath.dirname(v))
                run_text(B, st, c, f'nox {s["name"]}')
            if s.get('unparsed'):
                B.effects.append(eff('judge', why=f'nox session {s["name"]}: {s["unparsed"][:80]}'))
    finally:
        st.depth -= 1
        st.cwd = old


def hatch_call(B, st, a, origin):
    if st.depth >= 1:
        B.effects.append(eff('und', why='script not read', detail='hatch called at depth 2'))
        return
    subs, flags, vals, pos = sub_and_flags(a, {'-e', '--env', '-p', '--project', '--python', '-py', '-i', '--include',
                                                '-x', '--exclude'})
    s = subs[0] if subs else ''
    env = (vals.get('-e') or vals.get('--env') or [None])[0]
    if s == 'build':
        st.wheels[J(st.cwd, 'dist')] = st.cwd
        return
    if s == 'fmt':
        B.effects.append(eff('others', why='hatch fmt'))
        return
    if s not in ('run', 'test', 'env', 'shell'):
        return
    if s == 'run' and pos:
        script = pos[0]
        if ':' in script:
            env = script.split(':', 1)[0]
    if s == 'test':
        env = 'hatch-test'
    if s == 'env':
        if subs[1:2] != ['create'] and not (pos[:1] == ['create']):
            return
        rest = [x for x in pos if x != 'create']
        env = rest[0] if rest else env
    if s == 'shell' and pos:
        env = pos[0]
    env = env or 'default'
    if UNK in env or '$' in env:
        B.effects.append(eff('und', why='build argument', detail=f'hatch environment {env}'))
        return
    proj = nearest_project(B, st, st.cwd)
    if proj is None:
        B.effects.append(eff('und', why='would not run', detail='hatch without a project'))
        return
    conf = B.tree.struct('hatch', proj, env)
    if conf is None or conf.get('error'):
        B.effects.append(eff('judge', why=f'hatch: {(conf or {}).get("error", "unreadable")}'))
        return
    st.depth += 1
    old = st.cwd
    try:
        for c in conf.get('commands', []):
            st.cwd = J(st.prefix, proj)
            run_text(B, st, c, f'hatch {env}')
    finally:
        st.depth -= 1
        st.cwd = old


# ---------------------------------------------------------------- actions (uses:)

NEUTRAL_NAMING = ('actions/setup-python', 'astral-sh/setup-uv', 'actions/cache', 'actions/upload-artifact',
                  'actions/download-artifact', 'dorny/paths-filter', 'tj-actions/changed-files', 'codecov/codecov-action',
                  'docker/', 'actions/setup-node', 'snok/install-poetry', 'abatilo/actions-poetry', 'pdm-project/setup-pdm',
                  'actions/checkout', 'github/codeql-action', 'pypa/gh-action-pypi-publish', 'actions/upload-pages-artifact',
                  'softprops/action-gh-release', 'actions/github-script', 'peaceiris/', 'coverallsapp/', 'SonarSource/',
                  'sonarsource/', 'actions/attest-build-provenance', 'sigstore/')
ENV_FILE_ACTIONS = ('conda-incubator/setup-miniconda', 'mamba-org/setup-micromamba', 'mamba-org/provision-with-micromamba')
JUDGE_ACTIONS = ('py-actions/py-dependency-install', 'fedora-python/tox-github-action', 'pypa/cibuildwheel')
REQLIKE = re.compile(r'(?i)(^|[\s/])(requirements[^/\s]*\.(txt|in)|constraints[^/\s]*\.txt|[^/\s]*\.lock|pyproject\.toml|setup\.py|'
                     r'setup\.cfg|Pipfile|environment[^/\s]*\.ya?ml)(\s|$)')
INSTALL_CMD = re.compile(r'\b(pip3?|uv|poetry|pipenv|pdm)\s+(install|sync)\b|\btox\b|\bnox\b|\bhatch\s+(run|test)\b')


def action_step(B, st, uses, with_):
    name = uses.split('@', 1)[0]
    lname = name.lower()
    if lname.startswith('actions/checkout'):
        repo_in = (with_.get('repository') or '').strip()
        if repo_in and UNK not in repo_in and repo_in.lower() != (B.tree.repo_slug or '').lower():
            return
        ref = (with_.get('ref') or '').strip()
        dflt = getattr(B.tree, 'default_branch', '') or ''
        if ref and UNK not in ref and not re.fullmatch(r'[0-9a-f]{40}', ref) and ref not in (dflt, 'refs/heads/' + dflt):
            B.effects.append(eff('judge', why=f'checkout of ref {ref[:40]}'))
        path = (with_.get('path') or '').strip()
        st.avail = True
        st.prefix = J(path) if path and UNK not in path else ('' if not path else UNK)
        if st.prefix == UNK:
            B.effects.append(eff('und', why='build argument', detail='checkout path'))
            st.prefix = ''
        return
    if lname.startswith('actions/download-artifact'):
        p = (with_.get('path') or '').strip()
        w = ws_path(st, p) if p else st.cwd
        if w not in (None, UNK):
            st.artefacts[w] = list(with_.get('__projects__') or [])
        return
    if lname.startswith(('docker/build-push-action', 'docker/bake-action')):
        B.effects.append(eff('container', why='container build'))
        return
    if lname.startswith('pre-commit/action') or lname.startswith('pre-commit-ci/'):
        B.effects.append(eff('others', why='pre-commit hooks'))
        return
    if lname.startswith(ENV_FILE_ACTIONS):
        ef = (with_.get('environment-file') or '').strip()
        if ef:
            env_file(B, st, ef)
        return
    if lname.startswith(('snok/install-poetry', 'abatilo/actions-poetry')):
        v = (with_.get('version') or with_.get('poetry-version') or '').strip()
        if v:
            B.tool_specs['poetry'] = '==' + v
        if norm(B.L) == 'poetry':
            package(B, 'poetry==' + v if v and re.match(r'^\d', v) else 'poetry', False, False, False)
        return
    if lname.startswith(JUDGE_ACTIONS):
        B.effects.append(eff('judge', why=f'action {name}'))
        return
    if lname.startswith(NEUTRAL_NAMING):
        return
    vals = ' '.join(str(v) for v in with_.values())
    if INSTALL_CMD.search(vals):
        B.effects.append(eff('judge', why=f'action {name} with an install command in its inputs'))
    elif REQLIKE.search(vals):
        B.effects.append(eff('judge', why=f'action {name} names a requirements file'))


def walk(B):
    st = State(B)
    for s in B.steps:
        o = s.get('origin', 'run')
        st.env.update(s.get('env') or {})
        if o == 'external-call':
            B.effects.append(eff('und', why='external', detail=f'reusable workflow {s.get("uses", "")[:80]}'))
            continue
        if o == 'nested-action':
            B.effects.append(eff('und', why='script not read', detail=f'local action {s.get("uses", "")} called at depth 2'))
            continue
        if o == 'unreadable':
            B.effects.append(eff('und', why='unreadable', detail=s.get('note', '')))
            continue
        if o == 'judge':
            B.effects.append(eff('judge', why=s.get('note', 'extraction')))
            continue
        if s.get('if'):
            B.flags.add('conditional step')
        if s.get('uses'):
            n0 = len(B.effects)
            action_step(B, st, s['uses'], s.get('with') or {})
            for e in B.effects[n0:]:
                e['cond'] = bool(s.get('if'))
            continue
        run = s.get('run')
        if run is None:
            continue
        wd = s.get('wd')
        st.cwd = ''
        if wd:
            w = ws_path(st, wd)
            st.cwd = w if w not in (None,) else UNK
        n0 = len(B.effects)
        st.dirstack = []
        run_text(B, st, run, o)
        for e in B.effects[n0:]:
            e['cond'] = bool(s.get('if'))
    return B.effects


SUB_ORDER = ['upgrade', 'lock absent', 'lock unused', 'other file', 'inline']


def decide(B, effects):
    """(class, sub-label, reason, flags) of one job (LH015's decide, with the brief's changes)."""
    E = [e for e in effects if e['kind'] not in ('neutral', 'container')]
    state, last_T, ov = None, -1, None
    for i, e in enumerate(E):
        k = e['kind']
        if k == 'T':
            state, last_T = 'T', i
        elif state == 'T' and e.get('overrides') and k in ('fresh', 'override', 'other_pin', 'index_own'):
            state, ov = ('other_pin' if k == 'other_pin' else 'overridden'), e
        elif k == 'other_pin' and state != 'T':
            state = 'other_pin'
    flags = sorted(B.flags)
    if state == 'T':
        t = E[last_T]
        late = [e for e in E[last_T + 1:] if e['kind'] in ('judge', 'und')]
        if late:
            flags.append('later step not read')
        if any(e.get('may_relock') for e in E if e['kind'] == 'T'):
            flags.append('may re-lock')
        if any(e.get('cond') for e in E if e['kind'] == 'T') and not any(not e.get('cond') for e in E if e['kind'] == 'T'):
            flags.append('class rests on a conditional step')
        return 1, '', t.get('why', ''), flags
    judges = [e for e in E if e['kind'] == 'judge']
    unds = [e for e in E if e['kind'] == 'und']
    if judges:
        return 'to judge', '', '; '.join(sorted({e['why'] for e in judges}))[:300], flags
    if unds:
        u = unds[0]
        return 6, u['why'], (u.get('detail') or '')[:200], flags
    if state == 'overridden':
        return 2, 'upgrade', ov.get('why', ''), flags
    if state == 'other_pin':
        e = next(e for e in E[::-1] if e['kind'] == 'other_pin')
        return 4, 'inline pin' if e.get('inline') else '', e.get('why', ''), flags
    own = [e for e in E if e['kind'] == 'index_own']
    if own:
        return 3, '', own[0]['why'], flags
    fresh = [e for e in E if e['kind'] in ('fresh', 'override')]
    if fresh:
        subs = {e.get('sub') for e in fresh}
        tlocks = [t for t in B.T if B.T_kind.get(t) == 'lockfile']
        if tlocks and not ({'upgrade', 'lock absent'} & subs) and any_checkout(B):
            subs.add('lock unused')
        sub = next(s for s in SUB_ORDER if s in subs)
        return 2, sub, '; '.join(sorted({e.get('why', '') for e in fresh}))[:300], flags
    if any(e['kind'] == 'container' for e in effects):
        return 5, 'container build only', '', flags
    if any(e['kind'] == 'others' for e in E):
        return 5, 'other named packages only', '', flags
    return 5, 'no Python install', '', flags


def any_checkout(B):
    return B.system == 'gitlab' or any((s.get('uses') or '').lower().startswith('actions/checkout') for s in B.steps)


def classify_job(B):
    effects = walk(B)
    c = decide(B, effects)
    named = [e for e in effects if e['kind'] in ('fresh', 'override')]
    Ts = [e for e in effects if e['kind'] == 'T']
    info = {
        'names_L': 'yes' if any(e.get('names_L') for e in named) else ('no' if named else ''),
        'spec': ' | '.join(sorted({s for e in named for s in (e.get('spec_list') or ([e['spec']] if e.get('spec') else []))})),
        'own_pkgs': ' '.join(sorted({e['pkg'] for e in effects if e['kind'] == 'index_own'})),
        'own_spec': ' '.join(sorted({e['pkg'] + e.get('spec', '') for e in effects if e['kind'] == 'index_own'})),
        'other_pin': ' '.join(sorted({v for e in effects if e['kind'] == 'other_pin' for v in e.get('version', [])})),
        'effects': ' || '.join(f"{e['kind']}:{e.get('sub') or ''}:{e.get('tool', '')}:{(e.get('why') or '')[:70]}:{(e.get('detail') or '')[:50]}"
                               for e in effects)[:900],
        'T_files': '|'.join(sorted({f for e in Ts for f in e.get('files', [])})) if c[0] == 1 else '',
        'T_tools': ' '.join(sorted({e.get('tool', '') for e in Ts})) if c[0] == 1 else '',
        'tools': ' '.join(sorted({e.get('tool', '') for e in effects if e['kind'] in ('T', 'fresh', 'other_pin', 'index_own')})),
        'container_build': 'yes' if any(e['kind'] == 'container' for e in effects) else 'no',
    }
    info['T_lock'] = 'yes' if c[0] == 1 and any(B.T_kind.get(f) == 'lockfile' for e in Ts for f in e.get('files', [])) else 'no'
    return c, info
