"""LH044: tabulate a weekly read against an earlier read under the brief's measures 1 to 4 and 8.

Offline: reads only the kept classes.csv, robots.csv, usage_token.csv, readlog.csv and summary.json of
two reads, and the kept RDAP records under data/ (amendment 9's egress rule), and makes no request.
Written for read 1 (15 November 2026) by the read-1 subagent; the egress section added by amendment 9.

    python3 -I studies/LH044/scripts/compare_reads.py <earlier label> <later label>

Prints a plain-text report; the checkpoint keeps its output beside it.

Definitions (brief, Measures; Missing evidence):
- read: a service whose probe was answered (any class from the probe, excluding the unknown classes
  below) or whose robots.txt was itself walled (`wall_at_robots`);
- unknown: `unreachable`, `unread_proxy`, `robots_unreachable`, `robots_redirect`,
  `not_probed_host_cap`, `skipped_retry_after`; never open, never walled;
- declared: `robots_disallowed`, counted under measure 4, not a wall and not open;
- closing: `open` at the earlier read and walled at the later; opening: the reverse (measure 3).
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent.parent / 'data'
WALLS = {'challenge', 'login', 'rate_limited', 'refused', 'api_closed', 'wall_at_robots'}
UNKNOWN = {'unreachable', 'unread_proxy', 'robots_unreachable', 'robots_redirect',
           'not_probed_host_cap', 'skipped_retry_after'}
DECLARED = {'robots_disallowed'}
AI = ['GPTBot', 'ChatGPT-User', 'OAI-SearchBot', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot',
      'anthropic-ai', 'CCBot', 'Google-Extended', 'PerplexityBot', 'Perplexity-User', 'Bytespider',
      'Amazonbot', 'Applebot-Extended', 'meta-externalagent', 'cohere-ai', 'Diffbot']


def load(label):
    d = D / ('read-' + label)
    cls = {r['id']: r for r in csv.DictReader(open(d / 'classes.csv'))}
    rob = {r['id']: r for r in csv.DictReader(open(d / 'robots.csv'))}
    ut = d / 'usage_token.csv'
    usage = {r['id']: r for r in csv.DictReader(open(ut))} if ut.exists() else None
    log = list(csv.DictReader(open(d / 'readlog.csv')))
    summ = json.load(open(d / 'summary.json'))
    return cls, rob, usage, log, summ


def state(c):
    if c in WALLS:
        return 'wall'
    if c in UNKNOWN:
        return 'unknown'
    if c in DECLARED:
        return 'declared'
    return 'read'


def tally(cls):
    out = {}
    for s in ('named', 'drawn'):
        rows = [r for r in cls.values() if r['stratum'] == s]
        t = Counter()
        for r in rows:
            c = r['class']
            st = state(c)
            t['services'] += 1
            if c == 'wall_at_robots':
                t['wall_at_robots'] += 1
            elif st in ('read', 'wall'):
                t['probe_answered'] += 1
            if st in ('read', 'wall'):
                t['state_read'] += 1
            if st == 'wall':
                t['walled'] += 1
            if c == 'open':
                t['open'] += 1
            if c in ('open_unconfirmed', 'js_notice'):
                t['open_unconfirmed_or_js'] += 1
            if st == 'declared':
                t['robots_disallowed'] += 1
            if st == 'unknown':
                t['unknown'] += 1
                t['unknown:' + c] += 1
        out[s] = t
    return out


def by_class_group(cls):
    t = Counter()
    for r in cls.values():
        st = state(r['class'])
        if st in ('read', 'wall'):
            t[(r['stratum'], r['class_group'], 'read')] += 1
        if st == 'wall':
            t[(r['stratum'], r['class_group'], 'wall')] += 1
    return t


def robots_counts(rob):
    t = Counter()
    for r in rob.values():
        t['parsed'] += 1
        if r['star_root_allowed'] == 'False':
            t['star_root_disallowed'] += 1
        if r['lighthouse_probe_allowed'] == 'False':
            t['probe_disallowed_lighthouse_or_star'] += 1
        if r.get('obeyed_probe_allowed') == 'False':
            t['probe_disallowed_obeyed'] += 1
        if r['star_root_allowed'] == 'True' and any(r[a] == 'False' for a in AI):
            t['star_allows_root_but_ai_token_disallowed'] += 1
    return t


def _ip(a):
    return tuple(int(x) for x in a.split('.'))


def rdap_records():
    """Every kept RDAP network record under data/ (read-*/rdap/*.json, and the prebrief's p*.body):
    (start, end, net handle, registrant handle, registrant name)."""
    out = []
    for f in sorted(D.glob('read-*/rdap/*.json')) + sorted(D.glob('prebrief-*/p*.body')):
        try:
            d = json.loads(f.read_text())
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(d, dict) or d.get('objectClassName') != 'ip network' or ':' in d.get('startAddress', ':'):
            continue
        reg = [e for e in d.get('entities', []) if 'registrant' in (e.get('roles') or [])]
        name = ''
        if reg:
            name = ' '.join(v[3] for v in (reg[0].get('vcardArray') or [None, []])[1] if v[0] == 'fn')
        out.append((_ip(d['startAddress']), _ip(d['endAddress']), d.get('handle', ''),
                    reg[0].get('handle', '') if reg else '', name))
    return out


def registrant(addr, recs):
    """The registrant organisation of the most specific kept record covering addr, or None."""
    a = _ip(addr)
    cover = [r for r in recs if r[0] <= a <= r[1]]
    if not cover:
        return None
    r = min(cover, key=lambda r: [y - x for x, y in zip(r[0], r[1])])
    return '%s (%s)' % (r[3], r[4]) if r[3] else r[2]


def egress(sa, sb, recs=None):
    """Amendment 9 (16 November 2026, post hoc, after read 1): within each route, the egress is the set
    of registrant organisations of the addresses that route echoed; it changed between two reads when
    both reads echoed on the route, every address is covered by a kept RDAP record, and the two sets
    differ. A route with no echo at either read is 'unread', never a change. A registered network
    within the same registrant (NET-34-128 to NET-35-184, both Google LLC) is not a change."""
    recs = rdap_records() if recs is None else recs
    ea, eb = sa.get('egress_ip_echoed', {}), sb.get('egress_ip_echoed', {})
    out = {}
    for rt in sorted(set(ea) | set(eb)):
        ra = {a: registrant(a, recs) for a in ea.get(rt, [])}
        rb = {a: registrant(a, recs) for a in eb.get(rt, [])}
        unknown = sorted(a for a, r in list(ra.items()) + list(rb.items()) if r is None)
        sa_, sb_ = sorted(set(ra.values()) - {None}), sorted(set(rb.values()) - {None})
        if not ra or not rb:
            verdict = 'unread at one read (not a change)'
        elif unknown:
            verdict = 'undecided until the unknown addresses are looked up'
        elif sa_ != sb_:
            verdict = 'CHANGED: classes on this route are not compared'
        else:
            verdict = 'unchanged'
        out[rt] = {'earlier': sa_, 'later': sb_, 'unknown': unknown, 'verdict': verdict}
    return out


def main(a, b):
    ca, ra, ua, la, sa = load(a)
    cb, rb, ub, lb, sb = load(b)
    print('LH044 compare_reads: %s against %s' % (b, a))
    print('classifier: %s then %s' % (sa.get('classifier'), sb.get('classifier')))
    print('provider at later read: %s' % sb.get('provider'))
    print()
    print('== Measure 1 and 2: tally by stratum (later read; earlier in brackets) ==')
    ta, tb = tally(ca), tally(cb)
    keys = ['services', 'probe_answered', 'wall_at_robots', 'state_read', 'walled', 'open',
            'open_unconfirmed_or_js', 'robots_disallowed', 'unknown']
    for s in ('named', 'drawn'):
        print(s + ': ' + ', '.join('%s %d (%d)' % (k, tb[s][k], ta[s][k]) for k in keys))
        unk = sorted(k for k in set(tb[s]) | set(ta[s]) if k.startswith('unknown:'))
        print('   ' + ', '.join('%s %d (%d)' % (k, tb[s][k], ta[s][k]) for k in unk))
        n = tb[s]['services']
        print('   unknown share %d/%d = %.3f (inconclusive above 0.2)' % (tb[s]['unknown'], n, tb[s]['unknown'] / n))
    allunk = tb['named']['unknown'] + tb['drawn']['unknown']
    alln = tb['named']['services'] + tb['drawn']['services']
    print('panel unknown share %d/%d = %.3f' % (allunk, alln, allunk / alln))
    ans = tb['named']['state_read'] + tb['drawn']['state_read']
    ou = tb['named']['open_unconfirmed_or_js'] + tb['drawn']['open_unconfirmed_or_js']
    print('open_unconfirmed or js_notice among read: %d/%d' % (ou, ans))
    print()
    print('By class of service, walled/read (later; earlier in brackets):')
    ga, gb = by_class_group(ca), by_class_group(cb)
    groups = sorted({(k[0], k[1]) for k in list(ga) + list(gb)})
    for s, g in groups:
        print('  %s %s: %d/%d (%d/%d)' % (s, g, gb[(s, g, 'wall')], gb[(s, g, 'read')],
                                          ga[(s, g, 'wall')], ga[(s, g, 'read')]))
    print()
    print('By stratum and route of the later read (class counts):')
    for k, v in sorted(sb.get('by_stratum_route', {}).items()):
        w = sum(n for c, n in v.items() if c in WALLS)
        r = sum(n for c, n in v.items() if state(c) in ('read', 'wall'))
        print('  %s: walled %d of %d read; %s' % (k, w, r, dict(sorted(v.items()))))
    print()
    print('== Walls at the later read ==')
    for i, r in sorted(cb.items()):
        if r['class'] in WALLS:
            print('  %s %s %s %s status=%s was=%s | %s' % (i, r['stratum'], r['host'], r['class'], r['status'],
                                                         ca[i]['class'], r['detail'][:120]))
    print()
    print('== Measure 3: changes (both bracketing reads known) ==')
    closings, openings, newly_walled, other = [], [], [], []
    for i in sorted(cb):
        x, y = ca[i]['class'], cb[i]['class']
        if x == 'open' and y in WALLS:
            closings.append(i)
        if x in WALLS and y == 'open':
            openings.append(i)
        if y in WALLS and x not in WALLS:
            newly_walled.append(i)
        if x != y:
            other.append(i)
    for name, ids in (('closings', closings), ('openings', openings),
                      ('walled now, not walled at earlier read (any earlier class)', newly_walled)):
        print('%s: %d' % (name, len(ids)))
        for i in ids:
            print('  %s %s %s: %s -> %s' % (i, cb[i]['stratum'], cb[i]['host'], ca[i]['class'], cb[i]['class']))
    walls_gone = [i for i in sorted(cb) if ca[i]['class'] in WALLS and cb[i]['class'] not in WALLS]
    print('walled at earlier read, not walled now (any later class): %d' % len(walls_gone))
    for i in walls_gone:
        print('  %s %s %s: %s -> %s | %s' % (i, cb[i]['stratum'], cb[i]['host'], ca[i]['class'], cb[i]['class'],
                                            cb[i]['detail'][:100]))
    print()
    print('All class changes: %d' % len(other))
    trans = Counter((ca[i]['class'], cb[i]['class']) for i in other)
    for (x, y), n in sorted(trans.items(), key=lambda kv: (-kv[1], kv[0])):
        print('  %s -> %s: %d  [%s]' % (x, y, n, ' '.join(i for i in other if (ca[i]['class'], cb[i]['class']) == (x, y))))
    print()
    print('== Measure 4: robots.txt declarations ==')
    qa, qb = robots_counts(ra), robots_counts(rb)
    for k in sorted(set(qa) | set(qb)):
        print('  %s: %d (%d)' % (k, qb[k], qa[k]))
    both = sorted(set(ra) & set(rb))
    print('  parsed at both reads: %d; only earlier: %s; only later: %s' % (
        len(both), ' '.join(sorted(set(ra) - set(rb))), ' '.join(sorted(set(rb) - set(ra)))))
    cols = ['lighthouse_probe_allowed', 'star_root_allowed', 'star_probe_allowed'] + AI
    ch = 0
    for i in both:
        diffs = ['%s %s->%s' % (c, ra[i][c], rb[i][c]) for c in cols if ra[i][c] != rb[i][c]]
        if diffs:
            ch += 1
            print('  change %s %s: %s' % (i, rb[i]['host'], '; '.join(diffs)))
    print('  services parsed at both reads with any measure-4 change: %d' % ch)
    tok = Counter()
    for r in rb.values():
        if r['star_root_allowed'] == 'True':
            for t in AI:
                if r[t] == 'False':
                    tok[t] += 1
    print('  later read, among files allowing * at /, files disallowing each token at /:',
          dict(sorted(tok.items(), key=lambda kv: -kv[1])))
    obeyed = [i for i, r in rb.items() if r.get('obeyed_probe_allowed') == 'False']
    print('  later read, probe withheld under the obeyed rule (amendment 5): %d' % len(obeyed))
    for i in sorted(obeyed):
        print('    %s %s %s | %s' % (i, cb[i]['stratum'], rb[i]['host'], rb[i].get('obeyed_decided_by', '')[:110]))
    print()
    print('== Measure 4, entry 18: __usage_ai-training ==')
    for lab, u in ((a, ua), (b, ub)):
        if u is None:
            print('  %s: no usage_token.csv' % lab)
            continue
        named = [r for r in u.values() if r['usage_token_named'] == 'True']
        ment = [r for r in u.values() if r['usage_token_mentioned'] == 'True']
        print('  %s: %d files parsed, %d with a group naming the token, %d mentioning it anywhere' % (
            lab, len(u), len(named), len(ment)))
        for r in named:
            c = (cb if lab == b else ca)[r['id']]
            print('    %s %s %s root_allowed=%s rules=%s' % (r['id'], c['stratum'], r['host'],
                                                          r['usage_token_root_allowed'], r['usage_token_rules'][:80]))
    print()
    print('== Measure 8: our own load (later read) ==')
    hosts = Counter()
    for r in lb:
        from urllib.parse import urlsplit
        hosts[(urlsplit(r['url']).hostname or '').lower()] += 1
    print('  requests %d (readlog rows %d), bytes retained %s, max to one host %s (readlog: %d), routes %s' % (
        sb.get('requests'), len(lb), sb.get('bytes_retained'), sb.get('max_requests_to_one_host'),
        max(hosts.values()), sb.get('routes')))
    print('  kinds:', dict(Counter(r['kind'] for r in lb)))
    print('  earlier read: requests %s, bytes %s, max %s' % (sa.get('requests'), sa.get('bytes_retained'),
                                                            sa.get('max_requests_to_one_host')))
    print()
    print('== Egress (inconclusive rule, within route) ==')
    print('  earlier:', sa.get('echoed_blocks_16'), sa.get('egress_ip_echoed'))
    print('  later:  ', sb.get('echoed_blocks_16'), sb.get('egress_ip_echoed'))
    print('  amendment 9 (registrant organisation of each echoed address, from kept RDAP records):')
    for rt, v in sorted(egress(sa, sb).items()):
        print('    %s: earlier %s; later %s -> %s' % (rt, v['earlier'], v['later'], v['verdict']))
        if v['unknown']:
            print('      no kept RDAP record covers %s: look it up once (rdap.arin.net) and keep it in the'
                  ' later read\'s rdap/' % ', '.join(v['unknown']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
