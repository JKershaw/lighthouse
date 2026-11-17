# R-0084: resolution of LH044 read 1's reviews (17 November 2026)

**In short.** This note settles what the three reviews of the closing web's first weekly read left open. The checkpoint was cleared; the only proposed public line, the evidence review's for the investigation page, was not cleared as written. We chose to write a corrected read-1 line rather than wait for read 2, and give it below as proposed text, not yet on the page. Three optional suggestions on the checkpoint's opening were taken where they changed no figure, with a Correction line. A fresh agent rechecks every sentence listed here before anything public changes.

**Row:** LH044-read-01-resolution-recheck (resolution half; the recheck is a different fresh agent).
**Writer:** a research subagent in Claude Code (Claude Opus 5.5) for the scheduled run of 17 November 2026.
**Inputs:** studies/LH044/checkpoints/2026-11-15.md as at 94b8ef8 (repository HEAD 06914fb); notes/R-0072-lh044-read-01.md, notes/R-0076-lh044-amend.md, notes/R-0080-lh044-reader.md; studies/LH044/brief.md amendments 3 to 9; both reads' classes.csv; investigations/ai-cost-and-spread.md (LH044 lines 27 to 31); programme.md line 91.
**Requests made:** none (offline).
**Files changed:** studies/LH044/checkpoints/2026-11-15.md (In short and one Correction line) and this note. No public page edited.

## The decision: (a), a corrected read-1 line, proposed

**Why a line now rather than none until read 2.** The investigation page is where a reader learns what the closing web has seen, and today it shows only the baseline (13 of 67 named, 1 of 26 drawn walled). Read 1 has since cleared an evidence review, a fresh reading of its amendments and a reader-and-inference review, so it is better checked than the baseline line the page already carries. Its most informative observation, PubMed answering openly at the baseline and refusing a week later, would otherwise sit only in a working document for at least another five days, plus read 2's own reviews. A reader is better served by an honest line that says what changed, what counts only under a rule fixed afterwards, why the two weeks' totals don't compare one to one, and that read 2 decides whether any of it holds, than by a page that looks current and isn't. The risk of waiting is a stale page; the risk of publishing is a line overtaken in a week, which the line itself says may happen. Read 2's line, when it comes, replaces or follows this one after its own reviews.

**Placement proposed:** a new bullet directly after the closing web's baseline bullet (after the paragraph on amendment 5, now line 31), not a rewrite of the baseline line, as R-0072 advised.

### Proposed investigation-page line (not placed)

> - **Reviewed working read (an evidence review and a reader-and-inference review). Load: the closing web, read 1 (15 November).** A week after the baseline, the study's labelled requests found three services that had answered openly now refusing them: PubMed, with a bare 403, and two journals drawn at random, with a 403 naming Imunify360's bot protection. Crossref's API, rate-limited at the baseline, answered. By the study's definitions that's three closings and one opening, but one of the closings, a journal reached by plain HTTP, counts only under a rule for changing addresses that we fixed after seeing this read; under the earlier rule it was set aside, for two. Of the services our requests could read, 11 of 68 named and 6 of 31 drawn showed a wall, and those totals don't compare one to one with the baseline's: two of the drawn walls are new only because the study now reads differently (a page that sends readers straight to a captcha, which a rule adopted after the baseline counts as a challenge, and a captcha on a journal's contact form, reached now that the study follows robots.txt redirects, which we don't think is a wall), and Maven Central's two hosts, walled at the baseline, are now out of sight under the provider robots.txt rule described above. PubMed's refusal and one journal's met requests from the address block registered to Anthropic; the other journal's request went by the plain-HTTP route, whose echoed addresses are Google's, though its own address isn't known. So one request can't say whether a refusal is set for us or for everyone. Read 2 on 22 to 24 November says whether any of it holds ([checkpoint](../studies/LH044/checkpoints/2026-11-15.md)).

### How it meets R-0080's must-fixes

1. **Stale closing count.** It gives three closings and one opening, says the rule admitting the third (amendment 9, 16 November) was fixed after the read was seen, and keeps two under the earlier reading.
2. **Drawn count read as walls going up.** It says the totals don't compare one to one, names the two drawn walls that come from how the study reads (P04, classifier 0.3 under amendment 4; P31, reached under amendment 3, its captcha read as not a wall by the writer, R-0072 and R-0080), and takes the suggested clause on Maven Central's two hosts (now `robots_disallowed` by ClaudeBot under amendment 5).

### Changed from R-0080's offered wording, and why

- R-0080 said the other journal's refusal met "an address registered to Google". The checkpoint says P38's closing "was seen on a route whose address for that request is unknown at either read"; only the route's echoed addresses (P04's, 35.184.25.35 at read 1) are known to be Google's. The proposed line says the route's echoed addresses are Google's and that the request's own address isn't known.
- R-0080 said two drawn walls "weren't walls a week earlier only because the study read them differently". P31 was unread at the baseline (`robots_redirect`), not read as open, so the line says "new only because the study now reads differently" and says how each arose.
- R-0080's "a page a new rule now reads as a challenge" is made concrete: P04's robots.txt answered with a page that refreshes at once to a captcha path, and amendment 4 (8 November, after the baseline) made classifier 0.3 read that as a challenge; at the baseline the same kind of page was `open_unconfirmed` under 0.2.
- The line opens with the changes (what a like-for-like reader can compare) and puts the totals second, with their caveat attached.
- The label follows the page's convention ("Each line opens with how far it has been checked"): "Reviewed working read", matching the page's "Reviewed working record" and its In short's "there is no reviewed finding yet".

### Checked against classes.csv and the amendments

From data/read-2026-11-08T1920Z/classes.csv and data/read-2026-11-15T1413Z/classes.csv (wall column), recounted here offline:

```
baseline named walled 13: F11 F13 R02 R06 R07 D09 D13 A08 A09 A13 A15 A20 O07
read 1   named walled 11: F11 F13 R02 D09 D13 A08 A09 A11 A15 A16 O07
baseline drawn walled  1: P34
read 1   drawn walled  6: P04 P17 P31 P34 P38 P40
A11 open (200, marker) -> refused 403, egress-proxy both reads
P40 open -> refused 403, egress-proxy both reads
P38 open -> refused 403, direct-http both reads
A13 wall_at_robots (rate_limited:429) -> open, egress-proxy
P04 open_unconfirmed (0.2) -> wall_at_robots challenge:captcha-refresh (0.3), direct-http
P31 robots_redirect -> wall_at_robots challenge:recaptcha (0.3), egress-proxy
P17 gone (404) -> refused 403, direct-http
R06, R07 rate_limited -> robots_disallowed "by ClaudeBot: Disallow: /"
A20 rate_limited -> gone (404); A16 robots_disallowed -> wall_at_robots rate_limited:429
```

So of the five drawn services newly walled, two (P04, P31) come from the instrument and three (P17, P38, P40) answered differently. Named: 13 minus A13 (opening), A20 (now 404), R06 and R07 (out of sight by rule), plus A11 and A16, gives 11. "Imunify360's bot protection": the three probe 403s carry the body "Access denied by Imunify360 bot-protection" (checkpoint; R-0072 point 5). "Three closings, one opening" under amendment 9, two under the earlier reading: checkpoint, Changes; R-0076 point 4. Read 2's window, 22 to 24 November: schedule row LH044-read-02.

### Companion clause for programme.md (proposed, not placed)

The consistency rule asks programme.md to say the same at the same certainty. Its line 91 says LH044 "has an unreviewed baseline and reads weekly from 15 November to 7 February 2027". Proposed replacement for that clause, linking rather than restating figures:

> [LH044](studies/LH044/brief.md), the closing web, has an unreviewed baseline and a reviewed first weekly read ([checkpoint of 15 November](studies/LH044/checkpoints/2026-11-15.md)), and reads weekly to 7 February 2027.

The front page carries no LH044 line, so nothing there is proposed.

## The checkpoint's opening: optional suggestions taken

R-0080's Readability 1 and 2 were cheap, supported and change no figure, so both were taken. Readability 3 (Imunify360 refusals on Google-registered routes) is a labelled interpretation for read 2's checkpoint or the record, not the opening; it is left for read 2's writer, as R-0080 suggests.

Sentences changed in studies/LH044/checkpoints/2026-11-15.md, exact text:

**In short, second sentence.** Was: "Of the services whose answer we could read, 11 of 68 named ones and 6 of 31 drawn at random put a wall in front of that request; PubMed, which answered openly a week ago, now refused us with a bare 403, as did two drawn journals, and Crossref's API, walled a week ago, answered."
Now: "Of the services whose answer we could read, 11 of 68 named ones and 6 of 31 drawn at random put a wall in front of that request, two of the drawn walls new only because the study now reads those services differently; PubMed, which answered openly a week ago, now refused us with a bare 403, two drawn journals that had answered refused us with a 403 naming a bot-protection product, and Crossref's API, walled a week ago, answered."

**In short, third sentence.** Was: "One week can't say whether any of that holds."
Now: "Most of our requests leave from an address block registered to Anthropic, so we can't tell a wall set for us from one set for everyone, and one week can't say whether any of that holds."

Support: 206 of 274 panel requests left through the egress proxy, whose echoed addresses are in the block registered to Anthropic, PBC (checkpoint, measure 8; R-0072 point 1); brief, Limits, on a 403 to that block.

**Correction line added** after the second Correction notice:
"**Correction, 17 November 2026 (reader-and-inference review, [notes/R-0080](../../../notes/R-0080-lh044-reader.md); resolution [notes/R-0084](../../../notes/R-0084-lh044-read-01-resolution.md)).** The In short now says that two of the drawn walls are new only because the study reads those services differently (P04 under classifier 0.3, P31 through a robots.txt redirect followed under amendment 3), that the two drawn journals' 403s named a bot-protection product rather than being bare, and that most requests leave from an address block registered to Anthropic. No figure, class or count changed. The earlier edition is at commit 94b8ef8."

No other sentence in the checkpoint changed; classes.csv and every data file are unchanged.

## For the recheck

Read once, against the checkpoint, both classes.csv files and brief amendments 3 to 9: the proposed investigation-page line, the programme.md companion clause, the two changed In short sentences and the Correction line. Nothing above is on a public page; the driver places the line and clause only if the recheck clears this version.
