# LH018 sources and boundaries

All pages and responses below were read 21 October 2026, UTC. Exact response timestamps and SHA-256 hashes are in `data/snapshot-2026-10-21/read_log.csv`; raw bodies are retained beside it. The source's publication time and the collection time are separate fields. No source below observes a running PHP deployment.

| Source | URL | What it says or records, and the edge |
| --- | --- | --- |
| PHP project's 21 October advisory | https://www.php.net/archive/2026.php | Four fixed upstream versions for CVE-2026-109618 and CVE-2026-109619; release date, not exact first-availability time. Read before protocol. |
| PHP Foundation's 21 October account | https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/ | Coordinated release narrative, prior knowledge of Chainguard's image; full primary page read again at 16:51:59 UTC. Attribution to the Foundation, not an independent test of its claims. |
| Debian security tracker | https://security-tracker.debian.org/tracker/CVE-2026-109618 and https://security-tracker.debian.org/tracker/CVE-2026-109619 | Fixed and vulnerable package revisions by source and suite. Status current at retrieval; no initial-fix hour. |
| Debian LTS advisory DLA-4848-1 | https://www.debian.org/lts/security/dla-4848-1 | Bookworm `php8.2` advisory dated 21 October. |
| Debian security advisory DSA-6574-1 | https://www.debian.org/security/dsa-6574-1 | Trixie `php8.4` advisory dated 21 October. |
| Ubuntu CVE API | https://ubuntu.com/security/cves/CVE-2026-109618.json and https://ubuntu.com/security/cves/CVE-2026-109619.json | `php8.3` noble security-pocket status and revision; embedded USN record with recorded publish timestamp. The CVE documents have their own `published` and `updated_at`, which are not package publication times. |
| Ubuntu USN-8948-1 | https://ubuntu.com/security/notices/USN-8948-1 | Human-facing vendor notice dated 21 October; its JSON embedded in the two CVE records supplies 13:56:19 UTC. |
| Docker Hub tag API | https://hub.docker.com/v2/namespaces/library/repositories/php/tags/8.5.12-apache and the same path with `8.4.27-fpm`, `8.3.36-cli`, `8.2.35-fpm` | Current tags and per-platform digest/push metadata at retrieval. Documentation https://docs.docker.com/reference/api/hub/latest/operations/GetRepositoryTag/ was read before protocol. A tag is a movable pointer. |
| OCI registry | `https://registry-1.docker.io/v2/library/php/manifests/<linux-amd64 digest>` and `/blobs/<configuration digest>` for the four selected tags; exact URLs in the read log | The saved manifest identifies a config; the config declares a PHP_VERSION and PHP_URL and includes build history. It is a builder's representation of an image, not an inspection of a running binary. Prior source assessment: studies/LH006/sources.md and studies/LH007/sources.md. Anonymous bearer responses were discarded. |
| Ubuntu OSV documentation | https://documentation.ubuntu.com/security/security-updates/osv/ | Read before protocol for vendor status and backport interpretation; published date not displayed in the passage used. The Ubuntu security API docs at https://ubuntu.com/security/api/docs timed out and were not cited as read. |

The four-query bounded discovery on 21 October also returned search leads about Debian, Ubuntu, Alpine and Docker; only the primary documentation explicitly listed above was opened before collection. No Alpine outcome was inspected. No literature estimate was used as evidence for a result here.
