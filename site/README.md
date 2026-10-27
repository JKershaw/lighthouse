# The Lighthouse site

Eleventy builds the website from this repository's Markdown. Every Markdown file outside harbour/, site/ and .claude/ becomes a page at a path mirroring its own, so a new file appears on the next build.

## Build and serve locally

Needs Node 18 or later.

```
cd site
npm ci
npm run build    # writes site/_site
npm run serve    # rebuilds on change, at http://localhost:8080
npm test         # the scan and HTML rewrites, against test/fixtures/repo
```

## What the site reads

A piece (articles/*.md, articles/short/*.md) may open with a header before its `# Title`: `published` (YYYY-MM-DD; else the byline's date, else git), `summary` (for listings; else the opening paragraph), `status` (`draft` or `released`), `investigation` (an id in investigations/) and `revised` (items `YYYY-MM-DD: sentence`, shown as a notice). A blockquote beginning `**Correction, <date>.**` or `**Later evidence, <date>.**` is shown as a notice, and its date counts as the piece's latest update in listings. A piece with neither `published` nor a byline is dated by the commit that added it, so a later edit does not move it. An essay (essays/*.md) takes the same header and is laid out the same way, labelled Essay; released essays are listed at /essays/, which the navigation links once one is released. On the front page, the latest pieces close the section headed "Findings", or follow the first section when there is none, and the latest released essays close the section headed "Essays". A piece that links review notes (notes/R-*.md) shows a Reviewed badge linking to them; a draft shows none. Pages read in one of three registers: findings (articles/), essays, and records (studies/, notes/ and any document whose header is shown as facts), which are set in sans-serif. The front page's watch strip is read from notes/php-watch-log.md: its newest `## <date>` day, the latest `HH:MM UTC` in an item's bold label, and its `**Flagged for review...**` item; without the log, or a day in it, the strip is left out. An investigation is investigations/<id>.md with `title`, `id`, `attention`, `question`, `current`, `started`, `studies` and `pieces` (in reading order). The site's description and its address, which the Atom feed at /feed.xml uses for its links, are in site.json. The feed lists released pieces, short forms and essays.

## Publish with GitHub Pages

.github/workflows/site.yml builds and deploys on every push to main. To enable it, open the repository's Settings, then Pages, and set Source to GitHub Actions. A run made before Pages was enabled fails at its Pages step; re-run it from the Actions page, or push to main again, and the next run deploys. The site appears at https://jkershaw.github.io/lighthouse/.

For a custom domain, enter it under Settings, Pages, Custom domain. At your DNS provider, point a subdomain such as www at jkershaw.github.io with a CNAME record, or an apex domain at the A and AAAA addresses GitHub's Pages documentation lists. Tick Enforce HTTPS once the certificate is issued. Deploying from Actions needs no CNAME file.

## Any other host

Any static host can serve site/_site. Below a domain's root, build with PATH_PREFIX set to that path, such as /lighthouse/.

## Home screen and offline reading

On HTTPS (or localhost), the manifest allows a browser to offer installation or Add to Home Screen. Icons are PNG renders of assets/favicon.svg at 192, 512 and 180 pixels; the light background and theme colour match the site's paper token. There is no installation prompt or tracking.

The build writes manifest.webmanifest and sw.js after generating the pages. The worker saves the front page, every top-level section front present in that build, the offline fallback, CSS, scripts and local fonts. It also saves opened pages and their illustrations, including a first visit directly to an article. HTML always goes to the network first with the HTTP cache bypassed; a saved copy is used only when the network request fails. A server error remains a server error. Static assets use the cache first.

A content hash changes the worker on each changed build. Installation fetches the new shell before activating it, refreshes saved illustrations where possible, and removes the preceding asset cache. Opened pages survive an update and are refreshed on their next online visit. Storage is bounded to 80 pages and 120 assets, apart from the protected shell (section fronts, CSS, scripts, fonts and icons); a browser may also evict saved data. Offline copies reflect the last successful visit, rather than a promise that an account is current. No background checking happens when the site is closed.

Source Serif 4 is served locally in its original regular, semibold and italic styles, alongside the interface face Source Sans 3 in regular and semibold. The font files were retrieved on 27 October 2026 through [Google Fonts' CSS endpoint](https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap) and converted from TTF to WOFF2 with fontTools. Their SIL Open Font Licenses are included for [Source Serif 4](assets/fonts/source-serif-4-LICENSE.md) and [Source Sans 3](assets/fonts/source-sans-3-LICENSE.md). Reading needs no third-party stylesheets, fonts or scripts.

`npm test` checks shell generation and prefix handling. For browser checks, install Playwright as a development tool, build, then run `npm run test:offline`. Set PLAYWRIGHT_MODULE to an absolute Playwright module path and CHROMIUM_PATH to a Chromium executable when using a preinstalled browser. The same test supports a build made with PATH_PREFIX=/lighthouse/ when that variable is also passed to the test command. It exercises Chromium's manifest and installability checks, first-visit saving, offline pages and illustrations, the fallback, fresh online HTML, a new worker and old-cache removal. Screenshots are kept in test/screenshots/offline-36/.

## The front page and section fronts

README.md selects its lead with `lead: articles/name.md` and supplies a short `deck:` in the same opening header. Only a released full finding can lead. Its first existing image supplies the illustration, original alternative text and caption; a draft or a missing illustration cannot supply an image. The publication and latest substantive update are shown beside it. The lead deck must remain true when read alone.

The four section fronts are always available at /watch/, /articles/, /essays/ and /map/. Their optional hand-set leads, ledes and short listing summaries live in [sections.md](sections.md), as repository paths rather than template constants. The scan supplies lists, dates and kinds, with drafts excluded. The daily log is labelled unreviewed wherever it is listed. Short listing summaries are editorial signposts; they do not replace a piece's full summary.

The home page shows compact section lists. All of README.md's original prose, figures and qualifications remain in the keyboard-accessible **Background and qualifications** disclosure below them, and README.md continues to read as ordinary Markdown on GitHub. Nothing in a released article is rewritten by these templates.
