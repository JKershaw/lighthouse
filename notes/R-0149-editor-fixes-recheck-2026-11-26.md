# Recheck of the editor's fixes after the check of 26 November 2026

**In short.** A fresh agent read the applied text once: the front page item for the map of who watches the internet, the opening of the investigation page on what AI activity costs the shared internet and its lines for the Amazon flaw study and the defensive-side study, and the plain opening of the closing web's brief. The headline, blurb, investigation opening and study lines are accurate against their sources and at the same certainty as AGENTS.md and programme.md. One must fix: the brief's opening now says the investigation page holds "the reviewed parts" of the closing web's reads, but the page also carries the baseline, labelled unreviewed. One optional change restores "spreading" to the investigation's opening.

Rechecker: a subagent of the driving session, Claude Code, Opus 5.5, 26 November 2026. No web requests, no credentials read, nothing edited but this note. This is the one reading after a review round, not a chain; the changes below are listed for the driving session, not sent to another reader.

## What I checked

- **The note and the diff.** notes/R-0148-editor-fixes-2026-11-26.md and scratchpad fix2.diff: the must-fix and all three optional changes were applied word for word. No added line has an em or en dash or an internal code in prose (study codes appear only in link targets).
- **site/learned.md.** The headline "Of 48 public watchers we found in November 2026, none saw the whole of its layer" and the blurb's "none that saw the whole of its own layer" match articles/who-watches-the-internet.md's title, summary ("none saw the whole of its layer") and body ("What goes unwatched is narrower than a layer"). The absolute carries its window and "we found". Tense now agrees.
- **investigations/ai-cost-and-spread.md, In short.** articles/rules-for-robots.md is released (19 November 2026, this investigation); its subject is what sites ask, how published counts say crawlers heed it, and how our own 3,497 requests of 8 November fared (113 broke a rule), so "the web's rules for robots and how well our own agents kept them" is fair and no longer reads "follow" as "obey". "None of it yet says what AI activity costs shared infrastructure, or whether any of it keeps itself going" doesn't contradict the reviewed lines below it (closing web read 1, the registry worms, LH052's organisational record, ARTEX round 2): none of them measures cost or self-sustaining activity, and the page's own preamble says nothing below is evidence of AI activity sustaining or spreading itself. It matches AGENTS.md's Where things stand ("its one released piece is the paper on the web's rules for robots") and programme.md line 99, whose "Answered" studies (LH043, LH046, LH047, LH052) answer sub-questions, not the question itself. The new sentence names only "keeps itself going", where the page's first sentence and the line above ask "keeping itself going or spreading"; see Optional.
- **Lines 7 and 8 (LH059, LH061).** studies/LH059/data/read-2026-11-25T1415Z/ exists; studies/LH061/ holds searches.md, fetchlog.csv, claims.csv and derived/; schedule/runs.csv's run of 25 November 14:12 UTC records the LH059 first read and the LH061 searches and reads as unreviewed. Both lines are accurate.
- **studies/LH044/brief.md, In short.** studies/LH044/checkpoints/ holds 2026-11-08.md (baseline), 2026-11-15.md (read 1) and 2026-11-22.md (read 2), so "weekly reads followed from 15 November" is right. The investigation page carries the baseline (line 38, opening "**Unreviewed. Load: the closing web, baseline.**") and read 1 (reviewed), not read 2. "The reviewed parts on the investigation page" therefore says the page holds only reviewed parts, which its baseline line contradicts.

## Must fix

1. studies/LH044/brief.md, In short. Replace

   `what they show is in the study's checkpoints, and the reviewed parts on the investigation page, not in this brief.`

   with

   `what they show is in the study's checkpoints, and the baseline and the first weekly read on the investigation page, not in this brief.`

## Optional

1. investigations/ai-cost-and-spread.md, In short, to keep the question's two halves together. Replace

   `or whether any of it keeps itself going.`

   with

   `or whether any of it keeps itself going or spreads.`

## Changes made by this reading

None to the checked files. This note is the only file written.
