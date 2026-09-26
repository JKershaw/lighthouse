# LH004 annotated reading list

Every source used in `LH004.md`, in the order it first appears there. Each entry gives what the source is, why it was used, the URL (or S number where Lighthouse_Research_Design.md already assigns one), and the date it was read. Two attempted sources that failed are listed at the end, per Method's account of them.

### S14 Andres Freund's oss-security disclosure

The primary first-hand account of discovery: an engineer's own description of noticing ssh logins taking unusual CPU and running more slowly, tracing this to `liblzma`, and setting out the backdoor's technical mechanism (build-time injection, hijacked `crc32_resolve`/`crc64_resolve`, a redirected `RSA_public_decrypt`). This is the primary source for the activity-layer detection in LH004, as Lighthouse_Research_Design.md already states.

https://www.openwall.com/lists/oss-security/2024/03/29/4, read 2026-09-26.

### S15 CVE-2024-3094 (NVD)

The canonical vulnerability record: description, published date (29 March 2024) and CVSS base score (10.0, critical). Used to date the public disclosure and its assessed severity. The NVD web page itself returned no usable content to the fetch tool used here (it needs scripts to render, a caveat Lighthouse_Research_Design.md already records against this source); the NVD REST API endpoint at `services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-3094` was read instead and gave the same description, dates, CVSS vector and a reference list.

https://nvd.nist.gov/vuln/detail/CVE-2024-3094, read 2026-09-26 (page did not render; API read as a substitute, same date).

### Tukaani project's own account

The upstream maintainer's (Lasse Collin's) own statement of what happened: that the 5.6.0 and 5.6.1 release tarballs, created and signed by Jia Tan, contained the backdoor; that the trigger code was never in the git repository; and an account of what access Jia Tan actually held. Used as the closest thing to a primary source on the project side, distinct from Freund's discovery-side account.

https://tukaani.org/xz-backdoor/, read 2026-09-26.

### Russ Cox, "Timeline of the xz open source attack"

The timeline reconstruction used throughout LH004 for the multi-year social-engineering campaign (first contact in October 2021 through the pressure campaign of 2022 and the handover of maintainership) and for the early-March 2024 valgrind reports that preceded Freund's disclosure by about three weeks. Widely cited and detailed enough to date individual commits; this study did not independently verify its dates against the live git history, and says so in Limits.

https://research.swtch.com/xz-timeline, read 2026-09-26.

### thesamesam (Sam James), "xz-utils backdoor situation" gist

A comprehensive, community-maintained technical write-up, including the specific mechanism by which the malicious `build-to-host.m4` script, present only in the release tarball and excluded from git via `.gitignore`, decoded a payload hidden in two committed test files. Also the source, in the author's own reflective aside, confirming that valgrind problems had been reported from Fedora before the disclosure, and that they went uninvestigated at the time.

https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27, read 2026-09-26 (page states it was last updated 2026-09-09).

### Red Hat, "Urgent security alert for Fedora 40 and Rawhide users"

A vendor advisory, used for Red Hat's own affected-versions statement (Fedora 40 and Rawhide; no RHEL version affected) and its recommended remediation, and for the alert's own publication and update dates (29 and 30 March 2024).

https://www.redhat.com/en/blog/urgent-security-alert-fedora-40-and-rawhide-users, read 2026-09-26.

### Red Hat, CVE-2024-3094 vendor page

Used to confirm the CVSS vector string and Red Hat's affected-products statement in a second, independent Red Hat page from the advisory blog above.

https://access.redhat.com/security/cve/CVE-2024-3094, read 2026-09-26.

### Fedora Magazine, "CVE-2024-3094: Urgent alert for Fedora Linux 40 and Rawhide users"

Fedora's own incident account, with the most precise timestamps found in any source used here: notification on 28 March 2024, Fedora Council informed 29 March, Fedora 40 reverted to a clean build at 04:33:13 UTC on 29 March, and Rawhide reverted at 15:21:19 UTC the same day. Also confirms Fedora 38 and 39 were never affected.

https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/, read 2026-09-26.

### Debian Security Tracker, CVE-2024-3094

Debian's own tracked status for this CVE. Read for the fixed-version table, but its "not affected" statements for buster, bullseye, bookworm and unstable reflect the tracker's state as read today, not the state on 29 March 2024, when unstable and testing did carry the compromised package. LH004's Limits section explains this distinction and relies on the contemporaneous vendor and press sources above, not this tracker, for the March 2024 position.

https://security-tracker.debian.org/tracker/CVE-2024-3094, read 2026-09-26.

## Named but not separately read for this essay

**S16 (Log4Shell)** and **S17 (the left-pad removal)**, both already sourced in Lighthouse_Research_Design.md, are the two alternative propagation cases Lighthouse_Initial_Research_Programme.md names for this ticket. LH F04 states xz as the first choice; this study followed that choice and did not fetch fresh material on either alternative.

## Fetches attempted and not usable

**Ars Technica's report on the disclosure** could not be fetched at all from this container: the fetch tool returned "Claude Code is unable to fetch from arstechnica.com." Not cited anywhere in the essay.

https://arstechnica.com/security/2024/03/backdoor-found-in-widely-used-linux-utility-breaks-encrypted-ssh-connections/, attempted 2026-09-26, fetch failed.

**An initial guess at Red Hat's advisory URL** returned HTTP 404 before the correct URL (naming Fedora 40, not 41) was found by search. Listed here for completeness; the working URL is cited above and is the one relied on.

https://www.redhat.com/en/blog/urgent-security-alert-fedora-41-and-fedora-rawhide-users, attempted 2026-09-26, HTTP 404.
