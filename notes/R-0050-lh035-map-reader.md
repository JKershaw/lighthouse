# R-0050: LH035 map, reader stage

## What a reader would believe, written before reading the record

**Principal finding, said back.** In November 2026 Lighthouse read the public pages of 48 free-to-use instruments that watch the internet. Each of ten layers, from cables to traffic, has at least one watcher. But each watcher sees only part of its layer, the part visible from where it sits. Eleven of the 48 build on others, so there are fewer independent views than instruments.

**Observed.** What the instruments' own pages say: who publishes what, on which layer, free or not; 11 draw on another; about 17 state no limits; one (Epoch's AI data centres) estimates its own completeness at about 45 per cent; Censys's page claims broad IPv6 coverage that its own paper denies; NVD reports a backlog; EPSS's training data are private. The routing figures (1.3 per cent of about 74,000 networks; 192,000 links against 401,000) are two preprints' numbers, not Lighthouse's.

**Explained.** "Each sees from where it stands": inside a network, probing from outside, or collecting reports. The piece labels this its own reading, made from 40 of the 48 rows and untested. A reader may still take it as the finding, because the title and both summaries state it flatly.

**Caused.** Nothing causal is claimed beyond position limiting view, and shared sources letting one gap spread through several instruments.

**Limits a reader would notice.** Documentation, not data; counts are of instruments, not coverage. Not a census: crt.sh, OpenINTEL, IODA and the Internet Archive are missing, twenty leads went unread, and Shodan was left out because its pricing pages could not be read. Treating free-with-account as free is generous. Draft, not yet reviewed.

(README.md has no "Current focus" section, so nothing was read from it.)

## Stage two: against the record

Read: studies/LH035/ (LH035.md v0.3, brief.md, data/instruments.json, data/literature.json, review/recount_output.txt; sources.md and searchlog.md by the record's account), and programme.md, Next. My one calculation is studies/LH035/review/gap_kinds.py, with its output in gap_kinds_output.txt.

**What the round establishes**

The round establishes facts about the documentation. The instruments' own pages do say what the pieces quote. On 6 November, 214 of 228 quotations were found verbatim in the raw pages. The counts reproduce in review/recount_output.txt:
- the any-layer counts (certificates 3; names and running services 4 each);
- 11 of the 48 instruments draw on another;
- 17 state no limit (14 to 18 depending on how borderline rows are read);
- one gives a coverage percentage on its own pages.

Every layer has at least one instrument by the study's inclusion test. Each instrument observes from a stated vantage, and several gaps are position-shaped: routing collectors, traffic views and telescopes.

The round does not establish that gaps are "the same kind of thing each time". The record calls the vantage grouping a post hoc, untested reading (LH035.md, Findings, "Lighthouse's reading of the blind spots"). That reading predates the study: the brief takes it from the essay (brief.md, "What is already known"). The same writer wrote the blind-spot column and then grouped it.

**Material claim problems**

1. **The headline explanation is stated as the finding, and the pieces' own examples contradict it.**
   - Passages:
     - articles/who-watches-the-internet.md, title: "but each sees only from where it stands".
     - The same article, body: "it is the same kind of thing each time: each instrument sees from where it stands".
     - The same article, summary, which lists "the evidence behind the exploit-prediction score we read is private" as an instance.
     - articles/short/who-watches-the-internet.md: "they share a shape: each instrument sees from where it stands".
   - Evidence:
     - Of the seven gaps the full piece lists under "Why it matters", 2 are about position (routes, traffic). 3 are about access or payment (names list, running services, exploitation evidence), 1 is a definition (who downloads) and 1 is a chosen scan scope (IPv6).
     - Across the 48 rows' own blind_spot field, I code 30 as position. 10 are proxy or definition problems: a fetch is not an install, a proof of concept is not an attack, popularity is not existence. 2 are access, 5 are stale data or out of scope by design, and 1 is blank (review/gap_kinds_output.txt; this is my coding, not a test).
     - The measurements can all be correct while "same kind each time" is wrong: about a third of the gaps are about what is counted or who may read it, not where the instrument stands.
   - Resolution:
     - New title: "Every layer of the internet had a public watcher in November 2026, by what we found, but none sees the whole of its layer".
     - New body sentence: "What goes unwatched is narrower than a layer. Some of it is where an instrument stands, such as routing collectors in about 1.3 per cent of networks, or traffic seen one network at a time. Some is what it counts, such as a fetch that is not an install, or a ranking that is not a list of names. And some is who may read it: scanning data behind payment, or exploitation evidence kept private. That the gaps sort by where an instrument stands is our untested reading (below)."
     - Short form: "The gaps sit inside the layers: some come from where an instrument stands, some from what it counts, and some from who may read it."
     - The record's "In short" needs the same change.

2. **"Only one estimates how complete it is" drops the record's qualifier "on its own pages".**
   - Passage: articles/who-watches-the-internet.md, "Only one, an estimate of AI data centres, estimates how complete it is".
   - Evidence: Censys's own paper estimates its coverage at 98 per cent of IPv4 services on the top 10 ports and 62 per cent across all ports (data/literature.json, L01). The record limits its claim to "Epoch AI's pages" (LH035.md, Findings, "What the instruments say of themselves").
   - Resolution: "Only one, an estimate of AI data centres, gives a figure for its own completeness on the pages we read (about 45 per cent of deployed AI computing capacity); Censys's staff estimate theirs in a paper, at 98 per cent of IPv4 services on the most common ports and 62 per cent across all of them."

Not material, recorded for stage review:
- The 1.3 per cent figure counts vantage points as of May 2023 (L06), and the piece says "a 2024 preprint" honestly. It could add "in 2023".
- On running services, a no-account rule would leave only W3Techs, which measures websites rather than hosts. This sits uneasily with the record's line that a stricter reading would change no layer's coverage (Limits). The piece's last paragraph and its running-services paragraph already flag the choice.

**Readability**

1. The full piece's title is 26 words. The short form's "Who watches the internet?" could serve, with the finding moved to the standfirst.
2. Put the 90 per cent interval (30 to 78) beside "about 45 per cent", so that one number is not read as precise.

**Next step**

Adjust, then continue: fix the two passages above before release. The record's own Next item 4 would not separate the explanations in play:
- It proposes classing each instrument's vantage blind and comparing that with the blind-spot column.
- But that column was written by a writer who held the thesis, and inside/outside blind spots follow from vantage almost by definition, so agreement is expected whatever the truth.
- The live rival explanation is that gaps follow access terms and what is counted, not position.

A study that could separate them would code each instrument's own stated limits (cannot_see, in its own words, plus the literature) by kind, under a rule fixed in advance and blind to vantage, with two coders. It would then ask whether vantage predicts kind.

The evidence for that is already held, so it costs no new reads and could be done now. But it tests an essay's thesis and adds little to knowledge of the internet. I would not schedule it unless the essay's claim is to be repeated. Next items 2 and 3 (thin layers, names and IPv6) would improve the map more, but only if the map page is to be kept up. Otherwise, after release, the better step is an outward question.

## Resolution, by the driving session

Made by the driving session of the scheduled run 2026-11-07T1413Z. Both material problems were resolved as proposed. Problem 1: the title now ends "but none sees the whole of its layer"; the summary's "But each sees only from where it stands" became "But none sees the whole of its layer"; the body's "same kind of thing each time" sentence became the proposed three-way sentence (where an instrument stands, what it counts, who may read it); the opening's "the pattern we kept meeting" became "one we kept meeting"; the section heading "Where the watchers stand" became "Where each one stops"; the post hoc paragraph now says that, gone back over all 48, about a third of the blind spots were about what is counted or who may read it (review/gap_kinds_output.txt: 17 of 47 coded, by this review), labelled as itself a reading; the short form's sentence and summary, and the record's "In short", changed to match. Problem 2: the completeness sentence now says "on the pages we read" and gives Censys's paper's 98 and 62 per cent. Readability 2 was taken (the 90 per cent interval). Readability 1 was not: the title states the finding, as AGENTS.md asks. The two points judged not material were left. The next step is weighed at the programme checkpoint. The recheck reads both reviews' resolutions.
