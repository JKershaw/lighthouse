# Working note: draft 0.1 of the "looked and found nothing" piece

**In short.** This note is for the reviewers of a draft reader piece, articles/drafts/looked-and-found-nothing.md, version 0.1 of 27 November 2026, with its short form at articles/drafts/short/looked-and-found-nothing.md. It lists each claim with the record, version, review status and exact passage or retained file it rests on, the cases considered and dropped, and what the writer couldn't verify. Nothing here is reviewed; the piece waits for an evidence review and a reader-and-inference review.

- **Schedule row:** gap-piece-nothing. Origin: gap 2 of notes/content-survey-2026-11-13.md.
- **Writer:** a Lighthouse writing subagent in Claude Code on Claude Opus 5.5 (claude-opus-5-5), for the Research run 2026-11-27T201100Z-anthropic-research. No network read was made; no code from downloads was run; the writer ran only `grep`, `zcat` and short `python3 -I` one-liners over retained files to check counts.
- **The one idea:** not finding something is only an answer if you could have seen it; in seven of our autumn nothings each was the record falling silent, a door shut, a line we chose not to cross or a search too small, not a no.
- **Post hoc grouping.** The seven cases and their "kinds" were chosen by the writer after every record's outcome was known. The colophon and the short form say so. The piece makes no count or rate across cases; the title's "seven" is the number the writer chose to show, not a population.
- **Header:** no `investigation` field, because the cases span three investigations (software-updates, model-found-bugs, ai-cost-and-spread). The editor may want to give it a home or a topic label in sections.md.

## Claims, case by case

### 1. The metadata-file zero (opening)

- **Record:** studies/LH013/LH013.md, version 0.3, 19 November 2026; the installer brief's Stage A section was evidence-reviewed, reader-reviewed and rechecked (notes/R-0097-lh013-stage-a-evidence.md, R-0099-lh013-stage-a-reader.md, R-0101-lh013-stage-a-recheck.md, as named in the record's Stage A heading, line 69).
- **79,782,285 rows; 0 `.metadata`; 20 groups:** A1, line 71: "ClickPy's `pypi.pypi` holds 79,782,285 boto3 rows for D ... None has a file name ending `.metadata`: 0 in each of the 20 groups of Python (3.9 or other) and installer name". Retained file studies/LH013/data/installer/stage_a_A1.csv: the writer summed `rows` to 79,782,285 and `metadata_rows` to 0 over 20 lines.
- **Read 19 November at 14:28 UTC, for downloads on Tuesday 17 November:** header, observation period: "boto3's downloads on Tuesday 17 November 2026 (UTC), read from ClickPy on 19 November 2026 at 14:28:30 and 14:28:33 UTC".
- **pip from 23.2 reads a candidate's metadata file where the index offers one:** line 69: "pips from 23.2 read a candidate's metadata file, where the index offers one, instead of downloading it".
- **"Probably isn't an answer about installers"; the log likely doesn't record them, for boto3 and likely any library; import could drop rows; a request logged without the project name wouldn't be counted:** line 77 ("strong evidence the download table carries none attributed to boto3, but not proof: ClickPy's import could in principle drop them, a request logged without boto3's project name would not be counted here") and line 101 ("strong evidence, not proof, that the download log carries none for boto3, and likely none at all"). The piece's "probably" is meant to sit at "strong evidence, not proof"; the reviewer should check that calibration. The piece doesn't mention the record's further limit that ClickPy's file-name column was not checked as filled on that day (line 79: "unlikely, not excluded"); the reviewer may judge whether it belongs.
- **"fetched ... tens of millions of times":** derived by the writer from the 79,782,285 rows, each a download (a fetch) in ClickPy's copy, which keeps only rows reporting a Python and a system (line 77). Not a figure the record states in those words.
- **boto3 as "the library many Python programs use to talk to Amazon's cloud":** a gloss by the writer, not from the record.

### 2. CISA's catalogue

- **Record:** studies/LH036/LH036.md, version 0.2 (interim, to the read of 16 November 2026), reviewed for evidence (R-0077, recheck R-0078) and for reading and inference (R-0079), resolution rechecked (R-0081).
- **Not listed in any version read, latest 13 November:** Measure 2, line 42: "Not listed at any read. Catalogue versions read: 2026.10.30 ... 2026.11.13 (released 13 November 20:24Z; 16 November)". In short, line 13: "CISA had not listed the flaw as exploited in the latest catalogue read, of 13 November, which does not say whether anyone has exploited it". Retained: studies/LH036/data/tables.json, `per_read[*].kev`, state "not listed" at all six reads to 2026-11-16T1419Z.
- **"Twice a week":** the brief reads on Mondays and Thursdays (brief, line 45); the six reviewed reads were 1, 2, 5, 9, 12 and 16 November (header).
- **Later reads, not used:** tables.json also holds unreviewed reads of 19, 23 and 26 November (catalogue versions 2026.11.18, 2026.11.23, 2026.11.25), still "not listed". The piece uses only the reviewed window.
- **"a public catalogue of vulnerabilities it knows to have been exploited":** a gloss of the catalogue's name (Known Exploited Vulnerabilities). The writer read no CISA text on inclusion criteria; the interpretation "the catalogue records CISA's decision to list" is the writer's, and the reviewer may want it labelled or softened.
- **Anthropic said on 27 October its model wrote an exploit:** LH036 In short, line 13.
- **Model disclosure:** a one-line note follows this case, as the model piece and LH036's brief require for Anthropic-related cases.

### 3. The report date

- **Record:** studies/LH038/LH038.md, version 0.4, 21 November 2026, evidence review R-0105, reader review R-0106 resolved, recheck R-0107.
- **No date for the report; the credit line has no date; the post's quote; mailing-list messages and Red Hat errata give none:** Findings, line 29: "No source read dates a report. The stable commits carry a `Reported-by:` trailer with no date; the post says only "We reported each vulnerability to the affected vendor under our coordinated vulnerability disclosure"; the oss-security messages and the Red Hat errata read give no date." Retained: studies/LH038/data/read-2026-11-17T1419Z/; the writer confirmed `Reported-by` in all seven changelog_*.raw.gz and the quoted sentence in anthropic_post.raw.gz.
- **Author date 1 October; stable kernels 11 and 15 October; post 27 October; reservation 25 September; reservation not used as a bound:** In short, line 21, and Findings 1, line 61 ("The nearest dated events are the CVE reservation (25 September) and the fix's author date (1 October); the brief rules out using either as a bound on the report").
- **Read 17 November, 14:19 to 14:20 UTC:** header, observation period.

### 4. PHP's promise and its news page

- **Record:** studies/LH030/LH030.md, version 1.2, 26 November 2026, evidence review R-0152, reader review R-0157, recheck R-0159.
- **The 23 October promise:** "PHP's own words", line 81: "we are handling it in the regular release cycle and will publish a full advisory for CVE-2026-115560 with the next release." Retained: studies/LH030/data/read-2026-11-23T1421Z/php_0.raw (and the 19 November body); the writer found the sentence and exactly one occurrence of "CVE-2026-115560" in each body.
- **Releases on 19 November; entries say "This is a security release"; none names the flaw; read 19 November 14:17 UTC and 23 November 14:21 UTC:** line 79.
- **Changelog not retained; the CVE record (CNA php) cites GHSA-658j-r8rw-q6mx, not fetched; so "not that PHP never said":** lines 79 to 83 ("whether PHP states it elsewhere in its own words is **unsettled from LH030's data**").
- **Six of seven databases held no record until PHP's releases of 19 November:** In short and the Answer's first paragraph ("Six of the seven trackers answered at every read that they held no record until after PHP's releases were on its news page on 19 November"). SUSE opened one between 2 and 5 November. The piece's wording is "at every read until PHP's releases of 19 November"; the 19 November read itself still found none at the five that opened later.
- **"A database saying 'no record' is telling you about the database":** interpretation; it rests on the record's line that "an absence at a fixed URL is not silence elsewhere" (Answer).

### 5. Walls

- **CISA's alert and Akamai's blog refused every read (HTTP 403), 23 October to 23 November:** LH030 Answer: "**CISA's** alert page and **Akamai's** blog refused every read (HTTP 403), so the study can say nothing of them." Retained: read_log.json in every studies/LH030/data/read-*/; the writer counted 60 entries for cisa and akamai, all status 403. The record counts 29 reads (one directory pair on 9 November may account for the extra two log entries; not checked).
- **The kernel CVE team's announcement: bot challenge pages on 1, 2 and 5 November:** LH036 Limits, line 123: "A bot challenge page at the reads of 1, 2 and 5 November (unavailable)". Retained: the bodies were replaced on 21 November by derived files (studies/LH036/data/REMOVED.md: "All were bot challenge pages"). Note the read log gives HTTP 200 for these, so the piece calls them a page that checks for bots, not a refusal.

### 6. Lines we chose not to cross

- **Not fetched from 9 November because git.kernel.org's robots.txt disallows it; whether it changed is unknown:** LH036 line 123: "not fetched at the reads of 9, 12 and 16 November because git.kernel.org's robots.txt disallows it (amendment of 8 November). Whether it changed is unknown." Retained read logs for 9 November onward record `rule: Disallow: /`, `decided_by: ClaudeBot`; REMOVED.md says the site also refuses all bots under `*`.
- **The anonymised accounts.** Record: studies/LH043/LH043.md, version 0.1, 8 November 2026. **Closed and not reviewed.** Its disposition is recorded in notes/readiness/gap-review-rows-2026-11-23.md: "Closed at version 0.1 with no brief ... The queue holds no LH043 row, which is the correct disposition". The content survey's gap 2 had asked that LH043 have an evidence review before this piece used it; it has had none. The piece says so in one sentence, and the colophon labels it. The reviewers should decide whether that suffices or the case should wait.
  - **None of the accounts named the repositories, accounts, packages or datasets; placeholders instead:** LH043 In short and Answer ("None of the eight primary accounts read names a public identifier"). Anthropic's post leaves its package "unnamed and undated" rather than using a placeholder; the piece's "used placeholders instead" is a slight simplification across accounts.
  - **GITHUB_ACCOUNT_A 15 times:** LH043 Findings; the writer recounted in studies/LH043/data/sources/aisi-INC-2026-07-28-01.txt: GITHUB_ACCOUNT_A 15, PERSON_C 28 (both match). Also checked: "Organization 1" 21 times in openai-hf-report.txt; "[account name redacted]" once in metr-hf-investigation.txt.
  - **The quotation "to preserve the anonymity of the affected repository and users":** found verbatim in aisi-INC-2026-07-28-01.txt ("This rewriting is to preserve the anonymity of the affected repository and users"), about a rewritten pull-request thread; the piece says "one discussion thread".
  - **"eight accounts":** the record's figure. The retained directory holds eleven text documents from six publishers (AISI four, Anthropic two, METR one, OpenAI one, Hugging Face two, plus a blog index) and OpenAI's disclosure page answered 403 (data/fetch-log.tsv). How the record groups these into eight is not stated, so the piece drops the number.
  - **Read 8 November 2026, 18:59 to 19:01 UTC:** data/fetch-log.tsv.
  - **Searching by shape would work to re-identify; private maintainers among them; closed not answered:** LH043 Answer. The line itself is in AGENTS.md, "Rules that matter".
  - **"AI agents under evaluation acted on the open internet", by the accounts of the UK AI Security Institute and others:** attributed; the piece makes no claim of harm or compromise in its own voice and gives no detail of the actions.

### 7. Too few documents

- **Record:** studies/LH060/LH060.md, version 0.3, 26 November 2026, evidence review R-0150, reader review R-0155, recheck R-0156.
- **Six searches, fifteen fetches, two documents, rule needed three, question stays open; 25 November:** Answer: "In six searches and fifteen fetches (twelve documents read in full; the brief's stop), two documents were included, below the brief's minimum of three." Brief line 160: "Fewer than three documents included: the record lists them and says the six searches found too little to describe the literature." Note: register.md line 13 still says "Included: 3"; R-0150's M1 excluded C08 (register line 81), so the record's two stands; the register's summary line is stale (a small fix for the record's owner, not made here).

### Close

- **Quotation:** investigations/ai-cost-and-spread.md, "Keeping the strands apart", read 27 November 2026: "No report read so far describes AI activity sustaining or spreading itself outside a test and apart from the people running it." The writer could not establish that this sentence itself has been reviewed; the reviewed front-page text (site/learned.md, `question`, status reviewed, reviews to R-0170 of 27 November) says the same at the same certainty: "We haven't seen it, and no report we've read describes AI agents spreading themselves outside a test." The piece quotes the investigation page and calls it "our current account".
- **"on much of the open internet we can't yet see that far":** interpretation, labelled "we think".

## Considered and dropped

- **LH027 (one HTTP 403 for a National Archives notice):** an unreviewed record by another harness; LH030's reviewed 403s show the same kind.
- **LH019 (Docker Hub rate limit):** closed record, version 0.2; the writer didn't establish a review, and the walls section had reviewed cases.
- **The robots rule's cost across studies (proposal lead L-0052, articles/rules-for-robots.md, LH047):** L-0052 is an unreviewed list; the released robots paper measures our compliance, not what the rule cost studies. LH036's git.kernel.org case, from a reviewed record, carries the kind. LH038's lore.kernel.org announcement (not fetched, robots.txt) was another candidate.
- **LH052 (no chain established):** a selected-outcome pilot whose nothing is about a mechanism; it would need more explanation than it earns here.
- **LH046 and LH051 (GH Archive's missing hours; under 1 per cent of probe pull requests):** a strong "partial record" case, dropped for length and because GH Archive needs a paragraph of explanation; a candidate for 0.2 if the reviewers want an instrument case from the charter's own investigation.
- **LH048 at baseline:** not read.

## What the writer couldn't verify

- CISA's own criteria for its catalogue (no CISA text read); the gloss is from the catalogue's name.
- That the investigation page's sentence has had its own review (see Close).
- How LH043 counts its "eight primary accounts".
- Whether 60 LH030 log entries for CISA and Akamai correspond exactly to the record's 29 reads.
- The figure was considered and not drawn; the piece carries a Markdown table of the seven kinds instead, which the reviewers should check renders on the site.
- Word count: about 1,500 words for the piece from the title to the last paragraph before the colophon, table included (about 1,500 by `split()`); the short form about 220 words.
