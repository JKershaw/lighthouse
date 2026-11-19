# R-0102: fresh recheck of the R-0100 resolution in the LH047 paper draft, "The web's rules for robots are mostly requests"

**In short.** The reader review of the draft article on the web's rules for robots (R-0100) cleared it, and its resolution added one sentence to the summary and declined two suggestions. We read once what the resolution wrote and checked the new sentence against the judged requests: of the 113 breaches under the rules as fixed, 89 are PyPI interface requests and 9 are Crawl-delay breaches that exist only because reading robots.txt counted as a request, with no overlap, so 98 of 113 (87 per cent) and "most" is true. The declined suggestions' reasons are factually right. Two small wording points in the summary and the stale colophon lines are worth fixing at release; none blocks. Verdict: cleared for release.

- **Rechecker:** a fresh recheck subagent in Claude Code (model reported by the harness: Opus 5.5, claude-opus-5-5), 19 November 2026. I didn't write the draft, the record, any of its reviews or the resolution. I run on the same family of models as the drafter and the reviewers, so this is a review contribution, not independent confirmation. One reading, not a chain: I edited nothing in the draft.
- **Version rechecked:** commit 7d1b809 (HEAD at the time), blobs articles/drafts/rules-for-robots.md 15b892bc144d095bc909beb26352fea1400de7cd, articles/drafts/rules-for-robots.svg 450023d69711cc1b5ab6051f2d38fbefec16f766, articles/drafts/short-rules-for-robots.md 259a617cf85c37f5bb2f73e9fd3eb9aa4dd5aab2. The working tree matched these blobs. `git diff 4d2f00d 7d1b809 -- articles/drafts/` changes only the article's summary line; the figure and short form are unchanged by the resolution.
- **Code and output:** [studies/LH047/review/paper/recheck_r0102.py](../studies/LH047/review/paper/recheck_r0102.py) and [recheck_r0102.out](../studies/LH047/review/paper/recheck_r0102.out), offline: `python3 -I studies/LH047/review/paper/recheck_r0102.py`. It reads only studies/LH047/data/audit/requests-judged.csv and studies/LH047/data/robots-index.csv. It reproduces figures the draft already states; it sets no new reading.
- **No network request** was made. Spend: not available from inside this subagent.

## What I checked

1. **The new summary sentence**, "Most of the 113 rest on our strictest readings: 89 went to an interface PyPI documents for programs but whose robots.txt asks crawlers to avoid, and 9 count only because we treated reading robots.txt as a request."
   - The 113: 172 breaches under reading A, less the 59 that break only the post hoc name rule (R8), leaves 113. Reproduced.
   - PyPI: 89 of the 113 are pypi.org requests, all 89 break R1 under the star group's `/pypi/*/*/json` (88) or `/pypi/*/json` (1) disallow, all 89 to JSON-interface URLs; 88 answered 404, one 200. 85 are the LH041 collector's; 4 come from the essay's drafting agent and reviews. Two of the 89 (the essay reader review's) also break R8, which doesn't matter here because R1 alone puts them in the 113.
   - Crawl-delay: 11 of the 113 break R5. 9 comply once the robots.txt read is excluded (R5_excl_robots), and those 9 break no other rule, so they count only because the read counted as a request; all 9 are LH044's, each 2 seconds after the robots.txt read. The other 2 are the arXiv page-to-page cases.
   - Overlap between the two classes: 0. Union 98 of 113, 86.7 per cent; "most" holds. PyPI alone is 78.8 per cent. The 15 left are 8 other robots.txt (R1), 5 pages kept (R4) and 2 page-to-page Crawl-delay, which matches the body's list.
   - "Strictest readings" agrees with the body: the body says our rules applied robots.txt to every automated request, interface or not, and calls page-to-page "the more natural reading" of Crawl-delay.
2. **The declined suggestions' reasons.**
   - Readability 3 ("up to about 25 minutes later" for all 65): the 9 verdicts resting on a current re-read are on files whose index times run 20:41:01 to 20:43:23 UTC (all 58 current re-read files used anywhere in the audit fall between 20:40:58 and 20:43:30, so "between 20:40 and 20:43 UTC" in the body holds). Their requests were 19:02:05 to 19:35:00 UTC, so the re-reads came 67.8 to 99.5 minutes after, all 9 over 25 minutes. The 56 other after-the-request copies lag at most 25.6 minutes. So the reason is right: the suggested wording would have understated the lag for the 9. Its phrase "for the evening's earliest requests" understates it a little, since it holds for all 9, but that is in the note, not the piece. 4 of the 9 are among the 113, 5 among the post hoc 59.
   - Readability 1 (shorter title): the reason is a judgement, and its factual basis holds: the current title's first sentence carries the catalogue's "mostly requests", which the suggested title drops.
3. **Title and summaries, absolutes and windows.** The title's "mostly requests" rests on the catalogue (most of twenty) and its count carries "On one evening in November 2026". The article summary's "all of them requests to one site's interface ... and all answered 'not found'" is scoped to the 85 (85 of 85, all 404) within the sentence dated "the evening of 8 November 2026". The new sentence carries no absolute. "most of these asks are requests that nothing enforces" describes the kind of rule from its specifications, as the body does ("Most of them are requests. Where there is enforcement, it comes from servers ..."), not an observation over a window; I count it fine, as R-0100 did. The short form's summary ("most of them from one collector") and its "all to the Python Package Index's interface" and "all answered 'not found'" hold for the 85.
4. **Consistency.** The new summary agrees with the body ("We sent 89 ... 85 of them"; "11 came sooner than a Crawl-delay asked. 9 of those count only because ..."), with the figure (85 dark blue, 12 light blue of which 4 are the other PyPI requests, 11 orange with 9 only because of the read, 5 grey; 59; 19) and with the short form, which doesn't state the strictness but says nothing that contradicts it.
5. **Sentences fixed after R-0098 still in place.** "14 of the 19 break no group addressed to the names Anthropic gives the fetcher that reads a page when a person asks, or its agents." is present once; both datelines read "Draft, not yet released"; "robots.txt rules disallowed" is in the figure legend, the SVG description and the alt text. R-0082's fixes also hold: no "133" anywhere, "5 got no answer" in body, figure footer, SVG description and alt text, "only one package record came back, to a reviewer".
6. **Style.** No en or em dashes (counted by code point) in the article, SVG or short form. British spelling throughout ("behaviour", "honour", "licensing"); the only "color" is a CSS property in the SVG, and "authorization" is inside the RFC quotation. No internal codes in the prose.

## Findings

### Must-fix

None.

### Should-fix (not blocking)

1. **The new sentence's grammar.** "an interface PyPI documents for programs but whose robots.txt asks crawlers to avoid" makes the robots.txt the interface's and leaves "avoid" without an object. Exact replacement for
   > Most of the 113 rest on our strictest readings: 89 went to an interface PyPI documents for programs but whose robots.txt asks crawlers to avoid, and 9 count only because we treated reading robots.txt as a request.

   with
   > Most of the 113 rest on our strictest readings: 89 went to an interface PyPI documents for programs, which PyPI's robots.txt asks crawlers to avoid, and 9 count only because we treated reading robots.txt as a request.

2. **"one site's interface" after PyPI is named.** With the new sentence, the summary's last sentence calls PyPI "one site" just after naming it, and a reader may wonder whether the 85 are a different site. Exact replacement for
   > 85 of the 113 came from one collector that read no robots.txt, all of them requests to one site's interface for programs, and all answered "not found".

   with
   > 85 of the 113 came from one collector that read no robots.txt, all of them among those PyPI requests, and all answered "not found".

3. **Colophons are stale.** The article's says "its reader review is to come" and the short form's "reviews to come". Release completes the colophon anyway (AGENTS.md step 4); it should say the evidence review, its recheck, the reader review and this recheck were done, and drop "Draft". This is release mechanics, not a claim.

### Fine

The summary's 89 and 9 and "most of the 113" (98 of 113, no overlap); the reasons given for declining readability 1 and 3; the body's 9 re-reads "between 20:40 and 20:43 UTC" and "up to about 25 minutes" for the 56; every absolute in the title and both summaries; consistency of summary, body, figure and short form; the post-R-0098 and post-R-0082 sentences; British English and no dashes.

## Verdict

**Verdict: cleared for release.** The two wording replacements above are optional and don't change a figure or a meaning; if taken, they are listed in the release note, not sent to another reader.

## Applied by the driving session at release, 19 November 2026

Suggestions 1 and 2 were applied as written ("which PyPI's robots.txt asks crawlers to avoid"; "all of them among those PyPI requests"), and both colophons were completed at release (finding 3). Listed here and not sent to another reader, as AGENTS.md step 4 says.
