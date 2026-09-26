#!/usr/bin/env python3
"""LH007 step 3c: which images have their layers read, in what order (brief.md, 'Readings' point 2).
Per repository, at most 10 images: tier 1 the last image before the release and the first after it;
tier 2 the first and last in the period; tier 3 the images nearest to days +7, +14, +21 and -14;
tier 4 the nearest image outside the period on each side. Tier 5 (bisection) is added by
plan_bisect() after the first reads. Docker Hub images are ordered by (tier, sample rank), so the
counted budget is spread across repositories; other registries in the same order without a budget.
Writes data/layer_plan.csv. No network access."""
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, DATA
from collect_images import RELEASE, P0, P1, sampled

FMT = '%Y-%m-%dT%H:%M:%SZ'
rel = datetime.datetime.strptime(RELEASE, FMT)


def t(r):
    return r['first_pushed'] if r['image'].startswith('docker.io/') else r.get('created', '')


def days(s):
    return (datetime.datetime.strptime(s, FMT) - rel).total_seconds() / 86400


def plan():
    imgs = read_csv('images.csv')
    rank = {img: k for img, _, k in sampled()}
    out = []
    for img in rank:
        rows = sorted([r for r in imgs if r['image'] == img and t(r) and r['position'] not in ('not readable',)], key=t)
        inside = [r for r in rows if P0 <= t(r) <= P1]
        pick = {}

        def add(r, tier, why):
            if r is not None and r['index_digest'] not in pick:
                pick[r['index_digest']] = (tier, why, r)
        before = [r for r in inside if t(r) < RELEASE]
        after = [r for r in inside if t(r) >= RELEASE]
        add(before[-1] if before else None, 1, 'last before release')
        add(after[0] if after else None, 1, 'first after release')
        add(inside[0] if inside else None, 2, 'first in period')
        add(inside[-1] if inside else None, 2, 'last in period')
        for d in (7, 14, 21, -14):
            if inside:
                add(min(inside, key=lambda r: abs(days(t(r)) - d)), 3, f'nearest to day {d:+d}')
        outb = [r for r in rows if t(r) < P0][-1:]
        outa = [r for r in rows if t(r) > P1][:1]
        add(outb[0] if outb else None, 4, 'nearest before period')
        add(outa[0] if outa else None, 4, 'nearest after period')
        for dig, (tier, why, r) in pick.items():
            out.append(dict(image=img, sample_rank=rank[img], tier=tier, reason=why, index_digest=dig, tags=r['tags'][:120],
                            time=t(r), days_since_release=round(days(t(r)), 2), position=r['position']))
    out.sort(key=lambda o: (0 if not o['image'].startswith('docker.io/') else 1, o['tier'], o['sample_rank'], o['time']))
    for i, o in enumerate(out, 1):
        o['order'] = i
    write_csv('layer_plan.csv', out, ['order', 'image', 'sample_rank', 'tier', 'reason', 'index_digest', 'tags', 'time',
                                      'days_since_release', 'position'])
    import collections
    print(collections.Counter((o['image'].split('/')[0], o['tier']) for o in out))


if __name__ == '__main__':
    plan()
