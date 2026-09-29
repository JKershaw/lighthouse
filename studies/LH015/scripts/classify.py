"""LH015: the class of each build of each recipe for a pair, by the brief's rules ("Classes of a recipe for a pair").

The parsing and resolution here are shared with collect.py, which runs them against the live tree and records every
existence query, pattern match and file read (data/tree_paths.csv, data/aux_lines.csv); this script replays those
records offline, so that its output depends only on stored inputs. It decides the literal cases and writes "to judge"
with the reason otherwise; data/judgements.csv (the writer's, an input) then supplies those classes.

python3 classify.py        writes data/recipe_classes.csv
"""
import collections
import copy
import json
import os
import posixpath
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401
from packaging.requirements import Requirement, InvalidRequirement  # noqa: E402
from packaging.specifiers import SpecifierSet, InvalidSpecifier  # noqa: E402

UNK = '⟨ARG:'   # a value that only a build command gives (an ARG with no default, or a template placeholder)


class Unrecorded(Exception):
    pass


# ================================================================ Dockerfile

def parse_dockerfile(text):
    """Instructions as dicts {n, op, rest}; continuation lines joined, comments dropped, heredoc bodies appended."""
    lines = text.replace('\r\n', '\n').split('\n')
    esc = '\\'
    for ln in lines[:5]:
        m = re.match(r'\s*#\s*escape\s*=\s*(\S)', ln, re.I)
        if m:
            esc = m.group(1)
    out, i, n = [], 0, len(lines)
    while i < n:
        raw, start = lines[i], i + 1
        i += 1
        if not raw.strip() or raw.strip().startswith('#'):
            continue
        buf = raw.rstrip()
        while buf.endswith(esc) and i < n:
            buf = buf[:-1].rstrip()
            while i < n and (not lines[i].strip() or lines[i].strip().startswith('#')):
                i += 1
            if i < n:
                buf += ' ' + lines[i].strip()
                i += 1
        m = re.match(r'\s*([A-Za-z]+)\s*(.*)', buf, re.S)
        if not m:
            continue
        op, rest = m.group(1).upper(), m.group(2).strip()
        if op in ('RUN', 'COPY', 'ADD'):
            for dash, q, word in re.findall(r'<<(-?)(["\']?)([A-Za-z_][A-Za-z0-9_]*)\2', rest):
                body = []
                while i < n:
                    l2 = lines[i]
                    i += 1
                    if l2.strip() == word:
                        break
                    body.append(l2)
                rest += '\n' + '\n'.join(body)
        out.append({'n': start, 'op': op, 'rest': rest})
    return out


def words(s):
    try:
        return shlex.split(s, posix=True)
    except ValueError:
        return s.split()


def parse_arg(rest):
    out = []
    for t in words(rest):
        k, _, v = t.partition('=')
        out.append((k, v if '=' in t else None))
    return out


def parse_env(rest):
    t = words(rest)
    if t and '=' not in t[0]:
        return [(t[0], rest.split(None, 1)[1].strip().strip('"\'') if len(rest.split(None, 1)) > 1 else '')]
    return [tuple(x.split('=', 1)) for x in t if '=' in x]


VAR = re.compile(r'\$(?:\{([A-Za-z_][A-Za-z0-9_]*)(?:(:?[-+])([^}]*))?\}|([A-Za-z_][A-Za-z0-9_]*))')


def subst(s, env):
    def rep(m):
        name, op, word = m.group(1) or m.group(4), m.group(2), m.group(3)
        if name not in env:
            return word if op in (':-', '-') else m.group(0)
        v = env[name]
        if op in (':+', '+'):
            return word if v else ''
        if op in (':-', '-') and (not v or v.startswith(UNK)):
            return word
        return v
    return VAR.sub(rep, s)


def template_marks(s):
    """Template placeholders ({{ x }}, {% %}, @x@) read as values only a build command gives."""
    return re.sub(r'\{\{[^}]*\}\}|\{%[^%]*%\}|@[A-Z_]+@', UNK + 'template⟩', s)


def stages_of(instrs, build_args=None):
    glob_args, stages = {}, []
    for ins in instrs:
        if ins['op'] == 'FROM':
            t = [x for x in words(subst(ins['rest'], {**glob_args, **(build_args or {})})) if not x.startswith('--')]
            name = t[2].lower() if len(t) >= 3 and t[1].lower() == 'as' else None
            stages.append({'idx': len(stages), 'name': name, 'base': (t[0] if t else '').lower(), 'ins': [], 'n': ins['n'],
                           'from_rest': ins['rest']})
        elif not stages:
            if ins['op'] == 'ARG':
                for k, v in parse_arg(ins['rest']):
                    glob_args[k] = (build_args or {}).get(k, v)
        else:
            stages[-1]['ins'].append(ins)
    for s in stages:
        s['base_stage'] = stage_ref(stages, s['base'], s['idx'])
    return glob_args, stages


def stage_ref(stages, ref, before):
    ref = (ref or '').lower()
    for s in stages[:before]:
        if s['name'] == ref or str(s['idx']) == ref:
            return s['idx']
    return None


def copy_parts(rest):
    flags, excl, body = {}, [], rest
    while True:
        m = re.match(r'--([a-z-]+)(?:=("[^"]*"|\S+))?\s*', body)
        if not m:
            break
        k, v = m.group(1), (m.group(2) or '').strip('"')
        if k == 'exclude':
            excl.append(v)
        else:
            flags[k] = v
        body = body[m.end():]
    body = body.split('\n', 1)[0].strip()
    if body.startswith('['):
        try:
            parts = json.loads(body)
        except ValueError:
            parts = words(body.strip('[]').replace(',', ' '))
    else:
        parts = words(body)
    return flags, excl, parts[:-1], (parts[-1] if len(parts) >= 2 else None)


def run_parts(rest):
    mounts, body = [], rest
    while True:
        m = re.match(r'--([a-z-]+)(?:=(\S+))?\s*', body)
        if not m:
            break
        if m.group(1) == 'mount':
            d = {}
            for kv in (m.group(2) or '').split(','):
                k, _, v = kv.partition('=')
                d[k.strip()] = v.strip().strip('"\'') if _ else 'true'
            mounts.append(d)
        body = body[m.end():]
    return mounts, body


def exec_text(rest):
    r = rest.strip()
    if r.startswith('['):
        try:
            return ' '.join(shlex.quote(x) for x in json.loads(r))
        except ValueError:
            pass
    return r


def final_path(stages, target):
    need, stack = {target}, [target]
    while stack:
        s = stages[stack.pop()]
        deps = [s['base_stage']] if s['base_stage'] is not None else []
        for ins in s['ins']:
            if ins['op'] in ('COPY', 'ADD'):
                f = copy_parts(ins['rest'])[0].get('from')
                if f is not None:
                    deps.append(stage_ref(stages, f, s['idx']))
            elif ins['op'] == 'RUN':
                for m in run_parts(ins['rest'])[0]:
                    if m.get('from'):
                        deps.append(stage_ref(stages, m['from'], s['idx']))
        for j in deps:
            if j is not None and j not in need:
                need.add(j)
                stack.append(j)
    return sorted(need)


# ================================================================ shell

KEYWORDS = {'if', 'then', 'else', 'elif', 'fi', 'do', 'done', 'while', 'until', 'for', 'case', 'esac', '!', '{', '}', 'in'}


def commands(s, depth=0):
    """Simple commands of a shell text as token lists; `sh -c '...'` is opened; redirections kept as '>' tokens."""
    out = []
    for line in s.split('\n'):
        try:
            lx = shlex.shlex(line, posix=True, punctuation_chars=True)
            lx.whitespace_split = True
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
        while c and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', c[0]):
            c = c[1:]
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
        elif b in ('sudo', 'exec', 'time', 'nice', 'nohup', 'command', 'eval', 'env', 'tini', 'dumb-init', 'catatonit'):
            pass
        elif b in ('timeout', 'chroot', 'gosu', 'su-exec'):
            i += 1
        elif t == '--' or (i > 0 and t.startswith('-') and posixpath.basename(c[i - 1]) in ('env', 'sudo', 'tini', 'dumb-init')):
            pass
        else:
            break
        i += 1
    return env, c[i:]


def redirect_out(c):
    """(command without redirections, output file or None)."""
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


DELEGATED = ('ansible-playbook', 'ansible-pull', 'salt-call', 'chef-solo', 'chef-client', 'puppet')
PYTHON = re.compile(r'^(python|pypy)(\d(\.\d+)?)?$')
TOOLS = ('uv', 'poetry', 'pipenv', 'pdm', 'pipx', 'conda', 'mamba', 'micromamba', 'pip-sync', 'pip-compile', 'easy_install',
         'make', 'gmake', 'just', 'task', 'invoke', 'inv', 'nox', 'tox', 'hatch', 'rye', 'pixi')


def parse_cmd(c):
    """{'fam', 'args', 'env', 'out'} for an installer, a build tool, a make target or a script call; None otherwise."""
    env, c = strip_prefix(c)
    c, out = redirect_out(c)
    if not c:
        return None
    b = posixpath.basename(c[0])
    r = {'env': env, 'out': out, 'args': c[1:], 'argv0': c[0]}
    if re.fullmatch(r'pip(\d(\.\d+)?)?', b):
        r['fam'] = 'pip'
    elif PYTHON.match(b):
        j = 1
        while j < len(c) and c[j].startswith('-') and c[j] != '-m' and c[j] != '-c':
            j += 1
        if j + 1 < len(c) and c[j] == '-m':
            mod = c[j + 1]
            r['args'] = c[j + 2:]
            fams = {'pip': 'pip', 'uv': 'uv', 'pipx': 'pipx', 'pipenv': 'pipenv', 'poetry': 'poetry', 'pdm': 'pdm', 'piptools': 'piptools',
                    'build': 'build', 'ensurepip': None, 'venv': None, 'virtualenv': None}
            if mod not in fams or fams[mod] is None:
                return None
            r['fam'] = fams[mod]
        elif j < len(c) and c[j].endswith('setup.py'):
            r['fam'], r['script'], r['args'] = 'setup.py', c[j], c[j + 1:]
        elif j < len(c) and c[j].endswith('.py') and not c[j].startswith('-'):
            r['fam'], r['script'], r['args'] = 'pyscript', c[j], c[j + 1:]
        elif j < len(c) and c[j] == '-':
            r['fam'] = 'stdin-python'
        else:
            return None
    elif b in DELEGATED:
        r['fam'] = 'delegated'
    elif b in TOOLS:
        r['fam'] = b
    elif b in ('sh', 'bash', 'dash', 'zsh', 'ash', 'source', '.'):
        a = [x for x in c[1:] if not x.startswith('-')]
        if not a:
            return None
        r['fam'], r['script'], r['args'] = ('source' if b in ('source', '.') else 'call'), a[0], a[1:]
    elif c[0].startswith(('./', '/', '../')) or b.endswith('.sh'):
        r['fam'], r['script'] = 'call', c[0]
    else:
        return None
    return r


def truthy(v):
    return (v or '').strip().lower() not in ('', '0', 'false', 'no', 'off')


def sub_and_flags(args, valued):
    """Subcommand words and flags of uv, poetry, pdm, pipenv or conda; valued flags take the next word."""
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
              '--with', '--from', '--cache', '--annotation-style', '--resolver', '--pip-args', '--extra-index', '-x'}


def pip_args(args):
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
        elif UNK in a and not re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]*(\[[^\]]*\])?\s*(==|>=|<=|~=|!=|<|>)', a):
            r['unk'].append(a)
        elif a in ('.', '..') or a.startswith(('.', '/', '~', '$')) or '/' in a.split('[')[0] or \
                re.search(r'\.(whl|tar\.gz|zip|tgz)$', a) or a.startswith('file:'):
            r['paths'].append(a[5:] if a.startswith('file:') else a)
        else:
            r['pkgs'].append(a)
        i += 1
    return r


# ================================================================ ignore files (Go filepath.Match, ** and ! exceptions)

def ig_patterns(lines):
    pats = []
    for t in lines or []:
        t = t.strip()
        if not t or t.startswith('#'):
            continue
        neg = t.startswith('!')
        if neg:
            t = t[1:].strip()
        t = posixpath.normpath(t.lstrip('/'))
        if t == '.':
            continue
        pats.append((neg, re.compile(glob_re(t))))
    return pats


def glob_re(p):
    out, i = '', 0
    while i < len(p):
        ch = p[i]
        if p.startswith('**', i):
            i += 2
            if p.startswith('/', i):
                i += 1
                out += '(?:.*/)?'
            else:
                out += '.*'
            continue
        if ch == '*':
            out += '[^/]*'
        elif ch == '?':
            out += '[^/]'
        elif ch == '[':
            j = p.find(']', i + 1)
            if j < 0:
                out += re.escape(ch)
            else:
                cls = p[i + 1:j].replace('\\', '\\\\')
                out += '[' + ('^' + cls[1:] if cls.startswith('^') else cls) + ']'
                i = j
        elif ch == '\\' and i + 1 < len(p):
            i += 1
            out += re.escape(p[i])
        else:
            out += re.escape(ch)
        i += 1
    return '^' + out + '$'


def ig_excluded(rel, pats):
    """Whether a context-relative path is excluded: the last matching line decides; a line matches the path or a parent."""
    parts = rel.split('/')
    cands = ['/'.join(parts[:k]) for k in range(1, len(parts) + 1)]
    ex = False
    for neg, rx in pats:
        if any(rx.match(c) for c in cands):
            ex = not neg
    return ex


def J(*parts):
    ps = [p for p in parts if p not in ('', None, '.')]
    if not ps:
        return ''
    p = posixpath.normpath(posixpath.join(*ps))
    return '' if p == '.' else p


def cjoin(wd, p):
    return posixpath.normpath(posixpath.join(wd or '/', p))


def within(rp, ctx):
    return ctx == '' or rp == ctx or rp.startswith(ctx + '/')


# ================================================================ requirement facts

def spec_of(lines, lib):
    """PEP 508 specifiers of the library found in the lines (quoted strings, requirement lines, Poetry tables)."""
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


# ================================================================ the build walk

class Ctx:
    """One build: recipe instructions, target, context, ignore lines, the pair's T and L, and the tree."""

    def __init__(self, instrs, tree, ctx, ignore_lines, T, T_kind, L, pinned, own, target=None, build_args=None,
                 template=False, repo_libs=()):
        self.instrs, self.tree, self.ctx = instrs, tree, ctx
        self.pats = ig_patterns(ignore_lines)
        self.T, self.T_kind, self.L, self.pinned = set(T), T_kind, L, pinned
        self.own = {norm(x) for x in own if x}
        self.build_args = build_args or {}
        self.glob_args, self.stages = stages_of(instrs, self.build_args)
        self.target = target
        self.template = template
        self.effects, self.notes = [], []
        self.tool_specs = {}


def eff(kind, **kw):
    kw['kind'] = kind
    return kw


def resolve(B, st, cp, mounts=()):
    """Where the file or directory at container path cp comes from."""
    cp = posixpath.normpath(cp)
    for g, e in list(st['gen'].items())[::-1]:
        if cp == g or cp.startswith(g.rstrip('/') + '/'):
            return ('gen', e)
    for e in (list(st['map']) + list(mounts))[::-1]:
        d = e['dest']
        if e.get('kind') == 'file':
            if cp == d or cp == cjoin(d, posixpath.basename(e['src'])):
                return check(B, e['src'], e)
            continue
        if cp == d or d == '/' or cp.startswith(d.rstrip('/') + '/'):
            rest = cp[len(d):].lstrip('/') if d != '/' else cp.lstrip('/')
            if 'stage' in e:
                return via_stage(B, e, cp, rest)
            if 'ext' in e:
                return ('ext', e['ext'])
            if 'unknown' in e:
                return ('unknown', e['unknown'])
            rp = J(e['src'], rest)
            if B.tree.exists(rp):
                return check(B, rp, e)
    return None


def via_stage(B, e, cp, rest):
    """Follow a path copied from another stage into that stage's own files, as they stood at its end."""
    sst = getattr(B, 'end', {}).get(e['stage'])
    if sst is None or e.get('depth', 0) > 3:
        return ('stage', e['stage'])
    cands = []
    for s in e.get('srcs') or []:
        s = posixpath.normpath(s)
        if not e.get('dir_dest') and cp == e['dest']:
            cands.append(s)
        cands.append(cjoin('/', J(s, rest)))
        b = posixpath.basename(s)
        if rest == b or rest.startswith(b + '/'):
            cands.append(cjoin(posixpath.dirname(s) or '/', rest))
    for c in cands:
        r = resolve(B, sst, c)
        if r and r[0] in ('repo', 'gen'):
            return r
    return ('stage', e['stage'])


def check(B, rp, e):
    if not B.tree.exists(rp):
        return ('missing', rp)
    if not within(rp, B.ctx):
        return ('outside', rp)
    rel = rp[len(B.ctx):].lstrip('/') if B.ctx else rp
    if rel and ig_excluded(rel, B.pats):
        return ('excluded', rp)
    for x in e.get('excl', []):
        if rel and ig_excluded(rel, ig_patterns([x])):
            return ('excluded', rp)
    return ('repo', rp)


def in_context(B, rp):
    if not within(rp, B.ctx):
        return False
    rel = rp[len(B.ctx):].lstrip('/') if B.ctx else rp
    return not (rel and ig_excluded(rel, B.pats))


KNOWN_DIRS = {'/', '/tmp', '/opt', '/srv', '/root', '/home', '/usr', '/usr/local', '/usr/src', '/var', '/etc', '/bin',
              '/usr/local/bin', '/usr/bin'}


def do_copy(B, st, ins, sidx):
    flags, excl, srcs, dest = copy_parts(subst(ins['rest'], st['env']))
    if dest is None:
        return
    dabs = cjoin(st['wd'], dest)
    dir_dest = dest.endswith('/') or len(srcs) > 1 or any(re.search(r'[*?\[]', s) for s in srcs) or \
        dabs in st.setdefault('dirs', set()) | KNOWN_DIRS or dabs == st['wd']
    frm = flags.get('from')
    if frm is not None:
        j = stage_ref(B.stages, frm, sidx)
        if j is not None:
            st['map'].append({'dest': dabs, 'stage': j, 'srcs': srcs, 'dir_dest': dir_dest})
        else:
            st['map'].append({'dest': dabs, 'ext': frm})
            if any(re.search(r'site-packages|venv|wheel|/opt/conda|lib/python|\.local', s) for s in srcs + [dest]):
                B.effects.append(eff('judge', why=f'environment copied from image {frm}', n=ins['n']))
        return
    for s in srcs:
        if re.match(r'^[a-z]+://', s) or s.startswith('git@'):
            continue
        if UNK in s:
            st['map'].append({'dest': dabs, 'unknown': s})
            continue
        rel = posixpath.normpath(s.lstrip('/'))
        rel = '' if rel == '.' else rel
        if rel.startswith('..'):
            continue
        if re.search(r'[*?\[]', rel):
            for m in B.tree.glob(B.ctx, rel):
                st['map'].append({'dest': cjoin(dabs, posixpath.basename(m)), 'src': m, 'kind': 'file', 'excl': excl})
            continue
        rp = J(B.ctx, rel)
        if rel == '' or B.tree.isdir(rp):
            st['map'].append({'dest': dabs, 'src': rp, 'kind': 'dir', 'excl': excl})
        else:
            st['map'].append({'dest': cjoin(dabs, posixpath.basename(rel)) if dir_dest else dabs, 'src': rp, 'kind': 'file',
                              'excl': excl})


def walk(B):
    """Install effects of the build, in build order through the final path, then at start."""
    B.effects, B.notes = [], []
    if not B.stages:
        return [eff('und', why='would not build', detail='no FROM instruction')]
    tgt = len(B.stages) - 1 if B.target is None else stage_ref(B.stages, B.target, len(B.stages))
    if tgt is None:
        return [eff('und', why='other', detail=f'target {B.target} not found')]
    B.path = final_path(B.stages, tgt)
    end = {}
    B.end = end
    for i in B.path:
        s = B.stages[i]
        if s['base_stage'] is not None and s['base_stage'] in end:
            st = copy.deepcopy(end[s['base_stage']])
        else:
            st = {'env': {}, 'wd': '/', 'map': [], 'gen': {}, 'wheels': {}, 'entry': None, 'cmd': None}
        for ins in s['ins']:
            op = ins['op']
            if op == 'ARG':
                for k, v in parse_arg(ins['rest']):
                    if k in B.build_args:
                        st['env'][k] = B.build_args[k]
                    elif v is not None:
                        st['env'][k] = subst(v, st['env'])
                    elif B.glob_args.get(k) is not None:
                        st['env'][k] = B.glob_args[k]
                    else:
                        st['env'][k] = UNK + k + '⟩'
            elif op == 'ENV':
                for k, v in parse_env(subst(ins['rest'], st['env'])):
                    st['env'][k] = v
            elif op == 'WORKDIR':
                st['wd'] = cjoin(st['wd'], subst(ins['rest'], st['env']).strip().strip('"\''))
                st.setdefault('dirs', set()).add(st['wd'])
            elif op in ('COPY', 'ADD'):
                do_copy(B, st, ins, i)
            elif op == 'RUN':
                run_step(B, st, ins, i)
            elif op == 'ENTRYPOINT':
                st['entry'] = ins
            elif op == 'CMD':
                st['cmd'] = ins
        end[i] = st
        B.end = end
    fst = end[tgt]
    for ins in (fst['entry'], fst['cmd']):
        if ins:
            run_step(B, fst, ins, tgt, at_start=True)
    return B.effects


def run_step(B, st, ins, sidx, at_start=False):
    mounts = []
    if at_start:
        text = exec_text(ins['rest'])
    else:
        ms, text = run_parts(ins['rest'])
        if text.strip().startswith('['):
            text = exec_text(text)
        for m in ms:
            if m.get('type', 'bind') != 'bind':
                continue
            tgt = subst(m.get('target') or m.get('dst') or m.get('destination') or '', st['env'])
            if not tgt:
                continue
            dabs = cjoin(st['wd'], tgt)
            if m.get('from'):
                j = stage_ref(B.stages, m['from'], sidx)
                mounts.append({'dest': dabs, 'stage': j} if j is not None else {'dest': dabs, 'ext': m['from']})
                continue
            rel = posixpath.normpath(subst(m.get('source') or m.get('src') or '.', st['env']).lstrip('/'))
            rel = '' if rel == '.' else rel
            rp = J(B.ctx, rel)
            kind = 'dir' if rel == '' or B.tree.isdir(rp) else 'file'
            mounts.append({'dest': dabs, 'src': rp, 'kind': kind})
    text = subst(text, st['env'])
    if B.template:
        text = template_marks(text)
    shell(B, st, text, st['wd'], dict(st['env']), mounts, ins['n'], at_start, 0)


def shell(B, st, text, cwd, env, mounts, n, at_start, depth, script=None):
    for c in commands(text):
        pre, c2 = strip_prefix(c)
        if not c2:
            env.update(pre)
            continue
        b = posixpath.basename(c2[0])
        if b == 'cd':
            cwd = cjoin(cwd, c2[1] if len(c2) > 1 and c2[1] != '-' else '/root')
            continue
        if b in ('cp', 'mv') and len([t for t in c2[1:] if not t.startswith('-')]) == 2:
            src, dst = [t for t in c2[1:] if not t.startswith('-')]
            r = resolve(B, st, cjoin(cwd, src), mounts)
            if r and r[0] == 'repo':
                kind = 'dir' if B.tree.isdir(r[1]) else 'file'
                st['map'].append({'dest': cjoin(cwd, dst), 'src': r[1], 'kind': kind})
            elif r and r[0] == 'gen':
                st['gen'][cjoin(cwd, dst)] = r[1]
            elif r is None and UNK not in src:
                st['map'].append({'dest': cjoin(cwd, dst), 'ext': f'{src} (from outside the repository)'})
            continue
        if b == 'export':
            for t in c2[1:]:
                if '=' in t:
                    k, _, v = t.partition('=')
                    env[k] = v
            continue
        p = parse_cmd(c2)
        if p is None:
            continue
        p['env'] = {**env, **p['env']}
        before = len(B.effects)
        try:
            installer(B, st, p, cwd, mounts, n, at_start, depth)
        except Unrecorded as ex:
            B.effects.append(eff('judge', why=f'not recorded at collection: {ex}'))
        for e in B.effects[before:]:
            e.setdefault('n', n)
            e['at_start'] = at_start
            if script:
                e['via'] = script


def call_script(B, st, p, cwd, mounts, n, at_start, depth):
    s = p['script']
    name = posixpath.basename(s)
    looks = re.search(r'(?i)install|setup|deps|depend|requirement|bootstrap|build|venv|env|pip|poetry|uv|entry|start|run', name)
    if UNK in s:
        B.effects.append(eff('und', why='build argument', detail=s))
        return
    if depth >= 1:
        if looks:
            B.effects.append(eff('und', why='script not read', detail=f'{name} called at depth 2'))
        return
    r = resolve(B, st, cjoin(cwd, s), mounts)
    if not r or r[0] != 'repo':
        if looks and r and r[0] in ('stage', 'ext'):
            B.effects.append(eff('und', why='script not read', detail=f'{name} from {r[0]}'))
        else:
            B.notes.append(f'script {name} not in the repository ({r[0] if r else "not copied"})')
        return
    lines = B.tree.lines(r[1], 'script', B.L)
    if lines is None:
        B.effects.append(eff('und', why='unreadable', detail=r[1]))
        return
    text = '\n'.join(lines)
    if p['fam'] in ('make', 'gmake'):
        text = make_target(lines, p.get('target'))
    shell(B, st, text, cwd, dict(p['env']), mounts, n, at_start, depth + 1, script=r[1])


def make_target(lines, target):
    out, on, first = [], False, None
    for t in lines:
        m = re.match(r'^([A-Za-z0-9_.%/-]+)\s*:(?!=)', t)
        if m and not t.startswith('\t'):
            first = first or m.group(1)
            on = m.group(1) == (target or first)
            continue
        if on and t.startswith('\t'):
            out.append(t.strip().lstrip('@-'))
    return '\n'.join(out)


def installer(B, st, p, cwd, mounts, n, at_start, depth):
    fam, a, env = p['fam'], p['args'], dict(p['env'])
    if p.get('out'):
        env['__out'] = p['out']
    if fam == 'delegated':
        B.effects.append(eff('und', why='script not read', detail=f'install delegated to {posixpath.basename(p["argv0"])} (amendment 7)'))
        return
    if fam in ('call', 'source'):
        if fam == 'source' and re.search(r'activate$', p['script']):
            return
        return call_script(B, st, p, cwd, mounts, n, at_start, depth)
    if fam in ('make', 'gmake'):
        subs = [x for x in a if not x.startswith('-') and '=' not in x]
        d = cwd
        if '-C' in a and a.index('-C') + 1 < len(a):
            d = cjoin(cwd, a[a.index('-C') + 1])
            subs = [x for x in subs if x != a[a.index('-C') + 1]]
        f = a[a.index('-f') + 1] if '-f' in a and a.index('-f') + 1 < len(a) else None
        mk = f or next((x for x in ('Makefile', 'makefile', 'GNUmakefile') if resolve(B, st, cjoin(d, x), mounts)), 'Makefile')
        return call_script(B, st, {**p, 'script': cjoin(d, mk), 'target': subs[0] if subs else None}, cwd, mounts, n,
                           at_start, depth)
    if fam in ('just', 'task', 'invoke', 'inv', 'nox', 'tox', 'hatch', 'rye', 'pixi', 'easy_install', 'stdin-python'):
        if fam == 'stdin-python':
            return
        B.effects.append(eff('judge', why=f'{fam} task'))
        return
    if fam == 'pyscript':
        if re.search(r'(?i)install|requirement|deps|setup', posixpath.basename(p['script'])):
            B.effects.append(eff('judge', why=f'python script {posixpath.basename(p["script"])}'))
        return
    if fam == 'build':
        out = next((a[i + 1] for i, t in enumerate(a[:-1]) if t in ('--outdir', '-o')), None) or \
            next((t.split('=', 1)[1] for t in a if t.startswith('--outdir=')), None)
        src = next((t for t in a if not t.startswith('-') and t != out), '.')
        st['wheels'][cjoin(cwd, out or J(src, 'dist') or 'dist')] = cjoin(cwd, src)
        return
    if fam == 'setup.py':
        if a[:1] and a[0] in ('install', 'develop'):
            return project(B, st, posixpath.dirname(cjoin(cwd, p['script'])) or '/', cwd, mounts, {'no_deps': False})
        if a[:1] and a[0] in ('bdist_wheel', 'sdist', 'build'):
            st['wheels'][cjoin(cwd, 'dist')] = cwd
        return
    if fam == 'pip':
        sub = next((x for x in a if not x.startswith('-')), '')
        rest = a[a.index(sub) + 1:] if sub else []
        if sub in ('install', 'wheel', 'download'):
            return pip_like(B, st, pip_args(rest), cwd, env, mounts, 'pip', sub)
        return
    if fam == 'pipx':
        subs, flags, vals, pos = sub_and_flags(a, PIP_VALUED)
        if subs[:1] == ['install'] or subs[:1] == ['inject']:
            return pip_like(B, st, pip_args(pos[1:] if subs[:1] == ['inject'] else pos), cwd, env, mounts, 'pipx', 'install')
        return
    if fam == 'piptools':
        sub = a[0] if a else ''
        fam, a = ('pip-compile' if sub == 'compile' else 'pip-sync'), a[1:]
    if fam == 'uv':
        return uv(B, st, a, cwd, env, mounts)
    if fam in ('pip-compile', 'pip-sync'):
        return compile_or_sync(B, st, fam, a, cwd, env, mounts)
    if fam == 'poetry':
        return poetry(B, st, a, cwd, env, mounts)
    if fam == 'pipenv':
        return pipenv(B, st, a, cwd, env, mounts)
    if fam == 'pdm':
        return pdm(B, st, a, cwd, env, mounts)
    if fam in ('conda', 'mamba', 'micromamba'):
        subs, flags, vals, pos = sub_and_flags(a, {'-f', '--file', '-n', '--name', '-p', '--prefix', '-c', '--channel'})
        if vals.get('-f') or vals.get('--file'):
            B.effects.append(eff('judge', why=f'{fam} environment or spec file'))
        elif subs[:1] == ['install'] or subs[:1] == ['create']:
            names = [norm(re.split(r'[=<>!~ ]', x)[0]) for x in pos]
            if norm(B.L) in names:
                B.effects.append(eff('judge', why='conda-level L'))
            elif names:
                B.effects.append(eff('others', why=f'{fam} packages'))
        return


def pip_like(B, st, r, cwd, env, mounts, tool, sub):
    up = r['upgrade'] or truthy(env.get('PIP_UPGRADE'))
    reqs = r['req'] + ([env['PIP_REQUIREMENT']] if env.get('PIP_REQUIREMENT') else [])
    cons = list(r['con'])
    if env.get('PIP_CONSTRAINT'):
        cons = cons + env['PIP_CONSTRAINT'].split()
    if env.get('UV_CONSTRAINT'):
        cons = cons + env['UV_CONSTRAINT'].split()
    if r['wheel_dir'] and sub == 'wheel':
        st['gen'][cjoin(cwd, r['wheel_dir'])] = len(B.effects)
    for f in reqs:
        B.effects.append(req_file(B, st, f, cwd, mounts, up, r['force'], False))
    for f in cons:
        e = req_file(B, st, f, cwd, mounts, up, r['force'], True)
        if e['kind'] == 'fresh':
            e = eff('neutral', why='constraints file without L pin')
        B.effects.append(e)
    for x in r['paths']:
        project(B, st, x, cwd, mounts, r)
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
    if nm in ('poetry', 'pipenv', 'pdm', 'uv', 'pip', 'setuptools', 'wheel', 'pip-tools'):
        B.tool_specs[nm] = str(rq.specifier)
    if nm == norm(B.L):
        sp = rq.specifier
        vs = [v for v in B.pinned if V(v)]
        admits_pin = any(sp.contains(v, prereleases=True) for v in vs) if vs else True
        exact = [s for s in sp if s.operator in ('==', '===') and '*' not in s.version]
        if exact:
            B.effects.append(eff('judge', why=f'L named inline with one version ({sp})', names_L=True, spec=str(sp)))
            return
        B.effects.append(eff('fresh', sub='upgrade' if up else 'inline', names_L=True, spec=str(sp) or 'any',
                             overrides=up or force or not admits_pin, why=f'L inline {sp}'))
    elif nm in B.own:
        B.effects.append(eff('index_own', pkg=nm, spec=str(rq.specifier), why=f'own package {nm} from the index',
                             overrides=eager))
    else:
        B.effects.append(eff('others', pkg=nm, why=f'named package {nm}', eager=eager))


def req_file(B, st, f, cwd, mounts, up, force, constraint, level=0):
    if UNK in f:
        return eff('und', why='build argument', detail=f)
    if f.startswith(('http://', 'https://')):
        return eff('judge', why=f'requirements from a URL {f[:60]}')
    cp = cjoin(cwd, f)
    r = resolve(B, st, cp, mounts)
    if r is None:
        return eff('und', why='would not build', detail=f'{f} not in the image') if level == 0 else \
            eff('und', why='would not build', detail=f'include {f} not in the image')
    k, v = r
    if k == 'gen':
        return eff('neutral', why='installs a file generated in the build', gen=v)
    if k == 'ext':
        return eff('und', why='external', detail=f'{f} comes from {v}'[:120])
    if k == 'stage':
        return eff('judge', why=f'requirements file from {k} {v}')
    if k == 'unknown':
        return eff('und', why='build argument', detail=v)
    if k in ('missing', 'outside', 'excluded'):
        return eff('und', why='would not build', detail=f'{v} {k}')
    rp = v
    if rp in B.T:
        return eff('T', files=[rp], why=f'{"-c" if constraint else "-r"} {rp}')
    lines = B.tree.lines(rp, 'requirements', B.L)
    if lines is None:
        return eff('und', why='unreadable', detail=rp)
    subs = []
    if level < 2:
        for how, inc in includes(lines):
            subs.append(req_file(B, st, inc, posixpath.dirname(cp), mounts, up, force, how == 'c', level + 1))
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
    return eff('fresh', sub='upgrade' if (up and named) else 'other file', names_L=named, spec='; '.join(spec) or None,
               spec_list=spec, files=[rp], overrides=named and (up or force), why=f'{rp}')


def project(B, st, x, cwd, mounts, r):
    x0 = re.sub(r'\[[^\]]*\]$', '', x)
    if UNK in x0:
        B.effects.append(eff('und', why='build argument', detail=x))
        return
    cp = cjoin(cwd, x0)
    if re.search(r'\.(whl|tar\.gz|zip|tgz)$', x0) or '*' in x0:
        d = posixpath.dirname(cp)
        for g, pdir in st['wheels'].items():
            if d == g or d.startswith(g + '/'):
                return project(B, st, pdir, '/', mounts, r)
        for e in (list(st['map']) + list(mounts))[::-1]:
            dest = e['dest']
            if 'stage' not in e or not (d == dest or d.startswith(dest.rstrip('/') + '/') or
                                        (not e.get('dir_dest') and posixpath.dirname(dest) == d)):
                continue
            sst = getattr(B, 'end', {}).get(e['stage'])
            for src in (e.get('srcs') or []) if sst else []:
                sd = cjoin('/', src)
                if re.search(r'[*?\[]|\.(whl|tar\.gz|zip|tgz)$', posixpath.basename(sd)):
                    sd = posixpath.dirname(sd)
                for g, pdir in sst['wheels'].items():
                    if sd == g or sd.startswith(g + '/') or g.startswith(sd + '/'):
                        return project(B, sst, pdir, '/', (), r)
            break
        rr = resolve(B, st, d, mounts)
        if rr and rr[0] in ('stage', 'gen'):
            B.effects.append(eff('neutral', why='wheel from a stage or step in the build'))
        elif rr and rr[0] == 'repo':
            B.effects.append(eff('und', why='external', detail=f'prebuilt wheel {x0} in the context'))
        else:
            B.effects.append(eff('judge', why=f'wheel {x0} of unknown origin'))
        return
    mans, other = [], None
    for m in ('pyproject.toml', 'setup.py', 'setup.cfg'):
        rr = resolve(B, st, cjoin(cp, m), mounts)
        if rr and rr[0] == 'repo':
            mans.append(rr[1])
        elif rr and rr[0] not in ('missing',):
            other = other or rr
    if not mans and resolve(B, st, cp, mounts) is None and '$' not in cp:
        names = {norm(x) for x in cp.split('/') if x}
        if names & B.own:
            B.effects.append(eff('judge', why=f'own project source outside the repository at {cp}'))
        else:
            B.effects.append(eff('others', pkg=posixpath.basename(cp), why=f'source outside the repository {cp}'))
        return
    if not mans:
        if other and other[0] in ('stage', 'gen'):
            B.effects.append(eff('neutral', why='project from a stage'))
        elif other and other[0] == 'excluded':
            B.effects.append(eff('und', why='would not build', detail=f'manifest of {x} excluded'))
        else:
            B.effects.append(eff('judge', why=f'no manifest found for {x} at {cp}'))
        return
    if any(m in B.T for m in mans):
        B.effects.append(eff('T', files=[m for m in mans if m in B.T], why=f'project {x} with manifest in T'))
        return
    lines = []
    for m in mans:
        ls = B.tree.lines(m, 'manifest', B.L)
        if ls is None:
            B.effects.append(eff('und', why='unreadable', detail=m))
            return
        lines += ls
    text = '\n'.join(lines)
    reads = sorted(t for t in B.T if posixpath.basename(t) in text and posixpath.dirname(t).startswith(posixpath.dirname(mans[0])))
    if reads:
        t = reads[0]
        how = bool(re.search(r'open\(|read_text|readlines|parse_req|\.read\(|file\s*=|file:|requirements_txt|-r ', text))
        rr = resolve(B, st, cjoin(cp, t[len(posixpath.dirname(mans[0])):].lstrip('/')), mounts)
        B.effects.append(eff('judge', why=f'manifest names T file {posixpath.basename(t)} (read pattern {"yes" if how else "no"}; '
                                          f'T file available {"yes" if rr and rr[0] == "repo" and rr[1] == t else "no"})', files=mans))
        return
    if not r.get('no_deps'):
        for m in mans:
            hold, vers = versions_in(m, '\n'.join(B.tree.lines(m, 'manifest', B.L) or []), B.L, 'manifest')
            if hold:
                B.effects.append(eff('other_pin', files=[m], version=vers, overrides=not set(vers) & set(B.pinned),
                                     why=f'project {x}: {m} pins L {",".join(vers)}' + (' (amendment 2)' if kind_of(m) is None else '')))
                return
    named = names_lib(text, B.L)
    B.effects.append(eff('fresh', sub='other file', names_L=named and not r.get('no_deps'), spec_list=spec_of(lines, B.L),
                         files=mans, why=f'project {x} ({",".join(posixpath.basename(m) for m in mans)} not in T)'))


def lock_step(B, st, proj, lockname, cwd, mounts, frozen, up, reader, relock=False, out=None, requires_lock=False):
    """A lock-reading command at project dir proj: uv, Poetry, Pipenv or PDM, as tabled in the brief."""
    lk = resolve(B, st, cjoin(proj, lockname), mounts)
    man_name = 'Pipfile' if lockname == 'Pipfile.lock' else 'pyproject.toml'
    mn = resolve(B, st, cjoin(proj, man_name), mounts)
    man_T = mn and mn[0] == 'repo' and mn[1] in B.T
    idx = len(B.effects)
    if out:
        st['gen'][cjoin(cwd, out)] = idx
    if lk and lk[0] == 'repo':
        if lk[1] not in B.T:
            ls = B.tree.lines(lk[1], 'lockfile', B.L)
            if ls is None:
                B.effects.append(eff('und', why='unreadable', detail=lk[1]))
                return
            hold, vers = versions_in(lk[1], '\n'.join(ls), B.L, 'lockfile')
            if hold:
                B.effects.append(eff('other_pin', files=[lk[1]], version=vers, why=f'{reader} lock {lk[1]} not in T locks L',
                                     overrides=not set(vers) & set(B.pinned)))
            else:
                B.effects.append(eff('fresh', sub='other file', names_L=False, files=[lk[1]], overrides=True,
                                     why=f'{reader} lock {lk[1]} not in T, without L'))
            return
        if up:
            B.effects.append(eff('T', files=[mn[1]], why=f'{reader} upgrade, pinned in T manifest') if man_T else
                             eff('fresh', sub='upgrade', names_L=None, overrides=True, why=f'{reader} re-resolves'))
        else:
            B.effects.append(eff('T', files=[lk[1]], may_relock=relock and not frozen, why=f'{reader} with lock {lk[1]}'))
        return
    if lk and lk[0] in ('stage', 'gen', 'ext', 'unknown'):
        B.effects.append(eff('judge', why=f'{reader} lock from {lk[0]}'))
        return
    if frozen or requires_lock:
        B.effects.append(eff('und', why='would not build', detail=f'{reader} requires {lockname}, not available'))
        return
    if not mn or mn[0] != 'repo':
        B.effects.append(eff('judge', why=f'{reader} without {lockname} or manifest at {proj}'))
        return
    if man_T:
        B.effects.append(eff('T', files=[mn[1]], why=f'{reader} without lock; manifest in T'))
        return
    ls = B.tree.lines(mn[1], 'manifest', B.L)
    if ls is None:
        B.effects.append(eff('und', why='unreadable', detail=mn[1]))
        return
    hold, vers = versions_in(mn[1], '\n'.join(ls), B.L, 'manifest')
    if hold:
        B.effects.append(eff('other_pin', files=[mn[1]], version=vers, overrides=not set(vers) & set(B.pinned),
                             why=f'{reader} without the lock: {mn[1]} pins L {",".join(vers)}'))
        return
    has_T_lock = any(B.T_kind.get(t) == 'lockfile' for t in B.T)
    B.effects.append(eff('fresh', sub='lock absent' if has_T_lock else 'other file', names_L=names_lib('\n'.join(ls), B.L),
                         spec_list=spec_of(ls, B.L), files=[mn[1]], overrides=True,
                         why=f'{reader} without the lock resolves {mn[1]}'))


UV_VALUED = PIP_VALUED | {'--out-dir', '--cache-dir', '--config-file', '--color', '--allow-insecure-host', '--native-tls', '--env-file',
                          '--only-group', '--no-group', '--extra', '--group', '--package', '--python', '-p', '--with',
                          '--with-requirements', '--with-editable', '--script', '--no-install-package', '--prune', '--format'}


def uv(B, st, a, cwd, env, mounts):
    subs, flags, vals, pos = sub_and_flags(a, UV_VALUED)
    s = subs[0] if subs else ''
    proj = cwd
    for k in ('--directory', '--project'):
        for v in vals.get(k, []):
            proj = cjoin(proj, v)
    frozen = '--frozen' in flags or '--locked' in flags or truthy(env.get('UV_FROZEN')) or truthy(env.get('UV_LOCKED'))
    ups = [norm(x) for x in vals.get('--upgrade-package', []) + vals.get('-P', [])]
    up = '--upgrade' in flags or '-U' in flags or norm(B.L) in ups
    if s == 'pip':
        s2 = subs[1] if len(subs) > 1 else ''
        if s2 == 'install':
            return pip_like(B, st, pip_args(a[a.index('install') + 1:]), cwd, env, mounts, 'uv', 'install')
        if s2 in ('sync', 'compile'):
            return compile_or_sync(B, st, 'pip-sync' if s2 == 'sync' else 'pip-compile', a[a.index(s2) + 1:], cwd, env, mounts)
        return
    if s == 'tool' and subs[1:2] == ['install']:
        return pip_like(B, st, pip_args(pos), cwd, env, mounts, 'uv', 'install')
    if s in ('sync', 'run', 'export', 'lock'):
        if s == 'run' and ('--no-sync' in flags or truthy(env.get('UV_NO_SYNC')) or '--no-project' in flags or
                           '--script' in vals or '--isolated' in flags):
            return
        if s == 'lock' and ('--check' in flags or '--check-exists' in flags):
            return
        out = (vals.get('-o') or vals.get('--output-file') or [None])[0] if s == 'export' else None
        return lock_step(B, st, proj, 'uv.lock', cwd, mounts, frozen, up, f'uv {s}', relock=True,
                         out=out or (env.get('__out') if s == 'export' else None))
    if s in ('add', 'remove'):
        B.effects.append(eff('judge', why=f'uv {s}'))
    if s == 'build':
        st['wheels'][cjoin(cwd, (vals.get('-o') or vals.get('--out-dir') or ['dist'])[0])] = cwd


def compile_or_sync(B, st, fam, a, cwd, env, mounts):
    r = pip_args(a)
    files = r['paths'] + r['pkgs']
    up = r['upgrade'] or bool(r['upgrade_pkgs']) or '-U' in a or '--upgrade' in a
    if fam == 'pip-sync':
        for f in files or ['requirements.txt']:
            e = req_file(B, st, f, cwd, mounts, False, False, False)
            if e['kind'] in ('fresh', 'other_pin'):
                e['overrides'] = True
            B.effects.append(e)
        return
    out = r['out'] or (os.path.splitext(files[0])[0] + '.txt' if files and files[0].endswith('.in') else 'requirements.txt')
    oc = cjoin(cwd, out)
    rr = resolve(B, st, oc, mounts)
    idx = len(B.effects)
    st['gen'][oc] = idx
    if rr and rr[0] == 'repo' and rr[1] in B.T and not up:
        B.effects.append(eff('T', files=[rr[1]], why=f'{fam} keeps the pins of {rr[1]}'))
        return
    ins = [req_file(B, st, f, cwd, mounts, False, False, False) for f in files if not f.endswith('.toml')]
    named = any(e.get('names_L') for e in ins)
    B.effects.append(eff('fresh', sub='upgrade' if up else 'other file', names_L=named, overrides=True,
                         spec_list=[s for e in ins for s in (e.get('spec_list') or [])], why=f'{fam} resolves afresh'))


POETRY_VALUED = {'-C', '--directory', '-P', '--project', '--only', '--with', '--without', '-E', '--extras', '-o', '--output', '-f',
                 '--format', '--lock'}


def poetry(B, st, a, cwd, env, mounts):
    subs, flags, vals, pos = sub_and_flags(a, POETRY_VALUED)
    s = subs[0] if subs else ''
    proj = cwd
    for k in ('-C', '--directory', '-P', '--project'):
        for v in vals.get(k, []):
            proj = cjoin(proj, v)
    if s in ('install', 'sync', 'export'):
        out = (vals.get('-o') or vals.get('--output') or [None])[0] if s == 'export' else None
        return lock_step(B, st, proj, 'poetry.lock', cwd, mounts, False, False, f'poetry {s}', out=out)
    if s == 'lock':
        spec = B.tool_specs.get('poetry', '') + ' ' + env.get('POETRY_VERSION', '')
        if re.search(r'(^|[=<~ ])1\.', spec) or '<2' in spec:
            B.effects.append(eff('judge', why='poetry lock with Poetry older than 2 (installer version)'))
            return
        if '--regenerate' in flags:
            return lock_step(B, st, proj, 'poetry.lock', cwd, mounts, False, True, 'poetry lock --regenerate')
        return lock_step(B, st, proj, 'poetry.lock', cwd, mounts, False, False, 'poetry lock', relock=True)
    if s == 'update':
        return lock_step(B, st, proj, 'poetry.lock', cwd, mounts, False, True, 'poetry update')
    if s in ('add', 'remove'):
        B.effects.append(eff('judge', why=f'poetry {s}'))
    if s == 'build':
        st['wheels'][cjoin(proj, 'dist')] = proj


def pipenv(B, st, a, cwd, env, mounts):
    subs, flags, vals, pos = sub_and_flags(a, {'--python', '--pypi-mirror', '--categories'})
    s = subs[0] if subs else ''
    proj = posixpath.dirname(cjoin(cwd, env['PIPENV_PIPFILE'])) if env.get('PIPENV_PIPFILE') else cwd
    if s == 'sync' or (s == 'install' and '--deploy' in flags and not pos):
        return lock_step(B, st, proj, 'Pipfile.lock', cwd, mounts, True, False, f'pipenv {s}')
    if s == 'requirements':
        return lock_step(B, st, proj, 'Pipfile.lock', cwd, mounts, True, False, 'pipenv requirements', out=env.get('__out'))
    if s == 'install' and not pos:
        old = re.search(r'(==|<=?)\s*20(1\d|2[0-3])\.', B.tool_specs.get('pipenv', ''))
        if old:
            return lock_step(B, st, proj, 'Pipfile.lock', cwd, mounts, False, True, 'pipenv install (Pipenv before 2024)')
        return lock_step(B, st, proj, 'Pipfile.lock', cwd, mounts, False, False, 'pipenv install', relock=True)
    if s in ('install', 'update', 'lock', 'upgrade'):
        B.effects.append(eff('judge', why=f'pipenv {s} {" ".join(pos)[:40]}'))


def pdm(B, st, a, cwd, env, mounts):
    subs, flags, vals, pos = sub_and_flags(a, {'-p', '--project', '-G', '--group', '-o', '--output', '-L', '--lockfile'})
    s = subs[0] if subs else ''
    proj = cjoin(cwd, (vals.get('-p') or vals.get('--project') or ['.'])[0])
    if s in ('install', 'sync', 'export'):
        out = (vals.get('-o') or vals.get('--output') or [None])[0] if s == 'export' else None
        return lock_step(B, st, proj, 'pdm.lock', cwd, mounts, '--frozen-lockfile' in flags, False, f'pdm {s}',
                         requires_lock=(s == 'sync'), out=out)
    if s == 'update':
        return lock_step(B, st, proj, 'pdm.lock', cwd, mounts, False, True, 'pdm update')
    if s in ('add', 'remove', 'lock'):
        B.effects.append(eff('judge', why=f'pdm {s}'))


# ================================================================ a build's class

SUB_ORDER = ['upgrade', 'lock absent', 'lock unused', 'other file', 'inline']


def decide(B, effects):
    """(class, sub-label, reason, flags) of one build, or ('to judge', '', reasons, flags)."""
    E = [e for e in effects if e['kind'] != 'neutral']
    state, last_T, ov = None, -1, None
    for i, e in enumerate(E):
        k = e['kind']
        if k == 'T':
            state, last_T = 'T', i
        elif state == 'T' and e.get('overrides') and k in ('fresh', 'override', 'other_pin', 'index_own'):
            state, ov = ('other_pin' if k == 'other_pin' else 'overridden'), e
        elif k == 'other_pin' and state != 'T':
            state = 'other_pin'
    flags = []
    installs = [e for e in E if e['kind'] not in ('others', 'judge', 'und')]
    if installs and all(e.get('at_start') for e in installs):
        flags.append('at start only')
    elif any(e.get('at_start') for e in installs):
        flags.append('at start')
    if B.template:
        flags.append('template')
    late = [e for e in E[last_T + 1:] if e['kind'] in ('judge', 'und')] if state == 'T' else []
    if state == 'T' and not late:
        t = E[last_T]
        if t.get('may_relock'):
            flags.append('may re-lock')
        return 1, '', t.get('why', ''), flags
    judges = [e for e in E if e['kind'] == 'judge']
    unds = [e for e in E if e['kind'] == 'und']
    if state == 'T':
        judges, unds = [e for e in late if e['kind'] == 'judge'], [e for e in late if e['kind'] == 'und']
    if judges:
        return 'to judge', '', '; '.join(sorted({e['why'] for e in judges}))[:300], flags
    if unds:
        u = unds[0]
        return 6, u['why'], (u.get('detail') or '')[:200], flags
    if state == 'overridden':
        return 2, 'upgrade', ov.get('why', ''), flags
    if state == 'other_pin':
        e = next(e for e in E[::-1] if e['kind'] == 'other_pin')
        return 4, '', e.get('why', ''), flags
    own = [e for e in E if e['kind'] == 'index_own']
    if own:
        return 3, '', own[0]['why'], flags
    fresh = [e for e in E if e['kind'] in ('fresh', 'override')]
    if fresh:
        subs = {e.get('sub') for e in fresh}
        tlocks = [t for t in B.T if B.T_kind.get(t) == 'lockfile' and in_context(B, t)]
        if tlocks and not ({'upgrade', 'lock absent'} & subs):
            subs.add('lock unused')
        sub = next(s for s in SUB_ORDER if s in subs)
        return 2, sub, '; '.join(sorted({e.get('why', '') for e in fresh}))[:300], flags
    if any(e['kind'] == 'others' for e in E):
        return 5, 'other named packages only', '', flags
    return 5, 'no Python install', '', flags


def classify_build(B):
    effects = walk(B)
    c = decide(B, effects)
    named = [e for e in effects if e['kind'] in ('fresh', 'override')]
    info = {
        'names_L': 'yes' if any(e.get('names_L') for e in named) else ('no' if named else ''),
        'spec': ' | '.join(sorted({s for e in named for s in (e.get('spec_list') or ([e['spec']] if e.get('spec') else []))})),
        'own_pkgs': ' '.join(sorted({e['pkg'] for e in effects if e['kind'] == 'index_own'})),
        'other_pin': ' '.join(sorted({v for e in effects if e['kind'] == 'other_pin' for v in e.get('version', [])})),
        'installers': ' '.join(sorted({e.get('why', '').split(' ')[0] for e in effects if e['kind'] != 'others'} - {''}))[:120],
        'effects': ' || '.join(f"{e['kind']}{'@start' if e.get('at_start') else ''}:{e.get('sub') or ''}:{e.get('why', '')[:80]}"
                               for e in effects)[:600],
        'notes': '; '.join(B.notes)[:200],
        'own_spec': ' '.join(sorted({e['pkg'] + e.get('spec', '') for e in effects if e['kind'] == 'index_own'})),
    }
    Ts = [e for e in effects if e['kind'] == 'T']
    info['T_files'] = '|'.join(Ts[-1].get('files', [])) if c[0] == 1 and Ts else ''
    info['T_lock'] = 'yes' if any(B.T_kind.get(f) == 'lockfile' for f in info['T_files'].split('|') if f) else 'no'
    return c, info


# ================================================================ offline tree (replays collect.py's records)

class StoredTree:
    def __init__(self, repo, commit, q, aux):
        self.q = q.get((repo, commit), {})
        self.aux = aux.get((repo, commit), {})

    def _get(self, kind, key):
        k = (kind, key)
        if k not in self.q:
            raise Unrecorded(f'{kind} {key}')
        return self.q[k]

    def exists(self, p):
        return p == '' or self._get('exists', p) == 'yes'

    def isdir(self, p):
        return p == '' or self._get('isdir', p) == 'yes'

    def glob(self, ctx, pat):
        v = self._get('glob', J(ctx, pat))
        return [x for x in v.split('|') if x]

    def lines(self, p, kind, lib):
        if p not in self.aux:
            raise Unrecorded(f'read {p}')
        st, ls = self.aux[p]
        return None if st != 'read' else ls


def load_stored():
    q, aux = {}, {}
    for r in read_csv('tree_paths.csv'):
        q.setdefault((r['repo'], r['commit']), {})[(r['query'], r['path'])] = r['result']
    for r in read_csv('aux_lines.csv'):
        d = aux.setdefault((r['repo'], r['commit']), {})
        if r['line'] == '0':
            d[r['path']] = (r['text'], [])
        elif r['path'] in d:
            d[r['path']][1].append(r['text'])
    return q, aux


def recipe_instrs(rows):
    """Instructions rebuilt from recipe_lines.csv rows of one recipe (parts concatenated in order)."""
    out, cur = [], None
    for r in rows:
        key = (r['n'], r['op'])
        if cur is None or cur['key'] != key:
            cur = {'key': key, 'n': int(r['n']), 'op': r['op'], 'rest': ''}
            out.append(cur)
        cur['rest'] += r['text']
    return out


def main():
    frame = {r['pair_id']: r for r in read_csv('frame.csv')}
    files = {}
    for r in read_csv('frame_files.csv'):
        files.setdefault(r['pair_id'], []).append(r)
    builds = read_csv('recipes.csv')
    lines = {}
    for r in read_csv('recipe_lines.csv'):
        lines.setdefault((r['repo'], r['commit'], r['path']), []).append(r)
    q, aux = load_stored()
    own = {}
    for r in frame.values():
        own.setdefault(r['repo'], set()).add(r['package'])
    judged = {}
    if os.path.exists(os.path.join(DATA, 'judgements.csv')):
        for r in read_csv('judgements.csv'):
            judged[r['build_id']] = r
    pypi = {}
    if os.path.exists(os.path.join(DATA, 'pypi.csv')):
        for r in read_csv('pypi.csv'):
            pypi.setdefault(r['build_id'], []).append(r)
    out = []
    for b in builds:
        if b['primary'] != 'yes':
            continue
        fr = frame[b['pair_id']]
        tree = StoredTree(fr['repo'], b['commit'], q, aux)
        T = [t for t in b['T_paths'].split('|') if t]
        T_kind = {f['path']: f['pin_class'] for f in files[b['pair_id']]}
        pinned = sorted({v for f in files[b['pair_id']] for v in f['versions'].split(',') if v})
        res = {'build_id': b['build_id'], 'pair_id': b['pair_id'], 'role': b['role'], 'commit': b['commit'], 'path': b['path'],
               'target': b['target'], 'context': b['context']}
        ig = aux.get((fr['repo'], b['commit']), {}).get(b['ignore_file'])
        if b['readable'] != 'yes':
            res.update({'class': 6, 'sub': 'unreadable', 'reason': b['readable'], 'decided_by': 'script'})
        elif (fr['repo'], b['commit'], b['path']) not in lines:
            res.update({'class': 6, 'sub': 'would not build', 'reason': 'no FROM instruction', 'decided_by': 'script'})
        elif ig and ig[0] != 'read':
            res.update({'class': 6, 'sub': 'unreadable', 'reason': 'ignore file unreadable', 'decided_by': 'script'})
        elif b['context_how'] == 'undetermined':
            cands = [c for c in b['context_candidates'].split('|')]
            got = set()
            for c in cands:
                B = Ctx(recipe_instrs(lines[(fr['repo'], b['commit'], b['path'])]), tree, c, aux_ignore(aux, fr['repo'], b['commit'], c, b['path']),
                        T, T_kind, fr['library'], pinned, own[fr['repo']] | set(b['own_names'].split('|')) - {''},
                        b['target'] or None, json.loads(b['build_args'] or '{}'), b['template'] == 'yes')
                got.add(classify_build(B)[0][:2])
            if len(got) == 1 and 'to judge' not in [g[0] for g in got]:
                c1, s1 = got.pop()
                res.update({'class': c1, 'sub': s1, 'reason': 'same class in every candidate context', 'decided_by': 'script'})
            else:
                res.update({'class': 6, 'sub': 'context', 'reason': 'classes differ across candidate contexts'[:200],
                            'decided_by': 'script'})
        else:
            B = Ctx(recipe_instrs(lines[(fr['repo'], b['commit'], b['path'])]), tree, b['context'],
                    aux_ignore(aux, fr['repo'], b['commit'], b['context'], b['path']), T, T_kind, fr['library'], pinned,
                    own[fr['repo']] | set(b['own_names'].split('|')) - {''}, b['target'] or None,
                    json.loads(b['build_args'] or '{}'), b['template'] == 'yes')
            (cl, sub, why, flags), info = classify_build(B)
            res.update(info)
            res.update({'class': cl, 'sub': sub, 'reason': why, 'flags': ';'.join(flags),
                        'decided_by': 'script' if cl != 'to judge' else ''})
        if res['class'] == 'to judge':
            j = judged.get(b['build_id'])
            res['judge_reason'] = res['reason']
            if j:
                res.update({'class': j['class'], 'sub': j['sub'], 'reason': j['reason'], 'decided_by': 'writer'})
                if j.get('flags'):
                    res['flags'] = ';'.join(x for x in (res.get('flags', '').split(';') + j['flags'].split(';')) if x)
                for k in ('names_L', 'spec', 'own_spec', 'T_lock'):
                    if j.get(k):
                        res[k] = j[k]
        if str(res['class']) == '3' and b['role'] == 'snapshot':
            ps = pypi.get(b['build_id'], [])
            rd = [x['reading'] for x in ps]
            res['pypi'] = 'published pin' if rd and all(x == 'published pin' for x in rd) else \
                'published range' if 'published range' in rd else 'not listed' if rd and all(x == 'not listed' for x in rd) else \
                ('not read' if not rd else 'mixed')
            res['pypi_spec'] = ' '.join(x['requires_L'] for x in ps if x['requires_L'])
        out.append(res)
    fields = ['build_id', 'pair_id', 'role', 'commit', 'path', 'target', 'context', 'class', 'sub', 'reason', 'flags',
              'decided_by', 'judge_reason', 'names_L', 'spec', 'own_pkgs', 'own_spec', 'other_pin', 'T_files', 'T_lock', 'pypi',
              'pypi_spec', 'installers', 'effects', 'notes']
    write_csv('recipe_classes.csv', out, fields)
    # every context fixed by rule (1) must be supported by a retained compose stanza or workflow line (version 0.2)
    facts = collections.defaultdict(set)
    for (repo, commit), d in aux.items():
        for path, (st, ls) in d.items():
            for t in ls:
                if t.startswith('LH015-build '):
                    try:
                        f = json.loads(t[len('LH015-build '):])
                    except ValueError:
                        continue
                    facts[(repo, commit)].add((f.get('dockerfile', ''), f.get('context', '')))
    r1 = [b for b in builds if b['primary'] == 'yes' and b['context_how'] in ('compose', 'workflow')]
    ok = sum(1 for b in r1 if (b['path'], b['context']) in facts[(frame[b['pair_id']]['repo'], b['commit'])])
    print(f'rule (1) contexts supported by retained lines: {ok} of {len(r1)}')
    from collections import Counter
    c = Counter((r['role'], str(r['class'])) for r in out)
    print('builds classed:', len(out), dict(sorted(c.items())))


def aux_ignore(aux, repo, commit, ctx, recipe_path):
    """The ignore file's lines: <recipe name>.dockerignore beside the recipe, else .dockerignore at the context's root."""
    d = aux.get((repo, commit), {})
    beside = recipe_path.split('#')[0] + '.dockerignore'
    for p in (beside, J(ctx, '.dockerignore')):
        if p in d:
            st, ls = d[p]
            return ls if st == 'read' else ['**']
    return []


if __name__ == '__main__':
    main()
