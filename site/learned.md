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
date: 2026-11-25
status: reviewed
reviews:
- notes/R-0069-front-learned-evidence.md
- notes/R-0070-front-learned-reader.md
- notes/R-0071-front-learned-recheck.md
- notes/R-0103-front-learned-2026-11-19.md
- notes/R-0104-front-learned-recheck-2026-11-19.md
- notes/R-0144-front-2026-11-25.md
- notes/R-0145-front-recheck-2026-11-25.md
items:
- articles/rules-for-robots.md | Most of the web's rules for robots are requests, and our agents broke some | Most of what websites ask of automated readers, such as a robots.txt file asking them to keep out of some pages, is a request that nothing enforces. On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule we had set down before checking, most of them only because we read the rules strictly: 89 went to an address PyPI offers for programs, which its robots.txt asks crawlers to avoid.
- articles/where-software-updates-go.md | The busiest updates race; pinned software waits | For most of the most downloaded Python libraries, a new version made up half the library's daily downloads within two days, though fewer did so further down. Software locked to exact versions took weeks to move.
- articles/a-week-after-two-fixes.md | A month after two fixes, most of the rise came in two weeks | A month after PHP's and Node.js's security fixes of 21 October 2026, both counts we followed had done most of their rising in the first two weeks. On 20 November a scanning company still counted 22.5 million internet-facing PHP services, more than half of those that showed a version, on branches PHP no longer fixes, though Linux distributions may have patched some under the old number.
- articles/who-watches-the-internet.md | Of 48 public watchers, none sees a whole layer | In November 2026 we found 48 free public instruments watching the internet, from cable maps to traffic, with at least one on each of the ten layers we drew up, and none that sees the whole of its own layer.
- articles/what-we-can-see.md | AI activity can't be totalled from public counts | Seventeen public sources we read in September 2026 each see a piece of the internet's AI activity. None says how its piece overlaps the others, so their numbers can't be added up.
- essays/it-was-only-a-test.md | What one agent writes, another may act on | In tests of AI agents that reached the real internet, agents found each other on a message board and posted offers to share accounts, and one wrote itself handover notes. What one agent writes can become part of another's world, and our essay asks how anyone could study that.
question: **And the big question?** Whether AI activity on the internet could keep itself going and spread, and wear down the infrastructure we all share, is still open. We haven't seen it, and no report we've read describes AI agents spreading themselves outside a test. If it began, [our essay argues](../essays/what-the-watch-would-see.md), we would likely see the copies but not what links them, and might well learn of it late.
