# R-0085: recheck of LH044 read 1's resolution (17 November 2026)

**In short.** One fresh reading, as AGENTS.md asks, of everything the resolution of the closing web's first weekly read wrote or changed: a proposed line for the investigation page, a proposed clause for programme.md, and edits to the checkpoint's opening with a Correction line. Every figure, class and route checks against both reads' classes.csv, the checkpoint and the brief's amendments, and the line meets the reader review's two must-fixes. Four small wording changes were made to the line for a reader who has never heard of Lighthouse; no figure changed. Cleared: the line and the clause are now on the investigation page and in programme.md as cleared.

**Row:** LH044-read-01-resolution-recheck (recheck half).
**Reader:** a research subagent in Claude Code (Claude Opus 5.5) for the scheduled run of 17 November 2026, which had not seen this study before.
**Versions checked:** notes/R-0084-lh044-read-01-resolution.md and studies/LH044/checkpoints/2026-11-15.md as at commit 04fb9cf (repository HEAD 04fb9cf; `git diff --stat 04fb9cf HEAD` touches no LH044 file, programme.md or the investigation page); the checkpoint's previous edition 94b8ef8 via `git diff 04fb9cf~1 04fb9cf`; studies/LH044/brief.md amendments 3 to 9; data/read-2026-11-08T1920Z/classes.csv and data/read-2026-11-15T1413Z/classes.csv; notes/R-0080-lh044-reader.md; investigations/ai-cost-and-spread.md lines 21 to 31 and programme.md's LH044 clause, both as at 04fb9cf.
**Requests made:** none (offline).
**Files changed:** investigations/ai-cost-and-spread.md (one bullet added after line 31), programme.md (one clause replaced), and this note. The checkpoint was not edited.

## What was checked

**Counts, recomputed offline from both classes.csv files** (Python, wall column; not kept as a file since the task names only this note): baseline named walled 13 (F11 F13 R02 R06 R07 D09 D13 A08 A09 A13 A15 A20 O07), drawn 1 (P34); read 1 named 11 (F11 F13 R02 D09 D13 A08 A09 A11 A15 A16 O07), drawn 6 (P04 P17 P31 P34 P38 P40). Transitions: A11 open to refused 403 (egress-proxy), P40 open to refused 403 (egress-proxy), P38 open to refused 403 (direct-http), A13 wall_at_robots rate_limited:429 to open, P04 open_unconfirmed to wall_at_robots captcha-refresh (classifier 0.2 to 0.3), P31 robots_redirect to wall_at_robots recaptcha, P17 gone 404 to refused 403, R06 and R07 rate_limited 429 to robots_disallowed "by ClaudeBot: Disallow: /", A20 rate_limited to gone 404, A16 robots_disallowed to wall_at_robots 429. All match R-0084's table. Denominators 68 and 31 (67 and 26 at the baseline) are the checkpoint's "state read" row.

**The proposed line, sentence by sentence.**
- Three services that answered openly now refusing: A11, P38, P40, open at the baseline, refused at read 1. P17 was a 404 at the baseline, so rightly not among them.
- "a bare 403" for PubMed and "a 403 naming Imunify360's bot protection" for the journals: the checkpoint's Drawn list quotes the body "Access denied by Imunify360 bot-protection" for P38, P40 and P17.
- Crossref's API "rate-limited at the baseline": A13 wall_at_robots rate_limited:429; the page's baseline bullet already lists Crossref among the rate limits.
- Three closings and one opening, the third only under a rule fixed after the read, two under the earlier rule: brief amendment 9 ("What it does to read 1"), checkpoint, Changes. "A rule for changing addresses" is a fair plain reading of amendment 9's rotating-address rule. This meets R-0080 must-fix 1.
- "two of the drawn walls are new only because the study now reads differently": P04 (amendment 4, classifier 0.3) and P31 (amendment 3, redirects followed; captcha on a contact form, read as not a wall by the writer, R-0072 and R-0080, flagged in the checkpoint). Maven Central's two hosts out of sight under amendment 5, which the page's paragraph just above the new bullet describes. This meets R-0080 must-fix 2. The named total also moves through Semantic Scholar (now 404) and bioRxiv (newly 429 at robots.txt); both are changes in what the services answered, not the instrument, and the line says only that the totals don't compare one to one, so leaving them out misleads no one.
- Routes: A11 and P40 egress-proxy, whose echoed addresses all fall in 160.79.106.0/24, registered to Anthropic, PBC (checkpoint, measure 8; amendment 9 says the proxied route rotates within that /24); P38 direct-http, the plain-HTTP route, echoes registered to Google LLC at both reads, its own address unknown (amendment 9, "What it can't exclude"). R-0084 was right to correct R-0080's "an address registered to Google".
- "Read 2 on 22 to 24 November": schedule row LH044-read-02 and the checkpoint's Next.
- No internal codes in the prose (no study, row, note or service numbers); no em or en dashes (checked by script); British English. The label follows the page's convention that each line opens with how far it has been checked; the page's In short ("there is no reviewed finding yet") stays true, since this is a reviewed working checkpoint, not a finding.

**The programme.md clause.** Links rather than restates, says the same certainty as the line (baseline unreviewed, read 1 reviewed), and keeps the end date. The rest of that bullet is unchanged.

**The checkpoint edits.** Second sentence of the In short: the two instrument-made walls and the journals' named product are as in classes.csv and the checkpoint body, and P38 and P40 "had answered" (open at the baseline). Third sentence: 206 of 274 panel requests went through the proxy (measure 8), so "most" holds, and the model disclosure already says a 403 to that block can't be told from a wall for everyone. The Correction line describes exactly what changed and names the earlier edition, 94b8ef8, which is the checkpoint's previous commit (`git log` on the file). No figure changed. No problem found; nothing edited.

## Changes made to the proposed line (no figure changed)

1. "under the earlier rule it was set aside, for two" to "under the earlier rule it was set aside, leaving two": "for two" read as a fragment.
2. "a captcha on a journal's contact form, reached now that the study follows robots.txt redirects, which we don't think is a wall" to "a captcha on the contact form of a journal's page, which the study reaches now that it follows robots.txt redirects and which we don't think is a wall": the captcha sits on the publisher's page about the journal (checkpoint, Flag for review: P31), and the old "which" could attach to the redirects.
3. "are now out of sight under the provider robots.txt rule described above" to "are now kept out of sight by the robots.txt rule described above": "provider robots.txt rule" is house shorthand; the paragraph above says what the rule is.
4. "whose echoed addresses are Google's" to "whose echoed addresses are registered to Google": matches what RDAP shows and the parallel "registered to Anthropic", without implying the addresses are Google's own machines.

## Placed as cleared

Investigation page, new bullet directly after the closing web's baseline bullet (after its amendment 5 paragraph), as R-0072 and R-0084 advised:

> - **Reviewed working read (an evidence review and a reader-and-inference review). Load: the closing web, read 1 (15 November).** A week after the baseline, the study's labelled requests found three services that had answered openly now refusing them: PubMed, with a bare 403, and two journals drawn at random, with a 403 naming Imunify360's bot protection. Crossref's API, rate-limited at the baseline, answered. By the study's definitions that's three closings and one opening, but one of the closings, a journal reached by plain HTTP, counts only under a rule for changing addresses that we fixed after seeing this read; under the earlier rule it was set aside, leaving two. Of the services our requests could read, 11 of 68 named and 6 of 31 drawn showed a wall, and those totals don't compare one to one with the baseline's: two of the drawn walls are new only because the study now reads differently (a page that sends readers straight to a captcha, which a rule adopted after the baseline counts as a challenge, and a captcha on the contact form of a journal's page, which the study reaches now that it follows robots.txt redirects and which we don't think is a wall), and Maven Central's two hosts, walled at the baseline, are now kept out of sight by the robots.txt rule described above. PubMed's refusal and one journal's met requests from the address block registered to Anthropic; the other journal's request went by the plain-HTTP route, whose echoed addresses are registered to Google, though its own address isn't known. So one request can't say whether a refusal is set for us or for everyone. Read 2 on 22 to 24 November says whether any of it holds ([checkpoint](../studies/LH044/checkpoints/2026-11-15.md)).

programme.md, replacing "has an unreviewed baseline and reads weekly from 15 November to 7 February 2027.":

> [LH044](studies/LH044/brief.md), the closing web, has an unreviewed baseline and a reviewed first weekly read ([checkpoint of 15 November](studies/LH044/checkpoints/2026-11-15.md)), and reads weekly to 7 February 2027.

The front page carries no LH044 line; nothing there changes.

## Not checked

No kept response body was reopened here; the Imunify360 wording, the P31 page and the echoed addresses were taken from the checkpoint's description, which R-0072 checked against the bodies. The rendered site was not viewed.

## Verdict

**Cleared**, with the four wording changes above. No must-fix finding remains: the line meets both of R-0080's must-fixes, every figure matches the retained data, and the checkpoint edits stand as written.
