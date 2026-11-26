#!/usr/bin/env python3
"""R-0153 (reader-and-inference review of LH051 record 1.1): context for measure 3.
Reads only data/hours.csv and data/counts.csv (aggregate counts). Fetches nothing.
Asks: how big is the probe's held count beside everything the files hold in the same hours?
Usage: python3 -I studies/LH051/review/R-0153_context.py
"""
import csv, statistics
from pathlib import Path
D = Path(__file__).resolve().parents[1] / 'data'
hours = {r['hour']: r for r in csv.DictReader(open(D / 'hours.csv')) if r['http_status'] == '200'}
counts = list(csv.DictReader(open(D / 'counts.csv')))
def key(h):
    d, hh = h.rsplit('-', 1); return (d, int(hh))
order = sorted(hours, key=key)
def span(a, b):
    return [h for h in order if key(a) <= key(h) <= key(b)]
def tot(hs, col):
    return sum(int(hours[h][col]) for h in hs)
ev = [int(hours[h]['events']) for h in order]
pr = [int(hours[h]['PullRequestEvent']) for h in order]
print(f'held hours: {len(order)}')
print(f'all events per hour: median {statistics.median(ev)}, range {min(ev)} to {max(ev)}')
print(f'PullRequestEvent per hour: median {statistics.median(pr)}, range {min(pr)} to {max(pr)}')
for name, a, b, vendor in [('Aikido', '2026-11-10-12', '2026-11-11-14', 61839),
                           ('StepSecurity', '2026-11-10-0', '2026-11-12-7', 63000)]:
    hs = span(a, b)
    m1 = sum(int(c['events']) for c in counts if c['marker'] == 'M1' and c['event_type'] == 'PullRequestEvent'
             and c['action'] == 'opened' and c['hour'] in hs)
    allpr = tot(hs, 'PullRequestEvent'); allev = tot(hs, 'events')
    print(f'{name}: {len(hs)} hours; all held events {allev}; all held PullRequestEvent {allpr}; '
          f'M1 opened {m1} ({100*m1/allpr:.1f}% of held PR events); vendor search count {vendor} '
          f'= {vendor/allpr:.2f} x all held PR events of every kind in those hours')
# baseline vs campaign hours: did total PR events rise when the campaign ran?
base = span('2026-11-09-0', '2026-11-10-11'); camp = span('2026-11-10-12', '2026-11-11-14')
print(f'mean PullRequestEvent per hour: baseline {tot(base,"PullRequestEvent")/len(base):.0f}, '
      f'Aikido window {tot(camp,"PullRequestEvent")/len(camp):.0f}')
# peak probe hours as a share of their hour's PR events
for h in ('2026-11-11-11', '2026-11-11-12'):
    m1 = sum(int(c['events']) for c in counts if c['hour'] == h and c['marker'] == 'M1'
             and c['event_type'] == 'PullRequestEvent' and c['action'] == 'opened')
    print(f'{h}: M1 opened {m1} of {hours[h]["PullRequestEvent"]} PR events, {hours[h]["events"]} events in all')
