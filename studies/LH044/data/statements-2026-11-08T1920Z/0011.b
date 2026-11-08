        <!DOCTYPE html>
        <html lang="en">
        <head><title>Anubis sends AI scraperbots to a well-deserved fate [LWN.net]</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
<meta property="og:title" content="Anubis sends AI scraperbots to a well-deserved fate">
<meta property="og:site_name" content="LWN.net">
<meta property="og:type" content="article">
<meta property="og:description" content="Few, if any, web sites or web-based services have gone unscathed by the locust-like hordes of A [...]">
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
<META NAME="robots" CONTENT="noai, noimageai">
        <link rel="icon" href="https://static.lwn.net/images/favicon.png"
              type="image/png">
        <link rel="alternate" type="application/rss+xml" title="LWN.net headlines" href="https://lwn.net/headlines/rss">
        <link rel="stylesheet" href="/CSS/lwn-v1">
<style>div.MakeALink { display: none }</style>

        
        </head>
        <body>
        <a name="t"></a>
<div id="menu"><a href="/" aria-label="Return to the front page">
            <img src="https://static.lwn.net/images/logo/barepenguin-70.webp" class="logo"
                 border="0" alt="LWN.net Logo">
            <span class="logo">LWN<br>.net</span>
            <span class="logobl">News from the source</span></a>
            <a href="/" aria-label="Return to the front page">
            <img src="https://static.lwn.net/images/lcorner-ss.png" class="sslogo"
                 border="0" alt="LWN"></a><div class="navmenu-container">
           <ul class="navmenu">
        <li><a class="navmenu" href="#t"><b>Content</b></a><ul><li><a href="/current/">Weekly Edition</a></li><li><a href="/Archives/">Archives</a></li><li><a href="/Search/">Search</a></li><li><a href="/Kernel/">Kernel</a></li><li><a href="/Security/">Security</a></li><li><a href="/Calendar/">Events calendar</a></li><li><a href="/Comments/unread">Unread comments</a></li><li><hr></li><li><a href="/op/FAQ.lwn">LWN FAQ</a></li><li><a href="/op/AuthorGuide.lwn">Write for us</a></li></ul></li>
<li><a class="navmenu" href="#t"><b>Edition</b></a><ul><li><a href="/Articles/1029427/">Return to the Front page</a></li></ul></li>
</ul></div>
</div> <!-- menu -->
<div class="topnav-spacer"></div>
<div class="top-banner not-print"><!-- no top ad served --></div>
<div class="topnav-container">
<div class="not-handset"><form action="https://lwn.net/Login/" method="post" name="loginform"
                 class="loginform">
        <label><b>User:</b> <input type="text" name="uname" value="" size="8" id="uc" /></label> 
		<label><b>Password:</b> <input type="password" name="pword" size="8" id="pc" /></label> <input type="hidden" name="target" value="/Articles/1028558/" /> <input type="submit" name="submit" value="Log in" /></form> |
           <form action="https://lwn.net/subscribe/" method="post" class="loginform">
           <input type="submit" name="submit" value="Subscribe" />
           </form> |
           <form action="https://lwn.net/Login/newaccount" method="post" class="loginform">
           <input type="submit" name="submit" value="Register" />
           </form>
        </div>
               <div class="handset-only">
               <a href="/Login/"><b>Log in</b></a> /
               <a href="/subscribe/"><b>Subscribe</b></a> /
               <a href="/Login/newaccount"><b>Register</b></a>
               </div>
               </div><div class="maincolumn flexcol">
<div class="middlecolumn">
<div class="PageHeadline">
<h1>Anubis sends AI scraperbots to a well-deserved fate</h1>
</div>
<div class="ArticleText"><main>
<blockquote class="ad">
<b>Ready to give LWN a try?</b>
<p>
With a subscription to LWN, you can stay current with what is happening in the Linux and free-software community and take advantage of subscriber-only site features.  We are pleased to offer you <b><a href="https://lwn.net/Promo/nst-trial1/claim">a free trial subscription</a></b>, no credit card required, so that you can see for yourself.  Please, join us!
</blockquote>
<div class="FeatureByline">
           By <b>Joe Brockmeier</b><br>July 10, 2025</br>
           </div>
<p>Few, if any, web sites or web-based services have gone unscathed by
the locust-like hordes of AI crawlers looking to <a href="https://lwn.net/Articles/1008897/">consume (and then
<em>re-consume</em>) all of the world's content</a>. The <a
href="https://anubis.techaro.lol/">Anubis</a> project is designed to
provide a first line of defense that blocks mindless bots&mdash;while
granting real users access to sites without too much hassle. Anubis is
a young project, not even a year old. However, its development is
moving quickly, and the project seems to be enjoying rapid
adoption. The most recent release of Anubis, <a
href="https://anubis.techaro.lol/blog/release/v1.20.0/">version
1.20.0</a>, includes a feature that many users have been interested in
since the project launched: support for challenging clients without
requiring users to have JavaScript turned on.</p>

<h4>Block bots, bless browsers</h4>

<p>AI scraping bots, at least the ones causing the most headaches, are
designed to ignore <a
href="https://en.wikipedia.org/wiki/Robots.txt"><tt>robots.txt</tt></a>
and evade detection by lying about their <a
href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent
header</a>, and come from vast numbers of IP addresses, which poses a 
serious problem for site owners trying to fend them off. The swarms of
scrapers can be devastating for sites, particularly those with
dynamically generated content like Git forges.</p>

<p>How do site owners block bots while leaving the door
open for the people those sites are supposed to serve? Most methods
that might help also subject users to annoying <a
href="https://en.wikipedia.org/wiki/CAPTCHA">CAPTCHAs</a>, block RSS
readers and Git clients, or introduce other friction that makes a site
less usable. Blocking bots without too much friction is the problem
that Anubis hopes to solve.</p>

<img src="https://static.lwn.net/images/2025/anubis-happy.png" class="lthumb" border="0"
alt="[Anubis mascot image]" title="Anubis mascot image"/>

<p>The MIT-licensed project was <a
href="https://xeiaso.net/blog/2025/anubis/">announced</a> in January
by its author, Xe Iaso. Anubis is written in Go (plus some JavaScript
used for testing clients); it is designed to sit between a <a
href="https://en.wikipedia.org/wiki/Reverse_proxy">reverse proxy</a>,
such as <a href="https://caddyserver.com/">Caddy</a> or <a
href="https://nginx.org/">NGINX</a>, and the web-application
server.</p>

<p>In a <a
href="https://xeiaso.net/talks/2025/bsdcan-anubis/">write-up of a
lightning talk</a> given at <a
href="https://www.bsdcan.org/2025/">BSDCan 2025</a> in June, Iaso said
that Anubis was initially developed simply to keep scrapers from
taking down Iaso's Git server. They hosted the project on <a
href="https://github.com/TecharoHQ">GitHub</a> with the organization
name <a href="https://techaro.lol/">Techaro</a>. The name was supposed
to be for a fake startup as a satire of the tech industry. Then GNOME
started using the project, and it took off from there. Now Techaro is
the name that Iaso is actually using for their business.</p>

<p>Many LWN readers are already familiar with the project's mascot,
shown to the left, which is displayed briefly after a client
browser has successfully passed Anubis's test. In the short time that
the project has been available, it has already been pressed into
service by a <a href="https://xeiaso.net/notes/2025/anubis-works/">number
of free-software projects</a>, including the <a
href="https://lkml.org/">Linux Kernel Mailing List archive</a>, <a
href="https://sr.ht/">sourcehut</a>, <a
href="https://ffmpeg.org/">FFmpeg</a>, and others. A <a
href="https://git.xeserv.us/xe/anubis-test/src/branch/main/README.md">demo</a>
is available for those who have not yet encountered Anubis or just want
a refresher.</p>

<p>The project takes its name from the <a
href="https://en.wikipedia.org/wiki/Anubis">Egyptian god of funerary
rites</a>; Anubis was reputed to weigh
the hearts of the dead to determine whether the deceased was worthy
of entering paradise. If the heart was lighter than a feather, the
deceased could proceed to a heavenly reward&mdash;if not, they would
be consumed by <a
href="https://en.wikipedia.org/wiki/Ammit">Ammit</a>, the devourer of
the dead.</p>

<h4>How Anubis works</h4>

<p>Sadly, we have no crocodile-headed god to dispatch AI scrapers for
eternity. The next best thing is to deny them entry, as Anubis does,
by putting up a <a
href="https://en.wikipedia.org/wiki/Proof_of_work">proof-of-work</a>
challenge that helps sniff out scrapers in disguise. Iaso was inspired
to take this approach by Adam Back's <a
href="https://en.wikipedia.org/wiki/Hashcash">Hashcash</a> system,
originally proposed in 1997.</p>

<p>Hashcash was intended to make sending spam more expensive by
requiring a "stamp" in each email's headers. The stamp would be
generated by causing the client to run a hash-based proof-of-work
task, which required some CPU time for every email. Email without a
stamp would be routed to <tt>/dev/null</tt>, thus sparing a user's
inbox. The idea was that Hashcash would be little burden for users
sending email at normal volume, but too costly to generate large
amounts of spam. Hashcash did not take off, to the detriment of all of
our inboxes, but that doesn't mean the idea was entirely without
merit.</p>

<!-- middle-ad -->

<p>When a request comes to Anubis, it can issue a challenge, evaluate
the response, and (if the client passes) issue a signed JSON web token
(JWT) cookie (named "<tt>techaro.lol-anubis-auth</tt>") that will
allow the browser access to the site's resources for a period of
time.</p>

<p>Anubis decides what action to take by consulting its <a
href="https://anubis.techaro.lol/docs/admin/policies">policy
rules</a>. It has three possible actions: allow, challenge, or
deny. Allow passes the request to the web service, while deny sends an
error message that is designed to look like a successful request to AI
scrapers. Challenge, as one might expect, displays the challenge page
or validates that a client has passed the challenge before routing the
request.</p>

<p>The default policy for Anubis is to challenge
"<q>everything that might be a browser</q>", which is <a href="https://webaim.org/blog/user-agent-string-history/">usually
indicated by the presence of the string <tt>Mozilla</tt> in the
User-Agent header</a>. Because the creators of AI scrapers know that
their bots are unwelcome (and apparently have no ethics to speak of)
most scraper bots try to pass themselves off as browsers as well. But
they generally do not run client-side JavaScript, which means they can
be stymied by tools like Anubis.</p>

<p>Administrators have the choice of JSON or YAML for writing custom
policy rules. Rules can match the User-Agent string, HTTP request
header values, and the request path. It is also possible to filter
requests by IP address or range. So, for example, one might allow a
specific search engine bot to connect, but only if its IP address
matches a specific range.</p>

<p>The difficulty of Anubis's challenge is also configurable. It
offers <a
href="https://anubis.techaro.lol/docs/admin/algorithm-selection">fast
and slow</a> proof-of-work algorithms, and allows administrators to
set a higher or lower difficulty level for running them. The fast
algorithm uses optimized JavaScript that should run quickly. The slow
algorithm is designed to waste time and memory. A site
might have a policy that lowers the difficulty for a client that has
specific session tokens or ratchets up the difficulty for clients
that request specific resources. One might also set policy to
automatically allow access to some resources, like
<tt>robots.txt</tt>, without any challenge. The difficulty level is
expressed as a number; a difficulty of 1 with the fast algorithm
should take almost no time on a reasonably fast computer. The default
is 4, which is noticeable but only takes a few seconds. A difficulty of
6, on the other hand, can take minutes to complete.</p>

<h4>New features</h4>

<p>The 1.20.0 release includes RPMs and Debian packages for several
architectures, as well as other binaries for Linux and source
code. Iaso would like to expand that to providing binary packages for
BSD, as well as better testing for BSDs in general. In addition to the
packages supplied by the project, Anubis is also <a
href="https://github.com/TecharoHQ/anubis?tab=readme-ov-file#packaging-status">packaged</a>
by a few Linux distributions, <a
href="https://ports.freebsd.org/cgi/ports.cgi">FreeBSD Ports</a>, the
<a href="https://brew.sh/">Homebrew</a> project, and <a
href="https://repology.org/project/anubis-anti-crawler/versions">others</a>. However,
many of the packages are not up-to-date with the most recent Anubis
stable version. A <a
href="https://anubis.techaro.lol/docs/admin/installation#docker-image-conventions">container
image</a> for Anubis is also available for those who would prefer that
method of deployment.</p>

<p>The release introduces <a
href="https://anubis.techaro.lol/docs/admin/robots2policy"><tt>robots2policy</tt></a>,
a command-line tool that converts a site's <tt>robots.txt</tt> to
Anubis policy. I tried it
with LWN's <a
href="https://lwn.net/robots.txt"><tt>robots.txt</tt></a> and it
correctly added rules against allowing bots to access <a
href="https://lwn.net/Search/">site search</a> and <a
href="https://lwn.net/ml/">mailing-list search</a>, but only included
one rule denying access to a specific crawler, as it expects each
<tt>User-agent</tt> line to have its own allow or disallow rule. 

<p>Another new feature in 1.20.0 is <a
href="https://anubis.techaro.lol/docs/admin/configuration/thresholds">custom-weight
thresholds</a>, a way for administrators to set variable thresholds for
client challenges based on how suspicious a client is&mdash;much like
scoring used by spam filters. Does a client's user-agent have the
string "bot" in it? Administrators can assign more weight points and
up the difficulty level of the proof-of-work challenge. Does a client
present a cookie that indicates that it already has a session with a
trusted service? It can have points taken off its weight score. If a
score is low enough, a client can be waved through without any
challenge at all. If the score is too high, the client can be assigned
a particularly difficult challenge that will take longer to
complete.</p>

<p>Some administrators <a
href="https://github.com/TecharoHQ/anubis/issues/95#issuecomment-2852790645">have
been hesitant to use Anubis</a> because they would rather not block
users who turn off JavaScript. Indeed, that was one reason that we
opted not to deploy Anubis for LWN's bot problem. With
1.20.0, administrators can use the <a
href="https://anubis.techaro.lol/docs/admin/configuration/challenges/metarefresh"><tt>metarefresh</tt></a>
challenge in addition to, or in place of, the JavaScript proof-of-work
challenge. As the name suggests, it makes use of the <a
href="https://en.wikipedia.org/wiki/Meta_refresh">meta refresh</a>
HTML element that can instruct a browser to refresh a page or redirect
to a new page after a set time period, usually a few seconds. This
method is currently off by default, as it is still considered somewhat
experimental.</p>

<p>I installed 1.20.0 on a test Debian bookworm system running
Apache. The <a
href="https://anubis.techaro.lol/docs/admin/environments/apache">documentation</a>
for Apache was <a href="https://github.com/TecharoHQ/anubis/pull/784#partial-pull-merging">missing a line in the sample configuration</a> (the opening
stanza for the mod_proxy module), but it was otherwise easy to get up
and running. The project also has documentation for other environments
that might require special configuration, such as using Anubis with
Kubernetes or WordPress. Given the project's speed of development, the
documentation seems well-tended overall; the pull request I filed for
the missing stanza in the Apache documentation was reviewed almost immediately.</p>

<h4>Anime girl and other complaints</h4>

<p>Some have complained that the Anubis mascot is "<q>not appropriate
for use on customer facing systems</q>" and <a
href="https://github.com/TecharoHQ/anubis/issues/281">asked</a> for a
flag to disable it. Iaso has <a
href="https://github.com/TecharoHQ/anubis/issues/281#issuecomment-2810942983">said</a>
that the ability to change or disable branding is an "<q>enterprise
feature</q>", though they are open to making it a feature if Anubis <a
href="https://github.com/TecharoHQ/anubis/discussions/278">becomes
fiscally sustainable</a>. While Anubis is free software, Iaso has <a
href="https://anubis.techaro.lol/docs/funding/">asked</a> ("<q>but not
demand, these are words on the internet, not word of law</q>") people
not to remove the anime girl character from Anubis deployments unless
they support Anubis development financially.

<p>Initially, there was some
<a
href="https://github.com/TecharoHQ/anubis/issues/33#issuecomment-2741845002">controversy</a>
because Anubis was using a mascot that was generated with AI, which
did not sit well with some folks. In March, Iaso <a
href="https://github.com/TecharoHQ/anubis/issues/33#issuecomment-2741848496">noted</a>
that they were <a
href="https://github.com/TecharoHQ/anubis/discussions/143">commissioning
a new mascot</a> from <a
href="https://bsky.app/profile/celphase.bsky.social">CELPHASE</a>, an
artist based in the European Union, which became the current anime
girl mascot.</p>

<p>Even with a professionally designed character, some organizations,
such as <a href="https://duke.edu/">Duke University</a>, are hesitant
to deploy Anubis in part because of its mascot. Duke experienced
problems with bot traffic overwhelming several services, such as the
<a href="https://repository.duke.edu/">Digital Repositories at
Duke</a> and its <a href="https://archives.lib.duke.edu/">Archives
&amp; Manuscripts</a> catalog, and performed a pilot project with
Anubis.</p>

<p>The <a
href="https://library.duke.edu/about/depts/assessment-user-experience">Assessment
&amp; User Experience Strategy</a> department of the university library
released a <a
href="https://dukespace.lib.duke.edu/server/api/core/bitstreams/816ef134-55cf-49f6-9a8b-1e8a2324b1ff/content">report</a>
in June, written by Sean Aery, about the pilot project. Aery reported
that Anubis was effective&mdash;it blocked more than 4 million unwanted HTTP
requests per day&mdash;while still allowing real users and
well-behaved bots. Some real users were blocked too; 12 people
reported having a problem with Anubis in one week, but that was
usually due to having cookies disabled, according to the report.</p>

<p>However, despite Anubis's efficacy, the first limitation listed
by Aery was the user interface for the challenge page:</p>

<blockquote class="bq">
The images, messages, and styles presented in the default challenge
page UI are not ideal -- particularly its anime girl mascot
image. Anubis lacks convenient seams to revise any of these elements.
</blockquote>

<p>As of this writing, Duke is "<q>in discussions</q>" with Iaso about
"<q>a sustainable way forward</q>" and is still using Anubis; in the
meantime, it has customized the page interface with artwork it has
deemed more appropriate.</p>

<p>Aery does list some real limitations that users should be
aware of before adopting the project, however. For example, the report
notes that it is very early days for the project and for the practice
of fending off AI scrapers. The project is evolving rapidly, so
administrators will have to stay on top of frequent updates. And there
is no guarantee that Anubis will maintain its edge against scrapers in
the long run. Today, Anubis works very well at blocking unwanted
visitors, but tomorrow? Many scrapers aren't willing to abide by a gentle
"no" now; they are unlikely to give up easily if Anubis and other
bot-blockers start denying access to resources their
ethically-challenged owners really want. Bot
makers will start looking for and finding ways around the
blockers. Blockers versus bots will no doubt be a arms race the same
way that spam filtering is a never-ending battle against spammers.</p>

<p>Another limitation is Anubis's bus factor; Iaso is responsible for
about half the commits to the project. More than 80 people have
contributed to the project since its inception, but only one
contributor (Jason Cameron) has more than ten commits to the
repository.</p>

<p>Iaso is not just carrying most of the development load for Anubis;
they are also trying to build a business around the project. The
boundaries between Anubis, the open-source project, and Iaso's budding
business are fuzzy; combining BDFL-type governance with the 
potential conflicts of interest coming from a related business has been
known to go poorly. That is not to say that it will in this instance,
of course.</p>

<p>Anubis already ships with <a
href="https://anubis.techaro.lol/docs/admin/thoth">advanced reputation
checking</a> that works only with a paid service called Thoth offered
by Techaro. Thoth allows Anubis to filter IP addresses by geography
(<a href="https://en.wikipedia.org/wiki/Internet_geolocation">GeoIP</a>) or <a
href="https://en.wikipedia.org/wiki/Autonomous_system_(Internet)">BGP
autonomous system numbers</a> so administrators can block or challenge
clients by region or provider (such as Cloudflare). As the project
continues to gain traction, it will be interesting to see if Iaso
accepts contributions that might conflict with Techaro paid services.</p>

<h4>The future</h4>

<p>Iaso said at BSDCan&nbsp;2025 that they were not sure what the end
game for Anubis is:</p>

<blockquote class="bq">
<p>I want to make this into a web application firewall that can
potentially survive the AI bubble bursting. Because right now the AI
bubble bursting is the biggest threat to the business, as it were.</p>
</blockquote>

<p>Since Anubis is, essentially, a one-person show, it raises the
question of whether they will be able to stay ahead in the inevitable
arms race against scrapers. Iaso did say that they hope to hire
another developer, and to provide Anubis as a hosted service at some
point. Iaso is also trying out new ways to sort bots from real
browsers with various <a
href="https://en.wikipedia.org/wiki/Device_fingerprint">browser
fingerprinting</a> techniques, such as John Althouse's <a
href="https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md">JA4
TLS</a> and a novel method of Iaso's own devising called <a
href="https://github.com/TecharoHQ/anubis/blob/6b09ac95431374bf3c6a7e2872cacc59bb2c8801/docs/docs/developer/thr1.mdx">Techaro
HTTP Request Fingerprinting Version 1</a> (THR1).</p>

<p>Anubis only denies scrapers access to content; it does not, as some
might wish, actually feed nonsense data to scrapers to poison the data
sets that are being created. There are, at least, two open-source
projects that do set out to punish unwanted crawlers by sending the
bots data to give them indigestion: <a
href="https://zadzmo.org/code/nepenthes/">Nepenthes</a> and <a
href="https://lib.rs/crates/iocaine">iocaine</a>. Anubis has an <a
href="https://github.com/TecharoHQ/anubis/issues/61">open issue</a>
to add a target for unverified requests that would allow
administrators to redirect clients to Nepenthes or iocaine instead of
simply blocking access. Iaso has <a
href="https://github.com/TecharoHQ/anubis/issues/61#issuecomment-2746560798">said</a>
that they are willing to do this but thinks "<q>Anubis itself should
not be directly generating the poison</q>".</p>

<p>User "gackillis" has put
together a proof-of-concept project called <a
href="https://gacki.protogen.world/git/gackillis/jackals-carapace">jackal's
carapace</a> that works together with Anubis. It "<q>very slowly spits
out garbage data</q>", pointing to a tarpit for scrapers while Anubis
is loading. If the scraper takes the bait, it winds up in the tarpit
instead of being fed real content. However, gackillis warns (in all
caps) that the project is not ready for real-world deployments and
could spike CPU and network usage dramatically.</p>

<p>On July&nbsp;6, Iaso <a
href="https://github.com/TecharoHQ/anubis/releases/tag/v1.21.0-pre1">announced</a>
a pre-release of Anubis 1.21.0. The major changes in the upcoming
release include the addition of new storage types for Anubis's temporary
data, support for localized responses, and allowing access to <a
href="https://commoncrawl.org/">Common Crawl</a> by default "<q>so
scrapers have less incentive to scrape</q>". It also includes a fix
for a pesky <a
href="https://github.com/TecharoHQ/anubis/issues/564">bug that
delivers an invalid response</a> for some browsers after passing
Anubis's test. That bug was thought to be fixed in 1.20.0, but the bug
was reopened <a
href="https://github.com/TecharoHQ/anubis/issues/564#issuecomment-3016123552">after
reports</a> that users were still seeing the bug.</p>

<p>In a better world, Anubis would never have been necessary&mdash;at
least not in its current form. It's an additional layer of complexity
for site owners to manage and introduces friction for users browsing
the web. But Anubis is a lesser evil when compared to having sites knocked
offline by overzealous bot traffic or employing more burdensome
CAPTCHAs. With luck, Iaso and other contributors will be able to stay
one step (or more) ahead of the scrapers until the AI bubble bursts.</p><br clear="all"><hr>
    The LWN site is currently under high scraper load, so comment
    display has been suppressed for anonymous users.
    If you are a
        human, you may read the comments by clicking the button below:
        <p>
        <blockquote>
         <form action="/Articles/1028558/#Comments" method="POST">
        	<input type="submit" name="go" value="See the comments" />
         </form>
        </blockquote>
        <p>
        <b>Note</b>: you can avoid this step in the future by logging
        into your LWN account.
    
</main></div> <!-- ArticleText -->
</div> <!-- middlecolumn -->
<div class="rightcol not-print">
<!-- no side ad served -->
</div>
</div> <!-- maincolumn -->

            <br clear="all">
            <center>
            <P>
            <span class="ReallySmall">
            Copyright &copy; 2025, Eklektix, Inc.<BR>
            This article may be redistributed under the terms of the
              <a href="http://creativecommons.org/licenses/by-sa/4.0/">Creative
              Commons CC BY-SA 4.0</a> license<br>
            Comments and public postings are copyrighted by their creators.<br>
            Linux  is a registered trademark of Linus Torvalds<br>
            </span>
            </center>
            
            </body></html>
