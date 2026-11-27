published: 2026-11-27
summary: Anthropic said on 27 October 2026 that its model wrote an exploit for a serious Linux kernel flaw. The kernel's fix was in stable releases 12 to 16 days before that, but no public source we read in November says when the flaw was reported.
status: draft
investigation: model-found-bugs

# When was the Linux flaw in Anthropic's exploit post reported?

On 27 October 2026, Anthropic said that, after initial prompting, its model had written an exploit for a Linux kernel flaw that, it says, lets a remote attacker run commands as root on servers with a multipath TCP listener. What happened first? A disclosure note: the post is Anthropic's, and this was written on an Anthropic model.

Most of the dates are public. The fix's author date is 1 October. It was in stable kernel releases on 11 and 15 October, and the flaw's record was published on 15 October. So the fix was out 12 to 16 days before the post.

The first date isn't. No public source we read says when the flaw was reported. The kernel's fix credits a reporter without a date, and the post says only that Anthropic reported each flaw "to the affected vendor". Unknown here doesn't mean late, early or absent.

Anthropic's policy page says it generally waits 45 days after a patch before "publishing full technical details". The post, in prose without code when we read it on 17 November, came inside every 45-day window we could count. But neither text defines the details that wait covers, and the page allows it to be shortened. Those are dates beside a policy, not a verdict.

The main limit: it's one flaw, and what was said in private isn't in any public source we read.

[The full piece](../model-found-flaw-dates.md)

*27 November 2026 · Lighthouse · Draft, version 0.2, evidence review done with fixes applied, reader review pending, not released. Written by a Claude Code subagent on Claude Opus 5.5, made by Anthropic.*
