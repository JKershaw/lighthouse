#!/usr/bin/env python3
"""LH012: readings made after the counts were read (post hoc), two of them, offline from data/checks/
and data/week/python/. Prints the reading; replay.sh compares it with data/post_hoc_reading.txt.
1. What boto3's Python 3.9 downloads are, on one day (checks C1 to C3; C1 and C2 are the check of a
   surprising result against a second table, C3 the post hoc description).
2. How often Python 3.9 environments fetched boto3 compared with botocore over W.
New for LH012. Usage: python3 post_hoc.py"""
import csv, os

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def rd(*p):
    return list(csv.DictReader(open(os.path.join(DATA, *p))))


view = {r['python_minor']: int(r['n']) for r in rd('checks', 'boto3_python_view.csv')}
raw = {r['python_minor']: int(r['n']) for r in rd('checks', 'boto3_python_pypi.csv')}
print('1. boto3 on 23 September 2026, by Python minor: by-Python view against pypi.pypi')
print(f'   minors {len(view)} and {len(raw)}; identical counts for every minor: {view == raw}')
t = sum(raw.values())
print(f'   Python 3.9: {raw.get("3.9", 0):,} of {t:,} downloads ({raw.get("3.9", 0) / t * 100:.1f} per cent)')
c3 = rd('checks', 'boto3_py39_installers.csv')
top = c3[0]
print(f'   largest group of the 3.9 downloads (C3, post hoc): installer {top["installer"]}, ci {top["ci"]}, system {top["system"]}, '
      f'libc {top["libc_lib"]}: {int(top["n"]):,} ({int(top["n"]) / raw["3.9"] * 100:.1f} per cent of the 3.9 downloads)')
print()
print('2. Python 3.9 downloads over 21 to 27 September 2026 (post hoc)')
tot = {}
for p in ('boto3', 'botocore'):
    rows = rd('week', 'python', p + '.csv')
    tot[p] = (sum(int(r['n']) for r in rows if r['python_minor'] == '3.9'), sum(int(r['n']) for r in rows))
    print(f'   {p}: {tot[p][0]:,} of {tot[p][1]:,} ({tot[p][0] / tot[p][1] * 100:.1f} per cent)')
print(f'   boto3 over botocore, Python 3.9: {tot["boto3"][0] / tot["botocore"][0]:.2f}; all Pythons: {tot["boto3"][1] / tot["botocore"][1]:.2f}')
