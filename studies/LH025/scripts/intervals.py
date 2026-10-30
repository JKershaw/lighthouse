#!/usr/bin/env python3
"""Per-tag linux/amd64 digest at each daily read, from the retained Hub tag responses, and the
interval that bounds each change. Offline; reads data/snapshot-*/hubtag_*.raw and read_log.csv.

Usage: python3 studies/LH025/scripts/intervals.py
"""
from pathlib import Path
import csv
import json

DATA = Path(__file__).resolve().parents[1] / 'data'
TAGS = ['wordpress_php8_2_apache', 'wordpress_php8_3_fpm', 'drupal_10_6_php8_3_fpm', 'nextcloud_apache', 'nextcloud_fpm']

reads = []
for snap in sorted(DATA.glob('snapshot-*')):
    log = list(csv.DictReader(open(snap / 'read_log.csv', newline='')))
    reads.append((snap.name[9:], log[0]['utc'], snap))

for tag in TAGS:
    print(tag)
    last = None
    for day, start, snap in reads:
        f = snap / f'hubtag_{tag}.raw'
        if not f.exists():
            print(f'  {day} {start}  not read (unknown)')
            continue
        d = json.loads(f.read_bytes())
        img = [i for i in d['images'] if i.get('architecture') == 'amd64' and not i.get('variant')][0]
        dig, pushed = img['digest'][7:19], img['last_pushed'][:19]
        mark = ''
        if last and dig != last[0]:
            mark = f'  CHANGED: after {last[1]}, by {start}'
        print(f'  {day} {start}  {dig}  platform push {pushed}  tag push {d["tag_last_pushed"][:19]}{mark}')
        last = (dig, start)
