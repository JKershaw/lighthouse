# PHP: what the first-party accounts document about AI's role

**Working evidence note, 23 October 2026.** Codex (GPT-6.1 Sol). This compares claims in retained source responses; it is not a benchmark, a prospective measurement or a new edition of the public PHP article. It reuses known outcomes from LH024/LH028 and follows one link from Google to Wiz under [a bounded plan](plan.md). Model spend is unknown.

The sources describe overlapping research and coordination work involving several models and organisations. **Wiz explicitly names Wiz Atlas, Gemini 4 Argon and GPT-5.6 Sol in its own research.** Its report makes Google's reference to multiple models more specific. OpenAI's account identifies a separate Calif finding assisted by GPT-5.6 Sol and acknowledges Wiz's independent discoveries. These statements can coexist; neither account alone establishes one model's share of the result.

## Claims and their scope

| Stage | OpenAI's account | Google Cloud's account | Wiz's own research account | What the records support |
| --- | --- | --- | --- | --- |
| Discovery | Calif found a critical flaw using GPT-5.6 Sol; Wiz independently found and reported both vulnerabilities. | Wiz used several models and attributes a significant finding contribution to Gemini 4 Argon. | Names Wiz Atlas, Gemini 4 Argon and GPT-5.6 Sol across the research. Its retrospective timeline dates its first finding to 19 August. | Named participants report defensive model use. No task logs, model ablations or full division of labour are provided in these pages. |
| Exploit development | Does not allocate this event's exploit-development work to a particular model in the passages compared here. | Attributes a contribution in exploit development to Gemini 4 Argon. | Says models helped develop and adapt demonstration exploits for different applications and names all three tools. | Researcher-made demonstrations are distinct from hostile requests observed elsewhere. These claims do not identify an attacker's tools. |
| Detection and patch checking | Says its teams and partners helped test fixes; its proposed framework also discusses model-assisted adversarial testing. | Attributes attack-detection and patch-validation contributions to Gemini 4 Argon. | Attributes those tasks to Gemini and describes joint patch verification with PHP, Calif and OpenAI. | Event-specific statements must be kept apart from the broader framework. Neither detection effectiveness nor a model's marginal contribution is measured here. |
| Fixes and release | Assigns fixes and release leadership to PHP's maintainers, with partner support. | Describes the PHP fixes and downstream provider protections. | Describes joint discovery, coordination and patch verification; its timeline says patched releases and disclosure occurred on 21 October. | Maintainer action and provider action have their own records. Model use in research does not establish autonomous release or deployment. |
| Coordination | Describes OpenAI teams working with researchers, maintainers, providers and government agencies. | Describes Google Cloud/Wiz response and customer support. | Names a broad collaboration with PHP, Calif, OpenAI and infrastructure/security providers. | Organisational coordination is documented as participant testimony; these pages do not establish that an AI agent directed the response. |

“Does not allocate” describes this bounded reading, not proof that the task was absent. Wiz Atlas is named as a research tool in Wiz's account; the page does not expose its internal model composition, so the three names should not be treated as three equivalent or independent model experiments.

## What changes in Lighthouse's account

The next reviewed dated update should describe **AI-assisted defensive research across Calif and Wiz**, name each model/tool with its source and scope, and keep PHP's maintainer-led fixes and the human/organisational coordination explicit. The present public account already acknowledges Wiz's independent findings, but its named-model account centres on Calif/OpenAI. The new source adds Wiz's explicit three-tool statement and the wider task claims. This note prepares that addition; it does not silently revise the released article.

Google and Wiz use closely matching task language, and Wiz embeds an endorsement from Google's Gemini security lead. They are participating organisations describing shared work, not two independent experiments confirming model performance. OpenAI is also a participant. Independent discovery by separate research teams is a claim about the research relationship; it does not make Lighthouse's repeated reads independent observations of the software or model's work.

Wiz gives a retrospective discovery/reporting timeline, including a first finding on 19 August and a report to PHP on 24 August. Those dates were read by this session on 23 October; they are not Lighthouse's first-seen clocks or independently verified disclosure milestones. They precede Amazon's source-reported 17 October honeypot trace (LH028), but this ordering does not establish a leak or identify the actor behind that trace.

## What remains unmeasured

Wiz argues that AI reduced the time and expertise required, and contrasts one researcher's week with a much longer hypothetical team effort. The retained pages provide no comparison group, matched no-AI run, task-level time log, failed-attempt denominator or model-specific intervention. Attribute that acceleration assessment to Wiz; do not turn it into a measured speedup, a ranking, or a counterfactual estimate of prevented attacks.

Likewise, demonstrated research exploitation, externally observed attempted exploitation, successful compromise, protection availability and actual deployment remain separate. None of the three accounts supplies actor-side evidence that the reported hostile traffic used AI. Neither speed nor automation fills that gap.

## Source and read clocks

- **OpenAI:** [original article](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/), retained in [LH028's 23 October 16:00 slot](../../studies/LH028/data/snapshot-2026-10-23T1600Z/read_log.json), actual read 16:06:17–16:06:21 UTC. This comparison uses that retained edition; it makes no new current-page observation.
- **Google Cloud:** [original article](https://cloud.google.com/blog/products/identity-security/responding-to-core-php-vulnerabilities-cve-2026-109618-cve-2026-109619), retained as `google_cloud_0.raw` in [LH024's 23 October log](../../studies/LH024/data/snapshot-2026-10-23/read_log.csv), read at 17:44:24 UTC. The page displays 21 October and editor's revisions; those fields do not date the arrival of a particular AI-role sentence.
- **Wiz:** [research report](https://www.wiz.io/blog/php2shell-php-rce), displays 21 October, read 23 October 20:40:48–20:40:53 UTC, HTTP 200, 439,659 retained bytes, no truncation. [Read log](read_log.json), lossless [response](wiz.html.gz). This is outside the fixed watch panels and is not counted as their extra snapshot.

[replay.py](replay.py) verifies retained response lengths/hashes and prints a short evidence-marker index for a reviewer. Marker presence is not automated semantic validation. The source bytes and this attributed matrix require human/agent reading. [Review](review.md) records that check and its limits.
