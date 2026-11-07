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

## Declined, parked and expired

- (none yet)
