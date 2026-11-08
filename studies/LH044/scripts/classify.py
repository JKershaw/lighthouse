"""LH044 classifier and robots.txt matcher, as fixed in studies/LH044/brief.md (protocol 0.1).

classify() reads one retained response (status, headers, first 64 KiB of body) and names what a
single labelled request saw. It recognises walls; it never answers, solves or works around one.
The signature lists below are part of the protocol: changing them is a dated amendment, and a
re-run of classify over every retained read (python3 -I scripts/collect.py --classify <label>).

robots_allowed() implements RFC 9309 matching (product-token group, else '*'; longest match wins;
Allow wins a tie; '*' and '$' in patterns), so that no request goes to a path a robots.txt
disallows. Python's urllib.robotparser is not used: it ignores wildcards. From read 1
(amendment 3), the collector follows up to five robots.txt redirects and applies the rules of the
final robots.txt to the probe host; matching here is unchanged.
"""
import re
from urllib.parse import urlsplit, quote, unquote

CLASSIFIER_VERSION = '0.3'
# Amendment 4 (8 November 2026, post hoc, from read 1): reads labelled before AMENDMENT4_FROM are
# classified as version 0.2, so the baseline stays as read; later reads as 0.3.
AMENDMENT4_FROM = '2026-11-09'


def version_for(label):
    return '0.3' if label >= AMENDMENT4_FROM else '0.2'


WALL_CLASSES = ('challenge', 'login', 'rate_limited', 'refused', 'api_closed', 'wall_at_robots')

# (vendor, where, pattern); where is 'h:<header>' (regex on that header's value) or 'b' (body).
CHALLENGE_SIGS = [
    ('cloudflare', 'h:cf-mitigated', r'challenge'),
    # 0.2 (amendment 2, 8 November 2026, post hoc): '/cdn-cgi/challenge-platform' dropped; Cloudflare
    # injects that bot-detection script into ordinary pages too, so it is not by itself a challenge.
    ('cloudflare', 'b', r'challenges\.cloudflare\.com|_cf_chl_opt|cf-chl-'),
    ('cloudflare-turnstile', 'b', r'cf-turnstile'),
    ('anubis', 'b', r'within\.website/x/cmd/anubis|anubis_challenge|Making sure you(?:&#39;|\'|&rsquo;|’)re not a bot'),
    ('go-away', 'b', r'go-away/challenge|git\.gammaspectra\.live/git/go-away'),
    ('aws-waf', 'h:x-amzn-waf-action', r'challenge|captcha'),
    ('aws-waf', 'b', r'awswaf\.com|AwsWafIntegration'),
    ('datadome', 'b', r'captcha-delivery\.com'),
    ('human-perimeterx', 'b', r'px-captcha|_pxAppId'),
    ('imperva', 'b', r'_Incapsula_Resource'),
    ('sucuri', 'b', r'sucuri_cloudproxy_js'),
    ('vercel', 'h:x-vercel-mitigated', r'challenge'),
    ('kasada', 'b', r'KPSDK'),
]
# 0.3 (amendment 4, post hoc, after the baseline's P04): a page that sends the client at once to a
# captcha path, by meta refresh or a script, as the `/.well-known/sgcaptcha/` pages did.
CHALLENGE_SIGS_03 = [
    ('captcha-refresh', 'b', r'(?is)http-equiv=["\']?refresh["\']?[^>]*url=[^"\'>]*captcha'
                             r'|/\.well-known/sgcaptcha/'
                             r'|location(?:\.href)?\s*=\s*["\'][^"\']*captcha'),
]
# Captcha widgets count as a challenge only when the expected content marker is absent.
CAPTCHA_SIGS = [
    ('recaptcha', 'b', r'g-recaptcha|google\.com/recaptcha'),
    ('hcaptcha', 'b', r'h-captcha|hcaptcha\.com/1/api\.js'),
    ('friendly-captcha', 'b', r'frc-captcha'),
]
BLOCK_SIGS = [
    ('cloudflare-block', 'b', r'Sorry, you have been blocked|Attention Required! \| Cloudflare|cf-error-details'),
    ('akamai-block', 'b', r'errors\.edgesuite\.net|Reference&#32;&#35;'),
    ('imperva-block', 'b', r'Incapsula incident ID'),
    ('sucuri-block', 'b', r'Sucuri WebSite Firewall - Access Denied'),
    ('fastly-block', 'b', r'Fastly error: forbidden'),
]
RATE_PHRASES = r'(?i)rate[- ]?limit|too many requests|request limit exceeded|slow down'
AUTH_PHRASES = r'(?i)authenticat|unauthori[sz]ed|access token|api[ _-]?key|log ?in required|sign ?in|requires? (?:a )?login|credentials'
JS_PHRASES = r'(?i)enable javascript|javascript is (?:required|disabled)|requires javascript|you need to enable javascript|enable cookies'
LOGIN_PATH = r'(?i)(/login|/log_in|/log-in|/signin|/sign_in|/sign-in|/users/sign_in|/accounts/login|/auth/|/sso\b|/cas/login|/oauth|/session/new|/idp/|/u/login)'
CHALLENGE_PATH = r'(?i)(\.within\.website/|/cdn-cgi/challenge|/challenge\b|/captcha|go-away)'


def _hdr(headers, name):
    name = name.lower()
    return ' '.join(v for k, v in headers if k.lower() == name)


def _match(sigs, headers, text):
    for vendor, where, pat in sigs:
        if where == 'b':
            if re.search(pat, text):
                return vendor
        else:
            if re.search(pat, _hdr(headers, where[2:]), re.I):
                return vendor
    return ''


# 0.2 (amendment 2, 8 November 2026, post hoc): refusals written by this container's own egress
# policy, not by the origin. They are unread, never walls.
CONTAINER_SIGS = [
    ('container-github-policy', 'b', r'access to this repository is not enabled for this session'),
]


def classify(status, error, headers, body, surface, marker, url='', version=CLASSIFIER_VERSION):
    """Return (class, detail). surface is 'page', 'api' or 'file'; marker may be ''. version '0.2'
    reproduces the baseline's classifier; '0.3' adds CHALLENGE_SIGS_03."""
    if error:
        if error == 'proxy_refused':
            return 'unread_proxy', error
        return 'unreachable', error
    text = body.decode('utf-8', 'replace') if isinstance(body, bytes) else (body or '')
    own = _match(CONTAINER_SIGS, headers, text)
    if own:
        return 'unread_proxy', own
    marker_found = bool(marker) and marker in text
    vendor = _match(CHALLENGE_SIGS, headers, text)
    if not vendor and version >= '0.3':
        vendor = _match(CHALLENGE_SIGS_03, headers, text)
    if vendor and not (200 <= status < 300 and marker_found):
        return 'challenge', vendor
    if status == 429:
        return 'rate_limited', '429'
    if status == 503 and _hdr(headers, 'retry-after'):
        return 'rate_limited', '503+retry-after'
    if status in (403, 503) and re.search(RATE_PHRASES, text):
        return 'rate_limited', '%d+phrase' % status
    if status == 401:
        return ('api_closed' if surface == 'api' else 'login'), '401'
    if 300 <= status < 400:
        loc = _hdr(headers, 'location')
        if re.search(CHALLENGE_PATH, loc):
            return 'challenge', 'redirect:' + loc[:120]
        if re.search(LOGIN_PATH, loc):
            return 'login', 'redirect:' + loc[:120]
        same = (urlsplit(loc).hostname or urlsplit(url).hostname) == urlsplit(url).hostname
        return 'redirect_other', ('same-host:' if same else 'cross-host:') + loc[:120]
    if status in (403, 451):
        blk = _match(BLOCK_SIGS, headers, text)
        if blk:
            return 'refused', blk
        if re.search(AUTH_PHRASES, text):
            return ('api_closed' if surface == 'api' else 'login'), '%d+auth-phrase' % status
        return 'refused', str(status)
    if status in (404, 410):
        return 'gone', str(status)
    if 400 <= status < 500:
        return 'client_error_other', str(status)
    if status >= 500:
        return 'server_error', str(status)
    # 2xx
    if marker_found:
        return 'open', 'marker'
    cap = _match(CAPTCHA_SIGS, headers, text)
    if cap:
        return 'challenge', cap
    if surface == 'page' and re.search(r'(?i)type=["\']?password', text):
        return 'login', 'password-form'
    if not marker:
        return 'open', 'no-marker-set'
    if re.search(JS_PHRASES, text):
        return 'js_notice', 'marker-absent'
    return 'open_unconfirmed', 'marker-absent'


# ---------------------------------------------------------------- robots.txt (RFC 9309)

def parse_robots(text):
    """Return a list of groups: (set of lowercased agent tokens, list of (allow: bool, pattern))."""
    groups, agents, rules, last_was_agent = [], set(), [], False
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key, val = key.strip().lower(), val.strip()
        if key == 'user-agent':
            if not last_was_agent and (agents or rules):
                groups.append((agents, rules))
                agents, rules = set(), []
            agents.add(val.lower())
            last_was_agent = True
        elif key in ('allow', 'disallow'):
            last_was_agent = False
            if agents:
                rules.append((key == 'allow', val))
        else:
            # other lines (sitemap, crawl-delay) do not end a group's user-agent run
            continue
    if agents or rules:
        groups.append((agents, rules))
    return groups


def complete_lines(text, truncated):
    """Amendment 4: never apply a cut-off last line. If the body was cut at the read limit, drop
    everything after the last newline."""
    if truncated and '\n' in text:
        return text[:text.rindex('\n') + 1]
    return '' if truncated else text


def _rules_for(groups, token):
    tok = token.lower()
    mine = [r for a, rs in groups if tok in a for r in rs]
    if any(tok in a for a, _ in groups):
        return mine
    return [r for a, rs in groups if '*' in a for r in rs]


def _norm_path(url):
    s = urlsplit(url)
    p = s.path or '/'
    if s.query:
        p += '?' + s.query
    return quote(unquote(p), safe="/?=&;:@!$'()*+,~%-._")


def _pat_match(pattern, path):
    pattern = quote(unquote(pattern), safe="/?=&;:@!$'()*+,~%-._")
    anchored = pattern.endswith('$')
    if anchored:
        pattern = pattern[:-1]
    rx = '^' + '.*'.join(re.escape(part) for part in pattern.split('*'))
    if anchored:
        rx += '$'
    return re.match(rx, path) is not None


def robots_allowed(groups, token, url):
    path = _norm_path(url)
    if urlsplit(url).path == '/robots.txt':
        return True
    best = None  # (length, allow)
    for allow, pat in _rules_for(groups, token):
        if pat == '':
            continue  # an empty Disallow allows everything
        if _pat_match(pat, path):
            cand = (len(pat), allow)
            if best is None or cand[0] > best[0] or (cand[0] == best[0] and allow):
                best = cand
    return True if best is None else best[1]


AI_TOKENS = ['GPTBot', 'ChatGPT-User', 'OAI-SearchBot', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot',
             'anthropic-ai', 'CCBot', 'Google-Extended', 'PerplexityBot', 'Perplexity-User', 'Bytespider',
             'Amazonbot', 'Applebot-Extended', 'meta-externalagent', 'cohere-ai', 'Diffbot']
