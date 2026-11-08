"""LH047 part C: judge every audited request against the rules fixed in brief.md section 5.
Offline: reads data/requests.csv, data/transcripts/adhoc-requests.csv, data/robots-index.csv,
the retained robots.txt copies they point to, and ai.robots.txt's robots.json as read for the
brief (data/reads/catalogue-2/013.body).

Run from the repository root:  python3 -I studies/LH047/scripts/audit.py
Writes data/audit/requests-judged.csv (one row per request, every rule) and
data/audit/needs-current.txt (authorities whose only copies are unusable and which have no
current copy yet). Prints nothing else of substance; tabulate.py makes the tables.
"""
import csv, json, os, re, sys
from datetime import datetime
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import robots9309 as R  # noqa: E402

ROOT = os.getcwd()
D = os.path.join(ROOT, 'studies/LH047/data')
OUT = os.path.join(D, 'audit')
TOKEN = 'Lighthouse-research'
AGENT_TOKENS = ['Claude-User', 'Claude-Agent', 'Claude-Code']  # Anthropic's agent and user-directed fetcher tokens
ANTHROPIC = ['anthropic-ai', 'ClaudeBot', 'Claude-Web', 'Claude-User', 'Claude-SearchBot', 'Claude-Code', 'Claude-Agent']
AI_TOKENS = [k for k in json.load(open(os.path.join(D, 'reads/catalogue-2/013.body'))) if not k.startswith('__')]


def t(s):
    return datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S')


def auth(url):
    u = urlsplit(url)
    return '%s://%s' % (u.scheme, u.netloc)


# --- who made each request, how it identified itself, and what its body was used for --------
LOG_UA = {'essays/what-the-watch-would-see/reader-review/fetch-log.tsv': 'research-reader'}
AGENT_READ_LOGS = ('studies/LH041/data/prebrief/web-log.psv', 'studies/LH041/review/web/log.psv',
                   'studies/LH042/', 'studies/LH043/', 'studies/LH044/data/prebrief', 'studies/LH044/data/statements',
                   'studies/LH045/data/before-the-brief', 'studies/LH046/data/sources/')
ROBOTS_FIRST = {  # does the collector behind this log read robots.txt before each host's first request?
    'studies/LH041/data/prebrief/web-log.psv': 'no', 'studies/LH041/data/2026-11-08T1910Z/requests.csv': 'no',
    'studies/LH041/review/web/log.psv': 'yes (urllib.robotparser)', 'studies/LH042/': 'yes (urllib.robotparser; 5xx read as allow)',
    'studies/LH043/': 'no (robots.txt read after the pages)', 'studies/LH044/data/prebrief': 'no',
    'studies/LH044/data/read': 'yes (own parser, first 64 KiB)', 'studies/LH044/data/statements': 'yes (own parser, first 64 KiB)',
    'studies/LH044/data/httparchive': 'yes', 'studies/LH044/data/wayback': 'yes',
    'studies/LH045/data/before-the-brief': 'no (robots.txt read in the same batch)', 'studies/LH045/data/epoch': 'yes (urllib.robotparser)',
    'studies/LH045/data/ietf': 'yes (urllib.robotparser)', 'studies/LH046/data/sources/': 'no (robots.txt read after the home page)',
    'studies/LH046/data/fetch-log.tsv': 'by hand before the run (searchlog)', 'studies/LH046/review/': 'by hand before the run (reviewer read robots.txt at 20:13)',
    'essays/': 'no',
}


def lookup(table, log, default=''):
    for k, v in table.items():
        if log.startswith(k):
            return v
    return default


def use_of(log, url):
    p = urlsplit(url).path.lower()
    if p.endswith('/robots.txt'):
        return 'robots'
    machine = re.search(r'\.(json|gz|zip|csv|xml|txt|yaml|md|pdf)$', p) or '/api' in p or p.startswith('/pypi/') \
        or urlsplit(url).hostname in ('registry.npmjs.org', 'data.gharchive.org', 'api.osv.dev', 'datatracker.ietf.org')
    if log.startswith('transcript:'):
        return 'script' if machine else 'agent-read'
    if any(log.startswith(a) for a in AGENT_READ_LOGS) or log.startswith('essays/'):
        return 'script' if (machine and not p.endswith('.pdf')) else 'agent-read'
    return 'script'


def load_requests():
    reqs = []
    logged = list(csv.DictReader(open(os.path.join(D, 'requests.csv'), newline='')))
    for r in logged:
        if r['sent'] != 'yes':
            continue
        reqs.append(dict(source='log', log=r['log'], who=r['study'], method=r['method'], url=r['url'], utc=r['utc'],
                         status=r['status'], ua=LOG_UA.get(r['log'], 'lighthouse'), note=r['note'], truncated=r['truncated']))
    for r in csv.DictReader(open(os.path.join(D, 'transcripts/adhoc-requests.csv'), newline='')):
        dup = [x for x in logged if x['url'] == r['url'] and abs((t(x['utc']) - t(r['utc'])).total_seconds()) <= 15]
        if dup:
            continue  # the same request is in a fetch log
        if urlsplit(r['url']).hostname == 'lighthouse.harbour.cat':
            continue  # Lighthouse's own site: not an audited third party
        reqs.append(dict(source='transcript', log='transcript:' + r['transcript'], who=r['transcript'].split('(')[-1].rstrip(')'),
                         method=r['method'], url=r['url'], utc=r['utc'], status=r['status'], ua=r['ua'], note=r['note']))
    return reqs


# --- robots.txt copies ----------------------------------------------------------------------
def load_copies():
    copies = {}
    for r in csv.DictReader(open(os.path.join(D, 'robots-index.csv'), newline='')):
        copies.setdefault(r['authority'], []).append(r)
    # robots.txt states seen only in transcripts (not retained as files)
    copies.setdefault('https://dashboard.shadowserver.org', []).insert(0, dict(
        authority='https://dashboard.shadowserver.org', utc='2026-11-08T19:01:07Z', study='transcript', status='error:reset',
        file='', truncated='False', source_log='transcript a6843267 line 91'))
    return copies


STUDY_OF_LOG = lambda log: log.split('/')[1] if log.startswith('studies/') else log


def resolve_chain(copy, copies, depth=0):
    """Follow a retained robots.txt redirect through LH047's current re-read hops of the same chain."""
    return copy


CONTAINER_TEXT = (b'not enabled for this session', b'sessions are bound to their configured repositories')


def state_of(copy):
    st = copy['status']
    if copy.get('file') and st == '403':
        try:
            if any(x in open(os.path.join(ROOT, copy['file']), 'rb').read(4096) for x in CONTAINER_TEXT):
                return 'container'
        except OSError:
            pass
    if st.startswith('error') or st in ('', 'reset', 'timeout') or 'URLError' in st or 'Error' in st:
        return 'unreachable'
    try:
        code = int(st)
    except ValueError:
        return 'unreachable'
    if 200 <= code < 300:
        return 'parsed'
    if 300 <= code < 400:
        return 'redirect'
    if 400 <= code < 500:
        return 'unavailable'
    return 'unreachable'


_CHAINS = None


def current_chain(a, copies):
    """LH047's current re-read for authority a: the hops of its chain in the order read (a chain
    starts at hop 0 and may cross to other hosts); the last hop decides."""
    global _CHAINS
    if _CHAINS is None:
        _CHAINS = {}
        p = os.path.join(D, 'reads/robots-current/readlog.csv')
        cur = None
        for r in csv.DictReader(open(p, newline='')) if os.path.exists(p) else []:
            if r['robots_verdict'] != 'robots.txt':
                continue
            hop = int(r['note'].split()[-1])
            safe = urlsplit(r['url']).netloc.replace(':', '_')
            c = dict(authority=auth(r['url']), utc=r['utc'], study='LH047-current', status=r['status'],
                     file='studies/LH047/data/reads/robots-current/robots-%s-%d.txt' % (safe, hop), truncated='False', source_log=p)
            if hop == 0:
                cur = auth(r['url'])
                _CHAINS[cur] = [c]
            elif cur:
                _CHAINS[cur].append(c)
    return _CHAINS.get(a, [])


def pick_copy(req, copies):
    """Return (copy, provenance) for the request's authority, by the brief's order of preference."""
    a = auth(req['url'])
    if 'robots unreadable' in req.get('note', '') or re.search(r'robots=robots 5\d\d', req.get('note', '')):
        return dict(authority=a, utc=req['utc'], study=STUDY_OF_LOG(req['log']), status='error:collector note',
                    file='', truncated='False', source_log=req['log']), 'collector\'s own note at the time'

    rt = t(req['utc'])
    cands = [c for c in copies.get(a, []) if c['study'] != 'LH047-current']
    same = [c for c in cands if c['study'] == STUDY_OF_LOG(req['log']) and t(c['utc']) <= rt]
    usable = lambda c: state_of(c) != 'redirect'
    same = [c for c in same if usable(c)]
    if same:
        return max(same, key=lambda c: t(c['utc'])), 'retained, same study'
    other = [c for c in cands if usable(c)]
    if other:
        c = min(other, key=lambda c: abs((t(c['utc']) - rt).total_seconds()))
        lab = 'retained, same study, read after the request' if c['study'] == STUDY_OF_LOG(req['log']) else 'retained, other study'
        return c, lab
    hops = current_chain(a, copies)
    if hops:
        last = hops[-1]
        return last, 'current re-read (not the file in force at the time)'
    return None, 'none'


def judge_robots(req, copy, prov):
    """R1, R2, R3 and the R4 inputs for one request."""
    path = urlsplit(req['url']).path or '/'
    q = urlsplit(req['url']).query
    full = path + ('?' + q if q else '')
    res = dict(robots_prov=prov, robots_file=copy['file'] if copy else '', robots_status=copy['status'] if copy else '',
               R1='', R1_rule='', R2='', R2_agent='', R2_tokens='', R3='', R3_tokens='', signal='', crawl_delay='', near='')
    if path == '/robots.txt' and not q:
        res.update(R1='complies', R1_rule='robots.txt itself', R2='complies', R2_agent='complies', R3='')
        return res
    if copy is None:
        res.update(R1='unknown', R2='unknown', R2_agent='unknown', R1_rule='no robots.txt copy')
        return res
    st = state_of(copy)
    if st == 'unreachable':
        if prov.startswith('current'):
            res.update(R1='unknown', R2='unknown', R2_agent='unknown', R1_rule='robots.txt unreachable now; state at the time unread')
        else:
            res.update(R1='does not comply', R2='does not comply', R2_agent='does not comply', R1_rule='robots.txt unreachable at the time: complete disallow (RFC 9309 2.3.1.4)')
        return res
    if st == 'container':
        res.update(R1='unknown', R2='unknown', R2_agent='unknown', R1_rule="robots.txt refused by this container's own GitHub policy: unread")
        return res
    if st == 'unavailable':
        res.update(R1='complies', R2='complies', R2_agent='complies', R1_rule='robots.txt %s: no rules (RFC 9309 2.3.1.3)' % copy['status'])
        return res
    if st == 'redirect':
        res.update(R1='unknown', R2='unknown', R2_agent='unknown', R1_rule='robots.txt redirect not followed in any copy')
        return res
    text = open(os.path.join(ROOT, copy['file']), 'rb').read().decode('utf-8', 'replace')
    groups = R.parse(text)
    applied, how = R.groups_for(groups, TOKEN)
    ok, rule = R.decide(applied, full)
    res['signal'] = ' | '.join(R.extras(applied, 'content-signal') + ['content-usage: ' + v for v in R.extras(applied, 'content-usage')])
    res['crawl_delay'] = ' '.join(R.extras(applied, 'crawl-delay'))
    res['near'] = ' '.join(R.near_groups(groups, TOKEN))
    trunc = copy.get('truncated') == 'True'
    if trunc:
        res.update(R1='unknown', R2='unknown', R2_agent='unknown', R1_rule='copy cut at 64 KiB; the rule could lie beyond the cut (fragment says %s by %s)' % (
            'allow' if ok else 'disallow', rule))
        return res
    res['R1'] = 'complies' if ok else 'does not comply'
    res['R1_rule'] = '%s group: %s' % (how, rule if rule else 'no matching rule')
    bad = []
    for tok in ANTHROPIC:
        ap, h2 = R.groups_for(groups, tok, fallback=False)
        if h2 == 'token' and not R.decide(ap, full)[0]:
            bad.append(tok)
    res['R2_tokens'] = ' '.join(bad)
    res['R2_agent'] = 'does not comply' if (not ok or [b for b in bad if b in AGENT_TOKENS]) else 'complies'
    res['R2'] = 'does not comply' if (not ok or bad) else 'complies'
    ai = []
    for tok in AI_TOKENS:
        ap, h2 = R.groups_for(groups, tok, fallback=False)
        if h2 == 'token' and not R.decide(ap, full)[0]:
            ai.append(tok)
    res['R3'] = 'some AI token disallowed' if ai else 'no AI token disallowed'
    res['R3_tokens'] = str(len(ai))
    return res


def judge_signal(req, rob, kept):
    sig = rob['signal'].lower().replace(' ', '')
    if not sig:
        return 'not applicable', ''
    reasons = []
    use = req['use']
    if ('ai-input=no' in sig or 'ai-use=n' in sig) and use == 'agent-read':
        reasons.append('ai-input/ai-use refused and the body was read by a model')
    m = re.search(r'use=(immediate|reference|full)', sig)
    if m and m.group(1) in ('immediate', 'reference') and kept == 'yes' and req['status'].startswith('2'):
        # only a 2xx response collects content; an error page kept is not (a clarification made
        # after the first tabulation showed two 429 pages caught by the rule; see LH047.md, Method)
        reasons.append('use=%s and the full body is kept in the public repository' % m.group(1))
    return ('does not comply' if reasons else 'complies'), '; '.join(reasons)


def kept_in_repo(req):
    """Is the full body of this request kept in the repository? From the log's own file column."""
    log = req['log']
    if log.startswith('transcript:') or req['use'] == 'robots':
        return 'no' if log.startswith('transcript:') else 'yes'
    if log in ('studies/LH041/data/2026-11-08T1910Z/requests.csv', 'studies/LH046/data/fetch-log.tsv', 'studies/LH046/review/out/fetch-log.tsv'):
        return 'no (extracts or counts only)'
    if log.startswith('studies/LH045/data/before-the-brief'):
        name = req['note']
        withheld = {r['name'] for r in csv.DictReader(open(os.path.join(ROOT, 'studies/LH045/data/before-the-brief/withheld.csv')))
                    if r['name'] and not r['reason'].startswith('kept')}
        return 'no (withheld for its terms)' if name in withheld else 'yes'
    if log.startswith('essays/what-the-watch-would-see/reader-review') or log.startswith('essays/what-the-watch-would-see/claims-check'):
        base = os.path.dirname(os.path.join(ROOT, log))
        f = req['note'].split(' ')[0]
        return 'yes' if f and (os.path.exists(os.path.join(base, f)) or os.path.exists(os.path.join(base, 'data', f))) else 'no'
    if log.startswith('essays/what-the-watch-would-see/recheck'):
        f = req['note'].split(' ')[0]
        return 'yes' if os.path.exists(os.path.join(ROOT, 'essays/what-the-watch-would-see/recheck/data', f)) else 'no'
    if log.startswith('studies/LH044/'):
        return 'partial (cut at 64 KiB)' if req.get('truncated') == 'True' else 'yes'
    return 'yes'


WALL_MARKERS = (b'Just a moment', b'cf-mitigated', b'/.internal/challenge', b'Making sure you', b'captcha', b'challenge-form', b'cf-chl-')


def wall_of(req):
    st = req['status']
    if st in ('429', '401'):
        return 'wall (%s)' % st
    if req['log'].startswith('studies/LH044/data/read'):
        return ''  # LH044 walls come from its classes.csv, below
    if st in ('403', '503', '202'):
        return 'refusal %s (no challenge marker checked)' % st
    return ''


def main():
    reqs = load_requests()
    copies = load_copies()
    lh044 = {r['host']: r for r in csv.DictReader(open(os.path.join(ROOT, 'studies/LH044/data/read-2026-11-08T1920Z/classes.csv')))}
    need = set()
    rows = []
    for q in reqs:
        q['use'] = use_of(q['log'], q['url'])
        q['robots_first'] = lookup(ROBOTS_FIRST, q['log'], 'no (ad hoc command)' if q['source'] == 'transcript' else '')
        copy, prov = pick_copy(q, copies)
        if copy is None and urlsplit(q['url']).path != '/robots.txt':
            need.add(auth(q['url']))
        rob = judge_robots(q, copy, prov)
        kept = kept_in_repo(q)
        q.setdefault('truncated', '')
        r4, r4why = judge_signal(q, rob, kept.split(' ')[0])
        # R8 identification
        r8 = {'lighthouse': 'complies', 'curl-default': 'complies (unlabelled)', 'webfetch': 'unknown',
              'research-reader': 'does not comply (an unattributed name in a Mozilla string; classed after it was seen)'}[q['ua']]
        # walls (R6 inputs)
        w = wall_of(q)
        host = urlsplit(q['url']).hostname or ''
        if q['log'].startswith('studies/LH044/data/read') and host in lh044 and lh044[host]['wall'] == 'yes':
            at_robots = lh044[host]['class'] == 'wall_at_robots'
            if (urlsplit(q['url']).path == '/robots.txt') == at_robots:
                w = 'wall (%s)' % lh044[host]['class']
        reached = 'no (refused by the container)' if host in ('api.github.com', 'github.com', 'codeload.github.com') and q['status'] == '403' else (
            'no (no answer)' if q['status'] in ('reset', 'timeout') or 'rror' in q['status'] else (
                'status not recorded' if q['status'] == '' else 'yes'))
        if reached.startswith('no (refused'):
            rob = dict(rob, R1='unknown', R2='unknown', R2_agent='unknown', R1_rule="answered by this container's GitHub policy; GitHub not reached")
        rows.append(dict(source=q['source'], reached=reached, log=q['log'], who=q['who'], method=q['method'], url=q['url'], host=host, utc=q['utc'],
                         status=q['status'], ua=q['ua'], use=q['use'], kept=kept, robots_first=q['robots_first'], wall=w, **rob,
                         R4=r4, R4_why=r4why, R8=r8))
    # R6: a later request to the same URL after a wall, or to the same host with another User-Agent
    rows.sort(key=lambda r: (r['utc'], r['url']))
    for i, r in enumerate(rows):
        r['R6'] = 'complies'
        r['R6_why'] = ''
    for i, r in enumerate(rows):
        if r['wall'].startswith('wall') or r['wall'].startswith('refusal'):
            later = [x for x in rows[i + 1:] if x['url'] == r['url']]
            other_ua = [x for x in rows[i + 1:] if x['host'] == r['host'] and x['ua'] != r['ua']]
            for x in later:
                kind = 'R6' if r['wall'].startswith('wall') else 'refusal-context'
                if kind == 'R6':
                    x['R6'] = 'does not comply'
                x['R6_why'] = (x['R6_why'] + '; ' if x['R6_why'] else '') + '%s: same URL after %s at %s (%s)' % (
                    kind, r['wall'], r['utc'][11:19], r['who'])
            for x in other_ua:
                if r['wall'].startswith('wall'):
                    x['R6'] = 'does not comply'
                    x['R6_why'] += '; other User-Agent to the host after a wall'
    # R7 terms (brief section 4: only where a Lighthouse record quotes them)
    for r in rows:
        if r['host'] in ('www.silicondata.com', 'www.dramexchange.com', 'news.metal.com', 'www.metal.com', 'vast.ai', 'learn.microsoft.com'):
            r['R7'] = 'complies' if not r['kept'].startswith('yes') or r['use'] == 'robots' else 'does not comply'
            r['R7_why'] = 'LH045 quotes terms forbidding storage or reproduction; ' + r['kept']
        elif r['host'] == 'epoch.ai':
            r['R7'], r['R7_why'] = 'complies', "Epoch's data are free to use with attribution (LH045 brief); kept with attribution"
        else:
            r['R7'], r['R7_why'] = 'terms not read', ''
    # R5 rate: per who and host, shortest gap and largest count in 60 s; Crawl-delay where set
    by = {}
    for r in rows:
        by.setdefault((r['who'], r['host']), []).append(r)
    for (who, host), rs in by.items():
        ts = sorted(t(x['utc']) for x in rs)
        gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
        mx = 0
        j = 0
        for i2 in range(len(ts)):
            while (ts[i2] - ts[j]).total_seconds() >= 60:
                j += 1
            mx = max(mx, i2 - j + 1)
        cd = next((x['crawl_delay'] for x in rs if x['crawl_delay']), '')
        ts2 = sorted(t(x['utc']) for x in rs if x['use'] != 'robots')
        gaps2 = [(b - a).total_seconds() for a, b in zip(ts2, ts2[1:])]
        verdict = 'complies'
        why = ''
        if cd:
            try:
                need_gap = float(cd.split()[0])
                if gaps and min(gaps) < need_gap:
                    verdict, why = 'does not comply (advisory)', 'Crawl-delay %s; shortest gap %.0f s' % (cd, min(gaps))
            except ValueError:
                pass
        v2 = 'complies'
        if cd:
            try:
                if gaps2 and min(gaps2) < float(cd.split()[0]):
                    v2 = 'does not comply (advisory)'
            except ValueError:
                pass
        for x in rs:
            x['R5_excl_robots'] = v2
            x['R5'] = verdict
            x['R5_why'] = why
            x['host_n'] = len(rs)
            x['host_max60'] = mx
            x['host_min_gap'] = '%.0f' % min(gaps) if gaps else ''
    # overall verdicts
    for r in rows:
        for reading, rk in (('A', 'R1'), ('B', 'R2'), ('B_agent', 'R2_agent')):
            vs = [r[rk], r['R4'], r['R5'], r['R6'], r['R7'], r['R8']]
            if any(v.startswith('does not comply') for v in vs):
                r['overall_' + reading] = 'does not comply'
            elif r[rk] == 'unknown' or r['R8'] == 'unknown':
                r['overall_' + reading] = 'unknown'
            else:
                r['overall_' + reading] = 'complies'
    os.makedirs(OUT, exist_ok=True)
    fields = ['source', 'reached', 'log', 'who', 'method', 'url', 'host', 'utc', 'status', 'ua', 'use', 'kept', 'robots_first', 'robots_prov',
              'robots_file', 'robots_status', 'R1', 'R1_rule', 'R2', 'R2_agent', 'R2_tokens', 'R3', 'R3_tokens', 'near', 'signal', 'R4', 'R4_why',
              'crawl_delay', 'host_n', 'host_max60', 'host_min_gap', 'R5', 'R5_why', 'R5_excl_robots', 'wall', 'R6', 'R6_why', 'R7', 'R7_why', 'R8',
              'overall_A', 'overall_B', 'overall_B_agent']
    with open(os.path.join(OUT, 'requests-judged.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, 'needs-current.txt'), 'w') as f:
        f.write(''.join(a + '/robots.txt\n' for a in sorted(need)))
    print('requests judged:', len(rows), '; authorities still without a copy:', len(need))


if __name__ == '__main__':
    main()
