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

Set by the keeper (7 November 2026) and flexible: when a limit bites, a run says so in a line and suggests a change, rather than working around it or debating it; the keeper changes it.

- **Active investigations:** at most three. Opening one always waits for the keeper. Active now, three of three: [Where does a software update go?](investigations/software-updates.md), [When a model finds the bug](investigations/model-found-bugs.md) and [What AI activity costs the shared internet](investigations/ai-cost-and-spread.md) (P-0014, opened 8 November 2026).
- **Started without review:** at most two new studies in any seven days, urgent watches included. Deepenings and repairs of a study already running do not count, nor does anything the keeper starts or agrees.
- **Urgent watches:** at most two at once, each ending 14 days after its first read unless the keeper extends it.
- **Every recurring read** has an end date or a stop condition in its brief, so promises cannot pile up for ever.
- **Spend:** no envelope, and not a reason to hold work back for now (the keeper, 30 October and 7 November 2026). "For the next review" gives the spend of the runs since the last review.

## From the keeper

Last reviewed by the keeper: 2026-11-07T10:45Z (written by /keeper at the end of each review).

Directions, blind spots and things to look at. The sweep reads this first and treats each line as a proposal of the highest priority it can give.

- 8 November 2026, at the review: about $200 to $1,000 of spend for that session (at list rates; the keeper pays a subscription with a weekly cap, not list prices), to assign as the session sees fit, "ideally covering any gaps". Don't worry too much about budget. What the session starts under this counts as started by the keeper.
- 8 November 2026: Lighthouse does not try to re-identify people, repositories, accounts or systems that a source has anonymised. "Agreed, that's a line we won't cross." Agents are to be cautious, having read essays/it-was-only-a-test.md; now in AGENTS.md, Rules that matter.
- 8 November 2026: on the exposed-services agent's partial read of a robots.txt (notes/incidents/2026-11-08-robots-partial-read/): "That's a very interesting fault, especially given our essay, a very mild version in a sense." On email addresses already in git history: "The email is fine." On following robots.txt redirects in the closing web: "Always happy to follow the standards."
- 8 November 2026, on what tonight's studies ran into: "There's now classes of data and access, from rules we voluntary follow, routes we don't consider, paid information, licensed information, etc. not to mention private, or ephemeral." Drawn up as P-0022.
- 8 November 2026, following on: "There's many ways we can get what we need, but we're finding where agents' limits are (both by request, by compliance, or a wall), and this is where the human researcher (me, hello) can help; subscriptions, scripts, etc. this also must follow the warnings we learned from agents too keen to answer questions." Added to P-0022.
- 8 November 2026, on P-0022: "Good idea, perhaps a simple paper to document. In a sense we're following the rules of the road, checking for agents who might not heed requests. Documenting those rules is a useful map. Especially if we can see how effectively each is working (eg we overstepped earlier)." P-0022 started as LH047.
- 8 November 2026, on robots.txt groups addressed to Anthropic's agents: "Lighthouse should obey the rules, and is both it's own agent, currently using this harness, model, etc. when we use OpenAI we'll follow those relevant rules, etc." Now in AGENTS.md, Rules that matter; collectors carry it from scripts/robots_tokens.json.

## For the next review

Written by the sweep of 7 November 2026 (08:53 UTC), the first, run as a test.

- **Started without review:** P-0015, how far the poisoned LiteLLM 1.107.0 travelled before it was pulled, under the gate's conditions. The throttle stands at 1 of 2 new studies this week, 0 of 2 urgent watches; the gate kept the second slot free for what the sweeps of 10 and 13 November find.
- **Decided by the keeper, 7 November 2026:** yes to P-0014 and P-0013, and the free slot to L-0014, drawn up as P-0017 and started. The earlier text: **waiting for you:** P-0014, a third investigation (what AI activity costs the shared internet, and whether any of it sustains itself), and P-0013, the closing web, which would open under it. Recommendation: yes to both, with the gate's conditions on P-0013 (Lighthouse's own requests labelled and time-limited).
- **The gate overruled the driving session** on P-0012 (GitHub's trigger change): not urgent, since nothing is lost by waiting, and overstated as a switch-off. It went to the backlog, as did P-0016 (Brotli).
- **Leads the gate judged more urgent than some proposals:** L-0014 (WordPress core's version shares, which change daily and keep no history) and L-0011 (compute prices, whose free history rolls over). Either could take the free slot; recommendation: L-0014, which fits the software-updates instruments.
- **Spend since the last review:** the sweep's seven scouts about $7.7 (six Sonnet 5.5 scouts unpriced, about $5 at Sonnet 5's rates; the Opus wildcard $2.68), the gate as in the commit.

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

## Agreed by the keeper

Agreed and not yet started: the next run takes these after the started lane (schedule/runner.md, step 5).

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


## Backlog

Each proposal: kind (watch, deepening, repair, new question, new investigation), priority (urgent with its deadline, high, normal, lead), status (backlog, started, waiting, agreed, declined, parked, expired, done), the investigation it belongs to, where it came from with dates read, why it is worth asking, a rough cost, and the next step. Declined and expired proposals stay at the end with the reason, so they are not proposed again unchanged.



### P-0022 Classes of data and access: what Lighthouse may read, and what each class hides

- Kind: repair of method, across investigations. Priority: high (the keeper's line of 8 November 2026). Status: started by the keeper, 8 November 2026, as studies/LH047 (the rules of the road), with a simple paper to follow. Investigation: what AI activity costs the shared internet, and the map of instruments.
- Source: the keeper, 8 November 2026 (From the keeper), on what that evening's studies ran into. Examples from one night: rules Lighthouse follows voluntarily (robots.txt kept the closing-web probe from 32 of 161 services, studies/LH044; a dashboard's /api/ disallowed, notes/incidents/2026-11-08-robots-partial-read/); routes Lighthouse does not consider (re-identifying what a source anonymised, studies/LH043; scanning or querying exposed hosts, studies/LH042); paid information (BigQuery's download table, P-0002; Censys's report behind a form, LH042); licensed information (five compute-price series whose terms forbid keeping them, studies/LH045 and P-0021; Epoch's CC BY log kept); private (incident accounts with every identifier withheld; email addresses Lighthouse now withholds itself); ephemeral (PyPI's deleted releases leave no registry time, LH041; GH Archive's hours missing whole event types, studies/LH046; the Wayback Machine refusing this container, LH044; data that rolls over, LH045).
- Why: each class hides a different part of the world, and the gaps are not random: what is walled, licensed, private or gone is often where the activity the charter asks about would be. The map of instruments says where each instrument stops by where it stands, what it counts and who may read it; this would add, for each source Lighthouse reads or declined to read, which class kept it out, so a finding's blind side can be stated by class.
- Cost: small to start: a classification column for the map's rows and for every source a study recorded as unread, refused, withheld or dropped since September, from the records' own fetch logs; then a short essay or note if the pattern earns one.
- Next step: the next horizon sweep reads this first (From the keeper) and decides the form; a natural first step is a table of tonight's refusals and walls by class, from the fetch logs of LH041 to LH046.
- The keeper's route (the keeper, 8 November 2026): where an agent's limit is a request, a rule it complies with or a wall, the keeper, as the human researcher, can sometimes help: a subscription, a script run on the keeper's own machine, an account a task then names. The same warnings apply as to agents too keen to answer a question (essays/it-was-only-a-test.md; notes/incidents/2026-11-08-robots-partial-read/). So: an ask to the keeper is a proposal in this file, saying what the data would answer, which class kept it out, what the study does without it, and that "no" is an acceptable answer; the keeper's help never extends to a route Lighthouse does not consider (re-identifying what a source anonymised, getting round a wall, breaking a source's terms), since a person doing it on an agent's behalf is the same act; and data obtained that way says so in its record (who obtained it, how, under what terms, when), so a reader can tell it from what any reader could fetch.

### P-0021 A price for compute that Lighthouse may keep

- Kind: repair of an instrument for an active investigation. Priority: normal. Status: backlog (the keeper, 8 November 2026: wait; no publisher is contacted). Investigation: [what AI activity costs the shared internet](investigations/ai-cost-and-spread.md).
- Source: [studies/LH045/brief.md](studies/LH045/brief.md), Part A, and its [for-driver note](studies/LH045/for-driver.md); lead L-0011; sources.md S39.
- Why: the charter names "the compute behind them", and price is the one daily public trace of it the sweep found; the cost strand has no price instrument because every free daily series checked forbids keeping it.
- Cost: small once permitted.
- Next step: the keeper's choice between two routes, both outside what a session may do alone: ask one publisher (Silicon Data's public index is the closest fit) for written consent to keep and publish its daily index with attribution, which is contacting a third party; or look further for an openly licensed price series (none found in a bounded check of five sources, 8 November 2026). Until then no series is kept, and a single attributed figure may be quoted in a dated sentence.
- Keeper, 2026-11-08: agreed, we wait. A sweep or study that finds an openly licensed daily price series draws this up again; no publisher is asked.

### P-0023 One shared fetcher for every collector and ad hoc read

- Kind: repair of method. Priority: high. Status: backlog (proposed by LH047, 8 November 2026, for the next sweep to gate). Investigation: none; every study that reads other people's sites.
- Source: [studies/LH047/LH047.md](studies/LH047/LH047.md) (record 0.1, unreviewed), Findings F5 to F12, and its [for-driver note](studies/LH047/for-driver.md): collectors that read no robots.txt (96 of the 97 robots.txt breaches the audit counted), an unreachable robots.txt treated as permission where RFC 9309 says assume complete disallow, robots.txt cut at 64 KiB against the standard's floor of 500 KiB, a reviewer that did not name Lighthouse, Crawl-delay not honoured, 51 requests in no repository log, and whole pages kept where a Content-Signal `use=reference` asks for excerpts.
- Why: each fault was a collector doing its own fetching; one fetcher would make the keeper's robots.txt rule (AGENTS.md, Rules that matter) hold everywhere by construction rather than by each study's care.
- Cost: small to medium: one module under scripts/, then each collector moved onto it by a dated amendment in its brief.
- Next step: scripts/robots_gate.py now exists, and row robots-sweep-1 (open, 9 to 16 November) brings every collector under it; this proposal widens that to a fetcher that reads robots.txt whole (at least 500 KiB), follows its redirects, obeys the token rule from scripts/robots_tokens.json, treats unreachable as disallow, honours Crawl-delay, sends the Lighthouse User-Agent, logs every request into the study's folder, and refuses when any of that fails. LH047's scripts/robots9309.py and scripts/fetch.py are a starting point but do not yet honour Crawl-delay.

### P-0020 Widen the map of instruments on its thin layers: names and the IPv6 address space

- Kind: deepening. Priority: normal. Status: backlog (added by the scheduled run 2026-11-07T1413Z, for the next sweep to gate). Investigation: none; the map (studies/LH035).
- Source: studies/LH035/LH035.md, Next items 2 and 3, and the checkpoint of 7 November 2026 in programme.md, after the map page was released.
- Why: the released map's thinnest layers are certificates, names and running services, and no free instrument read covers IPv6 broadly; the record names unread leads (OpenINTEL, IPv6 hitlists, iGDB, ICANN's public data page, crt.sh) that could change what the map says no one watches.
- Cost: small; reading documentation, as LH035 did, under a short amendment.
- Next step: an amendment to LH035's brief fixing which leads are read and the same inclusion test, then the reads and a dated notice on the map page if a row changes what it says.

### P-0012 GitHub blocks `pull_request_target` by default in public repositories: what breaks, what changes

- Kind: watch. Priority: normal (the gate found nothing is lost by waiting: workflow history is kept in git and brownout failures stay on record). Status: backlog. Investigation: none yet; fits P-0014 if agreed, else software updates.
- Source: [horizon sweep 2026-11-07T0853Z, scout 3](notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md): GitHub's changelog reports brownouts on 9 and 16 November, 16:00 to 18:00 UTC, and enforcement on 2 December; StepSecurity reports the trigger as the TanStack worm's entry point in May. Read through a fetch tool; the changelog is to be read raw before a brief.
- Why: a platform closing the door a self-spreading worm used is a dated, public intervention on the road such spread travels; how many public workflows rely on the trigger, and what their owners do across the three dates, is observable.
- Cost: small; GH Archive and public workflow files, a baseline before 9 November.
- Next step: a brief fixed before outcomes: a sample of public repositories whose workflows use the trigger, read before, during and after each date.
- Gate's notes (GitHub's changelog read raw, 09:22 UTC): blocked by default, re-enabled by a repository's event policy, so not "switched off"; enforcement already moved once, from 2 November; the trigger is one reported worm entry point among several; no sampling frame for affected repositories is named yet.

### P-0016 Brotli's CVE-2026-111497: how far the fix had spread by CISA's deadline

- Kind: deepening. Priority: normal, time-sensitive (CISA's federal deadline 10 November). Status: backlog. Investigation: software updates.
- Source: [scout 2](notes/horizon/2026-11-07T0853Z/scout-2-security.md): disclosed 21 October, found by OpenAI's security researchers, root cause fixed upstream in February without a release, in CISA's catalogue from 27 October; PyPI's brotli 1.2.1 uploaded 22 October. Lighthouse met it only as the reason for PHP's Windows rebuilds of 26 October.
- Why: a library fix with an unusually long gap between the upstream commit and a release, and a regulatory deadline, read with the instruments Lighthouse already has.
- Cost: small to one study.
- Next step: a brief, after reading the upstream history and the advisory raw.
- Gate's notes: whether a model found the flaw is not established, and OpenAI competes with the company whose models Lighthouse runs on, so the model disclosure applies; adding it to "When a model finds the bug" would widen that investigation, the keeper's call.

### P-0018 A dated "This week" line at the top of the front page

- Kind: editorial. Priority: high. Status: done 8 November 2026 (the keeper's direction of 8 November): a dated "This week" block on the front page, read from site/this-week.md, which the scheduled run keeps at its editor's step; items labelled Reported or Lighthouse; hidden when more than eight days stale. Investigation: none (the site). The runner instruction for keeping it is proposed in site/for-driver.md and waits for the keeper, since it changes schedule/runner.md.
- Source: [editor's visit of 7 November 2026](notes/editor/2026-11-07T0956Z.md), the reader's first suggestion: a returning reader had to rebuild the week from Releases, Proposals and the log.
- Why: the front page shows the newest run and the latest findings, but nothing says in plain words what was released, started and decided since last week.
- Cost: small; generated from releases.md, schedule/runs.csv, proposals.md's keeper lines and the studies' checkpoints, with a sentence the editor may hand-set in README.md's header.
- Next step: design it with the Now box; the gate decides whether the editor may add it without review (it shows no finding).
- Keeper, 2026-11-08: yes to the runner step; schedule/runner.md step 7 now keeps site/this-week.md.

### P-0019 Reader-facing pages without internal codes, and a Latest list that reflects what is current

- Kind: editorial. Priority: normal. Status: partly done 8 November 2026: the Now box, study pages and investigation pages show plain names in place of row ids, study codes and proposal numbers (codes kept in title attributes, breadcrumbs and addresses); Latest is ordered newest first by publication or correction and says so. Left: the Schedule, Proposals and Releases pages, and older study pages whose opening falls back to an Answer that cites codes (L-0036). Investigation: none (the site).
- Source: [editor's visit of 7 November 2026](notes/editor/2026-11-07T0956Z.md), the reader's second and third suggestions: P-, LH- and R- numbers, "the gate", "throttle" and script commands on the Schedule, Proposals and Releases pages; and a September piece with a "no correction" notice of 3 November ranked above the October PHP work.
- Why: the codes are right for records and wrong for a newcomer; and a dated notice that changes nothing in a piece's claim arguably should not lift it to the top.
- Cost: small to medium; plain labels beside codes in listings, and a rule for which notices count as activity in Latest.
- Next step: list the reader-facing pages and the codes each shows; propose the rule for Latest.

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

## Declined, parked and expired

- (none yet)
