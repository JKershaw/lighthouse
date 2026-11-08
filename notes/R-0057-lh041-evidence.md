# R-0057: evidence review of LH041, the registry worms, dated (record 0.1)

**In short.** We checked LH041's first record against its sources and data. Every important count reproduces exactly with separate code: 2,244 matching records, the waves found and how, Shai-Hulud 2.0's 88 maintainer clusters in 14.7 hours, ChainDrop's 13 clusters and 444 packages in 3.7 hours, and the AntV wave's single large cluster. The brief came before the data. Six things needed correcting: one misread vendor timeline, one cluster read as an account, a missing post hoc label in the opening, and three small count or wording errors. They are fixed in record 0.2, no must-fix item remains, and the reader-and-inference review comes next.

- **Reviewer:** an evidence-review subagent in Claude Code (Claude Opus 5.5) for the driving session, 8 November 2026, 19:45 to 20:40 UTC. I did not write LH041, and I formed this view before reading the study's for-driver.md or any other note.
- **Reviewed:** studies/LH041/LH041.md 0.1 (commit 65e3d4a), brief.md (147e953), scripts/waves.py, collect.py, tabulate.py, draw_figure.py, replay.sh, the retained read data/2026-11-08T1910Z/, data/prebrief/ and figure-reach.svg.
- **My code and output:** [studies/LH041/review/](../studies/LH041/review/): reproduce.py, checks2.py, checks3.py and selection_check.py, each with its `-output.txt`; fetch_sample.py and web/ (the re-read pages and their log); the figure as rendered at 720 by 700, light and dark.
- **Spend:** not available from inside this subagent. `harbour/hb tokens --latest` prices the transcript.

## What I read

| What | URL | UTC | Status |
|---|---|---|---|
| OSV npm export (same generation 1794135770331461 and sha256 32aba799… as read 1; not retained, 220 MB) | https://osv-vulnerabilities.storage.googleapis.com/npm/all.zip | 2026-11-08T20:21:57Z | 200 |
| OSV PyPI export (same generation 1794147478659500 and sha256 5d2d2b48… as read 1; not retained) | https://osv-vulnerabilities.storage.googleapis.com/PyPI/all.zip | 2026-11-08T20:22:08Z | 200 |
| StepSecurity, ChainDrop (w19) | https://www.stepsecurity.io/blog/chaindrop-npm-worm | 2026-11-08T20:18:45Z | 200 |
| Snyk, AntV wave (w10) | https://snyk.io/blog/mini-shai-hulud-antv-npm-supply-chain-attack/ | 2026-11-08T20:18:47Z | 200 |
| Unit 42, Shai-Hulud and 2.0 (w16) | https://unit42.paloaltonetworks.com/npm-supply-chain-attack/ | 2026-11-08T20:18:49Z | 200 |
| Aikido, Tensorlake (w14) | https://www.aikido.dev/blog/tensorlake-npm-package-compromised | 2026-11-08T20:18:52Z | 200 |
| Elastic, ChainDrop (w13) | https://www.elastic.co/security-labs/shai-hulud-chaindrop-npm-supply-chain | 2026-11-08T20:18:53Z | 200 |
| Unit 42, npm threat landscape (w07) | https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/ | 2026-11-08T20:18:56Z | 200 |

Each page host's robots.txt was read first and allowed the page. All six pages came back at the same byte length as the copies retained before the brief. They are kept gzipped, with emails redacted, under review/web/, and log.psv holds the hash of the bytes received. I also read the retained text of all nineteen pre-brief pages (data/prebrief/web/) to look up each indicator. I fetched no package, tarball, payload or packument, and ran or imported nothing from any record.

## What I checked

1. **Brief before outcomes.** The brief, waves.py and collect.py were committed at 147e953, 19:09:55 UTC. The first OSV request in requests.csv started at 19:10:04 (collect.py logs the time a request starts). Every pre-brief read in web-log.psv falls between 19:01:11 and 19:04:25. The one OSV record read before the brief, MAL-2023-1 (a 2023 record with no link to any wave), was retained and holds no wave text. `git diff 147e953 HEAD` shows waves.py and brief.md unchanged. collect.py changed only to read null fields as empty and to redact emails, as the record's Method says. Two caveats: commit times are set by the committer, not stamped from outside; and the OpenSSF files and MAL-2023-1 have read times in sources.md but no row in web-log.psv.
2. **Indicators against the vendor pages.** I searched the retained pre-brief text for every specific and shared indicator in waves.py, after lower-casing and undoing defanging. All are quoted in the pages waves.py names except one: **"tensrlake" (W13) appears in no retained page.** No record joined on it (Tensorlake's one record joined by a hash), so no count depends on it. The six live re-reads confirm the claims the record leans on:
   - StepSecurity: 444 packages and 2,212 versions; 11 carriers and 433 packages (2,201 versions) "republished automatically"; counts as of 18:10 UTC; keyv 6.0.0 at 09:35:00; second tier from 09:38:13.
   - Snyk: 01:39 UTC; 323 packages; one account that "maintained 547 packages".
   - Unit 42: "first reported in early November 2025"; "over 25,000" repositories; "moderate confidence" that an LLM wrote the September script.
   - Elastic: math_init.js marks packages "trojanized during worm propagation to other maintainers".
   - Aikido: 8 October 2026.
   - Unit 42's threat-landscape page: 32 Red Hat packages on 1 June.

   Indicators that could look like names are not people. "m-kosche", "skyleen" and "iseekaigogo" are command servers that the vendors print as domains.
3. **Independent reproduction** (review/reproduce.py). It reads the indicator lists from waves.py as literals and reuses none of tabulate.py. It recomputes matching, joins, registry dating and clusters, using its own graph search. Everything below matched the committed tables exactly:
   - **Selection.** My matcher agrees with the stored match on all 2,244 records. Over the whole re-downloaded export, which is byte-identical to read 1, it selects the same 2,244 records with none missed or extra (selection_check.py). The export holds 223,208 npm and 12,013 PyPI MAL- records, and 163,919 npm records published from 1 September 2025.
   - **Joins, brief's view.** Indicator 1,241; window 751; ambiguous W02+W10 4; window overlaps 144 (W08+W09), 5, 1 and 1; lineage, unassigned 93; seed only 3; withdrawn 1.
   - **Joins, post hoc view.** Window 896; lineage, unassigned 94.
   - **Shai-Hulud 2.0, post hoc.** 88 clusters, 87 after the first. 1,029 registry-dated versions between 03:10:05 and 17:54:20 UTC on 24 November 2025, 14.74 hours. Median new cluster at 7.07 hours. The first cluster has 32 packages.
   - **ChainDrop, post hoc, indicator joins.** 444 records and packages; 2,236 versions in the window, 2,127 of them registry-dated, from 09:35:00 to 13:18:41 (3.73 hours). 13 clusters: the first holds 11 packages, 12 later clusters hold 416, and 17 packages have no packument (11 + 416 + 17 = 444). New clusters appeared at 0.05 to 3.72 hours. **The first cluster is exactly the 11 carriers StepSecurity lists by name** (checks3.py). That makes the record's comparison stronger than "a comparison of counts, not of package lists". The second cluster's first publish is at 09:38:13, the second StepSecurity gives for its first automated republish.
   - **AntV.** Clusters of 316, 6 and 37 packages, the later two at 1.24 and 164.83 hours.
   - **Other waves.** W01, W06, W08, W10, W12 and W13 reproduce in both views, as do the clocks (0.47 to 18.22 hours; medians 4.0 to 11.7; first imports 4.0, 3.5 and 9.3 hours for W07, W08 and W12; bare-midnight `published` on 316, 32 and 2 records). So do the out-of-window versions (18, 26, 8), the seeds, the math_init.js count, residue (1,992 records and 5,126 versions; 2,137 and 5,550) and the 20 of 20 spot check.
   - **replay.sh** ran in 3.5 seconds and rewrote every table and the figure byte for byte (`git status` clean afterwards).
4. **The two post hoc readings.** Both are justified, and the record labels them, counts them (two decisions) and says what would test them: a brief for later waves fixing both in advance. Without the first, a 2017 version sets Shai-Hulud 2.0's first cluster (103 packages) and a February 2026 version sets ChainDrop's, which makes "after the first" meaningless. Neither reading changes a wave's cluster count. They change only which cluster comes first and the time spans. The second follows from the brief's own table of ecosystems. The headline timings in the opening came from the post hoc view but were not labelled there (correction 4). "Upper bound" appears wherever spread is measured: the opening, the Answer, Limits and the figure footer. One gap: the bound covers the person question, not clustering error (Suggestions).
5. **Clusters read as people or accounts.** The Limits say plainly that a cluster is not an account, a person or an organisation. The Answer's AntV line broke that: it said "mainly one account ... not spread between accounts", under a derived-measurement label and against the brief's pre-set reading, which is "spread across clusters" (two later clusters). The hashes partly support the account reading: one maintainer hash is on all 316 packages of the first cluster, out of 29 hashes in it. But the cluster is still not shown to be one publisher (correction 3). The for-driver.md lines repeat the account reading (Suggestions). The Interpretation bullet, "one stolen account used at scale", is labelled and attributed, and can stand.
6. **Caution.** No package, tarball or payload was fetched or run. The collector reads JSON metadata only. The record, brief, sources.md and for-driver.md name no maintainer; I searched for the account names the vendor pages print and found none. The mechanism is described at the level of "stolen tokens publish poisoned versions". waves.py holds indicators of compromise quoted from public pages, which are not working instructions. My own checks counted hashes and recovered no name. Maintainer names are hashed with a salt that is published in collect.py, so the hashes keep names out of the files but would not stop anyone matching them against npm's public maintainer lists (Suggestions). Nothing anonymised by a source is involved, since npm publishes maintainer lists.
7. **The figure.** I rendered it in a 720 by 700 window, light and dark (review/figure-*-720x700.png), and in full. It passes scripts/check_chart_style.py. Both themes are legible, the colours hold, and the panel numbers match the tables. The SVG is 790 px tall, so a 700 px window cuts off the bottom row's axes and the footer with the post hoc label. It scales on a page, so this is not a defect. The ChainDrop panel runs to 52 hours, which squeezes the 3.7-hour burst against the axis. The AntV panel labels its y-axis only at 0 and 5.

## What I found

Must-fix, all corrected in 0.2 (the record's Corrections lists them):

1. **"None withdrawn" was false.** MAL-2026-4377 (lineage marker only) was withdrawn on 26 May 2026. The tabulator dropped it correctly, but the record didn't report it, which the brief requires.
2. **ChainDrop's clock misread StepSecurity.** The record said the registry put the start "three minutes before the first publish StepSecurity's timeline lists". In fact the timeline lists keyv 6.0.0 at 09:35:00, the same second as the registry. 09:38:13 is the first automated republish, and the brief took it as the vendor clock. The brief's clock stays as fixed. Only the description changed.
3. **The AntV cluster was read as an account** in the Answer (finding 5 above).
4. **The opening's two timings were not labelled post hoc.**
5. **Lineage records outside every window.** The record had "22 npm records from June 2026" and left out a PyPI record from March 2026, because it mixed OSV's dates with the registry's. By the record's own dating the figures are 21 npm records and 1 PyPI record. The total of 93 holds.
6. **Two small inaccuracies.** Answer 1 said W09 appears "only ... post hoc", but under the brief's rule one npm record joins it by window. And the TanStack wave's last new cluster came at 30.02 hours, not "within 30 hours".

Also found, not must-fix: "tensrlake" is not quoted from any retained source, though waves.py says every indicator is. ChainDrop's 444 indicator records came mostly from two feeds together: amazon-inspector and ghsa-malware on 438, amazon-inspector alone on 3, ghsa-malware alone on 1, and no origin on 2. The record says the feed was not checked. 56 of Shai-Hulud 2.0's 88 clusters have a single maintainer hash.

## What I changed

studies/LH041/LH041.md, version 0.1 to 0.2: the six corrections above. To match them I also changed the header's version line, the review status in the opening, "before review" to "before release", the Findings label line and the "Not reviewed" limit. I added a Corrections entry that points to 65e3d4a. No figure, table, script or brief changed.

## Suggestions

- **Clustering error versus the upper bound.** Say what "upper bound" covers. Clusters can undercount the accounts reached, because co-maintained packages merge (AntV's first cluster has 29 hashes). They can overcount, because maintainers removed since a wave split clusters. If maintainer lists were unchanged, each publishing account sits inside one cluster, so clusters would be a floor on publishing accounts. The bound is on the person question only.
- **ChainDrop's first cluster.** Record that it is exactly StepSecurity's 11 named carriers (checks3.py), and that the feeds were checked (above).
- **Joins per wave.** Report indicator joins separately for W06 (2 records) and W07 (1 PyPI record, matched by a command-server domain). Both are counted among the "seven identified by indicator", but nearly all of each wave comes by window.
- **The residue share** sets records that include a few PyPI ones (4 in the brief's view, 43 post hoc) against an npm-only denominator. With npm only the share is still 1.2 to 1.3 per cent. Say so.
- **The salt.** Say the hashes use a published salt and are not anonymisation.
- **Read times.** Log the OpenSSF files and MAL-2023-1 in web-log.psv with status and time, and drop or source "tensrlake" in the amendment before read 2.
- **The figure.** Give ChainDrop a 0 to 6 hour scale, or an inset, to match the headline. Add y ticks at 1 to 3 on the AntV panel.
- **For the driver (for-driver.md, which I may not edit).** The investigation-page line says "the AntV wave stayed mostly inside one account's 316 packages", and programme.md's Next says "the AntV wave was mainly one account". Both should read "one maintainer group of 316 packages, which Snyk attributes to one compromised account". The investigation line's "under 15 hours" and "under 4 hours" should carry "by a reading chosen after the counts were seen". The schedule row LH041-reviews can note this review as done.
- **Miasma.** The Interpretation's "one compromised release pipeline" paraphrases Unit 42 loosely. Unit 42 says a compromised employee account pushed commits to the organisation's repositories (w07). "One compromised account in one organisation" is closer.

## Verdict

No must-fix item remains. The record is ready for the reader-and-inference review. That review, and a fresh agent's reading of the 0.2 changes, come before any line reaches a piece. This review is a second agent's agreement, not independent confirmation.
