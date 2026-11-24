"""R-0135 reader review, stage 2: checks on measure 3's reading.
Reads only LH040's committed tables and read-2 Q4 body; no network.
Run: python3 -I studies/LH040/review/r0135_index_checks.py"""
import csv, os, statistics, collections
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rows = list(csv.DictReader(open(os.path.join(B, 'tables/m3_index.csv'))))
comp = [r for r in rows if r['role'] == 'comparison']
case = [r for r in rows if r['role'] == 'case'][0]
for end in ['13:23', '13:20', '12:47']:
    I = [float(r['I_' + end]) for r in comp]
    med = statistics.median(I)
    print(f"end {end}: comparison median {med:.4f}; 'within range' admits ratios "
          f"{min(I)/med:.2f} to {max(I)/med:.2f} of the median; case ratio {float(case['I_'+end])/med:.2f}")
# 1. case against comparison releases grouped by h (13:23 end)
print("\nComparison I (13:23) by hours newest on day 0:")
for lo, hi, lab in [(0, 2.5, 'h < 2.5 (all uploaded after 22:00 UTC)'), (2.5, 10, '2.5 <= h < 10'), (10, 25, 'h >= 10 (uploaded before 13:00 UTC)')]:
    g = sorted((float(r['I_13:23']), r['release']) for r in comp if lo <= float(r['h_13:23']) < hi)
    print(f"  {lab}: n={len(g)}, I = " + ", ".join(f"{v:.3f}" for v, _ in g))
print(f"  case 1.107.0: h={float(case['h_13:23']):.2f}, I={float(case['I_13:23']):.4f}")
# 2. bound on day-0 fetches after 13:23: if the post-pull rate on day 0 matched day 1's 331/24h
c0 = int(case['count_day0']); post = 331 * (24 - 13 - 23/60) / 24
print(f"\nIf day 0 after 13:23 ran at day 1's rate (331/day): about {post:.0f} fetches, "
      f"{100*post/c0:.2f}% of C0; I under 13:23 would be {float(case['I_13:23'])*(c0-post)/c0:.4f}")
# 3. installer-only robustness (LH056's check (b)) cannot be computed here: Q4 holds
# installer rows only for the case and comparison versions on their own days (on
# 2026-10-21 only 1.106.2 and 1.107.0), so no installer-only denominator exists.
q4 = list(csv.DictReader(open(os.path.join(B, 'data/read-2026-11-23T1433Z/Q4_installer.raw'))))
print("\nQ4 versions held on 2026-10-21:", sorted({r['version'] for r in q4 if r['date'] == '2026-10-21'}),
      "-> installer-only index not computable from retained data")
