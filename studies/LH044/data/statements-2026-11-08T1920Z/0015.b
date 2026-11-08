<!DOCTYPE html>
<html lang="en">

<head>
    <title>AI crawlers need to be more respectful - Read the Docs</title>
    <meta charset="utf-8" />
    <meta name="generator" content="Pelican" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta property="og:site_name" content="Read the Docs" />
    <link rel="canonical" href="https://about.readthedocs.com/blog/2024/07/ai-crawlers-abuse/" />
    <meta property="og:url" content="https://about.readthedocs.com/blog/2024/07/ai-crawlers-abuse/" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="AI crawlers need to be more respectful" />
    <meta name="description" content="We talk a bit about the AI crawler abuse we are seeing at Read the Docs, and warn that this behavior is not sustainable." />
    <meta property="og:description" content="We talk a bit about the AI crawler abuse we are seeing at Read the Docs, and warn that this behavior is not sustainable." />
    <meta property="og:image" content="https://about.readthedocs.com/images/headers/ai-crawlers.jpg" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="AI crawlers need to be more respectful" />
    <meta name="twitter:description" content="We talk a bit about the AI crawler abuse we are seeing at Read the Docs, and warn that this behavior is not sustainable." />
    <meta name="twitter:image" content="https://about.readthedocs.com/images/headers/ai-crawlers.jpg" />
    <meta name="tags" content="ai" />
    <meta name="tags" content="crawlers" />
    <meta name="tags" content="abuse" />
    <meta name="author" content="Eric Holscher" />
    <meta property="article:published_time" content="2024-07-25" />


    <link rel="apple-touch-icon" sizes="180x180" href="https://about.readthedocs.com/theme/img/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://about.readthedocs.com/theme/img/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="24x24" href="https://about.readthedocs.com/theme/img/favicon-24x24.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://about.readthedocs.com/theme/img/favicon-16x16.png">
    <link rel="shortcut icon" href="https://about.readthedocs.com/theme/img/favicon.ico">

    <link href="https://about.readthedocs.com//feeds/atom.xml" type="application/atom+xml" rel="alternate" title="Read the Docs Atom Feed" />
      <link href="https://about.readthedocs.com//feeds/engineering.atom.xml" type="application/atom+xml" rel="alternate" title="Read the Docs Categories Atom Feed" />

    <link rel="stylesheet" type="text/css" href="https://about.readthedocs.com/theme/css/site.css" />
    <script src="https://kit.fontawesome.com/53af4251af.js" crossorigin="anonymous"></script>

    <script src="https://about.readthedocs.com/theme/js/vendor.js"></script>
    <script src="https://about.readthedocs.com/theme/js/site.js"></script>
<script async type="text/javascript" src="/_/static/javascript/readthedocs-addons.js"></script><meta name="readthedocs-project-slug" content="readthedocs-about" /><meta name="readthedocs-version-slug" content="latest" /><meta name="readthedocs-resolver-filename" content="/blog/2024/07/ai-crawlers-abuse/" /><meta name="readthedocs-http-status" content="200" /></head>

<body>

<div class="ui basic fitted attached segment">
  <div class="ui container">
    <div class="ui middle aligned grid">

        <div class="four wide computer five wide tablet eleven wide mobile left aligned column">
          <div class="ui horizontally fitted basic segment">
            <a href="https://about.readthedocs.com/" aria-label="Read the Docs homepage">
              <img class="ui image" src="https://about.readthedocs.com/theme/img/logo-wordmark-dark.svg" width="220" alt="Read the Docs logo"/>
            </a>
          </div>
        </div>

        <div class="five wide mobile only right aligned column">
          <div class="ui wide dropdown" data-module="dropdown" data-action="select">
            <i class="fad fa-bars large icon" style="--fa-secondary-opacity: 0.8;"></i>
            <div class="left menu">

              <a class="item" href="https://about.readthedocs.com/features/">
                <i class="fad fa-arrow-progress primary icon"></i>
                Product
              </a>
              <a class="item" href="https://about.readthedocs.com/pricing/">
                <i class="fad fa-diagram-venn primary icon"></i>
                Pricing
              </a>
              <a class="item" href="https://about.readthedocs.com/blog/">
                <i class="fad fa-newspaper fa-swap-opacity primary icon"></i>
                Blog
              </a>
              <a class="item" href="https://docs.readthedocs.io" target="_blank">
                <i class="fad fa-book primary icon"></i>
                Docs
              </a>

              <div class="divider"></div>

                <div class="header">Log in</div>
  <a class="item" data-analytics="community-login" href="https://app.readthedocs.org/dashboard/">
    <i class="fad fa-people-group primary icon"></i>
    Read the Docs Community

    <p class="ui mini grey text">
      <code>https://readthedocs.org</code>
    </p>
  </a>
  <a class="item" data-analytics="commercial-login" href="https://app.readthedocs.com/dashboard/">
    <i class="fad fa-building secondary icon"></i>
    Read the Docs Business

    <p class="ui mini grey text">
      <code>https://readthedocs.com</code>
    </p>
  </a>
    <a class="item"
      data-analytics="signup-modal"
      onclick="jQuery('#signup-modal').modal('show');">
      <i class="fas fa-plus primary icon"></i>
      Sign up
    </a>

  <a class="item" href="/choosing-a-platform/">
    <i class="fad fa-circle-question grey icon"></i>
    Choosing a platform
  </a>


            </div>
          </div>
        </div>

        <div class="twelve wide computer eleven wide tablet left aligned tablet only computer only column">
          <div class="ui big borderless secondary menu">

            <a class="item" href="https://about.readthedocs.com/features/">
              Product
            </a>

            <a class="item" href="https://about.readthedocs.com/pricing/">
              Pricing
            </a>

            <a class="item" href="https://about.readthedocs.com/blog/">
              Blog
            </a>

            <a class="item" href="https://docs.readthedocs.io" target="_blank">
              Docs
            </a>

            <div class="right menu">

              <div class="item">
                <div class="ui floating top right pointing dropdown" data-module="dropdown" data-action="select" data-display-type="block">
                  <a class="ui">
                    Log in
                  </a>
                  <div class="menu">
                      <div class="header">Log in</div>
  <a class="item" data-analytics="community-login" href="https://app.readthedocs.org/dashboard/">
    <i class="fad fa-people-group primary icon"></i>
    Read the Docs Community

    <p class="ui mini grey text">
      <code>https://readthedocs.org</code>
    </p>
  </a>
  <a class="item" data-analytics="commercial-login" href="https://app.readthedocs.com/dashboard/">
    <i class="fad fa-building secondary icon"></i>
    Read the Docs Business

    <p class="ui mini grey text">
      <code>https://readthedocs.com</code>
    </p>
  </a>

  <a class="item" href="/choosing-a-platform/">
    <i class="fad fa-circle-question grey icon"></i>
    Choosing a platform
  </a>

                  </div>
                </div>
              </div>

              <div class="item">
                <a class="ui button"
                   data-analytics="signup-modal"
                   onclick="jQuery('#signup-modal').modal('show');">
                  Sign up
                </a>
              </div>

            </div>
          </div>
        </div>

    </div>
  </div>
</div>


<div class="ui modal"
       id="signup-modal"
       data-module="modal"
       data-inverted="true">
    <div class="header">Get started with Read the Docs</div>
    <div class="content">
      <div class="ui center aligned basic fitted segment">
        <p>
          Which site best fits your project?
        </p>
      </div>

      <div class="ui stacking centered grid">
        <div class="stretched row">

          <div class="seven wide computer sixteen wide tablet column">
            <div class="ui raised segment">
              <div class="ui header">
                Read the Docs Community
                <div class="sub header">
                  For free and open-source projects
                </div>
              </div>

              <div class="ui relaxed list">
                <div class="item">
                  <i class="fad fa-lock-open primary icon"></i>
                  Clone public repositories
                </div>
                <div class="item">
                  <i class="fad fa-eye primary icon"></i>
                  Public documentation
                </div>
                <div class="item">
                  <i class="fad fa-rectangle-ad primary icon"></i>
                  Ads supported hosting
                </div>
              </div>

              <div class="ui center aligned basic fitted segment">
                <p>
                  <b>Free</b> for open-source software.
                </p>

                <a class="ui primary center aligned button"
                  data-analytics="community-signup"
                   href="https://app.readthedocs.org/accounts/signup/">
                  Sign up
                </a>
              </div>
            </div>
          </div>

          <div class="seven wide computer sixteen wide tablet column">
            <div class="ui raised segment">
              <div class="ui header">
                Read the Docs Business
                <div class="sub header">
                  For commercial and non-free projects
                </div>
              </div>

              <div class="ui relaxed list">
                <div class="item">
                  <i class="fad fa-lock-keyhole primary icon"></i>
                  Clone private and public repositories
                </div>
                <div class="item">
                  <i class="fad fa-eye-slash primary icon"></i>
                  Public and private documentation
                </div>
                <div class="item">
                  <i class="fad fa-users primary icon"></i>
                  Team management for your organization
                </div>
              </div>

              <div class="ui center aligned basic fitted segment">
                <p>
                  Plans starting at <b>$50/month</b>.
                </p>

                <a class="ui primary center aligned button"
                  data-analytics="commercial-signup"
                   href="https://app.readthedocs.com/accounts/signup/">
                  Sign up
                </a>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <div class="actions">
      <a href="/choosing-a-platform/" class="ui cancel button"><i class="fad fa-circle-question grey icon" aria-hidden="true"></i>Choosing a platform</a>
      <a href="/features/" class="ui cancel button"><i class="fad fa-sparkles grey icon" aria-hidden="true"></i>Explore all the features</a>
    </div>
  </div>

  <main>  <section>
    <div class="ui very padded docutils text container">

      <div class="ui breadcrumb">
        <a class="section" href="/">Home</a>
        <div class="divider"> / </div>
        <a class="section" href="/blog/">Blog</a>
        <div class="divider"> / </div>
          <a class="section" href="/blog/category/engineering.html">Engineering</a>
          <div class="divider"> / </div>
        <div class="active section">AI crawlers need to be more respectful</div>
      </div>

      <div class="ui medium header">
        AI crawlers need to be more respectful
      </div>

      <div class="ui text menu">
        <time class="item" datetime="2024-07-25T00:00:00-07:00">Jul 25, 2024</time>

          <div class="item">
            <div class="ui dropdown" data-module="dropdown">
              <i class="fas fa-tag icon"></i>
              <i class="fas fa-caret-down icon"></i>
              <div class="menu">
                <div class="header">Tagged</div>
                  <a class="item" href="/blog/tag/ai.html">
                    <i class="fas fa-tag icon"></i>
                    ai
                  </a>
                  <a class="item" href="/blog/tag/crawlers.html">
                    <i class="fas fa-tag icon"></i>
                    crawlers
                  </a>
                  <a class="item" href="/blog/tag/abuse.html">
                    <i class="fas fa-tag icon"></i>
                    abuse
                  </a>
              </div>
            </div>
          </div>

        <div class="right menu">
          <div class="item">
Eric Holscher          </div>
        </div>
      </div>

      <div class="ui divider"></div>

      <img class="ui big rounded centered image" src="https://about.readthedocs.com/images/headers/ai-crawlers.jpg" alt="Photo by Zanyar Ibrahim on Unsplash">
        <div class="ui basic center aligned segment">
          <p><i>Photo by <a href="https://unsplash.com/@iizanyar?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Zanyar Ibrahim</a> on <a href="https://unsplash.com/photos/a-couple-of-people-that-are-sitting-in-a-car-JaUnya0pDIc?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a></i></p>
        </div>

      <div class="ui basic padded segment">
        <p>In the last few months, we have noticed an increase in abusive site crawling,
mainly from AI products and services. These products are recklessly crawling
many sites across the web, and we've already had to block several sources of abusive traffic.
It feels like a new AI gold rush,
and in their haste,
some of these crawlers are behaving in a way that harms the sites they depend on.</p>
<p>At Read the Docs,
we host documentation for many projects and are generally bot friendly,
but the behavior of AI crawlers is currently causing us problems.
We have noticed AI crawlers aggressively pulling content, seemingly without basic
checks against abuse.
Bots repeatedly download large files hundreds of times daily,
partially from bugs in their crawlers,
with traffic coming from many IP addresses without rate or bandwidth limiting.</p>
<p>AI crawlers are acting in a way that is not respectful to the sites they are crawling,
and that is going to cause a backlash against AI crawlers in general.
As a community-supported site without a large budget,
AI crawlers have cost us a significant amount of money in bandwidth charges,
and caused us to spend a large amount of time dealing with abuse.</p>
<h2 id="ai-crawler-abuse">AI crawler abuse</h2>
<p>We have been seeing a number of bad crawlers over the past few months,
but here are a couple illustrative examples of the abuse we're seeing:</p>
<h3>73 TB in May 2024 from one crawler</h3>
<p><strong>One crawler downloaded 73 TB of zipped HTML files in May 2024, with almost 10 TB in a single day</strong>. This cost us over $5,000 in bandwidth charges, and we had to block the crawler. We emailed this company, reporting a bug in their crawler, and we're working with them on reimbursing us for the costs.</p>
<p><img alt="AI crawler abuse, May 2024" src="/images/posts/bandwidth-may-2024.png"></p>
<p>This was a bug in their crawler that was causing it to download the same files over and over again.
There was no bandwidth limiting in place,
or support for Etags and Last-Modified headers which would have allowed the crawler to only download files that had changed.
We have reported this issue to them,
and hopefully the issue will be fixed.</p>
<p>We do have a CDN for these files,
but this request was for an old URL that had an old redirect in place.
This redirect went to an old dashboard download URL,
where we don't have CDN caching in place for security reasons around serving other dynamic content.
We are planning to fix this redirect to point to the cached URL.</p>
<details>
<summary>Example web requests</summary>

<pre>

-> curl -IL "https://media.readthedocs.org/htmlzip/chainer/v1.24.0/_modules/chainer/testing/_modules/chainer/_modules/cupy/indexing/_modules/chainer/initializers/normal.html"
HTTP/2 302
date: Thu, 25 Jul 2024 16:24:18 GMT
content-type: text/html
content-length: 138
location: https://buildmedia.readthedocs.org/media/htmlzip/chainer/v1.24.0/_modules/chainer/testing/_modules/chainer/_modules/cupy/indexing/_modules/chainer/initializers/normal.html
x-backend: web-i-0af0e99066a6e05c0
access-control-allow-origin: *
x-served: Nginx
cf-cache-status: DYNAMIC
server: cloudflare
cf-ray: 8a8d7fd81d060943-SEA

HTTP/2 302
date: Thu, 25 Jul 2024 16:24:18 GMT
content-type: text/html
content-length: 138
location: https://readthedocs.org/projects/chainer/downloads/htmlzip/v1.24.0/
x-backend: web-i-092bc168f09ac4a16
cf-cache-status: HIT
age: 537
expires: Thu, 25 Jul 2024 20:24:18 GMT
cache-control: public, max-age=14400
server: cloudflare
cf-ray: 8a8d7fda9837c87c-SEA

HTTP/2 200
date: Thu, 25 Jul 2024 16:24:18 GMT
content-type: application/zip
content-length: 5888860
content-disposition: filename=docs-chainer-org-en-v1.24.0.zip
x-amz-id-2: +DjI2tMbUou9XNK5+G53Gyhah4lhBwAgnRiqBh9vsR3KzqxajSTC4B+eIQBY+pi+ZR6McRQngSI=
x-amz-request-id: Z502YT87WEMM3ZY9
last-modified: Thu, 11 Feb 2021 09:12:59 GMT
etag: "c8cb418f5a8ff2e376fc5f7b7564e445"
x-amz-meta-mtime: 1495712654.422637991
accept-ranges: bytes
x-served: Nginx-Proxito-Sendfile
x-backend: web-i-01ce033e08bb601ef
referrer-policy: strict-origin-when-cross-origin
x-frame-options: DENY
x-content-type-options: nosniff
content-security-policy: object-src 'none'; frame-ancestors 'none'
cf-cache-status: DYNAMIC
server: cloudflare
cf-ray: 8a8d7fdbbf787565-SEA

</pre>

As you can see, this file was last modified in 2021.
However, crawlers didn't have this basic check and instead repeatedly downloaded files like these hundreds of times each.

</details>

<p><strong>Note</strong>: This company has been very responsive and did cover the cost of bandwidth for this abuse.</p>
<h3>10 TB in June 2024 from another</h3>
<p>In June 2024, <strong>someone used Facebook's content downloader to download 10 TB</strong> of data, mostly Zipped HTML and PDF files. We tried to email Facebook about it with the <a href="http://www.facebook.com/externalhit_uatext.php">contact information listed in the bot's user agent</a>, but the email bounced.</p>
<p><img alt="AI Crawler abuse, June 2024" src="/images/posts/bandwidth-june-2024.png"></p>
<p>We think this was someone using Facebook's content downloader to download all of our files, but we aren't really sure.
It could also be Meta crawling sites with their latest AI project,
but the user agent is not clear.</p>
<p><strong>Note</strong>: Facebook never replied to any of our emails, and continues to scrape us aggressively with their bots.</p>
<h2 id="actions-taken">Actions taken</h2>
<p>We have IP-based rate limiting in place for many of our endpoints,
however these crawlers are coming from a large number of IP addresses,
so our rate limiting is not effective.</p>
<p>These crawlers are using real user agents that identify them,
which is a good thing.
However, we can't simply rate limit all user agents to our platform because many real users use the same browsers with the same user agent.
(CDN providers: if you're reading this, there's an opportunity here!)</p>
<p>We have taken a few actions to try to mitigate this abuse:</p>
<ul>
<li>We have temporarily blocked all traffic from bots <a href="https://radar.cloudflare.com/traffic/verified-bots">Cloudflare identifies as AI Crawlers</a>, while we figure out how to deal with this.</li>
<li>We have started monitoring our bandwidth usage more closely and are working on more aggressive rate limiting rules.</li>
<li>We will reconfigure our CDN to better cache these files, reducing the load on our origin servers.</li>
</ul>
<h2 id="outcomes">Outcomes</h2>
<p>Given that our Community site is only for hosting open source projects,
AWS and Cloudflare do give us sponsored plans,
but we only have a limited number of credits each year.
The additional bandwidth costs AI crawlers are currently causing will likely mean we will run out of AWS credits early.</p>
<p><strong>By blocking these crawlers,
bandwidth for our downloaded files has decreased by 75% (~800GB/day to ~200GB/day).</strong>
If all this traffic hit our origin servers,
it would cost around $50/day, or $1,500/month,
along with the increased load on our servers.</p>
<p>Normal traffic gets cached by our CDN,
and doesn't cost us anything for bandwidth.
But because many of these files are not downloaded often (and they're large),
the cache is usually expired and the requests hit our origin servers directly,
causing substantial bandwidth charges.
Zipped documentation was designed for offline consumption by users, not for crawlers.</p>
<h2 id="next-steps">Next steps</h2>
<p>We are asking all AI companies to be more respectful of the sites they are crawling.
They are risking many sites blocking them for abuse,
irrespective of the other copyright and moral issues that are at play in the industry.</p>
<p>As a major host of open source documentation,
we'd love to work with these companies on a deal to crawl our site respectfully.
We could build an integration that would alert them to content changes,
and download the files that have changed.
However, none of these companies have reached out to us,
except in response to abuse reports.</p>
<p>We also ask that they implement basic checks in their crawlers for all sites.
A good example is the <a href="https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#scrapy.extensions.httpcache.RFC2616Policy">RFC2616Policy downloader from Scrapy</a>,
which implement many of these policies.</p>
<p>If these companies wish to be good actors in the space,
they need to start acting like it,
instead of burning bridges with folks in the community.</p>
      </div>

      <div class="ui basic paddded center aligned segment">
        <a href="/blog/" class="ui primary basic button">
          See more posts from our blog
        </a>
      </div>

    </div>
  </section>
</main>

<footer class="ui basic very padded inverted attached segment">
  <div class="ui container">

      <div class="ui four column stackable grid very padded">

        <div class="column">
          <div class="ui vertical inverted text menu">
              <h4 class="ui sub header">Stay updated</h4>
              <a class="item" href="/blog/">Blog</a>
              <a class="item" href="https://landing.mailerlite.com/webforms/landing/t0a9l4">Newsletter</a>
              <a class="item" href="https://status.readthedocs.com/">Status</a>
              <div class="item">
                <a href="https://github.com/readthedocs/" aria-label="Read the Docs on GitHub" rel="noopener noreferrer"><i class="icon large fab fa-github"></i></a>
                <a href="https://fosstodon.org/@readthedocs" aria-label="Read the Docs on Mastodon / Fediverse" rel="me"><i class="icon large fab fa-mastodon"></i></a>
              </div>
          </div>
        </div>

        <div class="column">
          <div class="ui vertical inverted text menu">
              <h4 class="ui sub header">Learn more</h4>
              <a class="item" href="https://docs.readthedocs.com/platform/stable/">Documentation</a>
              <a class="item" href="https://docs.readthedocs.com/platform/stable/tutorial/index.html">Tutorial</a>
              <a class="item" href="https://docs.readthedocs.com/platform/stable/config-file/index.html">Configure your project</a>
              <a class="item" href="https://docs.readthedocs.com/platform/stable/intro/doctools.html">Popular documentation tools</a>
              <a class="item" href="/comparisons/">Compare to other platforms</a>
          </div>
        </div>

        <div class="column">
          <div class="ui vertical inverted text menu">
              <h4 class="ui sub header">Product</h4>
              <a class="item" href="/features/">Features</a>
              <a class="item" href="/pricing/">Pricing</a>
              <a class="item" href="/privacy-policy/">Privacy Policy</a>
              <a class="item" href="/terms-of-service/">Terms of Service</a>
          </div>
        </div>

        <div class="column">
          <div class="ui vertical inverted text menu">
              <h4 class="ui sub header">Company</h4>
              <a class="item" href="/company/">About us</a>
              <a class="item" href="https://docs.readthedocs.com/platform/stable/support.html">Support</a>
              <a class="item" href="https://www.ethicalads.io/advertisers/?ref=rtd">Advertise with Us</a>
              <a class="item" href="https://docs.readthedocs.com/dev/latest/contribute.html">Contribute</a>

          </div>
        </div>

      </div>

      <div class="ui basic center aligned inverted segment">
        <i class="fad fa-copyright icon"></i>
        Copyright 2025, Read the Docs, Inc &amp; contributors
      </div>


  </div>
</footer></body>
</html>