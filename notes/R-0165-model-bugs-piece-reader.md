# R-0165: reader-and-inference review of the model-found flaw dates piece

Reviews draft version 0.2 of articles/drafts/model-found-flaw-dates.md and its short form, articles/drafts/short/model-found-flaw-dates.md.

## What a reader would believe, written before reading the record

**Said back.** The Linux fix was public in stable kernels 12 to 16 days before Anthropic's exploit post, and the post fell inside Anthropic's own 45-day wait; nobody publicly says when Anthropic reported the flaw.

**Observed.** Dated public events: number reserved 25 September, fix author date 1 October, stable kernels 11 and 15 October, record published 15 October, post 27 October, SUSE list 29 October and 3 November, oss-security 30 October, Red Hat 1 November, Ubuntu tracker 10 November; SUSE pages' 24 October release date; no report date anywhere read.

**Inferred.** That the post is "inside every 45-day window"; that no followed SUSE advisory was announced before the post.

**Generalised.** Little; the piece disclaims generalising well.

**Read stronger than written.** The title, the short form's "So the fix was out 12 to 16 days before the post" and "inside every 45-day window" will read as Anthropic having behaved properly, despite "not a verdict". The 26-day figure counts from an author date the piece says wasn't shown to be public, yet it is used as a policy window. The figure's question mark placed above 25 September may suggest the report came before the reservation. The disclosure about Anthropic's models may be read as having settled the bias question.

**Confusing.** The Anthropic page is "read on 17 November" (line 40) but policies "as we read them on 4 November" (line 54, Sources). The text calls 11 October a release date, but the figure calls it the release commits' author date. The SUSE paragraph's last sentence runs back in time. Line 54's 192 unread advisories sits beside 186 SUSE announcements, with no explanation of how they relate. "The Watch" on the front page doesn't mention the piece.

## Files opened

- articles/drafts/model-found-flaw-dates.md, lines 1 to 68 (whole)
- articles/drafts/model-found-flaw-dates.svg, rendered to PNG only (light theme)
- articles/drafts/short/model-found-flaw-dates.md, lines 1 to 21 (whole)
- README.md, heading list via search, then lines 13 to 26 ("## The watch")

## Stage 2: what the evidence supports

Read for stage 2: studies/LH038/LH038.md (0.4, whole), studies/LH038/scripts/timeline_output.txt (tail), the retained policy page (data/policies-2026-11-04T1415Z/anthropic_cvd.raw.gz) and post (data/read-2026-11-17T1419Z/anthropic_post.raw.gz), searched for their dates and the policy's 45-day and 90-day passages; studies/LH036/LH036.md (header, In short, Answer); investigations/model-found-bugs.md (whole); programme.md's Next (lines naming this investigation); studies/LH054/brief.md (lines 1 to 30 and a search for its comparison caveats); notes/reader-review.md, "Combined disclosure" only.

**Could the measurements be right and the explanation wrong?** Yes, in one place. Every date in the piece matches the records. But the piece implies one reading of the dates: the post came after the patch was available, inside Anthropic's wait. That reading holds only if "a patch is available" means the kernel's upstream or stable fix. If it means a fix that downstream users can install, which is the purpose the policy page itself states, then every distribution announcement we read came after the post: SUSE's list on 29 October, Red Hat on 1 November, Ubuntu's tracker on 10 November. Debian's dates are unknown. On that reading no 45-day window had opened before the post. The record keeps both readings, through its row for 29 October and its qualifier "before it". The piece's headline surfaces keep only the first. A fair title and summary would not give either reading as the answer.

### Material

**M1. "Every 45-day window" drops the record's "before it", and drops the windows the post preceded.** The piece's summary (line 2) says "inside every 45-day wait we could compute from Anthropic's policy page". Line 40 says "inside every 45-day window we could count from them, and inside the one from SUSE's 24 October release date too". The short form (line 14) says "came inside every 45-day window we could count".

The record's table computes windows from SUSE's list and CVE-page date of 29 October, at -2 days, after the post. Red Hat's 1 November errata are also later than the post. The record's own wording is "within 45 days of every candidate date before it", and the investigation page says "every candidate patch date before it". So "every window we could compute" is not true as written. The piece also picks the earlier of SUSE's two clocks for the comparison: the 24 October date, whose meaning isn't stated. It leaves out the 29 October date, which the record's rule supports as SUSE's public announcement. That is easier on Anthropic than the record allows.

The piece also omits the policy's stated purpose, quoted from the retained page: "to give downstream users time to deploy the fix before detailed exploitation information is public". With the "fix was out" line, the short form reads as a verdict of compliance.

Fix, in line 40 and the summary: "The post came 12 to 26 days after the kernel's dates, inside a 45-day window counted from any of them. Counted from the distributions' announcements we read, SUSE's list (29 October), Red Hat (1 November) and Ubuntu's tracker (10 November), no window had opened: each came after the post. The page says the wait exists 'to give downstream users time to deploy the fix', but it doesn't say which patch starts it." In the short form, replace the sentence with "came within 45 days of the kernel's fixes, but before any distribution announcement we read; the policy doesn't say which patch starts the wait." Keep "not a verdict".

**M2. The policy page is given a read date and a modified date that belong to the post.** Line 40 says: "That's the page as we read it on 17 November; it says it was last modified on 30 October, and we couldn't check what it said on the 27th." The sentence sits in the paragraph on Anthropic's policy page, so "the page" reads as that page. But the policy page was read on 4 November, as line 54 and the Sources say. Its retained copy says "Last updated Mar 6, 2026". The 17 November read and the dateModified of 30 October 15:24 UTC belong to the post (LH038, T6; LH036's header). As written, line 40 contradicts line 54, and it misdates a source.

Fix: "We read the post on 17 November. It gives a modified date of 30 October, and we couldn't check what it said on the 27th. We read the policy page on 4 November; it says it was last updated on 6 March 2026, which we couldn't check either." Move this out of the sentence about the policy, or attach it to the earlier sentence about the post.

**M3. Line 56 gives an incomplete list of the unknowns that could fall before the post.** It says: "The unknowns that could still fall before the post are Debian's own advisories, and any Ubuntu notice its tracker doesn't list." Line 34 says that "Whether any SUSE fix was public before the post stays unknown", and the record's Finding 4 agrees. So the 24 October SUSE pages are also an unknown that could fall before the post. So are the fix's first public appearance and the 12 Red Hat errata not followed, though Red Hat's tracker dates its earliest at 1 November. The record's Next words this more narrowly: the revision cannot move SUSE's earliest publication stamp.

Fix: "The revision will look at Debian's own advisories and Ubuntu's notices, the unknowns it can still date. Whether SUSE's 24 October pages were public before the post can't be settled from the sources we know of."

### Readability (optional)

- **R1. The title.** "Stable Linux had the fix 12 to 16 days before Anthropic's exploit post" leads with the dates that favour the post. The distribution announcements we read all came later. Consider "Stable Linux had the fix 12 to 16 days before Anthropic's exploit post, distributions' announcements came after it, and no source we read says when it was reported", or a question title like the short form's.
- **R2. "Released" and the author dates.** The figure's note says the stable dates are the release commits' author dates, and the record says "author dates are not release times". The text says "released". Add "(by the release commits' dates; the changelogs were posted the same day)" at line 18. Alternatively, drop the figure's note.
- **R3. The question mark in the figure.** It sits above 25 September and may suggest the report came earlier than that. Consider moving it beside the scale, labelled "not on the timeline". On the reservation (line 44), note that it may not mark a request: the comparison flaw's record was also reserved on 25 September (LH054's brief). That is one post hoc observation, which is why I suggest a hedge rather than a claim.
- **R4. Line 34's last sentence.** It reads as if the CVE page were a separate check after the two dates. In fact, it was the source of the second date, and its "none of 186" scan was made after the dates were seen. Suggest: "SUSE's page for the flaw, the source of the 29 October date, stamps none of the 186 SUSE announcements it lists before the post (read 16 November; a check made after we'd seen both dates)."
- **R5. 192 and 186.** Line 54's 192 unfollowed advisories include 174 SUSE ones. By SUSE's page, all of those are stamped 29 October or later, though their release dates weren't read. Saying so stops "earlier ones may be among them" from overstating for SUSE.
- **R6. Ubuntu's week.** Line 42 lays "a week after fixes are published" beside the stable kernels. Add a clause saying that Ubuntu's own fixes, by its tracker, came after the post, so the comparison depends on whose fixes count.
- **R7. "Fixes had reached".** Line 50 matches the investigation page. Consider "were listed as fixed for" in both, and mention SUSE's partial state (42 of 121 products on 16 November), which the piece omits there.
- **R8. The comparison case.** Line 56 should keep LH054's caveat: one case, chosen after a scout read it, disclosed under an embargo where this flaw had none. It is not a control.
- **R9. The policy's other 90-day sentence.** Line 40 omits the page's "after 90 days, or after a patch is released, whichever comes first". The record quotes it. Including it would show that the page's two clocks pull in different directions.

## Combined disclosure

I checked the piece, the figure as rendered, the caption, the short form, the linked records and the summaries as a bundle. The mechanism appears only as quotations of Anthropic's public post. There is no code, offset, trigger or host. Kernel versions and advisory names are public listings. Nothing combines into more than the sources publish. **Clears.**

## Next step

Fix M1 to M3 on every surface that carries them, then send the changed passages to the recheck. The question of which patch starts the policy's wait can't be settled from public text. State it as open, and weigh it at the investigation's checkpoint: a later essay on what disclosure means for a model-found flaw could address it. No new collection is needed for this piece.

**Verdict: not ready for release. Three material problems (M1 to M3), all wording; no date or count is wrong.**
