# R-0103: fresh review of the front page's new "What we've learned" item on the rules for robots, and of this week's 19 November items

kind: review note
date: 2026-11-19
reviewer: fresh Opus subagent in Claude Code (model reported by the harness: Opus 5.5, claude-opus-5-5)

**In short.** We checked the uncommitted front-page text against what it retells: the new first item of "What we've learned so far", on the paper about the web's rules for robots, and the four items and the `today` line added to "This week" on 19 November. Every figure is in its source and nothing claims harm or compromise in our voice. Two things must be fixed: the learned item's headline, "ours broke some", reads to a newcomer as "our rules broke some", and the learned block still carries the 13 November date and review list beside text no review has cleared. The rest are suggestions, the strongest being that, with three items already marked for the front page, none of 19 November's items, the week's one release among them, would reach it. After the two must-fixes the learned item is sound on the evidence, but under the block's own header it needs a fresh recheck of the changed wording before it is shown as reviewed.

- **Scope:** `git diff` of site/learned.md and site/this-week.md as they stood uncommitted on 19 November 2026. I wrote none of this text, the paper or its record. I run on the same family of models as the writers, so this is a review contribution, not independent confirmation. No network request was made; outside pages (PHP's, CISA's) were checked only through the repository's retained reads, as instructed. I edited no site file.
- **Spend:** not available from inside this subagent.

## What I checked

- site/learned.md, whole file (header comment, lines 1 to 20; front matter; all six items; the question line).
- site/this-week.md, header comment (lines 1 to 48), the new `week`, `updated` and `today` lines, the four new items and the existing `front` marks (2026-11-18 agent-framework, 2026-11-17 stolen AI keys, 2026-11-16 review conference).
- articles/rules-for-robots.md, the whole piece including its summary, figure alt text and colophon; releases.md line 5 (released 19 November, version 1.0).
- notes/R-0102-lh047-paper-recheck.md, What I checked, item 1, which reproduces from studies/LH047/data/audit/requests-judged.csv that 89 PyPI interface requests and 9 Crawl-delay requests counted only because reading robots.txt was a request are disjoint, 98 of the 113. I did not rerun its script; the split is also stated in the piece's own summary and in "What the requests were" (85 + 12 + 11 + 5 = 113; 89 PyPI = the collector's 85 + 4 others).
- notes/php-watch-log.md, section "19 November 2026" (bullets on PHP's releases and CISA's catalogue).
- studies/LH030/checkpoints/2026-11-19.md (whole) and studies/LH030/brief.md lines 7, 11 and 23 (PHP's 23 October instruction and the stop).
- studies/LH031/checkpoints/2026-11-19.md (whole).
- studies/LH040/brief.md lines 1 to 9 (how the record describes LiteLLM).
- studies/LH013/LH013.md: header, In short (line 14), the Stage A section (lines 67 to 79), Unknown stays unknown (line 101) and Corrections 0.3 (line 125).
- articles/a-week-after-two-fixes.md line 8 and investigations/software-updates.md line 93 (that the 21 October releases were PHP's emergency fix).

## What I found: the learned item

Item: "Most of the web's rules for robots are requests, and ours broke some | Most of what websites ask of automated readers, such as robots.txt's "keep out", is a request that nothing enforces. On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule as we had fixed it beforehand, most of them only on our strictest readings."

- "Most of what websites ask ... is a request that nothing enforces": true to the piece's summary ("most of these asks are requests that nothing enforces") and body ("We ... listed twenty. Most of them are requests."). The generalisation from twenty listed rules to "what websites ask" is the piece's own, in its title.
- "On one evening in November 2026": the evening of 8 November, 18:57 to 20:26 UTC. True.
- "113 of the 3,497 requests we could find from our own agents": both figures in the piece; "we could find" carries the piece's floor ("the true number can only be higher").
- "broke a rule as we had fixed it beforehand": the piece's wording. True, though see suggestion S2.
- "most of them only on our strictest readings": true. The piece's summary says "Most of the 113 rest on our strictest readings: 89 went to an interface PyPI documents for programs ... and 9 count only because we treated reading robots.txt as a request"; R-0102 reproduced that the two sets are disjoint, so 98 of 113. "Only" is fair: the piece says, of the 9, that counted page to page only 2 broke Crawl-delay, and of the 89 that they count because "Our rules said robots.txt applies to every automated request, interface or not". No figure or claim in the item is absent from the piece.
- Headline absolutes: none (no never, always, all, none), so no window is required. "Most of the web's rules for robots are requests" is the piece's own title claim.
- Headline grammar: see M1.
- Front matter: see M2.

As a newcomer, reading the whole block: it reads well and the new item fits, sitting naturally beside the PHP and watchers items as something concrete and slightly surprising, and its self-criticism suits the voice of the rest. Two snags a curious reader would hit: "ours" in the headline (M1), and "as we had fixed it beforehand", where "fixed" can be read as "repaired" and "strictest readings" is undefined (S2). The block loses its only item about a real past event (xz); that is an editorial choice, not an error. The question line is unchanged and still true to the essay it links.

## What I found: this week

1. **Robots paper (lighthouse, 19 November).** Every claim is in the piece: keep out of some pages or slow down; most asks are requests nothing enforces; it reads what others measured, then checks our own agents; one November evening; 113 of 3,497; "as we'd fixed it beforehand". No internal code. Sound. See S4 on the front mark.
2. **PHP releases (reported).** The four version numbers and the date match the log and the LH030 checkpoint (titles and dates only were read; page `Last-Modified` 19 November 14:00 GMT). "The first regular releases since October's emergency fix" matches the log's "the first regular releases for the 8.x branches since 21 October", and 21 October was the emergency release (articles/a-week-after-two-fixes.md line 8). "We'll read what they say about it on Monday": the stop's last read is Monday 23 November, and the record answers from that read and the releases' text. "PHP had said its newer flaw would wait for this release" is looser than the source: by the brief (line 7, line 11) PHP suggested switching off upload progress "until its next regular bugfix release" and promised a full advisory with that release; it did not say in terms that the flaw would wait, or be fixed then. The investigation page's own summary ("the newer flaw awaits PHP's next regular release") is similar, so this is a suggestion (S5), not a must-fix.
3. **CISA and LiteLLM (reported).** Catalogue version 2026.11.18; CVE-2026-40217, BerriAI LiteLLM, dateAdded 18 November; description about a guardrails test endpoint; "a different event from the one LH040 follows"; "Nothing beyond the catalogue entry was read". The item says each of these. "Open-source software that routes requests to AI models" is consistent with the record's "a popular Python library that sits between applications and AI model providers" (LH040 brief line 3). The exploitation claim is CISA's, attributed by naming its catalogue; nothing is said in our voice. Sound.
4. **Metadata files and boto3 (lighthouse).** "Nearly 80 million downloads" (79,782,285 rows), "no such row", 17 November, "a public copy of the index's log" (ClickPy) and "most likely because the log doesn't record them" all match the record (line 14, A1, line 77). But the bare "Not for boto3 on 17 November" answers more firmly than the record, which says "almost certainly don't shape boto3's counts" and calls the absence "strong evidence, not proof", with three named gaps (an unchecked file-name column, requests logged without boto3's project name, and the import). The recheck R-0101 softened the record's opening for exactly this. Suggestion S6. The trailing "[Our record](...)" follows the style of the 17 November item, so it is consistent.
5. **The `today` line.** True to items 1 to 3. "Listed ... as exploited" is attributed to the agency. The listing was on 18 November, not today, which the line leaves unsaid (S7).

No item uses an internal code, an em or en dash, or a figure absent from its source; all are British English.

## Must-fix

**M1. Learned headline: "ours" reads as "our rules".** After "the web's rules for robots", "ours" most naturally means "our rules", and "broke some" then has no clear object. Replace the headline with:

> Most of the web's rules for robots are requests, and our agents broke some

**M2. Learned front matter still certifies the 13 November text.** The file keeps `date: 2026-11-13`, `status: reviewed` and the three November reviews (R-0069 to R-0071) beside an item none of them read. Committed like this, the site would show the new item as reviewed. Until the recheck below is done, hold the change uncommitted (setting `status: draft` would hide the whole block on the live site, the five unchanged items with it, so it is the worse choice); once cleared, set `date: 2026-11-19` and add this note and the recheck's to `reviews:`, keeping the earlier three, which still cover the five unchanged items.

## Suggestions

**S2. Learned sentence: "fixed" and "strictest readings".** "Fixed" can read as "repaired", and a newcomer can't tell what the strictest readings were. Proposed second sentence:

> On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule we had set down before checking, most of them only because we read the rules strictly, such as counting the reading of robots.txt itself as a request.

or, shorter and keeping the concrete case the piece leads with:

> On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule we had set down before checking; 89 of them went to an address PyPI offers for programs, which its robots.txt asks crawlers to avoid.

Either stays within the piece (89, PyPI, robots.txt, "Crawl-delay ... treated reading robots.txt itself as a request"). If the original phrasing is kept, it is still true.

**S3. Learned sentence: quotation marks on "keep out".** robots.txt says "Disallow", not "keep out", so the quotation marks suggest a quotation that isn't there. Proposed:

> Most of what websites ask of automated readers, such as a robots.txt file asking them to keep out of some pages, is a request that nothing enforces.

**S4. This week: the front picks hide every 19 November item.** Three items are already marked `front` (18, 17 and 16 November), so all three front-page places are taken and none of today's items, including the week's one release, reaches the front page; the header asks for the picks to be reviewed at every update. Suggest marking the robots paper and dropping the mark from the 16 November review conference item (which leaves the week on 22 November and whose next step, the read from 21 November, is still ahead):

> - 2026-11-19 | lighthouse | front | Websites ask automated readers to keep out of some pages or slow down, ...

and `- 2026-11-16 | reported | The [review conference](...` without `front`. Which of the three to unmark is an editorial choice.

**S5. PHP item: what PHP said.** Proposed second sentence:

> PHP had suggested switching off a feature until this release to guard against a newer flaw, and promised a full advisory with it; we'll read what they say about it on Monday, [in our watch of that flaw](studies/LH030/checkpoints/2026-11-19.md).

**S6. Metadata item: hedge the answer as the record does.** Proposed:

> Do requests for a package's metadata file swell Python download counts? Almost certainly not for boto3 on 17 November: a public copy of the index's log had no such row among its nearly 80 million downloads that day, most likely because the log doesn't record them. [Our record](studies/LH013/LH013.md)

**S7. `today` line: the date of the listing.** Proposed:

> today: 2026-11-19 | PHP put out its first regular releases since October's emergency fix, and we saw that the US cyber agency had listed a flaw in LiteLLM, software that routes requests to AI models, as exploited on 18 November. We also published our paper on robots.txt.

## May the learned item be shown as reviewed?

On the evidence, yes once M1 is applied: every figure and claim is in the released piece, "most of them only on our strictest readings" is true to its breakdown (98 of 113), and the headline carries no absolute needing a window. But two conditions stand before `status: reviewed` covers it. First, M2: the front matter must be updated, not left certifying the earlier text. Second, the block's header asks for an evidence review, a reader-and-inference review and a recheck; this note does the first and a newcomer's reading in one pass by one agent, and AGENTS.md step 4 asks that whatever a round writes to resolve a review be read once by a fresh agent before release. So: apply M1 (and any suggestions taken), have a fresh agent read the changed wording once against the piece, then set `date: 2026-11-19`, keep `status: reviewed`, and list this note and that recheck under `reviews:`. Whether this note's newcomer reading counts as the block's reader-and-inference review is the driving session's call to record; I'd count it only if the session says so where it fixes the block.
