#!/usr/bin/env python3
"""LH014: the frame, offline. No network. Python 3 with the `packaging` library (PEP 440; 24.0 used).

  python3 frame.py --list   from data/clickpy_month_2026_08.csv (the ranking read in phase 2) writes
                            data/frame.csv and data/frame_checks.csv
  python3 frame.py          from data/frame.csv, pypi_walk.csv, pypi_versions.csv and, when present,
                            installer_names.csv, writes data/drawn.csv, releases.csv,
                            releases_first_excluded.csv, project_order.csv, overlap.csv,
                            mirror_installers.csv and ranking_comparison.csv
Both write under $LH014_OUT when it is set (the replay's temporary directory). Nothing here prints or
writes a monthly sum: the sums enter only as the order of the list, and the comparison with the
rankings earlier studies kept reports agreement, not values.

Rules, from the brief (snapshot 31c19166..., commit 353f17f), Population and unit and choices 1 to 8:
- Positions are counted over the list after LH011's packaging and installer tooling (17 names) is
  removed. LH011's 50 (studies/LH011/data/project_order.csv, which carries no count) are positions 1 to
  50 by construction and are removed by name wherever they fall; names are compared after PEP 503
  normalisation. Band A is positions 51 to 500, band B 501 to 5,000. A tie in the August sum across
  50/51, 500/501 or 5,000/5,001 is recorded; the list's own order (the sum descending, then the name
  ascending in byte order) decides.
- The draw order within a band is the ascending lowercase hexadecimal SHA-256 of the UTF-8 bytes of
  'LH014-20260929:' followed by the name as ClickPy stores it. The drawn projects are the first 80 in
  that order that PyPI served (data/pypi_walk.csv, written by collect_frame.py).
- Releases: LH011's rule as its frame.py applies it (not a pre-release or development release by PEP
  440; versions with no file or no parse take no part; first upload from 2026-04-01T00:00:00Z to
  2026-08-31T23:59:59Z; then higher than every earlier-uploaded non-pre-release version), less a
  project's first non-pre-release version, which replaces nothing (choice 4) and is written to
  releases_first_excluded.csv. The CI subsample is each project's first qualifying release in each
  calendar month. The reading order alternates between the bands in draw order (choice 5).
- The mirror class: installer names equal, ignoring case, to bandersnatch, z3c.pypimirror, Artifactory
  or devpi; a name that only contains one is listed and left out (choice 8).

Adapted from studies/LH011/scripts/frame.py. What changed: two bands drawn by salted hash from a ranked
list rather than the top 50; LH011's 50 and the tooling removed by PEP 503 name; the first-release
exclusion; the alternating reading order; the overlap flags, the mirror class and the comparison with
earlier rankings are new. The release columns are LH011's, with the band added."""
import csv, glob, hashlib, os, re, sys
from datetime import datetime
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
ROOT = os.path.dirname(os.path.dirname(STUDY))
OUT = os.environ.get('LH014_OUT', DATA)
SALT = 'LH014-20260929:'
START, END = '2026-04-01T00:00:00', '2026-08-31T23:59:59'
PER_BAND = 80
TOOLING = ['pip', 'setuptools', 'wheel', 'uv', 'virtualenv', 'pipenv', 'pipx', 'poetry', 'poetry-core', 'pdm',
           'pdm-backend', 'hatchling', 'flit-core', 'build', 'setuptools-scm', 'scikit-build-core', 'maturin']
MIRRORS = ['bandersnatch', 'z3c.pypimirror', 'artifactory', 'devpi']


def norm(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def rd(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def wr(name, rows, fields):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def draw_key(name):
    return hashlib.sha256((SALT + name).encode('utf-8')).hexdigest()


def lh011_50():
    return [r['project'] for r in rd(os.path.join(ROOT, 'studies', 'LH011', 'data', 'project_order.csv'))]


def ranking():
    """The phase 2 list in the brief's order (sum descending, name ascending in bytes), and whether the
    file as read was already in that order."""
    rows = rd(os.path.join(DATA, 'clickpy_month_2026_08.csv'))
    ordered = sorted(rows, key=lambda r: (-int(r['downloads']), r['project'].encode('utf-8')))
    return ordered, [r['project'] for r in ordered] == [r['project'] for r in rows]


def build_list():
    rows, order_ok = ranking()
    tool, l50 = {norm(t) for t in TOOLING}, {norm(p) for p in lh011_50()}
    out, natural, pos, k50 = [], 0, 50, 0
    for i, r in enumerate(rows, 1):
        n = norm(r['project'])
        rec = dict(raw_rank=i, project=r['project'], pep503=n)
        if n in tool:
            rec['status'] = 'removed: tooling'
        else:
            natural += 1
            rec['natural_position'] = natural
            if n in l50:
                k50 += 1
                rec.update(status="LH011's 50", position=k50)
            else:
                pos += 1
                band = 'A' if pos <= 500 else 'B' if pos <= 5000 else ''
                rec.update(status=('band ' + band) if band else 'beyond position 5,000', position=pos, band=band)
        out.append(rec)
    return rows, out, order_ok


def list_checks(rows, out, order_ok):
    sums = {r['project']: int(r['downloads']) for r in rows}
    by_pos = {int(r['position']): r['project'] for r in out if r.get('position', '') != ''}
    l50 = {norm(p) for p in lh011_50()}
    checks = [dict(check='rows in the list', value=len(out)),
              dict(check='file already in the order sum descending, name ascending', value=order_ok)]
    tools = [r for r in out if r['status'] == 'removed: tooling']
    checks.append(dict(check='tooling removed', value=len(tools),
                       detail='; '.join(f"{r['project']} (raw rank {r['raw_rank']})" for r in tools)))
    found50 = [r for r in out if r['status'] == "LH011's 50"]
    missing = sorted(l50 - {r['pep503'] for r in found50})
    checks.append(dict(check="LH011's 50 found in the list", value=len(found50), detail='missing: ' + ', '.join(missing) if missing else ''))
    disp_out = [r for r in found50 if int(r['natural_position']) > 50]
    disp_in = [r for r in out if r['status'] not in ("LH011's 50", 'removed: tooling') and int(r['natural_position']) <= 50]
    checks.append(dict(check="LH011's 50 displaced below position 50", value=len(disp_out),
                       detail='; '.join(f"{r['project']} (would be {r['natural_position']})" for r in disp_out)))
    checks.append(dict(check='other projects that would have been within the first 50', value=len(disp_in),
                       detail='; '.join(f"{r['project']} (would be {r['natural_position']})" for r in disp_in)))
    for edge in (50, 500, 5000):
        a, b = by_pos.get(edge), by_pos.get(edge + 1)
        tie = a is not None and b is not None and sums[a] == sums[b]
        group = [p for p in by_pos.values() if a is not None and sums[p] == sums[a]] if tie else []
        checks.append(dict(check=f'tie in the August sum across positions {edge} and {edge + 1}', value=tie,
                           detail=(f'{a} | {b}' + ('; equal sums: ' + ', '.join(group) if tie else '')) if a and b else 'edge not in the list'))
    seen = {}
    for r in out:
        seen.setdefault(r['pep503'], []).append(r['project'])
    coll = {k: v for k, v in seen.items() if len(v) > 1}
    checks.append(dict(check='names that collide under PEP 503', value=len(coll),
                       detail='; '.join(' = '.join(v) for v in coll.values())))
    for b in ('A', 'B'):
        checks.append(dict(check=f'projects in band {b}', value=sum(1 for r in out if r.get('band') == b)))
    return checks


def band_orders(frame_rows):
    return {b: sorted((r['project'] for r in frame_rows if r['band'] == b), key=draw_key) for b in ('A', 'B')}


def drawn_list(frame_rows):
    walk = rd(os.path.join(DATA, 'pypi_walk.csv'))
    orders = band_orders(frame_rows)
    info = {r['project']: r for r in frame_rows}
    drawn = []
    for b in ('A', 'B'):
        ws = sorted((w for w in walk if w['band'] == b), key=lambda w: int(w['walk_order']))
        for w in ws:   # the walk must follow the band's draw order exactly
            assert orders[b][int(w['walk_order']) - 1] == w['project'], (b, w['walk_order'], w['project'])
        served = [w for w in ws if w['result'] == 'served'][:PER_BAND]
        for k, w in enumerate(served, 1):
            drawn.append(dict(band=b, draw_order=k, walk_order=w['walk_order'], project=w['project'],
                              position=info[w['project']]['position'], raw_rank=info[w['project']]['raw_rank'],
                              pypi_name=w['info_name'], pypi_name_matches=norm(w['info_name']) == norm(w['project']),
                              sha256=draw_key(w['project'])))
    return drawn


def kind(new, old):
    if new.epoch != old.epoch:
        return 'epoch'
    a, b = list(new.release), list(old.release)
    n = max(len(a), len(b))
    a += [0] * (n - len(a)); b += [0] * (n - len(b))
    for i in range(n):
        if a[i] != b[i]:
            return ['major', 'minor'][i] if i < 2 else 'patch'
    return 'post'


def releases_for(drawn, versions):
    f = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    out, excluded = [], []
    for d in drawn:
        p = d['project']
        vs = [r for r in versions if r['project'] == p and r['parse'] == 'ok' and r['is_prerelease'] == 'False']
        vs.sort(key=lambda r: (r['first_upload_utc'], Version(r['version'])))
        newest, chain = None, []   # versions that became the newest when uploaded, in upload order
        for r in vs:
            if newest is None or Version(r['version']) > Version(newest['version']):
                chain.append((r, newest))
                newest = r
        seen_month = set()
        for i, (r, prev) in enumerate(chain):
            t = r['first_upload_utc'][:19]
            if not (START <= t <= END):
                continue
            if prev is None:
                excluded.append(dict(band=d['band'], project=p, version=r['version'], first_upload_utc=r['first_upload_utc'],
                                     reason='first non-pre-release version; replaces nothing (brief, choice 4)'))
                continue
            nxt = chain[i + 1][0] if i + 1 < len(chain) else None
            gap_h = round((f(nxt['first_upload_utc']) - f(r['first_upload_utc'])).total_seconds() / 3600, 2) if nxt else ''
            day0 = f(r['first_upload_utc'])
            month = t[:7]
            ci = month not in seen_month
            seen_month.add(month)
            out.append(dict(band=d['band'], project=p, version=r['version'], first_upload_utc=r['first_upload_utc'], day0=t[:10],
                            hours_left_in_day0=round(24 - (day0.hour + day0.minute / 60 + day0.second / 3600), 2),
                            replaced_version=prev['version'], replaced_first_upload_utc=prev['first_upload_utc'],
                            kind=kind(Version(r['version']), Version(prev['version'])),
                            next_newest_version=nxt['version'] if nxt else '', hours_to_next_newest=gap_h,
                            released_again_within_7d=(gap_h != '' and gap_h <= 168), yanked=r['any_yanked'], ci_subsample=ci))
    return out, excluded


def main_list():
    rows, out, order_ok = build_list()
    wr('frame.csv', out, ['raw_rank', 'project', 'pep503', 'status', 'natural_position', 'position', 'band'])
    checks = list_checks(rows, out, order_ok)
    wr('frame_checks.csv', checks, ['check', 'value', 'detail'])
    for c in checks:
        print(f"{c['check']}: {c['value']}" + (f"  [{c['detail']}]" if c.get('detail') else ''))


def compare_rankings():
    """Agreement of the phase 2 list with the August rankings LH008, LH010 and LH011 kept: names and
    ranks, and how many sums are identical, never the sums."""
    cur, _ = ranking()
    cur_rank = {r['project']: i for i, r in enumerate(cur, 1)}
    cur_sum = {r['project']: int(r['downloads']) for r in cur}
    out = []
    for label, rel, rank_col in (('LH008 top 200, read 2026-09-27', 'studies/LH008/data/top200.csv', 'rank'),
                                 ('LH010 top 500, read 2026-09-27', 'studies/LH010/data/top500.csv', 'rank'),
                                 ('LH011 top 80, read 2026-09-28', 'studies/LH011/data/clickpy_top_projects_2026_08.csv', None)):
        old = rd(os.path.join(ROOT, rel))
        if rank_col:
            old.sort(key=lambda r: int(r[rank_col]))
        n = len(old)
        same_rank = sum(1 for i, r in enumerate(old, 1) if cur_rank.get(r['project']) == i)
        common = [r for r in old if r['project'] in cur_sum]
        identical = sum(1 for r in common if int(r['downloads']) == cur_sum[r['project']])
        rel_max = max((abs(cur_sum[r['project']] - int(r['downloads'])) / int(r['downloads']) for r in common), default=0)
        moved = [f"{r['project']} {i}->{cur_rank.get(r['project'], 'absent')}" for i, r in enumerate(old, 1) if cur_rank.get(r['project']) != i]
        out.append(dict(ranking=label, file=rel, rows=n, same_project_at_same_rank=same_rank,
                        same_set_as_first_n=({r['project'] for r in old} == {r['project'] for r in cur[:n]}),
                        in_phase2_list=len(common), identical_sums=identical, largest_relative_difference=f'{rel_max:.6f}',
                        moved='; '.join(moved)))
    return out


def main():
    frame_rows = rd(os.path.join(DATA, 'frame.csv'))
    drawn = drawn_list(frame_rows)
    versions = rd(os.path.join(DATA, 'pypi_versions.csv'))
    rel, excl = releases_for(drawn, versions)
    ov = {norm(r['project']): r['why'] for r in rd(os.path.join(DATA, 'overlap_projects.csv'))}
    deps = {norm(os.path.basename(x)[:-4]) for x in glob.glob(os.path.join(ROOT, 'studies', 'LH012', 'data', 'deps', 'versions', '*.csv'))}
    for d in drawn:
        mine = [r for r in rel if r['project'] == d['project']]
        d.update(n_releases=len(mine), n_ci_subsample=sum(1 for r in mine if r['ci_subsample']),
                 n_first_excluded=sum(1 for x in excl if x['project'] == d['project']),
                 in_overlap_set=norm(d['project']) in ov, lh012_dependent=norm(d['project']) in deps,
                 releases_day0_22_to_31_aug=sum(1 for r in mine if '2026-08-22' <= r['day0'] <= '2026-08-31'))
    wr('drawn.csv', drawn, ['band', 'draw_order', 'walk_order', 'project', 'position', 'raw_rank', 'pypi_name', 'pypi_name_matches',
                            'sha256', 'n_releases', 'n_ci_subsample', 'n_first_excluded', 'in_overlap_set', 'lh012_dependent',
                            'releases_day0_22_to_31_aug'])
    wr('releases.csv', rel, ['band', 'project', 'version', 'first_upload_utc', 'day0', 'hours_left_in_day0', 'replaced_version',
                             'replaced_first_upload_utc', 'kind', 'next_newest_version', 'hours_to_next_newest',
                             'released_again_within_7d', 'yanked', 'ci_subsample'])
    wr('releases_first_excluded.csv', excl, ['band', 'project', 'version', 'first_upload_utc', 'reason'])
    a = [d for d in drawn if d['band'] == 'A']
    b = [d for d in drawn if d['band'] == 'B']
    order = []
    for k in range(max(len(a), len(b))):
        for x in (a[k:k + 1] + b[k:k + 1]):
            order.append(dict(read_order=len(order) + 1, band=x['band'], draw_order=x['draw_order'], project=x['project'],
                              n_releases=x['n_releases'], n_ci_subsample=x['n_ci_subsample']))
    wr('project_order.csv', order, ['read_order', 'band', 'draw_order', 'project', 'n_releases', 'n_ci_subsample'])
    wr('overlap.csv', [dict(band=d['band'], project=d['project'], in_overlap_set=d['in_overlap_set'],
                            why=ov.get(norm(d['project']), ''), lh012_dependent=d['lh012_dependent'],
                            releases_day0_22_to_31_aug=d['releases_day0_22_to_31_aug'])
                       for d in drawn if d['in_overlap_set'] or d['lh012_dependent']],
       ['band', 'project', 'in_overlap_set', 'why', 'lh012_dependent', 'releases_day0_22_to_31_aug'])
    if os.path.exists(os.path.join(DATA, 'installer_names.csv')):
        rows = []
        for r in rd(os.path.join(DATA, 'installer_names.csv')):
            low = r['installer'].lower()
            cls = 'mirror' if low in MIRRORS else 'listed, left out' if any(m in low for m in MIRRORS) else ''
            rows.append(dict(installer=r['installer'], mirror_class=cls))
        wr('mirror_installers.csv', rows, ['installer', 'mirror_class'])
    wr('ranking_comparison.csv', compare_rankings(), ['ranking', 'file', 'rows', 'same_project_at_same_rank', 'same_set_as_first_n',
                                                      'in_phase2_list', 'identical_sums', 'largest_relative_difference', 'moved'])
    for band, ds in (('A', a), ('B', b)):
        rs = [r for r in rel if r['band'] == band]
        print(f'band {band}: drawn {len(ds)}; with a qualifying release {sum(1 for d in ds if d["n_releases"])}; '
              f'releases {len(rs)}; first releases excluded {sum(1 for x in excl if x["band"] == band)}; '
              f'CI subsample {sum(1 for r in rs if r["ci_subsample"])}; in overlap set {sum(1 for d in ds if d["in_overlap_set"])}; '
              f'LH012 dependents {sum(1 for d in ds if d["lh012_dependent"])}')


if __name__ == '__main__':
    main_list() if '--list' in sys.argv else main()
