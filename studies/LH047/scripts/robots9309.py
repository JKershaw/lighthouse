"""LH047: a small robots.txt evaluator following RFC 9309 (September 2022), used both for
LH047's own requests (fetch.py) and for the audit of earlier requests (audit.py).

What it implements, with the RFC section:
- groups: one or more user-agent lines followed by rules; lines other than user-agent,
  allow and disallow (sitemap, crawl-delay, content-signal, ...) do not end a group (2.1, 2.2);
- a crawler obeys the group(s) whose user-agent value matches its product token,
  case-insensitively; several matching groups are combined; with none, the "*" group(s);
  with no such group either, no rule applies (2.2.1);
- the most specific (longest) matching rule wins; on a tie between allow and disallow,
  allow wins; "*" matches any sequence of characters and "$" ends the pattern (2.2.2, 2.2.3);
- /robots.txt itself is always allowed (2.2.2);
- matching is case-sensitive, against the URI's path with its query, after unencoding
  percent-encoded unreserved octets on both sides (2.2.2).
Matching of the user-agent value is exact (case-insensitive); groups whose value is a
prefix or extension of the token are reported separately by near_groups(), not obeyed.
"""
import re


def _clean(line):
    i = line.find('#')
    if i >= 0:
        line = line[:i]
    return line.strip()


def parse(text):
    """Return a list of groups: dict(agents=[...], rules=[(kind, pattern)], extras=[(key, value)])."""
    groups = []
    cur = None
    last_was_agent = False
    for raw in text.splitlines():
        line = _clean(raw)
        if not line or ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip().lower()
        val = val.strip()
        if key == 'user-agent':
            if cur is None or not last_was_agent:
                cur = dict(agents=[], rules=[], extras=[])
                groups.append(cur)
            cur['agents'].append(val)
            last_was_agent = True
        elif key in ('allow', 'disallow'):
            if cur is None:
                last_was_agent = False
                continue  # a rule before any user-agent line belongs to no group
            cur['rules'].append((key, val))
            last_was_agent = False
        else:
            if cur is not None:
                cur['extras'].append((key, val))
            # a non-group line does not end the run of user-agent lines (2.2)
    return groups


def groups_for(groups, token, fallback=True):
    """Groups that apply to `token` (exact, case-insensitive); with fallback, the '*' groups
    when none name the token. Returns (list of groups, 'token'|'star'|'none')."""
    t = token.lower()
    named = [g for g in groups if any(a.lower() == t for a in g['agents'])]
    if named:
        return named, 'token'
    if not fallback:
        return [], 'none'
    star = [g for g in groups if any(a == '*' for a in g['agents'])]
    if star:
        return star, 'star'
    return [], 'none'


def near_groups(groups, token):
    """User-agent values that are not the token but share a prefix with it either way
    (for example 'Lighthouse' against 'Lighthouse-research')."""
    t = token.lower()
    out = []
    for g in groups:
        for a in g['agents']:
            al = a.lower()
            if al != t and al != '*' and al and (t.startswith(al) or al.startswith(t)):
                out.append(a)
    return out


_UNRES = re.compile(r'%([0-9A-Fa-f]{2})')


def _norm(s):
    """RFC 9309 2.2.2: unencode percent-encoded unreserved ASCII octets; upper-case the rest."""
    def f(m):
        c = chr(int(m.group(1), 16))
        if c.isalnum() and c.isascii() or c in '-._~':
            return c
        return '%' + m.group(1).upper()
    return _UNRES.sub(f, s)


def _pattern_re(p):
    p = _norm(p)
    anchored = p.endswith('$')
    if anchored:
        p = p[:-1]
    rx = ''.join('.*' if c == '*' else re.escape(c) for c in p)
    return re.compile(rx + ('$' if anchored else ''), re.S)


def decide(groups_applied, path):
    """Return (allowed: bool, rule or None). path is the URI path with any query."""
    if path.split('?')[0] == '/robots.txt':
        return True, ('implicit', '/robots.txt')
    best = None
    for g in groups_applied:
        for kind, pat in g['rules']:
            if pat == '':
                continue  # an empty pattern matches nothing (2.2.2)
            if _pattern_re(pat).match(_norm(path)):
                key = (len(pat), 1 if kind == 'allow' else 0)
                if best is None or key > best[0]:
                    best = (key, (kind, pat))
    if best is None:
        return True, None
    return best[1][0] == 'allow', best[1]


def extras(groups_applied, key):
    return [v for g in groups_applied for k, v in g['extras'] if k == key]


def evaluate(text, token, path):
    groups = parse(text)
    applied, how = groups_for(groups, token)
    ok, rule = decide(applied, path)
    return dict(allowed=ok, rule=rule, group=how,
                content_signal=extras(applied, 'content-signal'),
                crawl_delay=extras(applied, 'crawl-delay'),
                near=near_groups(groups, token))


if __name__ == '__main__':
    t = """
# test
User-agent: *
Content-Signal: search=yes,ai-train=no
Allow: /

User-agent: *
Disallow: /api/
Allow: /api/public$

User-agent: ClaudeBot
User-agent: GPTBot
Disallow: /
"""
    g = parse(t)
    assert len(g) == 3, g
    a, how = groups_for(g, 'Lighthouse-research')
    assert how == 'star' and len(a) == 2
    assert decide(a, '/x')[0] is True
    assert decide(a, '/api/stats')[0] is False
    assert decide(a, '/api/public')[0] is True
    assert decide(a, '/api/public/x')[0] is False
    assert decide(a, '/robots.txt')[0] is True
    a, how = groups_for(g, 'claudebot')
    assert how == 'token' and decide(a, '/x')[0] is False
    assert groups_for(g, 'Claude-User', fallback=False)[1] == 'none'
    assert decide(*[[dict(agents=['*'], rules=[('disallow', '/a'), ('allow', '/a')], extras=[])], '/a'])[0] is True
    assert decide([dict(agents=['*'], rules=[('disallow', '/pypi/*/json')], extras=[])], '/pypi/x/json')[0] is False
    assert decide([dict(agents=['*'], rules=[('disallow', '')], extras=[])], '/a')[0] is True
    assert decide([dict(agents=['*'], rules=[('disallow', '/foo/baz')], extras=[])], '/foo/%62%61%7A')[0] is False
    print('robots9309 self-test passed')
