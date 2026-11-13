// The front page's budget (site/budgets.json), measured from the built page.
// Skipped when the site has not been built. While "enforce" is false the
// measurements are printed and the test passes, so the budget is on record
// before the page that meets it lands.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const budgets = JSON.parse(fs.readFileSync(path.join(site, 'budgets.json'), 'utf8'));
const built = path.join(site, '_site', 'index.html');

export function measureFront(html) {
  const part = (tag) => (html.match(new RegExp(`<${tag}[\\s>][\\s\\S]*?</${tag}>`)) || [''])[0];
  const text = (s) => s.replace(/<(script|style)[\s\S]*?<\/\1>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&[a-z#0-9]+;/gi, ' ');
  const links = (s) => (s.match(/<a\s[^>]*href=/g) || []).length;
  const header = part('header');
  return {
    mainWords: (text(part('main')).match(/\S+/g) || []).length,
    links: links(html),
    headerNav: links((header.match(/<nav[\s\S]*?<\/nav>/) || [''])[0]),
    footerLinks: links(part('footer')),
  };
}

test('front page budget', { skip: !fs.existsSync(built) && 'site not built' }, () => {
  const got = measureFront(fs.readFileSync(built, 'utf8'));
  const over = Object.entries(got).filter(([k, v]) => budgets.front[k] !== undefined && v > budgets.front[k]).map(([k, v]) => `${k} ${v} > ${budgets.front[k]}`);
  console.log(`front page: ${JSON.stringify(got)}${over.length ? `; over budget: ${over.join(', ')}` : ''}`);
  if (budgets.enforce) assert.deepEqual(over, [], 'the front page is over its budget (site/budgets.json)');
});
