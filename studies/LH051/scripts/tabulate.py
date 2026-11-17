#!/usr/bin/env python3
"""LH051 tabulator: measures 1 to 7 of the brief (studies/LH051/brief.md, protocol 0.1), offline.

Written 17 November 2026 for the checkpoint (schedule row LH051-checkpoint), after the reads of 13 November
(read-2026-11-13T1541Z) and 16 November (read-2026-11-16T1419Z) were held. It reads only data/hours.csv and
data/counts.csv, which hold aggregate counts and no identifier; it fetches nothing, writes nothing, and changes
nothing in the protocol. It implements the measures as written; where the brief leaves a choice open, the choice
made here is named in a comment marked AMBIGUITY and in the checkpoint note.

Usage:
  python3 -I studies/LH051/scripts/tabulate.py                # every held hour, to stdout
  python3 -I studies/LH051/scripts/tabulate.py --to 2026-11-12-23

Output is plain text with no clock time, so a replay over the same two CSV files is byte-identical.

Classes kept distinct (brief, Missing evidence): an hour is HELD if hours.csv has it with HTTP 200 and gzip_ok 1;
an hour in range without such a row is UNAVAILABLE (not empty). A held hour with no row in counts.csv held no
matching event. A GAP hour (no PushEvent, CreateEvent or DeleteEvent) is UNKNOWN, not zero, for every marker in
those three types; pull request events in it are counted as held.
"""
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import csv
import statistics

DATA = Path(__file__).resolve().parents[1] / 'data'

FIRST_HOUR = '2026-11-09-0'
BASELINE_LAST = '2026-11-10-11'          # measure 6: 36 baseline hours, 2026-11-09-0 to 2026-11-10-11
VENDOR_START_HOUR = '2026-11-10-12'      # measure 2: 12:00 to 13:00 UTC on 10 November
M4_LAST = '2026-11-12-23'                # measure 4: onset to the end of 12 November
WINDOWS = [                              # measure 3: (vendor, first hour, last hour, search count, 'more than'?)
    ('Aikido', '2026-11-10-12', '2026-11-11-14', 61839, False),
    ('StepSecurity', '2026-11-10-0', '2026-11-12-7', 63000, True),
]
NO_GAP_TYPES = ('PushEvent', 'CreateEvent', 'DeleteEvent')   # unknown in a gap hour
TYPES = ('PullRequestEvent', 'PullRequestReviewEvent', 'CreateEvent', 'DeleteEvent', 'PushEvent')
MARKERS = ('M1', 'M2', 'M3')


def h2dt(h):
    d, hh = h.rsplit('-', 1)
    return datetime.strptime(d, '%Y-%m-%d') + timedelta(hours=int(hh))


def dt2h(t):
    return f'{t:%Y-%m-%d}-{t.hour}'


def span(a, b):
    t, end, out = h2dt(a), h2dt(b), []
    while t <= end:
        out.append(dt2h(t))
        t += timedelta(hours=1)
    return out


def load(to):
    hours = {}
    for r in csv.DictReader(open(DATA / 'hours.csv', newline='')):
        if r['http_status'] == '200' and r['gzip_ok'] == '1':
            if to is None or h2dt(r['hour']) <= h2dt(to):
                hours[r['hour']] = r
    counts = []
    for r in csv.DictReader(open(DATA / 'counts.csv', newline='')):
        if r['hour'] in hours:
            r['events'] = int(r['events'])
            counts.append(r)
    return hours, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--to', help='last hour to include (YYYY-MM-DD-H); default the last held hour')
    args = ap.parse_args()
    hours, counts = load(args.to)
    if not hours:
        raise SystemExit('no held hour')
    last = max(hours, key=h2dt)
    rng = span(FIRST_HOUR, last)
    unavailable = [h for h in rng if h not in hours]
    gap = {h: hours[h]['gap_hour'] == '1' for h in hours}

    def n(h, marker, etype=None, action=None):
        """Events held in hour h for marker (and type, action). None if unknown (unavailable, or gap for a
        Push/Create/Delete type)."""
        if h not in hours:
            return None
        if etype in NO_GAP_TYPES and gap[h]:
            return None
        return sum(r['events'] for r in counts if r['hour'] == h and r['marker'] == marker
                   and (etype is None or r['event_type'] == etype) and (action is None or r['action'] == action))

    def fmt(v):
        return '?' if v is None else str(v)

    out = []
    p = out.append
    p('LH051 tabulation (studies/LH051/scripts/tabulate.py), protocol 0.1, measures as written')
    p(f'hours in range: {FIRST_HOUR} to {last}: {len(rng)}; held {len(hours)}; unavailable {len(unavailable)}'
      + (f' ({", ".join(unavailable)})' if unavailable else ''))
    p(f'gap hours among held: {sum(gap.values())}; held hours with any JSON error: '
      f'{sum(1 for h in hours if hours[h]["json_errors"] not in ("", "0"))}')
    p(f'reads holding these hours: {", ".join(sorted({hours[h]["read"] for h in hours}))}')
    p('"?" = unknown (gap hour for Push/Create/Delete, or unavailable); 0 = held and none matched')
    p('')

    # ---- Measure 1 -------------------------------------------------------------------------------------------
    p('== Measure 1: hourly series ==')
    p('Every matching (hour, marker, type, action) cell, with distinct repository and actor counts, as written by')
    p('the collector in data/counts.csv:')
    p('hour,marker,event_type,action,events,distinct_repos,distinct_actors')
    for r in sorted(counts, key=lambda r: (h2dt(r['hour']), r['marker'], r['event_type'], r['action'])):
        p(f'{r["hour"]},{r["marker"]},{r["event_type"]},{r["action"]},{r["events"]},'
          f'{r["distinct_repos"]},{r["distinct_actors"]}')
    p('')
    p('Per held hour (gap flag; M1 by type and action; M2 and M3 by type). PR = PullRequestEvent,')
    p('RV = PullRequestReviewEvent, CR = CreateEvent, DE = DeleteEvent, PU = PushEvent.')
    p('hour          gap | M1 PR:open close reop other  RV  CR  DE  PU | M2 PR  RV  CR  DE  PU | M3 PR  RV  CR  DE  PU')
    for h in rng:
        if h not in hours:
            p(f'{h:<13} unavailable')
            continue
        m1 = [n(h, 'M1', 'PullRequestEvent', a) for a in ('opened', 'closed', 'reopened', 'other')]
        m1 += [n(h, 'M1', t) for t in TYPES[1:]]
        rest = []
        for m in ('M2', 'M3'):
            rest.append(' '.join(f'{fmt(n(h, m, t)):>3}' for t in TYPES))
        p(f'{h:<13} {int(gap[h]):>3} | ' + ' '.join(f'{fmt(v):>5}' if i < 4 else f'{fmt(v):>3}'
                                                    for i, v in enumerate(m1))
          + ' | ' + rest[0] + ' | ' + rest[1])
    p('')

    # ---- Measure 2 -------------------------------------------------------------------------------------------
    p('== Measure 2: onset ==')
    onset = next((h for h in rng if h in hours and n(h, 'M1')), None)
    p(f'first held hour holding any M1 event: {onset}')
    if onset:
        types = sorted({(r['event_type'], r['action']) for r in counts if r['hour'] == onset and r['marker'] == 'M1'})
        p(f'  M1 events in it: {n(onset, "M1")} ({"; ".join(f"{t} {a}" for t, a in types)})')
    for h in rng:
        if h2dt(h) >= h2dt(onset or last):
            break
        if h not in hours:
            p(f'  earlier hour {h} unavailable: onset could be earlier')
    vs = VENDOR_START_HOUR
    p(f'vendor start hour {vs} (12:00 to 13:00 UTC, 10 November): '
      + ('unavailable' if vs not in hours else
         f'held, gap hour {int(gap[vs])}; M1 PR events {n(vs, "M1", "PullRequestEvent")}, '
         f'M1 review events {n(vs, "M1", "PullRequestReviewEvent")}, M1 Create/Delete/Push '
         f'{fmt(n(vs, "M1", "CreateEvent"))}/{fmt(n(vs, "M1", "DeleteEvent"))}/{fmt(n(vs, "M1", "PushEvent"))}'))
    if onset:
        before_unknown = [h for h in span(FIRST_HOUR, dt2h(h2dt(onset) - timedelta(hours=1))) if h in hours and gap[h]]
        p(f'  held hours before onset that are gap hours (M1 Create/Delete/Push unknown there): {len(before_unknown)}'
          f' of {len(span(FIRST_HOUR, onset)) - 1}')
    p('')

    # ---- Measure 3 -------------------------------------------------------------------------------------------
    p('== Measure 3: probe coverage ==')
    p('M1 PullRequestEvent opened, summed over the hours covering each vendor\'s window; share of its search count.')
    p('Pre-set reading: >= 50% "most"; 10% to under 50% "a minority"; under 10% "a small fraction".')
    for vendor, a, b, denom, more_than in WINDOWS:
        hs = [h for h in span(a, b) if h2dt(h) <= h2dt(last)]
        held = [h for h in hs if h in hours]
        miss = len(span(a, b)) - len(held)
        s = sum(n(h, 'M1', 'PullRequestEvent', 'opened') for h in held)
        share = 100 * s / denom
        reading = 'most' if share >= 50 else ('a minority' if share >= 10 else 'a small fraction')
        p(f'{vendor}: hours {a} to {b} ({len(span(a, b))} hours; held {len(held)}, not held {miss})')
        p(f'  opened M1 PR events: {s}; search count {"more than " if more_than else ""}{denom}; '
          f'share {share:.2f}%{" (upper estimate)" if more_than else ""}; pre-set reading: {reading}')
        if miss > len(span(a, b)) / 4:
            p('  more than a quarter of the window not held: measure 3 not formed for this window')
    p('')

    # ---- Measure 4 -------------------------------------------------------------------------------------------
    p('== Measure 4: internal completeness ==')
    if onset:
        hs = [h for h in span(onset, M4_LAST) if h2dt(h) <= h2dt(last)]
        ng = [h for h in hs if h in hours and not gap[h]]
        p(f'hours {onset} to {M4_LAST}: {len(hs)}; held and not gap: {len(ng)}; gap or unavailable: {len(hs) - len(ng)}')
        p('hour          M1 CreateEvent  M1 PR opened')
        for h in ng:
            p(f'{h:<13} {n(h, "M1", "CreateEvent"):>14}  {n(h, "M1", "PullRequestEvent", "opened"):>12}')
        sc = sum(n(h, 'M1', 'CreateEvent') for h in ng)
        so = sum(n(h, 'M1', 'PullRequestEvent', 'opened') for h in ng)
        p(f'sum over non-gap hours: M1 CreateEvent {sc}; M1 PR opened {so}')
        so_gap = sum(n(h, 'M1', 'PullRequestEvent', 'opened') for h in hs if h in hours and gap[h])
        p(f'(for scale: M1 PR opened in the gap hours of the same span, where CreateEvent is unknown: {so_gap})')
    p('')

    # ---- Measure 5 -------------------------------------------------------------------------------------------
    p('== Measure 5: cleanup over time ==')
    p('By UTC day, 10 November to the last complete day (all 24 hours held). Opened, closed and the cumulative')
    p('ratio count M1 PullRequestEvent; DeleteEvent is M1, all ref_types, known only in non-gap hours.')
    p('Vendors: StepSecurity "about 90%" still open (07:40 UTC, 12 Nov); Aikido "92%" still open (no time).')
    p('day         hrs gap |  opened closed  reop other | delete(non-gap) | cum.opened cum.closed closed/opened')
    day = h2dt('2026-11-10-0')
    co = cc = 0
    while day <= h2dt(last):
        hs = span(dt2h(day), dt2h(day + timedelta(hours=23)))
        held = [h for h in hs if h in hours]
        complete = len(held) == 24
        g = sum(1 for h in held if gap[h])
        o = sum(n(h, 'M1', 'PullRequestEvent', 'opened') for h in held)
        c = sum(n(h, 'M1', 'PullRequestEvent', 'closed') for h in held)
        ro = sum(n(h, 'M1', 'PullRequestEvent', 'reopened') for h in held)
        ot = sum(n(h, 'M1', 'PullRequestEvent', 'other') for h in held)
        de = sum(n(h, 'M1', 'DeleteEvent') for h in held if not gap[h])
        if complete:
            co += o
            cc += c
            ratio = f'{100 * cc / co:.2f}%' if co else 'n/a'
            p(f'{day:%Y-%m-%d} {len(held):>4} {g:>3} | {o:>7} {c:>6} {ro:>5} {ot:>5} | {de:>15} | '
              f'{co:>10} {cc:>10} {ratio:>13}')
        else:
            p(f'{day:%Y-%m-%d} {len(held):>4} {g:>3} | {o:>7} {c:>6} {ro:>5} {ot:>5} | {de:>15} | '
              f'(incomplete day: shown, not in measure 5 or the cumulative columns)')
        day += timedelta(days=1)
    p('')

    # ---- Measure 6 -------------------------------------------------------------------------------------------
    p('== Measure 6: the branch shapes ==')
    p(f'Baseline {FIRST_HOUR} to {BASELINE_LAST}; after {VENDOR_START_HOUR} to {last}. Hourly counts by type over')
    p('the hours where the count is known (held; and not gap for Create/Delete/Push); zero hours included.')
    periods = [('baseline', span(FIRST_HOUR, BASELINE_LAST)), ('after', span(VENDOR_START_HOUR, last))]
    p('marker type                    period    known  total  median  min  max')
    for m in ('M2', 'M3'):
        for t in TYPES:
            for name, hs in periods:
                vals = [v for v in (n(h, m, t) for h in hs) if v is not None]
                if vals:
                    p(f'{m:<6} {t:<24} {name:<8} {len(vals):>6} {sum(vals):>6} {statistics.median(vals):>7g} '
                      f'{min(vals):>4} {max(vals):>4}')
                else:
                    p(f'{m:<6} {t:<24} {name:<8} {0:>6}      ?       ?    ?    ?')
    p('')

    # ---- Measure 7 -------------------------------------------------------------------------------------------
    p('== Measure 7: gap hours ==')
    if onset:
        hs = [h for h in span(onset, last) if h in hours]
        for label, sel in (('gap hours', [h for h in hs if gap[h]]), ('other hours', [h for h in hs if not gap[h]])):
            by = {a: sum(n(h, 'M1', 'PullRequestEvent', a) for h in sel) for a in ('opened', 'closed', 'reopened', 'other')}
            tot = sum(by.values())
            per = f'{tot / len(sel):.2f}' if sel else 'n/a'
            p(f'{label:<12} from onset {onset}: {len(sel):>3} hours; M1 PR events {tot} (opened {by["opened"]}, '
              f'closed {by["closed"]}, reopened {by["reopened"]}, other {by["other"]}); per hour {per}; '
              f'hours with any {sum(1 for h in sel if n(h, "M1", "PullRequestEvent"))}')
        for a, b in (('2026-11-10-12', '2026-11-12-23'), ('2026-11-13-0', last)):
            sel = [h for h in span(a, b) if h in hours and h2dt(h) >= h2dt(onset)]
            if not sel:
                continue
            gh = [h for h in sel if gap[h]]
            oh = [h for h in sel if not gap[h]]
            p(f'  within {max(a, onset, key=h2dt)} to {b}: gap {len(gh)} hours, M1 PR '
              f'{sum(n(h, "M1", "PullRequestEvent") for h in gh)}; other {len(oh)} hours, M1 PR '
              f'{sum(n(h, "M1", "PullRequestEvent") for h in oh)}')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
