#!/usr/bin/env python3
"""LH009 step 1b: the class of each of the 37 fixes, from data/fix_texts.csv and data/fix_reads.csv (classify.py)
and the reader's judgements in data/flaw_judgements.csv. No network access. Writes data/fix_classes.csv.

announced   a security word (brief.md's list) in the changelog entry at the tag, the PyPI description's part for
            the version or the tag annotation, or the flaw named (reader's judgement), dated no later than 24 hours
            after the first upload (the tag's commit time for the changelog, the tagger time for an annotation,
            the upload for the description); later but before the advisory: announced late; otherwise silent.
strict_class the same with security words only (the flaw-named judgement dropped)."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, ts

LH008 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'LH008', 'data')
EV = {(e['library'], e['fixed_release']) for e in csv.DictReader(open(os.path.join(LH008, 'events.csv')))}
J = {(j['library'], j['version']): j for j in read_csv('flaw_judgements.csv')}
T = read_csv('fix_texts.csv')
rows = []
for r in read_csv('fix_reads.csv'):
    k = (r['library'], r['version'])
    up, adv = ts(r['uploaded']), ts(r['first_advisory'])
    mine = [t for t in T if (t['library'], t['version']) == k]
    primary = [t for t in mine if t['source'] in ('changelog at tag', 'tag annotation', 'PyPI description')]
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
    page = [t for t in mine if t['source'].startswith('GitHub release page')]
    rows.append(dict(
        library=r['library'], rank=r['rank'], version=r['version'], event='yes' if k in EV else 'no',
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
        class_=cls(has_sec or has_flaw), strict_class=cls(has_sec),
        basis='security word' if has_sec else ('flaw named' if has_flaw else 'none'),
        security_word_at_head_not_at_tag='yes' if head_sec and not any(t['source'] == 'changelog at tag' and t['security_words'] for t in mine) else 'no',
        release_page=page[0]['where'] if page else ''))
for x in rows:
    x['class'] = x.pop('class_')
write_csv('fix_classes.csv', rows)
for x in rows:
    print(x['event'], x['library'], x['version'], x['class'], x['strict_class'], x['basis'], x['hours_after_upload'], x['release_to_advisory_days'], x['security_word_at_head_not_at_tag'])
