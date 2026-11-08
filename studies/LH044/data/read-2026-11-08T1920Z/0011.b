# Our policy
#
# Allowed:
# - Search engine indexers
# - Archival services (e.g. IA)
#
# Disallowed:
# - Marketing or SEO crawlers
# - Anything used to feed a machine learning model
# - Bots which are too agressive by default. This is subjective, if you annoy
#   our sysadmins you'll be blocked.
#
# If you do not respect robots.txt or you deliberately circumvent it we will
# block your subnets and leave a bag of flaming dog shit on your mother's front
# porch.
#
# Reach out to ~sircmpwn/[email withheld by Lighthouse] if you have questions.

# It doesn't make sense to index these and/or it's expensive:
User-agent: *
Disallow: /*?*
Disallow: /*.tar.gz$
Disallow: /metrics
Disallow: /*/*/blame/*
Disallow: /*/*/commit/*
Disallow: /*/*/log/*
Disallow: /*/*/tree/*
Disallow: /*/*/item/*
Disallow: /*/*/mbox
Disallow: /*/*/*/raw

# Tarpit for any clients that don't respect robots.txt
Disallow: /tarpit

# Too aggressive, marketing/SEO
User-agent: SemrushBot
Disallow: /

# Too aggressive, marketing/SEO
User-agent: SemrushBot-SA
Disallow: /

# Marketing/SEO
User-agent: AhrefsBot
Disallow: /

# Marketing/SEO
User-agent: dotbot
Disallow: /

# Marketing/SEO
User-agent: rogerbot
Disallow: /

User-agent: BLEXBot
Disallow: /

# Huwei something or another, badly behaved
User-agent: AspiegelBot
Disallow: /

# Marketing/SEO
User-agent: ZoominfoBot
Disallow: /

# YandexBot is a dickhead, too aggressive
User-agent: Yandex
Disallow: /

# Marketing/SEO
User-agent: MJ12bot
Disallow: /

# Marketing/SEO
User-agent: DataForSeoBot
Disallow: /

# Used for Alexa, I guess, who cares
User-agent: Amazonbot
Disallow: /

# No
User-agent: turnitinbot
Disallow: /

User-agent: Turnitin
Disallow: /

# Does not respect * directives
User-agent: Seekport Crawler
Disallow: /

# Fairly certain that this is an LLM data vacuum
User-agent: ClaudeBot
Disallow: /

# Same
User-agent: Google-Extended
Disallow: /

# Marketing
User-agent: serpstatbot
Disallow: /

# Marketing/SEO
User-agent: barkrowler
Disallow: /

# Very aggressive, used for TikTok or something
User-agent: Bytedance
User-agent: Bytespider
User-agent: TikTokSpider
Disallow: /

# Facebook
User-agent: meta-externalagent
Disallow: /

# OpenAI
User-agent: OAI-SearchBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: GPTBot
Disallow: /

# Marketing/SEO
User-agent: AwarioRssBot
User-agent: AwarioSmartBot
Disallow: /

# AI slop
User-Agent: ImagesiftBot
Disallow: /

User-Agent: Crawlspace
Disallow: /
