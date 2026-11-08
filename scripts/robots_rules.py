#!/usr/bin/env python3
"""Which robots.txt rules Lighthouse obeys, and what they say about one path.

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys a robots.txt group
that names its own token (`Lighthouse-research`) or an agent token of the provider, harness or
model running the session (Claude Code on Anthropic's models: Anthropic's tokens; under OpenAI's
Codex: OpenAI's), else `*`; where several apply, the strictest wins. A collector names the provider
it runs under and obeys every listed provider's tokens when it cannot tell. The tokens, with where
each came from, are in scripts/robots_tokens.json.

This module is dependency-free (standard library only) and makes no network request.

  decide(body, url_or_path, provider=None, truncated=False)
      -> Decision(allowed, decided_by, rule, line, named, per_token, provider)
  provider_from_env()   'anthropic' or 'openai' from LIGHTHOUSE_PROVIDER, else None (= all providers)
  parse(text)           RFC 9309 groups
  token_allowed(groups, token, url_or_path)   one token's view (its group, else '*'), for measures
                        that describe what a file says to a named crawler

Matching follows RFC 9309: user-agent lines are matched case-insensitively on the product token
(the leading run of letters, '_' and '-' in the line's value, so `ClaudeBot/1.0` names ClaudeBot);
groups naming the same token are combined; the longest matching rule wins, Allow winning a tie;
'*' matches any run of characters and a final '$' anchors the end; /robots.txt is always allowed;
an empty Disallow allows everything. The body is read up to READ_LIMIT (512 KiB; RFC 9309 section
2.5 asks for at least 500 KiB) and only complete lines are parsed: a line cut at the limit, or at
a caller's own read cap (`truncated=True`), is never applied.

Strictest of the applicable groups: each applicable token that the file names is evaluated on its
own combined group; the path is disallowed if any of them disallows it. `*` applies only when the
file names none of the applicable tokens.

Usage:
  python3 -I scripts/robots_rules.py                       offline self-tests
  python3 -I scripts/robots_rules.py FILE URL [PROVIDER]   decide one path against a saved file
"""
from pathlib import Path
from urllib.parse import urlsplit, quote, unquote
import json
import os
import re
import sys

READ_LIMIT = 512 * 1024
TOKENS_FILE = Path(__file__).resolve().with_name('robots_tokens.json')
LIGHTHOUSE_TOKEN = 'Lighthouse-research'
_SAFE = "/?=&;:@!$'()*+,~%-._"


# ------------------------------------------------------------------ tokens and provider

def load_tokens(path=TOKENS_FILE):
    """Return {'lighthouse': [...], 'anthropic': [...], 'openai': [...]}: the tokens each key
    applies, as strings. Entries marked "applied": false in the file are recorded, not obeyed."""
    data = json.load(open(path))
    out = {}
    for key in ('lighthouse', 'anthropic', 'openai'):
        toks = []
        for e in data.get(key, []):
            if isinstance(e, str):
                toks.append(e)
            elif e.get('applied', True):
                toks.append(e['token'])
        out[key] = toks
    return out


def providers(tokens=None):
    tokens = tokens or load_tokens()
    return [k for k in tokens if k != 'lighthouse']


def provider_from_env(tokens=None):
    """LIGHTHOUSE_PROVIDER ('anthropic' or 'openai'); anything else, or unset, is None, which
    means a collector cannot tell and obeys every listed provider's tokens."""
    v = os.environ.get('LIGHTHOUSE_PROVIDER', '').strip().lower()
    return v if v in providers(tokens) else None


def applicable_tokens(provider=None, tokens=None):
    """Lighthouse's own token, then the provider's tokens, or every provider's when provider is
    None. Order is kept (it decides which token is reported when several disallow)."""
    tokens = tokens or load_tokens()
    out = list(tokens['lighthouse'])
    for p in ([provider] if provider else providers(tokens)):
        if p not in tokens:
            raise ValueError('unknown provider %r' % p)
        out += tokens[p]
    seen, uniq = set(), []
    for t in out:
        if t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return uniq


# ------------------------------------------------------------------ parsing

def complete_text(body, truncated=False):
    """The part of a robots.txt body Lighthouse parses: at most READ_LIMIT bytes, complete lines
    only. A body longer than the limit, or one the caller says was cut, loses its last partial
    line (all of it, if it has no newline)."""
    if isinstance(body, str):
        body = body.encode('utf-8', 'surrogateescape')
    body = body or b''
    if len(body) > READ_LIMIT:
        body, truncated = body[:READ_LIMIT], True
    if truncated:
        cut = max(body.rfind(b'\n'), body.rfind(b'\r'))
        body = body[:cut + 1] if cut >= 0 else b''
    text = body.decode('utf-8', 'replace')
    return text[1:] if text.startswith('﻿') else text


def _token_of(value):
    v = value.strip()
    if v.startswith('*'):
        return '*'
    m = re.match(r'[A-Za-z_-]+', v)
    return m.group(0).lower() if m else ''


class Group:
    __slots__ = ('agents', 'rules', 'line')

    def __init__(self, line):
        self.agents, self.rules, self.line = [], [], line   # rules: (allow, pattern, line, raw)

    def __repr__(self):
        return 'Group(line %d, %s, %d rules)' % (self.line, self.agents, len(self.rules))


def parse(text):
    """RFC 9309 groups, in file order. A run of user-agent lines starts a group; allow and
    disallow lines belong to the group above; other records (sitemap, crawl-delay) neither end a
    group nor start one; rules before any user-agent line are ignored."""
    groups, cur, in_agents = [], None, False
    for i, raw in enumerate(re.split(r'\r\n|\r|\n', text), 1):
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key, val = key.strip().lower(), val.strip()
        if key == 'user-agent':
            if not in_agents:
                cur = Group(i)
                groups.append(cur)
            tok = _token_of(val)
            if tok:
                cur.agents.append(tok)
            in_agents = True
        elif key in ('allow', 'disallow'):
            in_agents = False
            if cur is not None:
                cur.rules.append((key == 'allow', val, i, line))
    return groups


# ------------------------------------------------------------------ matching

def _path(url_or_path):
    s = urlsplit(url_or_path)
    p = s.path or '/'
    if s.query:
        p += '?' + s.query
    return quote(unquote(p), safe=_SAFE)


def _matches(pattern, path):
    pat = quote(unquote(pattern), safe=_SAFE)
    anchored = pat.endswith('$')
    if anchored:
        pat = pat[:-1]
    rx = '^' + '.*'.join(re.escape(part) for part in pat.split('*')) + ('$' if anchored else '')
    return re.match(rx, path) is not None


def _best(rules, path):
    """The deciding rule among rules for path: longest pattern, Allow on a tie; None if none."""
    best = None
    for allow, pat, line, raw in rules:
        if pat == '':
            continue
        if _matches(pat, path):
            n = len(quote(unquote(pat), safe=_SAFE).encode())
            if best is None or n > best[0] or (n == best[0] and allow and not best[1]):
                best = (n, allow, line, raw)
    return best


def _rules_naming(groups, token):
    tok = token.lower()
    named = [g for g in groups if tok in g.agents]
    return named, [r for g in named for r in g.rules]


def token_allowed(groups, token, url_or_path):
    """One token's view, as RFC 9309 defines it for a single crawler: its own (combined) group,
    else '*', else no rules."""
    if urlsplit(url_or_path).path == '/robots.txt':
        return True
    named, rules = _rules_naming(groups, token)
    if not named:
        named, rules = _rules_naming(groups, '*')
    b = _best(rules, _path(url_or_path))
    return True if b is None else b[1]


class Decision(dict):
    """allowed (bool); decided_by (a token, '*', or None when no group applied); rule (the
    deciding line, or None); line (its line number); named (applicable tokens the file names);
    per_token ({token: allowed} for each named one, or {'*': allowed}); provider (or 'all')."""
    __getattr__ = dict.__getitem__


def decide_groups(groups, url_or_path, provider=None, tokens=None):
    apply = applicable_tokens(provider, tokens)
    named = [t for t in apply if _rules_naming(groups, t)[0]]
    prov = provider or 'all'
    if urlsplit(url_or_path).path == '/robots.txt':
        return Decision(allowed=True, decided_by=None, rule='/robots.txt is always allowed', line=None,
                        named=named, per_token={}, provider=prov)
    path = _path(url_or_path)
    if not named:
        star, rules = _rules_naming(groups, '*')
        if not star:
            return Decision(allowed=True, decided_by=None, rule=None, line=None, named=[], per_token={},
                            provider=prov)
        b = _best(rules, path)
        ok = True if b is None else b[1]
        return Decision(allowed=ok, decided_by='*', rule=b[3] if b else None, line=b[2] if b else star[0].line,
                        named=[], per_token={'*': ok}, provider=prov)
    per, first_no, first_yes = {}, None, None
    for t in named:
        g, rules = _rules_naming(groups, t)
        b = _best(rules, path)
        ok = True if b is None else b[1]
        per[t] = ok
        hit = (t, b[3] if b else None, b[2] if b else g[0].line)
        if not ok and first_no is None:
            first_no = hit
        if ok and first_yes is None:
            first_yes = hit
    t, rule, line = first_no or first_yes
    return Decision(allowed=first_no is None, decided_by=t, rule=rule, line=line, named=named, per_token=per,
                    provider=prov)


def decide(body, url_or_path, provider=None, truncated=False, tokens=None):
    """Whether Lighthouse may request url_or_path under this robots.txt body (bytes or str), and
    which group decided. provider: 'anthropic', 'openai' or None (all listed providers)."""
    return decide_groups(parse(complete_text(body, truncated)), url_or_path, provider, tokens)


# ------------------------------------------------------------------ offline self-tests

LH044_BASE = Path(__file__).resolve().parents[1] / 'studies' / 'LH044' / 'data' / 'read-2026-11-08T1920Z'
# The eight probes the LH044 evidence review (notes/R-0059, review/ai_tokens_check-output.txt)
# found sent at the baseline to hosts whose robots.txt disallows an Anthropic token at the path.
EIGHT = ['D15', 'Q07', 'F06', 'F07', 'R06', 'R07', 'D11', 'P18']


def _selftest():
    import csv
    fails = []

    def check(name, cond):
        print(('ok   ' if cond else 'FAIL ') + name)
        if not cond:
            fails.append(name)

    T = {'lighthouse': ['Lighthouse-research'], 'anthropic': ['ClaudeBot', 'Claude-User', 'Claude-Code'],
         'openai': ['GPTBot', 'ChatGPT-User']}
    # synthetic cases
    f = 'User-agent: *\nDisallow: /a\n\nUser-agent: ClaudeBot\nDisallow: /b\n\nUser-agent: GPTBot\nDisallow: /c\n'
    check('* does not apply once a provider token is named',
          decide(f, '/a', 'anthropic', tokens=T).allowed and not decide(f, '/b', 'anthropic', tokens=T).allowed)
    check('provider openai obeys GPTBot, not ClaudeBot',
          decide(f, '/b', 'openai', tokens=T).allowed and not decide(f, '/c', 'openai', tokens=T).allowed)
    d = decide(f, '/c', None, tokens=T)
    check('provider None obeys every provider\'s tokens', not d.allowed and d.decided_by == 'GPTBot'
          and not decide(f, '/b', None, tokens=T).allowed)
    check('the Lighthouse-only view (lighthouse tokens alone) falls back to *',
          not decide(f, '/a', None, tokens={'lighthouse': ['Lighthouse-research']}).allowed)
    f2 = ('User-agent: Lighthouse-research\nAllow: /\n\nUser-agent: Claude-User\nDisallow: /x\n\n'
          'User-agent: *\nDisallow: /\n')
    d = decide(f2, '/x/1', 'anthropic', tokens=T)
    check('strictest of Lighthouse\'s and the provider\'s groups wins',
          not d.allowed and d.decided_by == 'Claude-User' and d.rule == 'Disallow: /x' and d.line == 5)
    check('allowed where every applicable group allows, * ignored', decide(f2, '/y', 'anthropic', tokens=T).allowed)
    check('no group at all allows everything', decide('Sitemap: /s.xml\n', '/z', None, tokens=T).allowed)
    # The rule as the keeper wrote it: '*' applies only when no applicable token is named, so a file
    # that shuts '*' out but lets a named provider token in lets Lighthouse in too. Recorded here so
    # that a change of reading is a visible change to this test.
    f6 = 'User-agent: *\nDisallow: /\n\nUser-agent: ClaudeBot\nAllow: /\n'
    check('as written: * set aside when a provider token is named, even when * is stricter',
          decide(f6, '/x', 'anthropic', tokens=T).allowed and not decide(f6, '/x', 'openai', tokens=T).allowed)
    f3 = 'User-agent: claudebot/1.0\nUser-agent: Other\nDisallow: /p\nCrawl-delay: 5\nAllow: /p/ok$\n'
    check('product token matched case-insensitively, version suffix ignored',
          not decide(f3, '/p/x', 'anthropic', tokens=T).allowed)
    check('longest match wins and $ anchors', decide(f3, '/p/ok', 'anthropic', tokens=T).allowed
          and not decide(f3, '/p/ok2', 'anthropic', tokens=T).allowed)
    f4 = 'User-agent: ClaudeBot\nDisallow: /q\n\nUser-agent: ClaudeBot\nDisallow: /r\n'
    check('groups naming the same token are combined', not decide(f4, '/r', 'anthropic', tokens=T).allowed)
    f5 = 'User-agent: *\nDisallow: /*.php$\nAllow: /a\nDisallow: /a\n'
    check('* wildcard', not decide(f5, '/x/y.php', None, tokens=T).allowed
          and decide(f5, '/x/y.php?q', None, tokens=T).allowed)
    check('Allow wins a tie', decide(f5, '/a/1', None, tokens=T).allowed)
    check('/robots.txt always allowed', decide('User-agent: *\nDisallow: /\n', '/robots.txt', tokens=T).allowed)
    check('empty Disallow allows', decide('User-agent: ClaudeBot\nDisallow:\n', '/', 'anthropic', tokens=T).allowed)
    check('percent-encoding normalised', not decide('User-agent: *\nDisallow: /%7Ea\n', '/~a/b', tokens=T).allowed)
    big = ('User-agent: *\n' + '# pad\n' * (READ_LIMIT // 6) + 'Disallow: /late\n').encode()
    check('rules past 512 KiB are not read', len(big) > READ_LIMIT and decide(big, '/late', tokens=T).allowed)
    cut = b'User-agent: *\nDisallow: /web/package\nDisallow: /web/pac'
    check('a cut-off last line is never applied',
          decide(cut, '/web/pac/1', truncated=True, tokens=T).allowed
          and not decide(cut, '/web/package', truncated=True, tokens=T).allowed)
    check('CRLF line endings', not decide('User-agent: *\r\nDisallow: /w\r\n', '/w', tokens=T).allowed)
    os.environ['LIGHTHOUSE_PROVIDER'] = 'OpenAI'
    p1 = provider_from_env(T)
    os.environ['LIGHTHOUSE_PROVIDER'] = 'codex'
    p2 = provider_from_env(T)
    del os.environ['LIGHTHOUSE_PROVIDER']
    check('provider from LIGHTHOUSE_PROVIDER; unknown or unset is None',
          p1 == 'openai' and p2 is None and provider_from_env(T) is None)
    check('scripts/robots_tokens.json loads, Lighthouse-research first',
          load_tokens()['lighthouse'] == ['Lighthouse-research'] and load_tokens()['anthropic']
          and load_tokens()['openai'])

    # the eight LH044 baseline probes, on their retained robots.txt files
    if not LH044_BASE.exists():
        print('skip LH044 retained files (not found)')
    else:
        svc = {s['id']: s for s in json.load(open(LH044_BASE / 'services.json'))['services']}
        log = {r['n']: r for r in csv.DictReader(open(LH044_BASE / 'readlog.csv'))}
        own = {'lighthouse': ['Lighthouse-research']}
        sent_allowed = 0
        for sid in EIGHT:
            s = svc[sid]
            body = (LH044_BASE / ('%04d.b' % int(s['robots_n']))).read_bytes()
            tr = log[str(s['robots_n'])]['truncated'] == 'True'
            old = decide(body, s['url'], None, tr, tokens=own)
            a = decide(body, s['url'], 'anthropic', tr)
            n = decide(body, s['url'], None, tr)
            o = decide(body, s['url'], 'openai', tr)
            sent_allowed += bool(s['probe_n']) and old.allowed
            check('%s %s: allowed under Lighthouse-only rules; disallowed as anthropic (by %s: %s, line %s) '
                  'and with provider unknown; as openai %s' % (
                      sid, s['host'], a.decided_by, a.rule, a.line,
                      'allowed' if o.allowed else 'disallowed (by %s)' % o.decided_by),
                  old.allowed and not a.allowed and not n.allowed)
        check('all eight probes were sent at the baseline, as the Lighthouse-only rule allowed', sent_allowed == 8)
    print('\n%d failed' % len(fails))
    return 1 if fails else 0


def _cli(argv):
    body = Path(argv[0]).read_bytes()
    d = decide(body, argv[1], argv[2] if len(argv) > 2 else provider_from_env())
    print(json.dumps(d, indent=1))
    return 0 if d.allowed else 2


if __name__ == '__main__':
    sys.exit(_cli(sys.argv[1:]) if len(sys.argv) > 1 else _selftest())
