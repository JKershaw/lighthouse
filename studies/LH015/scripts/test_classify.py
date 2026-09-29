"""Synthetic recipes for classify.py's rules (brief, "Classification and its check", step 2). python3 test_classify.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify as C  # noqa: E402


class FakeTree:
    def __init__(self, files):
        self.files = files
        self.dirs = {'/'.join(f.split('/')[:k]) for f in files for k in range(1, f.count('/') + 1)}

    def exists(self, p):
        return p == '' or p in self.files or p in self.dirs

    def isdir(self, p):
        return p == '' or p in self.dirs

    def glob(self, ctx, pat):
        import re
        rx = re.compile(C.glob_re(C.J(ctx, pat)))
        return sorted(f for f in self.files if rx.match(f))

    def lines(self, p, kind=None, lib=None):
        return self.files[p].split('\n') if p in self.files else None


L = 'requests'


def run(df, files, T, kinds=None, ignore=None, own=('myapp',), target=None, args=None, ctx=''):
    tree = FakeTree(files)
    B = C.Ctx(C.parse_dockerfile(df), tree, ctx, (ignore or '').split('\n') if ignore else [], T,
              kinds or {t: ('lockfile' if t.endswith('.lock') else 'exact pin') for t in T}, L, ['2.31.0'], own, target, args)
    (cl, sub, why, flags), info = C.classify_build(B)
    return cl, sub, flags, info


REQ = {'requirements.txt': 'requests==2.31.0\nflask>=2', 'pyproject.toml': '[project]\nname = "myapp"\ndependencies = ["requests>=2"]',
       'uv.lock': '[[package]]\nname = "requests"\nversion = "2.31.0"', 'app.py': ''}
CASES = [
    ('-r of a T file', 'FROM python:3.12\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt', REQ,
     ['requirements.txt'], {}, (1, '')),
    ('lock unused', 'FROM python:3.12\nWORKDIR /app\nCOPY . .\nRUN pip install .', REQ, ['uv.lock'], {}, (2, 'lock unused')),
    ('uv sync --frozen with lock', 'FROM python:3.12\nWORKDIR /app\nCOPY pyproject.toml uv.lock ./\nRUN uv sync --frozen --no-dev',
     REQ, ['uv.lock'], {}, (1, '')),
    ('uv sync --frozen without lock', 'FROM python:3.12\nWORKDIR /app\nCOPY pyproject.toml ./\nRUN uv sync --frozen', REQ,
     ['uv.lock'], {}, (6, 'would not build')),
    ('uv sync may re-lock', 'FROM python:3.12\nWORKDIR /app\nCOPY . /app\nRUN uv sync', REQ, ['uv.lock'], {}, (1, '', 'may re-lock')),
    ('uv sync lock absent', 'FROM python:3.12\nWORKDIR /app\nCOPY pyproject.toml ./\nRUN uv sync', REQ, ['uv.lock'], {},
     (2, 'lock absent')),
    ('exact pin in T manifest', 'FROM python:3.12\nCOPY . /src\nRUN pip install /src', REQ, ['pyproject.toml'], {}, (1, '')),
    ('own package from index', 'FROM python:3.12\nRUN pip install myapp==1.0', REQ, ['requirements.txt'], {}, (3, '')),
    ('other named only', 'FROM python:3.12\nRUN pip install --upgrade pip gunicorn', REQ, ['requirements.txt'], {},
     (5, 'other named packages only')),
    ('no install', 'FROM python:3.12\nCOPY . .\nCMD ["python", "app.py"]', REQ, ['requirements.txt'], {}, (5, 'no Python install')),
    ('ignored lock', 'FROM python:3.12\nWORKDIR /app\nCOPY . .\nRUN uv sync --locked', REQ, ['uv.lock'], {'ignore': '*.lock'},
     (6, 'would not build')),
    ('ignore exception', 'FROM python:3.12\nWORKDIR /app\nCOPY . .\nRUN uv sync --locked', REQ, ['uv.lock'],
     {'ignore': '**/*.lock\n!uv.lock'}, (1, '')),
    ('multi-stage prefix', 'FROM python:3.12 AS b\nCOPY requirements.txt .\nRUN pip install --prefix=/install -r requirements.txt\n'
     'FROM python:3.12-slim\nCOPY --from=b /install /usr/local\nCOPY . /app', REQ, ['requirements.txt'], {}, (1, '')),
    ('stage outside path', 'FROM python:3.12 AS dev\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\n'
     'FROM python:3.12 AS prod\nRUN pip install myapp', REQ, ['requirements.txt'], {}, (3, '')),
    ('upgrade after T', 'FROM python:3.12\nCOPY requirements.txt .\nRUN pip install -r requirements.txt && pip install -U requests',
     REQ, ['requirements.txt'], {}, (2, 'upgrade')),
    ('poetry export', 'FROM python:3.12\nWORKDIR /app\nCOPY pyproject.toml poetry.lock ./\n'
     'RUN poetry export -f requirements.txt -o requirements.txt && pip install -r requirements.txt',
     {**REQ, 'poetry.lock': 'x'}, ['poetry.lock'], {}, (1, '')),
    ('ARG without default', 'FROM python:3.12\nARG REQ\nCOPY . .\nRUN pip install -r $REQ', REQ, ['requirements.txt'], {},
     (6, 'build argument')),
    ('ARG given by compose', 'FROM python:3.12\nARG REQ\nCOPY . .\nRUN pip install -r $REQ', REQ, ['requirements.txt'],
     {'args': {'REQ': 'requirements.txt'}}, (1, '')),
    ('script one level', 'FROM python:3.12\nWORKDIR /app\nCOPY . .\nRUN ./scripts/install.sh',
     {**REQ, 'scripts/install.sh': 'set -e\npip install -r requirements.txt'}, ['requirements.txt'], {}, (1, '')),
    ('include of T', 'FROM python:3.12\nCOPY req/ /req/\nRUN pip install -r /req/prod.txt',
     {'req/prod.txt': '-r base.txt\ngunicorn', 'req/base.txt': 'requests==2.31.0'}, ['req/base.txt'], {}, (1, '')),
    ('another pinned file', 'FROM python:3.12\nCOPY . .\nRUN pip install -r requirements/deploy/x/prod.txt',
     {'requirements/deploy/x/prod.txt': 'requests==2.32.0', 'uv.lock': ''}, ['uv.lock'], {}, (4, '')),
    ('uv run at start', 'FROM python:3.12\nWORKDIR /app\nCOPY . .\nCMD ["uv", "run", "--frozen", "app.py"]', REQ, ['uv.lock'], {},
     (1, '', 'at start only')),
    ('other file never names L', 'FROM python:3.12\nCOPY requirements-prod.txt .\nRUN pip install -r requirements-prod.txt',
     {'requirements-prod.txt': 'flask==3.0', 'uv.lock': ''}, ['uv.lock'], {}, (2, 'lock unused')),
    ('context below root', 'FROM python:3.12\nCOPY requirements.txt .\nRUN pip install -r requirements.txt',
     {'svc/requirements.txt': 'requests==2.31.0', 'requirements.txt': 'x'}, ['requirements.txt'], {'ctx': 'svc'}, (4, '')),
    ('target build', 'FROM python:3.12 AS base\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\n'
     'FROM base AS test\nRUN pip install -U requests\nFROM base AS prod\nCMD ["python"]', REQ, ['requirements.txt'],
     {'target': 'test'}, (2, 'upgrade')),
    ('pip-sync of T', 'FROM python:3.12\nCOPY requirements.txt .\nRUN pip install pip-tools && pip-sync requirements.txt', REQ,
     ['requirements.txt'], {}, (1, '')),
    ('template placeholder', 'FROM python:3.12\nCOPY . .\nRUN pip install -r {{ reqfile }}', REQ, ['requirements.txt'],
     {'template': True}, (6, 'build argument')),
    # corrections after the blind check (R-0021, version 0.2)
    ('wheel built in another stage', 'FROM python:3.12 AS b\nWORKDIR /tmp\nCOPY . .\nRUN pip install build && python -m build\n'
     'FROM python:3.12-slim\nCOPY --from=b /tmp/dist/*.whl /dist/\nRUN pip install /dist/*.whl', REQ, ['uv.lock'], {},
     (2, 'lock unused')),
    ('install delegated to a playbook (amendment 7)', 'FROM python:3.12\nRUN pip install ansible==11.11.0 && '
     'git clone https://example.org/deploy.git /deploy && ansible-playbook /deploy/site.yml', REQ, ['requirements.txt'], {},
     (6, 'script not read')),
    ('manifest not in T pinning L (amendment 2)', 'FROM python:3.12\nWORKDIR /app\nCOPY pyproject.docker.toml pyproject.toml\n'
     'COPY src ./src\nRUN pip install .[cpu]', {'pyproject.docker.toml': '[project]\nname = "myapp"\ndependencies = ["requests==2.30.0"]',
                                                 'uv.lock': '', 'src/x.py': ''}, ['uv.lock'], {}, (4, '')),
]


def main():
    bad = 0
    for name, df, files, T, kw, want in CASES:
        tmpl = kw.pop('template', False)
        tree_kw = dict(kw)
        if tmpl:
            df = C.template_marks(df)
        cl, sub, flags, info = run(df, files, T, **tree_kw)
        ok = (cl, sub) == want[:2] and all(f in flags for f in want[2:])
        bad += not ok
        print(('ok  ' if ok else 'FAIL'), name, '->', cl, sub, flags, '' if ok else info['effects'][:200])
    print(f'{len(CASES) - bad} of {len(CASES)} passed')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
