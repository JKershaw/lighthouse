#!/usr/bin/env python3
"""LH006: derived tables. No network access.
data/image_timeline.csv: every image whose layers were read, with its build time, the installed mcp,
  the project's own requirement and lock at that time (git) and the requirement of the matching PyPI
  release, and LH005's share of 1.27.0 in mcp's downloads on the build day where LH005 holds it.
data/first_1_27_0.csv: per image repository, the last image read before 1.27.0 appeared and the first
  with it, against the project's git pin and PyPI requirement.
data/moving_tags.csv: tags that move, and whether their current digest is kept under another tag."""
import collections, csv, datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, STUDY

RELEASE = '2026-04-02T14:48:07Z'
LH005 = os.path.join(os.path.dirname(os.path.dirname(STUDY)), 'studies', 'LH005', 'data', 'mcp_daily_by_version_share.csv')
MOVING = {'latest', 'stable', 'staging', 'main', 'dev'}


def ts(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))


def days(a, b):
    return round((ts(a) - ts(b)).total_seconds() / 86400, 1)


def utc(s):
    return ts(s).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def main():
    imgs = {(r['image'], r['index_digest']): r for r in read_csv('images.csv')}
    res = read_csv('image_mcp.csv')
    pins = read_csv('project_mcp_pins_git.csv')
    pypi = read_csv('project_mcp_pins_pypi.csv')
    share = {r['date']: r['share_1.27.0'] for r in csv.DictReader(open(LH005))}
    configs = {}
    if os.path.exists(os.path.join(STUDY, 'data', 'image_configs.csv')):
        configs = {(r['image'], r['index_digest']): r for r in read_csv('image_configs.csv')}
    rows = []
    lr = read_csv('layer_reads.csv')
    for r in res:
        if r['method'].startswith('not read'):
            continue
        im = imgs[(r['image'], r['index_digest'])]
        mine = [x for x in lr if (x['image'], x['index_digest']) == (r['image'], r['index_digest'])]
        if r['mcp_installed']:
            reading = 'mcp dist-info found'
        elif mine and all(x['ended'] == 'layer end' for x in mine) and 'byte cap' not in r['method']:
            reading = 'no mcp dist-info in any layer read (all non-base layers read to the end)'
        elif sum(int(x['bytes_read'] or 0) for x in mine) == 0:
            reading = 'configuration read; layers not read (byte cap)'
        else:
            reading = 'not determined: byte cap reached before mcp was seen'
        cf = configs.get((r['image'], r['index_digest']), {})
        created = im.get('created') or cf.get('created', '')
        pushed = im.get('first_pushed', '')
        t = created or pushed
        pkg = im['package']
        state = {}
        for p in pins:
            if p['package'] == pkg and utc(p['committed_utc']) <= t:
                state[p['kind']] = p['mcp']
        ver = [x for x in im['tags'].split() if x[:1].isdigit() or (x[:1] == 'v' and x[1:2].isdigit())]
        ver = sorted({v.lstrip('v') for v in ver if '-' not in v}, key=lambda v: -v.count('.'))
        pv = [p for p in pypi if p['package'] == pkg and ver and p['version'] == ver[0]]
        rows.append(dict(image=r['image'], package=pkg, tags=im['tags'], position=im['position'],
                         pushed_utc=pushed, created_utc=created, label_revision=im.get('label_revision') or cf.get('label_revision', ''),
                         days_from_release=days(t, RELEASE) if t else '',
                         mcp_installed=r['mcp_installed'], reading=reading,
                         git_requirement_at_build=state.get('requirement', ''), git_lock_at_build=state.get('lock', ''),
                         pypi_release=ver[0] if pv else '', pypi_requires=pv[0]['requires_mcp'] if pv else '',
                         push_minus_created_min=round((ts(pushed) - ts(created)).total_seconds() / 60, 1) if pushed and created else '',
                         lh005_share_1_27_0_on_build_day=share.get(t[:10], '')))
    rows.sort(key=lambda r: (r['image'], r['created_utc'] or r['pushed_utc']))
    write_csv('image_timeline.csv', rows)
    first = []
    by = collections.defaultdict(list)
    for r in rows:
        if r['mcp_installed']:
            by[r['image']].append(r)
    for img, rs in by.items():
        f = [r for r in rs if r['mcp_installed'] == '1.27.0']
        b = [r for r in rs if r['mcp_installed'] != '1.27.0' and (not f or (r['created_utc'] or r['pushed_utc']) < (f[0]['created_utc'] or f[0]['pushed_utc']))]
        pkg = rs[0]['package']
        pin_move = [p for p in pins if p['package'] == pkg and p['mcp'] in ('==1.27.0', '1.27.0')]
        req_move = [p for p in pypi if p['package'] == pkg and '1.27.0' in p['requires_mcp']]
        t1 = (f[0]['created_utc'] or f[0]['pushed_utc']) if f else ''
        first.append(dict(image=img, package=pkg,
                          last_read_without=f"{b[-1]['tags'].split()[0]} {b[-1]['created_utc'] or b[-1]['pushed_utc']} mcp {b[-1]['mcp_installed']}" if b else '',
                          first_read_with=f"{f[0]['tags'].split()[0]} {t1}" if f else 'none read',
                          days_from_release=days(t1, RELEASE) if f else '',
                          git_first_1_27_0=utc(pin_move[0]['committed_utc']) + f" ({pin_move[0]['file']} {pin_move[0]['mcp']})" if pin_move else 'none in span read',
                          image_minus_git_days=days(t1, utc(pin_move[0]['committed_utc'])) if f and pin_move else '',
                          pypi_first_requiring_1_27_0=f"{req_move[0]['version']} {req_move[0]['published_utc'][:19]}Z ({req_move[0]['requires_mcp']})" if req_move else 'none in span read'))
    write_csv('first_1_27_0.csv', first)
    mv = []
    hub = read_csv('tags_hub.csv')
    dig = collections.defaultdict(list)
    for t in hub:
        dig[(t['image'], t['digest'])].append(t['tag'])
    for t in hub:
        if t['tag'] in MOVING or t['tag'].endswith(('-latest', '-stable', '-staging')):
            others = [x for x in dig[(t['image'], t['digest'])] if x != t['tag']]
            mv.append(dict(image=t['image'], tag=t['tag'], last_pushed=t['last_pushed'][:19] + 'Z',
                           current_digest_also_tagged_as=' '.join(others[:3]) or 'no other tag'))
    for r in read_csv('images.csv'):
        if r['image'].startswith('ghcr.io/') and r['tags']:
            for tg in r['tags'].split():
                if tg in MOVING:
                    others = [x for x in r['tags'].split() if x != tg]
                    mv.append(dict(image=r['image'], tag=tg, last_pushed='(created ' + r['created'] + ')',
                                   current_digest_also_tagged_as=' '.join(others) or 'no other tag'))
    write_csv('moving_tags.csv', mv)
    # agentcrew: versions tagged both X and vX, and whether the two point at different images
    pairs = []
    ac = {t['tag']: t for t in hub if t['image'] == 'docker.io/daltonnyx/agentcrew'}
    for tag, t in ac.items():
        if tag[:1].isdigit() and '-' not in tag and 'v' + tag in ac:
            v = ac['v' + tag]
            pairs.append(dict(version=tag, plain_digest=t['digest'][:19], plain_pushed=t['last_pushed'][:19] + 'Z',
                              plain_platforms=len(__import__('json').loads(t['images'])),
                              v_digest=v['digest'][:19], v_pushed=v['last_pushed'][:19] + 'Z',
                              v_platforms=len(__import__('json').loads(v['images'])),
                              same_image='yes' if t['digest'] == v['digest'] else 'no',
                              hours_apart=round((ts(v['last_pushed']) - ts(t['last_pushed'])).total_seconds() / 3600, 1)))
    pairs.sort(key=lambda r: r['plain_pushed'])
    write_csv('agentcrew_version_tag_pairs.csv', pairs)
    # keboola: commits built as both canary-orion-<sha> and production-<sha> with different digests,
    # and which of the two the sha-<sha> tag points at now
    kb = collections.defaultdict(dict)
    for t in hub:
        if t['image'] == 'docker.io/keboola/mcp-server':
            for pre in ('canary-orion-', 'production-', 'sha-'):
                if t['tag'].startswith(pre):
                    kb[t['tag'][len(pre):]][pre] = (t['digest'], t['last_pushed'][:19] + 'Z')
    dbl = []
    for sha, v in kb.items():
        if 'canary-orion-' in v and 'production-' in v and v['canary-orion-'][0] != v['production-'][0]:
            later = max(('canary-orion-', 'production-'), key=lambda p: v[p][1])
            dbl.append(dict(commit=sha[:12], canary_pushed=v['canary-orion-'][1], production_pushed=v['production-'][1],
                            sha_tag_points_at=('the later build (' + later.rstrip('-') + ')') if v.get('sha-', ('',))[0] == v[later][0]
                            else ('no sha tag' if 'sha-' not in v else 'the earlier build')))
    dbl.sort(key=lambda r: r['canary_pushed'])
    write_csv('keboola_double_builds.csv', dbl)
    print('keboola double builds', len(dbl), collections.Counter(r['sha_tag_points_at'][:16] for r in dbl))
    lr = read_csv('layer_reads.csv')
    tot = collections.Counter()
    for r in lr:
        tot[r['image']] += int(r['bytes_read'] or 0)
    print('bytes read', dict(tot), sum(tot.values()))
    print('agentcrew pairs', len(pairs), collections.Counter(p['same_image'] for p in pairs))
    for f in first:
        print(f)


if __name__ == '__main__':
    main()
