#!/usr/bin/env python3
"""Which hosts that the live collectors read would refuse keeping a body today (the keeper, 21 November 2026)?

Takes every literal URL in each live study's collector scripts, panel and URL lists, and in the read logs of
the two latest data folders of each kind, and asks scripts/robots_gate.py's RobotsGate(UA).may_keep(url) (recurring
rule; one robots.txt GET per host, nothing else). Written for collectors_wired.md.
Usage, from the repository root: LIGHTHOUSE_PROVIDER=anthropic python3 -I notes/keeper/robots-intent-2026-11-21/live_hosts_survey.py OUT.json
"""
import glob, json, os, re, sys
from collections import defaultdict
from urllib.parse import urlsplit

sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
import robots_gate  # noqa: E402

UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
LIVE = ['LH030', 'LH031', 'LH032', 'LH033', 'LH034', 'LH036', 'LH037', 'LH040', 'LH041', 'LH042', 'LH044', 'LH045',
        'LH046', 'LH047', 'LH048', 'LH049', 'LH050', 'LH051', 'LH053', 'LH054', 'LH055', 'LH056', 'LH058']
URL = re.compile(r'https?://[^\s"\'<>`\\),\]]+')


def urls_for(s):
    files = glob.glob('studies/%s/scripts/*.py' % s) + glob.glob('studies/%s/*.json' % s) + \
        glob.glob('studies/%s/scripts/*.txt' % s) + glob.glob('studies/%s/scripts/*.json' % s)
    by_prefix = defaultdict(list)  # the two latest folders of each kind (read-, vendor-, wayback-, ...)
    for d in sorted(glob.glob('studies/%s/data/*/' % s)):
        by_prefix[re.split(r'\d', os.path.basename(d.rstrip('/')), maxsplit=1)[0]].append(d)
    dirs = [d for ds in by_prefix.values() for d in ds[-2:]]
    for d in dirs:
        files += [f for f in glob.glob(d + '**/*', recursive=True) if 'log' in os.path.basename(f).lower()
                  and f.endswith(('.csv', '.json', '.jsonl'))]
    out = set()
    for f in files:
        try:
            t = open(f, errors='replace').read()
        except OSError:
            continue
        for u in URL.findall(t):
            u = u.rstrip('.;:')
            if '{' in u or '%s' in u or u.endswith('/robots.txt') or 'lighthouse.harbour.cat' in u:
                continue
            p = urlsplit(u)
            if p.hostname and '.' in p.hostname:
                out.add(u)
    return out


def main():
    gate = robots_gate.RobotsGate(UA)
    res = defaultdict(dict)
    for s in LIVE:
        by_host = defaultdict(list)
        for u in sorted(urls_for(s)):
            by_host[urlsplit(u).hostname].append(u)
        for host, us in sorted(by_host.items()):
            refused = []
            for u in us[:40]:
                keep, why = gate.may_keep(u)
                if not keep:
                    refused.append((u, why))
            res[s][host] = {'urls': len(us), 'refused': refused[:5], 'n_refused_of_checked': [len(refused), min(len(us), 40)]}
    json.dump({'studies': res, 'robots': {k: {'status': v.get('status'), 'sha256': v.get('sha256'), 'error': v.get('error')}
                                          for k, v in gate.cache.items()}}, open(sys.argv[1], 'w'), indent=1)
    for s, hosts in res.items():
        bad = {h: v['n_refused_of_checked'] for h, v in hosts.items() if v['refused']}
        print(s, len(hosts), 'hosts; refusing keep:', bad)


if __name__ == '__main__':
    main()
