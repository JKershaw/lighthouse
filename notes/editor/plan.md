title: The editor's visit
kind: working plan
date: 2026-11-07

# The editor's visit

**Set 7 November 2026, at the keeper's request.** Lighthouse is part science (studies and their reviews), part news of what is happening (watches, sweeps, the daily log) and part an account of how things are (pieces and the current account). The editor's visit checks, once a day, that the site shows all three to someone who arrives knowing nothing, the way an editor at an online newspaper looks at the front page. It is the last step of an Editor run, or of the compatible all-purpose runner (schedule/runner.md, step 7), after the relevant work is live. Watch, Research and Horizon do not dispatch the reader or regenerate the editorial digests. This prepares the split; it changes no external trigger.

## Ownership and handover

The daily Editor run reads the intervening run records and retained outcomes since the last visit, not just its own commits. It owns `site/this-week.md`, the front-page presentation and the upkeep of `site/learned.md`. Refresh and merge main before editing these files; retain newer editorial items, dates and reviews rather than restoring a snapshot from another role's earlier checkout. Research still performs the reviewed publication and required public corrections; a necessary correction to a digest is a minimal reviewed patch, not a second editorial visit.

Before dispatching a reader, check today's retained visit note and active Editor run records on main. If today's visit is already complete, retain its result and do only remaining claimed maintenance. Rollout should use one Editor trigger per UTC day and avoid overlapping Editor/all-purpose runs. This PR does not add a separate visit lock or queue row; retry an interrupted visit from its retained note, and reconcile ambiguous active ownership before dispatching another reader.

## The reader

A fresh agent that has not seen the repository or the run's work is given only the site's address, https://lighthouse.harbour.cat, and today's reader:

| Day (UTC) | Reader |
| --- | --- |
| Monday | a curious newcomer who has never heard of Lighthouse |
| Tuesday | a journalist looking for a story and a source to quote |
| Wednesday | someone who runs servers and wants to know what to do |
| Thursday | a sceptic looking for overclaiming |
| Friday | a researcher who wants the data and the method |
| Saturday | someone checking back after a week away |
| Sunday | a reader on a phone with five minutes |

It reads the site in a browser (Playwright, preinstalled), at phone and desktop width, in light and dark, starting from the front page and following what that reader would follow, for about twenty pages at most. It does not read the repository. It answers, in its own words:

1. What is this, and why should I care?
2. What is happening now, in the world and in Lighthouse's work, and could I tell from the front page?
3. What changed since the last visit (it is given the last visit note's "front page as seen" section, and nothing else from it)?
4. What would I read first, and did it deliver?
5. Do I trust it? What made me trust or doubt it?
6. What confused me, looked stale, contradicted another page or broke?
7. What did I want to know and could not find?
8. What on the front page looked cheap, cluttered or out of place (the keeper, 18 November 2026)?

It keeps screenshots only in the scratchpad, not the repository. It is told not to read keys from the environment, to keep searches out of harbour/.session/, and not to commit.

## The editor

The run that dispatched the reader then acts as editor, reading the reader's answers beside what the run itself knows:

- **Check the plain openings.** Every study on the front page should open with an "In short" paragraph that a newcomer can follow (AGENTS.md, Writing). Write a missing one from the document's own text, or rewrite one that reads stiffly or has drifted from its record.
- **Fix small things now:** a broken link, a stale date, a layout fault, a missing label in site/sections.md (each study on watch has a short label there, "studies/LH0xx | label"). AGENTS.md: fix small things without filing them.
- **Keep the front page current,** which is ordinary work: README.md's introduction when the investigations change, and the investigation pages. The lead story chooses itself: the newest released finding or essay. Pin a different one only for a reason a reader would see (a correction, or news that makes an older piece the one to read), with `lead:` and `lead until: YYYY-MM-DD` (and, if needed, `deck:`) in README.md's header, at most two weeks ahead, and say why in the visit note; the pin lapses by itself. A piece shows its first illustration on the front, or the one its header names with `front figure:` (a path as written in its body), which is metadata, not prose. A released piece's prose is never changed here; that goes through its reviews.
- **Check the front page against its rules** (site/README.md, "Front-page rules"; the keeper, 18 November 2026) before committing any change to what it shows. Changing its layout or adding a section is a keeper decision.
- **Coverage of what is happening.** If a watch, the daily log or a sweep turned up something a reader should see today and the front page does not show it, the editor says so. Unreviewed material is shown only in the Now box, labelled; anything stated as a finding needs a piece and its reviews, so the editor adds a proposal (kind: piece) for a reviewed note, urgent where the news is time-bound. Lighthouse's own claim of harm or compromise still waits for the keeper.
- **Everything larger** (a missing page, a confusing piece, an unanswered reader question) goes to proposals.md as a lead or proposal (kind: editorial), for the next sweep's gate.

## Daily updates and release checks

Once the site build for the run's commit has succeeded and the site shows it, a fresh agent visits the live site as today's reader and the run acts as editor on what it reports: fix small things, keep the front page current (including `site/this-week.md`, below), propose coverage of what a reader should see and cannot, and write the visit note. Commit the note and any fixes once more, fast-forward main and check the build. Check that AGENTS.md's "Where things stand" reflects intervening starts, closures, releases and changes of investigation state, replacing anything out of date (the keeper, 17 November 2026). A run that cannot start a fresh agent skips the visit and says so in its line in `runs.csv`. At the same step, update `site/this-week.md` as its header comment says (the keeper, 8 November 2026): set `updated` to today and `week` to the seven days ending today, drop items from before the week, and add an item for each thing a returning reader should hear about since the last update (a piece or essay released or corrected, an investigation opened or closed, a study begun or answered, a keeper decision that changes what Lighthouse does, an outside event Lighthouse follows), labelled `reported` or `lighthouse`, in plain words with no internal codes; mark up to three as `front`, the ones a returning reader most needs, and link a reported item's own source as well as our record (the keeper, 18 November 2026). If nothing new happened, still set `updated` and `week`, so the block does not disappear while its items are within the week. Write for a person, not an agent (the keeper, 13 November 2026): lead with what happened and why a reader might care, and keep any caveat to one short clause.

   At the same step (the keeper, 13 November 2026), two more things on the front page. **The day's line:** in site/this-week.md's header, set `today: YYYY-MM-DD | one or two plain sentences` saying what the runs read that day, in words a person would use, at most about 40 words (the keeper, 18 November 2026), naming nothing a newcomer couldn't follow (say "an attack operation run through AI agents", not its codename), with no figure that is not in a retained read and no internal codes; the site shows it labelled Live and hides it two days after its date, so a day with no retained reads leaves it alone. **What we've learned so far** (site/learned.md, the front page's opening): when intervening runs released a piece or essay, or a correction or later-evidence notice changed one the block retells, draft the change as the file's header comment says (a new item retelling the piece, replacing the weakest, or a corrected sentence), have a fresh agent check every changed sentence against its piece and then read the block as a reader would, apply what they find, and only then commit it, with the reviews as notes in notes/ named in the file's `reviews` and its `date` set to the day. The editor's visit says so when a released piece is more than a week newer than the block's `date` and not in it.


## The note

notes/editor/`<UTC label>`.md: the reader and the time, the front page as seen (the lead story and why it leads, This week's three, and each investigation's Latest line, in a few lines), the reader's answers, what the editor fixed, what it proposed, and the spend.

## Limits

One reader a day, an agent playing a part: it is a check on the site's clarity and currency, not a survey of readers. It sees the site as it was after the run's work went live, so the next visit is the first to see the editor's own fixes.
