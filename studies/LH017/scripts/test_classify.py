"""Synthetic cases for LH017's rules (ci.py, extract.py): each is a small repository, a pair's L and T, and the class
the brief gives its job. Run: python3 test_classify.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ci as C  # noqa: E402
import extract as X  # noqa: E402
from collect import relevant  # noqa: E402


class FakeTree:
    def __init__(self, files, libs, slug='o/r'):
        self.files, self.libs, self.repo_slug = files, libs, slug
        self.dirs = {'/'.join(f.split('/')[:k]) for f in files for k in range(1, f.count('/') + 1)}
        self.aux = {}

    def exists(self, p):
        return p == '' or p in self.files or p in self.dirs

    def read(self, p):
        return self.files.get(p)

    def lines(self, p):
        t = self.files.get(p)
        return None if t is None else relevant(t, self.libs, p)

    def struct(self, kind, p, key):
        if kind == 'uvmember':
            return X.uv_member(self, p, key)
        if kind == 'tox':
            return X.tox_struct(self, p, key)
        if kind == 'hatch':
            return X.hatch_struct(self, p, key)
        t = self.files.get(p)
        if t is None:
            return None
        return {'script': lambda: X.script_struct(t), 'make': lambda: X.make_struct(t, key),
                'just': lambda: X.just_struct(t, key), 'nox': lambda: X.nox_struct(t, key)}[kind]()


def jobs_of(files, wf='.github/workflows/ci.yml'):
    tree = FakeTree(files, ['cryptography'])
    d = X.load_yaml(files[wf])
    return tree, X.github_jobs(tree, wf, d, X.local_calls({wf: d}))


def run(files, T, L='cryptography', T_kind=None, pinned=('46.0.5',), own=('mypkg',), wf='.github/workflows/ci.yml'):
    tree, jobs = jobs_of(files, wf)
    tree.default_branch = 'main'
    out = []
    for j in jobs:
        B = C.Job(j['steps'], tree, T, T_kind or {t: ('lockfile' if t.endswith('.lock') else 'exact pin') for t in T}, L,
                  list(pinned), own)
        (cls, sub, why, flags), info = C.classify_job(B)
        out.append((j['job'], j['variant'], cls, sub, info['T_lock'], flags))
    return out


WF = '''on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{steps}
'''


def wf(steps):
    return WF.format(steps='\n'.join('      ' + s for s in steps.strip('\n').split('\n')))


PY = '[project]\nname = "mypkg"\ndependencies = ["cryptography==46.0.5"]\n'
PYR = '[project]\nname = "mypkg"\ndependencies = ["cryptography>=45"]\n'
LOCK = '[[package]]\nname = "cryptography"\nversion = "46.0.5"\n'

CASES = [
    ('uv sync --locked reads the T lock', {'.github/workflows/ci.yml': wf('- run: uv sync --locked'), 'pyproject.toml': PYR,
                                           'uv.lock': LOCK}, ['uv.lock'], (1, '', 'yes')),
    ('uv run without flags: class 1, may re-lock', {'.github/workflows/ci.yml': wf('- run: uv run pytest'), 'pyproject.toml': PYR,
                                                    'uv.lock': LOCK}, ['uv.lock'], (1, '', 'yes')),
    ('pip install -e . with the pin in a T manifest', {'.github/workflows/ci.yml': wf('- run: pip install -e .[test]'),
                                                       'pyproject.toml': PY}, ['pyproject.toml'], (1, '', 'no')),
    ('pip install -e . leaves the T lock unused', {'.github/workflows/ci.yml': wf('- run: pip install -e .'), 'pyproject.toml': PYR,
                                                   'uv.lock': LOCK}, ['uv.lock'], (2, 'lock unused', 'no')),
    ('pip -r of a T requirements file', {'.github/workflows/ci.yml': wf('- run: |\n    python -m pip install --upgrade pip\n    pip install -r requirements.txt'),
                                         'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('pip -r of a file that includes the T file', {'.github/workflows/ci.yml': wf('- run: pip install -r requirements-dev.txt'),
                                                   'requirements-dev.txt': '-r requirements.txt\npytest\n',
                                                   'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('poetry install reads poetry.lock', {'.github/workflows/ci.yml': wf('- uses: snok/install-poetry@v1\n- run: poetry install --no-interaction'),
                                          'pyproject.toml': PYR, 'poetry.lock': LOCK}, ['poetry.lock'], (1, '', 'yes')),
    ('working-directory and a T lock below the root', {'.github/workflows/ci.yml': wf('- run: uv sync --frozen\n  working-directory: backend'),
                                                       'backend/pyproject.toml': PYR, 'backend/uv.lock': LOCK},
     ['backend/uv.lock'], (1, '', 'yes')),
    ('cd in the script', {'.github/workflows/ci.yml': wf('- run: cd backend && poetry install'), 'backend/pyproject.toml': PYR,
                          'backend/poetry.lock': LOCK}, ['backend/poetry.lock'], (1, '', 'yes')),
    ('uv sync at the root misses a lock below it', {'.github/workflows/ci.yml': wf('- run: uv sync'), 'pyproject.toml': PYR,
                                                    'backend/pyproject.toml': PYR, 'backend/uv.lock': LOCK},
     ['backend/uv.lock'], (2, 'lock absent', 'no')),
    ('tox with deps from a T file', {'.github/workflows/ci.yml': wf('- run: pip install tox\n- run: tox -e py311'),
                                     'tox.ini': '[tox]\nenvlist = py311\n[testenv]\ndeps = -r requirements.txt\ncommands = pytest\n',
                                     'requirements.txt': 'cryptography==46.0.5\n', 'pyproject.toml': PYR},
     ['requirements.txt'], (1, '', 'no')),
    ('tox-uv lock runner', {'.github/workflows/ci.yml': wf('- run: uvx --with tox-uv tox -e type'),
                            'tox.ini': '[tox]\nenvlist = type\n[testenv:type]\nrunner = uv-venv-lock-runner\ncommands = mypy\n',
                            'pyproject.toml': PYR, 'uv.lock': LOCK}, ['uv.lock'], (1, '', 'yes')),
    ('tox skip_install with other deps only', {'.github/workflows/ci.yml': wf('- run: tox -e lint'),
                                               'tox.ini': '[testenv:lint]\nskip_install = true\ndeps = ruff\ncommands = ruff check\n',
                                               'uv.lock': LOCK}, ['uv.lock'], (5, 'other named packages only', 'no')),
    ('make target with a prerequisite', {'.github/workflows/ci.yml': wf('- run: make test'),
                                         'Makefile': 'PIP := python -m pip\ninstall:\n\t$(PIP) install -r requirements.txt\ntest: install\n\tpytest\n',
                                         'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('a script called by path', {'.github/workflows/ci.yml': wf('- run: ./scripts/setup.sh'),
                                 'scripts/setup.sh': '#!/bin/sh\nset -e\npip install -r requirements.txt\n',
                                 'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('no checkout: the file is not there', {'.github/workflows/ci.yml': 'on: push\njobs:\n  a:\n    runs-on: x\n    steps:\n      - run: pip install -r requirements.txt\n',
                                            'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (6, 'would not run', 'no')),
    ('pre-commit only', {'.github/workflows/ci.yml': wf('- uses: pre-commit/action@v3.0.1'), 'uv.lock': LOCK}, ['uv.lock'],
     (5, 'other named packages only', 'no')),
    ('container build only', {'.github/workflows/ci.yml': wf('- uses: docker/build-push-action@v6\n  with:\n    context: .'),
                              'uv.lock': LOCK}, ['uv.lock'], (5, 'container build only', 'no')),
    ('own package from the index', {'.github/workflows/ci.yml': wf('- run: pip install mypkg'), 'uv.lock': LOCK}, ['uv.lock'],
     (3, '', 'no')),
    ('L pinned inline', {'.github/workflows/ci.yml': wf('- run: pip install cryptography==46.0.4'), 'uv.lock': LOCK},
     ['uv.lock'], (4, 'inline pin', 'no')),
    ('L named with a range, with a T lock unused', {'.github/workflows/ci.yml': wf('- run: pip install "cryptography>=40"'),
                                                    'uv.lock': LOCK}, ['uv.lock'], (2, 'lock unused', 'no')),
    ('L named with a range', {'.github/workflows/ci.yml': wf('- run: pip install "cryptography>=40"'),
                              'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (2, 'inline', 'no')),
    ('T then an upgrade of L overrides', {'.github/workflows/ci.yml': wf('- run: uv sync --locked\n- run: uv pip install -U cryptography'),
                                          'pyproject.toml': PYR, 'uv.lock': LOCK}, ['uv.lock'], (2, 'upgrade', 'no')),
    ('frozen without the lock would not run', {'.github/workflows/ci.yml': wf('- run: uv sync --frozen'), 'pyproject.toml': PYR,
                                               'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'],
     (6, 'would not run', 'no')),
    ('local composite action', {'.github/workflows/ci.yml': wf('- uses: ./.github/actions/setup'),
                                '.github/actions/setup/action.yml': 'runs:\n  using: composite\n  steps:\n    - run: pip install -r requirements.txt\n      shell: bash\n',
                                'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('hatch run with the pin in the T manifest', {'.github/workflows/ci.yml': wf('- run: pipx install hatch\n- run: hatch run test'),
                                                  'pyproject.toml': PY}, ['pyproject.toml'], (1, '', 'no')),
    ('nox session installing a T file', {'.github/workflows/ci.yml': wf('- run: nox -s tests'),
                                         'noxfile.py': 'import nox\n@nox.session\ndef tests(session):\n    session.install("-r", "requirements.txt")\n    session.run("pytest")\n',
                                         'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('an unsubstituted secret decides', {'.github/workflows/ci.yml': wf('- run: pip install -r ${{ secrets.REQS }}'),
                                         'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (6, 'build argument', 'no')),
    ('another pinned file', {'.github/workflows/ci.yml': wf('- run: pip install -r ci/requirements.txt'),
                             'ci/requirements.txt': 'cryptography==46.0.4\n', 'uv.lock': LOCK}, ['uv.lock'], (4, '', 'no')),
    ('uv export piped to pip keeps the lock', {'.github/workflows/ci.yml': wf('- run: uv export --frozen -o requirements.txt\n- run: pip install -r requirements.txt'),
                                               'pyproject.toml': PYR, 'uv.lock': LOCK}, ['uv.lock'], (1, '', 'yes')),
    ('amendment 1: a script that moves to its own directory', {'.github/workflows/ci.yml': wf('- run: ./tools/build.sh'),
        'tools/build.sh': '#!/usr/bin/env bash\nROOT="$(cd "$(dirname "$0")/.." && pwd)"\ncd "$ROOT/app"\npip install -r requirements.txt\n',
        'app/requirements.txt': 'cryptography==46.0.5\n'}, ['app/requirements.txt'], (1, '', 'no')),
    ('a wheel built outside the repository is another package', {'.github/workflows/ci.yml': wf('- run: |\n    cd /tmp/vision\n    python setup.py bdist_wheel\n    pip install /tmp/vision/dist/torchvision-1.whl'),
        'uv.lock': LOCK}, ['uv.lock'], (5, 'other named packages only', 'no')),
    ('a wheel from a needed job\'s artefact installs the project', {'.github/workflows/ci.yml': '''on: push
jobs:
  build:
    runs-on: x
    steps:
      - uses: actions/checkout@v4
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with: {name: dist, path: dist/}
  test:
    needs: build
    runs-on: x
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: dist, path: dist}
      - run: pip install dist/*.whl
''', 'pyproject.toml': PY}, ['pyproject.toml'], None),
    ('a Makefile pattern rule', {'.github/workflows/ci.yml': wf('- run: make lint_flake8'),
                                 'Makefile': 'lint_%:\n\tpip install -r requirements-$*.txt\n',
                                 'requirements-flake8.txt': 'cryptography==46.0.5\n'}, ['requirements-flake8.txt'], (1, '', 'no')),
    ('a tox changedir by factor', {'.github/workflows/ci.yml': wf('- run: tox -e lint'),
                                   'tox.ini': '[testenv]\nchangedir =\n    common: ./packages/common\ndeps = -r./requirements-dev.txt\nskip_install = true\n',
                                   'requirements-dev.txt': 'cryptography==46.0.5\n'}, ['requirements-dev.txt'], (1, '', 'no')),
    ('a checkout of the default branch', {'.github/workflows/ci.yml': wf('- run: pip install -r requirements.txt').replace('actions/checkout@v4', 'actions/checkout@v4\n        with:\n          ref: main'),
                                          'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('ls of a pattern (amendment 1)', {'.github/workflows/ci.yml': wf('- run: |\n    python -m build\n    pip install $(ls dist/*.whl)'),
                                       'pyproject.toml': PY}, ['pyproject.toml'], (1, '', 'no')),
    ('a program made in the job is not a repository script', {'.github/workflows/ci.yml': wf('- run: ./mcp-publisher login'),
                                                               'uv.lock': LOCK}, ['uv.lock'], (5, 'no Python install', 'no')),
    ('a wheel listed by a subshell in a needed job\'s artefact (amendment 1)', {'.github/workflows/ci.yml': '''on: push
jobs:
  build:
    runs-on: x
    steps:
      - uses: actions/checkout@v4
      - run: python -m build
  tests:
    needs: build
    runs-on: x
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: dist, path: dist}
      - run: |
          PACKAGE=`(cd dist && ls *whl)` && echo $PACKAGE
          pip install --pre ./dist/$PACKAGE
''', 'pyproject.toml': PY}, ['pyproject.toml'], None),
    ('amendment 2: poetry update --lock installs nothing', {'.github/workflows/ci.yml': wf('- run: poetry update --lock'),
        'pyproject.toml': PYR, 'poetry.lock': LOCK}, ['poetry.lock'], (5, 'no Python install', 'no')),
    ('amendment 2: an install after poetry update --lock takes the re-resolved lock', {'.github/workflows/ci.yml': wf('- run: poetry update --lock && poetry install'),
        'pyproject.toml': PYR, 'poetry.lock': LOCK}, ['poetry.lock'], (2, 'upgrade', 'no')),
    ('a make target from an expression', {'.github/workflows/ci.yml': wf('- run: make ${{ env.FLAGS }}'), 'Makefile': 'all:\n\ttrue\n',
        'uv.lock': LOCK}, ['uv.lock'], (6, 'build argument', 'no')),
    ('xargs runs the installer', {'.github/workflows/ci.yml': wf('- run: grep "^pytest-" c.txt | xargs pip install -c ci/requirements-constraints.txt pytest'),
        'ci/requirements-constraints.txt': 'cryptography==46.0.4\n', 'uv.lock': LOCK}, ['uv.lock'], (4, '', 'no')),
    ('xargs bash -c runs its text', {'.github/workflows/ci.yml': wf('- run: ls | xargs -I {} bash -c \'pip install -r requirements.txt\''),
        'requirements.txt': 'cryptography==46.0.5\n'}, ['requirements.txt'], (1, '', 'no')),
    ('--no-deps installs no version of L', {'.github/workflows/ci.yml': wf('- run: pip install --no-deps .'), 'pyproject.toml': PY},
        ['pyproject.toml'], (2, 'other file', 'no')),
    ('amendment 3: uv sync --package takes the member manifest', {'.github/workflows/ci.yml': wf('- run: uv sync --package mypkg-tools'),
        'pyproject.toml': '[project]\nname = "root"\n[tool.uv.workspace]\nmembers = ["packages/*"]\n',
        'packages/core/pyproject.toml': '[project]\nname = "mypkg"\ndependencies = ["cryptography==46.0.5"]\n',
        'packages/tools/pyproject.toml': '[project]\nname = "mypkg-tools"\n[tool.uv.sources]\nmypkg = { workspace = true }\n'},
        ['packages/core/pyproject.toml'], (1, '', 'no')),
    ('amendment 3: uv run at a workspace root resolves the members too', {'.github/workflows/ci.yml': wf('- run: uv sync --package mypkg-tools\n- run: uv run pytest'),
        'pyproject.toml': '[project]\nname = "root"\n[tool.uv.workspace]\nmembers = ["packages/*"]\n',
        'packages/core/pyproject.toml': '[project]\nname = "mypkg"\ndependencies = ["cryptography==46.0.5"]\n',
        'packages/tools/pyproject.toml': '[project]\nname = "mypkg-tools"\n[tool.uv.sources]\nmypkg = { workspace = true }\n'},
        ['packages/core/pyproject.toml'], (1, '', 'no')),
    ('own package beside wheels an external action built', {'.github/workflows/ci.yml': wf('- uses: PyO3/maturin-action@v1\n  with:\n    command: build\n- run: pip install --find-links=target/wheels mypkg'),
        'pyproject.toml': PY}, ['pyproject.toml'], (6, 'external', 'no')),
    ('make in a directory outside the workspace', {'.github/workflows/ci.yml': wf('- run: |\n    pushd ~/go/src/x\n    make install\n    popd'),
                                                   'uv.lock': LOCK}, ['uv.lock'], (5, 'no Python install', 'no')),
]


def main():
    bad = 0
    for name, files, T, want in CASES:
        if want is None:
            res = run(files, T)
            got = [(j, c, sub) for (j, _, c, sub, _, _) in res]
            ok = any(j in ('test', 'tests') and c == 1 for (j, c, sub) in got)
            bad += not ok
            print(('ok  ' if ok else 'FAIL'), name, got if not ok else '')
            continue
        res = run(files, T)
        got = [(c, s, tl) for (_, _, c, s, tl, _) in res]
        ok = all(g == want for g in got) and got
        if not ok:
            bad += 1
        print(('ok  ' if ok else 'FAIL'), name, got if not ok else '')
    # matrix: one variant per requirements file, which differ
    files = {'.github/workflows/ci.yml': '''on: push
jobs:
  t:
    runs-on: x
    strategy:
      matrix:
        req: [requirements.txt, requirements-min.txt]
        py: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r ${{ matrix.req }}
''', 'requirements.txt': 'cryptography==46.0.5\n', 'requirements-min.txt': 'cryptography>=40\n'}
    res = run(files, ['requirements.txt'])
    got = sorted((c, s) for (_, _, c, s, _, _) in res)
    ok = got == [(1, ''), (2, 'other file')]
    bad += not ok
    print(('ok  ' if ok else 'FAIL'), 'matrix variants', got if not ok else '')
    # external reusable workflow
    files = {'.github/workflows/ci.yml': 'on: push\njobs:\n  a:\n    uses: org/shared/.github/workflows/py.yml@main\n'}
    res = run(files, ['uv.lock'])
    ok = [(c, s) for (_, _, c, s, _, _) in res] == [(6, 'external')]
    bad += not ok
    print(('ok  ' if ok else 'FAIL'), 'external reusable workflow')
    print(f'{len(CASES) + 2 - bad} of {len(CASES) + 2} cases pass')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
