# R-0108: fresh check of the surface lines carrying LH038 version 0.4

**In short.** We read once the uncommitted lines that carry the disclosure-timeline record's version 0.4 onto four public surfaces, and checked each against the record. They say what the record says at its certainty and keep "announced" and "released" apart, with three places where a date or the distinction could be lost; four small edits fix those. No line says or implies that a SUSE fix was, or wasn't, public before Anthropic's post of 27 October.

- **Who:** a fresh subagent in Claude Code (Claude Opus 5.5, model id claude-opus-5-5), for the surfaces round of 21 November 2026. I wrote and reviewed nothing in this study before this reading. A second agent's agreement is a review contribution, not independent confirmation.
- **Model disclosure.** I run on an Anthropic model, and these lines concern Anthropic's post. I read for wording easier or harder on Anthropic than the dates allow.
- **Scope.** One reading, not a chain: `git diff` of AGENTS.md, investigations/model-found-bugs.md, programme.md and observations.md, against studies/LH038/LH038.md version 0.4 (front matter, In short, Answer with its table and policy lines, Finding 4, Limits, Next, the 0.4 Corrections entry), notes/R-0106-lh038-v04-reader.md and notes/R-0107-lh038-v04-recheck.md. For the LH039 row in the same diff, studies/LH039/checkpoints/2026-11-21.md and the brief's stop. Nothing fetched; no keys read; schedule/ not touched; nothing committed.
- **Spend:** not available from inside this subagent; unknown, not zero.

## What I checked

1. **Dates and counts.** Fix author date 1 October, stable releases 11 and 15 October, CVE published 15 October, 12 days before the post of 27 October; SUSE Release Date 24 October for the four earliest followed advisories and 2 November for the eight later; CVE-page stamp and list message 29 October and 3 November; twelve followed SUSE advisories (4 and 8); list read 21 November; Red Hat errata from 1 November; 12 to 26 days. All match the record.
2. **Announced against released (R-0106).** The investigation page says "SUSE announced them after the post" and then that whether any SUSE fix was public before the post isn't known, with what the 24 October date marks unstated and no date for when pages went up or packages reached anyone. That matches Finding 4 and Next. AGENTS.md and programme.md said the list "dates every followed SUSE advisory" after the post, which can be read as dating the advisory itself; AGENTS.md also dropped the release date entirely, against R-0106's ask to keep both dates; programme.md gave only "a 24 October release date", though eight of the twelve carry 2 November. Fixed (changes 1 and 3). The investigation page gave the later eight's announcement day but not their release date; added (change 2).
3. **Before or after the post.** No changed line says or implies that a SUSE fix was public before the post, or that none was. Each keeps the record's "unknown".
4. **Lean.** With the changes, nothing reads easier on Anthropic (as "SUSE's fixes came after the post" would) or harder (as "SUSE released three days before the post" would). The unchanged 45-day sentence on the investigation page was cleared in earlier rounds; R-0107's advisory point on P1's "whichever comes first" patch branch is left untaken, as it touches unchanged text and is interpretation.
5. **Certainty and status.** The record is "reviewed and rechecked" at 0.4 (status field, In short); AGENTS.md and programme.md say so; observations.md said only "reviewed" (change 4). The removed AGENTS.md clause on the amendment's read "by 4 December to settle SUSE's clocks" is right to go: the read was made on 21 November.
6. **LH039 row in observations.md.** Matches checkpoint 2 (tabulated, unreviewed; reads 7 to 21 November; collection closed on 21 November as the brief's stop sets). No change.
7. **Voice.** British English, no em or en dashes in the changed lines (grep count 0), no internal codes in the investigation page's prose beyond those already there. The investigation page's paragraph is long; left as it is, since shortening it is beyond one checking pass.

## Changes (changed lines only)

1. **AGENTS.md, model-found-bugs bullet.** Old: "SUSE's announcement list dates every followed SUSE advisory after the post, and whether any SUSE fix was public before it stays unknown". New: "SUSE's announcement list dates every followed SUSE advisory's announcement after the post, beside release dates on its pages, the earliest 24 October, whose meaning isn't stated, so whether any SUSE fix was public before the post stays unknown".
2. **investigations/model-found-bugs.md, Where the evidence stands.** Old: "(29 October, and 3 November for the later eight), so SUSE announced them after the post." New: "(29 October, and 3 November for the later eight, whose pages give a release date of 2 November), so SUSE announced them after the post."
3. **programme.md, Next, model-found-bugs line.** Old: "finds SUSE's public announcement list dating every followed SUSE advisory after the post (29 October and 3 November), beside a 24 October release date whose meaning isn't stated,". New: "finds SUSE's public announcement list dating the announcement of every followed SUSE advisory after the post (29 October and 3 November), beside release dates on their pages (24 October and 2 November) whose meaning isn't stated,".
4. **observations.md, LH038 policies row.** Old: "version 0.4, reviewed". New: "version 0.4, reviewed and rechecked".

## Not changed (for the driver)

- programme.md's LH039 line, unchanged in this diff, still says LH039 "reads daily to 21 November, with its first checkpoint due on 14 or 15 November"; it is now out of date beside the observations row. Outside this check's scope.

## Verdict

Cleared, with the four changes above, which change no date, count or certainty.
