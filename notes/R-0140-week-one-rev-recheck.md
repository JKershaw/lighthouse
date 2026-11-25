title: Recheck of what the two review resolutions wrote into the week-one revision (version 2.0 draft)
kind: review note (single fresh reading, schedule row piece-week-one-rev-recheck)
date: 2026-11-25
reviewer: a fresh review subagent of the driving session of 25 November 2026 (Claude Code, Opus 5.5 as reported by the harness, not independently checked); one reading, not independent confirmation

# Recheck: "A month after two fixes" (version 2.0 draft)

**In short.** I read once every passage the resolutions of the evidence review (R-0138) and the reader review (R-0139) wrote into the draft, its short form and the one-off note, and checked each against the retained records and bodies. Most hold. Four needed small edits: the short form's summary gave PHP's late-rise explanation without its "three branches", one sentence said a comparison would settle the Node.js assumption when it couldn't, the Apigee sentence dated the bulletin's wording to a day we never read it, and the one-off note made for the dependency updates the same slip it had just corrected for one CVE. Verdict: **cleared**.

## What was checked

Commit checked: 28e4376 (`git log -1 --format=%h`), the diff from dd624a3 to it (identical to the scratchpad resolution.diff), covering articles/drafts/a-week-after-two-fixes-rev.md, a-week-after-two-fixes-rev-short.md and studies/LH034/oneoff-2026-11-25/note.md. Against: studies/LH033/LH033.md (1.2), data/record_v1.json (`m1_counts`), review/R-0139_not_patched.txt; studies/LH034/LH034.md (1.1); the three kept bodies in studies/LH034/oneoff-2026-11-25/ (decompressed in memory with `python3 -I`, nothing run); LH037's retained GCP-2026-072 bodies of 2 and 23 November. No web request. Calculation below was run inline from record_v1.json and is reproduced here as its output.

PHP decomposition of the day-14 to day-30 share rise (from `m1_counts`; points of share if only the branch count had changed, or only the patched count):

```
8.2 73.4 -> 78.2  rise 4.72  denominator only 3.80  numerator only 0.88
8.3 70.4 -> 75.0  rise 4.60  denominator only 3.98  numerator only 0.58
8.4 81.0 -> 86.5  rise 5.47  denominator only -3.21 numerator only 9.03
8.5 89.7 -> 92.2  rise 2.51  denominator only 1.97  numerator only 0.52
```

## Changed passages and verdicts

1. **Short form summary, PHP and Node.js late rise** ("fewer PHP services counted, nearly all of them ones not counted patched, rather than more patched, and from more Node.js downloads of newer versions rather than fewer below the fix"). The PHP half holds for 8.2, 8.3 and 8.5 (above; in each, services not counted patched fell by more than the branch shrank, so on net every service lost was a not-patched one, and "nearly all" is the cautious form of that net reading). In 8.4 the rise was more patched services and the branch grew. The summary, read without the body, stated it of PHP as a whole. **Changed** (added "in three branches"). The Node.js half matches LH034 Findings (81, 70 and 77 per cent of the rise on the means goes with added downloads).
2. **Short form, "(their own announcements, read once afterwards and not yet reviewed, don't say)"**. Holds; the kept bodies mention neither October nor v22.23.4, v24.22.1 or v26.12.1.
3. **Short form, distribution caveat**; full summary, same caveat. Holds; it is the body's own and Censys's stated limit.
4. **Full summary, "a rule chosen after the counts were seen that assumes, unchecked, that they carry October's fix"**. Holds (LH034 Answer).
5. **Revision line** (fewer PHP services counted in three branches, nearly all not counted patched; more Node.js downloads at or above the fix rather than fewer below it). Holds, as 1, with the branch qualifier already present.
6. **"the one counting rule the study added after seeing outcomes, and it assumes, without checking..."**. Holds (LH034: "one post hoc rule").
7. **"Setting October's list of flaws against what the November releases contain would settle that"**. Release notes list changes since the previous release, so October's flaws would be absent from them whether or not the fix was carried; the one-off note says the comparison isn't possible from what is retained either way. Stated more surely than the evidence supports. **Changed.**
8. **"on an average day ... 18.4, 12.9 and 25.8 per cent higher ... 4.0, 5.1 and 6.5 per cent lower"; "one of three ways the study split the days, all chosen then; collection has closed, so nothing will test it on fresh data"**. Holds (LH034 Findings: per-day means, "three pairs of day windows").
9. **Crossing with Python, "a reading made after the counts were seen that the studies didn't test, and now can't, since collection has closed"**. Holds for the Censys and nodejs.org counts it rests on. (LH033 still reads W3Techs once on 1 December, row LH033-w3techs-dec; that is a survey of websites and doesn't bear on the crossing or the predictions. The unchanged sentence "This is where the two studies stop collecting" is close to that window; the release round may want "stop collecting these counts". Not changed here.)
10. **Apigee, "no packaged fix was available when it wrote, on 24 October"**. The quoted wording is verbatim in both retained bodies, and GCP-2026-072 carries "Published: 2026-10-24" with no update line. But the earliest retained copy is of 2 November and the page then read "Last updated 2026-10-26 UTC", so the text on 24 October itself was never read. **Changed** to date the statement by our reads.
11. **W3Techs "on 25 and 26 October"**. Holds (LH033 measure 4: 1.9 to 5.9 on 25 October, 2.8 to 8.3 on 26 October).
12. **Predictions, "With collection closed, no later count from these studies will test them further."** Holds (as 9).
13. **One-off note, "In short" and "Not settled" ("whether they name any of October's flaws can't be checked")**. Holds.
14. **One-off note, v24.22.3 and v26.13.1 lines.** The CVE sets hold: 14 distinct identifiers in v22.23.5, 15 identical in v24.22.3 and v26.13.1, the extra one CVE-2026-126051. But the v26.13.1 line still gave "updates to brotli and undici" as if v24.22.3 lacked them; the kept v24.22.3 body updates brotli (1.2.1) and undici (7.30.2) as well as llhttp (9.4.4) and sqlite (3.54.1), and v26.13.1 has the same except undici 8.12.4. **Changed.**

No figure in the changed passages fails to match. No new post hoc reading is unlabelled. No em or en dash was added.

## Changes I made

- articles/drafts/a-week-after-two-fixes-rev-short.md, summary: "came mostly from fewer PHP services counted, nearly all of them ones not counted patched," became "came mostly from fewer PHP services counted in three branches, nearly all of them ones not counted patched,".
- articles/drafts/a-week-after-two-fixes-rev.md, Node.js paragraph: "Setting October's list of flaws against what the November releases contain would settle that; nothing now scheduled will do it." became "Only a source that says whether the November releases carry October's fixes would settle that; none we read does, and nothing now scheduled will look."
- articles/drafts/a-week-after-two-fixes-rev.md, Apigee paragraph: "no packaged fix was available when it wrote, on 24 October." became "no packaged fix was available, as the bulletin still said when we last read it, on 23 November."
- studies/LH034/oneoff-2026-11-25/note.md, v24.22.3 line: "...High): 15 distinct CVE identifiers." became "...High): 15 distinct CVE identifiers; the same llhttp and sqlite updates, plus updates to brotli (1.2.1) and undici (7.30.2)."
- studies/LH034/oneoff-2026-11-25/note.md, v26.13.1 line: "...CVE-2026-126051 among them, and updates to brotli and undici." became "...CVE-2026-126051 among them, and the same dependency updates, except undici to 8.12.4."

These changes are not sent to another reader.

## Disclosure

Combined disclosure stop (schedule/research-safety.md), applied to the version that will ship with these edits: **clears.** Aggregate public counts, public advisories and release notes with their public CVE identifiers; no hosts, accounts, people or mechanism detail; the edits add nothing beyond retained public text.

## Verdict

**Cleared.** Nothing that must be fixed remains in what the resolutions wrote. Release-time work already named elsewhere stands (R-0138 should-fix 6 and 7: programme.md and the investigation page aligned with the weaker reading of test A, the essay's Correction notice; links, figure path, revision date and colophon set at release).
