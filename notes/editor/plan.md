title: The editor's visit
kind: working plan
date: 2026-11-07

# The editor's visit

**Set 7 November 2026, at the keeper's request.** Lighthouse is part science (studies and their reviews), part news of what is happening (watches, sweeps, the daily log) and part an account of how things are (pieces and the current account). The editor's visit checks, once a day, that the site shows all three to someone who arrives knowing nothing, the way an editor at an online newspaper looks at the front page. It is the last step of every scheduled run (schedule/runner.md, step 7), after that run's own work is live.

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

It keeps screenshots only in the scratchpad, not the repository. It is told not to read keys from the environment, to keep searches out of harbour/.session/, and not to commit.

## The editor

The run that dispatched the reader then acts as editor, reading the reader's answers beside what the run itself knows:

- **Check the plain openings.** Every study on the front page should open with an "In short" paragraph that a newcomer can follow (AGENTS.md, Writing). Write a missing one from the document's own text, or rewrite one that reads stiffly or has drifted from its record.
- **Fix small things now:** a broken link, a stale date, a layout fault, a missing label in site/sections.md (each study on watch has a short label there, "studies/LH0xx | label"). AGENTS.md: fix small things without filing them.
- **Keep the front page current,** which is ordinary work: README.md's lead and deck among released findings, its introduction when the investigations change, the investigation pages. A released piece's prose is never changed here; that goes through its reviews.
- **Coverage of what is happening.** If a watch, the daily log or a sweep turned up something a reader should see today and the front page does not show it, the editor says so. Unreviewed material is shown only in the Now box, labelled; anything stated as a finding needs a piece and its reviews, so the editor adds a proposal (kind: piece) for a reviewed note, urgent where the news is time-bound. Lighthouse's own claim of harm or compromise still waits for the keeper.
- **Everything larger** (a missing page, a confusing piece, an unanswered reader question) goes to proposals.md as a lead or proposal (kind: editorial), for the next sweep's gate.

## The note

notes/editor/`<UTC label>`.md: the reader and the time, the front page as seen (the Now box and the Latest list, in a few lines), the reader's answers, what the editor fixed, what it proposed, and the spend.

## Limits

One reader a day, an agent playing a part: it is a check on the site's clarity and currency, not a survey of readers. It sees the site as it was after the run's work went live, so the next visit is the first to see the editor's own fixes.
