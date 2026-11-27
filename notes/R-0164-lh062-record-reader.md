# R-0164: reader-and-inference review of the LH062 record, stage 1

Reviews LH062 record version 0.2 (27 November 2026).

## What a reader would believe, written before reading the record

**Said back.** Published research on leaked passwords, keys and tokens is thin: three papers and two vendor posts. Leaked secrets mostly stay in public view for weeks to about a year, and many keep working; after researchers emailed owners, half came down in two weeks but most still worked, and exposures crept back. Nobody has tested whether telling owners helps.

**Observed.** The papers' and posts' own figures (81 per cent still present after 16 days; about 12 months average on websites; 1,405 to 706 exposed, 1,175 to 865 valid after emails; the vendor figures). Lighthouse's own observation is only what six searches found.

**Inferred.** That removal and loss of validity are separate outcomes that move apart, labelled interpretation; "half came down ... about three in four still worked" is Lighthouse's arithmetic within one study.

**Generalised.** "What published research says" in the opening's first sentence frames five documents as the literature; the Answer later says it is not. "Leaked secrets" is drawn from one GitHub sample (2018) and one web sample.

**Likely read stronger.** The opening sets "half came down" beside "three in four still worked" in one sentence, so a reader may take three in four of the removed keys as still working, or the emails as having caused the removals; neither is stated. "Exposures had crept back up" invites "owners re-leaked". The withdrawn third paper is counted in "three research papers" though it gives nothing, so the evidence sounds broader than two.

**Confusing.** "Venue" and "vendor stream", "known case", "stop gate", "kept: no" and the "Never done rule" are unexplained internal terms. The vendor post's "28.2 per cent still public" where "the secret was gone" is hard to parse. The front page section read mentions none of this, which is consistent with "nothing on a public page".

## Files opened

- /home/user/lighthouse/studies/LH062/LH062.md, lines 1 to 41 (up to, not including, "## Findings" at line 42).
- /home/user/lighthouse/README.md, lines 1 to 26 (opening and "## The watch", the nearest equivalent to "Current focus", which does not exist; headings listed by grep).
- schedule/research-safety.md was not opened; no disclosure concern arose.

## Stage 2: what the evidence supports

Read for stage 2: the whole of studies/LH062/ (LH062.md, brief.md, sources.md, searches.md, claims.csv, fetchlog.csv, derived/*.json, derive.py and tally.py by their output, tally-output.txt, review/check-output.txt and review/rereads.csv), investigations/ai-cost-and-spread.md (searched for LH062 and credential lines, and item 8 read whole), programme.md's Next (the LH062, LH061 and credential lines), studies/LH061/LH061.md (the A02 and A07 rows, Method and Corrections, by search), notes/reader-review.md ("Combined disclosure" and "After the review") and schedule/research-safety.md. No web request, no other note, no git history.

**Could the measurements be right while the explanation is wrong?** Yes, in three places. The authors' figures are transcribed faithfully (tally and the review's check reproduce every share). But the In short turns a sample found exposed at the end of a window into a typical lifetime, turns daily totals into the fate of a fixed set of keys, and leaves out that the only paper the searches added gives no figure. The record's "Read together" reading is plausible but is post hoc and unlabelled as such. My stage 1 reading ("leaked secrets mostly stay public for weeks to about a year, ... half came down after emails, most still worked") is stronger than the evidence on each of these points.

### Material

**M1. The 12-month average is read as how long an exposed key stays up, but the sample is keys still up and working at the end.**
Text (In short): "keys exposed on websites stayed up for about a year on average, as far as nine archive snapshots could show". Answer: "Credentials exposed on websites' landing pages stayed public for an average of 12 months (1 to 60), measured across nine archive snapshots, which bound it".
The population is 1,748 credentials "confirmed valid ... in HTTP Archive's September 2025 crawl", traced back through earlier snapshots from their first appearance. A sample drawn at the end of a window holds the long-lived exposures more often than the short-lived ones (one found in September 2025 is more likely to have been up for a long time), and those still up are cut off at the window's end. So the mean can be right and still not be the typical lifetime of an exposed key. The record doesn't say how a duration ends for a credential that was present at the end, or how a 10 per cent fall "in the first month" fits a sample that was all present at the end. The derived file can't settle that, so the paper's text should be reread, or the record should say it's unknown. The Limits section mentions the snapshot bound but not this selection.
Fix (In short): "keys found on websites in September 2025, all still working then, had been visible for about a year on average, as far as nine archive snapshots could show. Because these were keys still up at the end, that isn't how long a typical exposed key stays up." Add the same qualification to the Answer and a line in Limits, and say how the authors end a duration, or that the text read doesn't say.

**M2. Daily totals after the emails are read as what happened to the same keys, and as the owners' response.**
Text (In short): "after the researchers emailed the sites' owners, half the exposed keys came down within two weeks while about three in four of the keys that had worked at the start still did, and exposures had crept back up nearly six months on."
The figures are daily counts of "exposures" (1,405 to 706 to 1,019; 1,175 to 865 to 660). Whether that is distinct credentials or credentials counted once per site isn't stated (Findings). The rise by day 172 shows the count can grow, so it isn't shown to be one group of keys followed through. At least one email reached 68.5 per cent of sites, so about a third of the counted exposures may belong to sites that got no message. The In short calls all of them "keys" whose owners were emailed.
Fix: "after the researchers emailed the sites (at least one email got through to about two in three), the number of exposed keys they found each day halved within two weeks, and the number still working fell by about a quarter. Nearly six months on, the number of exposures had risen again. These are daily totals, not the same keys followed one by one." The Answer's after-notification bullet should carry "daily totals" and the 68.5 per cent with its denominator (see R1).

**M3. The evidence base and the unanswered half of the question drop out of the summary.**
Text (In short): "Six fixed searches and two papers we already knew gave us three research papers and two security companies' blog posts that followed leaked credentials over time. In the papers, ..."
Only two papers give any figure, and both were known before the brief, their outcomes already seen (Overlap). The one paper the searches added gives none (its figures are withheld). No paper measured whether keys keep working without anyone being told ("Still valid, unprompted (venue): not answered"). The Answer and Limits say all this ("the venue table is the two documents the study started from"), but the summary invites a reader to think the searches found the papers and that both halves of the question were answered.
Fix: "Six fixed searches found one new research paper, which in the end gave us no figures we could use, and two security companies' blog posts. So the research figures come from the two papers we started with, whose results we'd already seen. Neither paper measured how long keys keep working when nobody tells the owner."

**M4. A reading made after the figures were seen isn't labelled post hoc, and has a competing explanation.**
Text (Answer): "Read together (interpretation, labelled so): in the documents read, removal from public view and loss of validity are separate outcomes that can move apart."
No hypothesis in the brief sets this up. It was formed after reading, and A07's pattern was already in LH061's table ("removal fell then returned; revocation kept falling") before the brief was written. AGENTS.md asks for such a reading to be labelled post hoc, with the number of comparisons, and to name what could test it. For A07 specifically, a rising count of "exposures not removed" next to a falling count still valid could also come from the day-172 scan finding exposures the earlier scans missed, or from counting per site, rather than from the same keys being removed but still working. W4's "more than half of taken-down keys still valid" is the more direct evidence. The two documents don't share a unit, so they are two separate observations, not a replication.
Fix: "Read together (interpretation, post hoc: formed after the figures were seen, and for A07 known before the brief; two documents, one reading): ... A07's day-172 counts fit it but could also reflect what the later scan counted; W4's figure on taken-down keys is the more direct. Nothing in this study tests it; a study built around one unit and one place (Next) could."

### Readability (optional)

- **R1. The denominator of 68.5 per cent.** Findings says "at least one delivered to 1,668 websites (68.5 per cent)", and the review's check computes 1,668 / 2,435 *entities*. The Answer has "68.5 per cent of sites". The authors' "71% of sites (1,729 domains)" implies about 2,435 sites as well, so it may be the same number. Name the denominator the authors use, or say they don't state it.
- **R2. A02's year and place.** "most leaked secrets in one sample of public code were still in place after 16 days" could become "in one 2018 sample of public code on GitHub, most leaked secrets were still in the current files after 16 days, and even removed ones stayed in the history". Its "secrets" are candidates that passed the authors' filters, not checked with providers. A clause on that would help.
- **R3. The In short's last sentence is about process.** "This version has had an evidence review ... but not yet its reader review" could become "It has been checked once against its sources, with fixes applied, but not yet read for how it might mislead, so nothing from it is on a public page yet."
- **R4. W6's 28.2 per cent.** "of 5,000 repositories where 'the secret was gone within 5 days', 28.2 per cent were still public" is hard to read. Something like: "where the vendor no longer found the secret within five days, 28.2 per cent of 5,000 sampled repositories were still public; what 'gone' means isn't stated."
- **R5. Stale lines for the release session's consistency check.** Item 8 on the investigation page still says LH062 has had "nothing ... read yet", and programme.md's Next still says P-0053 "goes to the sweep's gate". Update both when the LH062 line is written.
- **No balance problem found.** Google's gift to A07's authors, the unnamed AI developer among A07's services, GitHub's ownership and both vendors' commercial interest are disclosed. W4's headline "never revoked" isn't repeated as a finding (the record gives 74 per cent at day 31). Nothing is easier or harder on Anthropic or any vendor than the sources allow. The In short contains no internal codes, so it meets the letter of the plain-opening rule; M1 to M3 are about what it claims.

### Combined disclosure

Clears. The bundle (the record, its derived files, claims.csv with the withheld rows, sources, searches and fetch log, the investigation page and LH061's published record) holds aggregate durations and shares only. It contains no credential, host, repository or account, no method of finding or testing credentials, and no per-provider or per-platform figure that LH061 hasn't already published at its authors' level. The withheld rows are gaps, and the shape of those gaps lets a reader infer nothing beyond the document's own public title.

### Next step for the study

Adjust, then stop. Collection is complete under the stop gate. Resolve M1 to M4 in the record (M1 may need one reread of A07's method, inside the brief's twelve GETs and before 14 December), have a fresh agent recheck what the resolution wrote, then add one line to the investigation page and no article. Before any follow-up on a single unit goes to proposals.md, its design should separate exposures found at the end of a window from ones followed forward from when they appeared.

**Verdict: not yet cleared. Four material problems, all about how the summary and one reading interpret correctly transcribed figures, must be resolved, or disagreed with in the note with reasons, before the record is treated as reviewed. Combined disclosure clears.**
