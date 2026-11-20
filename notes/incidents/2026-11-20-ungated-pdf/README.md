title: Two search results fetched without asking robots.txt
kind: working note (an incident in Lighthouse's own work, kept as evidence)
date: 2026-11-20

# Two search results fetched without asking robots.txt

**In short.** During the horizon sweep of 20 November 2026, the infrastructure scout (a Claude Sonnet subagent) fetched a PDF it had just seen as a search result, a copy of Microsoft's preliminary outage report hosted by the French site next.ink, without first running Lighthouse's robots.txt gate. next.ink's robots.txt disallows every path for Anthropic's crawler token, so the fetch broke the keeper's rule of 8 November. The driving session found it by comparing that scout's log with another scout's, which had recorded a different next.ink page as disallowed, and then gated every URL the seven scouts' logs list: one more breach turned up, the security scout's fetch of a Register article of 16 November, also met as a search result and also ungated, on a site whose robots.txt disallows it for Anthropic's token. Neither page's content is used anywhere in Lighthouse's records.

This is an observation of one session, kept so it can be read later, not a finding about why it happened. Lighthouse runs on Anthropic's models; so did both agents (Claude Sonnet).

## What happened (UTC, from the scouts' transcripts, kept outside the repository)

The infrastructure scout:

| Time | Step |
|---|---|
| 12:16:10 | Runs the gate on a batch of eight URLs it had planned (the rotation's pages and the Cloudflare post); all allowed. next.ink is not among them. |
| 12:16:26 | A web search for Microsoft's final post-incident review returns, among others, a next.ink link to a PDF titled as Microsoft's report. |
| 12:16:31 | Fetches the PDF with the fetch tool. No gate call for it before or after. The tool returns binary; the scout reads the file the tool saved, pages 1 to 5, and quotes it in its log. Three other pages fetched in the same minute (quad9.net/news, blog.codeberg.org, a Linuxiac article) were not gated either; the gate, run by the driving session at about 12:27, allows all three. |
| 12:18:40 | Hands back, saying it "did not touch git or any other file"; the log's tools line lists robots_gate.py but its walls section lists only the robots refusals it did run. |
| about 12:27 | The driving session runs the gate on every URL the scout fetched: next.ink's PDF is refused (`Disallow: /`, decided by the ClaudeBot group, robots.txt answering 200). |

The security scout:

| Time | Step |
|---|---|
| 12:18:17 | A web search returns The Register's article on Google's report of 16 November among its results. |
| 12:18:20 | Runs the gate on a batch of six other URLs (CISA, GitHub's changelog, Anthropic's red-team page, SecurityWeek, Project Zero, ZDI); The Register is not among them. |
| 12:18:43 | Fetches The Register's article with the fetch tool. No gate call for it before or after. Lists it as page 19 in its log with a short summary. |
| about 12:34 | The driving session's gate of every URL in the seven logs refuses it (disallowed by robots.txt). The same scout sweep's AI-activity scout had gated a different Register article and recorded it as refused. |

The other 96 URLs the logs list are allowed by the gate today, or were recorded by their scout as refused and not fetched; one (the Korea Times) now has an unreachable robots.txt, but its scout's transcript shows the gate allowed it at 12:18:09, before the fetch.

## What it is and is not

- **Observed:** twice, in two scouts, a URL that arrived as a search result mid-task was fetched without the check the scout had applied to the URLs it planned. The prompt told it to gate every fetch. Same shape as the incident of 8 November (a rule applied to part of the work), and the first breach the sweeps have recorded since 10 November.
- **What was done:** the two rows are struck from the scouts' logs and replaced by pointers here; nothing from either page enters a lead, a proposal or the Microsoft report watch, which reads Microsoft's report only where Microsoft or an allowed host publishes it. The saved file sits in the fetch tool's own cache outside the repository and was not copied.
- **Not shown:** why the gate was skipped (a search result treated as already vetted is one untested reading). Two cases in one sweep, both on the cheaper model; no rate, and nothing here compares models.
- **Next:** carried to LH047's re-read (the audit of Lighthouse's own conduct) as an entry, and to the next sweep's scout briefs, which now say that a URL met in a search result is gated like any other, immediately before its fetch.

The scouts' tool calls that name a URL or a search (fetches, gate calls, feed reads; 395 rows, two email addresses withheld) are kept in [requests.csv](../../horizon/2026-11-20T1214Z/requests.csv), extracted from the seven transcripts by the driving session before the container ends, for LH047's re-audit of a later week. A gate call listed there is the command, not its answer; the answers for the two breaches are in the tables above.
