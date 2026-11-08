# LH046 search log (sources read before the brief)

All reads 8 November 2026, UTC, by the research subagent (Claude, Opus 5.5), with the User-Agent `Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)`. Bodies, HTTP status and sha256 of the bytes received are in data/sources/ and data/sources/fetch-log.tsv; text conversions (`python3 -I ../LH043/scripts/html2txt.py in.html out.txt`) sit beside them. None of these reads touches a GH Archive file; they are documentation, status and changelog pages.

## Read

- **gharchive.org home page** (19:33:48, 200, 19,366 bytes, sha256 566652fb..., the same bytes LH035 read on 6 November). Says GH Archive records "the public GitHub timeline", "15+ event types", "aggregated into hourly archives"; archives from 1/1/2015 are "recorded from the Events API"; the payload "may be updated by GitHub at any point". No status notice, no statement of completeness, no note of any gap or change in 2026.
- **robots.txt** of www.gharchive.org and data.gharchive.org (identical, 1,248 bytes): content-signal definitions only, with no Disallow line and no content-signal value set.
- **GH Archive's repository README** via raw.githubusercontent.com (200): licence notes only; no status.
- **GitHub REST docs, "REST API endpoints for events"** (200). States for "List public events": "This API is not built to serve real-time use cases. Depending on the time of day, event latency can be anywhere from 30s to 6h." Timeline endpoints hold up to 300 events and 30 days. No notice of a change in October or November 2026.
- **GitHub REST docs, "GitHub event types"** (200). PushEvent and CreateEvent are still documented; the PushEvent payload is `repository_id`, `push_id`, `ref`, `head`, `before` (no commit list); CreateEvent has `ref`, `ref_type` (branch, tag or repository), `full_ref`, `master_branch`, `description`, `pusher_type`. No deprecation notice.
- **GitHub REST docs, breaking changes** (for version 2022-11-28, as requested): no Events entry. The page for version 2026-03-10 was not requested.
- **GitHub changelog**: front page, feed (10 items, 4 to 7 November), and the month pages for September, October and November 2026 (October's runs from 1 to 31 October, 118 entries). Searched the text for "event", "push", "timeline", "feed", "API". Nothing about the Events API or public activity events in any of the three months. Two October entries mention pushes and were read in full:
  - 15 October 2026, "Email notifications for repository push events have been retired": email notifications for pushes stopped "to help prevent spam and abuse". It says nothing about the Events API. The date coincides with the first day of the scan's lead; nothing in the entry links the two, and this record does not.
  - 12 October 2026, "Push attribution for commits in limited public preview": a durable pusher identity on commits, for Enterprise preview customers. Nothing about the Events API.
- **GitHub changelog, 8 August 2025, "Upcoming changes to GitHub Events API payloads"** (read because LH002 found PushEvent payloads without commit lists): push events lose "commit summaries and counts", pull request events lose slow fields, `author_association` is removed from several types; brownout 8 September 2025, change on 7 October 2025; events "could take up to eight hours to appear" before, "almost immediately" after. This explains the payload LH002 saw; it is a year before the window and says nothing of event types disappearing.
- **githubstatus.com incidents API** (`/api/v2/incidents.json`, the last 50 incidents, 31 August to 8 November 2026). No incident names the Events API, the public event timeline or GH Archive. Incidents that mention events: 7 October (write operations failed 15:06 to 15:16 and 16:52 to 17:01 UTC, outside the 12:00 hour); 19, 21 and 22 October (the event streaming platform degraded; on 22 October, 13:05 to 15:20 UTC, "repository push events (12m)" were delayed, which GitHub describes as an internal delay, not the public API); 4 November (events that trigger Actions). These are dated so the results can be set beside them; none is evidence of a cause.

## Unread

- GH Archive's issue tracker (github.com/igrigorik/gharchive.org/issues): HTTP 403 from this session's proxy, which says the repository is not enabled for the session; the GitHub API answered the same, and the GitHub tool refused it. Not read; any report there of missing events is unknown to this study.
- githubstatus.com/history renders its list with JavaScript; the incidents API above was read instead.
- The changelog's own search (`?s=events+api`) returned the front page; the month pages were read instead.

## Web searches (leads, not sources)

- "GH Archive missing PushEvent October 2026" (about 19:37): links to a Hugging Face mirror (open-index/open-github) and skill pages; the summary said nothing about October 2026. Not opened.
- "GitHub Events API push events not appearing public events October 2026" (about 19:38): GitHub docs pages and a community discussion about delayed organisation feeds (community/discussions/168149, through a mirror domain); nothing dated October 2026. Not opened.
