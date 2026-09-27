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

A piece (articles/*.md, articles/short/*.md) may open with a header before its `# Title`: `published` (YYYY-MM-DD; else the byline's date, else git), `summary` (for listings; else the opening paragraph), `status` (`draft` or `released`), `investigation` (an id in investigations/) and `revised` (items `YYYY-MM-DD: sentence`, shown as a notice). A blockquote beginning `**Correction, <date>.**` or `**Later evidence, <date>.**` is shown as a notice. An investigation is investigations/<id>.md with `title`, `id`, `attention`, `question`, `current`, `started`, `studies` and `pieces` (in reading order). The site's description is in site.json.

## Publish with GitHub Pages

.github/workflows/site.yml builds and deploys on every push to main. To enable it, open the repository's Settings, then Pages, and set Source to GitHub Actions. A run made before Pages was enabled fails at its Pages step; re-run it from the Actions page, or push to main again, and the next run deploys. The site appears at https://jkershaw.github.io/lighthouse/.

For a custom domain, enter it under Settings, Pages, Custom domain. At your DNS provider, point a subdomain such as www at jkershaw.github.io with a CNAME record, or an apex domain at the A and AAAA addresses GitHub's Pages documentation lists. Tick Enforce HTTPS once the certificate is issued. Deploying from Actions needs no CNAME file.

## Any other host

Any static host can serve site/_site. Below a domain's root, build with PATH_PREFIX set to that path, such as /lighthouse/.
