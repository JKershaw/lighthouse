# R-0109: review of the robots intent gate (access modes, may_keep, page_reservation)

**In short.** A fresh agent checked the uncommitted change that carries out the keeper's decision of 21 November 2026 on robots.txt (reading by the owner's intention, and keeping no copy against it) in scripts/robots_rules.py, scripts/robots_gate.py, scripts/lh_fetch.py, scripts/robots_tokens.json and AGENTS.md. Reading works as decided for both providers and for an unknown provider, and every existing collector fetches exactly what it fetched before. Two things in the keeping rule need fixing before it's relied on: one retention token can never match, and `page_reservation` misses a reservation when a response carries more than one X-Robots-Tag header (and fails on a list of header pairs).

Reviewer: Claude Code subagent, Opus 5.5, 21 November 2026 (about 15:20Z), on branch claude/festive-hypatia-defc4p at 8351c36 plus the uncommitted diff. Read: AGENTS.md (Rules that matter), notes/keeper/2026-11-21-robots-intent.md, `git diff -- scripts/ AGENTS.md`, the whole of scripts/robots_rules.py and the changed parts of robots_gate.py and lh_fetch.py, the anthropic and openai entries of robots_tokens.json, and every caller of the gate, decide() and the tokens file under scripts/ and studies/. No code was edited. One web request pair: The Register's robots.txt through the gate CLI, as permitted.

## What was run

1. `python3 -I scripts/robots_rules.py`: all checks `ok`, `0 failed` (29 rule checks, the eight LH044 retained-file probes, and the closing probe check).
2. Edge cases on the rules module, in the scratchpad as edge.py (`python3 -I edge.py`). Output, as printed:

```
archive.org_bot (True, 'no training, archiving or * refusal at this path')
anthropic-ai+Claude-Web (True, 'no training, archiving or * refusal at this path')
PerplexityBot (True, 'no training, archiving or * refusal at this path')
CCBOT case (False, 'CCBot (a training or archiving crawler) is refused at this path')
oneoff Claude-Code refusal True
recurring Claude-Code refusal False
LH allow, * disallow: oneoff True keep (False, '* refuses automated readers at this path')
recurring default == explicit table False False
access_tokens recurring == load_tokens True
oneoff None table {'lighthouse': ['Lighthouse-research'], 'anthropic': ['Claude-User'], 'openai': ['ChatGPT-User']}
retention ['ClaudeBot', 'GPTBot', 'CCBot', 'Google-Extended', 'Applebot-Extended', 'meta-externalagent', 'FacebookBot', 'Bytespider', 'cohere-training-data-crawler', 'Diffbot', 'Amazonbot', 'ia_archiver', 'archive.org_bot']
ClaudeBot Allow, * Disallow /x (False, '* refuses automated readers at this path')
b'<META NAME="ROBOTS" CONTENT="NOAI">' -> meta robots: <meta name="robots" content="noai">
b"<meta content='1' name='tdm-reservation'>" -> meta tdm-reservation: 1
b'<meta name="tdm-reservation" content="0">' -> None
b'<meta name="googlebot" content="noai">' -> None
b'<meta name="description" content="robots and noai rules">' -> None
b'<meta name="tdm-reservation" content=1>' -> meta tdm-reservation: 1
b'<meta name="description" content="1 tdm-reservation">' -> meta tdm-reservation: 1
b'<meta name="robots" content="noai-ish">' -> meta robots: <meta name="robots" content="noai-ish">
b'<meta name="tdm-reservation" content="1"/>' -> meta tdm-reservation: 1
b'<meta name="robots" content="max-snippet:-1, noai"' -> None
two X-Robots-Tag headers (noai first) None
header list of pairs ERROR AttributeError 'list' object has no attribute 'items'
```

3. The gate and lh_fetch offline, with the robots cache stubbed and `_GATE.check` replaced by a recorder (gate_edge.py, `python3 -I gate_edge.py`):

```
anthropic SearchBot-only refusal: recurring False oneoff True oneoff keep True gate.may_keep (False, 'not fetched')
anthropic ClaudeBot-only: oneoff True False ClaudeBot (a training or archiving crawler) is refused at this path
anthropic 404 robots True True
anthropic 403 robots True True
None SearchBot-only refusal: recurring False oneoff True oneoff keep True gate.may_keep (False, 'not fetched')
None ClaudeBot-only: oneoff True False ClaudeBot (a training or archiving crawler) is refused at this path
None 404 robots True True
None 403 robots True True
bad access ctor: ValueError
redirect checks [('https://b/y', 'oneoff')]
urlopen access passed [('https://a/x', 'oneoff')]
```

4. Live, The Register (robots.txt read 2026-11-21 about 15:20Z, sha256 fe0613a0...234c), `LIGHTHOUSE_PROVIDER=anthropic python3 -I scripts/robots_gate.py [--oneoff] https://www.theregister.com/2026/`: recurring `allowed: false`, decided by ClaudeBot `Disallow: /`, exit 2; one-off `allowed: true`, decided by Claude-User `Allow: /`, `keep_body: false`, "* refuses automated readers at this path", exit 0. This matches the decision's own example of a site that welcomes Claude-User and refuses ClaudeBot.

The two scripts were kept in the session scratchpad, not the repository; their full text is reproducible from the outputs above (each line names the input).

## What was checked and found

**(1) Reading, both providers and unknown.** `access_tokens('oneoff', p)` gives Lighthouse-research plus the provider's tokens of kind "user-triggered fetcher" (Claude-User; ChatGPT-User), and both providers' when the provider is unknown, with strictest-wins over named groups and `*` only when none is named. That is the decision's point 1, no more and no less. `load_tokens` reads only the three keys, so the new `retention` object is not mistaken for a provider. Note that in one-off mode a group naming Claude-Code (the harness, applied since 8 November) is ignored: the output above shows a `User-agent: Claude-Code / Disallow: /` file admitting a one-off read. That follows the decision's wording; whether an explicit refusal of the harness is part of the owner's intention is the keeper's question (optional, below).

**(2) Existing collectors unchanged.** `decide()` with no `access` builds `access_tokens('recurring')`, which equals `load_tokens()` (checked: `True`), the table `decide_groups` used before. `RobotsGate` defaults to `access="recurring"`, the new constructor argument is last, and every caller found (`RobotsGate(UA)` in LH036, LH038, LH042, LH046, LH048, LH049, LH051, LH053, LH054, LH056; lh_fetch's `_GATE`; `decide(body, cur, None, tr)` in notes/robots-tokens-2026-11-08/fetch_sources.py; `decide_groups` in LH044) passes nothing new, so each fetches what it did. `check()` returns the same boolean; its info dict gains `access`, `keep_body` and `keep_reason`. No caller writes the dict into a fixed-field CSV; LH055's collector `json.dump`s it, so its robots/*.json files will carry three new fields from the next read (harmless, worth knowing).

**(3) may_keep and page_reservation.** Correct for: a training-crawler refusal; an archiving-crawler refusal; a `*` refusal; a refusal on another path (does not count); empty rules; product-token case (`ccbot/2.0` matches CCBot); a 4xx robots.txt (keep, as decision point 3 says); redirects in lh_fetch (the access mode reaches the redirect check). A retention token is counted only where the file names it, else its view would just be `*`, already checked; right. Found:

- `archive.org_bot` in the retention list can never match. The parser keeps only the leading run of letters, `_` and `-` as the product token (RFC 9309), so a file's `User-agent: archive.org_bot` is stored as `archive`, and the list's `archive.org_bot` is compared against that and fails (output: `archive.org_bot (True, ...)`). **Must fix**: drop it, or record it as `archive` with a note on why, since the list says it's honoured and it isn't.
- `page_reservation` builds a dict from `headers.items()`, so of two X-Robots-Tag headers only the last survives: an `HTTPMessage` (what urllib responses carry) with `noai` then `index` returns None. A list of `(name, value)` pairs, the form content_signal.decide and LH042's fetch use, raises AttributeError. **Must fix** before any collector calls it: accept an HTTPMessage, a dict or a list of pairs, and join repeated values.
- `RobotsGate.may_keep(url)` (and so `lh_fetch.may_keep`) calls `check(url)` in the gate's own mode, and `keep_body` is filled only when that mode allows the URL. On a recurring gate, a page read one-off from a site that refuses only Claude-SearchBot comes back `(False, 'not fetched')` although it was fetched and may be kept. It errs towards keeping less, so optional, but the reason is wrong; computing may_keep regardless of access would fix it.
- Neither may_keep helper says to ask about the final URL after a redirect; a collector passing the request URL may judge the wrong host. Optional: say so in the docstrings, or have lh_fetch expose the final URL's answer.
- `page_reservation` false positives that err safe: any meta tag mentioning `tdm-reservation` with a `content="1..."` (for instance a description), and `noai-ish`. Optional.
- `anthropic-ai` and `Claude-Web` (kind "older Anthropic token") and the name tokens ChatGPT and OpenAI are not counted as training crawlers, so a file refusing only them keeps the body. That follows the file's kinds, but such refusals are commonly written as training opt-outs; optional, for the keeper: add them to the retention list. Conversely the list holds Amazonbot, Diffbot and FacebookBot, which are not plainly training or archiving crawlers, so a refusal aimed at load stops a body being kept. The JSON's `_about` already says the operators' pages weren't read; optional.
- A file that refuses `*` but explicitly allows Lighthouse-research, or allows ClaudeBot itself, still yields no body. That is the decision's letter (point 2) and errs safe; noted, not a defect.

**(4) Tests.** Pass. They cover the reading modes for both providers and unknown, and may_keep and page_reservation on simple inputs. Gaps: may_keep is tested only with a hand-made retention list, never the real one, which is how the `archive.org_bot` dead entry got through; nothing exercises `RobotsGate.check` with an access mode or a 4xx keep answer, the lh_fetch redirect path, repeated headers or a list of header pairs. Optional (beyond the tests the two must-fixes need): add a check that every retention token survives `_token_of` unchanged, and a stubbed gate test like gate_edge.py. The variable `TK` in the new self-tests is unused.

**(5) AGENTS.md.** Accurate to the code on reading and on what may be kept. Two points, both optional: it says the gate "gives both answers (`access='oneoff'`, `keep_body`)", but the page's own reservation is a separate call (`robots_rules.page_reservation`) that a collector must make, and nothing enforces keeping at all: a collector that saves bodies keeps saving them until it is changed to ask. One clause naming `page_reservation`, and "a collector that keeps bodies asks both before saving", would make that plain. The bullet is now long; splitting the 21 November addition into its own bullet would read more easily.

## Outside this diff, but due soon

No collector yet calls `may_keep`, `keep_body` or `page_reservation`. The decision's point 2 binds from now, and LH033's collector keeps W3Techs bodies (W3Techs disallows Bytespider and ia_archiver, so they may not be kept); its next scheduled W3Techs read is LH033-w3techs-dec, from 1 December. That collector, and LH039's, which also reads W3Techs, need wiring before their next read, as the decision's LH033 amendment says.

## Must fix

1. Remove or correct `archive.org_bot` in robots_tokens.json's retention list (it can never match).
2. Make `page_reservation` read repeated headers and accept a list of pairs.

## Resolution (driver, 21 November 2026)

Both must-fix items fixed before commit: `archive.org_bot` is recorded as `archive`, with the reason in the list's `_about`, and a self-test now checks that every retention token is its own RFC 9309 product token; `page_reservation` reads every value of a repeated header from a dict, a list of (name, value) pairs or a urllib headers object, with a self-test. Optional items taken: one-off reads now also obey the harness token (Claude-Code), since a refusal of Claude Code is a refusal of what runs Lighthouse (the decision note says so); `anthropic-ai` is counted as a training refusal in the retention list; `may_keep` takes the access mode and its docstrings say to pass the final URL after a redirect; the unused `TK` is gone; AGENTS.md now names `page_reservation`, says each collector applies both before saving a body because nothing else enforces it, and the 21 November addition is its own bullet. Left as noted: the false positives that err safe, Amazonbot, Diffbot and FacebookBot in the list (kept, erring towards keeping less), and a stubbed gate test. The LH033 collector is wired for W3Techs in the same session (its brief's amendment of 21 November). `python3 -I scripts/robots_rules.py`: 0 failed after the changes.
