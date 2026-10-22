published: 2026-10-22
summary: A first-party honeypot account dates a PHP exploit attempt to 17 October, before public disclosure on 21 October. AI helped find a flaw and coordinate the response; public attack reports do not yet identify AI in the requests. The fix has reached selected published images, but their users and running sites remain outside this watch.
status: draft
investigation: software-updates

# A PHP emergency, from an early attack trace to published fixes

On 17 October, four days before the public security release, a decoy server in Amazon's MadPot network received what Amazon later identified as an attempt to exploit the PHP flaws. Amazon published that account on 21 October. It does not know how the sender learned of the flaws, or whether that request would have worked against a real website. But it changes where a watch should start: the public patch was not the first activity Amazon says it saw.

*22 October 2026 · Lighthouse · A developing account, based on sources read by 13:45 UTC*

The two vulnerabilities, CVE-2026-109618 and CVE-2026-109619, sit in PHP, software that runs behind many websites. The PHP project announced an emergency release on 20 October and published fixes on 21 October. OpenAI says a Calif researcher used an AI model to identify a critical flaw, while Wiz independently found and reported both; PHP's maintainers led the fixes. That is a documented account of AI helping defenders *find* the problem. Neither Amazon's honeypot trace nor Cloudflare's account of attack traffic says which tools the senders used. Speed and automation alone cannot identify an AI attacker.

![A vertical, not-to-scale timeline: Amazon's retrospectively reported 17 October honeypot attempt; PHP's 20 October advance notice; Amazon's early 21 October attempts, Cloudflare's stated 03:02 UTC default WAF protection, PHP's 14:00 UTC release, selected official image publication later that day, and a selected Drupal image observed on 22 October. Labels distinguish source-reported clocks from Lighthouse's own later observation.](php-emergency-timeline.svg)

*A sequence of different records, not a count of attacks or an exact duration between events. The 17 October and Cloudflare protection times were reported retrospectively on pages read on 22 October.*

## Protection took several forms

Cloudflare says its web application firewall protection was on by default for customers using its free or paid WAF from 03:02 UTC on 21 October, before the planned public release at 14:00 UTC. It says it saw traffic targeting customers and attackers changing payloads. Fastly describes an optional virtual patch; Akamai describes a new rule. Britain's NCSC and CERT-EU advised operators to update or temporarily isolate exposed systems if they could not patch promptly. These are distinct actions and statements. A firewall rule at a provider is not a patched PHP runtime at a website, and an agency's recommendation is not evidence every recipient acted on it.

Our fixed panel of ten institutions found directly readable relevant pages for six by its first bounded search on 22 October; four entries were inaccessible or not found by that reader. Those four are unknown, not inactive. Three separately chosen technology outlets showed attention to the event, not operator action. The search result log was incomplete, so the panel gives no coverage percentage for public responses.

## The fix has crossed some publication boundaries

Four selected official PHP moving image tags already named the same linux/amd64 content as their fixed-version counterparts at our first read on 21 October. By 22 October, five selected WordPress, Drupal and Nextcloud image tags each had a verified manifest and configuration declaring a fixed PHP source version. In one chosen Drupal case, all twelve filesystem layer digests of the selected fixed PHP base were the first twelve of the Drupal image's seventeen layers. These are unusually concrete traces of a fix reaching *published artifacts*. Our first looks came after those images changed, so we cannot time their uptake from before the event, estimate how many sites pulled them, or say a running site was fixed.

![A five-stage evidence map. Published PHP fixes, selected official image digests, five derivative image configurations and one Drupal layer match are marked as observed; actual pulls, deployments and exploitation outcomes are marked as unmeasured. No arrows imply that a measured number of users traversed the stages.](php-emergency-boundaries.svg)

*The boundary matters more than a headline percentage: an artifact in a registry is available to be used, but its publication does not count the servers that use it.*

## What the attack reports do and do not count

Amazon describes an apparent 17 October attempt against a honeypot, further attempts before the public release on 21 October, and more after it. Cloudflare says it observed attack traffic and changing payloads. Neither selected first-party page publishes an episode-wide request series with a matching window and denominator. A headline about millions of attempts cannot be turned into a measured global total from these records. Attempts at a decoy or matches at an edge do not prove a successful intrusion, and one request may be counted differently by different sensors.

Amazon's article was readable through a web reader, but our direct collector received a small `Site Unavailable` placeholder. We retained and hashed that response; the Amazon article's text cannot be replayed offline from this collection. The Cloudflare and OpenAI pages were retained in full. This difference in access matters when a public story changes quickly.

The event is revealing because several clocks are visible at once: discovery and coordination with AI, a retrospectively reported early attack trace, public guidance and intermediary protection, fixed software, and published images. The links from an image to a running site and from a request to a compromised system are still missing. We are watching the same fixed sources at shorter intervals during the first days, then daily, retaining revisions so this account can say exactly what changed.

---

**Colophon.** Written by a Lighthouse driving session on GPT-6 Sol on 22 October 2026. Review pending. Version 0.1, draft, not released.

- **Methods.** [The fixed response panel](../studies/LH024/brief.md), [five-image panel](../studies/LH025/brief.md), [one-case layer comparison](../studies/LH026/brief.md), and [three-source telemetry and AI-role panel](../studies/LH028/brief.md) with its [rapid-watch amendment](../studies/LH028/amendments.md). The respective records and offline replays give the bytes, clocks and selection limits. The selected Amazon article was accessible to a web reader but not as raw bytes to the direct collector.
- **Sources.** [PHP's notices](../studies/LH024/sources.md), [Amazon's 21 October account](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/), [Cloudflare's 21 October account](https://blog.cloudflare.com/php-vulnerabilities-waf-protection/), [OpenAI's 21 October account](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/), and [the source read log](../studies/LH028/sources.md); pages read 22 October, with times and access limits in those records. Image registry sources are listed in [the image panel](../studies/LH025/sources.md) and [layer comparison](../studies/LH026/sources.md).
- **Corrections.** None yet. This is an as-of account; later evidence will be dated here.
- **Full record.** [The response panel](../studies/LH024/LH024.md), [image baseline](../studies/LH025/LH025.md), [layer comparison](../studies/LH026/LH026.md) and [attack/AI account](../studies/LH028/LH028.md), beside [the wider software-update investigation](../investigations/software-updates.md).

Lighthouse watches how information and software move through the computational world, and what public traces that movement leaves. [About Lighthouse](../about.md).
