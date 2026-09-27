title: Where does a software update go?
kind: investigation
id: software-updates
attention: active
question: When a software library releases a new version, where does it go, how fast, and what makes the software built on it take it up?
current: articles/where-software-updates-go.md
started: 2026-09-26
studies:
- studies/LH002/LH002.md
- studies/LH005/LH005.md
- studies/LH006/LH006.md
- studies/LH007/LH007.md
- studies/LH008/LH008.md
- studies/LH009/LH009.md
- studies/LH010/LH010.md
pieces:
- articles/where-software-updates-go.md
- articles/where-a-software-update-went.md
- articles/what-a-download-shows.md
- articles/what-an-image-holds.md
- articles/what-moves-a-pin.md
- articles/pins-move-over-weeks.md
- articles/fixes-that-said-so.md
- articles/the-lead-was-a-few-libraries.md

## How the inquiry developed

We started by following one release of mcp, a Python library AI agents use, into nine projects built on it ([where a software update went](../articles/where-a-software-update-went.md)); the histories showed where it went but not why, or whether anyone ran it. The download log **extended** the trail past the projects and showed the new version at half of all downloads within two days, stopping at the download ([what a download shows](../articles/what-a-download-shows.md)). Published images **extended** it again, to the installation, and showed a project's software holding a version its own lockfile did not name ([what an image holds](../articles/what-an-image-holds.md)). A sample of images around a later release confirmed two paces, ranges within days and pins waiting, and **branched** into what moves a pin, where a security advisory seemed to ([what moves a pin](../articles/what-moves-a-pin.md)). Four libraries **revised** that: pins moved over weeks, after both release and advisory, with no burst ([pins move over weeks](../articles/pins-move-over-weeks.md)). Fixes' own notes then **narrowed** the question to whether a fix that says so draws pins sooner, which fourteen libraries suggested ([fixes that said so](../articles/fixes-that-said-so.md)). Thirty libraries **revised** that to unsettled: pooled it leans that way, library by library we could not tell ([the latest reading](../articles/the-lead-was-a-few-libraries.md)). [Where does a software update go once it is released?](../articles/where-software-updates-go.md) draws the whole together, and is the place to start.

The reading order above puts that account first and then the pieces in the order they were written, so that a reader who starts with the whole is led on through the steps that built it, and the last piece is the latest reading.

## Where it changed direction

- From projects to downloads: the histories stopped at what projects asked for, so we looked for a record on the far side of the release.
- From downloads to images: the log could not say what was installed, so we read the installations some projects publish.
- From installation to what moves a pin: images showed that pinned software waits, so the question became what ends the wait.
- From advisories to the fix's own notes: fixes came out before their advisories, so a move "before the advisory" was not a move before anyone knew.
- From fourteen libraries to thirty: two libraries carried the lead, so each library had to count once.
- From the notes back to downloads: five months of advisories held too few libraries, so the next reading returns to how fast releases reach downloads.

## Where the evidence stands

Attention says where we are looking; this says how firm the findings are. That a new release can reach half of a library's downloads within two days rests on one release of one library. That software built from open ranges took a release within days while pinned software waited showed in the published images of one library's dependents, and that pins move to security fixes over weeks held across four libraries. Whether a fix whose own notes say so draws pins sooner is not settled. No reading checked whether any project was exposed, and none can see software run.

## Beside it

- [The xz backdoor sat in public for nearly five weeks until a slow login gave it away](../articles/the-xz-backdoor.md): a historical case of a compromise travelling the same kind of distribution roads, unseen by the public sources we surveyed.
- [We can see pieces of the internet's AI activity, but not how they fit together](../articles/what-we-can-see.md): the survey of public sources whose edges this investigation keeps meeting.

## What is next

The question of fixes that say so rests unsettled: five months of advisories against the 500 most downloaded Python projects did not hold enough libraries to press it further, and a longer window may one day. The next reading goes back to the fast half of the road: whether a new release of a widely used library reaches half of its downloads within two days as a rule, as one did, and how much of that is automated builds rather than people. Its [brief](../studies/LH011/brief.md) was written before any download was read and no reading has begun; [the programme](../programme.md) says why it comes next and names the questions after it.
