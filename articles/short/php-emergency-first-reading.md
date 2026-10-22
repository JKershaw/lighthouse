published: 2026-10-22
summary: Amazon reports a pre-disclosure PHP exploit attempt against a honeypot. The early response has left visible traces in protection rules and published images, but not a count of affected or fixed sites.
status: released
investigation: software-updates

# The PHP patch was public on Wednesday; one reported attack trace is older

Amazon says one of its decoy servers received a PHP exploit attempt dated 17 October, four days before the vulnerabilities were disclosed and patched. It published the account on 21 October and does not know how the sender learned of the flaws or whether the attempt would have worked on a real site.

*22 October 2026 · Lighthouse*

This emergency has left unusually many public traces. OpenAI says a researcher used AI in finding a flaw and describes a coordinated response led by PHP's maintainers. Cloudflare says it put web firewall protection on by default for customers using its WAF before the public release and later saw attack traffic. By our first reads, selected official PHP images and five selected WordPress, Drupal and Nextcloud image tags held configurations declaring fixed PHP versions; one Drupal image shared every filesystem layer digest of a selected fixed PHP base before adding its own layers.

Each trace stops somewhere. The honeypot saw attempts, not confirmed intrusions. The AI account documents defensive discovery, not an attacker's tooling. A published image is available, but it does not tell us how many servers pulled or ran it. And Amazon's article was available to our web reader while its direct endpoint gave our archival collector a placeholder. We are recording the fixed sources again over the first days, with their access gaps intact.

[Read the developing account](../php-emergency-first-reading.md) and [its evidence](../../studies/LH028/LH028.md).
