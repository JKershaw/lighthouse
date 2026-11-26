# Recheck of the front page's "This week" changes of 26 November 2026, after R-0146

**In short.** A fresh agent read once the text written to resolve the check of today's This week block: the day's line and the new UN item of 26 November. Both are accurate against the reads they rest on, and "the session flaw PHP warned of in October" does pick out the flaw Google's 23 November update added, CVE-2026-115560, and not the other November session flaw. Nothing must be fixed. One optional change would bring the day's line into step with the item's "we plan to".

Rechecker: a subagent of the driving session, Claude Code, Opus 5.5, 26 November 2026. No web requests, no credentials read, nothing edited but this note. This is the one reading after a review round, not a chain.

## What I checked

- notes/R-0146-front-2026-11-26.md, and `git diff site/this-week.md` for the whole of today's change: the `week:`, `updated:` and `today:` lines, the new 2026-11-26 item and the removal of the four 19 November items. Must fix 1 and Optionals 1 and 2 are applied word for word.
- **The UN sentence of the day's line and the UN item**, against studies/LH050/checkpoints/2026-11-26-read.md and studies/LH050/reads.csv row LH050-R064. The page "took place" (on 21 November "will take place") and lists "CCW/CONF.VII/CRP.1/Rev.3 - Final document - as adopted": both in the checkpoint and the ledger row. "which it didn't on 21 November": the checkpoint compares with LH050-R048 of 21 November and calls the entry new. "We haven't read it yet, so we can't say what, if anything, it says about autonomous weapons": the checkpoint says the linked documents weren't fetched and that what the adopted document says about lethal autonomous weapons "is unknown from this read". "on 27 November": the final document check, row LH050-policy-final, is that date only, "subject to the robots gate", which the item's "we plan to" respects. The hyphen inside the quoted "Final document - as adopted" is the page's own hyphen-minus (R-0146 checked the byte), not a dash.
- **The PHP sentence**, against studies/LH037/checkpoints/2026-11-26T1414Z.md. GCP-2026-090 was published on 20 November for CVE-2026-126714 (studies/LH037/checkpoints/2026-11-23T1425Z.md); its update dated 23 November says the updated PHP versions "include updates against CVE-2026-126714, CVE-2026-115560, and other important security fixes". So "now", "patched PHP runtimes", "also" and "cover" are fair, and nothing about exploitation is said or implied (Google says nothing of it).
- **Which flaw.** PHP's notice of 23 October gave the instruction for CVE-2026-115560 until the next regular release (studies/LH030/LH030.md, In short and Answer; notes/php-watch-log.md throughout). CVE-2026-126714 ("phpAfterShell", in PHP's default file-based session handler) first appears in our reads in Google's bulletin of 20 November (studies/LH030/checkpoints/2026-11-23.md, Google Cloud row), and Cisco dates PHP's announcement of its fix to 19 November. No record I read has PHP warning of it in October. Both are session flaws (115560 is titled "Session serializer mismatch can lead to remote code execution"), but only 115560 was warned of in October, so the phrase identifies it uniquely, and it is the CVE Google's update added. It also avoids the "newer" ambiguity R-0146 found.
- **Readability and rules.** The day's line after the date is 41 words, within "about 40". No U+2013 or U+2014 anywhere in the file. No study codes, CVE numbers or internal names in the line. Nothing in our voice says harm is happening or that a named system is compromised; both sentences report what a page or a vendor says. British English. Read cold, the line makes sense to a newcomer; "also" leans on an unstated earlier statement, but "Google now says" carries it well enough.

## Must fix

None.

## Optional

1. **Match the day's line to the item's softer plan.** The item now says "we plan to read it on 27 November" because the read is subject to the robots gate at the time; the day's line still says "we'll read it". Replace

   `we'll read it on 27 November.`

   with

   `we plan to read it on 27 November.`

   (42 words in all.) Either wording is acceptable; this only keeps the two in step.
