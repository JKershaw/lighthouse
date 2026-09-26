# LH002 cohort

The ten repositories as fixed in brief.md before collection, with what each source returned for each. Every figure here is from a table in data/, read on 26 September 2026; the window is 2026-03-26T00:00:00Z to 2026-04-22T23:59:59Z. No repository was added, dropped or replaced after the brief was written. Contributor identities appear only as counts and classes; the pseudonymous per-author table is data/authors_pseudonymous.csv.

## Membership and selection

| id | repository | PyPI package | how it entered | first commit in git | first PyPI release |
| --- | --- | --- | --- | --- | --- |
| R00 | https://github.com/modelcontextprotocol/python-sdk | mcp | the library | 2024-09-24 | 2024-11-20 |
| R01 | https://github.com/saigontechnology/agentcrew | agentcrew-ai | frame A, hash order 1 | 2025-02-18 | 2025-06-23 |
| R02 | https://github.com/robertwhiffin/ai-slide-generator | databricks-tellr-app | frame A, hash order 2 | 2025-11-05 | 2026-01-19 |
| R03 | https://github.com/ooo0ooo/lean-lsp-mcp | lean-lsp-mcp | frame A, hash order 3 | 2025-03-29 | 2025-03-31 |
| R04 | https://github.com/paulieb89/pyp6xer-mcp | pyp6xer-mcp | frame A, hash order 4 | 2026-04-04 | 2025-12-08 |
| R05 | https://github.com/oraios/serena | serena-agent | frame A, hash order 5 | 2025-03-23 | 2025-07-21 |
| R06 | https://github.com/eddmpython/dartlab | dartlab | frame A, hash order 6 | 2026-03-06 | 2026-03-06 |
| R07 | https://github.com/mistralai/mistral-vibe | mistral-vibe | frame A, hash order 7 | 2025-12-09 | 2025-11-17 |
| R08 | https://github.com/drakkar-software/octobot | octobot | frame B, oldest first release | 2018-02-23 | 2019-01-16 |
| R09 | https://github.com/jesse-ai/jesse | jesse | frame B, second oldest | 2020-04-07 | 2020-04-06 |

Frame A is the 34 direct dependents of `mcp` 1.27.0 that Open Source Insights lists; frame B the 95 of `mcp` 1.26.0. The rule and the counts excluded at each step are in brief.md; the script is scripts/select_cohort.py and its full output, with every excluded package and the reason, is reproduced by running it.

**Inclusion notes.** Fork status could not be read: GitHub's REST API answered 403 through this session's proxy, and the proxy's rule is to report such a refusal, not route around it. Every repository here is the one its package's own metadata names, so none was chosen as a fork, but none is confirmed not to be one. R04's GitHub history begins on 2026-04-04 with a single commit holding the whole project, and its PyPI release of 2026-03-26 names a GitLab repository as its source (Open Source Insights, UNVERIFIED_METADATA); the nine days before are missing, not zero. R07's first commit in git, on 2025-12-09, is later than its first PyPI release, on 2025-11-17, so its earlier history is not on GitHub either; that falls before the window and does not affect its readings. No paths matched the vendored-content rule. Lockfiles are counted apart from other lines. R06's changed lines are 91 per cent JSON files (data/changed_lines_by_location.csv), which the tables keep visible rather than exclude.

## Readings over the window

| id | observed days | active days | commits | per observed day | bot / human account / unknown commits | PyPI releases | git tags | `mcp` in git at start | at end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R00 | 28 | 13 | 95 | 3.39 | 2 / 79 / 14 | 1 | 0 | (the library) | (the library) |
| R01 | 28 | 20 | 97 | 3.46 | 0 / 0 / 97 | 17 | 17 | >=1.24.0, lock 1.25.0 | >=1.24.0, lock 1.26.0 |
| R02 | 28 | 13 | 210 | 7.50 | 0 / 23 / 187 | 0 | 0 | none | >=1.0.0, lock 1.27.0 |
| R03 | 28 | 3 | 26 | 0.93 | 0 / 0 / 26 | 2 | 2 | ==1.26.0, lock 1.26.0 | ==1.27.0, lock 1.27.0 |
| R04 | 19 | 5 | 13 | 0.68 | 0 / 0 / 13 | 1 | 0 | no history | ==1.27.0, lock 1.27.0 |
| R05 | 28 | 28 | 435 | 15.54 | 9 / 42 / 384 | 4 | 4 | ==1.26.0, lock 1.26.0 | ==1.26.0, lock 1.26.0 |
| R06 | 28 | 28 | 1,482 | 52.93 | 1 / 1,481 / 0 | 35 | 50 | >=1.0, lock 1.26.0 | >=1.0, lock 1.27.0 |
| R07 | 28 | 8 | 9 | 0.32 | 0 / 0 / 9 | 9 | 9 | >=1.14.0, lock 1.26.0 | >=1.14.0, lock 1.26.0 |
| R08 | 28 | 16 | 124 | 4.43 | 1 / 0 / 123 | 1 | 1 | ==1.26.0 (nested file) | ==1.26.0 (nested file) |
| R09 | 28 | 9 | 17 | 0.61 | 0 / 0 / 17 | 4 | 0 | none | none |

Sources: data/repo_summary.csv, data/pypi_releases_in_window.csv, data/tags_in_window.csv and data/mcp_state_window_start_end.csv. "Human account" means an author address at GitHub's noreply domain with no bot marker; "unknown" is every other author without a bot marker, which includes people who commit under a personal or work address. R00's release tag is not counted as a window tag because it is a lightweight tag and git gives it the date of its commit, 24 March.

## Coverage by source

| id | git over HTTPS | Open Source Insights graph for the window-end version | Software Heritage GitHub origin | GH Archive, 2 April 14:00 UTC |
| --- | --- | --- | --- | --- |
| R00 | complete | resolved | archived, window-end head present | 0 events |
| R01 | complete | resolved | not archived | 0 events |
| R02 | complete | resolved, no `mcp` in that version | not archived | 2 events |
| R03 | complete | resolved | not archived | 0 events |
| R04 | from 4 April | resolved | not archived | 0 events |
| R05 | complete for surviving branches | resolved | archived, window-end head present | 2 events |
| R06 | complete | resolved | not archived | 0 events |
| R07 | complete | resolved | archived, window-end head present | 0 events |
| R08 | complete | resolved | archived, window-end head present | 0 events |
| R09 | complete | failed: the service reports a parse error in a requirement marker | archived, window-end head present | 0 events |

"Complete" means every commit reachable in September 2026 from a branch or tag; commits on branches deleted since are not in it (see LH002.md, Findings). Sources: data/software_heritage_coverage.json, data/depsdev_graphs_window_start_end.csv, data/gharchive_hour_vs_git.csv.
