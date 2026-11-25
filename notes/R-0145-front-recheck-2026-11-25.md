# Recheck of what was written after the front-page check of 25 November 2026

**In short.** A fresh agent read once, as AGENTS.md asks, everything the driving session wrote after the check of today's front-page changes: the fixes to "What we've learned" and "This week", the lines it trimmed for the word budget, the rewritten item on the keeper's decision, the first-read openings of the GreyNoise and Amazon studies, and four small renames. Every figure and date is in its source, and each of the check's five must-fix points has been resolved, three by trimming rather than rewording. Nothing must be fixed. Two optional changes would make the keeper item speak as "we" and save a word.

Rechecker: a subagent of the driving session, Claude Code, Opus 5.5, 25 November 2026. I made no web requests, read no credentials, searched nothing in harbour/.session/, committed nothing and edited nothing but this note.

## What I read

`git diff` of all seven changed files; notes/R-0144-front-2026-11-25.md; articles/a-week-after-two-fixes.md (version 2.0, header, summary and body to its close); notes/keeper/2026-11-24-defensive-side.md; the openings of studies/LH060/brief.md and studies/LH061/brief.md; studies/LH059/data/read-2026-11-25T1415Z/README.md, events_read1.csv and claims_read1.csv; studies/LH057/brief.md (opening, definitions, measures); and derived.json.gz from all five LH057 reads (21 to 25 November), parsed with `python3 -I`. For the essay item, which is unchanged since the check, I relied on the check's reading. I checked the added lines of every changed file by code point: they contain no character above U+007F, so no em dash, en dash or other dash.

## What I found

### site/learned.md

- **The item retelling the revised piece.** "A month after PHP's and Node.js's security fixes of 21 October 2026, both counts we followed had done most of their rising in the first two weeks." This matches the piece's summary ("both counts we followed had done most of their rising within two weeks"). "On 20 November a scanning company still counted 22.5 million internet-facing PHP services, more than half of those that showed a version, on branches PHP no longer fixes, though Linux distributions may have patched some under the old number." The piece has "On 20 November Censys counted 22.5 million services running those older branches, 51.8 per cent of all the PHP services that reported a version, down from 24.4 million a week after release", with the distribution caveat. "Still" is fair beside the earlier 24.4 million. The check's must-fix 1, where "Even then" read as two weeks in, is resolved: the date is now explicit. The headline, "A month after two fixes, most of the rise came in two weeks", is fair to the piece's title and close.
- **`reviews:`.** It now names R-0144 and this note (R-0145), so the check's must-fix 2 is resolved once this note exists. The header asks for an evidence review, a reader-and-inference review and a recheck. Here the check covered evidence and a newcomer's reading in one note, as the 19 November change did (R-0103 and R-0104), so the pair follows that precedent.

### site/this-week.md

- **`today:`.** "Amazon's post on AI agents finding a flaw dates the campaign from 8 September but not the operation against the imaging tool." events_read1.csv E1 gives the campaign start as 2026-09-08 and the operation's date as "not stated". "Operation" replaces "attack", so the check's must-fix 5 is resolved. "GreyNoise's decoys have logged no confirmed successful attack on October's PHP flaws since the one on 20 November." At all five reads, `successes_by_day` ends at 2026-11-20 with one row, the table is complete and its rows total 1,305, matching the headline. `summary_cves` names the tracker's two October CVEs. The phrase describes GreyNoise's log, which the brief's "no row listed" rule allows. Supported.
- **The revised-piece item (front, 25 November).** "A month after PHP's and Node.js's security fixes of 21 October, both counts we followed had done most of their rising within two weeks." These are the piece's words, and "followed" corrects the tense. The second sentence that the check found overstated (PHP's shares in general, and Node.js's rise without its rule) has been removed, so must-fix 3 is resolved by trimming. What's left claims nothing beyond the piece. The two name links go to the PHP and Node.js records, which the header allows. No internal codes show.
- **The essay item (25 November).** Unchanged since the check and supported there.
- **The Amazon study item (25 November).** "We've read Amazon's report once, unreviewed: what it says the agents did rests on the operator's own records, and it gives no date for the operation against the imaging tool." This matches the README ("everything Amazon says about what the agents did rests on the operator's own platform records") and E1. "Attacker's" has become "operator's", and the unattributed "instance left open" clause has gone, so must-fix 4 is resolved by trimming. The study link goes to the brief.
- **The keeper item (front, 24 November), rewritten.** "Lighthouse will study the defensive side: which defences work, how fast fixes arrive and how well organisations recover, never how self-spreading AI activity could be built." This matches the note's "which defences work, how fast fixes reach the systems that need them, and how well organisations recover together", and its rule that Lighthouse "doesn't work out, map or write down how such activity could be built" and doesn't study feasibility from the attacker's side. The note says the defensive questions are how Lighthouse pursues this side, and that it covers outcomes only. The links are labelled "what research has measured about [containment and recovery](LH061), and about [how operators of different sizes install fixes](LH060)". These match the openings: LH061 asks how much has been measured about whether containment and recovery work, and LH060 asks what research has measured about deployment by operator size. Nothing is untrue. The item no longer says the keeper made the decision, but "the decision" links to it. It says "Lighthouse" where every other item says "we" (see Optional).
- **The Amazon report item (front, 24 November), with "that CISA lists as MONAI Label" dropped.** "...found and used a flaw it judges unpublished in a medical-imaging AI tool, 'on their own'." Still true: the post itself says "an open-source medical imaging AI application" and never names it in its text (README). Every claim stays attributed to Amazon. Nothing in our voice asserts harm or names a compromised system.
- **Front marks.** Three: the revised piece (25 November), the keeper's decision (24 November) and Amazon's report (24 November). The mark has gone from the PHP record item of 23 November. This is as the check recommended.
- **`week`, `updated`.** "2026-11-19 to 2026-11-25" and "2026-11-25". Correct, and no item before 19 November remains.

### Study openings

- **studies/LH057/brief.md.** "Daily reads began on 21 November (updated 25 November; unreviewed): through 25 November, GreyNoise's list of confirmed successes had no entry after 20 November." Supported by the five derived files as above, through GreyNoise's update stamp of 2026-11-25T13:49:13Z. It's marked unreviewed, outside the protocol, and has no codes.
- **studies/LH059/brief.md.** "The first read was taken on 25 November (updated 25 November; unreviewed): Amazon dates the campaign from 8 September but gives no date for the operation against the tool, and what it says the agents did rests on the operator's own records; two sources were behind walls." Supported by E1 and the README. "Two sources were behind walls" is the advisory (D2) and the release record (D6), each 403 by both routes. OSV's 404 was a second route to D2, not a third source. The rest of the opening (rereads on 8 and 15 December, a record by 18 December) matches the brief.

### Renames

- glossary.md: four "Used in" links renamed "A month after two fixes". The W3Techs entry's "2 to 8 per cent" on 25 and 26 October is still in the piece. Fine.
- site/sections.md: "How far two fixes had spread a month on". Fine.
- investigations/software-updates.md: the piece is added to `pieces:`, where it wasn't listed before (no duplicate), and it is already described in the page's pieces section. Fine.

## Must fix

None.

## Optional

- **The keeper item.** "Lighthouse will study the defensive side" could read "We'll study the defensive side". That speaks as "we", like the other items and as the Writing rules ask, and it saves one word against the 1,250-word budget.
- **On the This week page,** the 25 November Amazon study item ("Amazon's report", "the imaging tool") sits above the 24 November item that introduces both. On the front page the day's line introduces them, so this only matters on the full page. Leave it unless words allow.
