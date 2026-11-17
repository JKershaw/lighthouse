title: Reader-and-inference review of LH042 record 0.2
kind: review note
version: 1.0
date: 2026-11-17
authors: a review subagent (Claude Code, Opus 5.5) dispatched by the driving session of 17 November 2026, schedule row LH042-reader-review

**In short.** I read LH042's record opening blind, wrote down what a reader would take from it, then read the record, brief, data, investigation page line and the evidence review. The counts and the series hold, and the record is careful about cause, but its opening tells a reader that OpenA2A's OpenClaw category fell from about 267,000 to about 154,000 and came back to about 206,000, without the publisher's own warning that sweeps a few weeks apart on the same queries differ by more than that: its June sweeps ran from 349,424 to 245,111 in total, and the June point is the lowest of the three. That caveat sits in the Answer and the figure, not in the opening or the investigation page, so a reader would believe the exposed population moved, which the evidence cannot show. Two must-fix items block release (that one, and two stale lines saying fixes are still owed that have been made); four suggestions are optional. Verdict: not cleared.

## Exact version reviewed

studies/LH042/LH042.md at repository HEAD 06914fbebc4010f142da98be7b458547552d82d3; the record file's blob is c370810c91e461807b8baeb28c2855072fc50500, last changed in bf814f1 (14 November 2026). Record header: version 0.2, dated 8 November 2026.

## What a reader would believe, written before reading the record

Stage 1 read only the record's header and its **In short.** paragraph (lines 1 to 14), since LH042 has no piece, short form or README "Current focus" section. No note, brief, data file or later section had been opened at this point.

A careful reader would say back: scanners and researchers have published many counts of AI services reachable from the internet (91 counts, 19 publishers), and the counts disagree hugely because they count different things and ask differently; one writer got 1,200 to 30,000 exposed Ollama servers on one day from three queries. The one consistent series since February 2026 is a research group's monthly Shodan-based index, whose OpenClaw category fell from about 267,000 (April) to about 154,000 (late June) and rose again to about 206,000 (1 November).

Observed: publishers' stated counts, checked against their own pages. Explained: the spread between counts is attributed "partly" to different definitions and query methods. Caused: nothing is claimed about why the OpenClaw series moved. A reader may still come away thinking the number of exposed OpenClaw instances fell and then partly recovered, even though the category "need not be OpenClaw itself".

Limits a reader would notice: claims are the publishers', not verified against hosts; reachable is not compromised; Lighthouse scanned nothing; only one series is like-for-like; more reads in December and January. A reader might not notice whether the 267,000 to 154,000 to 206,000 movement could be a change in the index's method or category rather than in exposure, nor how "made one way" was judged. The phrase "Contrary to what our horizon sweep found" implies an earlier internal claim was wrong, without saying what it said.

## Stage 1 inventory

Before writing the section above, this agent had read: the preamble, AGENTS.md, notes/reader-review.md, a file listing of studies/LH042/, a list of note names matching LH042 (names only), the record's section headings, its git log line and lines 1 to 15 of LH042.md. No note's content, the brief, data, investigation page or programme.md had been opened. The driving session can check this against the transcript.

## What I read in stage 2

studies/LH042/LH042.md (whole), for-driver.md, brief.md (opening and amendment headings), data/series_changes.txt, data/index_reads.csv, data/counts.csv (OpenA2A rows, C14, May to July rows), data/table.md (C14), data/SCREENING.md, the retained OpenA2A bodies data/round3-2026-11-08/004.body (sweep archive) and 005.body (methodology) and data/round4-2026-11-08/001.body (index), as text through scripts/totext.py; figure.svg rendered in light and dark; investigations/ai-cost-and-spread.md lines 32 and 81; programme.md line 91; schedule rows for LH042; then notes/R-0058-lh042-evidence.md. No host was visited or queried; nothing was fetched from the network.

## What the round establishes

- 91 admitted counts, 19 publishers, 57 series, six with two or more dates (data/series_changes.txt), as the opening says.
- Counts after February 2026 exist for Ollama and OpenClaw; the earlier "no count since February" did not hold.
- On one day one writer got about 1,165, 25,488 and 30,000 Ollama hosts from three queries (C17 to C19): method alone moves the number by a factor of more than twenty.
- OpenA2A's index lists nine monthly points; these are the publisher's figures, faithfully transcribed (index_reads.csv matches counts.csv).
- What it does not establish: any change in how many AI services are exposed. Every dated series is an index's or a sweep's count, and the one long run since February is noisier within a month than between months by its publisher's account.

## Material claim problems

**M1 (must-fix). The opening and the investigation page give the OpenClaw category's fall and recovery without the within-month variation that is as large.**
- Passage: LH042.md, In short: "whose OpenClaw category (which it says need not be OpenClaw itself) fell from about 267,000 in April to about 154,000 in late June and stood near 206,000 on 1 November." investigations/ai-cost-and-spread.md line 81: "(OpenClaw-family category 267,172 on 11 April, 153,638 on 26 June, 205,872 on 1 November 2026)".
- Evidence: OpenA2A's methodology (data/round3-2026-11-08/005.body) says the range within a month "can be wider than the change between months", and that three June sweeps "on the same query set" returned 349,424 (1 June), 320,506 (14 June) and 245,111 (26 June) exposed services in total. data/index_reads.csv: the plotted June point is the lowest of June's three (range 245,111 to 349,424, a spread of 104,313), and the plotted April point is the higher of April's two (313,900 to 321,929). The April to June OpenClaw fall is 113,534, about the size of June's within-month spread of totals, and the OpenClaw category is most of each total (from 63 per cent on 26 June to 83 per cent on 11 April in the listed sweeps). The index does not give per-category ranges, so the June 1 and June 14 OpenClaw figures are unknown to this record. The record's Answer carries OpenA2A's caveat ("a month-to-month step in its index is not by itself a change in the population") and so does the figure's footnote; the opening and the investigation page, which the site leads with, do not.
- What a reader would believe (stage 1 above): that the exposed OpenClaw-like population fell by about two fifths and partly recovered. The evidence supports only that the latest sweep of each month gave those figures.
- Proposed resolution: in the opening, after the three figures, add OpenA2A's own caveat with its numbers, for example: "though OpenA2A says sweeps weeks apart can differ by more than months do: its three June sweeps on the same queries totalled 349,424, 320,506 and 245,111, and the June point is the last and lowest." Carry the same clause, and the corrected label "OpenClaw category" (OpenA2A's "OpenClaw gateways", which it says need not be OpenClaw) in place of "OpenClaw-family category", into the investigation page's line 81. The Answer's "How the long series moved" could say the same of the April point (the higher of two sweeps). R-0058 offered the June clause as an optional suggestion; given how the opening reads, I think it is a claim problem.

**M2 (must-fix, small). The record says two fixes are still owed that have been made.**
- Passage: LH042.md, Next: "two of its must-fix items are outside the record (C14's method in data/counts.csv, and the key's copy in the Synthient body) and are listed under Corrections"; Corrections: "that file, and data/table.md built from it, are outside the reviewer's paths and are to be corrected by the record's owner" and "Withholding it there, and logging that in data/SCREENING.md, is for the record's owner".
- Evidence: data/counts.csv C14 now gives the method as "re-ran Cisco Talos's September 2025 Shodan query, which the page does not give" and fingerprint "not stated", and data/table.md row C14 matches; data/SCREENING.md, section "A second copy of the quoted key", logs the URL-encoded copy withheld at about 20:45 UTC on 8 November with hashes.
- Proposed resolution: a dated line in Corrections and Next saying both were done, by whom and when (SCREENING.md gives the key's time; the C14 edit's time from git if it can be found, otherwise say it is done at this version), and update Limits' "No reader-and-inference review yet" to name this note.

No other material problem. The record does not read a share as a rate, does not join publishers or methods, labels its post hoc readings, and says throughout that reachable is not compromised and that nothing was scanned. The "partly because they count different things" is supported only for the method part, which the same-day case shows; that is now stated.

## Suggested (optional)

1. Limits: "its index restates earlier months on current categories" is the record's inference from one value (March's LLM-endpoint 23,086 against the March report's port count), and OpenA2A says "No previously published figure has been restated onto the newer definition" (of 18 June). Label it as interpretation and quote OpenA2A, as R-0058 also suggested; it was not done.
2. Answer: "its totals split in two at the method boundary OpenA2A dates to 18 June 2026" could add that OpenA2A puts the difference at one to four detections in about 300,000 (005.body), so a reader does not take the split for a large break; the split itself follows the brief and is right.
3. The opening's "Contrary to what our horizon sweep found" names an internal process and leaves the reader to guess what it found; "Contrary to an earlier search of ours, which found no count after February," says it in plain words.
4. Figure: its version line still says "LH042 version 0.1" and its first panel "OpenClaw-family panels"; the record is 0.2 and calls the category OpenA2A's OpenClaw category. Both themes render legibly; the footnote on within-month sweeps is good and should stay.

## Next step

Adjust, then continue. The December and January index reads, as fixed, add two more latest-sweep points, which cannot by themselves tell a change in the indexed population from sweep-to-sweep variation, because the index publishes a within-month range only for totals and plots the latest sweep. Before the December read (3 to 7 December), an amendment could fix, in advance: retaining each month's sweep count and total range beside the plotted points (index_reads.csv already does this), reading per-category figures for every sweep where OpenA2A's sweep reports give them (robots permitting, within the request ceiling), and describing a month-to-month category step as not distinguishable from sweep variation when it is smaller than that month's stated total range. Locating the Ollama paper's data release, already in Next, is the only route to a daily series made one way and is worth keeping. Waiting is otherwise right: no other evidence available now would separate exposure change from index behaviour.

## Verdict

Not cleared. M1 and M2 must be resolved, then one fresh recheck of what the resolution writes, before release or public use beyond the current investigation-page line. Exact version reviewed: HEAD 06914fbebc4010f142da98be7b458547552d82d3, LH042.md blob c370810c91e461807b8baeb28c2855072fc50500 (record 0.2). This review is a contribution from a fresh agent on the same model family, not independent confirmation.
