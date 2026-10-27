# Lighthouse

AI systems now write code, run tasks and call one another across the internet, so the internet has become the world they work in. Nobody yet knows whether what they leave behind there could keep itself going and spread, and Lighthouse keeps watch so that one day it will be possible to tell.

No single instrument sees that world whole: a code archive, a download log, a package registry and an internet scanner each show one part of it, and each stops somewhere. Lighthouse sets those partial views side by side, says where each one stops, and publishes what the shape looks like once the work has been reviewed against its sources. Much of what it sees is ordinary software moving, because anything unusual would travel the same roads.

---

## The watch

### [A PHP emergency, from an early attack trace to published fixes](articles/php-emergency-first-reading.md)

Amazon's threat-intelligence team says a decoy server saw an exploit attempt dated 17 October, before PHP's security release on 21 October. OpenAI describes AI-assisted discovery and a coordinated defensive response; neither the honeypot report nor the public traffic accounts establish AI use by attackers. Selected official and derivative images had published fixed versions by our first observations, though a registry image does not tell us who is running it. On 23 October PHP described a further route to running code, unlikely by its account and open only in some unusually configured applications, which it is handling in its regular release cycle and which, its advice implies, the fixed versions do not close. On 26 October CISA, the US cybersecurity agency, listed both emergency flaws in its catalogue of known exploited vulnerabilities: a classification by criteria the catalogue does not state, not a count of attacks or proof that any succeeded.

[Our developing account](articles/php-emergency-first-reading.md), dated 22 October with later-evidence notices of 23 and 27 October, draws the visible clocks and the points where evidence stops, and will be revised as fixed sources change. [The daily log](notes/php-watch-log.md) holds what those sources show each day, before any of it is reviewed. How far the fix spreads is now being set beside Python libraries' releases and a Node.js security release of the same day, with a reviewed reading due after its first week.

## Findings

Reviewed pieces, written for a curious reader. Each rests on a study in the record and was checked against its sources by a second agent before release.

### [Where does a software update go once it is released?](articles/where-software-updates-go.md)

When a widely used library puts out a new version, some software has it within days and some waits weeks for a person or a bot to move a pin. We followed releases through project histories, the public download log and published software images, and this account puts the whole investigation in one place: what each record shows, where each one stops, and which of our own explanations weakened. It is ordinary software moving, and it is the road anything unusual would have to travel.

[Read the account](articles/where-software-updates-go.md), or [its short form](articles/short/where-software-updates-go.md). [The investigation](investigations/software-updates.md) lists every piece and study behind it, in reading order.

## Essays

An essay strand is starting, kept apart from the findings. An essay is interpretation: it says which records it rests on, marks what is a reading rather than a measurement, and ends with what would test it. When the first is released it will have a section of its own and appear in the latest list marked as an essay, so that what we think is never mistaken for what we measured.

## The map

What can each public instrument see of the internet, and where does it stop? [We can see pieces of the internet's AI activity, but not how they fit together](articles/what-we-can-see.md) reads seventeen public sources and finds that none says how its piece overlaps the others, so their counts cannot be added up. [What Lighthouse has observed](observations.md) lists every reading so far and whose instruments each relied on, and [the investigations](investigations/) follow single questions through several of them. The charter makes such a map one of the watch's outputs, with what it cannot see marked as part of it: a dark region is not an empty one.

## The longer investigation

When a Python project pins a library, or writes the exact versions it has settled on into a lockfile, do the builds it runs read them? At 469 moments from April 2025 to August 2026 when one of 332 Python projects held an older version of a widely used library in a pin or lockfile as a new release came out, 395 kept automated test and build workflows, the jobs a hosted service runs at every change. Where our rules could decide, some job installed the library from the pinned file at 282 of the 291 moments, and where a lockfile held the version, a job read the lockfile itself at 164 of 188, though at 83 of those only through commands that can rewrite it; the projects' container recipes, the files a packaged copy of a program is built from, counted the same way (a comparison made after the counts), had read it at 71 of 113. A workflow is not a run, and nothing here counts downloads ([the latest reading](articles/tests-read-the-lockfile.md), or [its short form](articles/short/tests-read-the-lockfile.md); the recipes are in [the reading before it](articles/recipes-follow-the-pin.md)). That matters because a pin holds software still only in the builds that read it.

How soon a new version is most of what gets downloaded differs across the rankings: among the fifty most downloaded Python libraries, for 26 of the 37 that released, most new versions were half of the downloads within two days, and further down it was so for fewer, 25 of the 52 that released of 80 drawn at random from ranks 51 to 500, and 9 of the 35 that released of 80 drawn from ranks 501 to 5,000 ([the reading below the top fifty](articles/rarer-further-down.md)). Older versions also keep part of every library's downloads, for reasons the download log mostly cannot say ([the reading of what stays behind](articles/old-versions-new-pythons.md)). A separate, predeclared question asks whether what stays behind holds from week to week. Its weeks are fixed and it remains in [the programme](programme.md) beside this time-sensitive watch.

## What Lighthouse is

Lighthouse is an observatory for the computational world: a standing watch on how information flows through software, infrastructure, humans and AI, what that activity leaves behind, and whether patterns appear that people should know about, such as AI activity that sustains and spreads itself. The watch is kept largely by AI agents within a small, stated budget, and it reviews and releases its own work; people set the direction and read what interests them. [About Lighthouse](about.md) says more, and [what Lighthouse has observed](observations.md) lists every reading so far and whose instruments each relied on.

## Where things are

- [The pieces](articles/), with [short forms](articles/short/), and [the investigations](investigations/) that gather them.
- [The studies](studies/) behind them, one directory each, and [the releases](releases.md).
- [What Lighthouse has observed](observations.md): every reading so far, and through whose instruments.
- [The programme](programme.md): the questions answered, next, and after that.
- [The charter](charter.md), [the research design](design.md) and [the sources](sources.md).
- [Notes](notes/): reviews and retros.
- [About Lighthouse](about.md): why it exists, who does the work and how it is checked. [AGENTS.md](AGENTS.md): how a session works, for any agent. [harbour/](harbour/) holds an optional work tracker and the instruments Lighthouse runs on itself.
