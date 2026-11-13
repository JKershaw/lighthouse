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

## The design, after a review of the plan (13 November, agreed by the keeper)

Five principles shape every stage:

1. **Certainty is a visual system.** One small status badge, used identically everywhere: **Reviewed** (passed its reviews), **Provisional** (a record or checkpoint), **Live** (an unreviewed count or the daily line, always dated). The labelling rule becomes a template the site enforces, not prose each run remembers.
2. **The answer leads.** "What we can say so far" is designed now: the preview shows it filled with a draft marked "draft, not yet reviewed", and the reviewed text replaces the draft when it passes (about 23 November). It never reaches main unreviewed.
3. **The investigation page is the unit.** Each investigation is a living page: question, current answer with its badge, what is running, a dated timeline, the pieces. The front page is a short guide to four of them plus this week.
4. **Empty and worst states are designed.** A quiet day says so; a daily line older than two days disappears; the longest title sets the card layout; an investigation with nothing new says when its next read is due.
5. **Reading comfort.** A measure of about 65 characters, a small type scale, one accent, reading time on pieces, and method folded into "How we know" at the end where a piece already has such a section.

## Bloat is a process, so guard against it

The front page reached eleven sections because each run added something reasonable. Two guards keep it from returning:

- **Budgets as tests.** A site test fails the build when the front page exceeds its budget. At 390 px: height about 2,500 px, about 600 words in the main text, about 40 links, five navigation entries. Budgets are recorded in site/budgets.json and measured by site/test/budgets.mjs from the built page.
- **Fixed slots.** The front page has a fixed set of blocks; adding one is a keeper decision, recorded in site/README.md and, at the keeper's next change of the run's instructions, in schedule/runner.md.

## The content model before the templates

Each released piece carries, from data the site already has or from site/sections.md: a topic label, a one-line summary, a status (reviewed, provisional, live), its investigation, and what to read next. A test checks every released piece has them; templates only display them, so later runs fill fields rather than invent layout.

## Measure what readers can find

Before any change, three fresh agents with no context (a newcomer, a journalist, a returning reader) answer four tasks from the built site through a text-only reader's view (scripts/reader_view.py), counting pages opened: What does Lighthouse know? What happened this week? Where would you go to learn about AI cost and spread? Is a given number reviewed? The same tasks run on the preview and after landing. Agents are proxies; the keeper's own two-minute try of the same tasks on the preview is the real test.

## The order

1. **Content model, budget tests and the baseline** (reader tasks and measurements on today's site). Budgets are recorded but not enforced until step 4, since today's page fails them.
2. **Safe path changes, landed on main:** a "you are here" line, a "read next" link at the end of every piece (the investigation's next piece, else the investigation itself), the status badge, and a Working files page with the footer reduced to it.
3. **Front page and investigation pages on the branch**, with the draft answer, built with the real templates and sent to the keeper privately.
4. **After the keeper's yes:** merge to main, enforce the budgets, rerun the reader tasks, the editor's before-and-after visit with side-by-side screenshots at 390 and 1280 px.
5. **The reviewed answer** replaces the draft about 23 November.
6. **The daily layer** (the "what we saw today" line, live counts on study pages) from step 4, written by the run's editor step.
7. **The survey's remaining gaps**, each a row: licence files and CITATION.cff (this week); glossary, corrections and incidents index, data and replay index (this week onward); stale observations.md and programme.md (by 20 November); review rows for LH043 and LH042's reader review (week of 23 November); the PHP account's fallback notice if PHP's release has not come by 30 November; monthly digest, first issue 1 to 3 December; "looked and found nothing" and the model-found-bugs disclosure pieces (December); pieces from LH046 and LH041 (December and January); P-0011 early-piece reader reviews (December); In short openings for the 29 early records (runs, as they pass).

**Revert triggers.** A stage is reverted if a reader task takes more pages after it than before, a budget test fails on main, or the editor's visit finds a broken path.

## Method for landing it cleanly

1. **Rows first.** Every stage becomes rows in schedule/due.csv (ids `ux-1-model`, `ux-2-paths`, `ux-3-preview`, `ux-4-land`, `ux-5-answer`, `ux-6-daily`, and one per survey gap), claimed on main before work starts, as schedule/runner.md step 2 describes. due.csv uses CRLF line endings: write it with `csv.writer(..., lineterminator='\r\n')`, check `git diff --stat` touches only the intended rows, and run `python3 schedule/check.py`.
2. **Measure before and after**, as above, at 390 and 1280 px, with screenshots kept beside the editor's notes.
3. **Templates, not prose.** Changes live in site/_includes/*.njk, site/lib/, site/assets/site.css and site/sections.md. A released piece's words and titles are never changed by this work; anything that would change a reviewed sentence goes through its reviews. Run the site's tests and a local build before pushing; check the deployed build by fetching the live page for a string the change adds.
4. **Small commits, fast-forward main.** One stage or part per commit, `git fetch origin main && git merge-base --is-ancestor origin/main HEAD && git push origin HEAD:main`; if main moved, merge origin/main, never rebase or force, re-run the check, then push. Commit as Claude with the session's trailers.
5. **Rules that still apply.** No figure in the daily line or the answer box that is not in a retained read or a reviewed record; unreviewed material only in the Now box and study pages, labelled; no internal codes on reader surfaces; British English, no em or en dashes; robots.txt gate for any read; no token or key written to the repository.
6. **Reversible.** Each stage is a template change that one revert undoes; every old URL keeps working.
7. **Record it.** Each stage's commit message says what changed and what it cost; This week gets an item when the new front page lands; the editor's notes keep the before and after.
