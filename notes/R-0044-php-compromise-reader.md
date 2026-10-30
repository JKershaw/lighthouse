title: R-0044, reader-and-inference review of the PHP account, version 1.3
kind: review note
date: 2026-10-30

# R-0044, reader-and-inference review of the PHP account, version 1.3

## What a reader would believe, written before reading the record

Said back: the PHP flaws fixed on 21 October have now been used to break into real machines. Palo Alto Networks says attackers exploited them through exposed firewall management pages, and confirmed a security firm's count of 25 servers taken over to root, three in a US government-affiliated network. An AI coding tool, Claude Code, sat on the attacker's machines, with no direct evidence it wrote the exploit.

Observed by Lighthouse: pages saying these things, read on 30 October; CISA's listings; Delft's counts; images holding the fix. Reported by others: the exploitation, the 25 servers, the 35 decoy shells. Explained: the PHP flaws chained with a kernel flaw gave root; CISA's kernel entry seems to confirm that chain. Caused: a reader takes the PHP flaws as the cause of real intrusions, and is nudged towards AI having helped. Claude Code is named twice and "AI-assisted development" quoted, while Unit 42's retracted agentic-AI claim appears only in the dated list.

Limits a reader would notice: the evidence is the companies' own and unchecked; decoys are not intrusions; Delft's "code execution" step is undefined. Harder to notice, or confusing: the compromised systems are firewalls with PHP inside (8.0.30, by Dream), not the websites and images the piece follows, which the front page and summary barely say; "0.02 per cent ... impacted" cannot be squared with 25 servers; "may still rest on attempts" reads oddly beside a vendor's report of real exploitation; and the title still ends at "published fixes".
