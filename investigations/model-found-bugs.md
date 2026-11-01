title: When a model finds the bug
kind: investigation
id: model-found-bugs
attention: active
question: When an AI model finds a serious flaw in software the internet runs on, and writes a working exploit for it, what happens next in public, who says what and when, how do the signals defenders rely on respond, and where does the fix land?
started: 2026-11-01
studies:
- studies/LH036/brief.md

## Why this, and why now

On 27 October 2026 Anthropic described five attack chains found with an unreleased internal model, among them an exploit the model wrote for CVE-2026-98432, a flaw in how the Linux kernel handles incoming IPv4 connections, giving remote root on servers with a Multipath TCP listener. The kernel had published the flaw and its fixes twelve days earlier and scored it 9.8 out of 10. Read on 1 November, EPSS, the public model that estimates how likely a flaw is to be exploited in the next 30 days, gave it 0.46 per cent for 31 October, below the median, and CISA's catalogue of exploited flaws did not list it. Debian's security updates carried fixes; Ubuntu's were pending, and its oldest supported releases had none. These are observations from one morning's reads, kept with the study's brief.

Lighthouse watches for what AI systems do on the internet and what their activity leaves behind. A model that finds a flaw and writes the exploit is such activity, and what follows, from the advisory to the fixed package, runs on roads the [software updates investigation](software-updates.md) already follows. This investigation keeps one flaw in view as its core and asks a few bounded questions around it. It does not try to follow every AI-related security story.

## Questions

1. **The core watch** ([LH036](../studies/LH036/brief.md), running from 1 November 2026). For CVE-2026-98432: how EPSS, CISA's catalogue, the CVE record's scoring and enrichment, NVD and the references move, read back to 15 October; and when each named distribution release's security channel carries a fix. Twice a week to mid January 2027.
2. **The disclosure timeline.** A dated reconstruction from primary sources: report, fix, CVE, distribution advisories, Anthropic's post, downstream notices; set beside the policies each party states (Anthropic's 90 days and 45 more, the kernel security team's, and the linux-distros list's). The report date is not public; the timeline records it as unknown unless a public source gives it. Brief to come.
3. **How the post's five chains were scored.** Chrome, Safari, Android, Windows and Linux: severity, EPSS and CISA's catalogue for each flaw the post names, a set chosen by the post, not by us. Five cases, not a sample. Brief to come.
4. **Later, an essay**: what responsible disclosure means when the finder is a model and a working exploit runs in under an hour. It waits for the evidence.

## Model disclosure

The exploit and the post are Anthropic's, and Lighthouse's agents, writers and reviewers alike, run on Anthropic models. The keeper chose to disclose this on every record and piece of the investigation rather than add a reviewer from another provider, for now (1 November 2026). Reviews are asked to look for wording easier on Anthropic, or on the exploit's significance, than the sources allow.

## What it will not do

It describes scores, listings, dates and fixes. It does not test any system for the flaw, judge whether anyone acted rightly in a record (judgement belongs to an essay, argued openly), or claim in Lighthouse's voice that the flaw is being exploited; a published report of exploitation is recorded as its source's claim.

## Where the evidence stands

Nothing measured yet. The core watch's brief was fixed on 1 November 2026 with the morning's reads disclosed in it; its first record follows the read of 16 November.
