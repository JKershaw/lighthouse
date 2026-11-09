#!/usr/bin/env python3
"""Content-Signal: whether a response may be kept whole in the public repository.

Cloudflare's Content Signals (studies/LH047/catalogue.md, A6) put a `Content-Signal:` line in a
robots.txt group, saying yes or no to `search`, `ai-input` and `ai-train`, and, experimentally, a
`use=` field: `immediate`, `reference` ("index, excerpt, and link back") or `full` ("summarize and
reproduce"). LH047's brief (R4) reads `use=reference` or `use=immediate` as not met when the full
body is kept in the public repository, and `use=full` as met. From 9 November 2026 (schedule row
use-reference-1, amendments of the same date to LH042's and LH044's briefs) Lighthouse's
collectors honour that reading: where the applicable signal asks for `use=reference` or
`use=immediate`, a response's body is not kept in the repository. What is kept is the SHA-256 of
the bytes received, the headers, and a bounded extract that the study's brief needs; the whole
body may be held beside it for the run only, in a file git ignores (`*.withheld-local`), so the
run can classify or quote it, and is never committed.

Which groups apply: those of the keeper's rule (scripts/robots_rules.py: groups naming
Lighthouse-research or one of the running provider's tokens, else `*`) and the group LH047's R4
read (Lighthouse-research, else `*`); a signal in any of them counts (the strictest wins). Without
the second, a file that disallows ClaudeBot by name would hide its `*` signal from Lighthouse. A `Content-Signal` response header with the same syntax is also
honoured; Cloudflare defines the line for robots.txt only, so honouring a header is a cautious
reading, not a specified one. Not handled here (left for a brief or the keeper): `ai-input=no`,
which bears on whether a model may read a body at all rather than on keeping it; `ai-train=no`,
which Lighthouse meets by training no model; and the IETF AI Preferences `Content-Usage` header and
robots.txt rule, whose vocabulary has no term for keeping or excerpting.

Standard library only; makes no network request.

  signal_lines(robots_text, provider=None)  the Content-Signal values of the applicable groups
  decide(robots_text, headers, provider=None)
      -> {'withhold': bool, 'signal': the line(s) as read, 'where': 'robots.txt' | 'header' | ''}
  title_of(body)                            a page's <title>, at most 200 characters
  excerpt(text, needle, width=120)          needle with up to width characters either side
  write_withheld(body_path, body, record)   placeholder at body_path, record beside it, the whole
                                            body in body_path + '.withheld-local' (git-ignored)

Usage: python3 -I scripts/content_signal.py     offline self-tests
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import html
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import robots_rules  # noqa: E402

WITHHOLD_USES = ('reference', 'immediate')
LOCAL_SUFFIX = '.withheld-local'
EXTRACT_MAX = 2000      # characters of extract kept per body, all fields together


def parse_signal(value):
    """'search=yes, ai-train=no, use=reference' -> {'search': 'yes', 'ai-train': 'no', 'use': 'reference'}"""
    out = {}
    for part in value.split(','):
        if '=' in part:
            k, v = part.split('=', 1)
            out[k.strip().lower()] = v.strip().lower()
    return out


def _groups(text):
    """[(agents, [signal values])] in file order, grouped as RFC 9309 groups user-agent lines; a
    Content-Signal line belongs to the group above it. A line before any user-agent line applies
    to every reader and is returned under the agent '*all*'."""
    groups, cur, in_agents, before = [], None, False, []
    for raw in re.split(r'\r\n|\r|\n', text):
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key, val = key.strip().lower(), val.strip()
        if key == 'user-agent':
            if not in_agents:
                cur = ([], [])
                groups.append(cur)
            tok = robots_rules._token_of(val)
            if tok:
                cur[0].append(tok)
            in_agents = True
        elif key in ('allow', 'disallow'):
            in_agents = False
        elif key == 'content-signal':
            (cur[1] if cur is not None else before).append(val)
    if before:
        groups.insert(0, (['*all*'], before))
    return groups


def _pick(gs, toks):
    named = [g for g in gs if any(t in g[0] for t in toks)]
    return named or [g for g in gs if '*' in g[0]]


def signal_lines(robots_text, provider=None):
    """The Content-Signal values that apply to Lighthouse: those of the groups the keeper's rule
    selects (Lighthouse-research or the provider's tokens, else '*') together with those of the
    group LH047's reading A selects (Lighthouse-research, else '*'). A file that names only
    training crawlers, as Cloudflare's managed file does, so still has its '*' signal read."""
    if isinstance(robots_text, bytes):
        robots_text = robots_rules.complete_text(robots_text)
    gs = _groups(robots_text or '')
    toks = [t.lower() for t in robots_rules.applicable_tokens(provider)]
    chosen = _pick(gs, toks)
    chosen += [g for g in _pick(gs, [robots_rules.LIGHTHOUSE_TOKEN.lower()]) if g not in chosen]
    chosen += [g for g in gs if '*all*' in g[0]]
    return [v for _, vals in chosen for v in vals]


def _asks_reference(values):
    return [v for v in values if parse_signal(v).get('use') in WITHHOLD_USES]


def decide(robots_text, headers, provider=None):
    """Whether to withhold a response's body. robots_text: the robots.txt that governed the
    request (str or bytes, or None if none was read); headers: list of (name, value) pairs."""
    hits = _asks_reference(signal_lines(robots_text, provider)) if robots_text else []
    if hits:
        return {'withhold': True, 'signal': ' | '.join(hits), 'where': 'robots.txt'}
    hv = [v for k, v in (headers or []) if k.strip().lower() == 'content-signal']
    hits = _asks_reference(hv)
    if hits:
        return {'withhold': True, 'signal': ' | '.join(hits), 'where': 'header'}
    return {'withhold': False, 'signal': '', 'where': ''}


def title_of(body):
    text = body.decode('utf-8', 'replace') if isinstance(body, bytes) else (body or '')
    m = re.search(r'(?is)<title[^>]*>(.*?)</title>', text[:200000])
    return re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()[:200] if m else ''


def excerpt(text, needle, width=120):
    i = text.find(needle)
    if i < 0:
        return ''
    return text[max(0, i - width):i + len(needle) + width]


def placeholder(record_name):
    return ('[body withheld by Lighthouse: the site\'s Content-Signal asks for use=reference; '
            'hash, headers and extract in %s]\n' % record_name).encode()


def write_withheld(body_path, body, record):
    """Write the placeholder at body_path, the record as <stem>.withheld.json beside it, and the
    whole body to body_path + LOCAL_SUFFIX for this run only (git ignores it). Returns the record."""
    body_path = Path(body_path)
    rec_path = body_path.with_name(body_path.stem + '.withheld.json')
    rec = {'withheld': 'body', 'why': 'Content-Signal use=reference (or use=immediate): '
           '"index, excerpt, and link back"; a whole copy in a public repository goes beyond it',
           'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
           'sha256_received': sha256(body).hexdigest(), 'bytes_received': len(body)}
    rec.update(record)
    ex = rec.get('extract') or {}
    if sum(len(str(v)) for v in ex.values()) > EXTRACT_MAX:
        raise ValueError('extract longer than %d characters' % EXTRACT_MAX)
    body_path.write_bytes(placeholder(rec_path.name))
    Path(str(body_path) + LOCAL_SUFFIX).write_bytes(body)
    rec_path.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    return rec


def record_path(body_path):
    body_path = Path(body_path)
    return body_path.with_name(body_path.stem + '.withheld.json')


def load_record(body_path):
    p = record_path(body_path)
    return json.loads(p.read_text()) if p.exists() else None


def _selftest():
    fails = []

    def check(name, cond):
        print(('ok   ' if cond else 'FAIL ') + name)
        if not cond:
            fails.append(name)

    cf = ('# As a condition of accessing this website ... Content-Signal = yes\n'
          'User-agent: *\nContent-Signal: search=yes,ai-train=no,use=reference\nAllow: /\n\n'
          'User-agent: Amazonbot\nDisallow: /\n')
    check('Cloudflare managed file: * group asks for use=reference', decide(cf, [])['withhold'])
    check('comment lines mentioning Content-Signal are not read', len(signal_lines(cf)) == 1)
    doaj = ('User-Agent: *\nContent-signal: search=yes, ai-train=yes, ai-input=yes, use=reference\n'
            'Disallow: /search\n')
    check('case and spaces in the line are tolerated', decide(doaj, [])['withhold'])
    own = 'User-agent: *\nContent-Signal: use=reference\nAllow: /\n\nUser-agent: Lighthouse-research\nAllow: /\n'
    check('a group naming Lighthouse-research replaces * (no signal there)', not decide(own, [])['withhold'])
    prov = 'User-agent: *\nAllow: /\n\nUser-agent: ClaudeBot\nContent-Signal: use=immediate\nAllow: /\n'
    check('a provider token group applies under provider anthropic', decide(prov, [], 'anthropic')['withhold'])
    check('...and not under provider openai', not decide(prov, [], 'openai')['withhold'])
    named = ('User-agent: *\nContent-Signal: search=yes,ai-train=no,use=reference\nAllow: /\n\n'
             'User-agent: ClaudeBot\nDisallow: /\n')
    check('a * signal still counts where the file names only a training crawler',
          decide(named, [], 'anthropic')['withhold'])
    check('use=full keeps', not decide('User-agent: *\nContent-Signal: use=full\n', [])['withhold'])
    check('ai-train=no alone keeps', not decide('User-agent: *\nContent-Signal: ai-train=no\n', [])['withhold'])
    check('no robots.txt, header asks for reference',
          decide(None, [('Content-Signal', 'search=yes, use=reference')])['where'] == 'header')
    check('title extracted', title_of(b'<html><title> A &amp; B </title>') == 'A & B')
    print('\n%d failed' % len(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(_selftest())
