#!/usr/bin/env python3
"""LH010 step 2c: the class of each fix. Copied from LH009's classes.py and changed as follows: the fixes are LH010's
(data/fix_reads.csv, from classify.py); a changelog entry first written after the tag (date_head_entries.py,
source 'changelog after the tag (history)') is a dated source, so such a fix is announced late if its words came
before the advisory and silent otherwise; the twelve events that are the same release as LH008's take their row
from studies/LH009/data/fix_classes.csv (brief.md, reuse), marked reused_from_LH009, with the event's LH010
advisory time and gap. No network access. Writes data/fix_classes.csv.

announced    a security word in the changelog entry at the tag, the PyPI description's part for the version or the
             tag annotation, or the flaw named (data/flaw_judgements.csv), dated no later than 24 hours after the
             first upload; later but before the first qualifying advisory: announced late; otherwise silent.
strict_class the same with security words only."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, ts

LH009 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'LH009', 'data')
EVR = {(e['library'], e['fixed_release']): e for e in read_csv('events.csv')}
J = {(j['library'], j['version']): j for j in read_csv('flaw_judgements.csv')}
T = read_csv('fix_texts.csv')
PRIMARY = ('changelog at tag', 'tag annotation', 'PyPI description', 'changelog after the tag (history)')
rows = []
for r in read_csv('fix_reads.csv'):
    k = (r['library'], r['version'])
    up, adv = ts(r['uploaded']), ts(r['first_advisory'])
    mine = [t for t in T if (t['library'], t['version']) == k]
    primary = [t for t in mine if t['source'] in PRIMARY]
    sec = [t for t in primary if t['security_words']]
    j = J[k]
    deciding = sec or ([t for t in primary if t['source'] == 'changelog at tag' and t['chars'] != '0'] if j['flaw_named'] == 'yes' else [])
    dated = min((ts(t['dated']) for t in deciding if t['dated']), default=None)

    def cls(has):
        if not has:
            return 'silent'
        if dated is None:
            return 'undated'
        h = (dated - up).total_seconds() / 3600
        return 'announced' if h <= 24 else ('announced late' if dated < adv else 'silent')

    has_sec, has_flaw = bool(sec), j['flaw_named'] == 'yes'
    head_sec = [t for t in mine if t['source'] == 'changelog at head' and t['security_words']]
    rows.append(dict(
        library=r['library'], rank=r['rank'], version=r['version'], event=r['event'], reused_from_LH009='no',
        uploaded=r['uploaded'], first_advisory=r['first_advisory'],
        release_to_advisory_days=round((adv - up).total_seconds() / 86400, 2), advisories=r['advisories'],
        repo=r['repo'], tag=r['tag'], tag_type=r['tag_type'], tag_commit_time=r['tag_commit_time'],
        changelog_entry_at_tag=' '.join(t['where'] for t in mine if t['source'] == 'changelog at tag') or 'none',
        description_part='yes' if any(t['source'] == 'PyPI description' and t['chars'] != '0' for t in mine) else 'no',
        annotation='yes' if any(t['source'] == 'tag annotation' and t['chars'] not in ('0', '') for t in mine) else 'no',
        security_word_in=' '.join(sorted({t['source'] for t in sec})) or 'none',
        flaw_named=j['flaw_named'], deciding_words=j['flaw_words'] or '', near_miss=j['near_miss_note'],
        deciding_text_dated=dated.strftime('%Y-%m-%dT%H:%M:%SZ') if dated else '',
        hours_after_upload=round((dated - up).total_seconds() / 3600, 2) if dated else '',
        cls=cls(has_sec or has_flaw), strict_class=cls(has_sec),
        basis='security word' if has_sec else ('flaw named' if has_flaw else 'none'),
        security_word_at_head_not_at_tag='yes' if head_sec and not any(t['source'] == 'changelog at tag' and t['security_words'] for t in mine) else 'no'))
# the twelve reused events
for x in csv.DictReader(open(os.path.join(LH009, 'fix_classes.csv'))):
    e = EVR.get((x['library'], x['version']))
    if not e:
        continue
    up, adv = ts(x['uploaded']), ts(e['advisory_published'])
    y = {k: x.get(k, '') for k in rows[0]}
    y.update(rank=e['rank'], event='yes', reused_from_LH009='yes', cls=x['class'], first_advisory=e['advisory_published'],
             release_to_advisory_days=round((adv - up).total_seconds() / 86400, 2))
    rows.append(y)
rows.sort(key=lambda x: (int(x['rank']), ts(x['uploaded'])))
for x in rows:
    x['class'] = x.pop('cls')
write_csv('fix_classes.csv', rows)
ev = [x for x in rows if x['event'] == 'yes']
print(len(rows), 'fixes;', len(ev), 'events')
for c in ('announced', 'announced late', 'silent', 'undated'):
    print(c, 'all fixes', sum(x['class'] == c for x in rows), 'strict', sum(x['strict_class'] == c for x in rows),
          '| events', sum(x['class'] == c for x in ev), 'strict', sum(x['strict_class'] == c for x in ev))
for x in ev:
    print(x['rank'], x['library'], x['version'], x['class'], x['strict_class'], x['basis'], x['hours_after_upload'], x['release_to_advisory_days'], x['reused_from_LH009'])
