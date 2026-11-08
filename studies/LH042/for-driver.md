# LH042: for the driving session

Everything below is for shared files this study may not edit. Nothing here has been reviewed.

## schedule/due.csv rows

The study's brief schedules two monthly index reads (Amendment 2), one bounded re-search and the record; the weekly dashboard read first planned was cancelled before its first date (Amendment 1), so it has no rows. An evidence review row is added because version 0.1 is unreviewed.

```
LH042-review,LH042,"Evidence review of record 0.1 (studies/LH042/LH042.md) before any public use: admission calls listed under Limits, five quotations reread against the bodies, sh studies/LH042/replay.sh, figure in both themes; note in notes/",2026-11-09,2026-11-20,open,2026-11-08,,studies/LH042/LH042.md,"unreviewed; reader review follows if a piece is drawn from it"
LH042-index-2026-12,LH042,"Read OpenA2A's Exposure Prevalence Index (brief, Amendment 2): fetch.py --label index-<UTC> --urls studies/LH042/scripts/index_urls.txt; extract_index.py data/index-<UTC>; admit new sweeps into data/counts.csv with quotations; check_quotes.py; build.py",2026-12-03,2026-12-07,open,2026-11-08,,studies/LH042/brief.md,"one request; restated rows kept beside earlier readings"
LH042-research-2026-12,LH042,"Bounded re-search: the queries of searchlog.md D1 to D23, restricted to publications after 8 November 2026; fetch and admit new counts under protocol 0.1; log in searchlog.md",2026-12-07,2026-12-14,open,2026-11-08,,studies/LH042/brief.md,
LH042-index-2027-01,LH042,"Last read of OpenA2A's Exposure Prevalence Index (brief, Amendment 2), as LH042-index-2026-12",2027-01-03,2027-01-07,open,2026-11-08,,studies/LH042/brief.md,"brief Amendment 2: the last read; a later read needs a further amendment with its own end date"
LH042-record,LH042,"Record version 1.0 (Answer, Findings, Method, Limits, Next, Corrections) after the January read, then its reviews",2027-01-07,2027-01-15,open,2026-11-08,,studies/LH042/brief.md,
```

## investigations/ai-cost-and-spread.md

Under Questions, item 2, after "Lighthouse scans nothing.":

> Brief fixed 8 November 2026 ([LH042](../studies/LH042/brief.md)); record 0.1, unreviewed, the same evening: 91 published counts from 19 publishers, admitted only where the page names what, when and how it counted. Counts after February 2026 exist for Ollama and OpenClaw, but they disagree by large factors because they count different things; the one long run made one way is OpenA2A's monthly Shodan index (OpenClaw-family category 267,172 on 11 April, 153,638 on 26 June, 205,872 on 1 November 2026). No internet-wide count of exposed Android debug ports was read. Index reads in December and January.

Under "Where the evidence stands", replacing or following "Nothing measured yet.":

> Exposure (LH042, record 0.1, unreviewed): published counts are plentiful and rarely comparable; reachable is not compromised, and Lighthouse scanned nothing.

## programme.md, Next

> ### Brief and record 0.1, 8 November 2026: exposed AI services, dated (LH042)
>
> Question 2 of the third investigation, from leads L-0001 to L-0003. The brief fixed how a published count is admitted (the counter's own page names what, when and how), kept methods apart and dated counts by scan; it was committed before any count was taken from a retained source. Collection found 91 admitted counts from 19 publishers and six series with two or more dates, five of them OpenA2A's monthly Shodan index; the sweep's "no count since February" was not borne out, but no publisher other than OpenA2A counted the same way twice. A weekly read of SecurityScorecard's DECLAWED dashboard was cancelled because its robots.txt disallows the figures' path and blocks AI agents' fetchers; OpenA2A's index, which allows them, is read in December and January instead. Next: the evidence review, the December re-search, and record 1.0 by 15 January 2027. Exposure is not spread, and nothing here is.

## sources.md entries

Numbers left to the driver (others may be adding entries at the same time).

> ### S__ OpenA2A Exposure Prevalence Index
>
> OpenA2A Research's public monthly index of internet-facing AI services from Shodan index analysis: 207 queries in ten categories, each category the sum of its queries, one point per month (the latest sweep that month), dated by the UTC day of the sweep, with the number and range of sweeps where a month held several. Its methodology page says the reports are written by OpenA2A's autonomous research system, ARIA, with a named human editor; that from 18 June 2026 totals exclude credential categories; and that the index sees what Shodan indexes. Its robots.txt allows its pages to every agent. LH042 read it on 8 November 2026 (latest sweep 1 November 2026, first listed 14 March 2026).
>
> https://research.opena2a.org/indices/exposure-prevalence
> https://research.opena2a.org/methodology

> ### S__ Ollama in the Wild
>
> Zuyao Xu, Xiang Li, Yuqi Qiu and Lu Sun, Ollama in the Wild: A Longitudinal Measurement of Exposed Ollama LLM Endpoints at Internet Scale, IMC 2026 (arXiv 2609.07115, 7 September 2026). Daily sweeps of the IPv4 space on Ollama's default port from 14 February 2025 to 13 February 2026 (362 observed days); it states an aggregate data release whose location LH042 did not find. Read 8 November 2026.
>
> https://arxiv.org/abs/2609.07115

> ### S__ SecurityScorecard DECLAWED
>
> SecurityScorecard STRIKE's live dashboard of OpenClaw instances ("favicon hash and HTTP title fingerprinting" from its internet-wide scans). Its figures load from a path its robots.txt disallows to every agent, beside a block list naming AI agents' fetchers, so Lighthouse does not read its counts (LH042, Amendment 1). Page read 8 November 2026.
>
> https://declawed.io/

## Notes for the driver

- One request to DECLAWED's disallowed `/api/stats` was made during the design read, before the whole robots.txt had been read; the brief's Amendment 1 records it as a fault.
- One retained body with one email address was committed in 20ca9a9 before the keeper's email rule; the next commit replaces it with the redacted body, and the earlier blob remains in history.
- No new proposal. A possible later question, not proposed: whether OpenA2A's index and Censys's report window (October 2025 to July 2026) can be set side by side once Censys's report figures are readable from Censys itself.
