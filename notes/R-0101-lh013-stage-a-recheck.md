# R-0101: recheck of what the R-0097 and R-0099 resolutions wrote into LH013 0.3 (Stage A)

**In short.** The driving session changed the Stage A section of LH013's record, programme.md's LH013 paragraph and proposals.md's P-0002 line to answer an evidence review and a reader review. I read each changed sentence once against the evidence it rests on. The figures, the claim about linehaul and the three surfaces' agreement all hold. One label is wrong: it says two sentences of the interpretation are the brief's, fixed before the read, when one of them now carries a caveat added after the count. Two summary sentences also state more surely than the record's own limits allow. Exact replacements are below.

**Who.** A fresh rechecker, Claude Code on Opus 5.5 (claude-opus-5-5, as the harness reports, not independently checked), dispatched for schedule row LH013-installer-A-record-recheck. I wrote nothing that I checked and did not take part in either review. This is one reading, not a chain. Offline only: no network request, no ClickPy query, no key read, nothing committed.

**Version read.** Repository HEAD 0e1a0b8 (19 November 2026); the changes are `git diff ff2bcfc 0e1a0b8 -- studies/LH013/LH013.md programme.md proposals.md` (commits 56d33a4 and 7d6bcbd).

## What I checked

- Every changed sentence in LH013.md (In short; Stage A's opening, A1, the class paragraph, What it means, Limits of Stage A; Limits, "Unknown stays unknown"; the dated note under Next; Corrections 0.3), programme.md's LH013 paragraph and P-0002's 2026-11-19 line.
- Against: studies/LH013/installer-brief.md (questions, sources section lines 33 to 56, Stage A measures and class rule, ceiling, stopping condition, inconclusive cases); data/installer/stage_a_A1.csv and stage_a_A2.csv; the last two rows of data/read_log.csv; data/docs/linehaul_parser.py.txt (whole, 231 lines); data/installer-brief-docs/clickpy_README.md (the import at line 343) and clickpy_pypi_columns.tsv; amendments.md ("The pip date"); studies/LH012/LH012.md (Findings, walk interpretation, Method, Corrections 0.4) and LH012's file pass (scripts/collect.py lines 154 to 157, data/week/files/); notes/R-0097 and notes/R-0099 with their resolutions.
- Figures, recounted by eye from the CSVs: 20 groups; 15 non-blank installer names (pip, uv, poetry, Nexus, Bazel, requests, Browser, bandersnatch, devpi, setuptools, pdm, Homebrew, OS, pex, Artifactory) and blank; 0 metadata rows in every group; Python 3.9 rows pip 41,737,447, uv 39,806, setuptools 370, blank 49; A2 79,782,285. Read log: 14:28:30 and 14:28:33 UTC, HTTP 200, rows returned 20 and 1, rows read 80,199,680 and 89,958 (sum 80,289,638). All match the record.
- Writing: no em or en dashes in any changed line; British spelling throughout; header unchanged and still consistent with 0.3.

## Findings

### Must-fix

**1. "What it means" mislabels a post-count caveat as the brief's.** The label reads "(interpretation: the first two sentences are the brief's, fixed before the read; ...)". The brief's own sentences (installer-brief.md, Stage A result class) end "That is strong evidence that the download table carries none, but not proof: ClickPy's filter could in principle drop them." The record's second sentence now adds "attributed to boto3" and the clause "a request logged without boto3's project name would not be counted here (linehaul takes the project from the log line, not the file name, and rejects a line that has none)", both written after the count, from R-0099. The caveat narrows the claim, so nothing is inflated, but a reader is told it was fixed before the read. Replace:

> **What it means** (interpretation: the first two sentences are the brief's, fixed before the read; the rest draws out what the brief says this decides).

with:

> **What it means** (interpretation: the first two sentences restate the brief's, fixed before the read, except that the caveat about boto3's project name was added after the count, by the reader review; the rest draws out what the brief says this decides).

### Should-fix

**2. "Whatever happens to such requests, none shapes boto3's counts" is surer than the record's own limits.** The record's Limits of Stage A say an empty file-name column on D would also give no metadata rows and is "unlikely, not excluded". If the column were empty, metadata rows could sit in boto3's per-version counts. So the In short and programme.md state as certain what the record holds as very likely.

In LH013.md's In short, replace:

> in the public copy of the log, so whatever happens to such requests, none shapes boto3's counts by version;

with:

> in a public copy of the log, so such requests almost certainly don't shape boto3's counts by version;

("a public copy": the package index's BigQuery table is itself public, and ClickPy is one copy of it.)

In programme.md's LH013 paragraph, replace:

> class absent: so no metadata-file row shapes boto3's counts by version; strong evidence, not proof, that the log carries none,

with:

> class absent: so metadata-file rows almost certainly do not shape boto3's counts by version (an empty file-name column, unlikely, is not excluded); strong evidence, not proof, that the log carries none for boto3,

**3. programme.md is broader than the record on the log as a whole.** The record grants "strong evidence, not proof" only for "none attributed to boto3" ("What it means") or "none for boto3", with "likely none at all" ("Unknown stays unknown"); programme.md's "strong evidence, not proof, that the log carries none" reads as the log-wide claim at the stronger certainty. The replacement in finding 2 adds "for boto3", which resolves it. If finding 2 is not taken, make only that change: "strong evidence, not proof, that the log carries none for boto3,".

**4. The dated note under Next puts a third query "within Stage A's ceiling", but Stage A has closed.** The brief's stopping condition: "Stage A closes when A1 and A2 are read". The ceiling of five queries is spare, but a third query would reopen a closed stage by amendment, which the note should say. Replace:

> it would be a dated amendment, labelled post hoc, within Stage A's ceiling of five queries (two used).

with:

> it would be a dated amendment, labelled post hoc, reopening Stage A, which closed when A1 and A2 were read, and kept within its ceiling of five queries (two used).

**5. Corrections 0.3 omits the note it added under Next.** Append, after "and the limits add the unchecked file-name column.":

> Next now notes the reader review's suggested firming query, not run.

### Fine

- **linehaul.** The parser text supports both halves. For a download line, `data["project"] = parsed["project_name"]` and `data["file"]["version"] = parsed.get("version")` take project and version from the log line's fields, while only the file name comes from the URL (`posixpath.basename(url)`). A `(null)` project becomes None (the `_nullable` groups); `Download.project` and `File.project` carry `instance_of(str)` validators, and the file's comment says a malformed line "should just raise so the caller can shunt it to the unprocessed/ bucket"; an empty field cannot match `_WORD` and raises `UnparseableEvent`. That a None reaches the validator unconverted depends on how cattrs treats untyped attrs fields, which is library behaviour not in the retained text, and the parser was read, not run; "rejects" is a fair reading of it. "Simple" lines take the project from the URL, but they go to a different table, so this doesn't touch the claim.
- **Pip 23.2 and "where offered"** agree with amendments.md, the installer brief (Sources and installer classes) and LH012's Findings and Corrections 0.4.
- **The file-name column limit.** ClickPy's README import (line 343) selects no file name, while the live schema has a `filename` column; LH012's file pass parsed wheel tags from real file names in September 2026 (collect.py lines 154 to 157; data/week/files/, ten libraries, boto3 not among them). "Unlikely, not excluded" is the right certainty.
- **P-0002's line** ("no free public source the brief read carries ... pepy.tech and other mirrors were not checked") matches installer-brief.md lines 33 and 40.
- **Consistency.** With findings 2 and 3 taken, the record, programme.md and P-0002 agree on the day, the class, the boto3-only certainty, the unreviewed label and Stage B waiting on an account. The In short, header and Next agree.
- **Corrections 0.3's account of R-0097**: one wrong count and five wording points, all taken. That's accurate. R-0097's point 2 wording was later replaced by R-0099's, and the entry's summary covers both.
- **In short readability.** It reads plainly, though its last sentence still carries three ideas (R-0099's readability point 2, not taken); splitting off "the main installer read still waits for an account" would help, at the writer's discretion.

Verdict: not cleared (must-fix: the label on "What it means" says the second sentence is the brief's, fixed before the read, though its boto3 project-name caveat was added after the count; the exact replacement in finding 1 resolves it, and findings 2 to 5 are at the writer's discretion).

## Applied by the driving session, 19 November 2026

The must-fix and all four should-fix replacements were applied as written. As AGENTS.md step 4 says, these changes are listed here and not sent to another reader.
