title: Whose robots.txt rules Lighthouse obeys, and which collectors check
kind: working note (method)
date: 2026-11-08

# Whose robots.txt rules Lighthouse obeys, and which collectors check

**In short.** On 8 November 2026 the keeper decided that Lighthouse obeys a site's robots.txt as its own agent and as whatever runs it. So a group addressed to Anthropic's agents binds Lighthouse while it runs on Anthropic's models, and OpenAI's while it runs under Codex. This note says what the rule is, where the token list comes from, and what shared code now applies it. It also lists every collector in studies/ that makes requests to other people's sites, with whether each checks robots.txt at all, for a sweep the driving session will schedule. Most don't; two have fetched kernel.org pages whose robots.txt, as read on 8 November, disallows every crawler.

## The rule

The keeper, 8 November 2026 (proposals.md, From the keeper; AGENTS.md, Rules that matter): "Lighthouse should obey the rules, and is both it's own agent, currently using this harness, model, etc. when we use OpenAI we'll follow those relevant rules, etc."

- A robots.txt group applies if it names Lighthouse's own token, `Lighthouse-research`, or an agent token of the provider, harness or model running the session. If the file names none of those, `*` applies.
- Where several groups apply, the strictest wins: a path is off limits if any applicable group disallows it.
- A collector names the provider it runs under, in the environment variable `LIGHTHOUSE_PROVIDER` (`anthropic` or `openai`). Unset, or any other value, means it can't tell, and it obeys every listed provider's tokens.
- Matching is RFC 9309: product tokens matched without regard to case, groups naming the same token combined, longest match, Allow on a tie, `*` and `$` honoured, /robots.txt always allowed, the body read up to 512 KiB, and only complete lines applied.

## The code

- [scripts/robots_tokens.json](../scripts/robots_tokens.json): the tokens, each with its source and when it was read.
- [scripts/robots_rules.py](../scripts/robots_rules.py): a small matcher using only the standard library. `decide(body, url, provider)` returns allowed or disallowed, which token's group decided, the deciding line and its line number. `provider_from_env()` reads `LIGHTHOUSE_PROVIDER`. `python3 -I scripts/robots_rules.py` runs its offline self-tests. Those include the eight closing-web baseline probes, on their retained robots.txt files: all eight are allowed under the old Lighthouse-only rule and disallowed under this one.
- The closing web (studies/LH044) uses it from read 1 (its brief, Amendment 5). No other collector has been changed.

## The tokens and where they came from

The two providers' own pages were read once each on 8 November 2026, after their robots.txt, with an honest User-Agent and nothing else. They're kept under [robots-tokens-2026-11-08/sources/](robots-tokens-2026-11-08/sources/) with email addresses withheld. In 002.b, Cloudflare's hex encoding of an address (`data-cfemail` and an `email-protection#` link) was also replaced by hand. [fetchlog.csv](robots-tokens-2026-11-08/sources/fetchlog.csv) gives each request's URL, UTC time, status and the sha256 of the bytes received, and [fetch_sources.py](robots-tokens-2026-11-08/fetch_sources.py) is the script that made them.

| Provider | Token | What the provider says it is | Source, read (UTC) |
|---|---|---|---|
| Anthropic | ClaudeBot | collects content that may be used in training | [Anthropic's crawler page](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), 200, 2026-11-08T20:41:51Z |
| Anthropic | Claude-User | fetches pages when a user asks Claude a question | same page |
| Anthropic | Claude-SearchBot | crawls to improve search results | same page |
| Anthropic | Claude-Agent | token added to a real browser's User-Agent when a hosted Claude agent drives it (Claude Duet named) | [Anthropic's hosted-browser page](https://support.claude.com/en/articles/18234133-how-do-anthropic-hosted-browsers-identify-themselves-when-they-browse-the-web-on-a-user-s-behalf), 200, 2026-11-08T20:42:25Z |
| OpenAI | GPTBot | crawls content that may be used in training | [OpenAI's crawler page](https://developers.openai.com/api/docs/bots) (platform.openai.com/docs/bots answered 301 to it), 200, 2026-11-08T20:41:59Z |
| OpenAI | OAI-SearchBot | crawls for ChatGPT's search | same page |
| OpenAI | OAI-AdsBot | visits landing pages submitted as ads | same page |
| OpenAI | ChatGPT-User | fetches pages for user actions in ChatGPT and Custom GPTs | same page |

Seen in the wild, not documented. These are names that robots.txt files in the closing web's baseline (studies/LH044/data/read-2026-11-08T1920Z/, read 19:18 to 19:26 UTC) use to address one of the two providers' agents, and that no provider page read lists. They're marked as such in the JSON and applied.

| Provider | Token | Where it was seen |
|---|---|---|
| Anthropic | Claude-Code (the harness Lighthouse runs in) | git.kernel.org, gitlab.freedesktop.org, ftp.eq.uc.pt |
| Anthropic | anthropic-ai, Claude-Web (older Anthropic names) | 12 and 11 baseline files, among them codeberg.org, repo1.maven.org and wiki.gentoo.org |
| OpenAI | ChatGPT (also how `ChatGPT Agent` reads, since a product token is only letters, `_` and `-`) | openlibrary.org; `ChatGPT Agent` at git.kernel.org, wiki.gentoo.org and four others |
| OpenAI | OpenAI | git.kernel.org, wiki.gentoo.org, www.biorxiv.org and others |

## Choices made here, for the driving session to confirm or reverse

- **Seen-in-the-wild names are applied.** It is the stricter choice: a file that writes `User-agent: OpenAI` or `User-agent: Claude-Code` means those agents. Setting `"applied": false` on an entry in scripts/robots_tokens.json would keep it on record without obeying it. On the closing web's baseline it makes no difference: the same eight probes are withheld either way, because ClaudeBot or GPTBot decides each one.
- **Claude-Agent is applied**, though Anthropic's page describes it as a browser token and does not mention robots.txt.
- **ChatGPT-User is applied**, though OpenAI's page says robots.txt rules "may not apply" to user-initiated actions.
- **`*` only when no applicable token is named**, as the rule is written. So a file that disallows `*` but allows ClaudeBot by name lets Lighthouse in as `anthropic`, where the old Lighthouse-only rule kept it out. No closing-web baseline file does this (0 of 91 parsed). The self-test records the behaviour, so a change of reading would show as a change to that test.
- **Not found:** no token for Codex on OpenAI's page, and no User-Agent for Claude Code's own fetches on either Anthropic page. Neither was searched for further.

## Collectors in studies/ that make requests to third-party sites

How they were found: `grep -rlE 'urllib|import requests|from requests|curl|fetch\(|urlopen|http\.client|httpx|aiohttp|wget'` over studies/ (harbour/.session/ not searched), then each match read for an actual request. Analysis, figure and review scripts that only parse URLs or retained files are left out: LH008 analyse.py and draw_figure.py, LH009 and LH010 analyse.py, LH010 reanalyse.py, LH012 and LH013 review scripts, LH016 replay_x3.py, LH017 r0026, LH033 python_side.py, LH034 R-0039_checks.py, LH035 build.py (its reads were ad hoc), LH044 draw_panel.py and redraw.py, and LH047 audit.py, normalise_logs.py, robots_index.py and transcript_requests.py. "Open rows" are the study's open rows in schedule/due.csv on 8 November 2026. None of these files was edited.

"Own UA, robotparser" means Python's urllib.robotparser checked for the collector's own User-Agent. That parser ignores `*` and `$` inside rules, and it doesn't consult any provider's tokens.

| Study | Scripts that request | Hosts (main) | Checks robots.txt? | Open rows |
|---|---|---|---|---|
| LH002 | collect_depsdev.py, select_cohort.py, swh_check.py | api.deps.dev, pypi.org, archive.softwareheritage.org | no | none |
| LH005 | common.py (curl) | sql-clickhouse.clickhouse.com and JSON APIs | no | none |
| LH006, LH007 | common.py (requests), via collect_pins.py, select_candidates.py | pypi.org, api.deps.dev | no | none |
| LH008 | common.py, via collect.py, select_libraries.py | pypi.org, api.deps.dev, api.osv.dev, ClickHouse | no | none |
| LH009, LH010 | common.py (requests, git), via collect.py, classify.py, osv_ranges.py / select_libraries.py | pypi.org, api.deps.dev, api.osv.dev, ClickHouse, git hosts | no | none |
| LH011, LH012 | common.py (curl), collect.py (LH012), review/requery.py | ClickHouse, pypi.org | no | none |
| LH013 | collect.py, common.py, preflight.py | pypi.org, docs.pypi.org, raw.githubusercontent.com, ClickHouse | no | installer brief (from 10 November) |
| LH014 | common.py, review/r0019_live.py | ClickHouse | no | none |
| LH015, LH017 | collect.py (LH017 also clones over git) | pypi.org, git hosts | no | none |
| LH016 | review/replay-X2/x2_requery.py | ClickHouse | no | none |
| LH018 | collect.py, augment.py | Docker Hub (hub.docker.com, auth.docker.io, registry-1.docker.io), security-tracker.debian.org, ubuntu.com, thephp.foundation | no | none |
| LH019, LH025, LH026 | collect.py | Docker Hub | no | none |
| LH020, LH021 | collect.py | api.github.com | no | none |
| LH022, LH023 | collect.py | api.github.com, Docker Hub | no | none |
| LH024 | collect.py, collect_daily.py | a fixed panel of news and notice URLs (selection-*.json) | no | none |
| LH028 | collect.py | aws.amazon.com, blog.cloudflare.com, openai.com | no | none |
| LH029 | collect.py, review/live_read.py | www.php.net | no | none |
| LH030 | collect.py (panel.json, 17 hosts), feasibility/check.py | www.php.net, www.cisa.gov, www.ncsc.gov.uk, www.suse.com, www.fastly.com, alas.aws.amazon.com and others | no | reads from 9 November |
| LH031 | collect.py, criteria.py, vendor.py, review/live_read.py | www.cisa.gov, raw.githubusercontent.com, paloaltonetworks.com | no | reads from 9 November |
| LH032 | advisory_check.py, review/collect_advisories.py | one CERT's public list and the vendor advisory URLs it links | no | reads from 9 November |
| LH033 | collect.py | packagist.org, php2shell.censys.com, w3techs.com, www.php.net | no | reads from 9 November |
| LH034 | collect.py | nodejs.org, storage.googleapis.com | no | reads from 9 November |
| LH036 | collect.py (panel.json, 13 hosts) | git.kernel.org, www.openwall.com, www.suse.com, www.cisa.gov, www.anthropic.com, ubuntu.com and others | no; see below | reads from 9 November |
| LH037 | collect.py (panel.json, 22 hosts) | vendor advisory sites (Google Cloud, Oracle, Ivanti, Citrix, Zyxel and others) | no | reads from 9 November |
| LH038 | collect.py, policies.py (panel.json, policies.json) | api.github.com, git.kernel.org, lore.kernel.org, cdn.kernel.org, www.openwall.com, www.debian.org, web.archive.org, www.anthropic.com | no; see below | read from 17 November |
| LH039 | collect.py, packagist.py | packagist.org, w3techs.com, api.wordpress.org, wordpress.org | no | daily reads from 9 November |
| LH040 | collect.py, collect_prebrief.py | api.deps.dev, pypistats.org, ClickHouse, documentation pages | no | read 1 from 9 November |
| LH041 | collect.py | osv-vulnerabilities.storage.googleapis.com, pypi.org, raw.githubusercontent.com, registry.npmjs.org | no | read 2 from 7 December |
| LH041 | review/fetch_sample.py | five security vendors' pages | yes: own UA, robotparser | (review) |
| LH042 | scripts/fetch.py, review/live_fetch.py | scanners' and researchers' publications, from fixed URL lists | yes: own UA, robotparser; fetch.py fetches anyway when robots.txt answers 5xx, saying so, where RFC 9309 treats 5xx as complete disallow | December reads |
| LH044 | collect.py, prebrief.py | the closing-web panel | yes: switched to robots_rules.py by Amendment 5 (prebrief.py ran once, before the brief) | weekly reads from 15 November |
| LH045 | collect_epoch.py, collect_ietf.py | epoch.ai, datatracker.ietf.org | yes: own UA, robotparser | from 12 November |
| LH045 | probe.py | pre-brief pages | no | (pre-brief) |
| LH046 | collect.py, review/scripts/refetch.py, fetch_sources.py | data.gharchive.org, documentation pages | no | recheck from 7 December |
| LH047 | scripts/fetch.py | audited sites' robots.txt and pages | yes: RFC 9309 (its own robots9309.py) for Lighthouse-research and seven Anthropic tokens, strictest | (another agent at work there; not read further) |

Many of these hosts are APIs (PyPI's JSON, deps.dev, ClickHouse's public SQL, Docker's registry, GitHub's API) rather than pages. The rule covers them all the same; the sweep would read each host's robots.txt.

**kernel.org (derived from retained files; no request made).** LH044 read the robots.txt files of git.kernel.org and lore.kernel.org at 19:18:56 and 19:18:58 UTC on 8 November 2026. Both disallow `/` to `*` and to ClaudeBot. Under the old rule and the new, those files close every git.kernel.org URL in LH036's panel (the CVE's mbox file and the upstream commit) and LH038's two kernel policy pages and lore.kernel.org query. LH036's read logs show the mbox file requested at its reads of 1, 2 and 5 November, and LH038's show its policy pages requested on 4 November. Whether the files said the same on those days was not checked. Both studies have reads scheduled: LH036 from 9 November, LH038 from 17 November. This was found by checking other studies' URLs against the 91 robots.txt files LH044 kept. Hosts LH044 did not read were not checked.
