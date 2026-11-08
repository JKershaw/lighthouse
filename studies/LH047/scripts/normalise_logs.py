"""LH047: gather every request in the retained fetch logs of LH041 to LH046 and the essays'
review folders into one table, data/requests.csv. Offline: reads only files in the repository.

Run from the repository root:  python3 -I studies/LH047/scripts/normalise_logs.py

One row per logged request: log, study, url, host, path, utc, status, note. A row the
collector logged but did not send (for example "not fetched: robots.txt disallows") is kept
with sent=no, so the table can show what a collector refused as well as what it sent.
"""
import csv, os, sys
from urllib.parse import urlsplit

ROOT = os.getcwd()
OUT = os.path.join(ROOT, 'studies/LH047/data/requests.csv')

LOGS = [
    # (path, study, format)
    ('studies/LH041/data/prebrief/web-log.psv', 'LH041', 'psv_lh041_prebrief'),
    ('studies/LH041/data/2026-11-08T1910Z/requests.csv', 'LH041', 'csv_lh041'),
    ('studies/LH041/review/web/log.psv', 'LH041-review', 'psv_lh041_review'),
    ('studies/LH042/data/round1-2026-11-08/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/data/round2-2026-11-08/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/data/round3-2026-11-08/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/data/round4-2026-11-08/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/data/round5-2026-11-08/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/data/dash-2026-11-08T1909Z/readlog.csv', 'LH042', 'csv_lh042'),
    ('studies/LH042/review/live/readlog.csv', 'LH042-review', 'csv_lh042_review'),
    ('studies/LH043/data/fetch-log.tsv', 'LH043', 'tsv_lh043'),
    ('studies/LH044/data/prebrief-2026-11-08T1915Z/readlog.csv', 'LH044', 'csv_lh044_prebrief'),
    ('studies/LH044/data/read-2026-11-08T1920Z/readlog.csv', 'LH044', 'csv_lh044'),
    ('studies/LH044/data/statements-2026-11-08T1920Z/readlog.csv', 'LH044', 'csv_lh044'),
    ('studies/LH044/data/httparchive-2026-11-08T1920Z/readlog.csv', 'LH044', 'csv_lh044'),
    ('studies/LH044/data/wayback-2026-11-08T1920Z/readlog.csv', 'LH044', 'csv_lh044'),
    ('studies/LH045/data/before-the-brief/readlog.csv', 'LH045', 'csv_lh045_pre'),
    ('studies/LH045/data/epoch/raw-2026-11-08T1913Z/readlog.csv', 'LH045', 'csv_lh045'),
    ('studies/LH045/data/ietf/raw-2026-11-08T1914Z/readlog.csv', 'LH045', 'csv_lh045'),
    ('studies/LH045/data/ietf/raw-2026-11-08T1915Z/readlog.csv', 'LH045', 'csv_lh045'),
    ('studies/LH046/data/sources/fetch-log.tsv', 'LH046', 'tsv_lh046_sources'),
    ('studies/LH046/data/fetch-log.tsv', 'LH046', 'tsv_lh046'),
    ('studies/LH046/review/out/fetch-log.tsv', 'LH046-review', 'tsv_lh046'),
    ('essays/what-the-watch-would-see/claims-check/fetch-log.tsv', 'essay-claims-check', 'tsv_essay'),
    ('essays/what-the-watch-would-see/reader-review/fetch-log.tsv', 'essay-reader-review', 'tsv_essay'),
    ('essays/what-the-watch-would-see/recheck/fetch-log.tsv', 'essay-recheck', 'tsv_essay'),
]


def rows_of(path, fmt):
    p = os.path.join(ROOT, path)
    if fmt.startswith('psv'):
        with open(p, newline='') as f:
            for r in csv.DictReader(f, delimiter='|'):
                yield dict(url=r['url'], utc=r['read_utc'], status=r['status'], note=r.get('file', ''), sent='yes')
    elif fmt == 'csv_lh041':
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                if not r['url']:
                    continue
                yield dict(url=r['url'], utc=r['read_utc'], status=r['status'], note=r['note'], sent='yes')
    elif fmt in ('csv_lh042', 'csv_lh042_review'):
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                st = r.get('http_status', r.get('status', ''))
                err = r.get('error', '')
                sent = 'no' if err.startswith('not fetched') else 'yes'
                yield dict(url=r['url'], utc=r['start_utc'], status=st, note=('robots=%s %s' % (r['robots'], err)).strip(), sent=sent)
                # fetch.py and live_fetch.py read robots.txt once per host without logging a row;
                # those reads are added by add_implicit_robots() below.
    elif fmt == 'tsv_lh043':
        with open(p) as f:
            for line in f:
                t = line.rstrip('\n').split('\t')
                if len(t) < 3:
                    continue
                yield dict(url=t[2], utc=t[0], status=t[1], note=t[3] if len(t) > 3 else '', sent='yes')
    elif fmt == 'csv_lh044_prebrief':
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                yield dict(url=r['url'], utc=r['utc'], status=r['status'] or r['error'], note=r['file'], sent='yes')
    elif fmt == 'csv_lh044':
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                yield dict(url=r['url'], utc=r['utc'], status=r['status'] or r['error'],
                           note='%s %s ua=%s' % (r['service'], r['kind'], r['ua']), sent='yes')
    elif fmt == 'csv_lh045_pre':
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                yield dict(url=r['url'], utc=r['utc_start'], status=r['status'], note=r['name'], sent='yes')
    elif fmt == 'csv_lh045':
        with open(p, newline='') as f:
            for r in csv.DictReader(f):
                sent = 'no' if r['status'] == 'skipped' else 'yes'
                yield dict(url=r['url'], utc=r['utc_start'], status=r['status'], note=r.get('note', '') or r.get('name', '') or r.get('file', ''), sent=sent)
    elif fmt == 'tsv_lh046_sources':
        with open(p) as f:
            for line in f:
                t = line.rstrip('\n').split('\t')
                yield dict(url=t[4], utc=t[0], status=t[1], note=t[5] if len(t) > 5 else '', sent='yes')
    elif fmt == 'tsv_lh046':
        with open(p) as f:
            for line in f:
                t = line.rstrip('\n').split('\t')
                yield dict(url=t[4], utc=t[0], status=t[1], note=t[5] if len(t) > 5 else '', sent='yes')
    elif fmt == 'tsv_essay':
        with open(p, newline='') as f:
            for r in csv.DictReader(f, delimiter='\t'):
                yield dict(url=r['url'], utc=r['read_utc'], status=r['http'], note=r['file'], sent='yes')
    else:
        raise SystemExit('unknown format ' + fmt)


def main():
    out = []
    for path, study, fmt in LOGS:
        for r in rows_of(path, fmt):
            u = urlsplit(r['url'].strip())
            out.append(dict(log=path, study=study, url=r['url'].strip(), scheme=u.scheme, host=u.hostname or '',
                            path=(u.path or '/') + (('?' + u.query) if u.query else ''),
                            utc=r['utc'], status=r['status'], sent=r['sent'], note=r['note']))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['log', 'study', 'url', 'scheme', 'host', 'path', 'utc', 'status', 'sent', 'note'])
        w.writeheader()
        w.writerows(out)
    print('rows', len(out), 'sent', sum(1 for r in out if r['sent'] == 'yes'))


if __name__ == '__main__':
    main()
