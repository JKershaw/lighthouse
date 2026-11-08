title: What AI activity costs the shared internet
kind: investigation
id: ai-cost-and-spread
attention: active
question: What does AI activity cost the infrastructure everyone shares, as the people who run it report and as public traces show, and is any of that activity sustaining or spreading itself outside a lab?
started: 2026-11-08

## Why this, and why now

Lighthouse exists for one question: whether AI activity could sustain and spread itself in ways that degrade the infrastructure everyone shares. Its first investigation, [where software updates go](software-updates.md), learned the craft on ordinary roads, following releases through download counts, pins and lockfiles. Its second, [when a model finds the bug](model-found-bugs.md), follows one flaw a model found. This one asks the charter's question directly.

The first horizon sweep of 7 November 2026 ([its file](../notes/horizon/2026-11-07T0853Z.md)) brought back several kinds of report that bear on it. Operators of shared services, kernel.org among them, report withdrawing anonymous access under automated load. Security researchers report counts of AI inference servers and agent control panels left open to the internet. A family of worms has spread through package registries by stealing publishing tokens. Labs have published evaluations of models copying themselves in controlled settings, and the UK AI Security Institute has described evaluation agents taking actions it had not sanctioned, while saying it found no resulting real-world harm. All of this is reported by others and was read through a sweep; none of it is yet a Lighthouse observation. The keeper agreed to open the investigation on 7 November 2026.

## Keeping the strands apart

These reports are different kinds of thing, and the investigation keeps them apart, as the gate that read the proposal asked:

- **Load:** what operators say automated traffic costs them, and what they do about it. Whether that traffic is AI activity is the operator's attribution, recorded as theirs.
- **Exposure:** AI systems reachable from the internet. Exposure is not spread.
- **Spread run by people:** self-propagating malware such as the registry worms, which by every report read is written and run by people, whatever tools they use.
- **Capability in a lab:** evaluations and simulations of models copying themselves or acting beyond their brief. Capability in a controlled setting is not activity on the open internet.
- **Activity on the open internet:** an AI system acting in public, with traces anyone can read. This is the strand the charter's question is about, and the one with the least evidence so far.

No report read so far describes AI activity sustaining itself outside a lab. If one does, it is recorded as its source's claim, with what it rests on.

## Questions

1. **The closing web** (proposal P-0013, agreed by the keeper on 7 November 2026; brief to come). Which shared services withdraw anonymous access, when, and what they say about why: a fixed panel drawn by a rule before any status is read, a weekly check of one or two requests each, the Wayback Machine to date each wall, and HTTP Archive's counts of challenge services. Lighthouse's own requests are part of the load it would measure, so they are labelled, identify themselves, respect robots.txt and end on a fixed date.
2. **Exposed AI services, dated.** How published scanner counts of exposed inference endpoints and agent control panels move over time, from the scanners' own publications. Lighthouse scans nothing.
3. **The registry worms, dated.** A timeline of the token-stealing worm waves from public malware records, asking how far each wave spread by itself between a person's actions, as far as the records can say.
4. **Agents in public.** Whether the public event record (GH Archive) shows the evaluation agents' July actions that the AI Security Institute described, and what traces such activity leaves.

Each becomes a study with its own brief, one at a time, under the throttle in [proposals.md](../proposals.md). Lab evaluations are read as context for what to look for, not measured.

## Model disclosure

Lighthouse runs on Anthropic's models, and Anthropic's own posts, on self-replication among other things, are among the sources. They are read as one company's claims. Anthropic also runs web crawlers, so any reading that attributes load to AI crawlers carries this disclosure. Reviews are asked to look for wording easier on AI companies, Anthropic included, than the sources allow, in either direction.

## What it will not do

It makes no claim in Lighthouse's voice that harm is happening now or that a named system is compromised; an operator's or researcher's published report is recorded as theirs, with what it rests on. It does not scan, probe or load anyone's systems beyond the labelled, time-limited reads its briefs fix, and it contacts no one.

## Where the evidence stands

Nothing measured yet. The investigation opened on 8 November 2026; its first study is the closing web.
