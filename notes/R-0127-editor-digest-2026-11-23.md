# R-0127: check of the Editor run's This week lines of 23 November 2026

**In short.** A fresh agent checked the day's line and the three items dated 23 November in site/this-week.md against the records they rest on. Two things must change: the PHP item says Cloudflare tells readers to switch the feature off, which Cloudflare's notice has never said in any read, and the day's line says Debian, Red Hat and SUSE list the newer PHP flaw "fixed", where they list fixed packages while SUSE's overall state is "Pending" and Debian and Red Hat still mark some releases vulnerable or affected. The other figures hold. Two suggestions are optional.

Checker: a fresh Opus 5.5 subagent (claude-opus-5-5, as reported by the harness), called by the Editor run of 23 November 2026. Offline, no network request, no file changed but this note. A second agent's agreement is a review contribution, not independent confirmation.

## What was read

- site/this-week.md (header comment, line 52 `today:`, the three 2026-11-23 items, and the earlier items for consistency of wording); notes/editor/plan.md (the day's line rule); site/_includes/home-this-week.njk and site/lib/front.js's comment (the day's line shows as Live, meaning unreviewed).
- studies/LH036/checkpoints/2026-11-23.md and 2026-11-19.md; studies/LH036/LH036.md header, In short and Answer; investigations/model-found-bugs.md; studies/LH038/LH038.md In short and T0.
- studies/LH030/checkpoints/2026-11-23.md in full; studies/LH030/brief.md and checkpoints/2026-10-24.md on Cloudflare's classes.
- studies/LH033/LH033.md header, In short, Answer and first Findings tables (version 1.2).
- studies/LH047/LH047.md header, In short, Part C week 47 Answer, W1, W5, Limits, Next and Corrections (version 0.6); notes/R-0126-lh047-reaudit-recheck.md opening (R-0125 was not reread beyond its resolution as reported in the record's Corrections).

## Day's line

> An exploit-prediction score for the Linux flaw Anthropic's model found jumped from under 1% to 82% on 21 November; no source we read says why. Debian, Red Hat and SUSE list PHP's newer flaw fixed.

**First sentence: fine, with a suggestion.** Source: LH036 checkpoint of 23 November, "0.00777 (0.78 per cent) for 19 and 20 November and 0.8213 (82.13 per cent), percentile 0.99664, for 21 and 22 November"; "Nothing in this read's sources dates or explains it". "Under 1%", "82%" and "21 November" are exact; "no source we read says why" matches. The line is shown labelled Live, which marks it unreviewed, so it needs no "unreviewed" of its own.

Suggestion (referent): the records say Anthropic's model *wrote an exploit for* the flaw (investigation page: "five attack chains found with an unreleased internal model, among them an exploit the model wrote for CVE-2026-98432"; LH038: "the one Anthropic's model wrote an exploit for"; the report date and reporter are unknown, LH038 T0). "Anthropic's model found" states Anthropic's account in our voice, and the investigation asks reviews to watch for wording easier on Anthropic than the sources allow. Earlier items this week use the same shorthand, so this is not a must-fix; if changed, change it here and leave the older items to age out. Replacement, one word longer: "the Linux flaw Anthropic says its model found".

**Second sentence: must fix.** Source: LH030 checkpoint of 23 November (unreviewed). Debian lists php8.2 bookworm and php8.4 trixie "vulnerable" beside fixed security-suite packages; Red Hat's `package_state` still lists RHEL 10 and RHEL 9 php streams as "Affected" beside nine fixed releases; SUSE's "Overall state of this security issue: Pending" beside a list of released packages. "List PHP's newer flaw fixed" reads as each tracker marking the flaw fixed, which none does as a whole. Replacement (same word count):

> Debian, Red Hat and SUSE now list fixes for PHP's newer flaw.

Full line with only the must-fix (37 words):

> An exploit-prediction score for the Linux flaw Anthropic's model found jumped from under 1% to 82% on 21 November; no source we read says why. Debian, Red Hat and SUSE now list fixes for PHP's newer flaw.

## Item: Censys and the PHP fix (lighthouse, front)

> Thirty days after October's emergency PHP fix, Censys counted 75% to 92% of internet-facing services in each fixed branch patched, nearly all within two weeks.

**Fine, with an optional suggestion.** Source: LH033 version 1.2, reviewed and rechecked: day 30 (20 November) shares 78.2, 75.0, 86.5 and 92.2 per cent; "Nearly all of that came in the first two weeks". 75% to 92% is exact after rounding; day 30 from 21 October is 20 November. "Censys counted ... patched" attributes the classification. A branch can only be known from a reported version, so "in each fixed branch" already restricts to version-reporting services. The record also calls the share a floor (distributions that fix PHP without changing its version); the linked record carries that, and the header asks for at most one short caveat. If a caveat fits, replacement (four words longer):

> Thirty days after October's emergency PHP fix, Censys counted 75% to 92% of internet-facing services in each fixed branch patched, a floor, nearly all within two weeks.

## Item: the newer PHP flaw's fix listed (reported)

> The fix for PHP's newer session flaw is now listed: the CVE record, Debian, Red Hat and SUSE put it at PHP's 19 November releases, while Ubuntu lists no fix yet and CERT-EU and Cloudflare still tell readers to switch the feature off.

**Must fix (Cloudflare).** Source: LH030 checkpoint of 23 November: CERT-EU still says "Set session.upload_progress.enabled=0 and restart every worker until the next regular bugfix release"; Cloudflare still says the flaw "affects fully patched PHP releases, including 8.5.12, and will be fixed in PHP's next regular release". Cloudflare's notice has been classed "no instruction" since the start (checkpoint of 24 October: "Cloudflare (link, explicit version scope, no instruction)"; brief: "its update paragraph carries neither the instruction nor PHP's condition"). The checkpoint's own In short calls CERT-EU and Cloudflare "the notices that carried it", which is loose and is the likely source of the slip; Research should correct that sentence when it writes the record.

The rest holds: the CVE record ends the affected ranges before 8.2.36, 8.3.37, 8.4.28 and 8.5.13 (19 November releases); Debian, Red Hat and SUSE list fixed packages at those versions (SUSE and Red Hat also list backported fixes for older branches, which "put it at" doesn't contradict); Ubuntu lists every package needs-triage with no patch. The item already says "unreviewed". Replacement (three words longer; the links unchanged):

> The fix for PHP's newer session flaw is now listed: [the CVE record](https://www.cve.org/CVERecord?id=CVE-2026-115560), Debian, Red Hat and SUSE put it at PHP's 19 November releases, while Ubuntu lists no fix yet, CERT-EU still tells readers to switch the feature off and Cloudflare still says a fix is coming. [Our last scheduled read](studies/LH030/checkpoints/2026-11-23.md), unreviewed.

## Item: our own requests, week 47 (lighthouse)

> We audited our own requests again, for 16 to 22 November: of 1,649 we logged, 2 broke a robots.txt rule under our own name and 53 broke some rule, mostly by coming sooner than a site's requested delay or going back to a page that had shown a wall. That's far fewer than on 8 November, but mostly because one collector isn't in this week, so it isn't a trend.

**First sentence: fine.** Source: LH047 0.6 In short and Part C week 47 Answer: 1,649 logged requests; 2 under Lighthouse's own token; 53 under reading A; most of the 53 Crawl-delay (40) or a return to a page that had answered with a wall (11). Version 0.6 is after the evidence review, the reader review and the recheck R-0126, so "reviewed record" holds.

**Second sentence: suggestion.** The record's "mostly because of one collector" is about robots.txt breaches (97 on 8 November, 85 of them one collector's), and "can't be compared as a trend" rests also on the floor of zero for unlogged requests and the different populations, not on the collector alone. "That's far fewer" leaves the reader to guess against which count. Replacement (same word count, 21; it drops the "so", which tied the trend caveat to the collector alone):

> That's far fewer than 8 November's 97 robots.txt breaches, mostly because one collector isn't in this week; it isn't a trend.

## Rules

No internal codes, em or en dashes, or Lighthouse claims of harm or compromise in any of the four. British English throughout. No absolute without its window.
