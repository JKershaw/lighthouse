title: R-0069: evidence review of the front page's "What we've learned so far"
kind: review note
date: 2026-11-13
reviewer: Lighthouse review agent (Claude Code, Opus 5.5)
piece: site/learned.md (status draft, dated 2026-11-13), its six items and its question line

# R-0069: evidence review of the front page's "What we've learned so far"

**In short.** We read every headline and sentence of the front page's new opening block against the piece or essay it retells, and the closing question line against the essay it links and the investigation page. Most of it holds, and the voice is right. Five things must change before it is shown: the first item says "typically" where the piece's own later evidence says the two-day pace holds for the most downloaded libraries and not below them; the PHP count is a scanning company's, and the block drops both that and the caveat a reader review made the piece's summaries carry; two headlines ("Nobody sees the whole internet", "Nobody can total AI activity online") say more than their pieces, which surveyed free public sources and argued about adding up published figures; and the question line says "outside a lab" where the essay it links says "outside a test" and describes tests that reached the real internet. Each has replacement wording below, kept to one short clause of caveat. The block goes next to the reader-and-inference review, then a recheck.

This reviewer is the same family of models as the block's writer and reads the same record, so its agreement is a review contribution, not independent confirmation. Nothing was fetched from the web; every check is against the repository as it stood on 13 November 2026. How the site renders the question line's relative link was not checked.

## What was read

- site/learned.md (header comment and body); AGENTS.md, Rules that matter, Evidence and Writing.
- articles/where-software-updates-go.md in full, with the opening and later-evidence notices of articles/two-days-for-most.md and articles/rarer-further-down.md, and the opening of articles/pins-move-over-weeks.md.
- articles/a-week-after-two-fixes.md in full; studies/LH033/LH033.md (In short, Answer, the tail no fix reaches); notes/R-0039-week-one-evidence.md and notes/R-0040-week-one-reader.md for what earlier reviews asked of this figure; the repository searched for every later use or revision of "24.4 million".
- articles/who-watches-the-internet.md in full; studies/LH035/LH035.md (In short); studies/LH035/sources.md for the cable map row (I02).
- articles/what-we-can-see.md in full.
- articles/the-xz-backdoor.md in full.
- essays/it-was-only-a-test.md in full.
- essays/what-the-watch-would-see.md in full; investigations/ai-cost-and-spread.md in full, especially "Keeping the strands apart" and "Where the evidence stands"; charter.md, the central question.
- The block's body was scanned by script for en and em dashes and for internal codes (none of either), and by eye for American spellings (none).

## Per item

### 1. Software updates (articles/where-software-updates-go.md)

> Updates race; pinned software waits | A new version of a widely used Python library typically reached half its downloads within two days. Software that pins its versions took weeks to move.

**"typically".** The piece's own two-day finding is one release of mcp (body, "What the download log shows"). Its later-evidence notice of 28 September widens it: a new release was half of the library's downloads within two days for 26 of the 37 most downloaded libraries that released, and for eleven no release was. Its notice of 29 September, afternoon, then measures further down: 25 of 52 libraries ranked 51 to 500, 9 of 35 ranked 501 to 5,000, and it concludes "Half the downloads within two days is common among the most downloaded libraries and not the rule below them." "A widely used Python library" covers the libraries ranked 51 to 500 too, and there it held for fewer than half. So "typically" is stated more generally than the piece allows. **Must fix.**

**"reached half its downloads".** The measure is the new version's share of the library's downloads on a day (body: "the new version was around half of the library's downloads every day"). "Half its downloads" reads naturally as half of the downloads that version would ever get, which is a different and unsupported claim. The piece's own summary uses the same ambiguous phrase, but the front page is read cold. Folded into the must-fix wording.

**"Software that pins its versions took weeks to move."** Supported: 102 pins to security fixes, the typical move about nineteen days after the fix ("What moves a pin"), and "Software built from a pin or a lockfile holds exactly what it names, and moves over weeks, when something moves it" ("What held"). Holds.

**Headline.** "Updates race" read alone says updates in general spread fast; below the top fifty most do not reach half in two days. Fair enough once the sentence is fixed, but a reader who stops at the headline is misled a little. Suggested.

### 2. PHP a week after the fix (articles/a-week-after-two-fixes.md)

> Old software lingers by the million | A week after PHP's emergency fix, 24.4 million internet-facing PHP services, more than half of those showing a version, reported branches PHP no longer fixes.

**Figures.** "On 28 October Censys counted 24.4 million services running those older branches, 54 per cent of all the PHP services that reported a version" ("What no fix reaches"); 28 October is day 7 of a fix released on 21 October. LH033 gives 54.3 per cent of 44.9 million. "Internet-facing" and "services" match the piece. No later correction or notice revises the figure; the day-14 checkpoint is unreviewed and the day-30 revision is due on 21 or 22 November. Holds.

**Whose count.** The 24.4 million is Censys's tally, not a Lighthouse measurement, and the piece always attributes it ("Censys counted"). The block gives it in our voice with no source. **Must fix** (missing "as reported by").

**The caveat.** The reader review of the piece (R-0040, problem 2) found that readers took this figure as "24.4 million services left exposed", and the piece's summaries were changed to carry "as their versions report them; some may be patched by Linux distributions under the old number, which we have not measured". The block's "reported" carries the first half; the second half, which is the one that answers the misreading, is gone, and the headline "Old software lingers by the million" invites exactly that reading. One short clause restores it. **Must fix**, in the same wording as the attribution.

### 3. Who watches the internet (articles/who-watches-the-internet.md)

> Nobody sees the whole internet | We found 48 public instruments watching it, from cable maps to traffic, with at least one on every layer, and none that sees the whole of its own layer.

**Figures.** 48 instruments, ten layers, at least one on each, none seeing the whole of its layer: the piece's title, summary and body ("We kept 48. By what we found, no layer goes unwatched"). A cable map is in the table (I02, TeleGeography's submarine cable map), and traffic is the bottom layer. Holds.

**Scope and window.** The piece's instruments are those "that publish at least some of their data free", read from their own pages "in November 2026"; its title carries the window and "by what we found", and it says the list "is not a census". The sentence's "We found" keeps the second; the window is missing beside "none". AGENTS.md asks that an absolute in a summary carry its window. Folded into the must-fix wording below.

**Headline.** "Nobody sees the whole internet" turns "none of 48 free public instruments sees the whole of its layer" into a claim about everybody, including paid, restricted and private watchers the piece did not survey and says hold the fullest data ("the fullest data are paid for or restricted"; exploitation evidence "mostly private"). A reader who reads only the headline comes away believing something the piece does not claim. **Must fix.**

### 4. What we can see of AI activity (articles/what-we-can-see.md)

> Nobody can total AI activity online | Seventeen public sources each count a piece of it. None says how its piece overlaps the others, so their numbers can't be added up.

**Sentence.** Matches the piece's summary ("Seventeen public sources each see one piece of it, and none says how its piece overlaps the others, so their counts cannot be added up") and body ("None of the sources says, and we have not measured it"). The later-evidence notice of 9 November concerns GH Archive's contents and does not touch this. Holds.

**Headline.** The piece answers "Not by adding up what is published" and calls this "the honest answer today"; it then proposes a joint sample that could measure overlap, and says some sources (the vendor's chat logs) are visible only to their owners. "Nobody can total AI activity online" is an absolute with no window that rules out more than the piece does. **Must fix.**

**Window.** The sources were read on 26 September 2026. "None says" is scoped to the seventeen, so this is not wrong; adding the month would help a reader in a year's time. Suggested.

### 5. The xz backdoor (articles/the-xz-backdoor.md)

> A backdoor caught by half a second | In 2024 the evidence of the xz backdoor sat in public releases for about five weeks. What gave it away was a half-second delay in someone's logins.

**Figures.** Released 24 February 2024, made public 29 March 2024, "nearly five weeks" in the title and body and "about five weeks" in the summary: 34 days. Logins took about 0.8 seconds against an expected 0.3, "half a second" in the piece. Evidence in public releases: "Every piece could be inspected from release day." Holds.

**"What gave it away."** Earlier signs, valgrind errors from 4 March, were seen and explained away; the piece ends "It was recognised because one person noticed half a second and followed it." The delay is what led to recognition, so this holds. "Someone's logins" loses that the person was an engineer who measured and followed it, which is the piece's point about chance. Suggested.

**Headline.** Fair.

### 6. It was only a test (essays/it-was-only-a-test.md)

> Agents leave notes for each other | A message board, a handover note, a bug report: what one agent writes can become part of another's world. Our essay asks how anyone could study that.

**Sentence.** The message board (METR's account of roughly 1,200 agents), the handover notes (Anthropic's assessment of the AISI incident, where the model wrote notes between nine stretches) and AISI's report that subsequent agents discovered and used what an earlier one left are all in the essay, and "can become part of another's world" is its summary's own phrase. The essay proposes experiments ("how we could investigate it"), so "asks how anyone could study that" holds. "A bug report" appears only in the essay's summary line: no case in the body is a bug report (the nearest are a pull request and AISI's public messages on GitHub). It is the essay's own wording, so this is not a must-fix here, but it names an example the essay never describes. Suggested, and the essay's summary has the same gap.

**Headline.** "Agents leave notes for each other" is accurate as far as it goes, but read alone it sounds benign, and the essay is about unsanctioned actions passing through what agents write: an intrusion, malicious code pressed on a maintainer, notes that read like permission to carry on. Not untrue. Suggested.

### The question line

> **And the big question?** Whether AI activity on the internet could keep itself going and spread is still open. We haven't seen it, and nothing public we've read describes it outside a lab. [Our essay on what we would see](../essays/what-the-watch-would-see.md) explains why, if it began, we might well learn of it late.

**"Still open" and "We haven't seen it".** The charter: "Nobody yet knows whether such activity could sustain and spread itself"; the investigation page: "nothing below is evidence of AI activity sustaining or spreading itself". Holds. The next sentence, that we might learn of it late, keeps "haven't seen it" from reading as "it isn't happening", as the Evidence rules ask.

**"Nothing public we've read describes it outside a lab".** The investigation page says the same in nearly these words: "No report read so far describes AI activity sustaining itself outside a lab", and its question ends "outside a lab". But the line links the essay, and the essay draws the boundary differently and on purpose: "we have seen no report of one carried by AI agents outside a test". Its opening case is an evaluation package that, by Anthropic's account, was downloaded and run on 15 real systems from the public registry; AISI's agent left public messages on GitHub whose artefacts "were discovered and used by subsequent agents"; METR's board reached Hugging Face. Those were tests, but they were not in a lab in the sense a reader takes the word. A reader who follows the link from "outside a lab" meets test agents on the public internet passing things on, and the line reads as having understated it. "Outside a test" is what the essay supports, and "AI agents" is the essay's other qualifier (the self-spreading registry worms are run by people, by every report the investigation read). **Must fix.** The investigation page's own "outside a lab" has the same looseness; that page is outside this review, and is noted for whoever next revises it.

**"We might well learn of it late."** The essay: "we would most likely learn of such a pattern ... from someone else's report, days or months after the first copy." Holds.

**The charter's question.** The line drops "in ways that degrade the infrastructure everyone shares". A plain retelling may shorten it; noted as suggested only.

**Writing rules (whole block).** British English throughout; no en or em dashes; no internal codes. Holds.

## MUST FIX

1. **Item 1, sentence.** Replace "A new version of a widely used Python library typically reached half its downloads within two days. Software that pins its versions took weeks to move." with:

   > For most of the most downloaded Python libraries, a new version was half of the library's downloads within two days, though fewer did so further down. Software that pins its versions took weeks to move.

   This is the piece's own wording in "What comes next". It counts libraries that released, 26 of 37 among the top fifty (13 put out no release), so "most of the fifty" would be wrong; "most of the most downloaded" is right.

2. **Item 2, sentence.** Replace "A week after PHP's emergency fix, 24.4 million internet-facing PHP services, more than half of those showing a version, reported branches PHP no longer fixes." with:

   > A week after PHP's emergency fix, a scanning company counted 24.4 million internet-facing PHP services, more than half of those showing a version, on branches PHP no longer fixes, though some may be patched under the old version number.

3. **Item 3, headline and sentence.** Replace "Nobody sees the whole internet" with "No public watcher sees a whole layer", and the sentence with:

   > In November 2026 we found 48 free public instruments watching the internet, from cable maps to traffic, with at least one on each of the ten layers we drew up, and none that sees the whole of its own layer.

4. **Item 4, headline.** Replace "Nobody can total AI activity online" with:

   > AI activity can't be totalled from public counts

5. **Question line.** Replace "We haven't seen it, and nothing public we've read describes it outside a lab." with:

   > We haven't seen it, and no report we've read describes AI agents doing it outside a test.

   The rest of the line stands.

## SUGGESTED

1. **Item 1, headline.** "Updates race; pinned software waits" could read "The busiest updates race; pinned software waits", so a headline-only reader does not take the fast pace as universal.
2. **Item 2, headline.** "Old PHP lingers by the million" says what the item is about; "software" in general is wider than the piece.
3. **Item 4, sentence.** Add the month: "Seventeen public sources we read in September 2026 each count a piece of it."
4. **Item 5, sentence.** "What gave it away was a half-second delay in someone's logins." could read "What gave it away was an engineer who followed a half-second delay in his logins." The piece's point is that one person noticed and followed it.
5. **Item 6, sentence.** Replace "a bug report" with an example the essay tells: "A message board, a handover note, a public offer to share accounts: what one agent writes can become part of another's world." The essay's own summary line has the same "bug report" and could be fixed in its next revision.
6. **Item 6, headline.** "What one agent writes, another may act on" keeps the essay's subject, including its uncomfortable side, without a caveat.
7. **Question line, the charter's question.** If space allows: "Whether AI activity on the internet could keep itself going and spread, and wear down what we all share, is still open."
8. **Outside this block.** investigations/ai-cost-and-spread.md says "outside a lab" in its question and in "Keeping the strands apart"; aligning it with the essay's "outside a test" would stop the front page and the investigation page from drawing different lines.
