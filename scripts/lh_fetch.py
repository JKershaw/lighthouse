#!/usr/bin/env python3
"""How every Lighthouse collector fetches and saves: a robots.txt-gated urlopen, and the one place
the rule on keeping a body is applied.

The keeper, 8 November 2026 (AGENTS.md, Rules that matter): Lighthouse obeys robots.txt as its own agent
and as whatever runs it. Collectors written before that rule call urllib's urlopen directly; they now
import `urlopen` from here instead, which asks scripts/robots_gate.py first. A URL that robots.txt
disallows, or whose robots.txt cannot be read, is not requested: `NotFetched` is raised, and the
collector's own error handling logs it as a missing reading ("NotFetched: ..."), never a negative.

  from lh_fetch import urlopen, redacted, UA      (redacted(body) -> bytes; redact_bytes -> (bytes, count))
  urlopen(req, access='oneoff')                    a one-off, targeted read (the keeper, 21 November 2026)
  save_body(path, body, url, headers, gate=, robots_body=) -> (kept, reason)
                                                  writes a body only where it may be kept
  keep_decision(url, body, headers, ...)          the keep rule itself: robots.txt and the page's reservation
  write_derived(path, url, reason, extracted, **meta)   the record that stands in for a body not kept
  python3 -I scripts/lh_fetch.py --selftest       offline tests of the gate and the keep path (robots.txt stubbed)

The keeper, 21 November 2026 (notes/keeper/2026-11-21-robots-intent.md): no body is kept where
robots.txt refuses *, an AI-training or archiving crawler, or the page reserves itself from AI use.
Every collector saves bodies only through save_body (notes/keeper/robots-intent-2026-11-21/
collectors_wired.md); where it says no, the collector logs body_kept = "no: <reason>" and, where its
measures need facts from the page, writes them with write_derived.

UA is Lighthouse's User-Agent with its robots token. redact_bytes withholds email addresses from a body
before it is saved (the keeper, 8 November 2026); a fetch log keeps the hash of the bytes received.
The provider is read from LIGHTHOUSE_PROVIDER; unset, every listed provider's tokens are obeyed.
"""
import os
import sys
import urllib.request
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from robots_gate import RobotsGate  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402,F401

UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
_GATE = RobotsGate(UA)


def redacted(body):
    """The body with email addresses withheld, as bytes (redact_bytes also returns the count)."""
    return redact_bytes(body)[0]


class NotFetched(Exception):
    """robots.txt disallows the URL, or could not be read: not requested in this run."""


def check(url, access=None):
    return _GATE.check(url, access)


def _require_allowed(url, access=None):
    ok, info = _GATE.check(url, access)
    if not ok:
        raise NotFetched("not fetched: %s (robots %s, status %s, group %s, rule %s, sha256 %s)" % (
            info.get("reason"), info.get("robots_url"), info.get("robots_status"),
            info.get("decided_by", ""), info.get("rule", ""), info.get("robots_sha256", "")[:16]))


class _RobotsCheckedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, access=None):
        super().__init__()
        self.access = access

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            parts = urlsplit(newurl)
            if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
                raise NotFetched("not fetched: invalid HTTP(S) redirect destination")
            _require_allowed(newurl, self.access)
        except (NotFetched, ValueError):
            fp.close()
            raise
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def urlopen(request, *args, check_redirects=False, access=None, **kwargs):
    """Check robots.txt before fetching, and before each redirect when requested. access='oneoff' for a
    one-off, targeted read; the default is the recurring-collection rule."""
    url = request.full_url if isinstance(request, urllib.request.Request) else request
    _require_allowed(url, access)
    if check_redirects:
        opener = urllib.request.build_opener(_RobotsCheckedRedirect(access))
        return opener.open(request, *args, **kwargs)
    return urllib.request.urlopen(request, *args, **kwargs)



NOT_KEPT_NOTE = ("Body not kept under the keeper's decision of 21 November 2026 (notes/keeper/2026-11-21-robots-intent.md): "
                 "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, or the page reserves itself "
                 "from AI use, so Lighthouse keeps the URL, read time, status, SHA-256 of the bytes received and the facts "
                 "its records use, not the page.")


_UNSET = object()


def keep_decision(url, body=None, headers=None, access=None, gate=None, robots_body=_UNSET):
    """(keep, reason) for a body fetched from url (the final URL after any redirect): robots.txt
    (robots_rules.may_keep, through the gate's cached file) and, when body or headers are given, the
    page's own noai / TDM reservation (robots_rules.page_reservation). gate: a collector's own
    RobotsGate, so robots.txt is read once per run; defaults to this module's gate. robots_body: the
    site's robots.txt already read by the caller (bytes), or None where it answered 4xx (no rules);
    then no gate is consulted. The one place the keep rule is applied; save_body and collectors
    that store bodies in their own form use it."""
    from robots_rules import page_reservation, may_keep as _may_keep_rules
    if robots_body is _UNSET:
        keep, why = (gate or _GATE).may_keep(url, access)
    elif robots_body is None:
        keep, why = True, 'robots.txt gave no rules'
    else:
        keep, why = _may_keep_rules(robots_body, url)
    if not keep:
        return False, why
    reserved = page_reservation(body, headers) if (body is not None or headers is not None) else None
    return (False, reserved) if reserved else (True, why)


def save_body(path, body, url, headers=None, access=None, gzip_body=None, gate=None, robots_body=_UNSET):
    """Save a fetched body only if it may be kept (keep_decision). Returns (kept, reason). Where it
    may not be kept, nothing is written: the caller logs body_kept = "no: <reason>" with URL, read
    time, status, size and the SHA-256 of the bytes received, and writes a derived file
    (write_derived) where its measures need facts from the page; a later script that finds no body
    treats the reading as unavailable, never as zero. Email addresses are withheld from a kept body.
    gzip_body defaults to whether path ends in .gz."""
    import gzip as _gzip
    keep, why = keep_decision(url, body, headers, access, gate, robots_body)
    if not keep:
        return False, why
    data = redacted(body)
    if gzip_body is None:
        gzip_body = str(path).endswith('.gz')
    if gzip_body:
        data = _gzip.compress(data, mtime=0)
    with open(path, 'wb') as f:
        f.write(data)
    return True, why


def write_derived(path, url, reason, extracted, **meta):
    """Write the derived file that stands in for a body not kept: URL, the reason, the facts a study
    uses (extracted), and any metadata given (read_utc, finish_utc, http_status, content_type, bytes,
    sha256, used_for ...), with the standard note. JSON, UTF-8, one indent. Email addresses are withheld
    from everything it writes (the serialised JSON goes through redacted(), as a kept body does; from
    21 November 2026)."""
    import json as _json
    rec = {'url': url, **meta, 'body_kept': 'no: ' + str(reason), 'body_removed': NOT_KEPT_NOTE,
           'extracted': extracted}
    text = redacted((_json.dumps(rec, indent=1, ensure_ascii=False) + '\n').encode('utf-8')).decode('utf-8')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path


# ------------------------------------------------------------------ offline self-tests
# python3 -I scripts/lh_fetch.py --selftest: the gate (scripts/robots_gate.py) and this module's keep
# path, with every robots.txt fetch stubbed, so nothing goes over the network. Added 21 November 2026;
# it tests the modules as they stand and changes none of their behaviour.

def _selftest():
    import io
    import json as _json
    import tempfile
    from urllib.error import HTTPError, URLError
    import robots_gate

    fails = []

    def check(name, cond):
        print(('ok   ' if cond else 'FAIL ') + name)
        if not cond:
            fails.append(name)

    # Stubbed robots.txt server: host -> (status, body) or an exception to raise.
    SITES = {
        'train.test': (200, b'User-agent: ClaudeBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n'),
        'user.test': (200, b'User-agent: Claude-User\nDisallow: /\n\nUser-agent: *\nAllow: /\n'),
        'star.test': (200, b'User-agent: *\nDisallow: /private/\n'),
        'arch.test': (200, b'User-agent: ia_archiver\nDisallow: /\n'),
        'open.test': (200, b'User-agent: *\nAllow: /\n'),
        'gone.test': (404, b'not found'),
        'forbid.test': (403, b'forbidden'),
        'broken.test': (503, b'unavailable'),
        'down.test': URLError('stubbed: no route'),
    }
    requested = []

    class _Resp(io.BytesIO):
        def __init__(self, status, body):
            super().__init__(body)
            self.status = status

    def fake_urlopen(req, timeout=None):
        url = req.full_url if hasattr(req, 'full_url') else req
        requested.append(url)
        host = urlsplit(url).hostname
        site = SITES.get(host, URLError('stubbed: unknown host'))
        if isinstance(site, Exception):
            raise site
        status, body = site
        if status >= 400:
            raise HTTPError(url, status, 'stub', {}, io.BytesIO(body))
        return _Resp(status, body)

    real_urlopen = robots_gate.urlopen
    real_gate = globals()['_GATE']
    robots_gate.urlopen = fake_urlopen
    try:
        g = RobotsGate(UA, provider='anthropic')

        # RobotsGate.check in both access modes
        ok_r, info_r = g.check('https://train.test/a')
        ok_o, info_o = g.check('https://train.test/a', access='oneoff')
        check('check: a file refusing only ClaudeBot refuses a recurring read', not ok_r and info_r['access'] == 'recurring')
        check('check: the same file admits a one-off read', ok_o and info_o['access'] == 'oneoff')
        check('check: an allowed read still carries keep_body False when ClaudeBot is refused',
              ok_o and info_o['keep_body'] is False and 'ClaudeBot' in info_o['keep_reason'])
        check('check: a refused read is never marked keepable', info_r['keep_body'] is False)
        ok_u, _ = g.check('https://user.test/a', access='oneoff')
        check('check: a named Claude-User refusal is obeyed one-off', not ok_u)
        g_once = RobotsGate(UA, provider='anthropic', access='oneoff')
        check('check: a gate built with access="oneoff" uses it by default',
              g_once.check('https://train.test/a')[0] and g_once.check('https://train.test/a')[1]['access'] == 'oneoff')
        try:
            RobotsGate(UA, access='sometimes')
            check('check: an unknown access mode is refused', False)
        except ValueError:
            check('check: an unknown access mode is refused', True)
        n0 = len(requested)
        g.check('https://train.test/b')
        g.may_keep('https://train.test/c')
        check('check and may_keep read each host\'s robots.txt once per gate', len(requested) == n0)

        # robots.txt answering 4xx: no rules, allowed and keepable
        for host, code in (('gone.test', 404), ('forbid.test', 403)):
            ok4, i4 = g.check('https://%s/page' % host)
            check('check: robots.txt %d means allowed, keep_body True' % code,
                  ok4 and i4['keep_body'] is True and i4['robots_status'] == code)
            check('may_keep: robots.txt %d means keep' % code, g.may_keep('https://%s/page' % host)[0])

        # robots.txt answering 5xx or unreachable: not fetched, not kept
        for host, label in (('broken.test', '503'), ('down.test', 'unreachable')):
            for acc in (None, 'oneoff'):
                ok5, i5 = g.check('https://%s/page' % host, access=acc)
                check('check (%s): robots.txt %s means not fetched and not kept' % (acc or 'recurring', label),
                      not ok5 and i5['keep_body'] is False and 'unreachable' in i5['reason'])
            check('may_keep: robots.txt %s means not kept' % label, not g.may_keep('https://%s/page' % host)[0])

        # RobotsGate.may_keep independent of access
        for host in ('train.test', 'user.test', 'star.test', 'arch.test', 'open.test'):
            u = 'https://%s/private/x' % host
            check('may_keep: same answer in both access modes for %s' % host,
                  g.may_keep(u) == g.may_keep(u, 'oneoff') == g.may_keep(u, 'recurring'))
        check('may_keep: user.test (only Claude-User refused) may be kept', g.may_keep('https://user.test/a')[0])
        check('may_keep: * refusal at the path means not kept, elsewhere kept',
              not g.may_keep('https://star.test/private/x')[0] and g.may_keep('https://star.test/public')[0])
        check('may_keep: an archiving crawler refused means not kept', not g.may_keep('https://arch.test/a')[0])

        # keep_decision, with this module's gate swapped for the stubbed one
        globals()['_GATE'] = g
        check('keep_decision: via the gate, refused for ClaudeBot', not keep_decision('https://train.test/a')[0])
        check('keep_decision: via the gate, open site kept', keep_decision('https://open.test/a')[0])
        check('keep_decision: a gate passed in is used',
              not keep_decision('https://open.test/a', gate=_FixedGate(False))[0])
        n0 = len(requested)
        kb = keep_decision('https://open.test/a', robots_body=b'User-agent: GPTBot\nDisallow: /\n')
        check('keep_decision: robots_body as bytes is read, no gate consulted', kb[0] is False and 'GPTBot' in kb[1])
        check('keep_decision: robots_body bytes allowing all keeps',
              keep_decision('https://train.test/a', robots_body=b'User-agent: *\nAllow: /\n')[0])
        kn = keep_decision('https://train.test/a', robots_body=None)
        check('keep_decision: robots_body None (4xx) means no rules, keep', kn[0] and 'no rules' in kn[1])
        check('keep_decision: with robots_body no robots.txt is requested', len(requested) == n0)
        page = b'<html><head><meta name="robots" content="noai"></head></html>'
        kr = keep_decision('https://open.test/a', page, None)
        check('keep_decision: a page reservation (meta noai) means not kept', not kr[0] and 'noai' in kr[1])
        check('keep_decision: a TDM header means not kept, also with robots_body None',
              not keep_decision('https://open.test/a', b'x', {'TDM-Reservation': '1'}, robots_body=None)[0])
        check('keep_decision: robots refusal wins before the page is read',
              'ClaudeBot' in keep_decision('https://train.test/a', page)[1])
        check('keep_decision: an ordinary page on an open site is kept',
              keep_decision('https://open.test/a', b'<p>hello</p>', {'Content-Type': 'text/html'})[0])

        # save_body writing or not writing
        with tempfile.TemporaryDirectory() as td:
            p1 = os.path.join(td, 'kept.html')
            k1 = save_body(p1, b'<p>write to someone@example.org</p>', 'https://open.test/a')
            data1 = open(p1, 'rb').read() if os.path.exists(p1) else b''
            check('save_body: kept on an open site, file written', k1[0] and os.path.exists(p1))
            check('save_body: email addresses withheld from the kept body', b'someone@example.org' not in data1
                  and data1.startswith(b'<p>write to '))
            p2 = os.path.join(td, 'refused.html')
            k2 = save_body(p2, b'<p>x</p>', 'https://train.test/a')
            check('save_body: refused (ClaudeBot), nothing written, reason returned',
                  not k2[0] and not os.path.exists(p2) and 'ClaudeBot' in k2[1])
            p3 = os.path.join(td, 'reserved.html')
            k3 = save_body(p3, page, 'https://open.test/a', robots_body=None)
            check('save_body: page reservation, nothing written', not k3[0] and not os.path.exists(p3))
            p4 = os.path.join(td, 'kept.raw.gz')
            save_body(p4, b'abc', 'https://open.test/a')
            import gzip as _gz
            raw4 = open(p4, 'rb').read()
            check('save_body: a .gz path is gzipped with mtime 0', _gz.decompress(raw4) == b'abc' and raw4[4:8] == b'\0\0\0\0')
            p5 = os.path.join(td, 'plain.gz')
            save_body(p5, b'abc', 'https://open.test/a', gzip_body=False)
            check('save_body: gzip_body=False writes the bytes as given', open(p5, 'rb').read() == b'abc')
            p6 = os.path.join(td, 'gate.html')
            check('save_body: gate= is passed to keep_decision',
                  not save_body(p6, b'x', 'https://open.test/a', gate=_FixedGate(False))[0] and not os.path.exists(p6))
            p7 = os.path.join(td, 'rb.html')
            check('save_body: robots_body= is passed to keep_decision',
                  not save_body(p7, b'x', 'https://open.test/a', robots_body=b'User-agent: CCBot\nDisallow: /\n')[0]
                  and not os.path.exists(p7))

            # write_derived's fields
            pd = os.path.join(td, 'x.derived.json')
            r = write_derived(pd, 'https://train.test/a', k2[1], {'title': 'T'}, read_utc='2026-11-21T00:00:00Z',
                              http_status=200, sha256='ab' * 32)
            rec = _json.load(open(pd, encoding='utf-8'))
            check('write_derived: returns its path', r == pd)
            check('write_derived: url, metadata, body_kept, body_removed and extracted',
                  rec['url'] == 'https://train.test/a' and rec['read_utc'] == '2026-11-21T00:00:00Z'
                  and rec['http_status'] == 200 and rec['sha256'] == 'ab' * 32
                  and rec['body_kept'] == 'no: ' + k2[1] and rec['body_removed'] == NOT_KEPT_NOTE
                  and rec['extracted'] == {'title': 'T'})
            check('write_derived: field order url, metadata, body_kept, body_removed, extracted',
                  list(rec) == ['url', 'read_utc', 'http_status', 'sha256', 'body_kept', 'body_removed', 'extracted'])
            pe = os.path.join(td, 'e.derived.json')
            write_derived(pe, 'https://train.test/a', k2[1], {'rows': [{'maintainer': 'someone@example.org'}],
                          'note': 'write to someone@example.org'}, contact='someone@example.org')
            raw_e = open(pe, encoding='utf-8').read()
            rec_e = _json.loads(raw_e)
            check('write_derived: email addresses withheld from extracted and metadata, JSON still valid',
                  'someone@example.org' not in raw_e and rec_e['extracted']['note'].startswith('write to ')
                  and rec_e['url'] == 'https://train.test/a')

        # lh_fetch.urlopen and its redirect handler pass the access mode
        try:
            urlopen('https://train.test/a')
            check('urlopen: recurring read refused before any request (NotFetched)', False)
        except NotFetched as e:
            check('urlopen: recurring read refused before any request (NotFetched)', 'disallowed' in str(e))
        try:
            urlopen('https://down.test/a', access='oneoff')
            check('urlopen: unreachable robots.txt refused one-off too', False)
        except NotFetched:
            check('urlopen: unreachable robots.txt refused one-off too', True)
        built = []
        real_build = urllib.request.build_opener

        class _Opener:
            def open(self, request, *a, **k):
                return 'opened'

        def fake_build(*handlers):
            built.extend(handlers)
            return _Opener()
        urllib.request.build_opener = fake_build
        try:
            res = urlopen('https://train.test/a', check_redirects=True, access='oneoff')
        finally:
            urllib.request.build_opener = real_build
        check('urlopen: a one-off read with check_redirects builds the redirect handler with access="oneoff"',
              res == 'opened' and len(built) == 1 and isinstance(built[0], _RobotsCheckedRedirect)
              and built[0].access == 'oneoff')

        class _FP:
            closed = False

            def close(self):
                self.closed = True
        req = urllib.request.Request('https://open.test/start')
        h1 = _RobotsCheckedRedirect('oneoff')
        nr = h1.redirect_request(req, _FP(), 302, 'Found', {}, 'https://train.test/next')
        check('redirect: one-off handler follows to a host refusing only ClaudeBot',
              nr is not None and nr.full_url == 'https://train.test/next')
        fp = _FP()
        try:
            _RobotsCheckedRedirect(None).redirect_request(req, fp, 302, 'Found', {}, 'https://train.test/next')
            check('redirect: recurring handler refuses the same destination and closes the response', False)
        except NotFetched:
            check('redirect: recurring handler refuses the same destination and closes the response', fp.closed)
        fp = _FP()
        try:
            h1.redirect_request(req, fp, 302, 'Found', {}, 'https://user.test/next')
            check('redirect: one-off handler obeys a named Claude-User refusal', False)
        except NotFetched:
            check('redirect: one-off handler obeys a named Claude-User refusal', fp.closed)
        fp = _FP()
        try:
            h1.redirect_request(req, fp, 302, 'Found', {}, 'ftp://open.test/x')
            check('redirect: a non-HTTP(S) destination is refused', False)
        except NotFetched:
            check('redirect: a non-HTTP(S) destination is refused', fp.closed)
        check('no request went anywhere but the stubbed robots.txt files',
              all(u.endswith('/robots.txt') for u in requested))
    finally:
        robots_gate.urlopen = real_urlopen
        globals()['_GATE'] = real_gate
    print('\n%d failed' % len(fails))
    return 1 if fails else 0


class _FixedGate:
    """A stand-in gate for the self-test: may_keep always answers as told."""
    def __init__(self, keep):
        self.keep = keep

    def may_keep(self, url, access=None):
        return self.keep, 'fixed by the self-test'


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        sys.exit(_selftest())
    print('usage: python3 -I scripts/lh_fetch.py --selftest', file=sys.stderr)
    sys.exit(2)
