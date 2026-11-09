<!--
This file is the front page's "This week" block (read by site/lib/front.js,
thisWeek; shown by site/_includes/home-this-week.njk). It is kept here, in one
place, by the scheduled run at its editor's step (schedule/runner.md, step 7),
and by any session that releases, opens or decides something a returning
reader should hear about.

Each time you update it:
1. Set `updated` to today (UTC, YYYY-MM-DD) and `week` to the seven days
   ending today: "<today minus 6 days> to <today>".
2. Drop items dated before the week's first day. The site hides them anyway,
   and hides the whole block when `updated` is more than 8 days before the
   build, so a missed update shows nothing rather than an old week.
3. Add one item for each thing since the last update that a returning reader
   would want: a piece or essay released or corrected; an investigation
   opened or closed; a study begun (its brief fixed) or answered; a keeper
   decision that changes what Lighthouse does; an outside event Lighthouse
   follows. Not routine reads, checkpoints that change no account, or process.
4. Write each as `- YYYY-MM-DD | reported | sentence` for something others
   published (say who, and link their page or our record of it), or
   `- YYYY-MM-DD | lighthouse | sentence` for our own work (link the page).
   One or two plain sentences in Markdown, repository paths from the root.
   No internal codes (no LH, P, R or L numbers, row ids, step numbers or file
   names in the text), British English, no em or en dashes, no figure that is
   not in a released piece or the cited source, and no claim in our voice that
   harm is happening or that a named system is compromised.
5. Newest first, at most six items; drop the oldest beyond six.

The block shows no finding. Whether the editor may change it without review is
the gate's decision on proposals.md P-0018.
-->
title: This week
week: 2026-11-03 to 2026-11-09
updated: 2026-11-09
items:
- 2026-11-09 | lighthouse | We added a later-evidence notice to [who watches each layer of the internet](articles/who-watches-the-internet.md) and to [what we can see](articles/what-we-can-see.md): GH Archive's hourly files of GitHub's public events were all there in 2026, but whole kinds of event were missing from many of the hours we read, and nobody yet knows whether GitHub's feed or the archive lost them.
- 2026-11-09 | lighthouse | We fixed the plan for a new study of [the flaws behind Anthropic's five attack chains](studies/LH048/brief.md): how each is rated and whether the public signals of exploitation move, read on Mondays to 4 January. Only two of the five flaws are named by number in Anthropic's post.
- 2026-11-09 | lighthouse | From today our collectors ask a site's robots.txt before each request; a few one-off and review reads still don't share that check. Some sources we used to read now ask automated readers to stay away, among them WordPress.org's statistics and Node.js's release list, so those readings stop.
- 2026-11-08 | lighthouse | We published a second essay, [What the watch would see of a pattern that copies itself](essays/what-the-watch-would-see.md): an invented case walked through the public records, showing where copies would leave traces and where nothing would.
- 2026-11-08 | lighthouse | We published an essay, [It was only a test](essays/it-was-only-a-test.md): what one agent leaves behind, a message board or a handover note, can become part of another's world.
- 2026-11-08 | lighthouse | We opened a third investigation, [what AI activity costs the shared internet](investigations/ai-cost-and-spread.md), and whether any of that activity is sustaining or spreading itself outside a lab. Its first study, on shared services withdrawing anonymous access, is due to start from 9 November.
