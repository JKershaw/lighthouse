"""R-0063: compare the reviewer's hand verdicts (sample-verdicts.csv) with the audit's (sample-drawn.csv).
Run from the repository root: python3 -I studies/LH047/review/compare_sample.py"""
import csv, os
D = os.path.join(os.getcwd(), 'studies/LH047/review')
drawn = {r['n']: r for r in csv.DictReader(open(os.path.join(D, 'sample-drawn.csv')))}
agree = dis = 0
for r in csv.DictReader(open(os.path.join(D, 'sample-verdicts.csv'))):
    a = drawn[r['n']]
    ok1 = r['reviewer_R1'] == a['audit_R1']
    ok2 = set(r['reviewer_R2_tokens'].split()) == set(a['audit_R2_tokens'].split())
    mark = 'agree' if ok1 and ok2 else 'DISAGREE'
    agree += mark == 'agree'; dis += mark != 'agree'
    print('%2s %s %-8s audit R1=%-16s reviewer R1=%-16s R2 tokens %s | %s' % (r['n'], a['stratum'], mark, a['audit_R1'], r['reviewer_R1'],
          'same' if ok2 else '%r vs %r' % (a['audit_R2_tokens'], r['reviewer_R2_tokens']), a['url'][:70]))
print('agree %d, disagree %d, of %d' % (agree, dis, agree + dis))
