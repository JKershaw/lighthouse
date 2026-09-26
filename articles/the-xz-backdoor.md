title: The xz backdoor: what could be seen, and by whom
kind: article
version: 0.1
date: 2026-09-26
authors: Lighthouse autopilot (Claude Code subagent), editing task E-0002
model: Opus 5.5 (claude-opus-5-5), as reported to this agent by its harness; not independently checked
grounded_at: 4ed151d
cites:
- studies/LH004/LH004.md@4ed151d (LH004, The xz backdoor, read through Lighthouse's three layers, version 0.1)
- studies/LH004/reading-list.md@4ed151d
- studies/LH004/brief.md@4ed151d
- Lighthouse_Founding_Charter.md@4ed151d (LH F01)
- Lighthouse_Research_Design.md@4ed151d (LH F02), S5, S11, S14, S15
- https://www.openwall.com/lists/oss-security/2024/03/29/4 (S14), read by LH004 2026-09-26
- https://nvd.nist.gov/vuln/detail/CVE-2024-3094 (S15), read by LH004 2026-09-26 through the NVD API
- https://tukaani.org/xz-backdoor/, read by LH004 2026-09-26
- https://research.swtch.com/xz-timeline, read by LH004 2026-09-26
- https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27, read by LH004 2026-09-26
- https://www.redhat.com/en/blog/urgent-security-alert-fedora-40-and-rawhide-users, read by LH004 2026-09-26
- https://access.redhat.com/security/cve/CVE-2024-3094, read by LH004 2026-09-26
- https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/, read by LH004 2026-09-26
- https://security-tracker.debian.org/tracker/CVE-2024-3094, read by LH004 2026-09-26

Draft awaiting the keeper's release decision under LH F03; not released.

For nearly five weeks in 2024, a backdoor sat in public inside two releases of xz-utils, a small compression library that on several Linux distributions ends up inside the ssh server. Nobody caught it by reading it. It was caught because one engineer's ssh logins had become about half a second slower, and disclosed on 29 March. The evidence was public first; the detection came from a side effect of running code. That order is why the case matters to anyone keeping watch.

Lighthouse describes such events at three layers. Activity is computation happening: builds, tests, logins. Residue is what activity leaves behind: code, release files, packages. Propagation is residue setting off activity elsewhere, as when one project's release is compiled into another's packages. LH004, the study behind this article, read the case's public record against those layers. Each event names its source; sentences giving the study's own reading say so.

## Public from the first day

Russ Cox's timeline reconstruction dates version 5.6.0 of xz-utils to 24 February 2024 and 5.6.1 to 9 March. The Tukaani project, the library's upstream home, states that these two release tarballs, created and signed by Jia Tan, contain the backdoor, and that the trigger code was never in the Git repository.

Sam James's community write-up explains the method: a build script present only in the tarball, kept out of Git by the project's ignore file, decoded a payload hidden in two openly committed test files and built it into the library. All of it was inspectable from release day, and on the record the study read, nobody's inspection caught it. In the study's reading, residue held the earliest evidence but was not where the case was found.

The releases then travelled on their own. Red Hat's security alert and Fedora Magazine's incident account report that Fedora's development branch, Rawhide, and Fedora 40's pre-release, for users with testing updates enabled, took 5.6.0 shortly after release and 5.6.1 after 9 March. Debian's unstable branch carried it too: that is where Andres Freund found it, by his own report (S14). Red Hat says no version of Red Hat Enterprise Linux was affected. In the study's reading, each build was a propagation link, a release in one place setting another's build system working, and the uptake was the ordinary cadence of rolling distributions.

Freund's report (S14), corroborated by Sam James and Red Hat, explains why a compression library mattered: several distributions patch the OpenSSH server to notify systemd when it is ready; the server then links libsystemd, which links liblzma, so compression code sits inside the process that checks keys, where the injected code could intercept authentication. In the study's reading, the library's connection to authentication, not its size, made it dangerous.

## Caught by a slow login

The first signal anyone noticed was activity. Cox's reconstruction places reports of valgrind errors, complaints from a memory-checking tool during testing, from Fedora's build and test infrastructure between about 4 and 9 March. Sam James confirms the reports came from Fedora: he later wondered whether he should have looked into why he could not reproduce them on Gentoo. The study did not check these dates against the Git history. Whoever ran those builds or received the reports could see the signal; how widely the reports circulated, the study does not say, and none of their readers recognised an attack.

The signal that broke the case came later, from one machine. Andres Freund posted to the oss-security list on 29 March that he had noticed "logins with ssh taking a lot of CPU, valgrind errors" on his Debian unstable system; an ssh connection took about 0.8 seconds where he expected about 0.3 (S14). He traced the extra time to liblzma and set out the mechanism (S14). In the study's reading, his workstation was the only observation point and his habit of measuring the only instrument, and the two signals were one phenomenon, first disbelieved, then believed.

Disclosure gave the residue a name. The National Vulnerability Database published CVE-2024-3094 the same day, with a base score of 10.0, critical (S15). Fedora Magazine records that Fedora, notified on 28 March, reverted Fedora 40 to a clean build at 04:33 UTC on 29 March and Rawhide at 15:21 UTC. In the study's reading, the spread had run for weeks, but its record, the distributions' advisories, was written only afterwards. That record also moves: Debian's security tracker, as the study read it on 26 September 2026, lists unstable as not affected, describing today's packages, not those of March 2024.

> **Illustration, described in words.** A timeline, 24 February to 30 March 2024, in three lanes. Residue: 5.6.0 on 24 February and 5.6.1 on 9 March, with a shaded band to 29 March marked "public, not caught". Propagation: Fedora taking each release, drawn in outline because the timing comes from later advisories; Debian unstable as an undated bar, since the sources give no date; the Fedora reverts on 29 March drawn solid. Activity: a hollow mark for the Fedora valgrind reports, about 4 to 9 March, and a solid one for Freund's post about his slow logins on 29 March. The reader should see that the earliest evidence sits in residue, the first detection in activity, and the account of propagation arrives last.

## What this says about watching

On the study's reading, the activity layer carried the first detected signal, twice: first as a test tool's errors in a distribution's automated builds, a standing check that fired and was not believed, visible only to those who ran the builds or read the reports; then as a slow login, visible only to the person at that machine. The residue was open to everyone and caught by no one before disclosure. Propagation ran through the distributions' package pipelines and was recorded by their own advisories, after the fact.

Neither public source Lighthouse has named for software activity and dependencies would, the study judges, have seen that spread. GH Archive (S5 in LH F02, Lighthouse's research design) would show the commits and tags on GitHub, not which distributions built them. Open Source Insights (S11) resolves dependency graphs for language ecosystems such as npm and PyPI, not the Debian and RPM packages this case travelled through. Whether any public source gathers the distributions' records together, the study leaves open. The study also finds that nothing compared a released tarball with the repository it claimed to come from, and proposes that comparison as a residue instrument, noting that tarballs built with autotools legitimately contain files absent from Git, so the difficulty is telling ordinary difference from a planted addition.

The case carries a survivor's bias. It was caught because a habitually curious engineer ran a system close enough to the release to carry it, and the slowdown was large enough to feel. A smaller slowdown, or a target further from technically curious users, plausibly would not have been caught, and the study cannot say how many such cases have passed unseen, nor, from any source it read, how many machines ran a compromised build. In the study's reading, what made this one visible was an effect of running code, noticed where very few could see it.

## Sources

Each web source was read by LH004 on 26 September 2026. S numbers refer to the source list in Lighthouse's research design (LH F02).

- LH004, The xz backdoor, read through Lighthouse's three layers, version 0.1, 26 September 2026: studies/LH004/LH004.md, reading-list.md and brief.md.
- Andres Freund, post to the oss-security list, 29 March 2024 (S14): https://www.openwall.com/lists/oss-security/2024/03/29/4
- National Vulnerability Database, CVE-2024-3094 (S15): https://nvd.nist.gov/vuln/detail/CVE-2024-3094 (read through the NVD API, as the page did not render)
- Tukaani project, its account of the backdoor: https://tukaani.org/xz-backdoor/
- Russ Cox, Timeline of the xz open source attack: https://research.swtch.com/xz-timeline
- Sam James, xz-utils backdoor situation: https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27
- Red Hat, Urgent security alert for Fedora 40 and Rawhide users: https://www.redhat.com/en/blog/urgent-security-alert-fedora-40-and-rawhide-users
- Red Hat, CVE-2024-3094 page: https://access.redhat.com/security/cve/CVE-2024-3094
- Fedora Magazine, CVE-2024-3094: Urgent alert for Fedora Linux 40 and Rawhide users: https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/
- Debian Security Tracker, CVE-2024-3094: https://security-tracker.debian.org/tracker/CVE-2024-3094
- Lighthouse Founding Charter (LH F01) and Research Design (LH F02), for the layer definitions and for what GH Archive (S5) and Open Source Insights (S11) cover; neither of those two was read for this case.
