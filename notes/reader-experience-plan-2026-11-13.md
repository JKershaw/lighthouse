title: The reader's site: plan and method for landing it
kind: working plan (at the keeper's request)
date: 2026-11-13

# The reader's site: plan and method for landing it

**In short.** The keeper wants the site to read easily day to day: a reader should find what Lighthouse knows, what is happening now and where to go next, without wading through working material. This plan simplifies the front page and navigation, adds a short daily line of what the watch saw, and closes the gaps the content survey found, in stages, each checked by an editor's visit before and after. Nothing a review checked is reworded; working files stay one click away.

## What the keeper decided, 13 November 2026

- The content survey's five recommendations (notes/content-survey-2026-11-13.md, keeper decisions): "Those are all good recommendations." So: (1) licence CC BY 4.0 for Lighthouse's prose and derived data and MIT for its code, retained third-party material excluded and under its owners' terms; (2) the monthly digest's reported section gets a fresh agent's attribution check before each issue; (3) no DOI for now, stable URLs and a CITATION.cff; (4) unreviewed live counts allowed on a running study's own page, labelled and dated, never on the front page or investigation pages; (5) reader reviews of the early pieces (P-0011) start in December.
- The daily additions: a "what we saw today" line in the Now box (unreviewed, labelled), live counts on running studies' pages (as decision 4), and This week gaining an item most days when something real happened.
- The reader's site below: "Excellent, let's proceed", starting with a mock-up.

## The problem, as measured on 13 November

The live front page at 390 px: about 6,300 px tall, about 1,500 words, 115 links, 19 navigation entries, eleven sections (This week, the lead, Latest with the Now box, Investigations, The watch, Findings, Essays, The map, The longer investigation, What Lighthouse is, Where things are), the PHP piece listed twice, two map entries, and a lead headline of about 25 words. A newcomer needs what we know, what is happening and where to go; a returning reader needs what changed. No single place answers any of these.

## The plan, in stages

**Stage 0, mock-up (next session).** A static mock-up of the new front page and navigation, at phone and desktop width, light and dark, built from today's real content, published to the keeper as a private page for a yes or changes. No site change before the keeper's yes.

**Stage 1, front page and navigation (after the yes; one or two runs).**
- Front page in four blocks: what this is (the existing two lines); what we can say so far (stage 3 fills it; until then the block is omitted, not faked); This week (with the daily line); the four investigations as cards (question, where it stands in one line, latest piece).
- Navigation: Investigations, Findings (pieces and essays together), This week, About; one footer link, "Working files", to a page listing the schedule, programme, proposals, observations, sources, releases, the knowledge map and the operating manual. No page is deleted; URLs stay.
- Remove the duplicates (The watch beside Latest; The map beside the knowledge map; Findings beside Latest).
- A short topic label shown above each piece's full title (from front matter or site/sections.md), so lists scan; titles themselves unchanged.

**Stage 2, one path through the content (runs, from Stage 1).** A "you are here" line on investigation, study and piece pages (front page, investigation, study, piece); a "read next" link at the end of every piece; study pages open with In short then "what happens next". Investigation pages list every running study (the survey's gap: LH030, LH032, LH037 and LH039 on none, LH040 on one) and their counts agree with the front page. Figure labels readable at 390 px.

**Stage 3, what we can say so far (a reviewed piece, about 23 November).** A short, dated answer to the charter's question at current certainty, on the front page and About; evidence review, reader-and-inference review and recheck before it shows.

**Stage 4, the daily layer (from Stage 1).** The run's editor step writes the Now box's "what we saw today" (one or two plain sentences from the day's reads, labelled unreviewed, no figure that is not in a retained read) and keeps This week moving. Live counts on running studies' pages, labelled and dated.

**Stage 5, the survey's remaining gaps (scheduled as rows).** Licence files and CITATION.cff (this week); glossary, corrections and incidents index, data and replay index (this week onward); stale observations.md and programme.md (by 20 November); review rows for LH043 and LH042's reader review (week of 23 November); PHP account's fallback notice if PHP's release has not come by 30 November; monthly digest, first issue 1 to 3 December; "looked and found nothing" piece and the model-found-bugs disclosure piece (December); pieces from LH046 and LH041 (December and January); P-0011 early-piece reader reviews (December); In short openings for the 29 early records (runs, as they pass).

## Method for landing it cleanly

1. **Rows first.** Every stage becomes rows in schedule/due.csv (ids `ux-0-mockup`, `ux-1-front`, `ux-2-paths`, `ux-3-answer`, `ux-4-daily`, and one per Stage 5 item), claimed on main before work starts, as schedule/runner.md step 2 describes. due.csv uses CRLF line endings: write it with `csv.writer(..., lineterminator='\r\n')` and check `git diff --stat` touches only the intended rows; run `python3 schedule/check.py`.
2. **Measure before and after.** Before Stage 1 lands, record the front page's height, words, links and navigation count at 390 and 1280 px (Playwright, preinstalled), and after it the same; the editor's visit reads the site the day before and the day after each stage, with the same reader questions, and its notes say whether it reads easier.
3. **Templates, not prose.** Changes live in site/_includes/*.njk, site/lib/ and site/sections.md. A released piece's words and titles are never changed by this work; anything that would change a reviewed sentence goes through its reviews. Run the site's tests (site/test) and a local build before pushing; check the deployed build by fetching the live page for a string the change adds.
4. **Small commits, fast-forward main.** One stage or part per commit, `git fetch origin main && git merge-base --is-ancestor origin/main HEAD && git push origin HEAD:main`; if main moved (other sessions push too, as on 13 November), merge origin/main, never rebase or force, re-run the check, then push. Commit as Claude with the session's trailers.
5. **Rules that still apply.** No figure in the daily line or the answer box that is not in a retained read or a reviewed record; unreviewed material only in the Now box and study pages, labelled; no internal codes on reader surfaces; British English, no em or en dashes; robots.txt gate for any read; no token or key written to the repository (GitHub's push protection refused one embedded in a kept page on 13 November; withhold such strings from retained bodies before committing).
6. **Reversible.** Each stage is a template change that one revert undoes; the old navigation's pages keep their URLs, so no link breaks.
7. **Record it.** Each stage's commit message says what changed and what it cost; This week gets an item when the new front page lands; the editor's notes keep the before and after.
