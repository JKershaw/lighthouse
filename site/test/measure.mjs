// Measure built pages for the reader's site budgets (site/budgets.json).
// Run after npm run build: node test/measure.mjs [url path ...] [--shots <dir>] [--check]
// Prints JSON: for each page and width (390 and 1280 px), the page height,
// the words in <main>, the links on the page, the header navigation entries
// and the <main> section headings. Fonts from the network are blocked so that
// layout does not depend on them. Supports PLAYWRIGHT_MODULE and CHROMIUM_PATH.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';
const pw = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const chromium = pw.chromium || pw.default.chromium;
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(site, '_site');
const args = process.argv.slice(2);
const shotAt = args.indexOf('--shots');
const shots = shotAt >= 0 ? args.splice(shotAt, 2)[1] : '';
const checkAt = args.indexOf('--check');
const check = checkAt >= 0 ? Boolean(args.splice(checkAt, 1)) : false;
const urls = args.length ? args : ['/'];
const types = { '.html': 'text/html', '.svg': 'image/svg+xml', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  let file = path.join(output, decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
  try {
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!file.startsWith(output + path.sep)) throw Error();
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  } catch { res.writeHead(404); res.end(); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true, args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'] });
const result = {};
try {
  const origin = `http://127.0.0.1:${server.address().port}`;
  for (const url of urls) {
    result[url] = {};
    for (const width of [390, 1280]) {
      for (const theme of shots ? ['light', 'dark'] : ['light']) {
        const context = await browser.newContext({ viewport: { width, height: 844 }, colorScheme: theme, deviceScaleFactor: shots ? 2 : 1 });
        await context.route('https://fonts.googleapis.com/**', (r) => r.abort());
        await context.route('https://fonts.gstatic.com/**', (r) => r.abort());
        const page = await context.newPage();
        await page.goto(origin + url, { waitUntil: 'load' });
        if (theme === 'light') result[url][width] = await page.evaluate(() => {
          const main = document.querySelector('main') || document.body;
          return {
            height: document.documentElement.scrollHeight,
            words: (main.innerText.match(/\S+/g) || []).length,
            links: document.querySelectorAll('a[href]').length,
            mainLinks: main.querySelectorAll('a[href]').length,
            nav: document.querySelectorAll('header nav a[href]').length,
            footerLinks: document.querySelectorAll('footer a[href]').length,
            sections: main.querySelectorAll('h2').length,
            overflow: document.documentElement.scrollWidth > window.innerWidth,
          };
        });
        if (shots) {
          fs.mkdirSync(shots, { recursive: true });
          const name = (url.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'front') + `-${width}-${theme}.png`;
          await page.screenshot({ path: path.join(shots, name), fullPage: true });
        }
        await context.close();
      }
    }
  }
} finally {
  await browser.close();
  server.close();
}
console.log(JSON.stringify(result, null, 2));
// --check: the front page's height at 390 px against site/budgets.json.
if (check && result['/']) {
  const budgets = JSON.parse(fs.readFileSync(path.join(site, 'budgets.json'), 'utf8'));
  const h = result['/'][390].height, max = budgets.front.heightAt390;
  console.error(`front page height at 390 px: ${h} (budget ${max})`);
  if (h > max && budgets.enforce) process.exit(1);
}
