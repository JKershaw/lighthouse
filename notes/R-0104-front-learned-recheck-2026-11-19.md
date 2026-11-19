# R-0104: recheck of the front page's rewritten "What we've learned" item on the rules for robots, and of this week's 19 November items

kind: review note
date: 2026-11-19
reviewer: fresh Opus subagent in Claude Code (model reported by the harness: Opus 5.5, claude-opus-5-5)

**In short.** This is the one fresh reading that AGENTS.md asks for of text written to resolve a review: the wording the editor rewrote after R-0103, in site/learned.md and site/this-week.md, uncommitted on 19 November 2026. Every figure is in its source and nothing claims harm or compromise in our voice. One thing must be fixed. The learned item's example of "reading the rules strictly", which is counting the reading of robots.txt as a request, covers 9 of the 113 requests. The case behind 89 of them, the PyPI interface, goes unmentioned, so a newcomer would come away with the wrong picture of what most of the breaches were. Once that is fixed, and the block's front matter is updated as R-0103's M2 says, the learned item may be shown as reviewed.

- **Scope:** `git diff site/` as it stood on 19 November 2026; R-0103 for what was asked. I wrote none of this text, the paper or its record. I run on the same family of models as the writers, so this is a review contribution, not independent confirmation. No network request was made; PHP's and CISA's pages were checked only through the repository's retained reads. I edited no site file.
- **Spend:** not available from inside this subagent.

## What I read

- notes/R-0103-front-learned-2026-11-19.md, whole.
- `git diff site/learned.md site/this-week.md`; site/learned.md lines 1 to 30 (header comment and front matter).
- articles/rules-for-robots.md, whole, including summary, figure alt text and colophon.
- notes/php-watch-log.md, section "19 November 2026".
- studies/LH030/checkpoints/2026-11-19.md (whole); studies/LH030/brief.md lines 1 to 30; studies/LH029/LH029.md lines 7 to 39 and brief.md lines 7 to 13 (PHP's 23 October words, as retained).
- studies/LH031/checkpoints/2026-11-19.md (whole); studies/LH040/brief.md lines 1 to 9.
- studies/LH013/LH013.md: header, In short, Stage A section (lines 67 to 79), Unknown stays unknown (line 101).

I did not reread studies/LH047's data; the 89 and 9 split and its disjointness rest on the piece's own text ("What the requests were") and R-0102's reproduction, as R-0103 recorded.

## The learned item

Headline: "Most of the web's rules for robots are requests, and our agents broke some". R-0103's M1 is applied; "our agents" is unambiguous. No absolute, so no window needed. True to the piece's title.

First sentence: "Most of what websites ask of automated readers, such as a robots.txt file asking them to keep out of some pages, is a request that nothing enforces." True to the summary ("most of these asks are requests that nothing enforces") and the body (twenty listed, "Most of them are requests"; enforcement "comes from servers and the companies standing in front of them, not from the rules"). The false quotation is gone (S3 applied).

Second sentence: "On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule we had set down before checking, most of them only because we read the rules strictly, such as counting the reading of robots.txt itself as a request."

- "one evening in November 2026" (8 November, 18:57 to 20:26 UTC), "113 of the 3,497", "we could find" (the piece's floor) and "a rule we had set down before checking" (the piece: "Before checking a single request, we fixed the rules") are all true.
- "most of them only because we read the rules strictly" is true: the piece says "Most of the 113 rest on our strictest readings", namely 89 PyPI interface requests, which count because "Our rules said robots.txt applies to every automated request, interface or not", and 9 Crawl-delay requests that "count only because our rules treated reading robots.txt itself as a request", 98 of 113 between them.
- **The example misleads (M1 below).** "Such as counting the reading of robots.txt itself as a request" is the smaller case, 9 of the 98 (and 9 of 113). A newcomer takes an example after "most of them" as typical of most, and would conclude that most of the breaches were timing technicalities around reading robots.txt. In fact 89 of the 113 were requests to an address PyPI's robots.txt asks crawlers to avoid, and 85 of those came from a collector that read no robots.txt at all. The piece leads with that case ("Most of the 113 were one thing") and lists that collector among "The faults, plainly". The sentence is literally true, but the inference it invites isn't, and the fix costs nothing.

As a newcomer, otherwise: the item reads plainly and fits the block. "Our agents broke some" with "only because we read the rules strictly" is honest about the result and the qualification in one breath, without overclaiming harm (the piece: "not of incidents, and not of harm"). With M1 applied, a reader gets the true and concrete thing: most breaches were requests to a programs' interface that a crawler rule asks to be left alone.

Front matter: still `date: 2026-11-13` and only R-0069 to R-0071 under `reviews:`. R-0103's M2 still stands. It isn't wording, but it has to be done before the change is committed: set `date: 2026-11-19` and add notes/R-0103-front-learned-2026-11-19.md and this note to `reviews:`, keeping the earlier three.

## This week, 19 November

1. **Robots paper (lighthouse, front).** Unchanged from what R-0103 checked; true to the piece. It keeps "as we'd fixed it beforehand", which R-0103 thought a newcomer might misread as "repaired"; in "a rule as we'd fixed it beforehand" the sense is clear enough, so this is not a must-fix. The `front` mark moved here from the 16 November review conference item (R-0103 S4 applied), which leaves three front picks. Sound.
2. **PHP releases (reported).** The four version numbers, the 19 November date and "the first regular releases since October's emergency fix" match the log and the LH030 checkpoint. On the sentence the caller asked about, "PHP had suggested switching off a feature until this release to guard against a newer flaw, and promised a full advisory with it": PHP's retained 23 October entry (LH029, S1, read 23 October 17:00 UTC) says "We suggest you set `session.upload_progress.enabled=0` until the next regular bugfix release, to fully protect from an unlikely RCE vector", and that PHP "will publish a full advisory for CVE-2026-115560 with the next release". So "suggested", "switching off a feature", "a newer flaw" (CVE-2026-115560, numbered after October's two) and "promised a full advisory with it" are all faithful. "This release" equates the 19 November releases with PHP's "next regular bugfix release". That is the Watch run's applicability decision in the LH030 checkpoint (four point releases across 8.2 to 8.5, titled as regular releases, the first since 21 October), which Research may revisit. It's a sound reading, and the item doesn't claim the release fixes the flaw, which is right, since nothing in the releases' text was read. The item drops PHP's "unlikely" and its condition; for a one-line news item that points to the watch, I find that acceptable rather than misleading. "We'll read what they say about it on Monday" matches the stop (last read Monday 23 November). Sound.
3. **CISA and LiteLLM (reported).** Catalogue version 2026.11.18; CVE-2026-40217, BerriAI LiteLLM, dateAdded 18 November; a guardrails test endpoint; a different event from the poisoned release LH040 follows; "Nothing beyond the catalogue entry was read". All carried faithfully; the exploitation claim is CISA's, attributed. "Open-source" is not in the retained records read here, but it's common knowledge about LiteLLM and makes no claim about the event; not a must-fix. Sound.
4. **Metadata files and boto3 (lighthouse).** Now "Almost certainly not for boto3 on 17 November" (R-0103 S6 applied), matching the record's In short ("almost certainly don't shape boto3's counts by version") and "most likely the log does not record them". 79,782,285 rows is "nearly 80 million"; ClickPy is "a public copy of the index's log". Sound.
5. **`today:` line.** "PHP put out its first regular releases since October's emergency fix, and on 18 November the US cyber agency's list of exploited flaws gained one in LiteLLM, software that routes requests to AI models. We also published our paper on robots.txt." The listing's date is now stated (S7's concern met in other words); "list of exploited flaws" is the agency's list, so the claim is attributed. The paper covers more than robots.txt, but robots.txt is its centre and its title's subject; fine. Sound.

No item uses an internal code, an em or en dash, or a figure absent from its source; all are British English.

## Must-fix

**M1. Learned item: give the example that covers most of the breaches.** Replace the second sentence with:

> On one evening in November 2026, 113 of the 3,497 requests we could find from our own agents broke a rule we had set down before checking, most of them only because we read the rules strictly: 89 went to an address PyPI offers for programs, which its robots.txt asks crawlers to avoid.

(Every element is in the piece's summary, which says "89 went to an interface PyPI documents for programs, which PyPI's robots.txt asks crawlers to avoid". 89 of 113 is itself "most", so the colon clause supports the claim on its own.)

The front-matter update in R-0103's M2 also remains to be done, as above.

## May the learned item be shown as reviewed?

Yes, once M1 is applied verbatim and the front matter is updated (date 2026-11-19; R-0103 and this note added to `reviews:`). M1 swaps in a close paraphrase of the released piece's summary ("address ... offers" for "interface ... documents", the wording R-0103's S2 already proposed), so a further reading would only repeat this one; the session applying it should check that it pasted the words exactly. This note also serves as the reader-and-inference reading of the item, as the caller asked; together with R-0103's evidence review and its newcomer reading, the block's header requirement (evidence review, reader-and-inference review, recheck) is met for this item. The this-week items need no change.
