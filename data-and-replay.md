# Data and replay

What each study keeps of what it read, where to find it, and how to rerun the study's figures from it. Most of our studies keep the raw responses, tables and scripts behind every figure, so you can check a number without asking us. The files live in the repository on GitHub, not on this site; each "data" link below opens the study's folder there. Sizes are on disk, as of 14 November 2026.

**On disk, 14 November 2026:** 49 studies have a data folder, holding 5,150 files and about 330 MB. 19 of them have a replay script (12 `replay.sh`, 7 `replay.py`); 18 more name another offline command that rebuilds or checks their figures; 12 keep their data with no offline rerun.

## Before you run anything

- Run every command from the top of a copy of the repository (`git clone https://github.com/JKershaw/lighthouse`).
- You need Python 3. The download studies (LH011 to LH014) also need the `packaging` library; their scripts note that version 24.0 was used. LH016's replay needs the repository's git history.
- A replay reads only what's kept and makes no network request, unless its line below says otherwise. Some compare their output with the kept files and change nothing; others rewrite their tables or figure in place, so `git status` afterwards is the check: a replay that reproduces the record leaves nothing changed.
- A collector script (usually `collect.py`) is different: it reads the live sources again, so it makes a new read rather than a replay, and what it finds may differ. We haven't listed those commands here.
- Where a line says it ran cleanly, we ran that command on 14 November 2026 and it finished without error or changed file. The others are as their records give them; we didn't run them for this page.

## Studies with a replay script

- **[LH010](studies/LH010/)**, pinned software and fixes that say so, counted library by library. [Data](studies/LH010/data/), 2.1 MB: the events, lags, fix texts and the reanalysis tables. `sh studies/LH010/replay.sh` ([script](studies/LH010/replay.sh)); ran cleanly. Add `--write` only after a deliberate change.
- **[LH011](studies/LH011/)**, how fast new releases of 37 Python libraries took half the downloads. [Data](studies/LH011/data/), 4.6 MB: download counts by version and day, build-server flags and the analysis tables. `sh studies/LH011/replay.sh` ([script](studies/LH011/replay.sh)).
- **[LH012](studies/LH012/)**, what keeps older versions downloaded. [Data](studies/LH012/data/), 20 MB: one week's downloads by version, Python, installer and system, with the requirements read. `sh studies/LH012/replay.sh` ([script](studies/LH012/replay.sh)); it also checks the files against hashes posted before any count.
- **[LH013](studies/LH013/)**, whether what stays behind held for two more weeks. [Data](studies/LH013/data/), 7.4 MB. `sh studies/LH013/replay.sh` ([script](studies/LH013/replay.sh)).
- **[LH014](studies/LH014/)**, the two-day pace below the top fifty libraries. [Data](studies/LH014/data/), 7.4 MB. `sh studies/LH014/replay.sh` ([script](studies/LH014/replay.sh)).
- **[LH015](studies/LH015/)**, whether container recipes install what the pin names. [Data](studies/LH015/data/), 9.8 MB: the recipe lines, classes and judgements. `sh studies/LH015/replay.sh` ([script](studies/LH015/replay.sh)).
- **[LH016](studies/LH016/)**, which steps of our own workflow changed what pieces say. [Data](studies/LH016/data/), 252 KB: the coded changes and the blind comparison. `bash studies/LH016/replay.sh` ([script](studies/LH016/replay.sh)).
- **[LH017](studies/LH017/)**, whether test and build workflows install what the pin names. [Data](studies/LH017/data/), 23 MB. `sh studies/LH017/replay.sh` ([script](studies/LH017/replay.sh)).
- **[LH023](studies/LH023/)**, a Drupal image's published recipe and base. [Data](studies/LH023/data/), 68 KB: one snapshot of retained responses. `python3 studies/LH023/scripts/replay.py` ([script](studies/LH023/scripts/replay.py)); ran cleanly.
- **[LH024](studies/LH024/)**, institutions' first-day notices about the PHP emergency. [Data](studies/LH024/data/), 18 MB: the panel's responses and daily search notes. `python3 studies/LH024/scripts/replay.py` ([script](studies/LH024/scripts/replay.py)); ran cleanly. Article bodies weren't kept, so their hashes can't be checked offline, as the script says.
- **[LH026](studies/LH026/)**, Drupal's image layers on the fixed PHP base. [Data](studies/LH026/data/), 40 KB. `python3 studies/LH026/scripts/replay.py` ([script](studies/LH026/scripts/replay.py)); ran cleanly.
- **[LH027](studies/LH027/)**, an outage notice the direct reader couldn't get. [Data](studies/LH027/data/), 12 KB: the one refused response. `python3 studies/LH027/scripts/replay.py` ([script](studies/LH027/scripts/replay.py)); ran cleanly.
- **[LH028](studies/LH028/)**, the first public attack trace, read about every six hours. [Data](studies/LH028/data/), 4.1 MB: six snapshots of three pages. `python3 studies/LH028/scripts/replay.py --snapshot 2026-10-22` ([script](studies/LH028/scripts/replay.py)), naming any snapshot folder's date; ran cleanly for that one.
- **[LH029](studies/LH029/)**, PHP's own notice of 23 October. [Data](studies/LH029/data/), 124 KB. `python3 studies/LH029/scripts/replay.py` ([script](studies/LH029/scripts/replay.py)); ran cleanly.
- **[LH032](studies/LH032/)**, PHP fixes in products, by the Dutch NCSC's list. [Data](studies/LH032/data/), 18 MB: each read of the list. `python3 studies/LH032/review/replay.py <clone>` ([script](studies/LH032/review/replay.py)) needs a local clone of the NCSC-NL/php2shell repository, which the script reads at a pinned commit; making that clone is the one network step.
- **[LH041](studies/LH041/)**, the registry worms, dated. [Data](studies/LH041/data/), 12 MB. `sh studies/LH041/replay.sh` ([script](studies/LH041/replay.sh)); it rewrites the tables and figure from the kept read.
- **[LH042](studies/LH042/)**, published counts of exposed AI services. [Data](studies/LH042/data/), 8.2 MB. `sh studies/LH042/replay.sh` ([script](studies/LH042/replay.sh)); it checks every quotation against the kept pages and rebuilds the table and figure.
- **[LH046](studies/LH046/)**, how complete GH Archive's hourly files are. [Data](studies/LH046/data/), 3.9 MB: counts per hour, not the files themselves (refetching them is about 17 GB). `sh studies/LH046/replay.sh` ([script](studies/LH046/replay.sh)); it rewrites the results and figure.
- **[LH047](studies/LH047/)**, the rules sites set for automated readers, and how well we kept them. [Data](studies/LH047/data/), 11 MB: our requests, the robots.txt copies and the audit. `sh studies/LH047/replay.sh` ([script](studies/LH047/replay.sh)), then `python3 -I studies/LH047/review/brief_as_fixed.py` for the count under the brief as fixed.

## Studies with another offline command

- **[LH002](studies/LH002/)**, a small software neighbourhood's public records. [Data](studies/LH002/data/), 152 KB: the tables. `python3 studies/LH002/scripts/summarise.py studies/LH002` prints the headline figures from them; ran cleanly.
- **[LH008](studies/LH008/)**, what moves a pin on four libraries. [Data](studies/LH008/data/), 1.1 MB. `python3 studies/LH008/scripts/analyse.py` rebuilds the tables with no network access, but its shared code imports the `requests` library, so that must be installed; it stopped for that reason here.
- **[LH009](studies/LH009/)**, fixes that said so. [Data](studies/LH009/data/), 852 KB. `python3 studies/LH009/scripts/analyse.py`, with the same `requests` caveat as LH008.
- **[LH018](studies/LH018/)**, the PHP fix's first public trail downstream. [Data](studies/LH018/data/), 420 KB: the first snapshot. `python3 studies/LH018/scripts/analyse.py`; ran cleanly.
- **[LH019](studies/LH019/)**, the official PHP image tags over time. [Data](studies/LH019/data/), 284 KB: four snapshots. `python3 studies/LH019/scripts/analyse.py --snapshot 2026-10-21`, naming a snapshot's date; ran cleanly for that one.
- **[LH020](studies/LH020/)**, from PHP's notice to the official images. [Data](studies/LH020/data/), 816 KB. `python3 studies/LH020/scripts/analyse.py`; ran cleanly.
- **[LH021](studies/LH021/)**, what consumer image repositories show of a rebuild. [Data](studies/LH021/data/), 756 KB. `python3 studies/LH021/scripts/analyse.py`; ran cleanly.
- **[LH025](studies/LH025/)**, five derived PHP image tags, read daily. [Data](studies/LH025/data/), 704 KB. `python3 studies/LH025/scripts/intervals.py`; ran cleanly.
- **[LH030](studies/LH030/)**, PHP's mitigation advice in public notices. [Data](studies/LH030/data/), 62 MB: every read of the panel. `python3 studies/LH030/scripts/classify.py studies/LH030/data/read-2026-10-23T1715Z && python3 studies/LH030/scripts/tabulate.py studies/LH030/data/read-2026-10-23T1715Z` for the baseline; the record gives the same two commands for later reads.
- **[LH033](studies/LH033/)**, PHP's fix on internet-facing servers, by Censys, W3Techs and Packagist. [Data](studies/LH033/data/), 1.1 MB. The record lists four commands, starting `python3 studies/LH033/scripts/tabulate.py 2026-10-29T0635Z`.
- **[LH034](studies/LH034/)**, Node.js's fix in nodejs.org's downloads. [Data](studies/LH034/data/), 872 KB. `python3 studies/LH034/scripts/tabulate.py`; ran cleanly.
- **[LH035](studies/LH035/)**, who watches each layer of the internet. [Data](studies/LH035/data/), 9.5 MB: the instruments and the pages read. `python3 studies/LH035/scripts/searchlog.py && python3 studies/LH035/scripts/build.py && python3 studies/LH035/scripts/diagram.py`.
- **[LH036](studies/LH036/)**, the kernel flaw a model exploited. [Data](studies/LH036/data/), 2.5 MB. `python3 studies/LH036/scripts/tabulate.py`; ran cleanly.
- **[LH037](studies/LH037/)**, vendors that ship PHP. [Data](studies/LH037/data/), 3.7 MB. `python3 -I studies/LH037/scripts/rescore.py` rescores the kept pages under both mention rules; ran cleanly.
- **[LH039](studies/LH039/)**, WordPress's fix for its own updater. [Data](studies/LH039/data/), 3.4 MB. `python3 -I studies/LH039/scripts/tabulate.py --packagist <label>`, naming one of its kept Packagist reads.
- **[LH040](studies/LH040/)**, the poisoned LiteLLM release. [Data](studies/LH040/data/), 8.0 MB. `python3 -I studies/LH040/scripts/tabulate.py --read 2026-11-09T1432Z`; ran cleanly.
- **[LH044](studies/LH044/)**, shared services closing their doors. [Data](studies/LH044/data/), 5.9 MB: every read's responses. `python3 -I studies/LH044/scripts/test_lh044.py` re-classifies the baseline's kept responses and checks the collector's rules offline.
- **[LH048](studies/LH048/)**, the flaws behind Anthropic's five attack chains. [Data](studies/LH048/data/), 644 KB. `python3 -I studies/LH048/scripts/summarise_read.py <read folder>`, naming one of its read folders.

## Studies that keep data with no offline rerun

Their records say what was read and keep it, with hashes, but give no command that rebuilds the figures offline. For the oldest, rerunning the scripts reads the live sources again.

- **[LH005](studies/LH005/)**, whether a public record connects a release to its installation. [Data](studies/LH005/data/), 1.3 MB: download-count query results.
- **[LH006](studies/LH006/)**, what published images installed. [Data](studies/LH006/data/), 2.5 MB.
- **[LH007](studies/LH007/)**, open ranges and pins after one release. [Data](studies/LH007/data/), 5.6 MB.
- **[LH022](studies/LH022/)**, a Drupal image link that couldn't be selected. [Data](studies/LH022/data/), 332 KB.
- **[LH031](studies/LH031/)**, PHP flaws in CISA's exploited list. [Data](studies/LH031/data/), 48 MB: every read of the catalogue.
- **[LH038](studies/LH038/)**, the kernel flaw's disclosure timeline. [Data](studies/LH038/data/), 140 KB: the disclosure policies read.
- **[LH043](studies/LH043/)**, evaluation agents on the open internet. [Data](studies/LH043/data/), 9.2 MB: the accounts read and the fetch log.
- **[LH045](studies/LH045/)**, records that roll over. [Data](studies/LH045/data/), 11 MB: captures of Epoch AI's data-centre records and the IETF's agent drafts, kept for a later study.
- **[LH049](studies/LH049/)**, the compromised bee-js release on npm. [Data](studies/LH049/data/), 960 KB.
- **[LH050](studies/LH050/)**, armed robots and human control. [Data](studies/LH050/data/), 3.2 MB: two dated reads.
- **[LH051](studies/LH051/)**, a CI secret stealer's traces, hour by hour. [Data](studies/LH051/data/), 528 KB: hourly counts; its record, with a replay command, is still to come.
- **[LH052](studies/LH052/)**, AI, organisational capacity and reliability. [Data](studies/LH052/data/), 40 KB: coding data and hashes; full source bodies weren't kept.
