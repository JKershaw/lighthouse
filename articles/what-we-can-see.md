title: What we can see of AI activity on the internet
kind: article
version: 0.1
date: 2026-09-26
authors: Lighthouse autopilot (Claude Code subagent), editing task E-0001
model: Opus 5.5 (claude-opus-5-5), as reported to this agent by its harness; not independently checked
grounded_at: ec007fd
cites:
- studies/LH003/LH003.md@ec007fd (LH003, Survey of surveys, version 0.1)
- studies/LH003/sources.md@ec007fd
- studies/LH003/brief.md@ec007fd
- Lighthouse_Founding_Charter.md@ec007fd (LH F01)
- Lighthouse_Research_Design.md@ec007fd (LH F02), S5, S7, S11, S18, S19
- https://www.gharchive.org/ (S5), read by LH003 2026-09-26
- https://docs.deps.dev/ (S11), read by LH003 2026-09-26
- https://pypistats.org/about, read by LH003 2026-09-26
- https://openrouter.ai/rankings (S19), read by LH003 2026-09-26
- https://www.anthropic.com/research/the-anthropic-economic-index, read by LH003 2026-09-26
- https://developers.cloudflare.com/ai-crawl-control/features/analyze-ai-traffic/ (S7), read by LH003 2026-09-26
- https://developers.cloudflare.com/radar/ (S18), read by LH003 2026-09-26
- https://osv.dev/, read by LH003 2026-09-26
- https://incidentdatabase.ai/, read by LH003 2026-09-26

Draft awaiting the keeper's release decision under LH F03; not released.

Nobody can look up how much AI activity there is on the internet. What exists is a scatter of sources, and the strongest finding of Lighthouse's first survey of them is how little their populations have in common. LH003, carried out on 26 September 2026 by reading sources' own public documentation, considered thirty-four candidates and gave seventeen a full entry. Each of the seventeen is scoped to a single population, such as one code forge, one API broker, one vendor's consumer product or one company's network. They count different things in different units: repository events, tokens, web requests, shares of conversations. And, LH003 records, none states how much its population overlaps any other's.

This matters because the obvious move, adding the numbers up, does not work. As LH003 points out, one underlying task could appear as a GitHub event, a dependency bump, a broker-routed inference call and a crawler hit, and nothing would join the four, because no source uses another's identifiers. A sum would mix units, might count one task several times, and would still miss everything that happens off these surfaces. The sources are partial views, not a census.

That conclusion is an interpretation, not a measurement, and two qualifications change how far it reaches. LH003 read each source's description of its own boundary and took no joint sample, so it cannot say how large any overlap is, only that none of the sources states it. And it took each description at its word, without testing it against the data.

## What each kind of source exposes

LH003 sorts sources by the layer they see, using Lighthouse's three plain names. Activity is computation happening, such as a model answering a request or a crawler fetching a page. Residue is what that activity leaves behind: changed code, configuration and data. Propagation is residue enabling later activity somewhere else, as when a changed dependency sets off changes in the projects that rely on it.

**Repository activity** is mostly residue. GH Archive records every public GitHub event, in hourly files, back to February 2011. Open Source Insights maps dependency graphs for seven package ecosystems, npm and PyPI among them, showing what a project's manifest resolves to, not what is installed or running. LH003's entries for both list what they cannot see: private repositories or packages, deployed code, and any reliable sign of whether a person or an agent made a given change. Download counts sit closer to activity and share the blind spot: PyPI's download statistics at pypistats.org do not distinguish a person's install from an automated build job.

**Model usage reports** see activity, in two kinds that differ in what a reader can check. OpenRouter's rankings show tokens processed per model, but only for calls routed through OpenRouter; a model called directly from its provider, run on someone's own servers or reached through another broker is invisible to it. The rankings data are live, queryable and licensed CC BY 4.0. The Anthropic Economic Index, a periodic report, classifies conversations from Claude.ai's Free and Pro tiers by occupational task, excluding API, Team and Enterprise traffic. The index says it is not representative of "all AI use generally", notes that coding is overrepresented, and suppresses any cell under 15 conversations or 5 accounts. As LH003 notes, a reader can re-derive OpenRouter's figures at any time, whereas each index report is a snapshot built from conversation logs no outside reader can query.

**Crawler measurements** see activity where it crosses one company's network. Cloudflare's AI Crawl Control counts requests and bytes from crawlers that Cloudflare has matched to a named AI operator, one domain at a time, and only where the feature is switched on. LH003 lists what it misses: crawlers Cloudflare has not identified, traffic that never touches Cloudflare, and the purpose of a crawl, whether gathering training data or fetching a page for a live agent. Cloudflare Radar publishes aggregate views of traffic across Cloudflare's network and its 1.1.1.1 resolver under a CC BY-NC 4.0 licence; anything that crosses neither is outside it.

At the margins, vulnerability databases such as OSV.dev, which gathers advisories from partner databases, record what LH003 calls a specific kind of residue: that a flaw was disclosed, not whether anyone exploited it. The AI Incident Database records harms from deployed AI that someone chose to submit and, LH003 notes, has no count of deployments to turn its tally into a rate.

None of the seventeen sees **propagation** directly. That is an observation, and it follows from Lighthouse's research design (LH F02), which treats propagation as a link derived between a residue record and later activity, not a surface any instrument reads. A propagation claim must be built by joining two sources, say a dependency change in Open Source Insights and a later change in a dependent project on GH Archive, then testing the join against ordinary explanations such as dependency-update bots, release trains and shared maintainers. That is the work Lighthouse's study LH002 is designed to attempt on a small scale.

> **Illustration, described in words.** A pale field stands for all the AI activity the question asks about, crossed by three bands labelled activity, residue and propagation. Small shaded patches sit in the first two bands, one per source, each labelled with its population: "public GitHub events", "one broker's traffic", "Claude.ai Free and Pro", "Cloudflare domains with the feature on". No line joins any two. The propagation band is empty except for a dashed arrow from residue to activity, labelled "built by joining records". The reader should take two things from it: the patches neither tile the field nor connect, so their numbers cannot be summed; and the unshaded field is unobserved, with no claim made about how much of it there is.

## What stays unobserved

Across all seventeen sources, LH003 found the same things missing. None can say which downloads, crawls or conversations were produced by an AI system rather than a person. None says at which layer such a system was operating. And none sees activity that happens off all these surfaces, such as calls made directly to a model provider rather than through a broker, work in private repositories, and deployments that never trigger a public event.

Lighthouse's charter (LH F01) calls such regions dark, meaning only that no instrument observes them directly. The charter is explicit in both directions: "A dark region is not an empty one," and "A poorly observed system is not thereby a dangerous one." Nothing in LH003 says whether the unobserved part is larger or smaller than the observed part, or more or less benign.

Three limits belong with this account. LH003 catalogues what sources say about themselves on one day; it is not a census of observatories, and candidates it could reach only through search-engine summaries are left out here. No methods reviewer has yet checked the study. And its central claim, that the sources' scopes barely touch, is open to a direct test that LH003 proposes next: take one small population and find which records appear in more than one source. Until someone does, the existing observatories remain partial views that do not add up to a count.

## Sources

Each web source was read by LH003 on 26 September 2026. S numbers refer to the source list in Lighthouse's research design (LH F02), which first checked those links on 25 September 2026.

- LH003, Survey of surveys, version 0.1, 26 September 2026: studies/LH003/LH003.md, sources.md and brief.md.
- GH Archive (S5): https://www.gharchive.org/
- Open Source Insights, deps.dev (S11): https://docs.deps.dev/
- PyPI download statistics: https://pypistats.org/about
- OpenRouter rankings (S19): https://openrouter.ai/rankings
- Anthropic Economic Index: https://www.anthropic.com/research/the-anthropic-economic-index
- Cloudflare AI Crawl Control (S7): https://developers.cloudflare.com/ai-crawl-control/features/analyze-ai-traffic/
- Cloudflare Radar (S18): https://developers.cloudflare.com/radar/
- OSV.dev: https://osv.dev/
- AI Incident Database: https://incidentdatabase.ai/
- Lighthouse Founding Charter (LH F01) and Research Design (LH F02), for the layer definitions and the charter's two sentences on unobserved regions.
