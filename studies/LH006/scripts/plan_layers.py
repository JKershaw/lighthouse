#!/usr/bin/env python3
"""LH006: the layer-reading plan (brief.md, amendment point 2). Tier 1 and 2 images per Docker Hub
repository by rule; ghcr.io images in time order. Tier 3 (bisection) rows are added by
plan_layers.py bisect after reading tiers 1 and 2. Writes data/layer_plan.csv. No network access."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, DATA

RELEASE, W1 = '2026-04-02T14:48:07Z', '2026-04-22T23:59:59Z'


def main(stage):
    imgs = [r for r in read_csv('images.csv') if r['position'] not in ('outside period', 'outside period (not read)', 'not readable')]
    by = collections.defaultdict(list)
    for r in imgs:
        r['t'] = r['first_pushed'] or r['created']
        by[r['image']].append(r)
    plan = read_csv('layer_plan.csv') if stage == 'bisect' else []
    have = {(p['image'], p['index_digest']) for p in plan}
    if stage == 'initial':
        for img, rs in by.items():
            rs.sort(key=lambda r: r['t'])
            if img.startswith('ghcr.io/'):
                for r in rs:
                    plan.append(dict(image=img, index_digest=r['index_digest'], tags=r['tags'], time=r['t'], tier=1, reason='ghcr.io: all images in scope, time order'))
                continue
            inside = [r for r in rs if r['position'].startswith('in ')]
            pick = []
            b = [r for r in inside if r['t'] < RELEASE]
            a = [r for r in inside if r['t'] >= RELEASE]
            w = [r for r in inside if r['t'] <= W1]
            if b: pick.append((b[-1], 1, 'last pushed before the release'))
            if a: pick.append((a[0], 1, 'first pushed after the release'))
            if w: pick.append((w[-1], 1, 'last pushed in the window'))
            if inside: pick.append((inside[-1], 1, 'last pushed in the period'))
            for r in rs:
                if r['position'] == 'nearest before period': pick.append((r, 2, 'nearest before the period'))
                if r['position'] == 'nearest after period': pick.append((r, 2, 'nearest after the period'))
            if inside: pick.append((inside[0], 2, 'first pushed in the period'))
            for r, tier, why in pick:
                k = (img, r['index_digest'])
                if k in have:
                    for p in plan:
                        if (p['image'], p['index_digest']) == k: p['reason'] += '; ' + why
                    continue
                have.add(k)
                plan.append(dict(image=img, index_digest=r['index_digest'], tags=r['tags'], time=r['t'], tier=tier, reason=why))
        plan.sort(key=lambda p: (int(p['tier']), not p['image'].startswith('ghcr.io/'), p['time']))
    else:  # bisect: between consecutive read images of one repository whose mcp versions differ
        res = {(r['image'], r['index_digest']): r['mcp_installed'] for r in read_csv('image_mcp.csv') if r['method'].startswith(('dist-info', 'not found', 'lockfile'))}
        for img, rs in by.items():
            if img.startswith('ghcr.io/'):
                continue
            rs.sort(key=lambda r: r['t'])
            read_idx = [i for i, r in enumerate(rs) if (img, r['index_digest']) in res]
            for i, j in zip(read_idx, read_idx[1:]):
                if res[(img, rs[i]['index_digest'])] != res[(img, rs[j]['index_digest'])] and j - i > 1:
                    m = rs[(i + j) // 2]
                    if (img, m['index_digest']) not in have:
                        have.add((img, m['index_digest']))
                        plan.append(dict(image=img, index_digest=m['index_digest'], tags=m['tags'], time=m['t'], tier=3,
                                         reason=f"midway between {rs[i]['tags'].split()[0]} and {rs[j]['tags'].split()[0]}, whose mcp differ"))
    write_csv('layer_plan.csv', plan, ['image', 'index_digest', 'tags', 'time', 'tier', 'reason'])
    print(collections.Counter((p['image'], p['tier']) for p in plan))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'initial')
