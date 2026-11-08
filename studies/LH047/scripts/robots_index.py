"""LH047: index every robots.txt copy retained by the audited studies on 8 November 2026, and
the current copies LH047 re-read (data/reads/robots-current/). Offline.

Usage (from the repository root):
  python3 -I studies/LH047/scripts/robots_index.py           write data/robots-index.csv
  python3 -I studies/LH047/scripts/robots_index.py --missing print scheme://host of audited
                                                             requests with no retained copy
Columns: authority (scheme://host[:port]), utc, study, status, file, truncated, source_log.
"""
import csv, os, sys
from urllib.parse import urlsplit

ROOT = os.getcwd()
D = os.path.join(ROOT, 'studies/LH047/data')


def auth(url):
    u = urlsplit(url)
    return '%s://%s' % (u.scheme, u.netloc)


def entries():
    out = []
    # LH043
    for line in open('studies/LH043/data/fetch-log.tsv'):
        t = line.rstrip('\n').split('\t')
        if t[2].endswith('/robots.txt'):
            out.append(dict(authority=auth(t[2]), utc=t[0], study='LH043', status=t[1],
                            file='studies/LH043/data/sources/' + t[3], truncated='False', source_log='studies/LH043/data/fetch-log.tsv'))
    # LH044 (read, statements, httparchive, wayback): NNNN.b bodies, first 64 KiB
    for sub in ('read-2026-11-08T1920Z', 'statements-2026-11-08T1920Z', 'httparchive-2026-11-08T1920Z', 'wayback-2026-11-08T1920Z'):
        log = 'studies/LH044/data/%s/readlog.csv' % sub
        for r in csv.DictReader(open(log, newline='')):
            if r['kind'].startswith('robots'):
                out.append(dict(authority=auth(r['url']), utc=r['utc'], study='LH044', status=r['status'] or ('error:' + r['error']),
                                file='studies/LH044/data/%s/%04d.b' % (sub, int(r['n'])), truncated=r['truncated'], source_log=log))
    # LH045
    log = 'studies/LH045/data/before-the-brief/readlog.csv'
    for r in csv.DictReader(open(log, newline='')):
        if r['url'].endswith('/robots.txt'):
            out.append(dict(authority=auth(r['url']), utc=r['utc_start'], study='LH045', status=r['status'],
                            file='studies/LH045/data/before-the-brief/%s.raw' % r['name'], truncated='False', source_log=log))
    log = 'studies/LH045/data/epoch/raw-2026-11-08T1913Z/readlog.csv'
    for r in csv.DictReader(open(log, newline='')):
        if r['url'].endswith('/robots.txt'):
            out.append(dict(authority=auth(r['url']), utc=r['utc_start'], study='LH045', status=r['status'],
                            file='studies/LH045/data/epoch/raw-2026-11-08T1913Z/robots.body', truncated='False', source_log=log))
    for sub in ('raw-2026-11-08T1914Z', 'raw-2026-11-08T1915Z'):
        log = 'studies/LH045/data/ietf/%s/readlog.csv' % sub
        for r in csv.DictReader(open(log, newline='')):
            if r['url'].endswith('/robots.txt'):
                out.append(dict(authority=auth(r['url']), utc=r['utc_start'], study='LH045', status=r['status'],
                                file='studies/LH045/data/ietf/%s/%s' % (sub, r['file']), truncated='False', source_log=log))
    # LH046
    log = 'studies/LH046/data/sources/fetch-log.tsv'
    for line in open(log):
        t = line.rstrip('\n').split('\t')
        if t[4].endswith('/robots.txt'):
            out.append(dict(authority=auth(t[4]), utc=t[0], study='LH046', status=t[1],
                            file='studies/LH046/data/sources/' + t[5], truncated='False', source_log=log))
    # LH047's current re-reads (scripts/fetch.py logs robots hops with an empty n)
    cur = os.path.join(D, 'reads/robots-current/readlog.csv')
    if os.path.exists(cur):
        for r in csv.DictReader(open(cur, newline='')):
            if r['robots_verdict'] == 'robots.txt':
                hop = r['note'].split()[-1]
                safe = urlsplit(r['url']).netloc.replace(':', '_')
                out.append(dict(authority=auth(r['url']), utc=r['utc'], study='LH047-current', status=r['status'],
                                file='studies/LH047/data/reads/robots-current/robots-%s-%s.txt' % (safe, hop),
                                truncated='False', source_log='studies/LH047/data/reads/robots-current/readlog.csv'))
    return out


def main():
    rows = entries()
    if '--missing' in sys.argv:
        have = {r['authority'] for r in rows}
        need = set()
        for r in csv.DictReader(open(os.path.join(D, 'requests.csv'), newline='')):
            if r['sent'] == 'yes' and not r['path'].startswith('/robots.txt'):
                a = auth(r['url'])
                if a not in have:
                    need.add(a)
        for a in sorted(need):
            print(a + '/robots.txt')
        return
    with open(os.path.join(D, 'robots-index.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['authority', 'utc', 'study', 'status', 'file', 'truncated', 'source_log'])
        w.writeheader()
        w.writerows(rows)
    print('robots copies indexed:', len(rows))


if __name__ == '__main__':
    main()
