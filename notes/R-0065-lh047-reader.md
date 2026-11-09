# R-0065: LH047 reader and inference review

## What a reader would believe, written before reading the record

**Principal finding, said back.** Websites ask bots to behave in many ways, but almost nothing enforces those asks. Outside measurements of how well AI crawlers obey disagree, partly because some AI companies (OpenAI, Google, Perplexity) say robots.txt does not cover fetches a user asks for, while Anthropic says its bots honour it. When Lighthouse checked itself over about an hour and a half on 8 November 2026, roughly one request in twenty (172 of about 3,500) broke a rule, far more than the 2 it knew of. Most were reads of PyPI's JSON interface, which PyPI both documents for programs and asks crawlers to avoid, and one reviewer's requests under an anonymous name. Since 9 November every collector checks robots.txt first.

**Observed, explained, caused.** Observed: the request counts, the breakdown, and what the operators' pages say. Explained: the disagreement between published figures is put down to counting different things and to the user-fetch exemption (labelled interpretation). Caused: the faults are attributed to collectors and agents that never read robots.txt; a reader would take the fix as having stopped them.

**Limits a reader would notice.** It is one short evening, a floor, and Lighthouse grading itself. "As our brief fixed it" signals the rule is Lighthouse's own reading, and a second rule gives 191. The page's note that 184 verdicts rest on robots.txt files re-read afterwards is easy to miss and would surprise a reader. A reader might still take "broke a rule" as harm done to sites, and might read the Anthropic contrast as a verdict that Anthropic behaves better, which nothing here measures.
