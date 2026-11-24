"""Resolution of R-0135 (reader review of LH040 1.0): the driving session's own checks.
Recomputes measure 3's rank, ratio to median and band width from tables/m3_index.csv,
and measure 2's installers on days 1 to 30 directly from read 2's raw Q4 and Q2 bodies.
No network. Run: python3 -I studies/LH040/review/resolution_r0135_checks.py"""
import csv, os, statistics, collections
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
R2 = os.path.join(B, 'data/read-2026-11-23T1433Z')

rows = list(csv.DictReader(open(os.path.join(B, 'tables/m3_index.csv'))))
comp = [r for r in rows if r['role'] == 'comparison']
case = [r for r in rows if r['role'] == 'case'][0]
print("Measure 3 (from tables/m3_index.csv)")
for end in ['13:23', '13:20', '12:47']:
    I = sorted(float(r['I_' + end]) for r in comp)
    c = float(case['I_' + end]); med = statistics.median(I)
    above = sum(v > c for v in I)
    print(f"  end {end}: case I {c:.4f}; comparison min {I[0]:.4f} median {med:.4f} max {I[-1]:.4f}; "
          f"band {I[0]/med:.2f} to {I[-1]/med:.2f} x median; case {c/med:.2f} x median; "
          f"rank {above+1} of 18; comparison releases below case: {17-above}")
    # largest reduction from the median that the rule would still read as ordinary
    print(f"    a release at the median, held down by up to {100*(1-I[0]/med):.0f}%, would still read 'within range'")
# relative position inside the band under 13:23
I = sorted(float(r['I_13:23']) for r in comp); c = float(case['I_13:23'])
print(f"  13:23: case sits {100*(c-I[0])/(I[-1]-I[0]):.0f}% of the way from the band's floor to its top")

print("\nMeasure 2 installers, days 1 to 30 (22 Oct to 20 Nov), from raw Q4")
q4 = list(csv.DictReader(open(os.path.join(R2, 'Q4_installer.raw'))))
tot = collections.Counter()
for r in q4:
    if r['version'] == '1.107.0' and '2026-10-22' <= r['date'] <= '2026-11-20':
        tot[r['installer'] or '(none)'] += int(r['count'])
n = sum(tot.values())
for k, v in tot.most_common():
    print(f"  {k}: {v} ({100*v/n:.1f}%)")
print(f"  total {n}; pip {tot.get('pip', 0)}; no name or Browser {tot['(none)']+tot['Browser']} "
      f"({100*(tot['(none)']+tot['Browser'])/n:.1f}%)")
q2 = list(csv.DictReader(open(os.path.join(R2, 'Q2_daily_by_version_oct_nov.raw'))))
t2 = sum(int(r['count']) for r in q2 if r['version'] == '1.107.0' and '2026-10-22' <= r['date'] <= '2026-11-20')
print(f"  Q2 by-version sum, same days: {t2}")
uvd = sorted((r['date'], int(r['count'])) for r in q4 if r['version'] == '1.107.0' and r['installer'] == 'uv' and r['date'] >= '2026-10-22')
print("  uv by day after day 0:", uvd)
