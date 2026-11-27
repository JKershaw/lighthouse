published: 2026-11-27
summary: Anthropic said on 27 October 2026 that its model wrote an exploit for a serious Linux kernel flaw. The kernel's fix was in stable releases 12 to 16 days before that, every distribution announcement we could date came after it, and no public source we read in November says when the flaw was reported.
status: draft
investigation: model-found-bugs

# When was the Linux flaw in Anthropic's exploit post reported?

On 27 October 2026, Anthropic said that, after initial prompting, its model had written an exploit for a Linux kernel flaw that, it says, lets a remote attacker run commands as root on servers with a multipath TCP listener. What happened first? A disclosure note: the post is Anthropic's, and this was written on an Anthropic model.

Most dates are public. The fix's author date is 1 October; it was in stable kernel releases on 11 and 15 October, and the flaw's record was published on 15 October, 12 to 16 days before the post. The distributions' announcements we could date, from SUSE, Red Hat and Ubuntu's tracker, came 2 to 14 days after it.

The first date isn't. No source we read says when the flaw was reported; the fix credits a reporter without a date. Unknown here doesn't mean late, early or absent.

Anthropic's policy page says it generally waits 45 days after a patch before "publishing full technical details", so that "downstream users" have "time to deploy the fix". The post, prose without code as read on 17 November, came within 45 days of the kernel's fixes, but before any distribution announcement we could date; the policy doesn't say which patch starts the wait. Neither text defines the details it covers, and the page allows it to be shortened or extended. Those are dates beside a policy, not a verdict either way.

The main limit: it's one flaw, and private exchanges aren't in any public source.

[The full piece](../model-found-flaw-dates.md)

*27 November 2026 · Lighthouse · Draft, version 0.3, evidence review and reader review done with fixes applied, recheck pending, not released. Written by a Claude Code subagent on Claude Opus 5.5, made by Anthropic.*
