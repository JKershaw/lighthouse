# LH059 first read, 25 November 2026 (row LH059-read-1)

**In short.** We read Amazon's post about the attacker's AI agents, the flaw's CVE and NVD records, CISA's listing, and the two other reports of the same framework in use, and tried twice each for the flaw's advisory and the project's release record. Unreviewed: Amazon dates the campaign from 8 September and its finding of the operator's open instance to 10 September, but gives no date for the operation against the medical-imaging tool or for telling the maintainers; the CVE record was published about an hour after Amazon's post on 20 November, and everything Amazon says about what the agents did rests on the operator's own platform records. The advisory and the release record were behind walls at this read, so the question of any public notice before 8 September stays open for them; rereads come on 8 and 15 December.

Read under [the brief](../../brief.md), protocol 0.1, in the one-off mode (`access='oneoff'`, `LIGHTHOUSE_PROVIDER=anthropic`), by a collection subagent in Claude Code (Claude Opus 5.5, Anthropic), 25 November 2026, 14:16:15 to 14:17:20 UTC by the collector's clock. Collector: [collect_read1.py](../../collect_read1.py). Everything here is unreviewed.

## Files

- `fetch_log.jsonl`: one line per request (10), with UTC times, URL, status, bytes and the sha256 of the bytes received. `robots/`: the gate's answer per document (for D2 and D6 the file holds the second route's answer; both routes were allowed, as the log's `robots_ok` shows).
- `sources.csv`: the source register.
- `D1.html.gz`, `D1.txt`: Amazon's post, kept through `save_body` (robots.txt: no training, archiving or `*` refusal at this path). Withheld before writing (`D1_keep.json`): the two indicator addresses, 64 hash-shaped strings in the page's code (none in the text), and two passages describing the exploit mechanism (which endpoint was hit, and how the agents turned file writes into code execution), each replaced by "[detail withheld by Lighthouse]". No email address was present.
- `derived/D2.json` to `derived/D8.json`: the brief's fields only; no body kept for D2 to D8. The standard `body_removed` note in each is the one `write_derived` always writes; the actual reason is in `body_kept` (derived only under the brief).
- `claims_read1.csv`: Amazon's claims C1 to C8 with their bases and a provisional status. `events_read1.csv`: E1 to E7 as read.

## Budget

Ten documents used of ten (counting every request, including the four that met walls: D2 by two routes, D6 by two routes). No discovery search was made: D7's and D8's locators worked, and D6 was located through the CVE record's references; its walls were not a locating failure a search could fix. No link inside a fetched document was followed. D9 and D10 were not used.

## What was found (unreviewed)

**The clock.** Amazon's post: published 2026-11-20T10:30:13-07:00 (17:30:13 UTC), modified time the same. CVE record: `datePublished` 2026-11-20T18:31:38Z, assigner MITRE, updated 2026-11-24T14:43:54Z; its description says the flaw was "exploited in the wild starting in September 2026" and gives no basis, and it names no finder. NVD: published 2026-11-20T19:18:51 (zone not given in the record), analysed. KEV: added 2026-11-23, due 2026-11-26, ransomware use "Unknown"; CISA's notes cite the project's advisory, a pull request and NVD and state no basis of its own. The advisory's dates (E3) and the 0.8.6 release date (E4) were not read. As description: 8 September to the CVE's publication is 73 days, and to KEV's listing 76.

**Before 8 September.** None found among what was read: the CVE record is dated 20 November. The advisory and release record were not read, so this is incomplete, and it never confirms Amazon's zero-day assessment.

**How Amazon's post ties to the flaw.** The post never names the application in its text ("an open-source medical imaging AI application"). The tie is the link behind "GitHub Security Advisory", which goes to the advisory GHSA-qc22-rmgc-vg94 in MONAI Label's repository, the same advisory the CVE record, NVD and KEV cite.

**Amazon's dates (E1).** Campaign of about 48 hours from 8 September; instance found 10 September; operation against the imaging tool: not stated; notification of maintainers: not stated.

**Bases (part a, provisional).** Amazon's window onto the operations is the operator's own Cairn instance, left open without authentication, whose "project configurations, actor prompts, and AI output" Amazon read. So the agents' actions and timings (C1, C2, C4) rest on agent-reported records and the operator's instructions, with Amazon's interpretation; the post describes no Amazon telemetry of the operations themselves. It records a human step after the discovery: the operator gave the agents a tunnel into a second university network, which Amazon "infer[s]" was itself gained with the flaw. The zero-day call (C3) is an absence-based assessment at "high confidence"; attribution (C5) is "moderate confidence" on prompt language, configured time zone and targeting. The CVE, NVD and KEV records corroborate that an advisory and a fixed version exist (C7), not who found or used the flaw.

**Unit 42 (12 November) and Gambit.** Neither names MONAI Label, Amazon or Amazon's campaign, and neither set of indicator addresses matches Amazon's (compared at this read, none retained). Unit 42 describes another Cairn campaign, August to September, on the operator's framework records, and says the flaws used were known ones. Gambit describes a separate, financially motivated operator; its page shows 22 September 2026 while its structured data says 23 November 2026, unreconciled. Gambit states that the operator's console harness "used Anthropic's opus-4.6 (after newer models refused its requests)", which bears on the brief's model and interest disclosure. Both are context, not corroboration, under the brief's dependence rule.

## Walls

- api.github.com, global advisories: HTTP 403 from the session's GitHub proxy (sessions bound to their configured repositories).
- OSV, by the advisory id: HTTP 404; OSV's message named two aliases instead (the CVE and a PyPI advisory id), neither fetched.
- api.github.com repository releases and the github.com release page: HTTP 403 from the session's proxy (repository not enabled for the session). The proxy's message suggests attaching the repository; that was not done, as a way round a wall.

## For the next steps

- The rereads cover D1 to D3 only, and D2 met walls on both routes today. Whether the rereads may try another route to GitHub's advisory, and whether D6 can be read at all from this container, needs a decision before 8 December; otherwise E3 and E4 stay unread and the before-8-September question stays incomplete.
- Gambit's statement naming an Anthropic model is in a source the brief reads only for context; the record's interest disclosure should carry it.
