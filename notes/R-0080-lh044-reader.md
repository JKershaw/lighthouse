# Reader-and-inference review: LH044 read 1 checkpoint (15 November 2026)

**In short.** A fresh reader-and-inference review, under notes/reader-review.md, of the LH044 read-1 checkpoint as it stands after its evidence review and brief amendments 7 to 9, and of any change it proposes to a public page. Stage 1 below was written after reading only the checkpoint; stage 2 then read the brief, the study's data and scripts, the evidence review's amendments and the public pages that mention LH044. Verdict at the end.

Reviewed version: studies/LH044/checkpoints/2026-11-15.md as last changed in commit 94b8ef803b4d4ece2c85e0d19349a1903eb7841f (16 November 2026, "LH044 amendments 7 to 9 (post hoc, after R-0072)"), read at repository HEAD 7be99531357aef10105bf9ee6d0fbd764155dd27 on 17 November 2026. Reviewer: a research subagent in Claude Code (Claude Opus 5.5) for the scheduled run of 17 November. The checkpoint was not edited.

## What a reader would believe, written before reading the record

(Read: the checkpoint file only. The pre-reading also included notes/reader-review.md, AGENTS.md and a listing of the study's directory and of notes/ file names, none of which describes LH044's results.)

A careful reader would say back: "A week after a first look, Lighthouse asked the same set of shared online services (archives, documentation sites, code forges, mirrors, open data, package registries, and a random set of journal and mirror sites) for their robots.txt and, where allowed, one labelled page. About one in six of the named services it could read (11 of 68) and about one in five of the random ones (6 of 31) put a wall in front of it. Three services that were open last week refused it this week, PubMed among them, and Crossref's API, walled last week, answered."

Observed: what one request from one address saw at each service, on two dates. Explained: little; the checkpoint explicitly does not explain the walls. The Crossref statements predate the study, PubMed and the journals said nothing findable. Caused: nothing is presented as caused; the reader is told a 403 to Anthropic's address block cannot be told apart from a wall for everyone, that nothing is said about AI traffic or harm, and that one week cannot say whether any change holds.

Limits a reader would notice: one request per service per read; the drawn stratum's unknown share over a fifth; the classifier changed between reads; the third closing depends on a rule amended after the read was seen; the drawn wall count rose from 1 to 6, and the checkpoint's opening does not say how much of that is walls going up and how much is new probes, redirects now followed and a classifier change; the body's list of walls lets a careful reader work it out. A reader skimming the opening might take "11 of 68" and "6 of 31" as walls against everyone, or as a rate across the web, rather than what one Anthropic-registered address saw.

## Stage 2: what was read

The brief (protocol 0.1 and amendments 2 to 9), the evidence review notes/R-0072-lh044-read-01.md and the fresh reading of its resolution notes/R-0076-lh044-amend.md (both named by this task, so unlike the usual dispatch this reviewer knew the evidence review's verdict before stage 2), studies/LH044/for-driver.md, both reads' classes.csv and read 1's readlog.csv, the investigation page investigations/ai-cost-and-spread.md (its LH044 lines) and programme.md's LH044 lines, and schedule/due.csv's LH044 rows. `git diff --stat 94b8ef8 HEAD -- studies/LH044` is empty, so the checkpoint and its data are as R-0076 cleared them. No network request was made.

The one tally made here, from the two classes.csv files (walls are the brief's six wall classes; offline, Python, not kept as a file since this task names only the note):

```
for each id walled at either read: baseline class -> read-1 class
drawn: P04 open_unconfirmed -> wall_at_robots (captcha-refresh)   P17 gone -> refused
       P31 robots_redirect -> wall_at_robots (recaptcha)          P34 wall_at_robots -> wall_at_robots
       P38 open -> refused                                        P40 open -> refused
named: A11 open -> refused; A13 wall_at_robots -> open; A16 robots_disallowed -> wall_at_robots;
       A20 rate_limited -> gone; R06, R07 rate_limited -> robots_disallowed; seven walled at both
```

## Proposed public-account changes

The checkpoint itself proposes no change to any public page; its own text is a working document that the site shows on the study's page. The only proposed public wording for read 1 is R-0072's suggested investigation-page line ("**Load: the closing web, read 1 (15 November).** ...", R-0072, section "The investigation page"), to be added "once released". Nothing about read 1 is on the investigation page, programme.md or the front page yet (the investigation page's only read-1 mention is amendment 5's rule, written 8 November). Row LH044-read-01-resolution-recheck follows this one and says no public line changes until the checks clear.

## What the round establishes

What one request from each panel service saw on 15 November against 8 November, under a protocol fixed beforehand and amended, with each amendment dated and labelled post hoc. Supported: 11 of 68 readable named and 6 of 31 readable drawn services walled (classes as read, classifier 0.3); PubMed, P38 and P40 open at the baseline and refused at read 1, Crossref's API the reverse; three closings and one opening under amendment 9, two under the earlier reading of the egress rule, both kept in the checkpoint; no wall dated; no operator statement explaining any change. The checkpoint attributes nothing, explains nothing and says one week cannot say whether anything holds. The measurements could be right while an explanation is wrong only where a reader supplies the explanation: that walls went up, or that they are aimed at Anthropic or at everyone. The checkpoint's body guards against both; its opening is thinner (Readability 1).

## Material claim problems

**In the checkpoint: none.** Each count in the opening matches classes.csv; the corrections and amendments are labelled and the earlier editions linked; the post hoc egress reading is labelled, with the earlier count kept; the P31 and P04 cases are set out wall by wall; the model disclosure and "nothing here attributes any traffic" stand. I found no wording easier on Anthropic than the evidence allows, or harder.

**In R-0072's proposed investigation-page line: two, material if the line is published as written.** They are must-fix only for whatever line the resolution row writes; if no read-1 line is published, they block nothing.

1. **The closing count is stale.** Passage (R-0072, "The investigation page"): "Under the brief that's two closings and one opening, with a third closing held out because our plain-HTTP requests left from a different registered block of Google's." Evidence: brief amendment 9 (16 November, post hoc) compares the plain-HTTP route by registrant, Google LLC at both reads, so the checkpoint's amended count is 3 closings (A11; P40 and P38) and 1 opening, with 2 under the earlier reading (checkpoint, Changes; R-0076 point 4). R-0072's own interim advice ("any public line gives the closings as 2") predates amendment 9. A reader of the line would believe the brief's rule set P38 aside, which is no longer the rule in force. Resolution: give three closings and one opening, say the rule that admits the third was fixed after this read was seen, and keep the two under the earlier reading.
2. **The drawn wall count invites a reading of walls going up that the record does not support.** Passage: "11 of 68 named and 6 of 31 drawn showed a wall (5 of 30 if a captcha on one journal's contact form isn't counted)", placed under the baseline line on the same page, which gives "1 of 26 drawn at random". A reader comparing the two lines would believe walls in the drawn stratum went from 1 to 6 in a week. Evidence (classes.csv, tally above): of the five drawn services walled at read 1 and not at the baseline, two are changes in the instrument, not in the service: P04's captcha-refresh page was `open_unconfirmed` under classifier 0.2 and is a wall under 0.3 (checkpoint: "at the baseline the same kind of page was `open_unconfirmed`"), and P31 was unread at the baseline (`robots_redirect`) and is reached now only because redirects are followed (amendment 3), its "wall" a contact-form captcha both the writer and R-0072 read as not a wall. The other three (P38, P40 open before; P17 a 404 before) did answer differently. The named count's fall from 13 to 11 has the same kind of mix: Maven Central's two hosts left the walled count because amendment 5's rule now withholds their probes, not because their walls came down. Resolution: say in the line that two of the drawn stratum's new walls come from changes to how the study reads, not from the services, and (suggested) that Maven's two hosts are now out of sight by rule.

A wording that would meet both, offered to the resolution, not adopted here: "**Load: the closing web, read 1 (15 November).** A week on, of the services one labelled request could read, 11 of 68 named and 6 of 31 drawn showed a wall. Of the drawn ones, two weren't walls a week earlier only because the study read them differently: one is a captcha on a journal's contact form, which we don't think is a wall, and one a page a new rule now reads as a challenge. Three services that answered openly at the baseline refused: PubMed, with a bare 403, and two drawn journals, through Imunify360's bot protection. Crossref's API, rate-limited at the baseline, answered. That's three closings and one opening, counting one closing on our plain-HTTP route under a rule for changing addresses that we fixed after seeing this read (two under the earlier rule). PubMed's refusal and one journal's met a request from an address block registered to Anthropic, the other journal's one from an address registered to Google, so one request can't say whether a refusal is set for us or for everyone. Read 2 on 22 November says whether any holds ([checkpoint](../studies/LH044/checkpoints/2026-11-15.md))." Its route attributions are from classes.csv (A11 and P40 egress-proxy, P38 direct-http); it should be checked against the record by the recheck like any resolution text.

## Readability (optional)

1. The checkpoint's opening says PubMed "refused us with a bare 403, as did two drawn journals". The journals' 403s were not bare: they named Imunify360. And the opening does not say that most requests leave from Anthropic's address block, the main limit on reading any 403, which the brief's own opening states. A clause ("from an address block registered to Anthropic, so we can't tell a wall for us from one for everyone") would carry it to readers who stop at the opening. Not material: "refused us" is accurate, and "one week can't say" is there.
2. The opening's "6 of 31 drawn" could carry "(two of them new only because the study now reads them differently)", for the reason in problem 2.
3. A labelled interpretation worth adding at read 2's checkpoint or the record: two of the three Imunify360 refusals (P38, P17) met plain-HTTP requests from Google-registered addresses, so those walls are not specific to Anthropic's block, whatever else they are keyed on.

## Next step

Read 2 on 22 to 24 November is the right next step and needs no change: it is the only evidence that can say whether the three closings and the opening hold, which is the question the checkpoint leaves open, and it runs with classifier 0.4 and amendments 7 to 9 already in force. It cannot tell a wall set for Anthropic's block from one for everyone; nothing within the brief's two requests per host can, and a second vantage would need its own amendment and the keeper's decision, which I don't think one week's three closings yet justify. Two small things for read 2's writer: tally walls both as read and on a like-for-like basis (services read by the same rule at both reads), so instrument changes stop showing up as walls going up; and resolve whether ai.robots.txt release 2.1 carries `__usage_ai-training` (the checkpoint and the gate disagree, and the kept body answers it without a request).

## Verdict

**Checkpoint (studies/LH044/checkpoints/2026-11-15.md at 94b8ef8): cleared.** No must-fix finding in its text.

**Proposed public account (R-0072's investigation-page line): not cleared as written.** Two must-fix findings (problems 1 and 2 above) bind any read-1 line the resolution row writes. Publishing no read-1 line is also a resolution; then nothing here blocks.

I edited no file but this note.
