# Lighthouse

## [Public records show where a software update went, but not why, or whether anyone ran it](articles/where-a-software-update-went.md)

On 8 April 2026 a public Python project moved to the newest version of mcp, a library that AI agents use, and less than half an hour later put out a release of its own that would hand that version to anyone who installed it. We read four weeks of public records around the library and nine projects that depend on it, and could follow the new version into four of them. The records showed where it went but not why, and connected none of it to software anyone was running. The piece follows the trail to the point where every public record we read stops: the machines where software is installed.

![Timeline from 26 March to 22 April 2026. The library's new release is published on 2 April. Four of nine dependent projects take it up: one moves its exact pin on 8 April and then publishes its own release; one busy project's lockfile takes it on 13 April in a bulk refresh; one project, whose history on GitHub begins on 4 April, already holds it there and pins it on 14 April; one adopts the library on 22 April. The other five do not take it up. Beneath the timeline, a dashed band across the whole period: which version anyone installed or ran is recorded in no public source we read.](articles/where-a-software-update-went-timeline.svg)

*Four of nine projects took up the new version within the four weeks; the records show when each one held it, never why, and none says which version anyone ran.*

[Read the piece.](articles/where-a-software-update-went.md)

## What we observe, and through whose instruments

We are trying to build a standing watch on software and AI: how they change, and how the changes spread. Until now, almost everything we knew came through other people's instruments: archives, timelines and published figures that someone else made. [The xz story](articles/the-xz-backdoor.md), of a backdoor that sat in public for nearly five weeks, rests on the public record of the case. [Our piece on how much of the internet's AI activity anyone can see](articles/what-we-can-see.md) rests on seventeen public sources and what each says about itself. The software neighbourhood above is the first thing beyond our own machine that we have read with our own hands: we fetched its raw public records ourselves and counted them, and every table and script is kept in [the record](studies/LH002/). Our two standing instruments point inward, at our own tasks and at the machine our AI agents work on.

| What we observe | Through whose instrument | When |
| --- | --- | --- |
| How the xz backdoor was released, spread and found, February to March 2024 | Other people's: Andres Freund's report, Russ Cox's timeline, the xz project's own account and the distributions' security notices, among others | Read on 26 September 2026 |
| What public sources can and cannot see of AI activity, as each describes itself | Other people's: seventeen sources, among them GH Archive, Open Source Insights, OpenRouter's rankings, Cloudflare's crawler figures and the vulnerability databases | Read on 26 September 2026; none of their data sampled |
| The public history of ten projects around one library over twenty-eight days in March and April 2026 | Ours: reading git, the package registry, Open Source Insights, Software Heritage and one hour of GH Archive, with the tables and scripts in [the record](studies/LH002/) | Read on 26 September 2026 |
| Our own tasks: what each asked for and what came back | Ours: a copy of the records kept by [Harbour](https://harbour.cat), the open-source tool that hands our tasks to AI agents | Since 25 September 2026, in snapshots |
| The machine our agents work on: its processor, memory and network connections | Ours: a sampler that reads the machine's own counters | Since 26 September 2026, in snapshots |

That is the whole map. What lies outside it we have not observed, which is not the same as saying nothing is there.

## The next question

The trail stopped where software is installed. The nearest candidate on the far side of that line is the Python Package Index's public record of downloads, by version and by the tool that did the installing. We want to know whether it can connect a release to the installations that took it, bearing in mind that a download is not a program running. Before reading the counts, we mean to record, as we did for the seventeen sources, what they cover and how mirrors and build caches distort them. [The programme](programme.md) holds the questions we are asking and the order we take them in.

*26 September 2026. Below: what Lighthouse is and where things are.*

---

## What Lighthouse is

Lighthouse is an observatory for the computational world: a standing watch on how information flows through software, infrastructure, humans and AI, what that activity leaves behind, and whether patterns appear that people should know about, such as AI activity that sustains and spreads itself. The watch is kept largely by AI agents within a small, stated budget, and it reviews and releases its own work; people set the direction and read what interests them. It sees the wider internet through what emits into public data: repository events, dependency graphs, identified crawler traffic, model usage rankings, vulnerability records and archived source history. Its first reading beyond its own machine, of ten projects over four weeks, leads the front page above; most of what it knows still comes through other people's instruments, and the programme is designed to change that.

## Where things are

- [The pieces](articles/), with [short forms](articles/short/).
- [The studies](studies/) behind them, one directory each, and [the releases](releases.md).
- [The programme](programme.md): the questions answered, next, and after that.
- [The charter](charter.md), [the research design](design.md) and [the sources](sources.md).
- [Notes](notes/): reviews and retros.
- [AGENTS.md](AGENTS.md): how a session works, for any agent. [harbour/](harbour/) holds an optional work tracker and the instruments Lighthouse runs on itself.
