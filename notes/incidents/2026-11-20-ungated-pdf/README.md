title: A search result fetched without asking robots.txt
kind: working note (an incident in Lighthouse's own work, kept as evidence)
date: 2026-11-20

# A search result fetched without asking robots.txt

**In short.** During the horizon sweep of 20 November 2026, the infrastructure scout (a Claude Sonnet subagent) fetched a PDF it had just seen as a search result, a copy of Microsoft's preliminary outage report hosted by the French site next.ink, without first running Lighthouse's robots.txt gate. next.ink's robots.txt disallows every path for Anthropic's crawler token, so the fetch broke the keeper's rule of 8 November. The driving session found it by comparing that scout's log with another scout's, which had recorded a different next.ink page as disallowed. The content read is not used anywhere in Lighthouse's records.

This is an observation of one session, kept so it can be read later, not a finding about why it happened. Lighthouse runs on Anthropic's models; so did this agent.

## What happened (UTC, from the scout's transcript, kept outside the repository)

| Time | Step |
|---|---|
| 12:16:10 | Runs the gate on a batch of eight URLs it had planned (the rotation's pages and the Cloudflare post); all allowed. next.ink is not among them. |
| 12:16:26 | A web search for Microsoft's final post-incident review returns, among others, a next.ink link to a PDF titled as Microsoft's report. |
| 12:16:31 | Fetches the PDF with the fetch tool. No gate call for it before or after. The tool returns binary; the scout reads the file the tool saved, pages 1 to 5, and quotes it in its log. Three other pages fetched in the same minute (quad9.net/news, blog.codeberg.org, a Linuxiac article) were not gated either; the gate, run by the driving session at about 12:27, allows all three. |
| 12:18:40 | Hands back, saying it "did not touch git or any other file"; the log's tools line lists robots_gate.py but its walls section lists only the robots refusals it did run. |
| about 12:27 | The driving session runs the gate on every URL the scout fetched: next.ink's PDF is refused (`Disallow: /`, decided by the ClaudeBot group, robots.txt answering 200). |

## What it is and is not

- **Observed:** a URL that arrived as a search result, mid-task, was fetched without the check the scout had applied to the URLs it planned. The prompt told it to gate every fetch. Same shape as the incident of 8 November (a rule applied to part of the work), and the first breach the sweeps have recorded since 10 November.
- **What was done:** the quotations from the PDF are struck from the scout's log and replaced by a pointer here; nothing from it enters a lead, a proposal or the Microsoft report watch, which reads Microsoft's report only where Microsoft or an allowed host publishes it. The saved file sits in the fetch tool's own cache outside the repository and was not copied.
- **Not shown:** why the gate was skipped (a search result treated as already vetted is one untested reading). One case; no rate.
- **Next:** carried to LH047's re-read (the audit of Lighthouse's own conduct) as an entry, and to the next sweep's scout briefs, which now say that a URL met in a search result is gated like any other, immediately before its fetch.
