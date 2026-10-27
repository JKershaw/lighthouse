// Run after npm run build. Browser dependencies are optional development tools:
// PLAYWRIGHT_MODULE=/path/to/playwright/index.mjs CHROMIUM_PATH=/path/to/chromium npm run test:offline
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(site, '_site');
const shots = path.join(site, 'test/screenshots/offline-36');
fs.mkdirSync(shots, { recursive: true });
let edition = 1;
let failArticle = false;
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webmanifest': 'application/manifest+json', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = http.createServer((request, response) => {
  let url = new URL(request.url, 'http://localhost');
  // Exercise the same build both at / and below a Pages-style prefix.
  let rel = decodeURIComponent(url.pathname).replace(/^\/lighthouse\//, '/');
  if (rel.endsWith('/')) rel += 'index.html';
  if (failArticle && rel === '/articles/php-emergency-first-reading/index.html') {
    response.writeHead(503, { 'Content-Type': 'text/html' }).end('<h1>Temporarily unavailable</h1>'); return;
  }
  const file = path.join(output, rel);
  if (!file.startsWith(output + path.sep) || !fs.existsSync(file)) { response.writeHead(404).end('not found'); return; }
  let body = fs.readFileSync(file);
  if (path.extname(file) === '.html' && edition > 1) body = Buffer.from(body.toString().replace('</main>', `<p id="fresh-edition">Edition ${edition}</p></main>`));
  if (rel === '/sw.js' && edition > 1) body = Buffer.from(body.toString().replace(/"version":"[^"]+"/, `"version":"browser-test-${edition}"`));
  if (rel === '/assets/site.css' && edition > 1) body = Buffer.from(`/* edition ${edition} */\n${body}`);
  response.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' }); response.end(body);
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true, args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'] });
// Playwright's waitForFunction polls synchronous predicates. Cache API checks
// are asynchronous, so evaluate and await each result before trying again.
async function waitInPage(page, predicate, argument) {
  const until = Date.now() + 15000;
  do {
    if (await page.evaluate(predicate, argument)) return;
    await new Promise((resolve) => setTimeout(resolve, 50));
  } while (Date.now() < until);
  throw new Error('Timed out waiting for asynchronous browser state');
}
try {
  // Prefix is passed when the build itself used PATH_PREFIX.
  const prefix = process.env.PATH_PREFIX || '/';
  const root = `${origin}${prefix.endsWith('/') ? prefix : prefix + '/'}`;
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: 'light' });
  const page = await context.newPage();
  // Start at an article rather than the precached front page, to test first-visit saving.
  const article = root + 'articles/php-emergency-first-reading/';
  await page.goto(article);
  await page.waitForFunction(() => navigator.serviceWorker.controller);
  await waitInPage(page, async () => (await caches.keys()).some((key) => key.endsWith(':pages')) &&
    Boolean(await (await caches.open((await caches.keys()).find((key) => key.endsWith(':pages')))).match(location.href)));
  const illustrations = await page.locator('main img').evaluateAll((images) => images.map((image) => image.currentSrc || image.src));
  assert.ok(illustrations.length > 0, 'the deep-link fixture has illustrations');
  await waitInPage(page, async (urls) => {
    const cache = await caches.open((await caches.keys()).find((key) => key.includes(':assets:')));
    return (await Promise.all(urls.map((url) => cache.match(url)))).every(Boolean);
  }, illustrations);
  const session = await context.newCDPSession(page);
  const app = await session.send('Page.getAppManifest');
  assert.deepEqual(app.errors, []);
  const manifest = JSON.parse(app.data);
  assert.equal(manifest.scope, prefix.endsWith('/') ? prefix : prefix + '/');
  const installability = await session.send('Page.getInstallabilityErrors');
  assert.deepEqual(installability.installabilityErrors, []);
  const assets = await page.evaluate(async () => (await (await caches.open((await caches.keys()).find((key) => key.includes(':assets:')))).keys()).map((key) => key.url));
  assert.equal(assets.filter((url) => url.endsWith('.woff2')).length, 5);
  await page.screenshot({ path: path.join(shots, 'reading-light-390.png') });
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.screenshot({ path: path.join(shots, 'reading-dark-390.png') });
  await context.setOffline(true);
  await page.goto(article);
  assert.ok((await page.locator('h1').textContent()).includes('PHP'));
  await page.waitForFunction(() => [...document.querySelectorAll('main img')].every((image) => image.complete && image.naturalWidth > 0));
  await page.goto(root + 'articles/');
  assert.equal(await page.locator('h1').textContent(), 'Pieces');
  await page.goto(root + 'never-opened/');
  assert.equal(await page.locator('h1').textContent(), 'You are offline');
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 390);
  await page.screenshot({ path: path.join(shots, 'fallback-dark-390.png') });
  const oldAssetCache = await page.evaluate(async () => (await caches.keys()).find((key) => key.includes(':assets:')));
  await context.setOffline(false);
  edition = 2;
  await page.goto(article);
  assert.equal(await page.locator('#fresh-edition').textContent(), 'Edition 2');
  await page.waitForFunction(() => [...document.querySelectorAll('main img')].every((image) => image.complete && image.naturalWidth > 0));
  await page.evaluate(async () => { const registration = await navigator.serviceWorker.getRegistration(); await registration.update(); });
  await waitInPage(page, async () => (await caches.keys()).some((key) => key.endsWith('assets:browser-test-2')));
  await waitInPage(page, async (old) => !(await caches.keys()).includes(old), oldAssetCache);
  const newCSS = await page.evaluate(async () => {
    const cache = await caches.open((await caches.keys()).find((key) => key.endsWith('assets:browser-test-2')));
    const css = await cache.match(new URL('assets/site.css', navigator.serviceWorker.controller.scriptURL).href);
    return css?.text();
  });
  assert.ok(newCSS.startsWith('/* edition 2 */'), newCSS);
  // A new worker keeps an opened article available offline.
  await context.setOffline(true);
  await page.goto(article);
  assert.equal(await page.locator('#fresh-edition').textContent(), 'Edition 2');
  await page.waitForFunction(() => [...document.querySelectorAll('main img')].every((image) => image.complete && image.naturalWidth > 0));
  await context.setOffline(false);
  failArticle = true;
  const unavailable = await page.goto(article);
  assert.equal(unavailable.status(), 503);
  assert.equal(await page.locator('h1').textContent(), 'Temporarily unavailable');
  await context.setOffline(true);
  await page.goto(article);
  assert.equal(await page.locator('#fresh-edition').textContent(), 'Edition 2');
  await context.setOffline(false);
  // A long reading session may evict old illustrations, never the font/CSS shell.
  const bounded = await page.evaluate(async (root) => {
    const cache = await caches.open((await caches.keys()).find((key) => key.endsWith('assets:browser-test-2')));
    for (let i = 0; i < 125; i++) {
      const url = new URL(`assets/favicon.svg?reading=${i}`, root).href;
      await fetch(url);
      for (let attempt = 0; attempt < 100 && !(await cache.match(url)); attempt++) await new Promise((resolve) => setTimeout(resolve, 10));
    }
    return { count: (await cache.keys()).length,
      css: Boolean(await cache.match(new URL('assets/site.css', root).href)),
      font: Boolean(await cache.match(new URL('assets/fonts/source-serif-4-normal-400.woff2', root).href)) };
  }, root);
  assert.ok(bounded.count <= 120);
  assert.equal(bounded.css, true);
  assert.equal(bounded.font, true);
  await context.close();
  console.log('Chromium: manifest/installability, first-visit caching, offline shell and fallback, fresh online HTML, build update and cache cleanup passed.');
} finally { await browser.close(); await new Promise((resolve) => server.close(resolve)); }
