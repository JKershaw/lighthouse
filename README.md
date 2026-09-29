# Lighthouse

## [Where does a software update go once it is released?](articles/where-software-updates-go.md)

When a widely used library puts out a new version, some software has it within days and some waits weeks for a person or a bot to move a pin. We followed releases through project histories, the public download log and published software images, and this account puts the whole investigation in one place: what each record shows, where each one stops, and which of our own explanations weakened. It is ordinary software moving, and it is the road anything unusual would have to travel.

[Read the account](articles/where-software-updates-go.md), or [its short form](articles/short/where-software-updates-go.md). [The investigation](investigations/software-updates.md) lists every piece and study behind it, in reading order.

---

## Current focus

When a Python project pins a library, or writes the exact versions it has settled on into a lockfile, does the recipe that builds its software read them? At 469 moments from April 2025 to August 2026 when one of 332 Python projects held an older version of a widely used library in a pin or lockfile as a new release came out, about half kept a container recipe, the file a packaged, ready-to-run copy of a program is built from. Where our rules could decide, 128 of 166 recipes installed from the pinned file; a quarter could not be decided, and a recipe is not an image anyone built or ran ([the latest reading](articles/recipes-follow-the-pin.md), or [its short form](articles/short/recipes-follow-the-pin.md)). That matters because a pin holds software still only in the builds that read it.

How soon a new version is most of what gets downloaded differs across the rankings: among the fifty most downloaded Python libraries, for 26 of the 37 that released, most new versions were half of the downloads within two days, and further down it was so for fewer, 25 of the 52 that released of 80 drawn at random from ranks 51 to 500, and 9 of the 35 that released of 80 drawn from ranks 501 to 5,000 ([the reading below the top fifty](articles/rarer-further-down.md)). Older versions also keep part of every library's downloads, for reasons the download log mostly cannot say ([the reading of what stays behind](articles/old-versions-new-pythons.md)). The next question is whether what stays behind holds from week to week. Its weeks are fixed, and it waits until the log's public copy holds them, from about 13 October 2026 ([the programme](programme.md)).

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
