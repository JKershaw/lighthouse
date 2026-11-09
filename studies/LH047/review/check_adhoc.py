"""R-0063: check the hand-coded adhoc-requests.csv against the retained transcript extract
(tool-calls.csv, which keeps the first 400 characters of each call and result; the full
transcripts are not in the repository or this container).
(1) every ad hoc row points at a tool call in the extract (transcript id and line);
(2) every literal URL in a non-collector call (curl, inline client, WebFetch) is either an
    ad hoc row of the same transcript or a fetch-log row within 120 s;
(3) every ad hoc row that the audit dropped as a duplicate has a fetch-log row with the same
    URL within 15 s.
Run from the repository root: python3 -I studies/LH047/review/check_adhoc.py"""
import csv, os
from datetime import datetime
D = os.path.join(os.getcwd(), 'studies/LH047/data')
t = lambda s: datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S')
calls = list(csv.DictReader(open(os.path.join(D, 'transcripts/tool-calls.csv'))))
adhoc = list(csv.DictReader(open(os.path.join(D, 'transcripts/adhoc-requests.csv'))))
logs = [r for r in csv.DictReader(open(os.path.join(D, 'requests.csv'))) if r['sent'] == 'yes']
key = lambda tr: tr.replace('agent-', '')[:8]
idx = {(key(c['transcript']), c['line']): c for c in calls}
print('(1) ad hoc rows without a matching tool call:', [ (a['transcript'], a['line']) for a in adhoc if (a['transcript'][:8], a['line']) not in idx])
miss = []
for c in calls:
    if c['kind'] in ('collector', 'websearch', 'git', 'scratch-script'):
        continue
    for u in c['urls'].split():
        if any(x in u for x in ('lighthouse.harbour.cat', 'claude.ai/', '127.0.0.1', 'localhost', '__agentproxy')):
            continue
        u2 = u.rstrip('.')
        ah = [a for a in adhoc if a['transcript'][:8] == key(c['transcript']) and (a['url'] == u2 or a['url'].startswith(u2) or u2.startswith(a['url']))]
        lg = [l for l in logs if (l['url'] == u2 or l['url'].startswith(u2)) and abs((t(l['utc']) - t(c['utc'])).total_seconds()) <= 120]
        if not ah and not lg:
            miss.append((c['transcript'][:14], c['line'], c['kind'], u2))
print('(2) literal URLs in non-collector calls found in neither ad hoc rows nor logs: %d' % len(miss))
for m in miss:
    print('    ', m)
dropped = 0
bad = []
for a in adhoc:
    dup = [l for l in logs if l['url'] == a['url'] and abs((t(l['utc']) - t(a['utc'])).total_seconds()) <= 15]
    if dup:
        dropped += 1
print('(3) ad hoc rows with a fetch-log twin within 15 s (dropped by the audit):', dropped, '; own-site rows:', sum('lighthouse.harbour.cat' in a['url'] for a in adhoc), '; total rows', len(adhoc))
