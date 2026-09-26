# The Lighthouse site

Eleventy builds the website from this repository's Markdown. Every Markdown file outside harbour/, site/ and .claude/ becomes a page at a path mirroring its own, so a new file appears on the next build.

## Build and serve locally

Needs Node 18 or later.

```
cd site
npm ci
npm run build    # writes site/_site
npm run serve    # rebuilds on change, at http://localhost:8080
```

## Publish with GitHub Pages

.github/workflows/site.yml builds and deploys on every push to main. To enable it, open the repository's Settings, then Pages, and set Source to GitHub Actions. The site appears at https://jkershaw.github.io/lighthouse/.

For a custom domain, enter it under Settings, Pages, Custom domain. At your DNS provider, point a subdomain such as www at jkershaw.github.io with a CNAME record, or an apex domain at the A and AAAA addresses GitHub's Pages documentation lists. Tick Enforce HTTPS once the certificate is issued. Deploying from Actions needs no CNAME file.

## Any other host

Any static host can serve site/_site. Below a domain's root, build with PATH_PREFIX set to that path, such as /lighthouse/.
