title: Tone, story and inference review of the essay draft "The instrument is part of the finding"
date: 27 October 2026
reviewer: a fresh Claude Code review agent on Claude Opus 5.5 (claude-opus-5-5), dispatched by the driving session; not independent of the writer, being the same model family reading the same records
what was read: essays/the-instrument-is-part-of-the-finding.md (status draft) first, as a reader, before any record; then AGENTS.md (Writing, including the paragraphs on essays and pieces), notes/reader-review.md, articles/what-we-can-see.md, articles/php-emergency-first-reading.md, articles/two-days-for-most.md (lines on the build-server flag), articles/tests-read-the-lockfile.md (opening and line 42), charter.md (purpose), programme.md (checkpoint of 27 October, evening); studies/LH033/brief.md, checkpoints/2026-10-25.md to 2026-10-27.md, data/read-2026-10-27T0637Z/tables.json, data/python_side.json and the branch list in data/read-2026-10-27T0637Z/censys.raw.gz; studies/LH034/brief.md, checkpoints/2026-10-27.md, data/tables.json; studies/LH011/LH011.md (CI flag findings), studies/LH018/LH018.md (Debian and Ubuntu packages), studies/LH030/LH030.md (CERT-EU advisory); and PHP's manual page https://www.php.net/manual/en/ini.core.php, re-read 27 October 2026 at about 18:48 UTC, where the essay's quotation on `expose_php` and its default "1" match word for word.
outputs: this note, and a full proposed revision at /tmp/claude-0/-home-user-lighthouse/d3d28a3a-ab47-5358-8710-a3e199843e34/scratchpad/essay-polished.md (not written into essays/; the driving session decides what to take)

## What a reader would believe, written after reading the essay and before the records

A careful reader would say back: "PHP and Node.js fixed flaws on the same day. PHP can only be seen by scanning servers, Node.js only by counting downloads. PHP is a world of old servers set up once and left; Node.js and Python are worlds rebuilt constantly, where fixes arrive automatically. Each instrument misses one kind of system: downloads miss neglected servers, scans miss careful administrators. More than half of PHP's version-reporting servers run versions that will never get a fix, and more than half of all PHP servers hide their version, many presumably by choice." They would notice the essay's warning that the 53 to 69 and 49 to 76 per cent figures are not comparable, but would probably take "older lines lag in both" as a second, independent sign that the two ecosystems behave alike, and would take "neglect" and "care" as things the instruments detect. Several of those beliefs go further than the records (Must fix 1, 3, 4 and 7; Should fix 2).

## Verdict

The figures are, with one unit slip, faithfully transcribed from the working records (calculations at the end). The draft's problems are of inference, not arithmetic: an absolute about the old branches, a slide from Censys's services to servers, a care/neglect symmetry that reads as measured, an automation story that leaves out Lighthouse's own released finding that cuts against it, and a weekend claim and test that cannot be supported by five days of a slow-rescanning count. The story is good and worth keeping; it gets better, not weaker, when the records' own complications are let in, especially the Packagist figure LH033 already holds, which shows the essay's thesis inside one ecosystem.

## Must fix

**M1. An absolute the record does not allow.** "Those servers did not miss this fix. There was never one for them."
What is wrong: Censys's class `affected_nofix` means branches PHP itself did not fix (LH033 brief, "branches PHP did not fix at all"). Censys's own notes, quoted in the brief, say counts of affected are an upper bound because distributions backport fixes without changing the version string, and nothing confines that to the fixed branches: distributions that keep an old branch for a long-term release can patch it under the old number. Whether any did for these CVEs is not in the records, so "never" is unsupported.
Proposed: "PHP released no fix for them. Some Linux distributions keep old branches patched for their long-term releases, usually under the old version number, so some of these may be protected; we have not measured how many."

**M2. Censys counts services, and the essay keeps calling them servers.** "counts the servers that answer with a PHP version"; "Censys's count is a census of residents: servers that stand on the internet and say what they are"; "Those servers did not miss this fix"; "Censys sees the forgotten PHP servers".
What is wrong: LH033's brief says Censys counts services (an address or hostname with a port), not machines or organisations, and forbids turning a Censys count into machines, sites or organisations. The essay gets it right where it gives figures ("23.8 million of the services") and slips elsewhere; a reader will take 23.8 million as machines.
Proposed: define once, early: "counts the services that answer with a PHP version (a service is an address and a port, not a machine or a website)", and use "services" wherever a count is meant. "Server" can stay in the illustrative sentences about a single machine.

**M3. "Care" and "neglect" read as measured, and the silent half reads as careful.** "The careful ones are harder to see. An administrator who turns the version header off drops out of the count; more than half the PHP services Censys counted reported no version at all, a share that jumped from under a third when Censys's detection changed on 23 October." And: "The download log cannot see neglect. The scanner cannot see care."
What is wrong: placed straight after "an administrator who turns the version header off", the "more than half" invites the reader to count the silent half as careful administrators. The records say the opposite of that reading: the no-version share went from 32.1 per cent on 22 October to 56.0 per cent on 23 October while Censys's total rose from 61.4 to 95.8 million (a factor of 1.56), which LH033's checkpoint calls a change in Censys's detection, not in the internet. Separately, "cannot see neglect" overstates: the nodejs.org log cannot see anything that stops fetching from nodejs.org, which includes machines updated through distributions, images or mirrors (LH034 brief), not only neglected ones. The symmetry is a good line, and programme.md already uses it, but it must be marked as a description of blind spots, not a measure of behaviour.
Proposed: keep the two concrete kinds of care (hidden header, distribution backport), then: "Nor can silence be read as care: the share of PHP services reporting no version rose from under a third to more than half on 23 October, when Censys's count of PHP services grew by more than half in a day, a change in the instrument, not the internet." And, at the close of the section: "These are blind spots by construction, not measurements of neglect or care, and they sit on opposite sides." Change "The download log cannot see neglect" to "A download log leans, by construction, towards whatever keeps coming back for more", and the test heading to "The download log cannot see what stops fetching".

**M4. The automation story leaves out Lighthouse's own released finding, and the proposed test is partly done.** "In the rebuilt world, a great deal of attention is automatic. A pipeline that installs the newest version picks up the fix without anyone deciding anything." And the test: "If rebuilt systems take fixes mostly through automation, the share of downloads from automated clients should rise faster after a release than the share from people. The Python index records which installer made each download; a study could read that for one release."
What is wrong: articles/two-days-for-most.md (from LH011) found that in the typical library 32 per cent of a new release's downloads in its first three days carried the build-server flag, against 41 per cent of the old release's, with the new release the less flagged in 96 of 104 releases; and articles/tests-read-the-lockfile.md found that projects' automated tests almost always install what the pin or lockfile names. So automation in the rebuilt world also re-fetches old versions, and the essay's prediction (automated share rises faster after a release) has, in the nearest measure Lighthouse has, gone the other way. Also, the field that matters is the CI flag that pip and uv send, not "which installer"; the flag is a floor on builds (LH011).
Proposed: "In the rebuilt world much attention is automatic, and it cuts both ways. A pipeline that asks for the newest version picks up a fix without anyone deciding anything. A pipeline rebuilt from a lockfile, a file listing the exact versions a project has settled on, fetches the old version again, just as automatically, until someone moves the number." Then the Python figures and: "And in the typical library, downloads flagged as coming from build servers were 32 per cent of a new release's first three days, against 41 per cent of the old release's on the same days." Test: "**Automatic attention cuts both ways.** If lockfiles hold automated builds back, a fix's share of build-server downloads should rise only as lockfiles move. A study could follow the flag installers send, day by day, through one fix's first month." Cite the piece in the notes.

**M5. The weekend contrast claims what five days of Censys cannot show, and the test built on it cannot discriminate.** "A census of standing servers has no such rhythm, as far as we can see, because a server that stands does not take weekends off." And the test: "If the distinction is real, the download curves should keep moving with the working week through the month, and the PHP service counts should not."
What is wrong: the Censys series held is days 0 to 5, one weekend, on a curve whose daily gains were shrinking (2.8 to 4.7 points on day 3, 1.2 to 2.0 on day 4, 1.0 to 1.5 on day 5, from the checkpoints), and Censys says a change can lag by hours, up to about a week for some websites. No weekly rhythm could be seen or ruled out. The reasoning also mixes two things: a standing server does not take weekends off, but the people who patch it do, so if the standing world waits on human acts its patching, if anything, should keep office hours; the counted stock simply cannot show it through slow rescans. And the test's first half is near certain whatever the reading (every weekend held since 26 September halves nodejs.org's volume, ratios 0.52 to 0.56), so it cannot fail in an informative way.
Proposed for the texture: "Censys's count, of services as last scanned with rescans that can lag by days, is too coarse to show whether patching keeps office hours." Proposed test, one that could fail and uses figures both studies will hold: "**Standing and rebuilt.** Changes that wait for someone to act accumulate slowly, as Python's pins did. If the distinction holds, PHP's patched shares should still be climbing in the fourth week, while most of the month's movement in Node.js's download shares comes in the first. It could fail: after Node.js's July security release, one line moved more after its first week than in it." (LH034 checkpoint, measure 4: line 24 rose 25 points from day 1 to day 7 and 32 from day 7 to day 30; July's day 7 is itself noisy, line 24 having been at 57.2 per cent on day 5, so the reads should compare weekly averages, not single days, and the essay's wording should not lean on one day.) Say that this test was chosen after day 5.

**M6. House rules for essays and pieces.** (a) "Our studies hold both series to day 30 (LH033 and LH034)": study numbers in prose, where AGENTS.md says a piece carries no internal references, and the essay paragraph asks the tests to name a study where one exists; both are met by a link, not a bare number. "Hold" is also wrong in tense: the studies will read to day 30. (b) The notes cite "studies/LH033", "studies/LH034", "studies/LH018" and LH008/LH011 as plain text; the essay rule is to cite by link every record or source a figure or claim rests on. (c) The opening's "followed by government warnings and wide coverage" and "a routine security release of the kind it makes every few months" rest on no cited record. The PHP emergency piece and LH030/LH031 support advisories from CERT-EU and CISA and attention in three technology outlets ("wide" is more than that); LH034's brief and checkpoint support a regular security release, the previous one in July, and note that October's came "with more press" than July's, which sits awkwardly with "routine".
Proposed: "Our [PHP](../studies/LH033/brief.md) and [Node.js](../studies/LH034/brief.md) studies both read to day 30." Links in the notes for each record. Opening: "PHP's was an emergency, followed by advisories from government agencies and coverage in the technology press; Node.js's was a regular security release, its first since July", with the PHP emergency piece and LH034's brief cited in the notes.

**M7. "Older lines lag in both" invites the agreement reading the essay warns against, and misstates the PHP case.** "In the first week, the oldest fixed line lagged the newer ones both in Node.js's downloads (line 22) and in PHP's service counts (8.2 and 8.3)."
What is wrong: "the oldest fixed line" is singular but names two PHP branches. More importantly, 8.3 is the branch Ubuntu 24.04 ships, and its fixed build reports 8.3.6 (LH018), so part of 8.3's lag is the instrument's floor, a known bias in one direction that the essay states elsewhere but not here. (Debian bookworm's fixed 8.2 build reports 8.2.35, LH018, so the bias is not shown for 8.2.) A reader seeing "lag in both" will take it as a shared behaviour.
Proposed: "In the first week the oldest fixed Node.js line (22) and the two older PHP branches (8.2 and 8.3) lagged. Even if that holds at day 30, the two measure different things, and in PHP part of the lag may be the instrument's: 8.3 is the branch Ubuntu 24.04 ships, whose fixed build keeps its old number."

**M8. A unit slip.** "Pinned projects, where a person or a bot has to move a number in a file, moved over weeks: of 102 we followed, 18 had moved within a week and 50 within a month."
What is wrong: the 102 are pinned repository-and-fix pairs (python_side.json, `lh008_fix_pairs_moved_within`, "pairs": 102), not projects; one repository can pin more than one of the four libraries.
Proposed: "Of 102 pins on those fixes in public projects, 18 had moved within a week and 50 within a month."

## Should fix

**S1. The title.** "The instrument is part of the finding."
What is wrong: it is abstract, and it calls the subject a finding in a piece whose second paragraph says "This is an essay, not a finding". AGENTS.md asks a title to state the finding or the tension; for an essay, the argument a reader could say back.
Proposed: "How a fix can be seen says how software lives" (used in the revision). Alternatives: "What we could count says what we were counting"; or keep the current title, which is memorable, if the keeper prefers it. The file's slug is the driving session's call.

**S2. Ecosystem or layer.** "So the first thing the comparison taught us came before any number. Each ecosystem offered us the instrument that matched how it lives." And "A typical PHP site was set up once, often years ago"; "Much of the Node.js and Python world is not like that."
What is wrong: a reader comes away with "PHP is standing, Node.js is rebuilt". The records show PHP's rebuilt side (Packagist logged 5,809.9 million Composer installs in September 2026, LH033 checkpoint of 25 October) and the essay's own triangulation section talks of layers, not ecosystems. "Typical" and "much" are unmeasured.
Proposed: "Each instrument sees the side its software turns towards the world." Replace "A typical PHP site" with "Picture a PHP website set up years ago". Add: "Both worlds exist in both languages: Composer, PHP's package manager, logged 5.8 billion package installs on Packagist in September, and Node.js has servers that stand for years. But each instrument sees mainly one: the scanner what stands, the download log what is rebuilt."

**S3. The strongest illustration of the thesis is in the records and missing from the essay.** LH033's brief fixed, before any outcome, a measure of "the flow-side size of the tail that no fix reaches": Packagist's share of September installs from PHP 8.1 and older, 10.0 per cent (583.7 of 5,809.9 million). From outside, the same branches are 54.7 per cent of version-reporting services. One ecosystem, two instruments, the old layer most of the picture from one side and a tenth of it from the other: that is the essay's argument in one pair of numbers, and it was anticipated by the brief, not found after the fact. Node.js's 12 to 16 per cent unfixed download share then reads as an inside number of the same kind, which is what the draft's "that number means something different" gestures at without showing.
Proposed: a paragraph in the blind-spots section: "The old branches show how far apart the two views sit. From outside, branches no fix reaches are more than half of the PHP services that announce a version. From inside, only 10 per cent of the Composer installs Packagist logged in September came from those branches. Node.js's unfixed share, about 12 to 16 per cent of daily downloads around the release, is an inside number of the same kind: old lines still fetched, not old servers still running. Months, units and populations differ, so no number here measures another. But the same layer of old software is most of the picture from one side and a small part of it from the other." Note the care needed: this must not itself become a similar-numbers-agree argument; the proposed wording says so.

**S4. The download log's reach is never stated.** "The Node.js project publishes how many times each exact version was downloaded from nodejs.org each day."
What is wrong: LH034's brief lists what the log does not see: distribution packages, Homebrew bottles, official container images once built, corporate mirrors and caches, runners that keep their own copy. Without this, "the download log" sounds like Node.js's whole rebuilt world. This is the one qualification the Node.js half needs; place it once.
Proposed: "Copies taken from a Linux distribution, a ready-made container image or a company's mirror never reach it."

**S5. Two uncited negatives.** "We found no public count of Node.js servers by version, and Node.js has no habit of announcing its version to visitors."
What is wrong: no search for such a count is recorded in LH034, and the second clause cites nothing.
Proposed: "We know of no public count of Node.js servers by version." Drop the second clause, or cite Node.js's documentation.

**S6. The windows metaphor, extended so that it seems to contradict the earlier piece.** "The same holds here, with one addition: where a window's edge falls tells you something about what lies beyond it."
What is wrong: articles/what-we-can-see.md says "A gap is evidence of neither... It only marks where our sources stop." "What lies beyond it" reads as the opposite. The essay's real point is that the frame's position says something about the system the instrument is pointed at.
Proposed: "In an earlier piece we described public sources on AI activity as windows, clear within their frame and showing nothing beyond it. That still holds. What this comparison adds is that where a window's frame falls can tell you something about the thing it is pointed at."

**S7. Too many metaphors, one misleading.** "census of residents", "What each light cannot see", "partial lights", "windows with soft edges", "strata".
What is wrong: four image systems in one essay. "Census" implies a complete enumeration, when more than half of PHP services report no version, and it sits awkwardly beside the name Censys. "Lights" competes with the house's windows. Strata is vivid and earns its place, but "each a layer of the web laid down in a different year" implies the services were installed in the branch's release year, which is not known.
Proposed: drop "census of residents"; head the section "What each view cannot see" and say "partial views"; keep strata with "each first released in a different year, each still answering on the internet".

**S8. The "Texture" section.** "Some of what the instruments show is texture rather than measurement" and "And who acts on a fix differs. For a Python library it is usually a lockfile or a test job. For Node.js it is an image maintainer, a version manager or a build step. For a great deal of PHP it is a hosting company, or nobody."
What is wrong: the weekend figures are measurements; what distinguishes them is that they were not among the planned measures. The "who acts" paragraph measures nothing ("usually", "a great deal", "nobody" are unsupported), a lockfile does not act, and the paragraph repeats the standing-and-rebuilt section.
Proposed: head it "The working week"; open "Two details we did not set out to measure, noticed after the counts were in."; cut the "who acts" paragraph.

**S9. The leap to AI.** "An agent that writes code, a bot that moves a pin, a crawler that reads pages: each is part of one of these layers, and anything that spread through the internet, deliberately or not, would have to travel through them at their speeds and past their blind spots. Lighthouse exists to tell whether..."
What is wrong: a crawler is not part of a software layer; it reads pages the standing layer serves. "Would have to" is a claim, not a reading; the essay should own it as expectation. "Lighthouse exists to" puts the institution in the prose where the house voice is "we".
Proposed: "An agent that writes code and a bot that moves a pin work in the rebuilt layer; a crawler reads pages the standing layer serves. Anything that spread through the internet, deliberately or not, would, we expect, travel through these layers at their speeds and past their blind spots. We keep this watch to be able to tell whether..." Merge the following "Much of that map already exists" paragraph into one closing sentence of the section to keep the story moving.

**S10. "Turns over within days" is stronger than Node.js's own comparison.** "a rebuilt layer that turns over within days"
What is wrong: LH034's same-instrument comparison, the July 2026 security release, has line 22 first at half on day 18 and line 24 at 29.4 per cent on day 7, with day-to-day swings of up to about 20 points. October's lines all passed half on day 2, but one release does not make "within days" a property of the layer.
Proposed: "a rebuilt layer that turns over quickly unless a list holds it still".

**S11. The opening tells rather than shows.** "The curves are interesting. What we had to do to see them is, we think, more interesting still."
What is wrong: AGENTS.md asks a piece to open with the thing itself and give a reason to care. The draft's best material, that one fix could be seen only from outside and the other only from inside, is held back to section one.
Proposed: "We set out to watch both spread, and found we could not watch them the same way. PHP we could see only from outside, by the servers that announce their version. Node.js we could see only from inside, by the project's record of what was downloaded. That difference, we came to think, is part of what we were seeing." Summary to match: "On 21 October 2026 PHP and Node.js both released security fixes. We could watch PHP's spread only from outside, through the servers that announce their version, and Node.js's only from inside, through downloads. This essay argues that how each could be seen, and what each view misses, says something about how the software lives."

**S12. "Python's fixes".** "Python's fixes held between 54 and 61 per cent of their libraries' downloads the day after release, and then rose only slowly"
What is wrong: these are four security fixes in four libraries, not Python's fixes in general.
Proposed: "Four security fixes held between 54 and 61 per cent of their libraries' downloads the day after release, and only 57 to 72 per cent a month on."

**S13. Jargon a curious reader trips on.** "headers", "branch" and "line" (used for the same idea without definition), "lockfile", "coincidence of scale", "Triangulation", "certificate logs, routing data".
Proposed: define a header once ("a label on every page it sends that browsers receive but do not show"), a branch once ("one of the parallel release lines a project keeps, such as PHP 8.3 and 8.4, each with its own fix"), a lockfile once; "a coincidence, not an agreement"; head the section "Side by side".

## Optional

**O1.** "Censys, a company that scans the whole internet": "a company that scans the internet's addresses" is more exact.

**O2.** "a habit from an earlier web that many servers still keep": the history is uncited; a figure from the records is more concrete: "On 26 October, 43.5 million services still reported one."

**O3.** "some of them more than a decade old": it is the branches, not the services, whose age is known (5.2 and 5.6 date from 2006 and 2014 by php.net's release history, not cited in the essay); "some first released more than a decade ago". Cite php.net's releases page if the keeper wants every claim linked.

**O4.** "more than half of those reporting a version": correct (54.7 per cent). For the release piece, not the essay, it may help a reader to know that the 23.8 million are 23.1 per cent of all PHP services Censys counted on 26 October.

**O5.** Day 5 shows a Node.js download share can fall as well as rise (line 26 from 77.3 to 61.5 per cent on Monday 26 October). Not needed in the essay; worth a sentence in the week-one piece, since it shows a flow behaving unlike a stock.

**O6.** The header could carry `investigation: software-updates`, as the related pieces do, if essays are to be listed with an investigation.

**O7.** The ending, "We will revise this essay when the day-30 figures are in", is plain and right for a section of tests; the essay's emotional close is the map paragraph, which the revision keeps immediately before the tests.

**O8.** The colophon should say, once applied, that the draft was revised after this review.

## What the revision changes in the claims

Every figure in the revision is in the records named above. Changes of claim, as against the draft: the old branches are no longer said never to have a fix (M1); Censys counts services (M2); the no-version share is no longer set beside careful administrators, and care and neglect are called blind spots, not measures (M3); automation is said to cut both ways, with the released build-server flag finding added (M4); the claim that standing servers show no weekly rhythm is withdrawn and the standing-and-rebuilt test replaced (M5); "older lines lag" gains the Ubuntu 8.3 caveat (M7); 102 pins, not projects (M8); PHP's rebuilt side and the Packagist 10.0 per cent figure are added (S2, S3); the nodejs.org log's reach is stated (S4); "within days" becomes "quickly" (S10); "who acts" is cut (S8). The rest is wording. Length: about 1,890 words of body against 1,720, the added length being S3 and the caveats in M1, M4 and S4; the "who acts" paragraph, the "Texture" preamble and the separate map paragraph were cut to pay for them.

## Calculations

Run with `python3 -I check.py`, reading only the retained tables.

```python
import json, datetime
php = json.load(open('/home/user/lighthouse/studies/LH033/data/read-2026-10-27T0637Z/tables.json'))
py  = json.load(open('/home/user/lighthouse/studies/LH033/data/python_side.json'))
node = json.load(open('/home/user/lighthouse/studies/LH034/data/tables.json'))

print("PHP day-5 patched share by branch:", {b: v['5']['share'] for b, v in php['m1_patched_share_by_branch'].items()})
t = php['m2_unfixed_tail']
d5 = t['5']
print("PHP day 5: nofix %.1fM, share of versioned %.4f, share of all %.4f, unknown share of all %.4f"
      % (d5['affected_nofix']/1e6, d5['nofix_share_of_versioned'], d5['affected_nofix']/d5['all'], d5['unknown_share_of_all']))
for k in ('0','1','2'):
    print(f"PHP day {k} ({t[k]['day']}): all {t[k]['all']/1e6:.1f}M, unknown share {t[k]['unknown_share_of_all']:.3f}")
print("PHP all services, day 2 / day 1: %.2f" % (t['2']['all']/t['1']['all']))

fx = py['four_security_fixes']
for d in ('1','30'):
    vals = [v[d] for v in fx.values()]
    print(f"Python four fixes day {d}: {min(vals):.3f} to {max(vals):.3f}")
print("Python pins:", py['lh008_fix_pairs_moved_within'])

m1 = node['measure_1_2026-10']
print("Node measure 1 keys:", list(m1)[:5])

bl = m1['by_line']
print("Node day-5 at-or-newer share by line:", {l: bl[l]['5']['share'] for l in bl})

tail = node['measure_2_unfixed_tail']
win = {d: v for d, v in tail.items() if '2026-10-18' <= d <= '2026-10-26'}
u = [v['unfixed_share'] for v in win.values()]
print("Node unfixed share, 18 to 26 Oct: %.4f to %.4f" % (min(u), max(u)))
for d in sorted(tail):
    if d >= '2026-10-16':
        wd = datetime.date.fromisoformat(d).strftime('%a')
        print(d, wd, "total %.1fM" % (tail[d]['total']/1e6))
wk = [tail[d]['total'] for d in ('2026-10-21','2026-10-22','2026-10-23','2026-10-26')]
we = [tail[d]['total'] for d in ('2026-10-24','2026-10-25')]
print("weekend mean / weekday mean (21-23, 26 Oct): %.2f" % ((sum(we)/2)/(sum(wk)/4)))
wk0 = [tail[d]['total'] for d in ('2026-10-12','2026-10-13','2026-10-14','2026-10-15','2026-10-16','2026-10-19','2026-10-20')]
we0 = [tail[d]['total'] for d in ('2026-10-17','2026-10-18')]
print("weekend before: %.1f to %.1fM, against weekdays %.1f to %.1fM; ratio of means %.2f" % (min(we0)/1e6, max(we0)/1e6, min(wk0)/1e6, max(wk0)/1e6, (sum(we0)/2)/(sum(wk0)/len(wk0))))
sats = [d for d in sorted(tail) if datetime.date.fromisoformat(d).weekday() >= 5]
print("every weekend day held, total in millions:", {d: round(tail[d]['total']/1e6,1) for d in sats if d >= '2026-09-23'})

# Every week held since 23 September: weekend-day mean over weekday mean (Mon to Fri of the same week)
weeks = {}
for d in sorted(tail):
    if d < '2026-09-21': continue
    dt = datetime.date.fromisoformat(d)
    wk = (dt - datetime.timedelta(days=dt.weekday())).isoformat()
    weeks.setdefault(wk, {'wd': [], 'we': []})['we' if dt.weekday() >= 5 else 'wd'].append(tail[d]['total'])
for wk, v in weeks.items():
    if v['wd'] and v['we']:
        print("week of", wk, "weekday %.1f to %.1fM, weekend %.1f to %.1fM, ratio of means %.2f" % (
            min(v['wd'])/1e6, max(v['wd'])/1e6, min(v['we'])/1e6, max(v['we'])/1e6,
            (sum(v['we'])/len(v['we']))/(sum(v['wd'])/len(v['wd']))))
```

Output:

```
PHP day-5 patched share by branch: {'8.2': 0.496, '8.3': 0.4901, '8.4': 0.6452, '8.5': 0.7571}
PHP day 5: nofix 23.8M, share of versioned 0.5472, share of all 0.2311, unknown share of all 0.5778
PHP day 0 (2026-10-21): all 56.9M, unknown share 0.284
PHP day 1 (2026-10-22): all 61.4M, unknown share 0.321
PHP day 2 (2026-10-23): all 95.8M, unknown share 0.560
PHP all services, day 2 / day 1: 1.56
Python four fixes day 1: 0.538 to 0.608
Python four fixes day 30: 0.573 to 0.723
Python pins: {'pairs': 102, '7 days': 18, '30 days': 50, 'clock': 'committer time after release, as LH008 data/lags.csv'}
Node measure 1 keys: ['day0', 'fixed', 'by_line', 'first_day_at_half', 'summary_days']
Node day-5 at-or-newer share by line: {'22': 0.527, '24': 0.6929, '26': 0.615}
Node unfixed share, 18 to 26 Oct: 0.1179 to 0.1646
2026-10-16 Fri total 24.2M
2026-10-17 Sat total 14.2M
2026-10-18 Sun total 12.9M
2026-10-19 Mon total 24.6M
2026-10-20 Tue total 26.3M
2026-10-21 Wed total 27.4M
2026-10-22 Thu total 30.3M
2026-10-23 Fri total 35.1M
2026-10-24 Sat total 16.2M
2026-10-25 Sun total 16.1M
2026-10-26 Mon total 30.5M
weekend mean / weekday mean (21-23, 26 Oct): 0.52
weekend before: 12.9 to 14.2M, against weekdays 21.3 to 27.1M; ratio of means 0.54
every weekend day held, total in millions: {'2026-09-26': 11.6, '2026-09-27': 11.5, '2026-10-03': 11.6, '2026-10-04': 11.3, '2026-10-10': 13.2, '2026-10-11': 12.5, '2026-10-17': 14.2, '2026-10-18': 12.9, '2026-10-24': 16.2, '2026-10-25': 16.1}
week of 2026-09-21 weekday 20.6 to 21.7M, weekend 11.5 to 11.6M, ratio of means 0.54
week of 2026-09-28 weekday 19.9 to 23.0M, weekend 11.3 to 11.6M, ratio of means 0.52
week of 2026-10-05 weekday 20.9 to 25.5M, weekend 12.5 to 13.2M, ratio of means 0.55
week of 2026-10-12 weekday 21.3 to 27.1M, weekend 12.9 to 14.2M, ratio of means 0.55
week of 2026-10-19 weekday 24.6 to 35.1M, weekend 16.1 to 16.2M, ratio of means 0.56
```

From the records without calculation: the Packagist figure, 583.7 of 5,809.9 million September installs from PHP 8.1 or older (10.0 per cent), is in studies/LH033/checkpoints/2026-10-25.md; the branch order 7.4, 8.1, 7.2, 5.6, 5.2 among unfixed branches matches both that checkpoint and the snapshot in data/read-2026-10-27T0637Z/censys.raw.gz (7.4 at 8.05 million, 8.1 at 2.74, 7.2 at 2.26, 5.6 at 2.12, 5.2 at 2.01); the July comparator (line 22 first at half on day 18; line 24 at 4.3, 29.4 and 61.4 per cent on days 1, 7 and 30) is in studies/LH034/checkpoints/2026-10-27.md; the build-server flag figures (32 against 41 per cent, 96 of 104 releases) are in articles/two-days-for-most.md and studies/LH011/LH011.md.

## Resolution, by the driving session

27 October 2026. The reviewer's revised text was adopted in full as essays/seen-from-outside-seen-from-inside.md, with three changes: the title is "Seen from outside, seen from inside" rather than the reviewer's proposal (the keeper's call, offered to them); the leading HTML comment, which the site renders as literal text, became a sentence in the colophon; and the file was renamed to match the title. Before adopting, the driving session checked each figure the revision adds against the records: 43.5 million version-reporting services on 26 October (23,818,548 on unfixed branches at 54.72 per cent, LH033 tables of read 2026-10-27T0637Z); the build-server flag at 32 against 41 per cent over 104 releases (articles/two-days-for-most.md); Censys's total rising from 61.4 to 95.8 million services between 22 and 23 October (the same tables); the four weekends before 24 and 25 October, each at 11 to 14 million downloads a day against 20 to 27 million on weekdays (LH034 tables); line 24 of the July release moving from 29.4 per cent on day 7 to 61.4 on day 30 (LH034 checkpoint); and Packagist's 10.0 per cent (LH033 checkpoint of 25 October). All match. The essay remains a draft; its release review (a figure and citation check, then the reader-and-inference review) follows when its figures are replaced by the reviewed week-one figures.
