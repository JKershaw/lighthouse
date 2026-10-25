# PHP media sweep: fixed plan

**Fixed 24 October 2026, before the first sweep.** Writer: a Claude Code driving session (Claude Opus 5.5), at the keeper's request. A working record of what the news and published commentary say about the October 2026 PHP flaws, twice a day through 30 October 2026. It is discovery, not a study: a sweep finds leads; it measures nothing and estimates no coverage.

## Queries, fixed

The same six, in this order, in the session's web-search tool, standard mode, one search each, no retry:

1. `PHP vulnerability exploited in the wild`
2. `PHP2Shell`
3. `PHP session upload progress vulnerability CVE-2026-115560`
4. `PHP vulnerability websites taken offline`
5. `PHP vulnerability AI discovered Gemini OpenAI Wiz`
6. `PHP vulnerability affected products vendors patch`

## Each sweep

Run by a Sonnet sub-agent at about 06:33 and 18:33 UTC. It writes `<UTC label>.md` here with: the search time; each query's ranked results as returned (title and URL; the tool's summary only where it names a lead); the list of URLs **new** since every earlier sweep file in this directory; and a triage of the new ones. It may open at most four new pages a sweep, chosen as the highest-ranked new results that make a claim of fact (exploitation, an operator's action, a version or fix, an AI role, a figure), read directly. For each opened page it records the URL, UTC read time, status, the page's own date where shown, and the claim in a sentence with a short quotation (no full copy of any article). Each claim is classed **reported by** the page, with the primary source it names, if any; never as an observation. A first-party page found this way is a lead for the driving session, which decides whether to read it under a study's protocol.

## What reaches the daily log

Only new, consequential reports, one plain line each, written as "X reports that ...", with a link to the sweep file. Anything that would change the public account (a claim of compromise, of exploitation with a stated source, of a new fix or of a version scope for CVE-2026-115560) is flagged for review and needs its primary source read before it goes anywhere near the article. Published reports of harm or compromise are tracked like any other report: quoted, attributed, with what they rest on and any contradicting source beside them. Only Lighthouse's own claim of harm or compromise waits for the keeper (AGENTS.md, as clarified on 24 October 2026).

## Limits

One search tool's ranking, on one day, in English: what it returns depends on its index and on wording, and an absence means nothing. Media restate each other; a claim repeated by many outlets is one claim.

**Change, 25 October 2026:** once a day from 26 October, at about 06:33 UTC, at the keeper's agreement, after three sweeps returned identical results. The queries and rules are unchanged.
