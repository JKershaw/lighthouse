# Lighthouse

Lighthouse watches the internet for what AI systems do there and what their activity leaves behind, and publishes what it finds. The question the watch is kept for is whether such activity could sustain and spread itself in ways that degrade the infrastructure everyone shares. Nobody knows yet, and Lighthouse means to be able to tell. The charter says why. This file says how a session works, for any agent in any harness.

## What is known

- The xz backdoor sat in public release files for about five weeks before a slow login gave it away. Both signals anyone noticed came from running code: a memory checker's errors in Red Hat's distributions from 4 March, then one engineer's timing. None of the seventeen sources surveyed, and no instrument Lighthouse has proposed, watches the distribution pipelines the compromise travelled through. The piece is articles/the-xz-backdoor.md; the record is studies/LH004/.
- The public observatories of AI activity are partial views. Seventeen sources each cover one population, such as one forge, one broker, one vendor's tier or one network; their counts cannot be added, because no source says how much they overlap and Lighthouse has not measured it. The piece is articles/what-we-can-see.md; the record is studies/LH003/.
- In one small neighbourhood of Python projects, the public record followed a new release into four of nine dependents within four weeks, and one step further where a project pinned it exactly, but could not say why any of them moved or whether anyone ran it. This is the first thing Lighthouse read with its own hands. The piece is articles/where-a-software-update-went.md; the record is studies/LH002/.
- The two instruments Lighthouse runs otherwise point inward, at its own tasks and its own machine.

## What is next

LH005. Ask whether any public record connects a software release to its installation, starting from the Python Package Index's download records by version and installer, read for the LH002 library across the LH002 window and set beside the dependents' moves the record holds. The design is in programme.md, which also names the questions after it.

## How a session goes

1. Read the front page, the two pieces and programme.md. Nothing else is required reading.
2. Do the next study in the programme, or the piece a finished study earns. Use subagents freely: Opus 5.5 for research and writing, Fable 5.1 for review, Sonnet 5 for collection and tabulation. Give each the task, the repository path and this file. The review is where money buys the most: the errors in the first drafts came from a research pass on Sonnet, and the review that caught them ran on Opus. Every subagent writes about 45,000 tokens of harness context before it starts, a floor of about $0.11 on Sonnet, $0.22 on Opus 5.5 and $0.56 on Fable 5.1, and a Fable review costs about twice an Opus one. About twenty dollars of measured subagent spend a session is the bound, and Claude spend is a measure at list rates rather than a bill.
3. Write what was found: a study as a record, a piece for readers, in the forms below.
4. Have a second agent on the strongest model review the piece against its sources. The reviewer reads the primary sources rather than summaries of them, reproduces the important calculation or says why it could not, and writes what it checked, found and changed as a note in notes/; a second agent's agreement is a review contribution, not independent confirmation. When the review finds nothing that must be fixed, release it: take the Draft label off, complete the colophon, add a line to releases.md, and put it on the front page.
5. Commit once at the end, with a message that says what was learned and what the session spent. Report what was learned about the internet, and the next question. Say nothing about process unless it failed.

Fix small things where you find them, without filing, listing or reporting them. Decide routine questions yourself and note the choice in a sentence where it was made. Nothing waits for a person except the three things below.

## Rules that matter

- Every claim says where it came from and when the source was read. Label a statement as observation, derived measurement, interpretation or scenario wherever a reader could confuse them. Never invent a timing, a count or a source. Say what was not checked.
- Three things wait for a person: a claim that harm is happening now, a claim that a named system is compromised, and anything irreversible outside this repository, such as contacting a third party. Everything else is the session's to decide.
- Do not read or use credentials from the environment unless the task names them. Never write a token, a session id or a key into the repository.
- No piece is released without a review that found nothing that must be fixed. Commit with a message that says what changed and why, and never rewrite history on a shared branch.

## Writing

Records are for checking: studies and notes. Pieces are for reading: articles, essays, short forms and the front page. Both in British English, with no em or en dashes in prose, and no invented figures.

A study lives in studies/LHnnn/ with its brief (the question, its scope, the resource ceiling and the stopping condition), its sources and its write-up. The write-up has a header (the question as its title, version, date, who wrote it and on which model, the commit the figures were taken from, the observation period, the instruments and versions used, what it cites, and any overlap to disclose) and then Answer, Findings, Method, Limits, Next and Corrections, where each entry says what changed, why, whether the conclusions changed, and where the earlier edition is. Cite a source by its S number in sources.md or by URL with the date read, and give the source's publication date and observation window beside it. Leave unfillable fields blank and say what could not be filled.

A piece is written for a curious person who has never heard of Lighthouse. A title that says the finding, a short opening that gives a reason to care, a discreet date and byline, and a small Draft label while it is under review. Open with the thing itself, a person, a moment or a surprise, never with Lighthouse or its method. One idea a reader could say back in a sentence, developed one thought at a time; say it, then qualify it once, where the qualification matters. Plain words; define a term where it is first needed and only if it is needed. No internal references in the prose: no document names, study numbers, tickets or roles; the piece speaks as "we". Honesty lives in the verbs: the record shows, nobody has measured, we think. An illustration drawn, not described, with a one-line caption. A colophon at the end: sources with dates, the method in a sentence, who wrote, edited and reviewed it, version and date, corrections, and one line on what Lighthouse is; it may link to the record beneath. Read it aloud before handing it over, and rewrite anything that trips.

## Where things are

- articles/ the pieces, with short forms in articles/short/.
- studies/ the record behind each piece, one directory per study.
- programme.md the questions: answered, next, and after that.
- design.md the method: the three layers, the surfaces, the four kinds of statement, calibration and risk.
- sources.md the numbered sources.
- charter.md why the watch is kept and what it will not do.
- notes/ reviews, retros and working notes.
- releases.md what has been released and when.
- harbour/ a work tracker Lighthouse can run its programme through and does not by default; its README says when it earns its keep and how to use it.

The six founding documents that the early records cite as LH F01 to F06 were folded into these files on 26 September 2026. Git holds them.
