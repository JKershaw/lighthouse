#!/usr/bin/env python3
"""LH011: the installers' own source for the CI flag. Reads PyPI's JSON for pip and uv, picks for
each the newest non-pre-release version whose first file was uploaded before 2026-04-01T00:00:00Z and
before 2026-09-01T00:00:00Z (the versions current on 1 April and on 31 August 2026), downloads those
versions' source distributions from files.pythonhosted.org into the scratch directory, and extracts
the files that build the User-Agent string PyPI's log processor parses. Writes
data/installer_versions.csv and data/installer_source_excerpts.txt (the relevant files' paths,
SHA-256 of each sdist, and the excerpted lines, with line numbers).

New for LH011: LH005 could not read how the flag is set (linehaul's repository was refused, and the
installers' sources were not read). Usage: python3 collect_installers.py"""
import hashlib, os, re, tarfile
from packaging.version import Version
from common import get_json, download, write_csv, SCRATCH, DATA

CUTS = ('2026-04-01T00:00:00', '2026-09-01T00:00:00')
# files whose text builds the User-Agent (found by searching each sdist for 'ci' and 'linehaul')
WANT = {'pip': [r'src/pip/_internal/network/session\.py$', r'src/pip/_internal/utils/misc\.py$'],
        'uv': [r'crates/uv-client/src/linehaul\.rs$', r'crates/uv-client/src/base_client\.rs$']}

rows, excerpts = [], []
for tool in ('pip', 'uv'):
    _, d = get_json('PyPI JSON API', f'I {tool}', f'https://pypi.org/pypi/{tool}/json', 'installer_versions.csv')
    for cut in CUTS:
        best = None
        for ver, files in d['releases'].items():
            v = Version(ver)
            if v.is_prerelease or v.is_devrelease or not files:
                continue
            t = min(f['upload_time_iso_8601'] for f in files)
            if t[:19] < cut and (best is None or v > Version(best[0])):
                best = (ver, t, files)
        ver, t, files = best
        sd = [f for f in files if f['packagetype'] == 'sdist'][0]
        path = os.path.join(SCRATCH, sd['filename'])
        if not os.path.exists(path):  # a second run reuses the scratch copy and checks its hash
            download('files.pythonhosted.org', f'S {tool} {ver}', sd['url'], path)
        sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        rows.append(dict(installer=tool, current_before=cut[:10], version=ver, first_upload_utc=t,
                         sdist=sd['filename'], sdist_url=sd['url'], sha256=sha,
                         pypi_sha256=sd['digests']['sha256'], sha256_matches=(sha == sd['digests']['sha256'])))
        with tarfile.open(path) as tf:
            for m in tf.getmembers():
                if any(re.search(p, m.name) for p in WANT[tool]):
                    text = tf.extractfile(m).read().decode('utf-8', 'replace').splitlines()
                    keep = set()
                    for i, line in enumerate(text):
                        if re.search(r'\bci\b|CI_ENV|looks_like_ci|linehaul|LineHaul|user_agent|BUILD_BUILDID|'
                                     r'GITHUB_ACTIONS|PIP_IS_CI|GITLAB|TRAVIS|TF_BUILD|CODEBUILD|JENKINS', line):
                            keep.update(range(max(0, i - 3), min(len(text), i + 4)))
                    excerpts.append(f'==== {tool} {ver} ({sd["filename"]}, sha256 {sha}) :: {m.name}')
                    excerpts += [f'{i + 1:5d}  {text[i]}' for i in sorted(keep)]
write_csv('installer_versions.csv', rows)
open(os.path.join(DATA, 'installer_source_excerpts.txt'), 'w').write('\n'.join(excerpts) + '\n')
print(rows)
