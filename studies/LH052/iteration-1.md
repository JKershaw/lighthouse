# What do four public outage accounts expose about AI and organisational capacity?

**In short.** This feasibility reading can describe technical failure and recovery in two of the four selected outages, while two accounts were inaccessible. The readable accounts do not establish a chain from AI-motivated staffing changes through lost knowledge to altered operational outcomes. The driver recorded the checkpoint and completed the conditional second iteration on the two preselected operator studies; collection has stopped.

Version: 0.2, evidence and reader checked; final recheck complete. Date: 13 November 2026. Writer: Codex, OpenAI; exact runtime model identifier unavailable. Monetary usage and token totals unavailable, not zero. Protocol: [brief.md](brief.md), retained before collection in local commit `bb8a6e9b1b0becee41b0cc35e22e6bab8c2d7a74`; the initial first-iteration record and data were retained in local commit 68b7093 before iteration 2 collection. Collection procedures began 08:52:02 to 08:53:06 UTC on 13 November; policy inspection continued thereafter. Exact substantive HTTP start and response-arrival clocks were not separately captured. Instruments: Python 3.12.14 standard-library HTTP and HTML parsers; repository `scripts/robots_gate.py`, `robots_rules.py`, `robots_tokens.json`, `redact_emails.py`; `LIGHTHOUSE_PROVIDER=openai`. Case-source matrix: [cases.csv](cases.csv); provenance: [sources-iteration-1.json](sources-iteration-1.json); access log: [reads-iteration-1.jsonl](reads-iteration-1.jsonl). Evidence is attributed operator reporting, not independently observed operations. Prior outcome knowledge and deliberate selection are disclosed in the brief; this is not an independent confirmation of the background review.

## Answer

The strongest supported mechanism is **technical amplification and impeded recovery through shared dependencies, retry behaviour and returning demand**. GitHub reports a scaling-policy/capacity failure followed by software client and gateway retries, with scraping attacks also reported to impede recovery; Cloudflare reports a configuration failure in a machine-learning serving path followed by debugging overhead and login backlogs. Both describe human mitigations and successful restoration. This is an interpretation across the readable operator accounts, not a prevalence estimate or an AI-causation finding. [I1-S01-E01/E02, I1-S05-E01/E02, I1-S04-E01/E02]

No readable source connects an AI-motivated service-team staffing change, loss of relevant expertise or review capacity, and an operational outcome. GitHub does report that operational practices lagged increased change and complexity and that teams/resources were redirected towards availability. That exposes an organisational claim, but supplies neither staffing baselines nor an AI link nor a measured loss of knowledge. Source silence is not evidence of no AI involvement; the two unread cases are unavailable, not silent. [I1-S01-E04/E05; I1-S05 follow-up actions; I1-S04 remediation section]

## Findings

| Fixed case | Readable evidence | Technical and recovery observability | Organisational attribution |
| --- | --- | --- | --- |
| GitHub, 17 August 2026 | I1-S01, published 20 August; linked I1-S05, report labelled 17 August 21:15 UTC | Scaling limits and authentication cascade; retries extended Copilot recovery; rerouting and retry controls helped | Reported operational-practice lag and resource redirection; AI-motivated staffing and expertise-loss chain not disclosed |
| Google Cloud, 12 June 2025 | I1-S02 unavailable | No case claims coded from returned placeholder | Unavailable |
| AWS, 19-20 October 2025 | I1-S03 unavailable | No case claims coded from returned placeholder | Unavailable |
| Cloudflare, 18 November 2025 | I1-S04, metadata dated 18 November | Permissions/configuration change affected Bot Management; rollback, restarts and scaling restored service | Failed technical assumption and initial diagnostic error reported; staffing history and AI-motivated reorganisation not disclosed |

**AI role needs its own distinction.** At GitHub, Copilot is an affected product; the source identifies a latent VS Code retry bug and gateway retry logic. The described mechanism is software retry logic, and the report does not establish that an AI agent initiated the traffic or chose the retries. It does not attribute the incident to AI code generation. GitHub also reports scraping attacks on codeload endpoints impeded recovery; their AI origin is not disclosed. At Cloudflare, an ML model normally produces bot scores used in access rules, so operational inference is explicitly present in the affected serving path. The reported failure involves a configuration generator, feature limit and proxy error; the account does not establish an autonomous model decision causing the outage or writing the change. Denial of malicious activity is not a denial of AI involvement. [I1-S01-E03, I1-S05-E02/E03, I1-S04-E01/E03]

**Controls and recovery are part of the evidence.** GitHub reports successful traffic rerouting and restoration after retry mitigation. Cloudflare reports known-good configuration restoration, service restarts and scaling of dashboard concurrency. Both describe planned follow-up controls; plans do not establish their subsequent effectiveness. No case in this reading measures a staffing handover, retained expertise or human review throughput. [I1-S01-E02/E05, I1-S05-E02/E04, I1-S04-E02/E04]

**Clocks are not interchangeable.** GitHub's linked account reports 13:28-21:15 UTC on 17 August, with most services recovered by 16:36 and the Copilot Token Service by 21:02; its retrospective report's actual publication/revision time is unavailable despite its displayed 21:15 label. The Cloudflare opening gives 11:20 UTC onset, while its timeline gives 11:28; this internal discrepancy is retained as conflicting, not reconciled. It reports core traffic largely recovered at 14:30 and all systems normal at 17:06. HTML publication metadata can have placeholder precision; the Cloudflare page also carries a later modified date in the provenance file. No timeline was reconstructed for the unread cases. [I1-S05-E05, I1-S04-E05]

## Method

The four known cases were taken in the fixed order. One discovery query per provider, issued together in one search-service call, resolved first-party URLs. Search snippets appeared incidentally; none is used as evidence, and no search rendering was used to fill an inaccessible account. Each resolved URL passed through the repository gate before the direct content request. The single linked follow-up was GitHub's root-cause/status account, linked explicitly from the main account's recovery paragraph. No additional source or case was sought.

Thirteen direct HTTP requests were recorded: five initial robots reads, five substantive endpoint requests, and three further robots-only inspections for retention comments on the readable hosts. There were no observed redirects, login attempts or credentials. Every direct response has its original-byte SHA-256, byte count and HTTP duration in the log. These total 677,667 received bytes and 81.410 seconds of measured HTTP duration; they exclude search backend activity, tool/harness work outside measured requests and analyst time. Connection setup, transfer and wait components within the measured HTTP duration were not separated. Search used one service request containing four queries, tool-reported wall time 1.8 seconds; original response bytes/hashes are not exposed by that service. The counts are a footprint of this collection, not its full computational or monetary cost. Analyst work was approximately 15 minutes by session-clock estimate; complete active-time metering is unavailable.

The gate mechanically returned allowed for Google and AWS, but both their robots URL and substantive URL returned the same 195-byte HTTP-200 HTML page headed **Site Unavailable**, saying access was unavailable. Consequently their authentic provider robots policies are unavailable/ambiguous and their incident accounts are unavailable. The collector recognised this after the gated substantive request. It stopped each case without a retry, alternate fetch route or web-render bypass. A syntactic no-rules result is not evidence of an authentic permissive policy. The other three robots responses were readable; Cloudflare explicitly signalled `ai-input=yes`, `search=yes` and `ai-train=yes`. Only brief evidence paraphrases are retained regardless of those signals.

There are five resolved documents/attempted substantive endpoints, three readable substantive documents and two missing accounts, within the eight-document ceiling. Thirty case-source-field rows retain the unit and source IDs: 15 explicit reported evidence, 12 unavailable, two not disclosed and one conflicting. These are coding counts, not independent cases or statistical observations. Codes may expose one disclosed part of a field while its causal components remain unknown; the AI-role rows and notes name those unknowns. Each retained evidence file supplies exact section/paragraph locators and 92-113 words of paraphrase, below 150 per source. Full bodies are temporary scratch material only, with email redaction applied before saving; the repository does not retain full copyrighted sources. The byte hashes cannot replay the sources, and the short evidence cannot reproduce private operational facts.

To check the coding counts without network access:

```python
import csv, collections, json
from pathlib import Path
p = Path('studies/LH052')
r = list(csv.DictReader((p / 'cases.csv').open()))
print(len(r), dict(collections.Counter(x['classification'] for x in r)))
h = [json.loads(x) for x in (p / 'reads-iteration-1.jsonl').read_text().splitlines()]
h = [x for x in h if x['type'] == 'http_request']
print(len(h), sum(x['bytes'] for x in h), round(sum(x['elapsed_seconds'] for x in h), 3))
```

Recorded output: `30 {'explicit reported evidence': 15, 'unavailable': 12, 'not disclosed': 2, 'conflicting': 1}`; `13 677667 81.41`.

## Limits

This deliberately selected panel is conditioned on already-known failures. Two cases could not be read, and public operator reporting has selective visibility even when accessible. Technical controls and operational-practice statements do not measure effective understanding or verify staffing causation. Software retries, architectural coupling, capacity/demand change, reported scraping attacks of undisclosed AI origin and reporting omissions remain alternatives. Neither missing information nor a successful recovery establishes safety. No Microsoft causal claim, company-wide layoff inference, significance test or outage-frequency estimate is made. Fresh evidence and reader reviews have checked this record; the final recheck is complete; this is a working record, not a released article.

## Next

The condition for iteration 2 is met: this outage panel does not support a staffing-to-operations chain. The driver recorded the checkpoint and completed the second iteration on the two operator studies named in the fixed protocol; collection is now stopped. This recommendation authorises no outreach, new cases, standing watch or new experiment. Publication remains blocked pending John's explicit approval; no commit or push was performed by this collector.

## Corrections

0.1, 13 November 2026: first unreviewed record. The collection clock is explicitly the start of the gate/collection procedure because the collector reused that timestamp for its later substantive HTTP request; exact HTTP start/arrival is unavailable. Google and AWS's HTTP-200 responses were reclassified as unavailable placeholders after inspection; the gate's mechanical result remains in the log, with the policy limitation explained above. These are collection/coding limitations, not a protocol amendment. No earlier result edition exists.

0.2, 13 November 2026: fresh evidence review restored GitHub's reported scraping attacks as a recovery complication with AI origin unknown, and clarified which overhead the measured HTTP duration excludes. Evidence-file word counts were recalculated. The organisational-attribution conclusion is unchanged; version 0.1 is retained in commit `68b7093`. Full-study review is still pending.

Completion note, 13 November 2026: the final recheck's two exact status corrections were applied. Canonical identifier is now LH052; the brief records the administrative alias. Collection and findings are unchanged.
