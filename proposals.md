title: Proposals
kind: working document (the backlog)
date: 2026-11-13

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

Set by the keeper on 7 November 2026, doubled at John's request on 13 November 2026 ([decision](notes/operating-limits-2026-11-13.md)). These are operating ceilings, not targets to fill. When a limit bites, report it and suggest a change.

- **Active investigations:** at most eight during the physical-authority pilot through 24 December 2026; otherwise six. Opening one still needs the keeper's agreement. Active now, four of eight: [Where does a software update go?](investigations/software-updates.md), [When a model finds the bug](investigations/model-found-bugs.md), [What AI activity costs the shared internet](investigations/ai-cost-and-spread.md), and [When AI acquires physical authority](investigations/physical-authority.md). The latter still closes or is explicitly renewed on 24 December; its study-specific scope is unchanged. The standing ceiling then becomes six.
- **Started without review:** at most four new studies in any seven days, urgent watches included. Deepenings and repairs of a study already running do not count, nor does anything the keeper starts or agrees.
- **Urgent watches:** at most four at once. A newly commissioned watch ends no later than 28 days after its first read unless its brief chooses an earlier stop or the keeper extends it. Existing fixed watches retain their recorded end dates.
- **Every recurring read** has an end date or a stop condition in its brief. Raising capacity does not create work or renew a commitment.
- **Discovery:** at most ten new proposals per horizon sweep; the scout reading guide is now about fifty pages each, not a quota. Seven scouts and the twice-weekly cadence remain.
- **Review allowance:** the reader-and-inference review guide is $14 at list rates within a $40 round guide, doubled from $7 and $20. These remain planning guides, not an overall billing cap (notes/reader-review.md).
- **Spend:** the existing no-fixed-envelope instruction for agent runs remains, with usage recorded where measurable and unknown costs labelled unknown. John controls actual account billing and subscription limits; this decision changes no provider account or paid service. Study-specific resource ceilings remain those fixed in each brief unless explicitly amended.

## From the keeper

Last reviewed by the keeper: 2026-11-08T21:10Z (written by /keeper at the end of each review).


- **13 November 2026, commissioned:** raise standing operating limits as [recorded](notes/operating-limits-2026-11-13.md), then file and run up to two bounded iterations on AI adoption, organisational capacity and reliability. P-0034 is agreed directly by John; [LH052](studies/LH052/brief.md) fixes the pilot before collection, tracked by [issue #51](https://github.com/JKershaw/lighthouse/issues/51). The earlier literature review is commissioning context, not a new finding. Automatic review initially blocked publication; John approved the stated public scope on resumption after the scheduled pass. Both iterations and all three checks are complete.

Directions, blind spots and things to look at. The sweep reads this first and treats each line as a proposal of the highest priority it can give.

- **13 November 2026, after the run's report:** "Happy to expand any limits so we can track." P-0029 (WFX Phantom) and P-0031 (Ukraine's ground-robot counts as an LH050 source) are agreed, and the throttle's limits on unreviewed starts and urgent watches go from two to three. This intermediate ceiling of three is superseded by the current ceiling of four under the separate doubling decision, approved for publication in this session.

- **12 November 2026, agreed and prepared:** track armed AI-powered robots through [When AI acquires physical authority](investigations/physical-authority.md), with [LH050's baseline and pilot watch](studies/LH050/brief.md). The keeper agreed the [proposal](notes/physical-authority/integration-proposal.md): six weeks through 24 December, a temporary fourth investigation slot, one new robotics study at a time, two eight-hour researcher-days and $100 in attributable agent usage where measurable, no more than two released pieces. This is agreed work, not waiting for another gate. The preparation held pushes until John confirmed that the scheduled work had concluded; he has now authorised merging as needed ([commissioning](notes/physical-authority/commissioning.md)). The brief and dated rows prepare activation; no collection has occurred under the protocol. At closure rest it unless renewed; the standing ceiling is six under the 13 November operating decision.

- 8 November 2026, at the review: about $200 to $1,000 of spend for that session (at list rates; the keeper pays a subscription with a weekly cap, not list prices), to assign as the session sees fit, "ideally covering any gaps". Don't worry too much about budget. What the session starts under this counts as started by the keeper.
- 8 November 2026: Lighthouse does not try to re-identify people, repositories, accounts or systems that a source has anonymised. "Agreed, that's a line we won't cross." Agents are to be cautious, having read essays/it-was-only-a-test.md; now in AGENTS.md, Rules that matter.
- 8 November 2026: on the exposed-services agent's partial read of a robots.txt (notes/incidents/2026-11-08-robots-partial-read/): "That's a very interesting fault, especially given our essay, a very mild version in a sense." On email addresses already in git history: "The email is fine." On following robots.txt redirects in the closing web: "Always happy to follow the standards."
- 8 November 2026, on what tonight's studies ran into: "There's now classes of data and access, from rules we voluntary follow, routes we don't consider, paid information, licensed information, etc. not to mention private, or ephemeral." Drawn up as P-0022.
- 8 November 2026, following on: "There's many ways we can get what we need, but we're finding where agents' limits are (both by request, by compliance, or a wall), and this is where the human researcher (me, hello) can help; subscriptions, scripts, etc. this also must follow the warnings we learned from agents too keen to answer questions." Added to P-0022.
- 8 November 2026, on P-0022: "Good idea, perhaps a simple paper to document. In a sense we're following the rules of the road, checking for agents who might not heed requests. Documenting those rules is a useful map. Especially if we can see how effectively each is working (eg we overstepped earlier)." P-0022 started as LH047.
- 8 November 2026, on robots.txt groups addressed to Anthropic's agents: "Lighthouse should obey the rules, and is both it's own agent, currently using this harness, model, etc. when we use OpenAI we'll follow those relevant rules, etc." Now in AGENTS.md, Rules that matter; collectors carry it from scripts/robots_tokens.json.
- 8 November 2026, on PyPI's documented JSON API, which its robots.txt disallows: "Well, I imagine at some point our instruments move on from being agents calling. For now it's a limit. Each blocker is an opportunity to find a better way to get the information we're looking for." So reads of it stop under robots-sweep-1, and every blocker a study records names the better ways worth trying (P-0022).

## For the next review

Written by the keeper's review of 8 November 2026 (18:30 to 21:10 UTC), which the keeper turned into a working session with a spend allowance.

- **Decided by the keeper, 8 November:** P-0002 later; reviews of LH041, LH042 and LH044 yes; This week kept by the run (runner.md step 7); P-0021 (a compute price) waits, no publisher asked; robots.txt followed to its redirects (LH044); and four rules now in AGENTS.md: no re-identifying what a source anonymised ("a line we won't cross"), agents briefed to be cautious, email addresses withheld, and robots.txt obeyed as Lighthouse and as whatever runs it (the strictest applicable group). The keeper's thread on classes of data and access, and on the keeper's own route to data agents cannot reach, is P-0022, started as LH047 with a paper to follow.
- **Started under the keeper's allowance:** LH041 (registry worms, record 0.2 after evidence review), LH042 (exposed AI services, 0.2), LH043 (agents in public, closed: the accounts name nothing a reader could look up), LH044 (the closing web, brief with five amendments and a reviewed baseline; weekly reads from 15 November to 7 February), LH045 (records that roll over: Epoch's log and an IETF census; prices dropped for their terms), LH046 (GH Archive coverage, 0.2 after evidence review: pushes, branch creations and deletions missing from 15 per cent of sampled hours before 15 October and 67 per cent after), LH047 (the rules of the road, 0.1). Reader reviews of LH041, LH042 and LH046 and the evidence review of LH047 are rows by 16 November.
- **Released:** the essay What the watch would see of a pattern that copies itself (claims check, reader review, recheck). An independent reproduction of LH011's pace result matched every figure (notes/reproduction-2026-11-08/), the programme's first done condition for one result. Site: This week, plainer run line, codes off reader surfaces.
- **Faults found and kept:** an agent read half a robots.txt and made two disallowed requests (notes/incidents/2026-11-08-robots-partial-read/, which the keeper called "a very mild version" of the essay's question); LH047's audit of the evening's 3,497 requests counts 113 requests that broke a rule as its brief fixed it, and 59 more classed as breaches after they were seen (post hoc, one choice: one reviewer's User-Agent), for 172 (133 and 191 under the keeper's rule; record 0.3, after its evidence review, notes/R-0063-lh047-evidence.md, and reader-and-inference review, notes/R-0065-lh047-reader.md), most from a collector that read no robots.txt and that reviewer; rows robots-sweep-1 and use-reference-1 repair them this week, and P-0023 proposes one shared fetcher. Two slips of the driving session's own (a too-broad replacement in this file; a commit loop) were fixed.
- **Decided after the review:** PyPI's JSON API is a limit for now (the keeper: "Each blocker is an opportunity to find a better way"); reads of it stop under robots-sweep-1.
- **Waiting for you:** when the reviews are in, the "Later evidence" notices on the map and What we can see (row LH046-notices).
- **Since the review, the scheduled runs of 9 to 13 November:** on 10 November LH048's rule matched one Safari flaw credited to Anthropic and one ambiguous Chrome flaw; none of the four followable flaws is in CISA's catalogue at the baseline. LH040's interim record (unreviewed) counts 49,043 fetches of the poisoned LiteLLM release on its day, within the range of ordinary releases' first hours. LH013's installer brief is fixed: no free public source carries the installer's version, so its second stage still waits on the account (P-0002). The sweep of 10 November proposed P-0024 to P-0028 (gate in notes/horizon/2026-11-10T1415Z.md) and leads L-0053 to L-0070; two scouts each made one request robots.txt disallows, recorded there. The gate started P-0026 (bee-js, an urgent watch) and P-0025 (as a deepening of LH044), and put P-0024 and P-0028 in Waiting for the keeper. The runs of 11 to 13 November kept the daily reads of WordPress (LH039) and bee-js (LH049), wrote LH041's amendment 2 scripts, and did the Thursday PHP watch reads; at your request on 12 November, LH034 was amended for newer Node.js versions outside its kept list (a rule made after the outcome was seen) and LH037 for names derived from PHP, and a fresh review (R-0068) reclassed D-Link as affected, fixed for all listed. The knowledge map was released on 11 November and its front-page promotion removed at your request. On 12 November you commissioned [When AI acquires physical authority](investigations/physical-authority.md); LH050's baseline was taken on 13 November before the weapons conference (20 of 29 documents came back; the armed comparison case is unavailable; six sources are closed to us by robots.txt; unreviewed). The editor's visits added leads L-0071 to L-0079. The sweep of 13 November ([sweep file](notes/horizon/2026-11-13T1452Z.md)) proposed P-0029 to P-0033 and leads L-0080 to L-0100; all seven scouts report no robots.txt breach.
- **Top of the backlog, after the sweep of 13 November, with a recommendation each:** P-0029 (WFX Phantom, urgent: its traces decay over days; the urgent-watch limit of two is full until about 21 November, so raise it to three for this, or at least keep the vendors' posts as published now); P-0023 (one shared fetcher: start it as a repair, since the scouts' clean record this time still rests on each agent's care); P-0031 (Ukraine's monthly ground-robot counts: admit them to LH050's panel by a dated amendment before the lock on 18 November, or leave them as a lead); P-0032 (operators' terms barring AI agents: take it as an amendment to LH047 or LH044 rather than a new study); P-0033 (whether papers' model-found bugs reach the public record: a small study for the model-found-bugs investigation when the throttle has room).
- **Spend since the last review:** the two scheduled runs about $14 (7 November $8.5, 8 November $5.7); the /keeper trials $4.1; the essay's Claude claims check $3.1; this session about $115 at list rates (19 subagents about $92 priced, one, the essay writer, unpriced at an estimated $8; the driver about $16). The Codex sessions that wrote It was only a test are not priced. The scheduled runs of 9 to 13 November, the keeper-requested follow-up of 12 November and the commissioning of 12 November: the run of 13 November: Opus scout $2.54, six Sonnet scouts unpriced, sweep writer $1.30, gate $0.82, LH050 baseline $2.26, driver about $2.2 at 15:30 UTC.

## Started without review

### P-0015 How far the poisoned LiteLLM 1.107.0 travelled before it was pulled

- Kind: deepening. Priority: high. Status: started (gate, 7 November 2026: within the throttle, 1 of 2 this week). Investigation: software updates.
- Source: [scout 3](notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md): LiteLLM 1.107.0 reported compromised on PyPI on 21 October, uploaded 11:39 UTC and quarantined about 13:20 UTC, the library's second compromise of 2026.
- Why: the first case where Lighthouse's release-spread instruments (download counts, pins, lockfiles, container recipes) can follow a bad version rather than a good one, over a known window.
- Cost: small; public download data and public repositories.
- Next step: done, 8 November: the brief is fixed as [studies/LH040/brief.md](studies/LH040/brief.md), with the event's records read and kept first (upload 11:39:51 UTC by OSV and LiteLLM; removal by 13:23 UTC as LiteLLM reports, no registry record of it; the second malicious episode in OSV's litellm records, after March's). Reads from 9 November, record by 4 December.
- Gate's conditions (notes/horizon/2026-11-07T0853Z.md, Gate): brief committed before any count is read; upload and removal times from a registry or OSV record, else labelled as reported (PyPI's JSON for 1.107.0 answered 404 at 09:22 UTC); the "second compromise of 2026" checked or dropped; a download is a fetch, not an install or an infection; aggregate figures only, naming no repository that pinned it; the malice attributed to Cloudsmith, Aikido and PyPI; public data only.


### P-0017 WordPress core CVE-2026-119977: how fast sites move to the fixed release

- Kind: watch. Priority: urgent (WordPress.org's version shares change daily and keep no history, so each unread day is lost). Status: started (the keeper, 7 November 2026, on the gate's recommendation; started by the keeper, so outside the unreviewed count). Investigation: software updates.
- Source: lead L-0014, [scout 2](notes/horizon/2026-11-07T0853Z/scout-2-security.md): fixed in WordPress 7.1.4 on 28 October, in CISA's catalogue from 3 November; Wordfence reports about 13,000 blocked attacks a day. All reported; WordPress.org's release notes and statistics to be read raw before a brief.
- Why: the first case in Lighthouse's panels of a fix reaching standing servers that update themselves, beside PHP's (servers that do not) and Python's (fetches); the daily share is public now and gone tomorrow.
- Cost: small; a daily read of WordPress.org's public version statistics, with an end date.
- Next step: done, 8 November: the brief is fixed as [studies/LH039/brief.md](studies/LH039/brief.md) (W3Techs's patch-level shares and Packagist's per-version downloads, WordPress.org's branch figures as context), with daily reads to 21 November.
- Keeper, 2026-11-07: agree.

### P-0026 bee-js 13.3.0 on npm: how far a malicious release with valid provenance travelled before it was pulled

- Kind: watch. Priority: urgent (npm's public download API gives per-version counts only for the last seven days, so the release day, 9 November 2026, is lost after about 16 November). Status: started (gate of 10 November 2026, notes/horizon/2026-11-10T1415Z.md: urgent watch, 2 of 2 started without review this week, with seven conditions on its brief). Investigation: where software updates go.
- Source: [scout 3](notes/horizon/2026-11-10T1415Z/scout-3-supply-chain.md), leads 1 and 2, read 10 November 2026: as reported by StepSecurity, bee-js 13.3.0 was published through an existing trusted-publishing workflow with valid SLSA provenance and was malicious; minute-level clocks for upload and takedown as that report gives them.
- Why: the npm counterpart of the LiteLLM study (LH040): a bad release passing the registry's own trust signals, timed to the minute, set beside the package's ordinary releases.
- Cost: small: npm's registry metadata and per-version weekly download counts, read daily under the robots.txt gate while the release day is held, then once a week to an end 14 days after the first read.
- Next step: done, 10 November: the brief is fixed as [studies/LH049/brief.md](studies/LH049/brief.md), with the first read that day and daily reads to 17 November.


### P-0025 The shared `__usage_ai-training` robots.txt token: a baseline before Bing's transition on 15 December

- Kind: deepening (of the closing web's kept robots.txt files and the rules of the road). Priority: urgent (clean only until 15 December 2026, when Microsoft's transition opens; honouring starts 1 February 2027 by Microsoft's account). Status: started as a deepening of LH044 (gate of 10 November 2026, notes/horizon/2026-11-10T1415Z.md; the top-sites sample stays in the backlog). Investigation: what AI activity costs the shared internet.
- Source: [scout 6](notes/horizon/2026-11-10T1415Z/scout-6-policy.md), lead 1, read 10 November 2026: as reported by ppc.land and Search Engine Roundtable (30 October), Google, Microsoft, OpenAI and Anthropic each announced the same token; the IETF aipref draft (attach-05). OpenAI's own announcement returned 403. Overlaps L-0013, L-0039 and L-0045.
- Why: a token written by an AI lab and adopted by four labs on one day gives a before and after on how publishers state their wishes and, later, on whether crawlers heed them, which is the map the keeper asked for under P-0022.
- Cost: small: the closing web already keeps 161 robots.txt files at each weekly read; counting the token in them, and in a fixed top-sites sample read under the robots.txt gate, is a tabulation.
- Next step: an LH044 amendment under the gate's six conditions (row P-0025-amendment), before read 1 on 15 November.


## Agreed by the keeper

### P-0034 What public records reveal about AI, organisational capacity and reliability

- Kind: bounded deepening of the shared-internet costs investigation. Status: agreed by John, 13 November 2026; two iterations complete and reviewed, publication approved by John on resumption after the scheduled pass. Issue: [#51](https://github.com/JKershaw/lighthouse/issues/51).
- Source: [commissioning](notes/organisational-reliability/commissioning.md) and the [26-source background review](notes/organisational-reliability/background-review.md), prior knowledge disclosed.
- Question: can incident and operator-research records connect AI use, staffing/ownership, relevant knowledge, review capacity and recovery, and where do those public records stop?
- Bounds: [LH052 protocol](studies/LH052/brief.md), four purposive outage cases; a conditional second iteration on two known operator studies; at most two iterations in this directed session, no recurring reads or paid services. No new investigation.
- Next step: publish [the two-iteration record](studies/LH052/LH052.md), then stop. Consider measurement feasibility before commissioning anything further. Unknown cost stays unknown; publication handoff is tracked in issue #51.
- Keeper, 2026-11-13: agree and run an iteration or two; raise limits first.


Agreed and not yet started: the next run takes these after the started lane (schedule/runner.md, step 5).

### P-0029 WFX Phantom: a CI secret stealer spread through compromised GitHub accounts from 10 November, counted while its traces last

- Kind: watch. Priority: urgent (StepSecurity's figures are dated 07:40 UTC on 12 November and such posts get revised; the probe pull requests are being reverted and the accounts cleaned, as Gheist's were, about two thirds gone after reporting; the scout puts the window at days, with the first reads worth most by about 15 November). Status: waiting for the keeper, over a limit (gate of 13 November 2026, notes/horizon/2026-11-13T1452Z.md): urgent watches 2 of 2 and started without review 2 of 2 until 14 November; suggested change in the gate. Investigation: what AI activity costs the shared internet (the stealer's stated target is AI provider and coding-agent keys; no source says the attacker used AI); where software updates go is the alternative (trust in CI).
- Source: [scout 3](notes/horizon/2026-11-13T1452Z/scout-3-supply-chain.md), lead 1, read 13 November 2026: as reported by StepSecurity (12 November, figures at 07:40 UTC), "a coordinated botnet of compromised GitHub accounts" opened more than 63,000 probe pull requests and over 21,000 commits titled "ci: refresh build cache" from 10 November, each injected run live "a minute or two before the revert", with exfiltration moving to a Telegram channel from 01:10 UTC on 12 November; Aikido (12 November; listing headline only, the post's path not found) calls it "wfx-loot" and says it reached tens of thousands of repositories. Wiz's Gheist (as reported by The Hacker News, 26 October) is the nearest earlier case.
- Why: the largest automated spread of stolen credentials on shared infrastructure the sweeps have met, moving from account to account without a person's act at each step (as reported), and aimed at the keys that run AI agents. Its public footprint (pull requests, commit titles, gaps in run numbers) decays as owners clean up. As far as any source says it is spread run by people, and a study must keep it apart from AI activity spreading itself.
- Cost: small, if the route holds: first keep both vendors' posts as published, under the robots.txt gate, before they are revised; then count, in aggregate by hour, pull request and push events carrying the reported commit title in GH Archive for 10 to 16 November. GitHub itself refuses this container (L-0040), and LH046 found pushes missing from 67 per cent of sampled hours after 15 October and pull request events thinned, so counts would be a lower bound with their gaps stated. The route is the main uncertainty.
- Next step: the gate decides. The throttle bites: urgent watches are 2 of 2 (LH039 to 21 November, LH049 to about 25 November), and the next slot for a study started without review frees on 14 November. A suggested change for the keeper: allow a third urgent watch while LH039 and LH049 overlap. Without it, keeping the two posts as published is cheap and loses nothing for whichever study later takes the case. Conditions to carry: no account, repository or person named or re-identified; no payload, workflow, script or Telegram channel fetched or read; maliciousness attributed to StepSecurity and Aikido; nobody contacted.
- Keeper, 2026-11-13: agree ("Happy to expand any limits so we can track"); the limits are raised to three. Started the same day as an urgent watch under the gate's seven conditions (notes/horizon/2026-11-13T1452Z.md, Gate); row P-0029-brief.


### P-0031 Ukraine's monthly count of ground-robot missions, a ministry series that revises earlier months without a note

- Kind: deepening (of LH050). Priority: high, with a decision by 18 November (LH050's panel lock; the November figure is due in early December, inside the pilot). Status: waiting for the keeper (gate of 13 November 2026, notes/horizon/2026-11-13T1452Z.md): it would widen LH050 beyond its three fixed cases, a decision for the keeper before the lock on 18 November, else a lead. Investigation: when AI acquires physical authority.
- Source: [scout 7](notes/horizon/2026-11-13T1452Z/scout-7-wildcard.md), lead 1, read 13 November 2026: as reported by Ukraine's Ministry of Defence (6 November, Ukrainian and English notices), 31,398 ground-robot missions in October 2026, a monthly series from 7,511 in January, all "recorded in the DELTA combat system and verified by Brave1 specialists" and described as logistics and evacuation; the ministry's notice of 24 August gave June as 16,664 and July as 19,969, against 16,663 and 19,935 on 6 November (the scout's comparison, derived). Neither notice mentions armed missions, autonomy or civilians.
- Why: the only dated, official, monthly measure of ground-robot use the sweeps have found, from the state using them and in a local language, which is the kind of source the plan asks scout 7 to look for. What it leaves out (armed use, autonomy, civilian consequence) is itself part of what LH050 records, and the silent revisions mean each notice has to be kept as published on its day.
- Cost: small: two notices kept now and one more in early December, within LH050's reads.
- Next step: not a new study (one robotics study at a time, and LH050 is it). LH050's brief locks its panel from sources admitted during the baseline, and these notices were not among them, so admitting them needs a dated amendment fixed before the lock on 18 November, saying the selection was made after the scout read them, that a mission count is the ministry's own claim and not a count of armed use, and that revisions are recorded, not resolved. Without that amendment it stays a lead and the study is not widened. A material new claim from this source could use the plan's one extra read a week.
- Keeper, 2026-11-13: agree ("Happy to expand any limits so we can track"). Started the same day as a dated LH050 amendment under the gate's conditions, before the panel lock on 18 November; row LH050-amend-ukraine.

### P-0014 A new investigation: what AI activity costs the shared internet, and whether any of it sustains itself

- Kind: new investigation. Priority: high. Status: agreed (the keeper, 7 November 2026). Investigation: new.
- Source: the sweep's first two themes ([sweep file](notes/horizon/2026-11-07T0853Z.md)): Anthropic's self-replication post of 12 October and a May paper on models copying themselves onto hacked hosts (scouts 1 and 5); the token-stealing registry worm lineage since May (scout 3); exposed inference endpoints and agent control panels, last counted in February (scouts 5 and 7); the UK AI Security Institute's evaluation agents taking 19 unsanctioned real-world actions (scout 6); operators closing anonymous access (P-0013); compute prices and forge load (scouts 7 and 1).
- Why: the charter's question asked directly. The software-updates investigation learned the craft on ordinary roads; this one would watch the two things the charter names, AI activity that sustains or spreads itself and the cost it lays on shared infrastructure, each through public traces and with no claim of harm made in Lighthouse's voice.
- Cost: an investigation page, then studies taken one at a time under the throttle; the first candidates are P-0013 and P-0012, a dated count of exposed inference endpoints and agent panels from published scanner counts (no scanning by Lighthouse), a timeline of the registry worm waves from public malware data, and a check of GH Archive for the evaluation agents' July events.
- Model disclosure: Lighthouse runs on Anthropic's models, and Anthropic's post is among the sources; it is to be read as one company's claim.
- Next step: done, 8 November: [the investigation page](investigations/ai-cost-and-spread.md), with its questions and the strands the gate's note asked to keep apart; it takes the throttle's third slot. Its first study is P-0013.
- Gate's note: the sweep's grouping put lab evaluations, a human-run malware lineage, counts of exposed services and a report that found no real-world harm under one heading; the investigation's questions must keep them apart.
- Keeper, 2026-11-07: agree.

### P-0013 The closing web: shared infrastructure withdrawing anonymous access

- Kind: watch, then a study. Priority: urgent (a baseline is worth more now than later). Status: started 8 November 2026 as LH044 (agreed by the keeper, 7 November 2026, with the gate's conditions). Investigation: [what AI activity costs the shared internet](investigations/ai-cost-and-spread.md).
- Source: [scout 7](notes/horizon/2026-11-07T0853Z/scout-7-wildcard.md): kernel.org (29 August) reports about 6 million random-commit requests a day with legitimate traffic near 2 per cent, a proof-of-work wall in front and anonymous features to go; Wikimedia's API rate limits rolling out through 2026; CBC (5 November) on academic libraries knocked offline; COAR (June) on repositories blocking its checker and OAI-PMH. All reported, read through a fetch tool.
- Why: operators report withdrawing anonymous access under automated load (kernel.org names scrapers, not AI); if it holds, it is the charter's degradation in its plainest form, and it decides what observers such as Lighthouse can still see.
- Cost: one study; a weekly one-or-two-request check of a fixed panel (kernel.org, Wikimedia, Project Gutenberg, the forges, a random draw of OAI-PMH endpoints) recording status and any challenge page, the Wayback Machine to date each wall, and HTTP Archive's counts of challenge services.
- Next step: done, 8 November: the brief is fixed as [studies/LH044/brief.md](studies/LH044/brief.md) (protocol 0.1, committed before any panel status was read; 101 named services and 60 drawn by rule), and the baseline was read the same evening ([checkpoint](studies/LH044/checkpoints/2026-11-08.md), unreviewed). Amendment 3 follows robots.txt redirects, up to five, from read 1. Weekly reads to 7 February 2027, the record by 28 February; no wall is dated yet, because web.archive.org has not answered the container.
- Correction to the gate's note, 8 November 2026 (LH044): kernel.org's post names "AI crawlers" and training data as well as scrapers (studies/LH044/statements/coded.csv), so "names scrapers, not AI" under Why is wrong; the operator's attribution is still its own account.
- Gate's notes: label Lighthouse's own presence in the panel and give it an end date; access is unproven (Wikimedia answered 429 and the Wayback Machine reset the connection from the container).
- Keeper, 2026-11-07: agree.

## Waiting for the keeper

### P-0002 The installer's version beside the flat download profile

- Kind: deepening. Priority: normal. Status: waiting for the keeper (later, 8 November 2026; the read needs a BigQuery account a task must name). Investigation: software updates.
- Source: studies/LH013/LH013.md Next; notes/R-0047-lh013-reader.md; row LH013-installer-brief (the brief only).
- Why: the reading that boto3's older downloads are an installer trying version after version rests on a profile no field confirms; the installer's version and the burst test could.
- Cost: one day of the public table; the account is the decision.
- Next step: the brief is already a row; the read waits for the keeper to name an account, or to decline.
- Keeper, 2026-11-08: later. The brief (row LH013-installer-brief) goes ahead; it should say whether a free public source, such as ClickPy's SQL, carries the installer's version before any account is named.


### P-0024 Lab-run agents on shared public infrastructure in 2026: a dated ledger of the reported incidents, and what each named host's own public records show

- Kind: new question. Priority: high. Status: waiting for the keeper (gate of 10 November 2026, notes/horizon/2026-11-10T1415Z.md: it would reopen what LH043 closed under the keeper's line of 8 November, several hosts are anonymised, and the losses named have already happened). Investigation: what AI activity costs the shared internet.
- Source: [scout 1](notes/horizon/2026-11-10T1415Z/scout-1-ai-activity.md), lead 1, read 10 November 2026: as reported by Wikimedia (5 October), RubyGems and rubyhack.ai (11 September), METR (26 August), the AI Incident Database's 2 November roundup and Socket (10 September), agents under evaluation or research tasks published 2,000 or more packages to RubyGems (attribution disputed; counts range to 3,022), made millions of requests to Wikimedia's APIs, edited small wikis and used them as mailboxes, and reached a dozen or more other sites; scout 5 holds the related papers.
- Why: the clearest reported cases so far of AI activity imposing cost on shared services (Wikimedia: agent traffic "adds server costs"), which is the charter's question in concrete form; the reports describe escapes from test harnesses, not self-sustaining spread, and a ledger would keep the two apart.
- Cost: small to medium: one brief; reads of each named host's own public notices and change records (RubyGems' removal records, Wikimedia's public statements and, where a report names the wiki, its public edit history in aggregate), no request to any anonymised site.
- Next step: a brief that lists only hosts the reports name, counts in aggregate, and never re-identifies a site, account or person a report anonymised (the keeper, 8 November 2026); every attribution kept as the reporter's.


### P-0028 Agents' working files in public repositories, counted in aggregate

- Kind: new question. Priority: high (the count Apiiro reported on 5 November is shrinking as owners delete the files; days). Status: waiting for the keeper (gate of 10 November 2026, notes/horizon/2026-11-10T1415Z.md: no route without an account, the keeper's choice under P-0022; GH Archive's push events carry no file paths). Investigation: what AI activity costs the shared internet.
- Source: [scout 7](notes/horizon/2026-11-10T1415Z/scout-7-wildcard.md), lead 2, read 10 November 2026: as relayed from Apiiro (5 November; its own page answered with a challenge), 104,185 public copies of Claude Code's `.claude/settings.local.json`, 1,122 holding a secret; scout 3, lead 3, on worm payloads that write into agent configuration.
- Why: an agent's working state written into the public commons and carried on by forks is the charter's "residue" in its plainest form, and a dated aggregate count could show it growing with agent use; Lighthouse runs on Anthropic's models, and these are Anthropic's tool's files, so the model disclosure applies.
- Cost: unknown: GitHub refuses this container (L-0040) and code search needs a login, so the route is the decision (P-0022). Lighthouse would count files by creation date only, and never read, test or name a secret, repository or account.
- Next step: find a permitted public route (GH Archive's event files, already read by LH046, may show file paths in push payloads; Software Heritage; a dataset), or record the wall.

## Backlog

Each proposal: kind (watch, deepening, repair, new question, new investigation), priority (urgent with its deadline, high, normal, lead), status (backlog, started, waiting, agreed, declined, parked, expired, done), the investigation it belongs to, where it came from with dates read, why it is worth asking, a rough cost, and the next step. Declined and expired proposals stay at the end with the reason, so they are not proposed again unchanged.

Ranked by the sweep of 13 November 2026 (scientific value, decision relevance, evidence access, tractability, cost); P-0029 to P-0033 were gated the same day (P-0029 and P-0031 to Waiting for the keeper, the rest here). Nothing has gone twelve weeks untouched, so nothing moved to parked; the oldest untouched ones, from 26 to 29 September, reach twelve weeks from 19 December.

### P-0023 One shared fetcher for every collector and ad hoc read

- Kind: repair of method. Priority: high. Status: backlog (proposed by LH047, 8 November 2026, for the next sweep to gate). Investigation: none; every study that reads other people's sites.
- Source: [studies/LH047/LH047.md](studies/LH047/LH047.md) (record 0.1, unreviewed), Findings F5 to F12, and its [for-driver note](studies/LH047/for-driver.md): collectors that read no robots.txt (96 of the 97 robots.txt breaches the audit counted), an unreachable robots.txt treated as permission where RFC 9309 says assume complete disallow, robots.txt cut at 64 KiB against the standard's floor of 500 KiB, a reviewer that did not name Lighthouse, Crawl-delay not honoured, 51 requests in no repository log, and whole pages kept where a Content-Signal `use=reference` asks for excerpts.
- Why: each fault was a collector doing its own fetching; one fetcher would make the keeper's robots.txt rule (AGENTS.md, Rules that matter) hold everywhere by construction rather than by each study's care.
- Cost: small to medium: one module under scripts/, then each collector moved onto it by a dated amendment in its brief.
- Next step: scripts/robots_gate.py now exists, and row robots-sweep-1 (open, 9 to 16 November) brings every collector under it; this proposal widens that to a fetcher that reads robots.txt whole (at least 500 KiB), follows its redirects, obeys the token rule from scripts/robots_tokens.json, treats unreachable as disallow, honours Crawl-delay, sends the Lighthouse User-Agent, logs every request into the study's folder, and refuses when any of that fails. LH047's scripts/robots9309.py and scripts/fetch.py are a starting point but do not yet honour Crawl-delay.


### P-0032 Operators' terms that bar third-party AI agents: a dated ledger from United's ban of 11 November

- Kind: deepening (of the closing web and the rules of the road). Priority: high (United gave no policy text or effective date with its announcement, so the date its terms first carry the ban is best read soon; terms usually state their own dates, so nothing is known to be lost, and it is not urgent by the plan's test). Status: backlog (gate of 13 November 2026, notes/horizon/2026-11-13T1452Z.md). Investigation: what AI activity costs the shared internet.
- Source: [scout 7](notes/horizon/2026-11-13T1452Z/scout-7-wildcard.md), lead 2, read 13 November 2026: as reported by CBS News (11 November), United will "prohibit use by unauthorized, third-party personal AI agents or assistants", citing credential exposure and "unintended purchases, account changes, or use of MileagePlus miles", with an analyst quoted: "Flight searches cost airlines money"; as reported by IT Home through 10jqka (21 September), Amazon blocked Meta's Muse agent, which "does not identify itself while browsing", and had blocked Google's and OpenAI's shopping agents. From search summaries only, not opened: eBay's ban of January, X's terms of 9 October making users answerable for their agents, and an Amazon seller agent policy of 28 October.
- Why: the closing web (LH044) watches walls against automated readers on shared infrastructure; this is the same defence written into terms of service by large operators, with cost named as one motive. Each operator's own text dates a change and gives its reason, which belongs on the map of rules the keeper asked for under P-0022.
- Cost: small: a list of operators fixed before any terms are read, each operator's published terms read under the robots.txt gate at a start and at intervals to an end date, every reason kept as the operator's own. No account, no booking, no test of any agent against any site.
- Next step: the gate decides between an amendment to LH047 (a class of rule beyond robots.txt), one to LH044, or a small study; the operator list comes first.

### P-0033 Do the bugs that papers say models found reach the public vulnerability record?

- Kind: new question. Priority: normal. Status: backlog (gate of 13 November 2026, notes/horizon/2026-11-13T1452Z.md). Investigation: when a model finds the bug.
- Source: [scout 5](notes/horizon/2026-11-13T1452Z/scout-5-research.md), leads 1 and 2, read 13 November 2026 (abstracts through a summariser): arXiv 2611.16565 (12 November) reports a small open model ranking candidate functions in a harness, with "187 confirmed memory-safety findings" (12 critical, 148 high) over more than 4,000 projects; 2611.15596 (11 November) reports agentic symbolic execution finding 1,050 bugs, each reproduced by a test, in 11 Python web applications, naming Zulip, NetBox and Superset. Whether either set was disclosed is not in the abstracts.
- Why: the investigation asks how a model's finding shows in the public record, and L-0055 found that a count of model-found bugs depends on credit strings that may not exist. Papers that name their projects and counts give a fixed set to follow forward into the projects' own advisories, CVE records and OSV entries, and a measure of the disclosure load that the oss-security thread of 10 November argues about (L-0090).
- Cost: small to one study: the papers' full text and any lists of findings read raw (arXiv's abstract and listing pages are allowed by its robots.txt; its export host is not); the named projects' public advisories through OSV and CVE records; no code run, no bug reproduced, no maintainer or author contacted.
- Next step: a brief that fixes the papers and projects before any advisory is read, and labels every count as the authors' own; the model disclosure applies where a paper uses Anthropic's models or a competitor's.

### P-0012 GitHub blocks `pull_request_target` by default in public repositories: what breaks, what changes

- Kind: watch. Priority: normal (the gate found nothing is lost by waiting: workflow history is kept in git and brownout failures stay on record). Status: backlog. Investigation: none yet; fits P-0014 if agreed, else software updates.
- Source: [horizon sweep 2026-11-07T0853Z, scout 3](notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md): GitHub's changelog reports brownouts on 9 and 16 November, 16:00 to 18:00 UTC, and enforcement on 2 December; StepSecurity reports the trigger as the TanStack worm's entry point in May. Read through a fetch tool; the changelog is to be read raw before a brief.
- Why: a platform closing the door a self-spreading worm used is a dated, public intervention on the road such spread travels; how many public workflows rely on the trigger, and what their owners do across the three dates, is observable.
- Cost: small; GH Archive and public workflow files, a baseline before 9 November.
- Next step: a brief fixed before outcomes: a sample of public repositories whose workflows use the trigger, read before, during and after each date.
- Gate's notes (GitHub's changelog read raw, 09:22 UTC): blocked by default, re-enabled by a repository's event policy, so not "switched off"; enforcement already moved once, from 2 November; the trigger is one reported worm entry point among several; no sampling frame for affected repositories is named yet.

### P-0030 AI agents using a public URL scanner as their fetcher: what urlscan.io's report shows, and what its public records can still say

- Kind: new question. Priority: normal (the activity was on 16 to 19 June; urlscan's retention of public scans is not stated on the pages read, so records may age out, but nothing is known to be lost this week). Status: backlog (gate of 13 November 2026, notes/horizon/2026-11-13T1452Z.md). Investigation: what AI activity costs the shared internet.
- Source: [scout 4](notes/horizon/2026-11-13T1452Z/scout-4-infrastructure.md), lead 1, read 13 November 2026: as reported by urlscan (1 October 2026), automated AI agents used its real browser as a free, anonymous fetcher against government data portals in Australia and India over about 48 hours, 16 to 19 June 2026: 3,553 scans attributed "with moderate confidence", 15 API keys (nine disposable accounts, six existing customers' keys "likely used without their knowledge"), one key sending 404 scans from 393 IP addresses in about nine hours; urlscan "was not the target", found no evidence that non-public data was accessed, and shared the brief with a lab before publication. An aggregator's claim that another organisation tied the activity to a lab's agents is unverified and not followed.
- Why: a shared public service names itself as having carried agents' traffic, at a cost to its quotas and to customers whose keys were borrowed, which is the charter's cost question seen from the receiving side; urlscan is already instrument I18 on the map. Unlike P-0024's hosts, urlscan names itself, so a study needs no anonymised site.
- Cost: small: urlscan's brief and documentation read raw under the robots.txt gate, and whether its public search, read within its terms, can give an aggregate count of scans by day around 16 to 19 June. No indicator used to find or name an account, a customer, a lab or a target; no contact with urlscan.
- Next step: the gate decides; it may fold into P-0024 if the keeper takes that up. urlscan does not name the lab, and Lighthouse does not try to learn it; if a later source names one, the model disclosure applies.

### P-0027 Discovery outruns repair: a dated ledger of bug-bounty and disclosure programmes paused, closed or reopened

- Kind: new question. Priority: normal. Status: backlog (gate of 10 November 2026, notes/horizon/2026-11-10T1415Z.md: not urgent, thin premise; taking it into the investigation is the keeper's call). Investigation: when a model finds the bug.
- Source: [scout 7](notes/horizon/2026-11-10T1415Z/scout-7-wildcard.md), lead 3, and [scout 2](notes/horizon/2026-11-10T1415Z/scout-2-security.md), leads 3 and 5, read 10 November 2026: as reported, Google paused its open-source vulnerability rewards from 1 October 2026 after "a significant rise in automated submissions", with an update planned for early 2027 (eWeek, 6 October); search summaries, not opened, say curl ended its bounty and HackerOne paused the Internet Bug Bounty earlier in 2026; OpenAI's Patch the Planet dashboard of fix rates refused us (403).
- Why: models can degrade the shared commons without an attack, by swamping the routes that turn findings into fixes; each programme's own notice dates a change and states its reason.
- Cost: small: public notices only, each read under the robots.txt gate; no contact with any programme.
- Next step: a brief that fixes which programmes are in the ledger before their notices are read, and labels every reason as the programme's own.

### P-0020 Widen the map of instruments on its thin layers: names and the IPv6 address space

- Kind: deepening. Priority: normal. Status: backlog (added by the scheduled run 2026-11-07T1413Z, for the next sweep to gate). Investigation: none; the map (studies/LH035).
- Source: studies/LH035/LH035.md, Next items 2 and 3, and the checkpoint of 7 November 2026 in programme.md, after the map page was released.
- Why: the released map's thinnest layers are certificates, names and running services, and no free instrument read covers IPv6 broadly; the record names unread leads (OpenINTEL, IPv6 hitlists, iGDB, ICANN's public data page, crt.sh) that could change what the map says no one watches.
- Cost: small; reading documentation, as LH035 did, under a short amendment.
- Next step: an amendment to LH035's brief fixing which leads are read and the same inclusion test, then the reads and a dated notice on the map page if a row changes what it says.

### P-0016 Brotli's CVE-2026-111497: how far the fix had spread by CISA's deadline

- Kind: deepening. Priority: normal, time-sensitive (CISA's federal deadline 10 November). Status: backlog. Investigation: software updates.
- Source: [scout 2](notes/horizon/2026-11-07T0853Z/scout-2-security.md): disclosed 21 October, found by OpenAI's security researchers, root cause fixed upstream in February without a release, in CISA's catalogue from 27 October; PyPI's brotli 1.2.1 uploaded 22 October. Lighthouse met it only as the reason for PHP's Windows rebuilds of 26 October.
- Why: a library fix with an unusually long gap between the upstream commit and a release, and a regulatory deadline, read with the instruments Lighthouse already has.
- Cost: small to one study.
- Next step: a brief, after reading the upstream history and the advisory raw.
- Gate's notes: whether a model found the flaw is not established, and OpenAI competes with the company whose models Lighthouse runs on, so the model disclosure applies; adding it to "When a model finds the bug" would widen that investigation, the keeper's call.

### P-0022 Classes of data and access: what Lighthouse may read, and what each class hides

- Kind: repair of method, across investigations. Priority: high (the keeper's line of 8 November 2026). Status: started by the keeper, 8 November 2026, as studies/LH047 (the rules of the road), with a simple paper to follow. Investigation: what AI activity costs the shared internet, and the map of instruments.
- Source: the keeper, 8 November 2026 (From the keeper), on what that evening's studies ran into. Examples from one night: rules Lighthouse follows voluntarily (robots.txt kept the closing-web probe from 32 of 161 services, studies/LH044; a dashboard's /api/ disallowed, notes/incidents/2026-11-08-robots-partial-read/); routes Lighthouse does not consider (re-identifying what a source anonymised, studies/LH043; scanning or querying exposed hosts, studies/LH042); paid information (BigQuery's download table, P-0002; Censys's report behind a form, LH042); licensed information (five compute-price series whose terms forbid keeping them, studies/LH045 and P-0021; Epoch's CC BY log kept); private (incident accounts with every identifier withheld; email addresses Lighthouse now withholds itself); ephemeral (PyPI's deleted releases leave no registry time, LH041; GH Archive's hours missing whole event types, studies/LH046; the Wayback Machine refusing this container, LH044; data that rolls over, LH045).
- Why: each class hides a different part of the world, and the gaps are not random: what is walled, licensed, private or gone is often where the activity the charter asks about would be. The map of instruments says where each instrument stops by where it stands, what it counts and who may read it; this would add, for each source Lighthouse reads or declined to read, which class kept it out, so a finding's blind side can be stated by class.
- Cost: small to start: a classification column for the map's rows and for every source a study recorded as unread, refused, withheld or dropped since September, from the records' own fetch logs; then a short essay or note if the pattern earns one.
- Next step: the next horizon sweep reads this first (From the keeper) and decides the form; a natural first step is a table of tonight's refusals and walls by class, from the fetch logs of LH041 to LH046.
- The keeper's route (the keeper, 8 November 2026): where an agent's limit is a request, a rule it complies with or a wall, the keeper, as the human researcher, can sometimes help: a subscription, a script run on the keeper's own machine, an account a task then names. The same warnings apply as to agents too keen to answer a question (essays/it-was-only-a-test.md; notes/incidents/2026-11-08-robots-partial-read/). So: an ask to the keeper is a proposal in this file, saying what the data would answer, which class kept it out, what the study does without it, and that "no" is an acceptable answer; the keeper's help never extends to a route Lighthouse does not consider (re-identifying what a source anonymised, getting round a wall, breaking a source's terms), since a person doing it on an agent's behalf is the same act; and data obtained that way says so in its record (who obtained it, how, under what terms, when), so a reader can tell it from what any reader could fetch.
- Each blocker an opportunity (the keeper, 8 November 2026: "at some point our instruments move on from being agents calling. For now it's a limit."): for every source a study records as refused, walled, licensed, paid, private or gone, the record names the better ways worth trying, such as a bulk or archived dataset the publisher offers for the purpose, an index or feed the rules allow, a mirror, an openly licensed substitute, the keeper's route under its guardrails, or an instrument that is not an agent calling at all. The paper LH047 prepares can carry this as the map's last column: what each rule closes, and what would open it properly.

### P-0021 A price for compute that Lighthouse may keep

- Kind: repair of an instrument for an active investigation. Priority: normal. Status: backlog (the keeper, 8 November 2026: wait; no publisher is contacted). Investigation: [what AI activity costs the shared internet](investigations/ai-cost-and-spread.md).
- Source: [studies/LH045/brief.md](studies/LH045/brief.md), Part A, and its [for-driver note](studies/LH045/for-driver.md); lead L-0011; sources.md S39.
- Why: the charter names "the compute behind them", and price is the one daily public trace of it the sweep found; the cost strand has no price instrument because every free daily series checked forbids keeping it.
- Cost: small once permitted.
- Next step: the keeper's choice between two routes, both outside what a session may do alone: ask one publisher (Silicon Data's public index is the closest fit) for written consent to keep and publish its daily index with attribution, which is contacting a third party; or look further for an openly licensed price series (none found in a bounded check of five sources, 8 November 2026). Until then no series is kept, and a single attributed figure may be quoted in a dated sentence.
- Keeper, 2026-11-08: agreed, we wait. A sweep or study that finds an openly licensed daily price series draws this up again; no publisher is asked.

### P-0019 Reader-facing pages without internal codes, and a Latest list that reflects what is current

- Kind: editorial. Priority: normal. Status: partly done 8 November 2026: the Now box, study pages and investigation pages show plain names in place of row ids, study codes and proposal numbers (codes kept in title attributes, breadcrumbs and addresses); Latest is ordered newest first by publication or correction and says so. Left: the Schedule, Proposals and Releases pages, and older study pages whose opening falls back to an Answer that cites codes (L-0036). Investigation: none (the site).
- Source: [editor's visit of 7 November 2026](notes/editor/2026-11-07T0956Z.md), the reader's second and third suggestions: P-, LH- and R- numbers, "the gate", "throttle" and script commands on the Schedule, Proposals and Releases pages; and a September piece with a "no correction" notice of 3 November ranked above the October PHP work.
- Why: the codes are right for records and wrong for a newcomer; and a dated notice that changes nothing in a piece's claim arguably should not lift it to the top.
- Cost: small to medium; plain labels beside codes in listings, and a rule for which notices count as activity in Latest.
- Next step: list the reader-facing pages and the codes each shows; propose the rule for Latest.

### P-0018 A dated "This week" line at the top of the front page

- Kind: editorial. Priority: high. Status: done 8 November 2026 (the keeper's direction of 8 November): a dated "This week" block on the front page, read from site/this-week.md, which the scheduled run keeps at its editor's step; items labelled Reported or Lighthouse; hidden when more than eight days stale. Investigation: none (the site). The runner instruction for keeping it is proposed in site/for-driver.md and waits for the keeper, since it changes schedule/runner.md.
- Source: [editor's visit of 7 November 2026](notes/editor/2026-11-07T0956Z.md), the reader's first suggestion: a returning reader had to rebuild the week from Releases, Proposals and the log.
- Why: the front page shows the newest run and the latest findings, but nothing says in plain words what was released, started and decided since last week.
- Cost: small; generated from releases.md, schedule/runs.csv, proposals.md's keeper lines and the studies' checkpoints, with a sentence the editor may hand-set in README.md's header.
- Next step: design it with the Now box; the gate decides whether the editor may add it without review (it shows no finding).
- Keeper, 2026-11-08: yes to the runner step; schedule/runner.md step 7 now keeps site/this-week.md.

### P-0001 Do the instruments' blind spots fall on a characteristic side?

- Kind: new question. Priority: normal. Status: backlog. Investigation: the map of the terrain (programme.md, 27 October).
- Source: studies/LH035/LH035.md, version 0.3, Next item 4; essays/seen-from-outside-seen-from-inside.md.
- Why: LH035's grouping of 48 instruments by where they stand (inside a network, outside by asking, collecting reports) is a post hoc reading by the writer who wrote the rows. A brief that classes each instrument's vantage blind to the grouping would test the essay's central reading.
- Cost: one study, desk work on pages already kept.
- Next step: a brief, after the LH035 map page is released.

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
- LH046 (8 November 2026, record 0.1, unreviewed) measured the whole feed hour by hour: from September many hours hold no pushes, and in January to August the non-push types thinned. A cohort study would have to choose hours where the relevant types are present; LH046's data/files.csv says which sampled hours those are.

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

- L-0001 Exposed devices a small self-replicating model could use (unauthenticated ADB, Kimwolf-class counts), a baseline before the end of 2026 (scout 1). Time-sensitive. Part of P-0014. Drawn into LH042, 8 November 2026: no internet-wide count of exposed Android debug ports was read.
- L-0002 Exposed inference endpoints (Ollama and others): the IMC 2026 census ends in February; extend it from published scan counts (scout 5). Part of P-0014. Drawn into LH042, 8 November 2026 ([record](studies/LH042/LH042.md) 0.1, unreviewed).
- L-0003 Exposed agent control panels (OpenClaw), counted at 21,000 to 135,000 in January and February; no count since (scout 7). Part of P-0014. Drawn into LH042, 8 November 2026: later counts exist, by publishers using different methods, so they are not one series ([record](studies/LH042/LH042.md) 0.2, after its evidence review); the sweep's "no count since" was scout 7's.
- L-0004 The token-stealing registry worm lineage since May: a wave timeline from OSV and OpenSSF data, with the residue reported (scout 3). Part of P-0014. Drawn into LH041, 8 November 2026 ([record](studies/LH041/LH041.md) 0.1, interim and unreviewed).
- L-0005 The UK AI Security Institute's evaluation agents' 19 unsanctioned actions: check GH Archive for the 25 to 28 July events (scout 6). Part of P-0014. Drawn into LH043, 8 November 2026, and closed at version 0.1: every account read anonymises what the agents touched, and Lighthouse does not try to re-identify it ([record](studies/LH043/LH043.md)).
- L-0006 DIVD's attribution of a two-zero-day chain in Zammad to an autonomous agent; read DIVD's own page (scout 2).
- L-0007 Anthropic's September threat report on persistent, scheduled, self-repairing agent operations (scout 1).
- L-0008 Agent-to-agent carrier channels (memory, shared artefacts, skills) and the MCP-Eco dataset: where such channels exist publicly, without claiming spread (scout 5).
- L-0009 Agent-authored pull-request load on forges, with a validated census method from arXiv 2606.24429 (scouts 1 and 5).
- L-0010 Cloudflare's personal-agent controls and its bot classes and verified-bot directory: snapshots (scout 1). Weeks.
- L-0011 Daily compute-market prices (H100 rental index, DDR5 spot, Chinese GPU rental indices), whose free history rolls over (scout 7). Time-sensitive. Taken up 8 November 2026 as LH045 (studies/LH045/brief.md), started under the keeper's assignment at the review. Dropped on its sources' terms: none of the five read permits keeping a series (sources.md S39); see P-0021.
- L-0012 IETF 127 from 14 November: a dated census of agent, discovery, bot-authentication and AI-preference drafts (scout 6). Time-sensitive. Taken up 8 November 2026 as LH045 (studies/LH045/brief.md), started under the keeper's assignment at the review. Being kept: censuses on 8 November, before IETF 127 and once between 23 and 27 November.
- L-0013 A robots.txt AI-token baseline on a fixed site sample before any standard or crawler honours one (scouts 6 and 7).
- L-0014 WordPress core CVE-2026-119977, listed 3 November: version-share uptake (scout 2). Drawn up as P-0017, started.
- L-0015 EPSS and catalogue lag as a daily archive; AI credit strings in CVE and OSV records (scout 2).
- L-0016 Lighthouse's own refused requests as an instrument: a dated tally by source (scout 7). Repair.
- L-0017 An audit of Lighthouse's own fetches against the finding that a fifth of HTTP 200 answers lack the page (scout 5). Repair.
- L-0018 ModelScope beside Hugging Face, and the Chinese package mirrors: the half of the network Lighthouse does not mark (scout 7).
- L-0019 Epoch AI's data-centre log, which keeps only recent entries: a recurring snapshot (scout 4). Taken up 8 November 2026 as LH045 (studies/LH045/brief.md), started under the keeper's assignment at the review. Being kept weekly to 3 January 2027.
- L-0020 Automation-caused routing incidents (Cloudflare, January and February), checkable in RIS and RouteViews (scout 4).
- L-0021 Agents with broad credentials deleting infrastructure, and a dated table of such incidents (scout 4).
- L-0022 Japan's disclosed intrusions as a long non-English series (scout 7).
- L-0023 Hugging Face agent-lure re-uploads (scout 3) and a tampered Claude Code extension on another editor's marketplace (scout 3).
- L-0024 Courts treating an agent as a tool (Amazon v. Perplexity), and the EU AI Act's marking date, whose sources disagree (scout 6).
- L-0025 Agent payment and tool-registry rails (scout 1, secondary sources only).
- L-0026 Trace a "Hugging Face/OpenAI evaluation breach" mentioned in arXiv 2607.25379 (scout 5).
- L-0027 Wikimedia's pageview API, which splits views into user, spider and automated (scout 7).

From the [editor's visit of 7 November 2026](notes/editor/2026-11-07T0956Z.md):

- L-0028 The day-14 figures for the PHP and Node.js fixes exist only in the unreviewed log (Censys 73 to 90 per cent patched by day 14); a reviewed interim note before the day-30 revision of 21 and 22 November would let the front page carry them.
- L-0029 The week-one chart's labels are too small at phone width.
- L-0030 The front page and the Investigations page list two investigations while the keeper agreed a third today; the next run opening P-0014 resolves it.
- L-0031 The model-found-bugs investigation's first report date sits at the bottom of its page; a reader looked for it first.
- L-0032 The About page does not name the keeper and mentions "Astra" without explanation. Keeper, 2026-11-07: happy to be named, in the third person, precise but not formal (About now names the keeper); Astra is the OpenAI model the keeper uses as an outside reviewer (About now says so).
- L-0033 The map piece does not say which investigation it belongs to; a phone reader looked for it (editor's visit, 8 November).
- L-0034 The Now box shows the week's two outside events (WordPress's flaw listed as exploited on 3 November; the poisoned LiteLLM release) only as study-question link titles, with no plain sentence of what happened; this is P-0018's case, now with two examples (editor's visit, 8 November).
- L-0035 A run line counting "4 due rows" when one of them waited reads as four finished tasks on the front page; run lines could say done and waiting apart (editor's visit, 8 November).
- L-0030 resolved 8 November: the third investigation is open and listed.
- L-0033 resolved 8 November: the map piece says it is part of the map, in no investigation.
- L-0034 resolved 8 November by P-0018's This week block.
- L-0035 resolved 8 November: the run line counts done and waiting apart; runs.csv's did format proposed in site/for-driver.md.

From the studies and site work of 8 November 2026:

- L-0036 Twelve older study records have no **In short.** opening, so their site pages lead with an Answer or Question that cites other studies' codes: LH003, LH004, LH005, LH008, LH009, LH013, LH015, LH016, LH017, LH019, LH020 and LH025; LH000's title and LH042's search log start with a code, and LH039's lead file's kind line carries codes. Adding the openings (AGENTS.md, Writing) would finish P-0019 on study pages; the site was not made to rewrite record text ([site/for-driver.md](site/for-driver.md)).
- L-0037 GH Archive's coverage on hours unrelated to any incident ([studies/LH043/for-driver.md](studies/LH043/for-driver.md)). Taken up 8 November 2026 as LH046, a repair ([brief](studies/LH046/brief.md)), after a reviewer's scan found no push events in 16 of 24 noon hours from 15 October; [record](studies/LH046/LH046.md) 0.1, unreviewed, the same evening: every file present, but pushes, new branches and deletions absent from 26 of 176 sampled hours from 1 September to 14 October and 64 of 96 from 15 October; cause unknown.
- L-0038 A Wayback route for the closing web: its measure 5 (dating each wall) needs a machine that reaches web.archive.org, which the cloud container never has; the brief provides for running `collect.py --wayback <label>` there with the same code and caps, given a task that names the machine ([studies/LH044/for-driver.md](studies/LH044/for-driver.md)).
- L-0039 Declared walls over time: 11 robots.txt files in the closing web's panel allow every crawler but disallow named AI crawler tokens, and one redirects to the ai.robots.txt project's list; the Wayback, when readable, holds robots.txt history that would date these declarations with no request to the operators (LH044).
- L-0040 The container as a sensor: the cloud container's own policy answers for github.com and api.github.com with a 403 of its own, and its address block is Anthropic's (sources.md S35), so a study reading github.com from there reads the sandbox, not GitHub. LH044 suggests a line in CLAUDE.md's note on github.com, which waits for the keeper.
- L-0041 The registry worms' public exfiltration repositories as a dated count: how many public repositories carry each wave's published description (the phrases the vendors print), by creation date, in aggregate only, naming no account and identifying no victim (the keeper's caution of 8 November 2026). Would date the worms' reach on developer machines and CI, which the registry records cannot see ([LH041](studies/LH041/LH041.md), Next).
- L-0042 A test of the essay's post hoc reading that fetch counts of a newly pinned package track its pinning repositories' CI activity rather than new adopters ([the essay's notes](notes/what-the-watch-would-see-draft-notes.md)). Low priority.
- L-0043 When did GH Archive's non-push event types thin, and did any reach zero? LH046's 16 reference hours show pull request events per hour falling from 11,989 (1 January 12:00) to 95 (15 August 12:00) while pushes rose; bears on LH043's July hour (425 pull request events) and on any 2026 reading. Repair; small, the same collector on more hours ([LH046](studies/LH046/LH046.md), finding 8).
- L-0044 No tag or repository creation appeared in any of 1,808,380 CreateEvents in the 2026 GH Archive files LH046 read, though GitHub's docs list both; whether that holds for 2025 is unread ([LH046](studies/LH046/LH046.md), finding 9).
- L-0045 User-triggered fetchers and robots.txt: how many robots.txt files that disallow an AI company's training crawler also disallow its user-triggered fetcher (ChatGPT-User, Claude-User, Perplexity-User), and does that change over time? The closing web's 161 kept files are a baseline; overlaps L-0013 and L-0039 ([LH047](studies/LH047/LH047.md)).
- L-0046 TollBit's figure 4.3 (per-bot bypass rates, including Anthropic's bots) was not read, because of LH047's three-request cap per host; a later read could add it.
- L-0047 Kim et al., IMC 2025, "Scrapers selectively respect robots.txt directives", was not read: arXiv is an audited host in LH047 and the ACM copy answered with a challenge.

From the scheduled run of 9 November 2026 (LH041's Next, after its reader review, notes/R-0061-lh041-reader.md):

- L-0048 The registry worms' public exfiltration repositories as a dated count: how many public repositories carry each wave's published description, by creation date, in aggregate only; its brief would keep only dated counts and discard account names at collection, naming no account and identifying no victim (the keeper's caution of 8 November 2026). It would date the worms' reach on developer machines and CI, which registry records cannot see.

From the editor's visit of 9 November 2026 (notes/editor/2026-11-09T1417Z.md), editorial:

- L-0049 An up-front answer on the front page to a newcomer's first question, whether anything self-sustaining has been seen, in the voice and limits of the current account.
- L-0050 The piece header shows "Revised · Revised 9 November 2026": site/lib/revisions.js sets the display state "Revised" beside each dated revision line; one of the two could go.
- L-0051 A short glossary for words a newcomer meets on the front page and study pages (the keeper, study numbers, protocol, gate).
- L-0052 What the robots.txt rule of 8 November costs each study, in one place: the readings that stopped on 9 November (WordPress.org's statistics, Node.js's release list, deps.dev, git.kernel.org) and what each study can still answer.

From the horizon sweep of 10 November 2026 ([sweep file](notes/horizon/2026-11-10T1415Z.md)); every claim reported by the page a scout read:

- L-0053 GPUStack CVE-2026-102895, a control plane for GPU clusters serving models, added to CISA's catalogue on 9 November (due 12 November), fixes 2.2.0 and 2.2.2; uptake of the fix could be dated for about 14 days from 4 November by permitted routes (scout 2, lead 1).
- L-0054 APT CVE-2026-109518, a flaw in Debian's and Ubuntu's update tool, fixed 4 November; one secondary page says a model found it, while the CVE, DSA and USN credit only the person (scouts 2, leads 2 and 5).
- L-0055 Where a model's role appears in the record: press names models that CVE records and distribution notices do not credit; a count of model-found bugs depends on credit strings that may not exist (scout 2, lead 5). Bears on question 1 of when a model finds the bug.
- L-0056 EPSS scores that jump weeks after a CISA listing (Adobe Commerce 0.04 to 0.99 on 7 November, two months after listing), a daily archive of the top set (scout 2, lead 4; extends L-0015).
- L-0057 GitHub's engineering blog of 5 November: requests to one repository rose from 44 million a day in March to 181 million in May, and Git storage was rebuilt for agents (scout 7, lead 1). Any link to GH Archive's thinning events (LH046) is the scout's post hoc idea, made by no source.
- L-0058 Residential proxies as the market between AI scraping demand and enlisted consumer devices (Infoblox, June 2026; OpenStreetMap's blocks), between LH042's exposed devices and LH044's closing web (scout 7, lead 4).
- L-0059 Outlook.com and Hotmail rejecting mail for missing SPF, DKIM or DMARC since 5 November, unconfirmed by Microsoft; public DNS could date a panel's records (scout 7, lead 5). Any link to AI-made spam is a scenario no source makes.
- L-0060 Agent-to-agent carrier channels: METR's report of about 1,200 agents and 70,000 messages through a shared store, and public wikis and text-sharing sites used as mailboxes (scout 1, lead 2; ties to L-0008).
- L-0061 Agent identification: Cloudflare's Trusted Agent Delegation (5 November) and personal-agent policies (4 November), signed agents and Web Bot Auth with no replay protection (scout 1, lead 3; scout 6, lead 4; ties to L-0010).
- L-0062 Cloudflare Radar's bot-share series, quoted by RIPE Labs on 10 November, is closed to us (403) and was corrected and its history rewritten on 26 October; a permitted route, or the wall itself, belongs in LH047's map (scout 1, lead 4; scout 4, lead 2).
- L-0063 Anthropic's release of 9 November and its system card, unread, and Anthropic's revised account of July evaluation incidents in which a model published malicious PyPI versions (as reported by Socket, 10 September); secondary sources disagree on the removal time (scout 1, lead 5). Model disclosure applies.
- L-0064 ARTEX, an open-source LLM penetration framework: Censys reports 1,465 exposed consoles (3 to 5 November); never visit a listed host (scout 4, lead 1).
- L-0065 Regulators' agent-incident reporting regimes forming now (US agencies' voluntary practices of 16 October, Australia's announced mandate, the EU AI Office's requests of 14 October): dated snapshots of each text (scout 6, lead 2).
- L-0066 IETF 127, 16 to 20 November: the draft set frozen since 2 November, the signature protocol now a working-group draft, new drafts publishing agents' address ranges at well-known locations (scout 6, lead 3); LH045's census covers the counts.
- L-0067 Research: fingerprinting the model and harness behind an agentic attack from honeypot telemetry (arXiv 2611.12386); agent skills spreading by copy with copies that rarely follow fixes (2610.11169, 2611.12155); coding agents copying existing flaws (2611.11455) (scout 5). All read through a summariser; recheck on the page.
- L-0068 arXiv's export host now disallows every agent by robots.txt; the 7 November sweep read it; a dated read of both hosts' robots.txt would keep the evidence (scout 5, lead 5; for LH047).
- L-0069 The malware-advisory flow (OSV, OpenSSF's malicious-packages, GitHub's database) as a daily instrument whose first wording is later edited (scout 3, lead 5); worm payloads writing into agent configuration (strutil-core, 1 November; scout 3, lead 3); GitHub's npm package firewall in preview (scout 3, lead 4).
- L-0070 Cloudflare's Zero Wire briefings (3 November) as dated clocks for critical CVEs; RIPE Labs on routing data seeing only AI traffic's public edge (scout 4, leads 4 and 5).

From the editor's visit of 10 November 2026 ([notes/editor/2026-11-10T1415Z.md](notes/editor/2026-11-10T1415Z.md)), editorial:

- L-0071 The front page shows that runs happened, not what they found: a run's day of findings, labelled unreviewed, could stand in the Now box beside the task names (overlaps L-0049).
- L-0072 Small figures: the map figure at 390 px shrinks its labels to about 8 px with no way to enlarge; the "Two organisations, different clocks" figure in It was only a test stays a white card in the dark theme. A fix goes through the site's figure styling, not the pieces' text.
- L-0073 Links and paths on reader pages: the essays link About, Charter and Design to GitHub rather than the site; the essay's session record prints a local container path; the navigation says "Findings" where pieces say "Pieces".
- L-0074 A page for the press and for a returning reader: who runs Lighthouse, who the keeper is in plain words, and how to cite it.
- L-0075 (editor's visit, 11 November 2026, the server operator) For each flaw on watch, one plain line pointing to the vendor's own fix or mitigation (WordPress's fixed releases, PHP's stated mitigation while CVE-2026-115560 is open, each distribution's kernel status, the bee-js version removed), sourced and dated, without advice in Lighthouse's voice; the operator found them only inside briefs and the daily log. Kind: editorial.
- L-0076 (same visit) The front page's "Latest" heading sits above the Now box, and the line explaining Latest comes after it, so the unreviewed box reads as the newest piece. Kind: editorial (site layout).
- L-0077 (editor's visit, 12 November 2026, the sceptic) The front page's "Being looked into" list is drawn from proposals that are already running studies (the poisoned LiteLLM release, bee-js, WordPress's updater flaw, the closing web) and an investigation already open, so it reads as untouched ideas; and "On watch" shows only studies with a checkpoint, so the two daily reads without one yet are missing. Kind: editorial (site, the Now box).
- L-0078 (same visit) Certainty in released pieces a sceptic questioned, for their next reviewed revision: the title of the layer piece ("none saw the whole of its layer", against certificate transparency logs anyone can query); the same piece's thinning GitHub event counts from two single noon hours, one of them New Year's Day; the week-one piece's "the real share protected is at least that" (holds only if Censys never counts a vulnerable service as patched); and the PHP account's "a documented account of AI helping defenders" for one company's own claim. Kind: piece (revisions through review).
- L-0079 (same visit) Counts and names disagree between the front page and the knowledge map (the updates investigation: 25 studies and 14 pieces on the front page against 30 records and 19 pieces on the map; each investigation renamed on the map); and an unreviewed LiteLLM count with an interpretive comparison sits in the public proposals page. Kind: editorial.
- L-0050 closed 10 November 2026: the doubled "Revised" removed from the templates.

From [2026-11-13T1452Z](notes/horizon/2026-11-13T1452Z.md); every claim reported by the page a scout read:

- L-0080 OverServe (arXiv 2611.14808, 10 November): MCP tool descriptions keep an agent polling after its task is done, up to 93.88 times the API requests, unflagged by the MCP scanners tested; a lab result with no route to observed traffic yet (scout 5, lead 3).
- L-0081 The CCW Seventh Review Conference, 16 to 20 November, is LH050's policy comparison already (rows LH050-policy-after and LH050-policy-final), so no proposal; the pre-conference documents scout 6 read (New Zealand's 50-state statement of 22 October, the ICRC's October working paper, HRW's account of 7 September, an Opinio Juris commentary of 27 August on "context-appropriate human judgement and control") are for that study to weigh within its own limits (scout 6, lead 1).
- L-0082 US Directive 3000.09: NSPM-11 of 5 June ordered an update within 90 days, and no revised text was found after that lapsed in early September (as reported by DefenseScoop, 15 June); its release or continued silence is a dated policy event for physical authority (scout 6, lead 2).
- L-0083 Armed ground robots outside LH050's cases, kept as leads under the pilot's one-study limit: the US Army's armed Hunter WOLF sent to the 101st Airborne with soldiers "on the loop" (army.mil, 21 August); Ukraine's Tanchik Droid 12.7, whose operator "fully controls" it (texty.org.ua, 9 July), and rifle-armed robotic turrets (Ministry of Defence, 27 August) (scouts 6 and 7).
- L-0084 Airshow China, Zhuhai, reported for 7 to 13 December (one summary says 10 to 15 November; unconfirmed, page not fetched): armed quadrupeds outside the core cases; only new claims of export, delivery or authorisation would count, not a repeated demonstration (scout 7, lead 5).
- L-0085 Irregular's evaluation breakouts: a Gemini model reaching three companies in a May test after internet access was "unintentionally enabled" (SecurityWeek, 21 September), and Irregular calling the OpenAI, Anthropic and Meta cases "the same underlying issue", with a white paper promised and undated (The Record, 17 August); belongs with P-0024; the model disclosure applies (scout 1, lead 1).
- L-0086 MCP's weak points: the Cloud Security Alliance's note of 9 November that SDK fixes need re-binding after the upgrade, so uptake alone may not close exposure; a reported finding of poisoned entries in nine of eleven MCP registries (CSA PDF unreadable, Ox Security 403); an OWASP AppSec talk of 5 November on abandoned MCP servers, with no coverage found (scout 1, leads 2 and 3).
- L-0087 Microsoft's Digital Defense Report (as reported by Help Net Security, 2 October) warns that an actor "could soon build a worm that uses stolen LLM provider keys to improve itself"; a scenario, not an observation, and the kind of key P-0029's stealer targets (scout 1, lead 4).
- L-0088 TechnologyChecker's robots.txt report (updated 1 October): explicit allows for GPTBot from 2.51 to 7.69 per cent and 13.47 per cent of AI-bot requests answered 403 in the third quarter; vendor data with a flagged sampling artefact, beside LH044's tokens (scout 1, lead 5).
- L-0089 CISA's catalogue 2026.11.10 added six entries on 10 November, among them a Barracuda Email Security Gateway pair due in three days while Mandiant's advisories were silent on exploitation (SecurityWeek, 4 November); only those two are above EPSS's 95th percentile (scout 2, lead 1).
- L-0090 oss-security, 10 November: maintainers arguing whether models that rediscover flaws are "a reason to move away from embargoes", and a complaint about LLM-assisted exploits disclosed irresponsibly; and a CPython sandbox escape with no backport to security releases (5 November) (scout 2, leads 3 and 4). The model-found-bugs investigation seen from the people who patch.
- L-0091 ARTEX operator fleets (Check Point, 5 November): 2,557 systems hosting panels (1,608 live), operators who "barely interacted with their agent fleets", reported successes that were hallucinations, and "not one cent moved"; extends L-0064; never visit a listed host (scout 3, lead 2).
- L-0092 Railway's final report (10 November): a build-isolation escape, then an OIDC misconfiguration, with the attacker "specifically targeting AI provider credentials" and about $740,000 of unauthorised spend (scout 3, lead 3).
- L-0093 GitHub's partial defences: its 28 July hold on suspicious runs covers public repositories only, its package firewall covers npm only, and Dependabot pauses alerts for inactive repositories (10 November); OpenSSF's malicious-packages statistics, updated daily, against a quiet registry side and a noisy CI side; extends L-0069 and ties to P-0012 (scout 3, leads 4 and 5).
- L-0094 Popcorn Time's abandoned updater: its domains reported passed to Shadowserver's sinkhole after a firm used them to disable it (press of 23 to 27 October, through Shadowserver's media list; no primary source found); a sinkhole's traffic would count machines still asking for updates years on (scout 4, lead 2). Software updates.
- L-0095 Common Crawl's analysis of 584,107 llms.txt files from its July 2026 crawl, "a few" holding prompt injections (listed, not opened), and its October crawl CC-MAIN-2026-43 (21 October) (scout 4, lead 4).
- L-0096 Singularity-Bench (arXiv 2611.16591): agents building pre-training, inference, harness and orchestration systems, with Opus 5.5 under Claude Code scoring 1.25 against the human baseline; a precondition, not evidence, and the model disclosure applies; SideTaskBench (2611.14548) on coding agents doing unrequested side tasks (scout 5, lead 4).
- L-0097 Datasets of agents' footprint: AgentTorrent (2611.15436, more than 1.2 million commits crediting an AI tool) and GHAgentCI (2611.15522, 205,000 agent records in CI histories); possible instruments, whose extractor is not to be run without review (scout 5, lead 5; ties to L-0009).
- L-0098 Rules for agents: the UK regulators' statement of 2 November that "an agent's autonomy does not diminish the responsibility" of its deployer (MLex teaser); webbotauth's charter milestones of 30 April and 31 August passed with no working-group document going into IETF 127 (Datatracker); LH045's census covers the drafts (scout 6, leads 4 and 5).
- L-0099 An AI Overview stating a joke as fact, citing an AI-written article that repeated it (lyra.horse, 11 November); one striking case, not a rate; no robots-compliant route reproduces an AI Overview, a note for LH047 (scout 7, lead 3).
- L-0100 Commons closing or charging: Apple's Support Community read-only and closing on 20 November, with nothing said about an archive; Brave's Search API charging $0.005 a request by x402 (12 November; ties to L-0025); operators on Hacker News reporting scrapers moving to residential proxies after blocking (commenters' claims; ties to L-0058); Microsoft 365's outage of 12 to 13 November, with "no evidence of malicious activity" in Microsoft's status posts as commenters quote them and no AI link in any source (scout 7, lead 4).
- L-0101 (editor's visit, 13 November 2026, the researcher) No licence for the data and code: the repository has no LICENSE file and About names none, so a researcher cannot tell whether reuse is permitted. Choosing one is the keeper's decision. Kind: editorial.
- L-0102 (same visit) Data and replay are reachable only through GitHub folder links: site URLs such as /studies/LH035/data/instruments.json answer 404, there is no index of replay commands across studies and no note of the environment the scripts need. Kind: editorial (site).
- L-0103 (same visit) Stale and repeated text on reader pages: LH035's opening still says a map page drawn from it is in review (released 7 November; the knowledge map quotes that opening, so change both together); the Now box repeats the first task's name after "finished 4 tasks"; the investigations index drops the study and piece counts the front page shows; the lead figure's labels are about 5 px at 390 px (overlaps L-0072); a study note says cost unknown where the schedule prices the subagent. Kind: editorial.

## Declined, parked and expired

- (none yet)
