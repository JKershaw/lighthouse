title: For the driver: the reader fixes of 8 November 2026 (P-0018, P-0019, L-0033 to L-0035)
kind: working note for the driving session
date: 2026-11-08

# For the driver: the reader fixes of 8 November 2026

Done in site/ only, under the keeper's direction of 8 November. No released text was changed; README.md was not touched. Committed to the session branch only, not pushed.

## What changed on the site

- **This week (P-0018, L-0034).** A dated block between the front page's introduction and the lead, read from `site/this-week.md` (new). Each item is one or two plain sentences, labelled **Reported** (others' accounts, attributed and linked) or **Lighthouse** (our own work), with its day. This week's five items, written from the records: the essay of 8 November; the third investigation opened on 8 November; the two briefs fixed on 8 November (WordPress's fixed release, read daily to 21 November; the poisoned LiteLLM release of 21 October, as its maintainers and security firms report it, first count due from 9 November); the map piece of 7 November; and, reported, CISA's listing of WordPress's updater flaw on 3 November (its entry links no attack report, as LH039's brief read it) with WordPress's fix of 28 October. The site drops items dated before the file's `week` and hides the whole block when `updated` is more than eight days before the build. At 390 px it runs to about 400 px above the lead; the editor may trim it.
- **The run line (L-0035).** The Now box's latest-run line is built by the site from schedule/runs.csv and due.csv, so the fix is in the site: it now says what the run finished and, counted apart, what was due at the run and still waits (rows naming the run, still open, whose window had opened by the run's day; rows the run added for later count as neither). For the run of 8 November it reads: finished 4 tasks (the brief for WordPress's fix for its own updater; the brief for the poisoned LiteLLM release; a read for WordPress's fix for its own updater; the investigation page for What AI activity costs the shared internet), 1 still waiting (the record for PHP's mitigation advice in public notices).
- **Codes off reader surfaces (P-0019).** Run-line items and keeper rows read in plain words (kind of work plus the study's short label from site/sections.md, else a proposal's title or the page title without its code), each with its row id in the link's `title` attribute for agents. Study pages and investigation pages show study titles without the leading `LHnnn:` (the investigation page had shown "LH036: LH036: ..."); the code stays in the breadcrumb, the address and a `title` attribute. The study page's file line no longer lowercases the kind ("study lh039, proposals.md p-0017" was a `capitalize` bug). The PHP log line now says "its last read logged at 14:19 UTC that day".
- **Latest (P-0019).** Ordered newest first by the date each piece or essay was published or last corrected, and the page says so above the list. A Later evidence notice or a `revised` item shows beside a piece but no longer lifts it, so the September piece's confirming notice of 3 November no longer sits above the October work.
- **L-0033.** A piece in no investigation that leads a section front now says so in its context box: the map piece reads "Part of the map, in no investigation". It belongs to no investigation (LH035 sits under the map strand in programme.md).
- Tests: 45 pass (`npm test`), including new ones for This week, the plain row names, waiting rows and the Latest rule. Built and checked at 390 and 1280 px, light and dark, front page and /studies/LH040/; nothing broke.

## The runner instruction (for schedule/runner.md)

runner.md says changes to it wait for the keeper; add this only if the keeper's direction of 8 November covers it. Suggested addition to step 7, after "keep the front page current":

> Update `site/this-week.md` as its header comment says: set `updated` to today and `week` to the seven days ending today, drop items from before the week, and add an item for each thing a returning reader should hear about since the last update (a piece or essay released or corrected, an investigation opened or closed, a study begun or answered, a keeper decision that changes what Lighthouse does, an outside event Lighthouse follows), labelled `reported` or `lighthouse`, in plain words with no internal codes. If nothing new happened, still set `updated` and `week`, so the block does not disappear while its items are within the week.

And, for L-0035, a change to step 6's runs.csv line: write `did` starting with the counts in this form, in place of "N due rows": `done N, waiting N (<ids>), added N rows: ...`. Optionally add a last column `plain` to runs.csv's header (`started,by,did,commit,plain`; earlier rows need no change): one plain sentence with no internal codes, which the front page shows in place of `did` when a run finished no row. The site already reads it if present.

## Status lines

- **P-0018:** `Status: done 8 November 2026 (the keeper's direction of 8 November): a dated "This week" block on the front page, read from site/this-week.md, which the scheduled run keeps at its editor's step; items labelled Reported or Lighthouse; hidden when more than eight days stale.`
- **P-0019:** `Status: partly done 8 November 2026: the Now box, study pages and investigation pages show plain names in place of row ids, study codes and proposal numbers (codes kept in title attributes, breadcrumbs and addresses); Latest is ordered newest first by publication or correction and says so. Left: the Schedule, Proposals and Releases pages, and older study pages whose opening falls back to an Answer that cites codes.`
- Leads: `L-0033 resolved 8 November: the map piece says it is part of the map, in no investigation.` `L-0034 resolved 8 November by P-0018's This week block.` `L-0035 resolved 8 November: the run line counts done and waiting apart; runs.csv's did format proposed in site/for-driver.md.`

## A new lead (for proposals.md's leads)

- Older study pages lead with an Answer or Question paragraph that cites other studies' codes, because their records have no **In short.** opening: LH003, LH004, LH005, LH008, LH009, LH013, LH015, LH016, LH017, LH019, LH020, LH025; titles or openings that start with a code: LH000 and LH042's search log; and LH039's lead file's kind line ("working note (study LH039, proposals.md P-0017)"). Adding In short openings to those records (AGENTS.md, Writing) would finish P-0019 on study pages; the site was not made to rewrite record text.

No due.csv rows are needed.
