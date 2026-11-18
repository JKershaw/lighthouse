title: When a model finds the bug
kind: investigation
id: model-found-bugs
attention: active
question: When an AI model finds a serious flaw in software the internet runs on, and writes a working exploit for it, what happens next in public, who says what and when, how do the signals defenders rely on respond, and where does the fix land?
started: 2026-11-01
studies:
- studies/LH036/brief.md
- studies/LH038/brief.md
- studies/LH048/brief.md
- studies/LH054/brief.md

## Why this, and why now

On 27 October 2026 Anthropic described five attack chains found with an unreleased internal model, among them an exploit the model wrote for CVE-2026-98432, a flaw in how the Linux kernel handles incoming IPv4 connections, giving remote root on servers with a Multipath TCP listener. The kernel had published the flaw and its fixes twelve days earlier and scored it 9.8 out of 10. Read on 1 November, EPSS, the public model that estimates how likely a flaw is to be exploited in the next 30 days, gave it 0.46 per cent for 31 October, below the median, and CISA's catalogue of exploited flaws did not list it. Debian's security updates carried fixes; Ubuntu's were pending, and its oldest supported releases had none. These are observations from one morning's reads, kept with the study's brief.

Lighthouse watches for what AI systems do on the internet and what their activity leaves behind. A model that finds a flaw and writes the exploit is such activity, and what follows, from the advisory to the fixed package, runs on roads the [software updates investigation](software-updates.md) already follows. This investigation keeps one flaw in view as its core and asks a few bounded questions around it. It does not try to follow every AI-related security story.

## Questions

1. **The core watch** ([LH036](../studies/LH036/brief.md), running from 1 November 2026). For CVE-2026-98432: how EPSS, CISA's catalogue, the CVE record's scoring and enrichment, NVD and the references move, read back to 15 October; and when each named distribution release's security channel carries a fix. Twice a week to mid January 2027.
2. **The disclosure timeline** ([LH038](../studies/LH038/brief.md), brief fixed 4 November 2026). A dated reconstruction from primary sources: report, fix, CVE, stable releases, distribution advisories, Anthropic's post, downstream notices; set beside the policies each party states, which were read and kept before the brief was fixed: Anthropic's (90 days, and 45 days after a patch before full technical details, worded differently in the post itself), the kernel security team's (fixes released at once or within 7 days, and AI-found bugs treated as public), the kernel CVE team's, the linux-distros list's (14 days at most), Ubuntu's and Debian's. The report date is not public; the timeline records it as unknown unless a public source gives it. One read on 17 November; the reviewed record on 18 November (below); one revision after LH036 stops.
3. **How the post's five chains were scored.** Chrome, Safari, Android, Windows and Linux: severity, EPSS and CISA's catalogue for each flaw the post names, a set chosen by the post, not by us. Five cases, not a sample. ([LH048](../studies/LH048/brief.md), brief fixed 9 November 2026.) The post names only two flaws by number, CVE-2026-33096 (Windows) and CVE-2026-98432 (Linux); the Chrome and Safari flaws are matched, by a rule fixed before reading, to the release notes the post links, and the Android chain has no identifier. Mondays to 4 January 2027, the record by 15 January. On 10 November the rule matched one Safari flaw that Apple credits to Anthropic (CVE-2026-43715) and one Chrome flaw that fits two steps; four Chrome and Safari steps matched nothing. At the first reading none of the four flaws that can be followed was in CISA's catalogue, all were rated High or Critical by at least one source, and their EPSS percentiles ran from 0.42 to 0.70 ([checkpoint](../studies/LH048/checkpoints/2026-11-10.md), unreviewed).
4. **Later, an essay**: what responsible disclosure means when the finder is a model and a working exploit runs in under an hour. It waits for the evidence.

## Model disclosure

The exploit and the post are Anthropic's, and Lighthouse's agents, writers and reviewers alike, run on Anthropic models. The keeper chose to disclose this on every record and piece of the investigation rather than add a reviewer from another provider, for now (1 November 2026). Reviews are asked to look for wording easier on Anthropic, or on the exploit's significance, than the sources allow.

## What it will not do

It describes scores, listings, dates and fixes. It does not test any system for the flaw, judge whether anyone acted rightly in a record (judgement belongs to an essay, argued openly), or claim in Lighthouse's voice that the flaw is being exploited; a published report of exploitation is recorded as its source's claim.

## Where the evidence stands

**Interim, reviewed against the data and for how it reads, and rechecked (17 November 2026).** The core watch's [interim record](../studies/LH036/LH036.md), to the read of 16 November, opens with the state of things: CISA had not listed the flaw as exploited by its catalogue of 13 November, which does not say whether anyone has exploited it; the exploit-prediction score's one large daily rise came two days before Anthropic's post, and the dates do not say why it moved; and fixes had reached Debian, the kernels of Red Hat's Enterprise Linux 8, 9 and 10 and Ubuntu's four newest releases, with Ubuntu's three oldest affected releases still pending. Read the record for the figures and their limits. Reads go on twice a week. The disclosure timeline took its one read on 17 November, and its [record](../studies/LH038/LH038.md), reviewed and rechecked on 18 November, finds no public date for when the flaw was reported. The fix's author date is 1 October; it was in stable kernels released on 11 and 15 October, and the CVE was published on 15 October, 12 days before Anthropic's post of 27 October. SUSE dates the earliest of its advisories we read two ways, 24 October on the advisory pages and 29 October in its list of announcements, either side of the post; the Red Hat errata we read are dated from 1 November. The post came within 45 days of every candidate patch date before it, the wait Anthropic's policy page says it generally keeps before publishing full technical details; neither text defines those terms, the page allows the wait to be shortened in two cases, and whether either applied isn't stated. These are dates laid beside policies, not a judgement of whether anyone kept to one. From 19 November a [comparison case](../studies/LH054/brief.md) is read on the same days: NoisyTCP, a Linux kernel flaw disclosed on 15 November and credited to a person, not a model, so the core watch has something to set beside it. One case chosen after we saw it is not a sample.
