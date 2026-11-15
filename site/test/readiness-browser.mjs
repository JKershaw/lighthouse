// Browser acceptance of the built queue. No requests leave the local server.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright';

const root = path.resolve('site/_site');
const prefix = (process.env.PATH_PREFIX || '').replace(/\/$/, '');
const model = JSON.parse(execFileSync('python3', ['schedule/check.py', '--json'], { encoding: 'utf8' }));
assert.equal(model.valid, true);
const server = createServer((request, response) => {
  let pathname = decodeURIComponent(new URL(request.url, 'http://local').pathname);
  if (prefix) {
    if (!pathname.startsWith(prefix + '/')) { response.writeHead(404).end(); return; }
    pathname = pathname.slice(prefix.length);
  }
  let file = path.resolve(root, '.' + pathname);
  if (file !== root && !file.startsWith(root + path.sep)) { response.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { response.writeHead(404).end(); return; }
  const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
  response.setHeader('content-type', types[path.extname(file)] || 'application/octet-stream');
  response.end(fs.readFileSync(file));
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
try {
  browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  const origin = `http://127.0.0.1:${server.address().port}`;
  const results = [];
  for (const width of [390, 1280]) for (const theme of ['light', 'dark']) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, colorScheme: theme, javaScriptEnabled: false });
    await page.route('**/*', route => route.request().url().startsWith(origin + '/') ? route.continue() : route.abort());
    const response = await page.goto(origin + prefix + '/schedule/');
    assert.equal(response.status(), 200);
    assert.equal(await page.getByRole('heading', { name: 'Schedule', exact: true }).count(), 1);
    for (const [title, ids] of [['Ready now', model.groups.ready], ['Ready, past deadline', model.groups.overdue]]) {
      const heading = page.getByRole('heading', { name: title, exact: true });
      assert.equal(await heading.count(), ids.length ? 1 : 0);
      if (ids.length) {
        const actual = await heading.locator('xpath=following-sibling::ul[1]').locator('li > strong').allTextContents();
        assert.deepEqual(actual, ids, title);
      }
    }
    assert.equal(await page.getByRole('heading', { name: 'Invalid queue', exact: true }).count(), 0);
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Schedule overflow at ${width} ${theme}`);
    await page.goto(origin + prefix + '/investigations/ai-cost-and-spread/');
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Investigation overflow at ${width} ${theme}`);
    results.push({ width, theme, ready: model.groups.ready.length, overdue: model.groups.overdue.length, noJavaScript: true });
    await page.close();
  }
  console.log(JSON.stringify(results));
} finally {
  await browser?.close();
  server.close();
}
