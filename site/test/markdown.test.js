// The Markdown plugin turns the repository's links into the site's: these
// cases pin how a link is resolved, when it is reported as broken, how bare
// paths in records become links, and that heading ids match GitHub's.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import MarkdownIt from 'markdown-it';
import lighthousePlugin, { resolveTarget, slugify, unresolved } from '../lib/markdown.js';
import { sourceUrl } from '../lib/repo.js';

function fakeRepo() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'lighthouse-md-'));
  fs.mkdirSync(path.join(root, 'studies/LH001/data'), { recursive: true });
  fs.writeFileSync(path.join(root, 'studies/LH001/data/rows.csv'), 'a\n');
  return {
    root,
    byPath: {
      'README.md': { url: '/' },
      'studies/LH001/LH001.md': { url: '/studies/LH001/LH001/' },
      'studies/LH001/brief.md': { url: '/studies/LH001/brief/' },
      'notes/R-0001.md': { url: '/notes/R-0001/' },
    },
    fileSet: new Set(['studies/LH001/fig.svg']),
    siteDirs: new Set(['studies/LH001']),
  };
}

test('slugify gives GitHub heading ids', () => {
  assert.equal(slugify('Where things stand'), 'where-things-stand');
  assert.equal(slugify("Week one: what's known?"), 'week-one-whats-known');
  assert.equal(slugify('  LH001 · 0.2  '), 'lh001--02');
});

test('resolveTarget maps repository links to pages, images, folders and source', () => {
  const repo = fakeRepo();
  try {
    const from = 'studies/LH001/LH001.md';
    assert.deepEqual(resolveTarget(repo, from, 'https://example.test/x'), { href: 'https://example.test/x' });
    assert.deepEqual(resolveTarget(repo, from, '#limits'), { href: '#limits' });
    assert.deepEqual(resolveTarget(repo, from, 'brief.md#question'), { href: '/studies/LH001/brief/#question' });
    assert.deepEqual(resolveTarget(repo, from, '../../notes/R-0001.md'), { href: '/notes/R-0001/' });
    assert.deepEqual(resolveTarget(repo, from, '/notes/R-0001.md'), { href: '/notes/R-0001/' });
    assert.deepEqual(resolveTarget(repo, from, 'fig.svg', { image: true }), { href: '/studies/LH001/fig.svg' });
    assert.deepEqual(resolveTarget(repo, from, 'missing.png', { image: true }), { missing: true });
    assert.deepEqual(resolveTarget(repo, 'README.md', 'studies/LH001/'), { href: '/studies/LH001/' });
    assert.deepEqual(resolveTarget(repo, from, 'data/rows.csv'), { href: sourceUrl('studies/LH001/data/rows.csv') });
    assert.deepEqual(resolveTarget(repo, from, 'data/'), { href: sourceUrl('studies/LH001/data', true) });
    assert.deepEqual(resolveTarget(repo, from, '../../../outside.md'), { missing: true });
    assert.deepEqual(resolveTarget(repo, from, 'nowhere.md'), { missing: true });
    assert.deepEqual(resolveTarget(repo, from, 'brief%2Emd'), { href: '/studies/LH001/brief/' });
  } finally {
    fs.rmSync(repo.root, { recursive: true, force: true });
  }
});

test('the plugin rewrites links, marks broken ones, links bare paths and numbers repeated headings', () => {
  const repo = fakeRepo();
  try {
    const md = new MarkdownIt().use(lighthousePlugin, { getRepo: () => repo });
    const env = { page: { inputPath: path.join(repo.root, 'studies/LH001/LH001.md') } };
    const before = unresolved.length;
    const html = md.render([
      '## Limits', '', '## Limits', '',
      'See [the brief](brief.md) and [a lost note](gone.md).', '',
      'Reviewed in notes/R-0001.md and studies/LH001/, not in notes/R-9999.md.', '',
      'This record, LH001.md, is not linked to itself.',
    ].join('\n'), env);
    assert.match(html, /<h2 id="limits">Limits<\/h2>/);
    assert.match(html, /<h2 id="limits-1">Limits<\/h2>/);
    assert.match(html, /<a href="\/studies\/LH001\/brief\/">the brief<\/a>/);
    assert.match(html, /<span class="unresolved" title="Link in the source does not resolve: gone.md">a lost note<\/span>/);
    assert.deepEqual(unresolved.slice(before), [{ from: 'studies/LH001/LH001.md', target: 'gone.md' }]);
    assert.match(html, /<a href="\/notes\/R-0001\/">notes\/R-0001.md<\/a>/);
    assert.match(html, /<a href="\/studies\/LH001\/">studies\/LH001\/<\/a>/);
    assert.match(html, /not in notes\/R-9999.md\./, 'an unknown bare path stays text');
    assert.doesNotMatch(html, /<a [^>]*>LH001.md<\/a>/);
  } finally {
    fs.rmSync(repo.root, { recursive: true, force: true });
  }
});

test('a title-led block of fields renders as a definition list', () => {
  const md = new MarkdownIt().use(lighthousePlugin, { getRepo: () => null });
  const html = md.render('title: A question\nstatus: open\nsources:\n- S1\n- S2\n');
  assert.match(html, /<dl class="meta fields">/);
  assert.match(html, /<dt>status<\/dt><dd>open<\/dd>/);
  assert.match(html, /<dt>sources<\/dt><dd><ul><li>S1<\/li><li>S2<\/li><\/ul><\/dd>/);
});
