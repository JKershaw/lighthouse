# LH035: Which public instruments observe the internet itself, at which layer, and where does each stop?

**Protocol 0.1, fixed 27 October 2026, before the survey's first read.** Writer: a Claude Code driving session (Claude Opus 5.5), at the keeper's agreement of the same evening that a map of the internet, as the terrain AI systems work in, is a standing aim, and that its first sketch should come from the research and instruments others already publish.

## Question

Which public instruments observe the internet's infrastructure, layer by layer; for each, what does it count, from where, how often, over what history, under what access terms, and what does it say it cannot see; and which layers, or which parts of them, does no public instrument found here observe?

LH003 asked the same of sources on AI activity. This study asks it of the terrain that activity runs on. It is the first sketch of a map, not a census: it describes instruments, measures nothing of the internet itself, and estimates no total.

## What is already known

The writer knows many candidate instruments from training and from Lighthouse's own use: Censys's PHP counts (LH033), W3Techs and Packagist (LH033), nodejs.org's download summaries (LH034), the Python package index's download records and ClickPy (LH011 to LH014), Docker Hub's registry (LH019, LH025), CISA's catalogue (LH031), the vulnerability records LH030 reads, and LH003's seventeen sources. That knowledge shapes the candidate list and is disclosed; every row is filled from the instrument's own pages read during this study, not from memory. The essay drafted the same evening (essays/seen-from-outside-seen-from-inside.md, unreleased) proposes that each instrument's blind spot sits on a characteristic side; that reading is not tested here, and the column that would bear on it is labelled below as interpretation.

## Layers, fixed now

1. **Physical and interconnection:** cables, facilities, exchange points.
2. **Routing:** the announcements that say which networks reach which addresses.
3. **Addresses and reachability:** which addresses answer, measured by scans or probes.
4. **Names:** the domain name system, zone files and ranked lists of domains.
5. **Certificates:** the public logs of certificates issued for websites.
6. **Running services and their software:** what answers on an address and port, and the versions it reports.
7. **Web content and technology:** crawls of pages and surveys of the technology websites use.
8. **Software supply:** registries, download logs and published images from which software is fetched.
9. **Vulnerability and exploitation records:** catalogues of flaws, fixes and observed exploitation, and decoy sensors.
10. **Traffic:** aggregate views of the traffic that crosses a network.

An instrument may sit on more than one layer. A layer that turns up no instrument is reported as such, as unobserved by what was found, not as empty.

## Population and unit

The unit is an instrument: a source that publishes observations of some layer across many organisations, with public documentation. Included when its documentation can be read without an account and some of its data can be read without payment (a free tier counts, and is described). Excluded: an organisation's view of its own estate only, a commercial product with no public data, a one-off paper whose data are not kept available, and sources whose subject is AI activity (LH003's subject), except where they also observe one of the layers. Each exclusion is listed with its reason.

Candidates come from three places, recorded per row: (a) instruments Lighthouse has used; (b) LH003's rows that touch a layer here; (c) a search plan fixed now, of two web searches per layer (twenty in all), each of the form "<layer> internet measurement dataset" and "<layer> public data internet-wide", with every result's title and URL written down before any is opened, opened results marked, unopened results listed as leads only. At most 45 included rows; if more qualify, the rows kept are those whose documentation states the widest population, ties to the longer history, and the rest are listed as qualified but not tabulated.

## What each row records

Name and URL; layers; what it counts (its unit, in its own words where it gives them); vantage (from where it observes: a scanner's addresses, a network's own traffic, a registry's logs); cadence; history depth; access and licence; publication date of the page read, observation window, and date read; what its documentation says it cannot see, quoted or closely paraphrased with the source; and, labelled as Lighthouse's reading, its characteristic blind spot, which may be blank. A field the pages do not fill stays blank and says so.

## The literature

Before the table is written, a bounded check of the measurement literature: at most eight searches for peer-reviewed or preprint papers that describe or evaluate instruments in the table (for example internet-wide scanning, top-list stability, certificate transparency coverage, routing data coverage), each search's results recorded with URLs, and at most twelve papers opened, read at least to their method and limits. A paper's evaluation of an instrument's coverage is cited beside that row. A search summary is a lead, not a source.

## Output

A record (studies/LH035/LH035.md, in the house form), the table (studies/LH035/sources.md), the search log, and a draft diagram of the layers with the instruments placed on them, drawn by a script kept in the study, which may later seed a map page. A piece, if the record earns one, takes AGENTS.md's full review sequence.

## Overlap

LH003's rows on GH Archive, PyPI Stats, Open Source Insights and OSV.dev touch layers 8 and 9; any such row here is re-read, not copied, and the reuse is disclosed. Instruments Lighthouse's studies have used are described here as instruments, not re-measured.

## Resource ceiling, stopping and what would leave it inconclusive

Reading only: no scan, no account, no paid service, no contact with anyone, no download of bulk data. At most about 120 page reads and twenty-eight searches. Model spend: about $20, recorded in the close-out; the survey is run by one Opus subagent, with the driving session checking a sample of rows against their pages. Stop when every candidate has a row or a reason, or at the ceiling, saying which candidates were not reached. A layer is inconclusive, not empty, if its candidates' pages could not be read; failed reads are logged with their status.
