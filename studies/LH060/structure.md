# LH060: structure-only check of LH033's and LH039's retained aggregates

**In short.** We looked only at the shape of the data Lighthouse already holds from its PHP and WordPress studies (key names, value types and CSV headers, never a value), to see whether anything there could stand in for an operator's size. One thing could: Censys's dashboard data, kept with every PHP read, carries a list by autonomous system (a network operator's routing identity) with counts of services and addresses per network. Nothing in the WordPress study's files does. Under the brief nothing already read is split by it; a proposal for a study on future reads goes to the next horizon sweep's gate.

Row LH060-structure, Research run 2026-11-25T151200Z-anthropic-research (Claude Code, Opus 5.5), 25 November 2026. Script: [scripts/structure.py](scripts/structure.py), run as `python3 -I studies/LH060/scripts/structure.py > studies/LH060/structure.txt` from the repository root. Output: [structure.txt](structure.txt). The script prints key paths with list positions collapsed to `[*]` and every digit in every key replaced by `#`, value types, and CSV header rows; it prints no value. It also reports, for each named file, whether the same-named file in each other read directory has the same masked key paths (same or different only). The files are exactly those the brief names, with `roots-7.1.4.json` and `johnpbloch-7.1.4.json` as the brief's "one" file of each kind. `.body` files, php.net release pages and git history were not opened.

## Candidate size field (file and label only)

- `studies/LH033/data/read-2026-11-21T1414Z/censys.raw.gz`: `.snapshot.asns[*]`, with labels `asn`, `as_name`, `services`, `ips`, `patched`, `affected`, `affected_nofix`, `affected_services`, `unknown`. An autonomous system is on the brief's list of candidate size fields, and `services` and `ips` per network are counts per operator. The same key paths are in all twelve other LH033 read directories' `censys.raw.gz`.

Not size proxies under the brief: `.snapshot.countries[*]` (country), branch and version labels throughout.

Not settled by structure, and not looked at: whether `asns` lists every network or only a top few, and whether one autonomous system is one operator (a hosting provider's network holds many customers' services, so a network's size is not its customers' size). W3Techs's derived files in both studies hold table rows as lists of strings (`.extracted.diagrams[*].rows[*][*]`); what those rows label can't be told from structure, and they were not read.

## What follows

As the brief says: no split of data already seen is made, and no value was read. A proposal for a study of patched shares by network size on Censys reads not yet taken is added to proposals.md for the next sweep's fresh gate. Its research safety question, that a per-network table names operators beside unpatched counts, is for that gate; the proposal offers size bands only, with no network named.

## Other structure facts (no values)

Same-name files differ in key paths across reads for LH033's `tables.json` (9 of 12 differ: later reads add measures) and `w3techs-history_details-8.3.derived.json` (4 of 5 differ: the month keys differ by read), and for one of LH039's `w3h-71.derived.json` and one `readlog.csv`. These are expected from the collectors' histories and bear on nothing here.
