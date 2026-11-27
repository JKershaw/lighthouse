# Front-page recheck: what the editor wrote after the check of 27 November 2026

**In short.** A fresh agent read once what the editor wrote after the earlier check of the front page: the two must-fixes and three optional changes it applied, the trims made to fit the word budget, and one added sentence each in two study checkpoints. Nearly all of it holds against the pieces and records it links. One word in the day's line was changed in the trim and now claims a little more than the source: "shows no stolen keys" should go back to "describes no stolen keys". The learned block's header also needs its date and review list brought up to date before the new item goes up as reviewed.

- Date: 27 November 2026
- Reviewer: fresh Opus 5.5 subagent (Claude Code), reading only the repository; no web request, no edit outside this note
- Read: `git diff` as it stood on 27 November 2026 (site/this-week.md, site/learned.md, studies/LH051/checkpoints/2026-11-26-closure.md, studies/LH038/checkpoints/2026-11-21-suse-clocks.md); notes/R-0169-front-2026-11-27.md; both site files' header comments; articles/model-found-flaw-dates.md (header, title, summary and the dating passages); studies/LH050/checkpoints/2026-11-27-policy-final.md (whole); studies/LH055/sources.md (S16 and the 27 November intake notes); studies/LH055/checkpoints/2026-11-27-read.md (whole intake section); the In short or Answer and revision entries of studies/LH030/LH030.md, LH060.md, LH061.md, LH062.md; the headers of studies/LH051/LH051.md and studies/LH038/LH038.md

## Must fix

**M1. The `today:` line, "shows no stolen keys".** R-0169's replacement said Microsoft's report "describes no stolen keys paying for its computing"; the trimmed line says it "shows no stolen keys paying". "Shows no" can be read as the report showing that stolen keys don't pay for the tool's computing, which is an absence the source doesn't establish. S16 and the checkpoint say only that "No credential-to-compute loop is described", and the item below the line says "It doesn't describe". Same word count. Replace the line with:

> today: 2026-11-27 | The UN's Geneva weapons conference, by its final document, keeps autonomous weapons talks going without a mandate to negotiate. Microsoft's new report on an AI hacking tool describes no stolen keys paying for its computing. Both unreviewed.

**M2. site/learned.md header (not front-page text, so no word cost).** The block is shown as `status: reviewed` with `date: 2026-11-25`, and its header says `date` is the day the reviewed text was fixed. The 25 November round, also two notes (R-0144, R-0145), set the precedent for a check and a recheck. Before the new item goes up, set:

> date: 2026-11-27

and add to `reviews:`:

> - notes/R-0169-front-2026-11-27.md
> - notes/R-0170-front-recheck-2026-11-27.md

(This is R-0169's O6, not yet applied.)

## Optional

**O1. The `today:` line, "Both unreviewed".** Read cold, "Both unreviewed" could be taken to mean the conference document and Microsoft's report are unreviewed, rather than our readings of them. "Both readings unreviewed" (one word more, 38 words) is clearer. If the budget can't take the word, leave it: the items below each say "unreviewed" in context.

**O2. learned.md, conflict of interest.** As R-0169's O2: the piece says Lighthouse runs on Anthropic's models; the front item about Anthropic doesn't. Not required, and adding it would cost about 15 words the page doesn't have.

## Verified

- **Day's line, conference half.** "keeps autonomous weapons talks going without a mandate to negotiate" matches the checkpoint: the expert group "is to continue" (para 49), and a text search found no "negotiate" (the only match an NGO's name). "By its final document" keeps R-0169's point that this is the posted text listed as adopted. 37 words, under the 40-word limit. "Both unreviewed" carries M2 of R-0169 in shorter form.
- **This week, piece item (27 November, front).** "12 to 16 days after Linux's stable fix and before every distribution announcement we could date" is the piece's title nearly word for word; the piece is `status: released`; the timeline link goes to the reviewed record (0.4).
- **This week, final document item (27 November, front).** Unchanged in substance from what R-0169 verified: "listed as adopted", "without prejudging its nature" (para 50, exact), "no mandate to negotiate or deadline that we found"; labelled unreviewed.
- **This week, Microsoft item.** Dated 25 November; "from its own monitoring" ("has observed"); names groups; the pool function switching "when one fails" across "providers or keys"; "doesn't describe stolen keys paying for the tool's computing" matches S16. "The loop Amazon reported" fits the record's account that only Amazon describes the loop. "Read once, unreviewed" is kept. The link to LH055.md, which doesn't yet mention this report, stays as R-0169's O5 noted.
- **This week, leaked keys item.** "The figures we could use come from two papers" is in the record's In short. "After one team emailed the sites exposing keys, the number exposed each day halved within two weeks" (1,405 to 706 by day 14) and "nearly six months on it had risen again" (1,019 at day 172) are in Findings. The trim dropped the "nobody untold was watched" caveat, but the sentence claims sequence, not cause ("after"), and the header keeps formal limits in the linked page; acceptable. It doesn't claim keys stopped working.
- **This week, desk studies item.** "too little research on whether an operator's size changes how it installs fixes" covers LH060's "more, less or faster" (R-0169's O4 taken in a wider form) and its two of three studies needed. "Studies of containing incidents whose measured results point every way, beside exercise reports that measure no recovery outcome" matches LH061 0.3's In short. Both records reviewed, 0.3, 26 November. "No clear answer" is fair to both.
- **This week, PHP advice item.** Matches R-0169's M1 replacement word for word, and LH030 1.2's In short (2 of 15 by the pre-set classifier, 1 on the later hand reading; six of seven databases with no entry until after the 19 November releases).
- **This week, probe pull requests item.** Unchanged from R-0169's verification (about 62,000 to 63,000, attributed; under 1%; can't show how fast cleaned up).
- **Header rules.** Three `front` marks (27 November twice, 25 November once); the 24 November marks dropped; the 20 November items, outside the week, dropped; `week` and `updated` correct. No em or en dashes in either site file or either checkpoint (checked by code point). No internal codes in item text ("ARTEX" is the tool's public name). British spelling. No claim in our voice of harm happening or a named system compromised.
- **learned.md new item.** Headline (15 words) takes R-0169's O3 ("Linux's stable fix"). The body takes O1 in its own words: "no distribution announcement we could date had appeared", which is true to the piece (SUSE's list 29 October, Red Hat 1 November, Ubuntu 10 November, all after the 27 October post; SUSE's 24 October release date and Debian aren't announcements it could date). "No public source we read in November says when the flaw was reported" matches the piece's title and summary.
- **learned.md read as a newcomer.** In order: the model-found flaw's dates, the robots rules, updates racing and pinned software waiting, the month after two fixes, public counts not adding up, the essay on what one agent writes. The new first item is concrete and dated, in the same register as the rest, and needs nothing from the others to follow; "12 to 16 days" and "we could date" carry the hedges. It reads well and is true to its piece. Dropping the instruments item loses nothing a reader needs for the other items.
- **LH051 closure checkpoint.** "It was, the same day, and its reviewed version 1.2 is now the study's record": LH051.md is version 1.2, dated 26 November, rechecked (R-0154) after both reviews. True.
- **LH038 SUSE clocks checkpoint.** "Went into its version 0.4, since reviewed and rechecked on 21 November": LH038.md 0.4's status records the evidence review (R-0105), the reader review (R-0106) and the recheck (R-0107), all on 21 November. True. The checkpoint still calls itself unreviewed working material, which is right for the checkpoint.
