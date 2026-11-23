"""LH047 re-audit of ISO week 2026-W47: judge every request in requests.csv under the brief's section 5
as fixed, Amendment 1 (R8 classes, R5 with and without robots.txt reads, reporting by request and by
practice) and Amendment 2 (the keeper's rule of 8 November as implemented by scripts/robots_rules.py and
scripts/robots_tokens.json at Amendment 2's commit f4eb46a, frozen in code/frozen_f4eb46a/). Offline:
reads requests.csv, the robots.txt copies retained in the week (read from git objects of the population
commit), the current re-reads in robots-current/, and ai.robots.txt's list as read for the brief.

Run from the repository root:
  python3 -I studies/LH047/data/reaudit-2026-W47/code/audit.py <population-commit>
Writes requests-judged.csv and summary.json; tabulate.py makes tables.md.

Context columns, not verdicts of the fixed protocol (the keeper's decision of 21 November 2026, made
during the week and after Amendment 2): K21_oneoff (robots_rules at the population commit, access
'oneoff', for rows whose log records access=oneoff) and K21_keep (its may_keep, for 2xx page rows after
the decision's commit at 2026-11-21T15:23:17Z whose body is kept in the repository).
"""
import csv, gzip, hashlib, importlib.util, json, os, re, subprocess, sys
from datetime import datetime
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, 'studies/LH047/scripts'))
import robots9309 as R9  # noqa: E402  the brief's R1/R2 evaluator, unchanged


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K8 = load('rr_f4eb46a', os.path.join(HERE, 'frozen_f4eb46a/robots_rules.py'))   # the keeper's rule of 8 November, at Amendment 2
K21 = load('rr_e74c302', os.path.join(HERE, 'frozen_e74c302/robots_rules.py'))  # as at the population commit (21 November decision)
TOKEN = 'Lighthouse-research'
ANTHROPIC = ['anthropic-ai', 'ClaudeBot', 'Claude-Web', 'Claude-User', 'Claude-SearchBot', 'Claude-Code', 'Claude-Agent']
AI_TOKENS = [k for k in json.load(open(os.path.join(ROOT, 'studies/LH047/data/reads/catalogue-2/013.body'))) if not k.startswith('__')]
K21_TIME = '2026-11-21T15:23:17Z'
GITHUB = ('api.github.com', 'github.com', 'codeload.github.com')
CHALLENGE = re.compile(r'Just a moment|challenge|Checking your browser|captcha|Anubis|error code: 1010', re.I)


def t(s):
    return datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S')


def auth(u):
    s = urlsplit(u)
    return '%s://%s' % (s.scheme, s.netloc)


def show(commit, path):
    try:
        return subprocess.run(['git', 'show', '%s:%s' % (commit, path)], capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


# ------------------------------------------------------------------ robots.txt copies

def retained_copies(P, rows):
    """Copies kept in the week: LH044's robots.txt bodies (chains with redirects) and LH045's epoch robots.body."""
    out = {}
    lh044 = sorted([r for r in rows if r['log'].startswith('studies/LH044/') and r['kind'] == 'robots' and r['sent'] == 'yes'],
                   key=lambda r: (r['log'], int(r['n'] or 0)))
    prev = None  # (hop-0 authority, previous status) while a redirect chain is being followed
    for r in lh044:
        d = os.path.dirname(r['log'])
        body = show(P, '%s/%04d.b' % (d, int(r['n']))) if r['n'] else None
        c = dict(utc=r['utc'], study='LH044', status=r['status'], body=body, truncated=r['truncated'] == 'True',
                 file='%s/%04d.b' % (d, int(r['n'])), prov_log=r['log'])
        out.setdefault(auth(r['url']), []).append(c)
        if prev and state(prev[1]) == 'redirect':
            out.setdefault(prev[0], []).append(dict(c, via='redirect chain from ' + prev[0]))
            prev = (prev[0], r['status'])
        else:
            prev = (auth(r['url']), r['status'])
    for r in rows:
        if r['log'].startswith('studies/LH045/data/epoch/') and r['kind'] == 'robots' and r['sent'] == 'yes':
            p = os.path.dirname(r['log']) + '/robots.body'
            out.setdefault(auth(r['url']), []).append(dict(utc=r['utc'], study='LH045', status=r['status'], body=show(P, p),
                                                          truncated=False, file=p, prov_log=r['log']))
    return out


def current_copies():
    """LH047's current re-reads of 23 November (robots-current/readlog.csv): chains by starting authority."""
    p = os.path.join(D, 'robots-current/readlog.csv')
    chains, cur = {}, None
    for r in csv.DictReader(open(p, newline='')):
        hop = int(r['note'].split()[-1])
        safe = urlsplit(r['url']).netloc.replace(':', '_')
        f = os.path.join(D, 'robots-current/robots-%s-%d.txt' % (safe, hop))
        body = open(f, 'rb').read() if os.path.exists(f) else None
        c = dict(utc=r['utc'], study='LH047-current', status=r['status'], body=body, truncated=False,
                 file=os.path.relpath(f, ROOT), sha=r['sha256_received'], url=r['url'])
        if hop == 0:
            cur = auth(r['url'])
            chains[cur] = [c]
        else:
            chains[cur].append(c)
    return chains


def state(code):
    try:
        c = int(code)
    except (TypeError, ValueError):
        return 'unreachable'
    if 200 <= c < 300:
        return 'parsed'
    if 300 <= c < 400:
        return 'redirect'
    if 400 <= c < 500:
        return 'unavailable'
    return 'unreachable'


LOGGED_STATUS = re.compile(r'robots\.txt answered (\d{3})')


def logged_robots_status(r, explicit):
    st = r['robots_logged_status']
    if not st:
        m = LOGGED_STATUS.search(r['gate_reason'])
        st = m.group(1) if m else ''
    if not st:
        st = explicit.get((r['log'], auth(r['url'])), '')
    return st


def pick(r, explicit, kept, cur):
    """(copy or state, provenance) for a page request, by the brief's order (section 4, Amendment 1)."""
    a = auth(r['url'])
    st = logged_robots_status(r, explicit)
    if st and st not in ('200',):
        return dict(status=st, body=None, file='', utc=r['utc'], truncated=False), 'robots.txt status logged at the time by the same log'
    rt = t(r['utc'])
    cands = [c for c in kept.get(a, []) if (state(c['status']) == 'parsed' and c['body'] is not None) or state(c['status']) == 'unavailable']
    same = [c for c in cands if c['study'] == r['study'] and t(c['utc']) <= rt]
    if same:
        return max(same, key=lambda c: t(c['utc'])), 'retained, same study'
    if cands:
        c = min(cands, key=lambda c: abs((t(c['utc']) - rt).total_seconds()))
        return c, ('retained, same study, read after the request' if c['study'] == r['study'] else 'retained in the week, other study')
    hops = cur.get(a)
    if hops:
        last = hops[-1]
        sha_t = r['robots_logged_sha256']
        lab = 'current re-read (not the file in force at the time)'
        if sha_t and len(hops) == 1 and last['sha'] == sha_t:
            lab = 'current re-read, bytes identical to the file read at the time (sha256)'
        elif sha_t:
            lab = 'current re-read, bytes differ from the file read at the time (sha256)'
        return last, lab
    return None, 'none'


def judge(r, copy, prov):
    p = urlsplit(r['url'])
    full = (p.path or '/') + ('?' + p.query if p.query else '')
    res = dict(robots_prov=prov, robots_file=copy['file'] if copy else '', robots_status=copy['status'] if copy else '',
               R1='', R1_rule='', R2='', R2_agent='', R2_tokens='', R3='', R3_tokens='', K8='', K8_rule='', signal='', crawl_delay='')
    if copy is None:
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = 'unknown'
        res['R1_rule'] = 'no robots.txt copy'
        return res
    s = state(copy['status'])
    if s == 'unreachable':
        cur = prov.startswith('current')
        v = 'unknown' if cur else 'does not comply'
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = v
        res['R1_rule'] = 'robots.txt unreachable now; state at the time unread' if cur else \
            'robots.txt unreachable at the time: complete disallow (RFC 9309 2.3.1.4)'
        return res
    if s == 'unavailable':
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = 'complies'
        res['R1_rule'] = 'robots.txt %s: no rules (RFC 9309 2.3.1.3)' % copy['status']
        return res
    if s == 'redirect':
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = 'unknown'
        res['R1_rule'] = 'robots.txt redirect not resolved'
        return res
    body = copy['body'] or b''
    if CHALLENGE.search(body[:4096].decode('utf-8', 'replace')) and b'user-agent' not in body.lower():
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = 'unknown'
        res['R1_rule'] = 'robots.txt answered with a challenge page: unread'
        return res
    text = body.decode('utf-8', 'replace')
    groups = R9.parse(text)
    applied, how = R9.groups_for(groups, TOKEN)
    ok, rule = R9.decide(applied, full)
    res['signal'] = ' | '.join(R9.extras(applied, 'content-signal') + ['content-usage: ' + v for v in R9.extras(applied, 'content-usage')])
    res['crawl_delay'] = ' '.join(R9.extras(applied, 'crawl-delay'))
    if copy.get('truncated'):
        for k in ('R1', 'R2', 'R2_agent', 'K8'):
            res[k] = 'unknown'
        res['R1_rule'] = 'copy cut short; the rule could lie beyond the cut'
        return res
    res['R1'] = 'complies' if ok else 'does not comply'
    res['R1_rule'] = '%s group: %s' % (how, rule or 'no matching rule')
    bad = []
    for tok in ANTHROPIC:
        ap, h2 = R9.groups_for(groups, tok, fallback=False)
        if h2 == 'token' and not R9.decide(ap, full)[0]:
            bad.append(tok)
    res['R2_tokens'] = ' '.join(bad)
    res['R2'] = 'does not comply' if (not ok or bad) else 'complies'
    res['R2_agent'] = 'does not comply' if (not ok or [b for b in bad if b in ('Claude-User', 'Claude-Agent', 'Claude-Code')]) else 'complies'
    ai = [tok for tok in AI_TOKENS if R9.groups_for(groups, tok, fallback=False)[1] == 'token'
          and not R9.decide(R9.groups_for(groups, tok, fallback=False)[0], full)[0]]
    res['R3'] = 'some AI token disallowed' if ai else 'no AI token disallowed'
    res['R3_tokens'] = str(len(ai))
    d = K8.decide(body, r['url'], provider=(r['provider'] or None))
    res['K8'] = 'complies' if d.allowed else 'does not comply'
    res['K8_rule'] = '%s: %s' % (d.decided_by, d.rule)
    res['_body'] = body
    return res


def main():
    P = sys.argv[1]
    rows = list(csv.DictReader(open(os.path.join(D, 'requests.csv'), newline='')))
    tree = set(subprocess.run(['git', 'ls-tree', '-r', '--name-only', '--full-tree', P], capture_output=True, text=True,
                              check=True).stdout.split('\n'))
    explicit = {(r['log'], auth(r['url'])): r['status'] for r in rows if r['kind'] == 'robots' and r['sent'] == 'yes' and r['status']
                and not r['status'].startswith('3')}
    kept, cur = retained_copies(P, rows), current_copies()
    out = []
    for r in rows:
        x = dict(r)
        sent = r['sent'] == 'yes' or r['sent'] == 'implicit robots read'
        x['counted'] = 'audited' if sent and r['kind'] in ('page', 'robots') else (
            'apart: refused by the gate' if r['sent'].startswith('no: refused') else (
                'apart: search' if r['kind'] == 'search' else 'apart: ' + r['sent']))
        if x['counted'] != 'audited':
            out.append(x)
            continue
        # use of the body (R4) and whether it is kept
        path = urlsplit(r['url']).path.lower()
        machine = bool(re.search(r'\.(json|gz|zip|csv|xml|txt|yaml|rss|atom|pdf)$', path) or '/api' in path or 'rss' in path or 'feed' in path
                       or r['method'] == 'POST' or r['host'] in ('data.gharchive.org', 'registry.npmjs.org', 'api.npmjs.org', 'api.osv.dev',
                                                                   'services.nvd.nist.gov', 'cveawg.mitre.org', 'sql-clickhouse.clickhouse.com',
                                                                   'packagist.org', 'api.wordpress.org', 'storage.googleapis.com'))
        x['use'] = 'robots' if r['kind'] == 'robots' else ('agent-read' if (r['log'].startswith('notes/') or 'handcoded' in r['log']
                                                                          or not machine) else 'script')
        bk = r['body_kept'].lower()
        if bk.startswith('no') or 'deleted' in bk:
            kept_b = 'no'
        elif bk.startswith('yes'):
            kept_b = 'yes'
        elif r['file']:
            f = r['file'] if r['file'].startswith('studies/') else os.path.dirname(r['log']) + '/' + r['file']
            base = re.sub(r'\.(raw|body|b|html|pdf|txt|json)(\.gz)?$', '', f)
            if base + '.withheld.json' in tree or f.endswith(('.derived.json', '.withheld.json')) or base + '.derived.json' in tree:
                kept_b = 'no'
            elif f in tree or f + '.gz' in tree:
                kept_b = 'yes'
            else:
                kept_b = 'no'
        else:
            kept_b = 'unknown'
        x['kept'] = kept_b
        x['reached'] = 'no (refused by the container)' if r['host'] in GITHUB and r['status'] == '403' else (
            'status not recorded' if r['status'] == '' else ('no (no answer)' if r['status'].startswith(('error', 'reset')) else 'yes'))
        if r['kind'] == 'robots':
            res = dict(robots_prov='', robots_file='', robots_status='', R1='complies', R1_rule='robots.txt itself', R2='complies',
                       R2_agent='complies', R2_tokens='', R3='', R3_tokens='', K8='complies', K8_rule='/robots.txt is always allowed',
                       signal='', crawl_delay='')
        else:
            copy, prov = pick(r, explicit, kept, cur)
            res = judge(r, copy, prov)
            if x['reached'].startswith('no (refused'):
                for k in ('R1', 'R2', 'R2_agent', 'K8'):
                    res[k] = 'unknown'
                res['R1_rule'] = "answered by this container's GitHub policy; GitHub not reached"
        body = res.pop('_body', None)
        x.update(res)
        # R4 usage preferences
        sig = x['signal'].lower().replace(' ', '')
        if not sig:
            x['R4'], x['R4_why'] = 'not applicable', ''
        else:
            why = []
            if ('ai-input=no' in sig or 'ai-use=n' in sig) and x['use'] == 'agent-read':
                why.append('ai-input/ai-use refused and the body was read by a model')
            m = re.search(r'use=(immediate|reference|full)', sig)
            if m and m.group(1) in ('immediate', 'reference') and kept_b == 'yes' and r['status'].startswith('2'):
                why.append('use=%s and the full body is kept in the public repository' % m.group(1))
            if kept_b == 'unknown' and m and m.group(1) in ('immediate', 'reference') and r['status'].startswith('2'):
                x['R4'], x['R4_why'] = 'unknown', 'use=%s; whether the body is kept is not known' % m.group(1)
            else:
                x['R4'], x['R4_why'] = ('does not comply' if why else 'complies'), '; '.join(why)
        # R8 identification (Amendment 1)
        x['R8'] = r['ua_class'] or 'unknown'
        # R7 terms (section 4: only where a Lighthouse record quotes them)
        if r['host'] == 'epoch.ai':
            x['R7'], x['R7_why'] = 'complies', "Epoch's data are free to use with attribution (LH045 brief); kept with attribution"
        else:
            x['R7'], x['R7_why'] = 'terms not read', ''
        # context: the keeper's 21 November decision (not a verdict of the fixed protocol)
        x['K21_oneoff'] = ''
        if r['access'].startswith('oneoff') and body is not None:
            d = K21.decide(body, r['url'], provider=(r['provider'] or None), access='oneoff')
            x['K21_oneoff'] = 'allowed' if d.allowed else 'refused'
        x['K21_keep'] = ''
        if r['kind'] == 'page' and r['utc'] >= K21_TIME[:19] and r['status'].startswith('2') and kept_b == 'yes':
            if body is not None:
                ok, why = K21.may_keep(body, r['url'])
                x['K21_keep'] = 'may keep' if ok else 'kept against the rule: ' + why
            elif state(x.get('robots_status', '')) == 'unavailable':
                x['K21_keep'] = 'may keep (robots.txt %s)' % x['robots_status']
            else:
                x['K21_keep'] = 'unknown'
        out.append(x)
    aud = [x for x in out if x['counted'] == 'audited']
    # R6 walls: a wall is 429, 401, or 403/503 with a challenge marker visible in the log; later requests to the same URL
    for x in aud:
        st, note = x['status'], (x['gate_reason'] + ' ' + x['note'])
        x['wall'] = ''
        if st in ('429', '401'):
            x['wall'] = 'wall (%s)' % st
        elif st in ('403', '503') and CHALLENGE.search(note):
            x['wall'] = 'wall (%s, challenge named in the log)' % st
        elif st in ('403', '503', '402'):
            x['wall'] = 'refusal %s (no challenge marker in the log)' % st
        x['R6'], x['R6_why'] = 'complies', ''
    srt = sorted(aud, key=lambda x: (x['utc'], x['id']))
    for i, x in enumerate(srt):
        if not x['wall'].startswith('wall'):
            continue
        for y in srt[i + 1:]:
            if y['url'] == x['url']:
                same_day = y['utc'][:10] == x['utc'][:10]
                y['R6'] = 'does not comply'
                y['R6_why'] = (y['R6_why'] + '; ' if y['R6_why'] else '') + 'same URL after %s at %s (%s; %s)' % (
                    x['wall'], x['utc'], x['practice'], 'same day' if same_day else 'a later day')
            elif y['host'] == x['host'] and y['ua'] != x['ua'] and y['ua'] and x['ua']:
                y['R6'] = 'does not comply'
                y['R6_why'] = (y['R6_why'] + '; ' if y['R6_why'] else '') + 'another User-Agent to the host after a wall at %s' % x['utc']
    # R5 Crawl-delay, per study and host; with and without robots.txt reads (Amendment 1)
    by = {}
    for x in aud:
        by.setdefault((x['study'], x['host']), []).append(x)
    for (study, host), xs in by.items():
        xs.sort(key=lambda x: (x['utc'], 0 if x['kind'] == 'robots' else 1, x['id']))
        cd = next((x['crawl_delay'] for x in xs if x['crawl_delay']), '')
        try:
            need = max(float(v) for v in cd.split()) if cd else None  # several Crawl-delay lines in the applicable groups: the strictest
        except ValueError:
            need = None
        ts = [t(x['utc']) for x in xs]
        gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
        mx, j = 0, 0
        for i in range(len(ts)):
            while (ts[i] - ts[j]).total_seconds() >= 60:
                j += 1
            mx = max(mx, i - j + 1)
        prev_all = prev_pages = None
        for x in xs:
            x['R5'], x['R5_why'], x['R5_excl_robots'] = 'complies', '', 'complies'
            if need is not None and prev_all is not None:
                g = (t(x['utc']) - t(prev_all['utc'])).total_seconds()
                if g < need:
                    if prev_all['utc_precision'] != 'second' or x['utc_precision'] != 'second':
                        x['R5'], x['R5_why'] = 'unknown', 'Crawl-delay %s; the previous request\'s time is not logged to the second (%s)' % (
                            cd, prev_all['utc_precision'])
                    else:
                        x['R5'], x['R5_why'] = 'does not comply (advisory)', 'Crawl-delay %s; %.0f s after the previous request' % (cd, g)
            if need is not None and x['kind'] != 'robots' and prev_pages is not None:
                g = (t(x['utc']) - t(prev_pages['utc'])).total_seconds()
                if g < need:
                    x['R5_excl_robots'] = 'unknown' if x['utc_precision'] != 'second' or prev_pages['utc_precision'] != 'second' \
                        else 'does not comply (advisory)'
            prev_all = x
            if x['kind'] != 'robots':
                prev_pages = x
        for x in xs:
            x['host_n'], x['host_max60'], x['host_min_gap'] = len(xs), mx, ('%.0f' % min(gaps)) if gaps else ''
    # overall verdicts: A (R1), B (R2), K8 (the keeper's rule of 8 November in R1's place)
    for x in aud:
        for name, rk in (('A', 'R1'), ('B', 'R2'), ('K8', 'K8')):
            vs = [x[rk], x['R4'], x['R5'], x['R6'], x['R7'], x['R8']]
            if any(v.startswith('does not comply') for v in vs):
                x['overall_' + name] = 'does not comply'
            elif x[rk] == 'unknown' or x['R8'] == 'unknown' or x['R4'] == 'unknown' or x['R5'] == 'unknown':
                x['overall_' + name] = 'unknown'
            else:
                x['overall_' + name] = 'complies'
    fields = ['id', 'counted', 'log', 'practice', 'study', 'run', 'kind', 'method', 'url', 'host', 'utc', 'utc_precision', 'status',
              'reached', 'sent', 'provider', 'access', 'ua', 'use', 'kept', 'robots_logged_status', 'robots_logged_sha256', 'gate_reason',
              'robots_prov', 'robots_file', 'robots_status', 'R1', 'R1_rule', 'R2', 'R2_agent', 'R2_tokens', 'R3', 'R3_tokens', 'K8',
              'K8_rule', 'signal', 'R4', 'R4_why', 'crawl_delay', 'host_n', 'host_max60', 'host_min_gap', 'R5', 'R5_why', 'R5_excl_robots',
              'wall', 'R6', 'R6_why', 'R7', 'R7_why', 'R8', 'overall_A', 'overall_B', 'overall_K8', 'K21_oneoff', 'K21_keep',
              'collector', 'collector_version', 'collector_flag', 'gated_in_code', 'note']
    with open(os.path.join(D, 'requests-judged.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(sorted(out, key=lambda x: x['id']))
    print('rows', len(out), 'audited', len(aud))


if __name__ == '__main__':
    main()
