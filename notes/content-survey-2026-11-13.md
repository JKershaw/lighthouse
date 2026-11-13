title: What Lighthouse publishes, what is missing, and when the gaps can close
kind: working note (editorial survey, at the keeper's request)
date: 2026-11-13

# What Lighthouse publishes, what is missing, and when the gaps can close

**In short.** The keeper asked for a survey of everything a reader can reach, the gaps in it, and how and when each could close. Most released writing comes from the first investigation and is still sound, but two of the four investigations have no reviewed piece at all and a third has only essays, several reviewed records have nothing a reader would meet, and no page says plainly what the watch can tell so far about AI activity sustaining itself. Many gaps are small fixes a scheduled run can make this week. The rest are reviewed pieces, which the existing schedule already crowds into late November and early December, and a few choices, such as a licence, that only the keeper can make.

Surveyed by a subagent on Opus 5.5 at commit 33a9822, from the repository only (the live site was not read). Every count below was taken from the files on 13 November 2026; where a count could not be made it says so. Costs are at list rates, from notes/reader-review.md, the editor's notes and proposals.md's spend lines; a figure marked "estimate" is this survey's, not a measurement.

## 1. Inventory

### By content type

| Type | Count | Where, and state |
| --- | --- | --- |
| Released pieces (full) | 18 | articles/*.md. 15 in the software-updates investigation; 3 outside any (the xz backdoor, What we can see, the layer map piece). Newest: the layer map piece, 7 November (1.1 on 9 November). |
| Short forms | 17 | articles/short/; every full piece has one except where-a-software-update-went. |
| Essays | 3 | essays/: Seen from outside, seen from inside (1.0, 30 October); It was only a test (1.1, 8 November); What the watch would see (1.0, 8 November). |
| Drafts | 1 | articles/drafts/reading-one-trace.md, a side-notes demonstration, "no release scheduled". |
| Knowledge map | 1 | map/knowledge-lineage/ (three pages), version 1, 11 November; graph asserted 10 November over 49 records and 21 publications. |
| Release lines | 33 | releases.md, 26 September to 11 November. |
| Study directories | 51 | studies/LH000, LH002 to LH051. LH001, the Harbour calibration the charter calls the standard candle, was never opened (programme.md still describes it). |
| Records (LHnnn.md) | 41 | All at version 0.1 to 0.4; none has reached 1.0. 12 open with an **In short.** paragraph (LH030 to LH035, LH040 to LH043, LH046, LH047); 29 (LH000 to LH029) do not, against AGENTS.md's rule of 7 November. |
| Brief only | 10 | LH036, LH037, LH038, LH039, LH044, LH045, LH048, LH049, LH050, LH051; all ten briefs open with In short; six have checkpoints. |
| Review notes | 68 | notes/R-0001 to R-0068. |
| Investigation pages | 4 | investigations/: software updates (from 26 September), model-found bugs (1 November), AI cost and spread (8 November), physical authority (12 November). |
| Site pages | about 20 | About, charter, design, sources, programme, proposals, releases, observations, schedule, follow (with an Atom feed), offline reading, notes and studies indexes, four section fronts (watch, findings, essays, map), the map's three pages, This week and the Now box on the front page. |
| Working logs a reader reaches | 4 kinds | notes/php-watch-log.md (173 lines), notes/physical-authority-watch-log.md, 8 editor's notes, 4 horizon sweep files; all unreviewed and labelled so. |
| Figures | 38 | 18 in articles/, 3 in essays/, 17 in studies/ (16 studies). Every article SVG carries a title element. |
| Replay commands | 12 | replay.sh in LH010 to LH017, LH041, LH042, LH046 and LH047. No index of them. |
| Data | studies/ holds 5,884 files, 341 MB | studies/*/data; served by the site only as GitHub folder links (site/eleventy.config.js passes through images, not data; L-0102). |
| Licence | none | No LICENSE file; About names none (L-0101). |

### Released pieces with versions and dates

| Piece | Current version | Released, last changed |
| --- | --- | --- |
| Where a software update went | 1.0 | 26 Sep |
| The xz backdoor | 1.0 | 26 Sep |
| What we can see | 1.1 | 26 Sep; later evidence 9 Nov |
| What a download shows | 1.0 | 26 Sep; later evidence 28 Sep |
| What an image holds | 1.0 | 26 Sep |
| What moves a pin | 1.0 | 26 Sep; later evidence 27 Sep |
| Pins move over weeks | 1.0 | 27 Sep |
| Fixes that said so | 1.0 | 27 Sep; later evidence 27 Sep |
| The lead was a few libraries | 1.1 | 27 Sep |
| Where software updates go (the synthesis) | 1.0 with six notices | 27 Sep; last notice 3 Nov |
| Two days for most | 1.2 | 28 Sep; 29 Sep |
| Old versions, new Pythons | 1.3 | 29 Sep; 3 Nov |
| Rarer further down | 1.0 | 29 Sep |
| Recipes follow the pin | 1.0 | 29 Sep |
| Tests read the lockfile | 1.0 | 30 Sep |
| A PHP emergency (the dated account) | 1.3 | 22 Oct; 30 Oct |
| A week after two fixes | 1.0 | 30 Oct |
| Every layer of the internet had a public watcher | 1.1 | 7 Nov; 9 Nov |

Eleven of these were released before 29 September, when the reader-and-inference review began, and P-0011 says the early pieces never had it; some were re-read in later rounds (two days for most at 1.2), and nobody has yet listed which still need it.

### Per investigation: what a reader can reach, and what is only in working files

- **Where does a software update go?** Reader-facing: the synthesis and 14 more pieces, one essay, the investigation page with a reading order. The PHP and Node.js watch is reachable through the dated account, the week-one piece and the daily log. Only in working files: LH030 (PHP's mitigation advice, 0.2), LH032 (the Dutch NCSC list, 0.1) and LH037 (vendors that ship PHP, brief and checkpoints), none linked from any investigation page; LH039 (WordPress's updater fix) and LH040 (the poisoned LiteLLM release, 0.1, unreviewed) are linked from no investigation page and mentioned on none; LH013's installer stage; the day-14 PHP and Node.js figures (log only, L-0028; overtaken by the day-30 rows). The page's front matter lists 25 studies, so LH013, LH031, LH033, LH034 and LH046, which its text links, do not count on the front page.
- **When a model finds the bug.** Reader-facing: the investigation page only. Only in working files: LH036's five checkpoints, LH048's two, LH038's brief. No record yet; the first, LH036-interim, is due 16 to 20 November.
- **What AI activity costs the shared internet.** Reader-facing: the investigation page (with lines from reviewed records) and two essays. Only in working files, though reviewed: LH041 (registry worms, 0.3, evidence and reader reviews and a recheck), LH046 (GH Archive coverage, 0.3, reviewed; reached readers only as notices on two older pieces and lines on two investigation pages), LH047 (the rules of the road, 0.3, reviewed). Evidence review only: LH042 (exposed AI services, 0.2; its reader review is folded into LH042-record, January). Unreviewed: LH043 (agents in public, closed), LH044 and LH045 (baselines), LH051 (from today). The page has no `studies:` front matter, so the front page's investigation card shows no study count for it at all (site/lib/front.js counts that field).
- **When AI acquires physical authority.** Reader-facing: the investigation page and This week. Only in working files: LH050's baseline (unreviewed), the commissioning record, the supplied essay (marked context, not an account). The pilot allows at most two released pieces.

## 2. Gaps

Each gap gives: how to close it; who decides (**run**: a scheduled or driving run can do it now; **reviewed**: needs a piece through evidence review, reader-and-inference review and a recheck; **keeper**); the earliest realistic date; rough cost; and what row or proposal already covers it.

The load to plan around: 178 rows are open in schedule/due.csv, 107 of them starting by 30 November (51 in the next seven days) and 50 in December. Reviewed releases already scheduled between 19 November and 11 December: the PHP account revision (php-account-rev, open-ended from 19 November), the robots.txt paper (LH047-paper-draft by 30 November, reviews by 7 December), the week-one revision and the first essay's revision (25 November to 6 December), the first armed-robot reader account (LH050-reader-draft 26 November to 4 December, reviews 5 to 11 December), plus record reviews for LH049, LH050 and LH051. A new reviewed piece fits best from 8 December, unless it is small.

Cost basis: a reader-and-inference review with its recheck has cost $0.70 to $1.72 on Opus 5.5 in the logged rounds of 27 October to 9 November (notes/reader-review.md); an editor's reader $0.67 to $1.00; a scheduled run's driver $1.75 to $3.09. A whole piece round (writer, evidence review, reader review, recheck) has not been priced as a whole: estimate $5 to $15.

### (a) Reader formats missing

1. **No explainer that stands apart from a study.** Words such as GH Archive, a download count, a pin, a lockfile, CISA's catalogue, EPSS and robots.txt are explained inside pieces, and a newcomer meets them first on the front page and study pages (L-0051 asks for a glossary). Close: a glossary page (a run, from definitions already in released pieces, no new claims), then two or three short explainers treated like essays (a citation check, the reader-and-inference review and a recheck): "What a download count counts", "What GH Archive is, and what is missing from it" (after LH046-recheck, 7 to 14 December), "What CISA's exploited list does and does not say". Who: glossary run; explainers reviewed. When: glossary by 20 November; first explainer 8 to 18 December. Cost: glossary under $3; each explainer estimate $4 to $8. Exists: L-0051 only.
2. **No "looked and found nothing" piece.** Several studies stopped at an honest nothing that readers never see: LH043 (every account of the evaluation agents' July actions anonymised what they touched, so there was nothing to look up), LH027 (The National Archives' notice refused us), LH013's installer stage (no free public source carries the installer's version), LH048 at baseline (none of the four followable flaws in CISA's catalogue), and the robots.txt rule's cost to each study (L-0052). Close: one reviewed piece, "Where we looked and found nothing we could use", built from LH043 (after its record has an evidence review) and L-0052's list, saying a missing reading is not a negative. Who: reviewed. When: LH043 evidence review in the week of 23 November; piece 8 to 18 December. Cost: estimate $6 to $12. Exists: L-0052; no row.
3. **No lasting digest.** This week shows at most six items and drops anything older than seven days (site/this-week.md, rules 2 and 5), so a reader away for a fortnight loses the thread, and the release history is only releases.md's dense lines. Close: a monthly page (notes/month/2026-11.md or a site section) assembled on the first days of each month from This week's items as they stood, releases.md and keeper decisions, under This week's own rules (links and figures only from released pieces or the cited source; reported items labelled). Who: keeper decides whether it needs review (decision 2 below); a run builds it. When: first issue 1 to 3 December, for November. Cost: under $3 a month. Exists: nothing; P-0018 (This week) is the nearest.
4. **No retrospective of corrections and incidents.** Corrections live in each colophon and in releases.md; the incidents (the half-read robots.txt, notes/incidents/2026-11-08-robots-partial-read/; LH047's audit counting 113 requests that broke a rule as its brief fixed it; the essay's dated correction, notes/R-0053; the PHP image deployment glitch; LH016's study of which reviews changed claims) are spread across notes. The site's feed already knows "Correction" and "Later evidence" kinds (site/lib/feed.js). Close: first a generated corrections index (every Correction and Later evidence notice, dated, linked), which a run can build from the notices; then, separately, a reviewed piece looking back over seven weeks of errors and what each changed. Who: index run; piece reviewed. When: index by 20 November; piece after the robots.txt paper, which covers the audit, so January. Cost: index under $3; piece estimate $6 to $12. Exists: nothing.
5. **No live view of a running watch.** The Now box names watches and the study pages list checkpoints, but nothing shows a series as it accumulates (LH033's figure is redrawn at each read inside the study directory; LH044 reads weekly to 7 February; LH049 and LH051 count daily or hourly). Unreviewed material is allowed only in the Now box, labelled (notes/editor/plan.md). Close: on a study page, not the front page, a dated, labelled-unreviewed chart or table of counts per read, drawn by the study's own script, with no interpretation. Who: keeper (it extends where unreviewed numbers may appear; decision 4). When: from the week of 23 November if agreed. Cost: a run per study, under $3 each. Exists: L-0071 (findings in the Now box) overlaps.
6. **No "reported" roundup beyond This week.** Outside events the sweeps and the log record (for example D-Link's statement, F5's report of scanning before publication, IETF 127) reach readers only as This week items for seven days or inside the log. Close: a "Reported" section in the monthly digest (gap 3), under This week's rules: whose account, linked, no figure beyond the source, no claim of harm or compromise in our voice. Who: keeper sets the review rule (decision 2). When: with the first digest, 1 to 3 December. Cost: included in gap 3. Exists: This week's `reported` label.
7. **No page for citing or for a returning reader** (L-0074): who runs Lighthouse, who the keeper is, and how to cite a piece or a record. Close: a short "Using and citing Lighthouse" page with a CITATION.cff, once the licence is chosen. Who: run, after decision 1. When: within two days of the decision. Cost: under $3. Exists: L-0074.

Interviews and outreach are excluded by the keeper's rule of 1 November and are not proposed.

### (b) Coverage

8. **The charter's question has no plain, current, dated answer a reader meets.** The nearest is one line mid-page on investigations/ai-cost-and-spread.md ("No report read so far describes AI activity sustaining itself outside a lab") and that page's "nothing below is evidence of AI activity sustaining or spreading itself". The front page and About say only that nobody yet knows. The editor's sceptic of 12 November wanted any finding about AI activity on the open internet and found only the investigation page's "none yet". Close: a short dated "What we can say so far" box on the front page and About, drafted from the investigation pages' own words, each strand (load, exposure, spread run by people, lab capability, activity on the open internet) with its status, reviewed like an essay, and updated whenever an investigation's account changes. Who: reviewed; the front-page placement is editorial (the editor's plan makes the front page ordinary work). When: draft 16 to 18 November, reviews 19 to 22 November, live about 23 November. Cost: estimate $4 to $8. Exists: L-0049.
9. **Model-found bugs has no record and no piece.** Its question is the closest to the charter of the three outward investigations, and readers have only the page. Close: as scheduled, LH036-interim (16 to 20 November) and LH038-record (18 to 30 November); then a reviewed short piece on the disclosure timeline once LH038's record is reviewed, rather than waiting for LH036's stop in January. Who: reviewed. When: piece 8 to 20 December. Cost: estimate $6 to $12. Exists: rows LH036-interim, LH038-record, LH036-record (January); no piece row. Also L-0031 (the page's first-report date sits at its foot) is still open.
10. **Reviewed records in the cost investigation with no reader piece.** LH041 (worm waves, 0.3) and LH046 (GH Archive gaps, 0.3) passed both reviews and a recheck; LH047 (0.3) has its paper scheduled. Close: LH047 as scheduled; a piece on GH Archive's missing events after LH046-recheck (7 to 14 December), which could double as the explainer in gap 1; a piece on the worm waves after LH041-record 1.0 (7 to 31 December). Who: reviewed. When: GH Archive piece 15 to 23 December; worms January. Cost: estimate $6 to $12 each. Exists: LH047-paper-draft and LH047-paper-reviews; LH046-recheck and LH041-record (records only); no piece rows.
11. **Studies linked from no investigation page.** LH030, LH032, LH037, LH039 (WordPress) and LH040 (the poisoned LiteLLM release) appear on no investigation page; LH039 and LH040 are proposals the gate started (P-0017, P-0015) and are labelled for the Now box in site/sections.md, so a reader can reach a study page with no investigation around it. Close: a line each under "Beside it" or the relevant question, from each brief's In short, labelled by status; add all running studies to each page's `studies:` front matter (also fixes gap 17). Who: run. When: 14 or 15 November. Cost: under $3. Exists: none.
12. **Records unreviewed for long, or not at all.** LH040 (0.1, unreviewed since 10 November; record 1.0 and reviews 24 November to 4 December), LH043 (0.1, unreviewed since 8 November, closed, no review row), LH032 (0.1 since 23 October; record 1 to 7 December), LH030 (0.2 since 31 October; LH030-record due now, window to 4 December), LH042 (reader review deferred to January although proposals.md's For the next review said reader reviews of LH041, LH042 and LH046 would be rows by 16 November: there is no LH042 reader row). Close: add rows for LH043's evidence review (it closed; a review would let gap 2 use it) and an LH042 reader review now rather than in January. Who: run adds rows; reviews by fresh agents. When: LH043 and LH042 reviews in the week of 23 November. Cost: $1 to $3 each. Exists: LH040-record, LH032-record, LH030-record, LH042-record; none for LH043 or an early LH042 reader review.
13. **A released piece later evidence has overtaken without a notice.** The PHP account (1.3, 30 October) does not yet carry F5's report of scanning before publication (flagged 9 November), D-Link's statement of 10 November (in This week and the log), or the vendor panel's reclassing of D-Link (notes/R-0068); and its revision row php-account-rev waits for PHP's next regular release, which PHP has not dated (the row's 19 November is a cadence inference). Close: give php-account-rev a fallback: if PHP has not released by 24 November, release a dated "Later evidence" notice for what has accumulated, with the reviews, and keep the PHP-release revision as its own later round. Who: reviewed. When: 24 to 30 November. Cost: $2 to $4 (comparable notice rounds' reader stage and recheck cost $1.11 to $1.72). Exists: php-account-rev; the fallback is new.
14. **Four sentences a sceptic questioned, with only two homes.** L-0078: the layer piece's title ("none saw the whole of its layer", against certificate transparency logs anyone can query) and its thinning counts from two noon hours, one on New Year's Day; the week-one piece's "the real share protected is at least that"; the PHP account's "a documented account of AI helping defenders". The second two fold into piece-week-one-rev and php-account-rev; the layer piece has no revision row. Close: a row for a reviewed 1.2 of the layer piece in December. Who: reviewed. When: 8 to 18 December. Cost: $2 to $4. Exists: L-0078; rows for two of the four.
15. **Early pieces without a reader-and-inference review.** Up to eleven, released before 29 September. Close: list which were never re-read in a later round, then review one at a time, starting with the synthesis and the pieces it leans on most (what-a-download-shows, the-lead-was-a-few-libraries). Who: reviewed; a run dispatches. When: two a week from 8 December, done by about 15 January. Cost: $1 to $2 each, $11 to $22 in all at most. Exists: P-0011 (backlog).
16. **The programme's founding calibration is unmentioned since September.** programme.md still describes LH001 and says the first collection "will hold LH001"; no study was opened. Close: either schedule it or write in programme.md's Next that it rests and why. Who: run (a programme choice is the session's under AGENTS.md); a new study start would count against the throttle. When: a sentence by 20 November. Cost: negligible. Exists: none.

### (c) Currency and consistency

17. **Counts that disagree.** The front page counts studies from each investigation's `studies:` field: software updates shows 25 (its text links LH013, LH031, LH033, LH034 and LH046 too), cost and spread shows none (eight studies running); the knowledge map counted 30 records and 19 pieces for software updates (L-0079); the investigations index drops the counts the front page shows (L-0103); releases.md's "all 49 study records" was true on 11 November and there are now 51 directories. Close: front matter fixed (gap 11); the map's refresh picks up the rest; L-0079 asks for names to match between front page and map. Who: run. When: 14 to 15 November. Cost: under $3. Exists: L-0079, L-0103.
18. **observations.md stops at the first PHP trail (22 October).** README and About call it "every reading so far", but its 17 rows end with the first PHP trail; the Node.js counts, Censys's tally, the instrument map, the worm records, GH Archive coverage, the closing web, the robots.txt audit and the armed-robot baseline are absent. Close: add a row per reading since, each with whose instrument and when, labelled unreviewed where it is. Who: run. When: by 20 November. Cost: $2 to $4 (one subagent). Exists: none.
19. **programme.md's header and Answered list are stale.** The header says "revised 30 September 2026 (last: LH017)"; Answered ends at LH013 and holds no entry for LH035 (released), LH041, LH046 or LH047 (reviewed), against AGENTS.md's consistency rule. "Questions after these" still says LH013 waits. Close: Answered entries at each record's own certainty, header redated. Who: run (a record's reviewed Answer can be restated; the release review normally checks agreement, so have a fresh agent read the new entries once). When: by 20 November. Cost: $2 to $4. Exists: none.
20. **The front page body and About lag the investigations.** README.md's "The longer investigation" is the 30 September account; About's "What it looks at" names only software records and inward instruments, not the cost, model-found bugs or physical-authority investigations. Close: a paragraph each, pointing to the investigation pages rather than restating figures. Who: run (editorial). When: by 20 November. Cost: under $3. Exists: none.
21. **Twenty-nine records without an In short opening.** LH000 to LH029; the site falls back to their Answer, and L-0036 lists twelve whose fallback cites other studies' codes. LH000's title starts with a code. Close: one subagent writes the 29 openings from each record's own Answer, no new claims. Who: run. When: 14 to 20 November. Cost: estimate $3 to $6. Exists: L-0036.
22. **Editor's leads still open.** From L-0049 onward and L-0101 to L-0103, only L-0050 is marked closed in proposals.md. Open and small enough for a run: L-0073 (essays link About, Charter and Design to GitHub; a local container path printed; "Findings" against "Pieces"), L-0076 (Latest heading above the Now box), L-0077 (the Now box's "Being looked into" lists running studies, "On watch" omits reads without a checkpoint), L-0079's unreviewed LiteLLM count on the proposals page, L-0103 (LH035's opening still says its map page "is in review", change with the knowledge map that quotes it; the Now box repeats the first task's name; a study note says cost unknown where the schedule prices it), L-0075 (one sourced, dated line per flaw on watch pointing to the vendor's own fix, without advice in our voice). P-0019's remainder (codes on the Schedule, Proposals and Releases pages) is also open. Close: one editorial run working down the list, closing each lead with a dated line. Who: run; L-0075 with a fresh agent's attribution check. When: 14 to 20 November. Cost: $3 to $6. Exists: the leads named, P-0019.

### (d) Reuse and trust

23. **No licence** (L-0101). A researcher cannot tell whether text, code or derived data may be reused. Retained third-party bodies carry their owners' terms, and five were already withheld for a Content-Signal of use=reference (use-reference-1). Who: keeper (decision 1). When: the day after the decision. Cost: negligible. Exists: L-0101.
24. **Data reachable only through GitHub folder links** (L-0102). Site URLs for study data answer 404; there is no index of the 12 replay commands and no note of the environment they need, although the Friday reader reproduced the layer map's figures from one. Close: a data and replay index page listing each study's data folder, replay command, environment (Python version, packages, network or offline) and size, linking to the repository; serve small derived tables on the site, not the 341 MB of raw bodies. Who: run (index); keeper for any hosting beyond the repository. When: index by 20 November. Cost: $2 to $4. Exists: L-0102.
25. **No citation identifier.** Pieces have stable addresses and versions, but nothing gives a citable record. Close: CITATION.cff and a "how to cite" line in each colophon (run); a DOI through an archive such as Zenodo means creating an outside account and a permanent deposit, which is irreversible outside the repository, so it is the keeper's (decision 3). When: CITATION.cff with the licence; DOI only if the keeper wants it. Cost: negligible. Exists: L-0074.
26. **Methods are per piece; the cross-cutting ones are scattered.** design.md, notes/reader-review.md and AGENTS.md hold how claims are labelled, reviewed and corrected, and About summarises. The sceptic and the researcher both doubted that every reviewer is another agent of the same model (notes/editor/2026-11-12T1414Z.md, 2026-11-13T1452Z.md); About says "a second agent" without that caveat. Close: one sentence in About's "How the work is checked" saying reviewers are agents on the same family of models, which makes a review a contribution, not independent confirmation (AGENTS.md's own wording). Who: run. When: by 20 November. Cost: negligible. Exists: raised in two editor's notes; no lead.

### (e) Accessibility and phone reading

27. **Figure text too small at phone width.** At 390 px the lead figure's labels are about 5 px (L-0103; its SVG is 720 wide with 11 px text), the map figure's about 8 px (L-0072), and the week-one chart's too small (L-0029, open since 7 November). One essay figure stays a white card in the dark theme (L-0072). The editor's readers found no horizontal scroll and no console errors (11 and 12 November), and every article figure has a title element. Close: through the site's figure styling, not the pieces' text: tap to open a figure full size, or let a wide figure scroll inside its own box, and a dark-theme rule for that essay figure; render each at 390 px in both themes with the Chromium command in CLAUDE.md. Who: run (no figure's data changes). When: by 20 November. Cost: $2 to $4. Exists: L-0029, L-0072, L-0103.
28. **Two boxes of notices before the lead at phone width** (editor's note of 12 November). Close: collapse dated notices to one line with "more" on narrow screens. Who: run. When: with gap 27. Cost: included. Exists: noted in notes/editor/2026-11-12T1414Z.md; no lead.

No other accessibility evidence was found: no screen-reader or contrast audit has been run, so neither a pass nor a fault can be claimed.

## 3. Plan

### This week (14 to 20 November): run work, no reviews needed

Weekend runs are light (LH039, LH049, LH044's first weekly read, LH045's Epoch read, LH039's checkpoint), so most of this fits on 14 and 15 November; the rest goes into the editor's step on 16 to 20 November.

1. Investigation pages: link LH030, LH032, LH037, LH039, LH040; complete every page's `studies:` front matter (gaps 11, 17).
2. One editorial pass over the open leads: L-0073, L-0076, L-0077, L-0079, L-0103 (with the knowledge map), L-0075 with an attribution check, P-0019's remainder (gap 22).
3. Figures at phone width and the dark-theme card (gaps 27, 28).
4. In short openings for LH000 to LH029 (gap 21).
5. observations.md brought up to date; programme.md's header and Answered; README's and About's paragraphs; About's sentence on same-model review (gaps 18, 19, 20, 26).
6. Glossary page; generated corrections index; data and replay index (gaps 1, 4, 24).
7. A sentence in programme.md's Next on LH001 (gap 16).
8. Rows: LH043 evidence review, LH042 reader review, a fallback date on php-account-rev, the layer piece's 1.2 (gaps 12, 13, 14).
9. Start the "What we can say so far" box (gap 8): draft by 18 November, reviews 19 to 22.

Estimated cost of the week's extra work: $20 to $40, above the scheduled runs.

### By end of November

- The "What we can say so far" box live on the front page and About (about 23 November).
- LH043 evidence review and LH042 reader review (week of 23 November).
- PHP account: the notice for F5 and D-Link by 30 November if PHP has not released (gap 13).
- Licence, CITATION.cff and the citing page, once decided (gaps 7, 23, 25).
- Scheduled already: the robots.txt paper draft, the week-one and first-essay revisions (which take the week-one L-0078 sentence), LH036's interim record, LH038's record, LH040, LH049 and LH051's records.

### December

- 1 to 3 December: the first monthly digest with its Reported section, if decided (gaps 3, 6).
- From 8 December, one new reviewed piece at a time beside the scheduled ones: the disclosure timeline piece (gap 9), the found-nothing piece (gap 2), the layer piece's 1.2 (gap 14), then the GH Archive piece or explainer after 14 December (gaps 1, 10).
- Two early-piece reader reviews a week (gap 15).
- Live views on study pages, if decided (gap 5).

### Later (January)

- The worm-waves piece after LH041-record 1.0 (gap 10).
- The retrospective of corrections and incidents, after the robots.txt paper (gap 4).
- The remaining early-piece reader reviews, to about 15 January.
- Model-found bugs' fuller account after LH036 stops (LH036-record, 12 to 31 January).

## 4. Keeper decisions needed

1. **A licence** (L-0101). Options: (a) CC BY 4.0 for prose and Lighthouse's own derived data, MIT for code, with retained third-party bodies excluded and kept under their owners' terms; (b) CC0 for data and code, CC BY 4.0 for prose; (c) no licence, saying so on About. Recommendation: (a), because attribution suits a research watch, MIT is the common default for scripts, and the exclusion matches the Content-Signal and robots.txt rules already kept.
2. **Whether the monthly digest and its Reported section need review.** Options: (a) This week's rules, kept by the run with no review, since they add no figure beyond released pieces and cited sources; (b) a fresh agent's attribution check before each issue (under $1); (c) the full reader-and-inference review. Recommendation: (b): cheap, and a month's Reported items are more likely to be quoted than a week's.
3. **A DOI.** Options: (a) none; stable URLs, versions and CITATION.cff; (b) a Zenodo deposit of each released piece or of monthly snapshots. Recommendation: (a) for now; revisit if anyone cites Lighthouse, since a deposit is permanent and needs an outside account.
4. **Unreviewed live counts on study pages.** Options: (a) keep unreviewed numbers in the Now box only, as now; (b) allow a labelled, dated, uninterpreted series on a running study's own page; (c) also on investigation pages. Recommendation: (b): a researcher can watch a series accumulate, and the front page and investigation pages stay reviewed.
5. **Whether early-piece reviews (P-0011) should go ahead.** Options: (a) start in December, at $11 to $22 at most; (b) leave in backlog. Recommendation: (a): the pieces still carry the front page's longer account, and the reviews have changed meaning in every round logged.
