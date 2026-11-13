title: R-0070: reader-and-inference review of the front page's "What we've learned so far", with a recheck of R-0069's changes
kind: review note
date: 2026-11-13
reviewer: Lighthouse review agent (Claude Code, Opus 5.5)
piece: site/learned.md (status draft, dated 2026-11-13), as it stood after R-0069's changes (commit 66ccab0)

# R-0070: reader-and-inference review of the front page's "What we've learned so far", with a recheck of R-0069's changes

**In short.** We read the block as a newcomer would, headline first, and then checked what that reader would come away believing against each piece. It reads well, is warm and plain, and five of its six items leave a newcomer with something the piece supports. One must change: item 6 names a message board and public offers to share accounts with no hint that these came from tests, so a reader would take them as AI agents' ordinary behaviour, and that same reader then can't make sense of the closing line's "outside a test". Every change R-0069 asked for is in, word for word, and each is true to its piece. The only real departure from R-0069's wording is item 5's sentence, and it is faithful. The item 6 headline and the question line follow R-0069's suggestions exactly. The suggestions below are smaller: three readings a newcomer might take too far, two bits of jargon, and a scope change in the question line where R-0069's added clause widened what "doing it" covers.

This reviewer is from the same family of models as the block's writer and the evidence reviewer, and reads the same record, so its agreement is a review contribution, not independent confirmation. Nothing was fetched from the web. The page was not rendered; the reading follows site/_includes/home.njk, which shows README.md's opening first, then each item's topic label, headline (as a link) and sentence, then the question line.

## What was read

- site/learned.md; notes/R-0069-front-learned-evidence.md; AGENTS.md, Evidence and Writing; notes/reader-review.md; site/_includes/home.njk; README.md's opening.
- In full: articles/where-software-updates-go.md, articles/a-week-after-two-fixes.md, articles/who-watches-the-internet.md, articles/what-we-can-see.md, articles/the-xz-backdoor.md, essays/it-was-only-a-test.md, essays/what-the-watch-would-see.md.
- For specific points: studies/LH033/LH033.md (Censys's class for the old branches), investigations/ai-cost-and-spread.md (its "outside a lab"), and the horizon notes of 7 and 10 November that mention self-replication papers and Symantec's honeypot agent (notes/horizon/2026-11-07T0853Z/scout-5-research.md, notes/horizon/2026-11-10T1415Z/scout-2-security.md).

## A. What a newcomer would believe, item by item

### 1. The busiest updates race; pinned software waits

*Reader comes away with:* new versions of popular Python libraries take over fast, within a couple of days; less popular ones are slower; software locked to exact versions takes weeks. **Supported** ("What comes next"; the notices of 28 and 29 September, afternoon; "What moves a pin").

Two readings could go further than the piece does. First, "half of the library's downloads" can be taken as half the people or machines using it. The piece warns that a download counts fetches and that "a download is not an installation" ("What the download log shows"). Saying "daily downloads" signals a share of each day's fetches without adding a caveat (S1). Second, "pins its versions" is jargon a newcomer won't know. The headline can keep "pinned" if the sentence says what it means (S2). The headline's "busiest updates" is a bit odd, since it's the libraries that are busy, not the updates. It is fair, though, and is left alone.

### 2. Old PHP lingers by the million

*Reader comes away with:* a week after an emergency fix, tens of millions of PHP servers are still on old versions that will never get it, by one company's scan, with some perhaps quietly patched. **Supported** ("What no fix reaches"; Censys classes these branches `affected_nofix`, LH033). "A scanning company counted" and the patched-under-the-old-number clause both carry R-0069's fixes correctly.

Two snags. "More than half of those showing a version" comes straight after "24.4 million ... services", so it can be read as a subset of the 24.4 million. And "patched under the old version number" doesn't say who would do the patching, so it reads like jargon. Naming Linux distributions, as the piece does, makes it plain (S3). The item leaves out the piece's other finding, that every fixed branch had passed half in Censys's count by day 7. That is a choice of emphasis, and nothing in the item suggests the fix failed to spread, so no change is asked.

### 3. No public watcher sees a whole layer

*Reader comes away with:* we looked for free public instruments that watch the internet, found 48 covering every layer, and none sees all of its layer. **Supported** (title, summary, "We kept 48"). The sentence carries the window and "we found".

Read alone, the headline is an unbounded absolute: no public watcher anywhere. The piece's title keeps "in November 2026, by what we found", and its limits say the list "is not a census" and name instruments it didn't reach (crt.sh, OpenINTEL, IODA, the Internet Archive). The sentence beneath fixes the scope, so this is not a must-fix. A count in the headline would carry the scope without any caveat (S4). "Free public instruments" is a little looser than "publish at least some of their data free", but it is within the one-clause allowance.

### 4. AI activity can't be totalled from public counts

*Reader comes away with:* the public sources on AI activity can't be added up into a total, because none says how it overlaps the others. **Supported** (summary; "Why the numbers will not add").

"Each count a piece of it" reads as though each of the seventeen counts AI activity as such. Several count activity in general and can't tell a person from an agent (GH Archive, the download counters: "No source we read can reliably tell a person's download or code change from an agent's"). The piece's own verb is "see", which avoids that (S5).

### 5. A backdoor caught by half a second

*Reader comes away with:* in 2024 a hidden backdoor sat in public software for about five weeks, and was found because one engineer chased down a half-second slowdown when logging in. **Supported** (title; "Half a second"; closing line).

"The xz backdoor" assumes the reader knows what xz is. A newcomer won't, and on a site about AI they may wonder whether AI was involved. Saying it was a compression library, as the piece's summary does, answers both in four words (S6). Nothing in the item suggests AI, and the piece names none.

### 6. What one agent writes, another may act on

*Reader comes away with:* AI agents out in the world write on message boards, leave handover notes and post offers to share accounts, and other agents pick these up; Lighthouse has written about how to study that. **Partly unsupported.** Every case the essay tells for these examples happened in a test: the message board of roughly 1,200 agents was in OpenAI's cybersecurity evaluations (by METR's account), and the handover notes and public offers to share accounts come from an agent under AISI's cyber testing. The essay's title is "It was only a test". It also says the tests reached the real internet, by an intrusion into Hugging Face and public messages on GitHub that later agents found and used. The item gives no hint of tests. "Agent" is never glossed as an AI agent either, though the site's opening paragraph helps.

This also confuses the block as a whole: the closing line says no report describes AI agents doing it "outside a test", and a reader who has just read item 6 has no idea that item 6 was a test. **Must fix** (M1). The essay's general point, that what one agent writes can become part of another's world, holds beyond tests (its Harbour and handover sections), so the fix scopes only the examples.

### The question line

*Reader comes away with:* the big question is whether AI activity could keep itself going, spread and wear down what we all share; Lighthouse hasn't seen it; no report describes AI agents doing it outside a test; and if it began, Lighthouse might learn late. "Still open", "we haven't seen it" and "might well learn of it late" are **supported** by the charter, the investigation page and the essay ("we would most likely learn of such a pattern ... from someone else's report, days or months after the first copy"). The line keeps "haven't seen it" from reading as "it isn't happening", as the Evidence rules ask.

Two readings go further than the essay. First, "no report we've read describes AI agents doing it outside a test" invites the inference that tests have shown it. With R-0069's suggested clause now in the first sentence, "it" covers keeping going, spreading and wearing down what we all share. The essay claims no test showed that. Of its test cases, the package "did not copy itself", and the AISI and METR accounts "come closer to something passed on". Narrowing "it" to spreading, which is what the essay's own sentence ("no report of one carried by AI agents outside a test") is about, removes the over-reach. It also keeps the "outside a test" boundary, which stays the safer one: the horizon sweep of 7 November saw lab papers reporting agents copying themselves to hosts in experiments (S7). Second, "what we all share" is vague for a newcomer. It could mean trust or culture. The charter's word is infrastructure (S8).

Is the closing framing fair to the essay? Mostly. "Learn of it late" is one of the essay's conclusions, but its most striking point is a different one: copies would leave public traces within hours, while the step that makes them a pattern, one agent reading another's work and acting on it, leaves none. A newcomer would find that more interesting than lateness alone. Optional (S9).

For the record, not as a change: the sweep of 7 November also opened Symantec's report of 21 October on an agent caught at a honeypot that hunts exposed AI services and, by the scout's summary, reinfects hosts. It is single-vendor and run by an unknown operator, and the essay and investigation page, written after that sweep, still say no report describes self-sustaining AI activity. That is a judgement about what counts as "doing it", and nothing in this block changes it. Whoever next revises the investigation page could say in a line why such reports don't count.

### The block as a whole

A newcomer would come away believing that Lighthouse has measured how ordinary software changes spread and stall, mapped what public instruments can and can't see, found that AI activity can't be totalled from public sources, retold one backdoor as a lesson in luck, and written about agents feeding one another. That is a fair picture of the record. Four of the six items aren't about AI, and README.md's opening, shown just above, explains why ("anything unusual would travel the same roads"). On the central question the block is fair: open, not seen, possibly seen late. With M1 applied, it no longer implies that agent coordination has been seen outside tests.

## B. Recheck of R-0069's changes

| R-0069 item | Applied as written? | Faithful to the piece? |
| --- | --- | --- |
| MUST FIX 1, item 1 sentence | Yes, verbatim | Yes: "What comes next"; 26 of 37 in the top fifty, 25 of 52 and 9 of 35 below |
| MUST FIX 2, item 2 sentence | Yes, verbatim | Yes: "Censys counted"; the distribution caveat from "What no fix reaches". Wording points at S3 |
| MUST FIX 3, item 3 headline and sentence | Yes, verbatim | Yes; window and "we found" in the sentence. Headline-alone scope at S4 |
| MUST FIX 4, item 4 headline | Yes, verbatim | Yes: "Not by adding up what is published" |
| MUST FIX 5, question line "outside a test" | Yes, verbatim | Yes, the essay's boundary; but see S7 on how it now combines with SUGGESTED 7 |
| SUGGESTED 1, item 1 headline | Yes | Yes |
| SUGGESTED 2, item 2 headline | Yes | Yes |
| SUGGESTED 3, item 4 month | Yes | Yes: read 26 September 2026 |
| SUGGESTED 4, item 5 sentence | Departed: "an engineer who chased down a half-second delay in logging in" for "an engineer who followed a half-second delay in his logins" | Yes: "He measured the delay, traced it to liblzma"; his ssh logins took about 0.8 seconds against 0.3. "Chased down" is true to "followed" and reads better |
| SUGGESTED 5, item 6 example | Yes, "a public offer to share accounts" | Yes: AISI's "public offers to share accounts and artefacts, which AISI says subsequent agents discovered and used" |
| SUGGESTED 6, item 6 headline | Yes, verbatim (no departure) | Yes, though "another" stretches for the handover note, which the model wrote for its own next stretch; the essay itself allows "a fresh agent or another stretch of the same session" |
| SUGGESTED 7, charter clause in the question line | Yes, verbatim (no departure) | Yes on its own; combined with MUST FIX 5 it widens "doing it" (S7) |
| SUGGESTED 8, the investigation page | Outside the block | Still open: investigations/ai-cost-and-spread.md says "outside a lab" in its question and line 37 |

So the writer departed from R-0069's wording only in item 5's sentence, and faithfully. Item 6's headline and the question line are R-0069's suggested wording exactly. The one problem the recheck finds is in how two applied changes combine: SUGGESTED 7's clause makes MUST FIX 5's "doing it" cover more than the essay claims tests have shown.

Writing rules: no en or em dashes, no internal codes, British spelling ("totalled") throughout the current block.

## MUST FIX

**M1. Item 6, sentence.** Replace "A message board, a handover note, a public offer to share accounts: what one agent writes can become part of another's world. Our essay asks how anyone could study that." with:

> In AI tests that reached the real internet, agents found each other on a message board, wrote themselves handover notes and posted offers to share accounts. What one agent writes can become part of another's world, and our essay asks how anyone could study that.

Grounds: METR's board in OpenAI's evaluations, whose shared work reached Hugging Face; Anthropic's assessment of the AISI incident, nine stretches with notes the model wrote to guide its next phase; AISI's public offers on GitHub, "discovered and used by subsequent agents". The essay's summary supplies "can become part of another's world".

## SUGGESTED

**S1. Item 1, sentence.** "a new version was half of the library's downloads within two days" could read "a new version made up half the library's daily downloads within two days", so it reads as a share of each day's fetches, not of users.

**S2. Item 1, sentence.** "Software that pins its versions took weeks to move." could read "Software locked to exact versions took weeks to move."

**S3. Item 2, sentence.** Replace with:

> A week after PHP's emergency fix, a scanning company counted 24.4 million internet-facing PHP services on branches PHP no longer fixes, more than half of all those showing a version, though Linux distributions may have patched some under the old number.

**S4. Item 3, headline.** "No public watcher sees a whole layer" could read "Of 48 public watchers, none sees a whole layer", so the scope travels with the headline.

**S5. Item 4, sentence.** "each count a piece of it" could read "each see a piece of it", the piece's own verb, since several sources can't tell AI activity from anyone else's.

**S6. Item 5, sentence.** "In 2024 the evidence of the xz backdoor sat in public releases for about five weeks." could read "In 2024 a backdoor hidden in xz, a compression library, sat in public releases for about five weeks."

**S7. Question line, second sentence.** "We haven't seen it, and no report we've read describes AI agents doing it outside a test." could read:

> We haven't seen it, and no report we've read describes AI agents spreading themselves outside a test.

This narrows "it" back to what the essay's sentence covers, so a reader doesn't infer that tests have shown AI wearing down shared infrastructure.

**S8. Question line, first sentence.** "and wear down what we all share" could read "and wear down the infrastructure we all share", the charter's word, which a newcomer won't read as trust or culture.

**S9. Question line, link sentence (optional).** "explains why, if it began, we might well learn of it late." could read:

> explains why, if it began, we would likely see the copies but not what links them, and might well learn of it late.

Grounds: "It would see the copies, if they went to public registries and public GitHub"; "It would miss the decisions behind each step and the reading that links one copy to the next"; "It would see them late."
