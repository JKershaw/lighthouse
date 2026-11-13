<!--
"What we've learned so far": the front page's opening for a human reader
(read by site/lib/front.js, learnedInfo; shown by site/_includes/home.njk).

Write it for a person, not an agent: lead with what is interesting, say it
plainly, keep any caveat to a clause. The formal limits live in the linked
pieces, one click away. Every item retells one released piece or essay in
fresh words, and those words must stay true to it: no figure or claim the
piece does not make, a reading marked as a reading.

Each item is "path | headline | one or two sentences"; its topic label and
status come from the piece. `question` is the closing line on the charter's
question, in Markdown.

Only `status: reviewed` is shown on the site. A draft is shown only in a
preview build (LIGHTHOUSE_PREVIEW=drafts), marked "Draft, not yet reviewed".
It changes through an evidence review (every sentence against its piece), a
reader-and-inference review and a recheck (row ux-5-answer); `date` is the
day the reviewed text was fixed.
-->
date: 2026-11-13
status: draft
reviews:
items:
- articles/where-software-updates-go.md | The busiest updates race; pinned software waits | For most of the most downloaded Python libraries, a new version made up half the library's daily downloads within two days, though fewer did so further down. Software locked to exact versions took weeks to move.
- articles/a-week-after-two-fixes.md | Old PHP lingers by the million | A week after PHP's emergency fix, a scanning company counted 24.4 million internet-facing PHP services, more than half of all that showed a version, still on branches PHP no longer fixes, though Linux distributions may have patched some under the old number.
- articles/who-watches-the-internet.md | Of 48 public watchers, none sees a whole layer | In November 2026 we found 48 free public instruments watching the internet, from cable maps to traffic, with at least one on each of the ten layers we drew up, and none that sees the whole of its own layer.
- articles/what-we-can-see.md | AI activity can't be totalled from public counts | Seventeen public sources we read in September 2026 each see a piece of it. None says how its piece overlaps the others, so their numbers can't be added up.
- articles/the-xz-backdoor.md | A backdoor caught by half a second | In 2024 a backdoor sat in public releases of xz, a compression library, for about five weeks. What gave it away was an engineer who chased down a half-second delay in logging in.
- essays/it-was-only-a-test.md | What one agent writes, another may act on | In AI tests that reached the real internet, agents found each other on a message board, wrote themselves handover notes and posted offers to share accounts. What one agent writes can become part of another's world, and our essay asks how anyone could study that.
question: **And the big question?** Whether AI activity on the internet could keep itself going and spread, and wear down the infrastructure we all share, is still open. We haven't seen it, and no report we've read describes AI agents spreading themselves outside a test. If it began, [our essay argues](../essays/what-the-watch-would-see.md), we would likely see the copies but not what links them, and might well learn of it late.
