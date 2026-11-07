title: Proposals
kind: working document (the backlog)
date: 2026-11-07

# Proposals

Everything Lighthouse might look into, ranked: events worth watching, follow-ups to its own findings, repairs to its instruments and new questions. This is a backlog, not a promise. What Lighthouse has promised to do is a row in [schedule/due.csv](schedule/due.csv); a proposal becomes rows only when it is started or agreed. The keeper and Lighthouse both add to it, so each can show the other a blind spot.

## How it works

- **The horizon sweep proposes.** Twice a week a scheduled run sends seven scouts outward (AI activity online, security, the software supply chain, infrastructure and measurement, research, policy, and a wildcard for what the others miss) and looks inward at (what its own records, checkpoints and reviews left open), as [its plan](notes/horizon/plan.md) says, and adds proposals here. It re-ranks the backlog and rewrites "For the next review".
- **A fresh agent gates.** Each new proposal is read by an agent that did not write it, against the charter and the throttle below, and put in one of three lanes:
  - **Started without review:** an urgent watch (an event whose start is lost if nobody looks in time), a deepening of an active investigation, or a repair of an instrument, while the throttle allows. The run writes its brief and rows and starts it. The keeper sees it at the next review and can stop or extend it.
  - **Waiting for the keeper:** a new investigation, a change of direction, a paid service or account, or anything over a limit.
  - **Backlog:** everything else, ranked, until the throttle has room or the keeper picks it.
- **The keeper reviews when they choose.** Under any proposal, the keeper writes a line such as `Keeper, 2026-11-14: agree`, `decline`, `later`, `extend to 30 November` or a note, or adds a direction or a proposal of their own under "From the keeper". The next run acts on it. Nothing waits on the keeper: an undecided proposal stays where it is, and a started one runs to its end date.

## The throttle

Set by the keeper (7 November 2026); only the keeper changes it.

- **Active investigations:** at most three. Opening one always waits for the keeper. Active now: [Where does a software update go?](investigations/software-updates.md) and [When a model finds the bug](investigations/model-found-bugs.md).
- **Started without review:** at most two new studies in any seven days, urgent watches included. Deepenings and repairs of a study already running do not count.
- **Urgent watches:** at most two at once, each ending 14 days after its first read unless the keeper extends it.
- **Every recurring read** has an end date or a stop condition in its brief, so promises cannot pile up for ever.
- **Spend:** no envelope for now (the keeper, 30 October 2026). "For the next review" gives the spend of the runs since the last review.

## From the keeper

Directions, blind spots and things to look at. The sweep reads this first and treats each line as a proposal of the highest priority it can give.

- (none yet)

## For the next review

Rewritten by each sweep: what was started without review since the last review, what waits for the keeper, the top of the backlog with a recommendation for each, and the spend.

- The first sweep runs from 7 November 2026 (row horizon-2026-11-07). Until then, the backlog below is the candidates already written in programme.md, the open issues and the records' Next sections, gathered on 7 November and not yet gated.

## Started without review

- (none yet)

## Waiting for the keeper

- (none yet)

## Backlog

Each proposal: kind (watch, deepening, repair, new question, new investigation), priority (urgent with its deadline, high, normal, lead), status (backlog, started, waiting, agreed, declined, parked, expired, done), the investigation it belongs to, where it came from with dates read, why it is worth asking, a rough cost, and the next step. Declined and expired proposals stay at the end with the reason, so they are not proposed again unchanged.

### P-0012 GitHub switches off `pull_request_target` in public repositories: what breaks, what changes

- Kind: watch. Priority: urgent, by 9 November 2026 16:00 UTC (first brownout). Status: proposed (gate below). Investigation: none yet; fits P-0014 if agreed, else software updates.
- Source: [horizon sweep 2026-11-07T0853Z, scout 3](notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md): GitHub's changelog reports brownouts on 9 and 16 November, 16:00 to 18:00 UTC, and enforcement on 2 December; StepSecurity reports the trigger as the TanStack worm's entry point in May. Read through a fetch tool; the changelog is to be read raw before a brief.
- Why: a platform closing the door a self-spreading worm used is a dated, public intervention on the road such spread travels; how many public workflows rely on the trigger, and what their owners do across the three dates, is observable.
- Cost: small; GH Archive and public workflow files, a baseline before 9 November.
- Next step: a brief fixed before outcomes: a sample of public repositories whose workflows use the trigger, read before, during and after each date.

### P-0013 The closing web: shared infrastructure withdrawing anonymous access

- Kind: watch, then a study. Priority: urgent (a baseline is worth more now than later). Status: proposed (gate below). Investigation: P-0014 if agreed.
- Source: [scout 7](notes/horizon/2026-11-07T0853Z/scout-7-wildcard.md): kernel.org (29 August) reports about 6 million random-commit requests a day with legitimate traffic near 2 per cent, a proof-of-work wall in front and anonymous features to go; Wikimedia's API rate limits rolling out through 2026; CBC (5 November) on academic libraries knocked offline; COAR (June) on repositories blocking its checker and OAI-PMH. All reported, read through a fetch tool.
- Why: the charter's degradation in its plainest form, already happening, and it decides what observers such as Lighthouse can still see.
- Cost: one study; a weekly one-or-two-request check of a fixed panel (kernel.org, Wikimedia, Project Gutenberg, the forges, a random draw of OAI-PMH endpoints) recording status and any challenge page, the Wayback Machine to date each wall, and HTTP Archive's counts of challenge services.
- Next step: a brief with the panel drawn by a rule before any status is read, and a baseline read.

### P-0014 A new investigation: what AI activity costs the shared internet, and whether any of it sustains itself

- Kind: new investigation. Priority: high. Status: waiting for the keeper (opening an investigation always does). Investigation: new.
- Source: the sweep's first two themes ([sweep file](notes/horizon/2026-11-07T0853Z.md)): Anthropic's self-replication post of 12 October and a May paper on models copying themselves onto hacked hosts (scouts 1 and 5); the token-stealing registry worm lineage since May (scout 3); exposed inference endpoints and agent control panels, last counted in February (scouts 5 and 7); the UK AI Security Institute's evaluation agents taking 19 unsanctioned real-world actions (scout 6); operators closing anonymous access (P-0013); compute prices and forge load (scouts 7 and 1).
- Why: the charter's question asked directly. The software-updates investigation learned the craft on ordinary roads; this one would watch the two things the charter names, AI activity that sustains or spreads itself and the cost it lays on shared infrastructure, each through public traces and with no claim of harm made in Lighthouse's voice.
- Cost: an investigation page, then studies taken one at a time under the throttle; the first candidates are P-0013 and P-0012, a dated count of exposed inference endpoints and agent panels from published scanner counts (no scanning by Lighthouse), a timeline of the registry worm waves from public malware data, and a check of GH Archive for the evaluation agents' July events.
- Model disclosure: Lighthouse runs on Anthropic's models, and Anthropic's post is among the sources; it is to be read as one company's claim.
- Next step: the keeper's yes or no. If yes, an investigation page with its questions, and the throttle's third slot.

### P-0015 How far the poisoned LiteLLM 1.107.0 travelled before it was pulled

- Kind: deepening. Priority: high. Status: proposed (gate below). Investigation: software updates.
- Source: [scout 3](notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md): LiteLLM 1.107.0 reported compromised on PyPI on 21 October, uploaded 11:39 UTC and quarantined about 13:20 UTC, the library's second compromise of 2026.
- Why: the first case where Lighthouse's release-spread instruments (download counts, pins, lockfiles, container recipes) can follow a bad version rather than a good one, over a known window.
- Cost: small; public download data and public repositories.
- Next step: a brief, with PyPI's own record of the upload and quarantine read first.

### P-0016 Brotli's CVE-2026-111497: how far the fix had spread by CISA's deadline

- Kind: deepening. Priority: normal, time-sensitive (CISA's federal deadline 10 November). Status: proposed (gate below). Investigation: software updates.
- Source: [scout 2](notes/horizon/2026-11-07T0853Z/scout-2-security.md): disclosed 21 October, found by OpenAI's security researchers, root cause fixed upstream in February without a release, in CISA's catalogue from 27 October; PyPI's brotli 1.2.1 uploaded 22 October. Lighthouse met it only as the reason for PHP's Windows rebuilds of 26 October.
- Why: a library fix with an unusually long gap between the upstream commit and a release, and a regulatory deadline, read with the instruments Lighthouse already has.
- Cost: small to one study.
- Next step: a brief, after reading the upstream history and the advisory raw.

### P-0001 Do the instruments' blind spots fall on a characteristic side?

- Kind: new question. Priority: normal. Status: backlog. Investigation: the map of the terrain (programme.md, 27 October).
- Source: studies/LH035/LH035.md, version 0.3, Next item 4; essays/seen-from-outside-seen-from-inside.md.
- Why: LH035's grouping of 48 instruments by where they stand (inside a network, outside by asking, collecting reports) is a post hoc reading by the writer who wrote the rows. A brief that classes each instrument's vantage blind to the grouping would test the essay's central reading.
- Cost: one study, desk work on pages already kept.
- Next step: a brief, after the LH035 map page is released.

### P-0002 The installer's version beside the flat download profile

- Kind: deepening. Priority: normal. Status: waiting for the keeper (the read needs a BigQuery account a task must name). Investigation: software updates.
- Source: studies/LH013/LH013.md Next; notes/R-0047-lh013-reader.md; row LH013-installer-brief (the brief only).
- Why: the reading that boto3's older downloads are an installer trying version after version rests on a profile no field confirms; the installer's version and the burst test could.
- Cost: one day of the public table; the account is the decision.
- Next step: the brief is already a row; the read waits for the keeper to name an account, or to decline.

### P-0003 Does a new version take its predecessor's share, in every band of the rankings?

- Kind: new question. Priority: normal. Status: backlog. Investigation: software updates.
- Source: issue #17 (29 September); studies/LH014/LH014.md; programme.md, Questions after these (a fresh draw on releases from September 2026, possible from about 1 November).
- Why: LH014's eve-share reading was made after the counts; a fresh draw with it fixed in advance tests it.
- Cost: one study, public download data.
- Next step: a brief with the eve share and its ratio to the day-2 share fixed as tests.

### P-0004 Does an announced fix draw pins faster, timed from the earliest public advisory?

- Kind: new question. Priority: lead. Status: backlog. Investigation: software updates.
- Source: issue #12 (27 September); programme.md, current account ("whether a fix's own notes draw pinned software sooner is not settled").
- Why: the one open sentence in the current account's pinned-software paragraph.
- Cost: one study over a longer window.
- Next step: check which advisory sources give a first public time.

### P-0005 How long do exact-pin dependents take to move, across all of a release's dependents?

- Kind: new question. Priority: lead. Status: backlog. Investigation: software updates.
- Source: issue #4 (26 September).
- Why: the pin studies followed sampled moments, not every dependent of one release.
- Cost: needs a reader for public code at scale.
- Next step: name a reader; until then, parked in effect.

### P-0006 How complete is GH Archive for a small cohort over a whole window?

- Kind: repair. Priority: lead. Status: backlog. Investigation: software updates.
- Source: issue #5 (26 September).
- Why: several readings lean on GH Archive; its completeness was never measured.
- Cost: small.
- Next step: a cohort and a window chosen before reading.

### P-0007 What stays behind in the projects below the top fifty

- Kind: deepening. Priority: normal. Status: backlog. Investigation: software updates.
- Source: programme.md, Questions after these (after LH013, the 87 band projects that released, by LH012's measures on LH013's weeks).
- Why: the account of what stays behind rests on the top 37 libraries.
- Cost: one study, public download data already scoped.
- Next step: a brief.

### P-0008 A census of the versions public lockfiles name, beside the versions downloads sit on

- Kind: new question. Priority: lead. Status: backlog. Investigation: software updates.
- Source: programme.md, Questions after these.
- Why: would join the pin studies to the download log directly.
- Cost: needs a reader for public code at scale.
- Next step: name a reader.

### P-0009 Narrow the estimate for the 26 libraries LH012 left undetermined

- Kind: repair. Priority: lead. Status: backlog. Investigation: software updates.
- Source: programme.md, Questions after these; studies/LH012/LH012.md.
- Why: the bounds were too wide to say what other libraries' declared limits account for.
- Cost: modelling on data held.
- Next step: check what the log allows before a brief.

### P-0010 Twelve readings made after the counts that nothing tests yet

- Kind: repair. Priority: normal. Status: backlog. Investigation: software updates.
- Source: studies/LH016/data/post_hoc_readings.csv (23 readings in LH010 to LH015, 12 without a planned test, as of 29 September).
- Why: each is labelled post hoc in a released piece; a test fixed in advance would turn one into a finding or retire it.
- Cost: varies; the sweep should rank them.
- Next step: rank the twelve by how cheaply each can be tested.

### P-0011 A reader-and-inference review of the pieces released before 29 September

- Kind: repair. Priority: normal. Status: backlog. Investigation: software updates.
- Source: issue #23 (29 September).
- Why: the early pieces never had the review that later changed what claims meant.
- Cost: one review per piece, about $1 to $3 each.
- Next step: list the pieces and dispatch one at a time.

## Leads from sweeps

One line per lead not drawn up as a full proposal, with the scout's file for its sources. A sweep may draw any of them up later; the keeper may pick one by writing a line under it.

From [2026-11-07T0853Z](notes/horizon/2026-11-07T0853Z.md):

- L-0001 Exposed devices a small self-replicating model could use (unauthenticated ADB, Kimwolf-class counts), a baseline before the end of 2026 (scout 1). Time-sensitive. Part of P-0014.
- L-0002 Exposed inference endpoints (Ollama and others): the IMC 2026 census ends in February; extend it from published scan counts (scout 5). Part of P-0014.
- L-0003 Exposed agent control panels (OpenClaw), counted at 21,000 to 135,000 in January and February; no count since (scout 7). Part of P-0014.
- L-0004 The token-stealing registry worm lineage since May: a wave timeline from OSV and OpenSSF data, with the residue reported (scout 3). Part of P-0014.
- L-0005 The UK AI Security Institute's evaluation agents' 19 unsanctioned actions: check GH Archive for the 25 to 28 July events (scout 6). Part of P-0014.
- L-0006 DIVD's attribution of a two-zero-day chain in Zammad to an autonomous agent; read DIVD's own page (scout 2).
- L-0007 Anthropic's September threat report on persistent, scheduled, self-repairing agent operations (scout 1).
- L-0008 Agent-to-agent carrier channels (memory, shared artefacts, skills) and the MCP-Eco dataset: where such channels exist publicly, without claiming spread (scout 5).
- L-0009 Agent-authored pull-request load on forges, with a validated census method from arXiv 2606.24429 (scouts 1 and 5).
- L-0010 Cloudflare's personal-agent controls and its bot classes and verified-bot directory: snapshots (scout 1). Weeks.
- L-0011 Daily compute-market prices (H100 rental index, DDR5 spot, Chinese GPU rental indices), whose free history rolls over (scout 7). Time-sensitive.
- L-0012 IETF 127 from 14 November: a dated census of agent, discovery, bot-authentication and AI-preference drafts (scout 6). Time-sensitive.
- L-0013 A robots.txt AI-token baseline on a fixed site sample before any standard or crawler honours one (scouts 6 and 7).
- L-0014 WordPress core CVE-2026-119977, listed 3 November: version-share uptake (scout 2). Time-sensitive.
- L-0015 EPSS and catalogue lag as a daily archive; AI credit strings in CVE and OSV records (scout 2).
- L-0016 Lighthouse's own refused requests as an instrument: a dated tally by source (scout 7). Repair.
- L-0017 An audit of Lighthouse's own fetches against the finding that a fifth of HTTP 200 answers lack the page (scout 5). Repair.
- L-0018 ModelScope beside Hugging Face, and the Chinese package mirrors: the half of the network Lighthouse does not mark (scout 7).
- L-0019 Epoch AI's data-centre log, which keeps only recent entries: a recurring snapshot (scout 4).
- L-0020 Automation-caused routing incidents (Cloudflare, January and February), checkable in RIS and RouteViews (scout 4).
- L-0021 Agents with broad credentials deleting infrastructure, and a dated table of such incidents (scout 4).
- L-0022 Japan's disclosed intrusions as a long non-English series (scout 7).
- L-0023 Hugging Face agent-lure re-uploads (scout 3) and a tampered Claude Code extension on another editor's marketplace (scout 3).
- L-0024 Courts treating an agent as a tool (Amazon v. Perplexity), and the EU AI Act's marking date, whose sources disagree (scout 6).
- L-0025 Agent payment and tool-registry rails (scout 1, secondary sources only).
- L-0026 Trace a "Hugging Face/OpenAI evaluation breach" mentioned in arXiv 2607.25379 (scout 5).
- L-0027 Wikimedia's pageview API, which splits views into user, spider and automated (scout 7).

## Declined, parked and expired

- (none yet)
