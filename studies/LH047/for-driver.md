# LH047: for the driving session

Written 8 November 2026 by the LH047 research subagent. Everything here is unreviewed. Figures brought into line with record 0.3 on 9 November 2026, after the evidence review (notes/R-0063-lh047-evidence.md) and the reader-and-inference review (notes/R-0065-lh047-reader.md).

## Faults found in Lighthouse's own conduct (stated plainly)

From studies/LH047/LH047.md, Answer and Findings F5 to F12; each is an observation of what was sent, not a finding about why.

1. **Collectors that do not read robots.txt.** LH041's collector (`studies/LH041/scripts/collect.py`) read no robots.txt and sent 85 requests to PyPI's JSON interface (all 85 answered with HTTP 404), which pypi.org's robots.txt disallows to every crawler (`/pypi/*/json`, `/pypi/*/*/json`); PyPI's documentation (docs.pypi.org) describes the same paths as its API. Four more such requests came from the essay's claims check, its reader review and its drafting agent. LH043's, LH044's and LH045's pre-brief reads, LH046's source reads, the three essay reviews and every ad hoc curl command also read pages without reading robots.txt first. 96 of the 97 robots.txt breaches came from these.
2. **An unreachable robots.txt treated as permission.** LH042's `fetch.py` fetches a page when robots.txt answers 5xx or cannot be reached ("fetch anyway"); RFC 9309 (2.3.1.4) says assume complete disallow. It did so once (dashboard.shadowserver.org, no answer). An ad hoc command read that dashboard before its robots.txt, and LH044's pre-brief sent three requests to web.archive.org, whose robots.txt the container could not reach that evening.
3. **robots.txt cut at 64 KiB.** LH044's collector parses only the first 64 KiB; RFC 9309 (2.5) sets a floor of 500 KiB. CRAN's file was cut; no request was sent on the fragment.
4. **A reviewer that did not name Lighthouse.** The essay's reader review (essays/what-the-watch-would-see/reader-review/) sent 61 requests as `Mozilla/5.0 (compatible; research-reader/1.0)`. The brief's rule had no class for that name; it was classed "does not comply" after it was seen, and 59 of the 61 break no other rule, so the count under the brief as fixed is 113, not 172.
5. **Crawl-delay not honoured.** No Lighthouse collector reads Crawl-delay. LH042 sent two arXiv requests 2 and 13 seconds after its previous one, against arXiv's 15 seconds; LH047's own collector read a paper at sysnet.ucsd.edu 2 seconds after its robots.txt, which sets 5.
6. **Requests in no repository log.** 51 requests appear only in transcripts, the known declawed.io overstep among them; the essay's drafting agent logged 11 reads in its scratchpad only.
7. **Groups addressed to Anthropic's tokens not obeyed** (before the keeper's decision): 6 requests that robots.txt allowed under the own-token reading broke a Claude-User or Claude-Code group (declawed.io four times, three of them ad hoc; LH044's probes of wiki.gentoo.org and ftp.eq.uc.pt), and 24 broke a group naming any of seven Anthropic tokens, most of them ClaudeBot (reading B adds 19 to the overall count, since 5 of the 24 already fail another rule).
8. **Whole pages kept where `use=reference` asks for excerpts**: declawed.io's front page (LH042 data/dash-2026-11-08T1909Z/001.body) and four LH044 bodies (doaj.org, jurnal.itg.ac.id and two COAR pages). Cloudflare calls the field experimental; the brief's rule counts it. Withheld on 9 November 2026 (schedule row use-reference-1): each body is now a placeholder, with the sha256 of the bytes received, the headers and the quotations the records use kept in a `.withheld.json` beside it; the collectors withhold such bodies from their next read (LH042 and LH044 briefs, amendments of 9 November 2026).

Suggested repair (a proposal, for the driving session to decide): one shared fetcher under scripts/ that every collector and ad hoc read goes through: reads robots.txt whole (at least 500 KiB), follows its redirects, obeys the keeper's token rule from scripts/robots_tokens.json, treats unreachable as disallow, honours Crawl-delay, sends the Lighthouse User-Agent, logs every request into the study's folder, and refuses when any of that fails. LH047's `scripts/robots9309.py` and `scripts/fetch.py` are a starting point but do not yet honour Crawl-delay. Whether to delete or keep the five bodies under item 8, and whether LH041's PyPI reads need a note in LH041's record, are the driving session's calls.

## schedule/due.csv rows

```
id,study,task,earliest,latest,status,updated,by,ref,note
LH047-brief,LH047,"Rules of the road (P-0022): brief fixed before part C was tabulated (protocol 0.1, dated note on the keeper's token decision)",2026-11-08,,done,2026-11-08,"driving session 2026-11-08, LH047 subagent (Claude Code, Anthropic cloud)",studies/LH047/brief.md,committed 0fbec8c
LH047-record,LH047,"Record version 0.1: catalogue of the rules (catalogue.md), public evidence of compliance, and the audit of Lighthouse's requests of 8 November",2026-11-08,,done,2026-11-08,"driving session 2026-11-08, LH047 subagent (Claude Code, Anthropic cloud)",studies/LH047/LH047.md,"0.1, unreviewed; replay sh studies/LH047/replay.sh"
LH047-review,LH047,"Evidence review of record 0.1 and catalogue.md (reproduce replay.sh; re-derive a sample of R1 and R2 verdicts by hand from the retained robots.txt copies; check every part B figure against the retained source; check the hand-coded adhoc-requests.csv against the transcripts), then the reader-and-inference review",2026-11-09,2026-11-16,open,,,studies/LH047/LH047.md,no paper before both reviews
LH047-paper-draft,LH047,"A simple paper (an article) from LH047 for readers who have never thought about robots.txt: the rules, how well they are heeded, and what we found in our own requests; drafted after LH047-review",2026-11-16,2026-11-30,open,,,studies/LH047/LH047.md,the keeper asked for a simple paper (proposals.md P-0022)
LH047-paper-reviews,LH047,"Evidence review, reader-and-inference review and recheck of the LH047 paper draft before release",2026-11-18,2026-12-07,open,,,studies/LH047/LH047.md,
LH047-reread,LH047,"Re-audit Lighthouse's own requests for one later week (all fetch logs and transcripts available) under the same rules and the keeper's token rule, after the shared fetcher repair if made; record 0.2",2026-11-23,2026-12-14,open,,,studies/LH047/brief.md,"ends 14 December 2026; needs a short dated amendment naming the week"
```

## investigations/ai-cost-and-spread.md, one line

- **The rules of the road (LH047, 8 November 2026, unreviewed).** Twenty mechanisms by which sites state what automated readers may do, most of them advisory; published measurements of compliance disagree, partly over whether robots.txt covers fetches a user asks for. Of 3,497 requests Lighthouse made that evening, 113 broke a rule as the brief fixed it, against 2 known beforehand, and 59 more, one reviewer's requests under an unattributed name, were classed as breaches after they were seen, for 172; 90 of the 172 got HTTP 404, most of them requests to PyPI's documented JSON interface that its robots.txt asks crawlers to avoid (superseded: the line now on the investigation page follows record 0.3) ([record](../studies/LH047/LH047.md), [catalogue](../studies/LH047/catalogue.md)).

## programme.md, Next

- **LH047, the rules of the road (started by the keeper, 8 November 2026).** Version 0.1 catalogues the rules, gathers the public evidence of how well crawlers heed them, and audits Lighthouse's own requests of 8 November: 113 of 3,497 broke a rule as the brief fixed it, and 59 more under a User-Agent class made after they were seen, for 172 (record 0.3), most from collectors that read no robots.txt. Next: the evidence and reader-and-inference reviews, then a simple paper; the repair the audit points to is one shared fetcher for every collector. An outward question it raises: how many sites that disallow an AI company's training crawler also disallow its user-triggered fetcher, now that operators say robots.txt may not apply to those (L-0013, L-0039).

## sources.md entries (next free numbers; the driving session assigns them)

```
### S46 RFC 9309, the Robots Exclusion Protocol

The IETF standard for robots.txt (Koster, Illyes, Zeller and Sassman, September 2022): groups by product token, longest-match rules, "complete disallow" when robots.txt is unreachable, a parsing floor of 500 KiB, and "these rules are not a form of access authorization". Read 8 November 2026 (studies/LH047/data/reads/catalogue-1/001.body).

https://www.rfc-editor.org/rfc/rfc9309.txt

### S47 Cloudflare's Content Signals Policy and managed robots.txt

Cloudflare's documentation of the `Content-Signal` line (search, ai-input, ai-train, and the experimental use= field), its default, and the policy text's claim to be a condition of access and an Article 4 reservation. Page last updated 2 November 2026; read 8 November 2026 (studies/LH047/data/reads/catalogue-2/003.body).

https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/

### S48 IETF AI Preferences drafts (vocabulary and attachment)

draft-ietf-aipref-vocab and draft-ietf-aipref-attach, editor's copies dated 14 September 2026 (revisions 08 and 05 in LH045's census): the train-ai, ai-use and search categories, the Content-Usage header and robots.txt rule, and the statement that the vocabulary does not ensure preferences are followed. Read 8 November 2026 (studies/LH047/data/reads/catalogue-2/004.body, 005.body).

https://ietf-wg-aipref.github.io/drafts/draft-ietf-aipref-vocab.txt
https://ietf-wg-aipref.github.io/drafts/draft-ietf-aipref-attach.txt

### S49 ai.robots.txt

A community list of 204 entries (203 AI crawler and agent tokens and the policy token `__usage_ai-training`) with operators' stated purposes and robots.txt policies, and ready-made robots.txt and server block files. Read 8 November 2026 through the jsDelivr mirror of its repository (studies/LH047/data/reads/catalogue-2/013.body to 015.body).

https://cdn.jsdelivr.net/gh/ai-robots-txt/ai.robots.txt@main/robots.json

### S50 Anthropic, "Does Anthropic crawl data from the web, and how can site owners block the crawler?"

Anthropic's description of ClaudeBot, Claude-User and Claude-SearchBot, its statements that they honour robots.txt and Crawl-delay and do not bypass CAPTCHAs, and its recognition from 30 October 2026 of a "no AI training" signal. Lighthouse runs on Anthropic's models. Read 8 November 2026 (studies/LH047/data/reads/catalogue-2/018.txt).

https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler

### S51 TollBit, State of the Bots reports

A publisher-tools company's quarterly reports from its customers' logs: the share of AI scrapes that fetched pages the publisher disallowed to that bot by name (3.3% in Q4 2024, 12.9% by March 2025, 13.26% in Q2 2025, about 15% in H1 2026), with per-bot figures. TollBit sells licensing and paywall services. Read 8 November 2026 (studies/LH047/data/reads/evidence-1/001.body, 002.body).

https://tollbit.com/bots/24q4/

### S52 Liu et al., "Somesite I Used To Crawl", ACM IMC 2025

UC San Diego and University of Chicago researchers' test sites, September 2024 to March 2025: seven of nine AI crawlers that visited respected robots.txt, ClaudeBot among them; most third-party assistant fetchers did not. Read 8 November 2026 from the authors' copy (studies/LH047/data/reads/evidence-1/007.body).

https://www.sysnet.ucsd.edu/~voelker/pubs/robots-imc25.pdf

### S53 Cloudflare, "Perplexity is using stealth, undeclared crawlers to evade website no-crawl directives"

Cloudflare's account (4 August 2025) of a test with new domains, of an undeclared crawler it attributes to Perplexity, and of ChatGPT-User stopping at robots.txt in the same test; Perplexity disputes it (its reply unread: a challenge). Read 8 November 2026 (studies/LH047/data/reads/evidence-1/004.txt).

https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/
```

## New leads (for proposals.md, if the driving session agrees)

- **User-triggered fetchers and robots.txt.** How many robots.txt files that disallow an AI company's training crawler also disallow its user-triggered fetcher (ChatGPT-User, Claude-User, Perplexity-User), and does that change over time? LH044's 161 kept files are a baseline; overlaps L-0013 and L-0039.
- **TollBit's figure 4.3** (per-bot bypass rates, including Anthropic's bots) was not read because of this study's three-request cap per host; a later read could add it.
- **Kim et al., IMC 2025** ("Scrapers selectively respect robots.txt directives") was not read: arXiv is an audited host here and the ACM copy answered with a challenge.
