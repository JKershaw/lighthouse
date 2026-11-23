"""LH047 re-audit, W47: class every candidate file from the mechanical search (candidates-raw.csv)
as a request log or not, by the rules below, written before any row was judged; writes logs.csv
(one row per candidate: include, reason, and for logs the format, practice, collector and provider).
Run from the repository root: python3 -I studies/LH047/data/reaudit-2026-W47/code/classify.py
"""
import csv, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE_UA = ''

# (regex on path, include, format, practice template, collector template, implicit_robots, reason)
RULES = [
    (r'^studies/(LH0\d\d)/data/(read|vendor|credit|pre-brief)-[^/]+/read_log\.json$', 'yes', 'read_log_json', None, None, '', 'collector read log'),
    (r'^studies/LH038/data/suse-clocks-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH038 suse_clocks.py', 'studies/LH038/scripts/suse_clocks.py', '', 'collector read log'),
    (r'^studies/LH039/data/raw-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH039 collect.py', 'studies/LH039/scripts/collect.py', '', 'collector read log'),
    (r'^studies/LH039/data/packagist-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH039 packagist.py', 'studies/LH039/scripts/packagist.py', '', 'collector read log'),
    (r'^studies/LH039/data/oneoff-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH039 oneoff_release_dates.py', 'studies/LH039/scripts/oneoff_release_dates.py', '', 'collector read log'),
    (r'^studies/LH044/data/(read|wayback)-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH044 collect.py', 'studies/LH044/scripts/collect.py', 'no', 'collector read log (robots.txt reads logged as rows)'),
    (r'^studies/LH045/data/epoch/raw-[^/]+/readlog\.csv$', 'yes', 'readlog_csv', 'LH045 collect_epoch.py', 'studies/LH045/scripts/collect_epoch.py', 'no', 'collector read log (robots.txt read logged as a row)'),
    (r'^studies/LH050/data/([^/]+)/fetch_log\.jsonl$', 'yes', 'fetch_log_jsonl', 'LH050 collector.py', 'studies/LH050/data/{1}/collector.py', '', 'collector fetch log'),
    (r'^studies/LH055/data/[^/]+/fetch_log\.jsonl$', 'yes', 'fetch_log_jsonl', 'LH055 collect.py', 'studies/LH055/scripts/collect.py', '', 'collector fetch log'),
    (r'^studies/LH056/data/prebrief-[^/]+/fetchlog\.csv$', 'yes', 'fetchlog_csv', 'LH056 collect_prebrief.py', 'studies/LH056/scripts/collect_prebrief.py', '', 'collector fetch log'),
    (r'^studies/LH056/data/read-[^/]+/fetchlog\.csv$', 'yes', 'fetchlog_csv', 'LH056 collect.py', 'studies/LH056/scripts/collect.py', '', 'collector fetch log'),
    (r'^studies/LH056/data/readiness-[^/]+/probe-log\.csv$', 'yes', 'lh056_probe', 'LH056 readiness probe', '', 'no', 'one-request probe log (endpoint not written in it)'),
    (r'^studies/LH057/fetchlog\.csv$', 'yes', 'fetchlog_csv', 'LH057 collect.py and pre-brief reads', 'studies/LH057/collect.py', 'yes', 'fetch log (each row names the gate read of robots.txt)'),
    (r'^studies/LH058/fetchlog\.csv$', 'yes', 'fetchlog_csv', 'LH058 pre-brief read', '', 'yes', 'fetch log (the row names the gate read of robots.txt)'),
    (r'^studies/LH051/data/fetch-log\.tsv$', 'yes', 'lh051_tsv', 'LH051 collect.py (GH Archive hours)', 'studies/LH051/scripts/collect.py', '', 'collector fetch log'),
    (r'^studies/LH013/data/read_log\.csv$', 'yes', 'lh013_csv', 'LH013 collect.py (ClickPy SQL)', 'studies/LH013/scripts/common.py', '', 'collector read log'),
    (r'^notes/horizon/2026-11-20T1214Z/requests\.csv$', 'yes', 'horizon_requests', 'Horizon 2026-11-20 scouts', '', 'no', 'log of the scouts\' tool calls'),
    (r'^notes/microsoft-outage-report/readings/2026-11-\d\d\.md$', 'yes', 'ms_reading', 'Microsoft report watch (notes)', '', 'yes', 'reading note with a table of requests and UTC times'),
]
EXCLUDE = [
    (r'/(robots|bodies|text|searches)/', 'a retained body, robots.txt decision or search record, not a request log (its request is in the run\'s log)'),
    (r'/data/[^/]+/[^/]+\.json\.gz$|\.(raw|body|b|h|raw\.gz|txt\.gz)$|\.withheld\.json$|\.derived\.json$|\.facts\.json$|derived\.json\.gz$', 'a retained body or derived file'),
    (r'(^|/)(brief|sources|README|LH0\d\d)\.md$|/checkpoints/|/review/|^notes/R-\d+|^proposals\.md$|^site/|^scripts/|/scripts/|\.py$', 'prose, code or review output, not a request log'),
    (r'^notes/horizon/2026-11-(17|18|20)T\d+Z(/scout-\d-[a-z-]+)?\.md$', 'scout or sweep note; its URLs carry no per-request UTC time (unlogged; see README)'),
    (r'^notes/keeper/', 'survey outputs and working files of the keeper\'s 21 November decision; no per-request UTC time (unlogged; see README)'),
    (r'^notes/php-media-sweep/', 'prose sweep note; its gate checks and reads are hand-coded in handcoded.csv'),
    (r'^notes/microsoft-outage-report/(comparison|gate-[^/]+)\.md$', 'prose, no request made for it'),
    (r'^notes/(php-watch-log|physical-authority-watch-log)\.md$', 'summary of reads logged elsewhere'),
    (r'(tables|summary|services|panel|hours|census|classes|coded|claims|links|result|credit_fields|inventory)[^/]*\.(json|csv)(\.gz)?$|reads\.csv$|record-[^/]*\.txt$|/[^/]*tabulation[^/]*\.txt$', 'derived table or index, not a request log (LH050 reads.csv duplicates its fetch logs)'),
]


def main():
    cands = list(csv.DictReader(open(os.path.join(OUT, 'candidates-raw.csv'), newline='')))
    out = []
    for c in cands:
        p = c['path']
        row = dict(path=p, include='no', format='', practice='', study='', run='', collector='', provider='', ua='', implicit_robots='',
                   utc_precision='', reason='')
        for rx, inc, fmt, prac, coll, imp, why in RULES:
            m = re.search(rx, p)
            if m:
                st = re.match(r'^(studies/(LH0\d\d)|notes/[^/]+)', p)
                study = st.group(2) or st.group(1)
                runm = re.search(r'(\d{4}-\d\d-\d\dT\d{4}Z|\d{4}-\d\d-\d\d)', p)
                if prac is None:  # read_log.json: one practice per study and kind of read
                    kind = m.group(2)
                    prac = '%s %s' % (study, {'read': 'collect.py', 'vendor': 'vendor.py', 'credit': 'collect.py (credit read)',
                                              'pre-brief': 'collect.py (pre-brief read)'}[kind])
                    coll = 'studies/%s/scripts/%s' % (study, 'vendor.py' if kind == 'vendor' else 'collect.py')
                coll = coll.replace('{1}', m.group(1)) if '{1}' in coll else coll
                row.update(include=inc, format=fmt, practice=prac, study=study, run=runm.group(1) if runm else '', collector=coll,
                           provider='anthropic', implicit_robots=imp, reason=why)
                break
        else:
            for rx, why in EXCLUDE:
                if re.search(rx, p):
                    row['reason'] = why
                    break
            else:
                row['reason'] = 'UNCLASSED'
        out.append(row)
    out.append(dict(path='studies/LH047/data/reaudit-2026-W47/handcoded.csv', include='yes', format='handcoded', practice='',
                    study='notes', run='', collector='', provider='anthropic', ua='', implicit_robots='no', utc_precision='minute-approx',
                    reason='requests named in prose notes (php-media-sweep, LH050 panel locking), hand-coded by code/handcode.py'))
    with open(os.path.join(OUT, 'logs.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(r['include'] for r in out), [r['path'] for r in out if r['reason'] == 'UNCLASSED'])


if __name__ == '__main__':
    main()
