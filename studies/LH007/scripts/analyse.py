#!/usr/bin/env python3
"""LH007 step 6: the tables. No network access.
data/image_timeline.csv  one row per image whose configuration was read: build time, days since the
                         release, install class and its basis, installed mcp, the project's pin and
                         lock at the build's commit, and whether they agree.
data/share_by_class.csv  by install class and bin of days since release: images read to a result and
                         how many held the new release (1.28.x).
data/first_new.csv       per repository: last image read without 1.28.x, first with it, and the
                         project's first commit pinning or locking 1.28.x.
data/disagreements.csv   images whose installed mcp differs from what the project's lock or pin says."""
import datetime, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv
from collect_images import RELEASE, P0, P1, sampled

FMT = '%Y-%m-%dT%H:%M:%SZ'
rel = datetime.datetime.strptime(RELEASE, FMT)
days = lambda s: (datetime.datetime.strptime(s, FMT) - rel).total_seconds() / 86400
PYPI = collections.defaultdict(list)
for r in read_csv('project_mcp_pins_pypi.csv'):
    PYPI[r['package']].append(r)


def pypi_at(pkg, when, version=None):
    """requires_dist of the named version, or of the latest release published at or before `when`."""
    rs = PYPI[pkg]
    if version:
        rs = [r for r in rs if r['version'] == version]
        return rs[0] if rs else None
    rs = [r for r in rs if r['published_utc'] <= when and not re.search(r'(a|b|rc|dev)\d', r['version'])]
    return rs[-1] if rs else None


def spec_of(manifest_specs, path):
    for s in manifest_specs.split('; '):
        if s.startswith(path + ':'):
            return s.split(': ', 1)[1]
    return ''


def classify(img, b, cfg_version):
    """(class, what fixes mcp, basis). The rule per repository is the brief's, applied to the Dockerfile
    at the build's commit (b['dockerfile_install_lines']) and the project's files there."""
    L = b['dockerfile_install_lines']
    lock = b['uv_lock_mcp'].split('=')[-1] if b['uv_lock_mcp'] else ''
    if not L:
        return 'unknown', '', 'no Dockerfile read at the build commit'
    if 'absent at this commit' in L:
        return 'unknown', '', L
    if 'uv sync' in L and b['lock_files']:
        return 'lockfile', f'uv.lock mcp {lock}' if lock else 'uv.lock', 'uv sync with the committed lockfile'
    if 'uv sync' in L:  # no lockfile committed: uv resolves from pyproject.toml at build time
        s = spec_of(b['manifest_specs'], 'pyproject.toml')
        if s.startswith('mcp=='):
            return 'exact pin', f'pyproject.toml {s}', 'uv sync with no lockfile committed; pyproject names one version'
        if s:
            return 'open range', f'pyproject.toml {s}', 'uv sync with no lockfile committed; pyproject admits a range'
    if 'pip install mcp-proxy-for-aws' in L:
        p = pypi_at('mcp-proxy-for-aws', b['created'])
        return 'open range', f'mcp-proxy-for-aws {p["version"] if p else "?"} requires {p["requires_mcp"] if p else "?"}', 'pip install by name from PyPI, no version; mcp through fastmcp\'s range'
    if 'mcp-mesh==' in L:
        v = cfg_version or ''
        p = pypi_at('mcp-mesh', b['created'], v) if v else None
        req = p['requires_mcp'] if p else ''
        m = re.search(r'(?<![\w-])mcp(==[^ |,]+)', req)
        if m:
            return 'exact pin', f'mcp-mesh {v} requires mcp{m.group(1)}', 'pip install mcp-mesh==VERSION; the package pins mcp exactly'
        return 'open range', f'mcp-mesh {v} requires {req or "?"}', 'pip install mcp-mesh==VERSION; the package gives mcp a range'
    if 'pip install seclab-taskflow-agent' in L:
        p = pypi_at('seclab-taskflow-agent', b['created'])
        req = p['requires_mcp'] if p else ''
        m = re.search(r'(?<![\w-])mcp(==[^ |,]+)', req)
        return ('exact pin' if m else 'open range'), f'seclab-taskflow-agent {p["version"] if p else "?"} requires {req}', 'pip install by name from PyPI; the release current at the build pins mcp'
    sub = b['dockerfile'].rsplit('/', 1)[0] + '/' if b['dockerfile'].startswith('python/') else ''
    for pat, path in ((r'pip3? install -r requirements\.txt|uv pip install --system -r requirements\.txt', 'requirements.txt'),
                      (r'uv pip install -r pyproject\.toml|pip3? install[^|]* \.( |$)|pip install --no-cache-dir \.|install -e \.', sub + 'pyproject.toml')):
        if re.search(pat, L):
            s = spec_of(b['manifest_specs'], path) or (spec_of(b['manifest_specs'], 'backend/requirements.txt') if 'requirements' in path else '')
            if img.endswith('aurapro-webui'):
                s = spec_of(b['manifest_specs'], 'backend/requirements.txt')
            if s.startswith('mcp=='):
                return 'exact pin', f'{path} {s}', 'installs from the project\'s own specifier, which names one version'
            if s:
                return 'open range', f'{path} {s}', 'installs from the project\'s own specifier, which admits a range; the lockfile is not used'
            return 'unknown', '', f'installs from {path}, which names no mcp at this commit'
    return 'unknown', '', 'the install lines read do not show how mcp is chosen'


def main():
    mcp = {(r['image'], r['index_digest']): r for r in read_csv('image_mcp.csv')}
    builds = {(r['image'], r['index_digest']): r for r in read_csv('image_builds.csv')}
    imgs = {(r['image'], r['index_digest']): r for r in read_csv('images.csv')}
    plan = {(r['image'], r['index_digest']): r for r in read_csv('layer_plan.csv')}
    pkg = {i: p for i, p, _ in sampled()}
    rows = []
    for c in read_csv('image_configs.csv'):
        k = (c['image'], c['index_digest'])
        b, m, im, pl = builds[k], mcp.get(k, {}), imgs[k], plan.get(k, {})
        inst = m.get('mcp_installed', '')
        if m.get('method', '').startswith('dist-info'):
            reading = 'installed mcp read'
        elif 'layers not read' in m.get('method', ''):
            reading = 'layers not read (byte cap)'
        elif 'byte cap' in m.get('method', ''):
            reading = 'not determined (byte cap during read)'
        else:
            reading = 'no mcp in layers read'
        own = m.get('own_installed', '') or c['label_version']
        tagver = max((t.lstrip('v') for t in im['tags'].split() if re.fullmatch(r'v?\d+\.\d+\.\d+', t)), key=len, default='')
        cls, fixes, basis = classify(c['image'], dict(b, created=c['created']), (m.get('own_installed') or c['label_version'] or tagver).lstrip('v'))
        lock = b['uv_lock_mcp'].split('=')[-1] if b['uv_lock_mcp'] else ''
        if not inst:
            agree = ''
        elif cls == 'lockfile':
            agree = 'agrees' if inst == lock else f'differs: lock {lock or "none found"}'
        elif cls == 'exact pin':
            pin = re.search(r'(?<![\w-])mcp==([^ |,;]+)', fixes)
            agree = 'agrees' if pin and pin.group(1) == inst else f'differs: pin {pin.group(1) if pin else "?"}'
        elif cls == 'open range':
            agree = ('project lock ' + lock + (' agrees' if lock == inst else ' differs')) if lock else 'no project lock'
        else:
            agree = ''
        d = days(c['created']) if c['created'] else None
        rows.append(dict(image=c['image'], package=pkg.get(c['image'], ''), tags=im['tags'][:80], created=c['created'],
                         days_since_release=round(d, 2) if d is not None else '',
                         position=im['position'], plan_reason=pl.get('reason', ''), own_version=own,
                         install_class=cls, what_fixes_mcp=fixes, class_basis=basis, commit=b['commit'],
                         commit_basis=b['commit_basis'], project_spec=b['manifest_specs'][:160], project_lock=b['uv_lock_mcp'],
                         reading=reading, mcp_installed=inst,
                         holds_new=('yes' if inst.startswith('1.28.') else 'no') if inst else '',
                         install_vs_project=agree))
    rows.sort(key=lambda r: (r['image'], r['created']))
    write_csv('image_timeline.csv', rows)

    def bin_of(d):
        if d is None or d == '':
            return ''
        if d < -28:
            return 'a before period'
        if d < 0:
            return 'b 28 days before'
        for hi, lab in ((7, 'c 0 to 7'), (14, 'd 7 to 14'), (21, 'e 14 to 21'), (28, 'f 21 to 28')):
            if d < hi:
                return lab
        return 'g after period'
    agg = collections.defaultdict(lambda: [0, 0, set()])
    for r in rows:
        if r['holds_new'] == '':
            continue
        k = (r['install_class'], bin_of(r['days_since_release']))
        agg[k][0] += 1
        agg[k][1] += r['holds_new'] == 'yes'
        agg[k][2].add(r['image'].split('/')[-1])
    out = [dict(install_class=c, days_bin=b[2:], images_read=v[0], holding_new=v[1], repositories=len(v[2]),
                which=' '.join(sorted(v[2]))) for (c, b), v in sorted(agg.items(), key=lambda kv: (kv[0][0], kv[0][1]))]
    write_csv('share_by_class.csv', out)
    for o in out:
        print(o['install_class'][:10].ljust(10), o['days_bin'].ljust(16), o['holding_new'], '/', o['images_read'], o['which'])

    pins = collections.defaultdict(list)
    for g in read_csv('project_mcp_pins_git.csv'):
        pins[g['repo']].append(g)
    from collect_builds import REPO
    first = []
    for img in sorted({r['image'] for r in rows}):
        rs = [r for r in rows if r['image'] == img and r['holds_new']]
        after = [r for r in rs if r['holds_new'] == 'yes']
        before = [r for r in rs if r['holds_new'] == 'no' and (not after or r['created'] < after[0]['created'])]
        repo = REPO.get(img, ('', ''))[0]
        gp = [g for g in pins[repo] if re.search(r'1\.28\.', g['mcp']) and not g['mcp'].startswith('<')]
        g0 = min(gp, key=lambda g: g['committed_utc']) if gp else None
        classes = sorted({r['install_class'] for r in rows if r['image'] == img})
        g0utc = datetime.datetime.fromisoformat(g0['committed_utc']).astimezone(datetime.timezone.utc).strftime(FMT) if g0 else ''
        first.append(dict(image=img, install_classes=' / '.join(classes), images_with_result=len(rs),
                          last_without=f"{before[-1]['tags'][:30]} {before[-1]['created']} {before[-1]['mcp_installed']}" if before else '',
                          first_with=f"{after[0]['tags'][:30]} {after[0]['created']} {after[0]['mcp_installed']}" if after else '',
                          first_with_days=after[0]['days_since_release'] if after else '',
                          project_first_128=f"{g0['commit']} {g0utc} {g0['file']} {g0['mcp']}" if g0 else 'none found 1 Apr to 15 Aug',
                          project_first_128_days=round(days(g0utc), 2) if g0 else '',
                          image_minus_project_days=round(after[0]['days_since_release'] - days(g0utc), 2) if after and g0 else ''))
    write_csv('first_new.csv', first)
    dis = [r for r in rows if 'differs' in r['install_vs_project']]
    write_csv('disagreements.csv', dis, ['image', 'tags', 'created', 'days_since_release', 'install_class', 'what_fixes_mcp',
                                         'mcp_installed', 'project_spec', 'project_lock', 'install_vs_project'])
    print('images', len(rows), 'with installed mcp', sum(1 for r in rows if r['mcp_installed']), 'disagreements', len(dis))


if __name__ == '__main__':
    main()
