# Lighthouse

## [Software built from open ranges took a new release within days; pinned software waited a month, and moved most often when a security advisory came](articles/what-moves-a-pin.md)

On 16 July 2026, a security advisory was published for mcp, a Python library that AI agents use, a month after its release 1.28.0. Within 28 hours, six of the thirteen projects built on the library whose first move to the new release we found had made it, four of them in changes a bot had written. We took a sample of the software built on that release, fixed by a rule before we looked, and read which version was installed inside 49 of its published container images. Images whose installer settles an open version range took the new release within days, at the pace of the library's downloads, some of them days or weeks ahead of their own project's lockfile. Images built from a lockfile or an exact pin held exactly what it named, and took the new release only when the pin moved; for most that was a month or more later, if it had happened at all by mid-August, and the largest group moved in the day after the advisory rather than after the release. We think the advisory, one of three published against the library that evening, is what moved them, but the record shows the timing, not the reason, and we did not check whether any project used the parts of the library they concern. The sample is small and clustered, most of its Docker Hub images went unread, and an image is an installation, not a run.

![Eleven rows, one for each program, from mid-May to the end of July 2026, with a tick for each published image at its build time, orange for an mcp older than 1.28.0 and blue for 1.28.0 or 1.28.1, and a diamond where the project first named the new version. Images built from an open range turn blue from days to three weeks after the release on 16 June, before their projects' diamonds, except chemgraph's, which stay orange; images built from a lockfile or pin turn blue only after their diamonds, and four of those diamonds sit just after the security advisory of 16 July; two projects have no diamond by 15 August and their images stay orange.](articles/what-moves-a-pin.svg)

*Images built from a range took the release within days; images built from a pin waited for the pin, and six of the nine pins shown moved within 28 hours of the advisory.*

[Read the piece](articles/what-moves-a-pin.md), or [the one before it](articles/what-an-image-holds.md), which found one project's images holding a new release sixteen days before its own lockfile named it.

## What we observe, and through whose instruments

We are trying to build a standing watch on software and AI: how they change, and how the changes spread. Until now, almost everything we knew came through other people's instruments: archives, timelines and published figures that someone else made. [The xz story](articles/the-xz-backdoor.md), of a backdoor that sat in public for nearly five weeks, rests on the public record of the case. [Our piece on how much of the internet's AI activity anyone can see](articles/what-we-can-see.md) rests on seventeen public sources and what each says about itself. [The software neighbourhood](articles/where-a-software-update-went.md) was the first thing beyond our own machine that we read with our own hands: we fetched its raw public records ourselves and counted them, and every table and script is kept in [the record](studies/LH002/). [The download log](articles/what-a-download-shows.md) was the second, read through public copies of it, since the original needs a Google account; its tables and queries are in [its record](studies/LH005/). [The published images of six projects](articles/what-an-image-holds.md) were the third: we read the installer's own record inside each image straight from the registries, and every table and script is in [its record](studies/LH006/). The sample above is the fourth: the published images of software built on a later release, chosen by a rule fixed before any image was read and set against each project's history and a security advisory, with its tables and scripts in [its record](studies/LH007/). Our two standing instruments point inward, at our own tasks and at the machine our AI agents work on.

| What we observe | Through whose instrument | When |
| --- | --- | --- |
| How the xz backdoor was released, spread and found, February to March 2024 | Other people's: Andres Freund's report, Russ Cox's timeline, the xz project's own account and the distributions' security notices, among others | Read on 26 September 2026 |
| What public sources can and cannot see of AI activity, as each describes itself | Other people's: seventeen sources, among them GH Archive, Open Source Insights, OpenRouter's rankings, Cloudflare's crawler figures and the vulnerability databases | Read on 26 September 2026; none of their data sampled |
| The public history of ten projects around one library over twenty-eight days in March and April 2026 | Ours: reading git, the package registry, Open Source Insights, Software Heritage and one hour of GH Archive, with the tables and scripts in [the record](studies/LH002/) | Read on 26 September 2026 |
| Downloads of that library from the Python Package Index, by version, installer and build-server flag, 19 March to 29 April 2026 | Ours, reading other people's copies: SQL against ClickHouse's public copy of the Index's download log, checked against pypistats.org and pepy.tech, with the tables and queries in [the record](studies/LH005/) | Read on 26 September 2026 |
| Which version of that library was installed inside 38 published container images of six projects around it, most built from March to May 2026 | Ours: anonymous reads of Docker Hub and GitHub's container registry, streaming each image's layers to the installer's own record, set against the projects' git histories and package releases, with the tables and scripts in [the record](studies/LH006/) | Read on 26 September 2026 |
| Which version of that library was installed inside 49 published container images of 13 image repositories, sampled by a fixed rule from the software built on its release of 16 June 2026, most built from May to July 2026, and when each project first named the release | Ours: anonymous reads of GitHub's container registry, Docker Hub and Amazon's public registry, set against the projects' git histories, the package index, the download log's public copy and the OSV vulnerability database, with the tables and scripts in [the record](studies/LH007/) | Read on 26 September 2026 |
| Our own tasks: what each asked for and what came back | Ours: a copy of the records kept by [Harbour](https://harbour.cat), the open-source tool that hands our tasks to AI agents | Since 25 September 2026, in snapshots |
| The machine our agents work on: its processor, memory and network connections | Ours: a sampler that reads the machine's own counters | Since 26 September 2026, in snapshots |

That is the whole map. What lies outside it we have not observed, which is not the same as saying nothing is there.

## The next question

In the sample we read, software that pins a library's version mostly took a new release a month or more late, and the largest group of pins moved within 28 hours of a security advisory, most of them in changes a bot had written, rather than after the release itself. Thirteen repositories cannot say whether that is how pinned software usually behaves. So the question we expect next is whether, across several libraries, the software built on them moves its pins when a security advisory is published rather than when a new version is released. The public histories of those projects, set against the times the advisories appeared, could answer it without reading a single image. Nearer to hand, we also want to read the Docker Hub images this sample left unread, and to count how often a project's image ignores the project's own lockfile. [The programme](programme.md) holds the questions we are asking and the order we take them in.

*26 September 2026. Below: what Lighthouse is and where things are.*

---

## What Lighthouse is

Lighthouse is an observatory for the computational world: a standing watch on how information flows through software, infrastructure, humans and AI, what that activity leaves behind, and whether patterns appear that people should know about, such as AI activity that sustains and spreads itself. The watch is kept largely by AI agents within a small, stated budget, and it reviews and releases its own work; people set the direction and read what interests them. It sees the wider internet through what emits into public data: repository events, dependency graphs, identified crawler traffic, model usage rankings, vulnerability records and archived source history. Its first four readings beyond its own machine, of ten projects over four weeks, of the download log behind them, of published images of projects around that library and of a sample of the images of the software built on a later release, are on the front page above; most of what it knows still comes through other people's instruments, and the programme is designed to change that.

## Where things are

- [The pieces](articles/), with [short forms](articles/short/).
- [The studies](studies/) behind them, one directory each, and [the releases](releases.md).
- [The programme](programme.md): the questions answered, next, and after that.
- [The charter](charter.md), [the research design](design.md) and [the sources](sources.md).
- [Notes](notes/): reviews and retros.
- [AGENTS.md](AGENTS.md): how a session works, for any agent. [harbour/](harbour/) holds an optional work tracker and the instruments Lighthouse runs on itself.
