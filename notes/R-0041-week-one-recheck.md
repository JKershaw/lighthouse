# R-0041: recheck of the week-one piece after reviews R-0039 and R-0040

30 October 2026. One fresh reading on Opus 5.5 (AGENTS.md step 4) of what the resolutions of the two reviews wrote, before release. Not sent on to another reader.

## What I read

- `git diff 3da4252 HEAD` for articles/a-week-after-two-fixes.md, articles/short/a-week-after-two-fixes.md, articles/a-week-after-two-fixes.svg, studies/LH033/LH033.md, studies/LH034/LH034.md and studies/LH034/scripts/draw_piece_figure.py, sentence by sentence.
- Evidence: studies/LH034/data/tables.json (measure 1 and measure 4, July days 0 to 30), the reviewers' check outputs studies/LH034/review/R-0039_checks.txt and R-0040_checks.txt (as data), studies/LH033/brief.md, studies/LH033/discovery.md (Censys's and W3Techs's own notes), the LH033 checkpoints, the list of retained reads in studies/LH033/data/ (W3Techs is held only in the reads of 25 and 26 October), and articles/php-emergency-first-reading.md for the agencies' advice. Not read: notes/R-0039*, notes/R-0040*, commit messages.
- The whole piece and short form once as a reader, after the changes.
- The figure: re-ran draw_piece_figure.py to a scratch path; the output is byte-identical to the committed SVG, and its day 7 labels (53.9, 72.2, 64.7; 53.0, 52.4, 67.8, 78.8) and the alt text's Python band (55.6 to 59.5) match the data. The diff to the SVG moves two points by 0.1 px and one tooltip from 42.1 to 42.2 (8.3, day 2: 42.15 unrounded), from rounding once; not re-rendered, since nothing visible changed.

## What I found

Checked and holding: every figure in the changed sentences. Node.js day 7 shares 53.9, 72.2, 64.7; all three lines first at half on day 2; line 22 at 48.1 and 49.3 on the weekend (days 3 and 4) then above half again; v26.13.0, dated 28 October, 18.3 per cent of line 26 on day 7. PHP 8.4 and 8.5 at half on day 2, 8.2 and 8.3 on day 6; day 7 shares 53.0, 52.4, 67.8, 78.8. Unfixed lines 11.8 to 16.5 per cent from 14 to 28 October, so "12 to 16" is right. Unknown-version count up 2.72 times on 23 October; 59.5 per cent unknown on day 7. W3Techs 1.9 to 8.3 per cent ("2 to 8"). Python: three of four fixes higher on day 30 than day 7 (starlette not). July: line 26 89.0 (day 7) or 89.4 (posting-aligned day 8), both "89". The unfixed branch sizes ("7.2, 5.6 and 5.2 at about two million each", 2.0 to 2.3 million across the 25 and 29 October snapshots). LH034's daily totals (weekends 11.3 to 16.2 million, weekdays 19.9 to 35.1) and July's day 14 and day 30 points match tables.json. The agencies' advice matches the earlier piece's account of the NCSC and CERT-EU. Censys's "up to about a week for some websites" and the patched definition match its notes as quoted in discovery.md, and the new "not checked" in LH033's Method is in its Limits. The posting-day comparison is labelled post hoc, one comparison, with a statement that nothing can test it. No ranking of the ecosystems, no cause claimed, downloads and services not treated as machines. British English; no em or en dashes in the changed files.

Found:

1. **Title and summaries: "the two daily counts we read".** The piece reads a third count, W3Techs, which updates daily and which we read on 25 and 26 October; it put the fixed releases at 2 to 8 per cent. So "every fixed line and branch had passed half in the two daily counts we read" says we read only two daily counts, and the title's "in the daily counts" could be taken to include W3Techs, where nothing had passed half. The absolute holds only for the two counts followed day by day through day 7 (Node.js's summaries and Censys), which is what the retained reads show. Fixed in the wording.
2. **W3Techs "because".** The piece gave the low W3Techs shares a cause ("because it visits each site about once a month and had not yet looked at most of them"). The record's support is W3Techs's stated visit rate, an inference rather than a measurement. Softened to "most likely because".
3. **LH034, "Line 24 moved more after its first week than in it."** True by net change only (29.4 points from day 0 to 7, 32.0 from day 7 to 30), and the line had touched 46.0 per cent on day 3. Replaced with the numbers. Record only; the piece does not use it.

Noted, not changed: "line 26 ... was lower by the seventh day" is true on both alignments; on posting alignment line 26 was lower on every day, on the brief's from day 3. The wording is not wrong.

## Changes I made

- articles/a-week-after-two-fixes.md, summary: "in the two daily counts we read" became "in the two counts we followed each day".
- articles/a-week-after-two-fixes.md, title: "in the daily counts" became "in the two counts we followed daily".
- articles/a-week-after-two-fixes.md, What this cannot tell us: "because it visits each site about once a month" became "most likely because it visits each site only about once a month".
- articles/short/a-week-after-two-fixes.md, summary: "in the two daily counts we read" became "in the two counts we followed each day".
- studies/LH034/LH034.md, July section: "Line 24 moved more after its first week than in it." became "Line 24 rose 32.0 points from day 7 to day 30, against 29.4 from day 0 to day 7, having touched 46.0 per cent on day 3."

No change to the figure script or SVG.

Must fix before release: none
