// The reader's content model (lib/model.js): every released piece and essay
// has a topic label, a summary, a status, a home and a next step.
import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyModel, statusOf } from '../lib/model.js';
import { scanRepo } from '../lib/repo.js';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('status: released pieces and essays are reviewed, drafts and records provisional', () => {
  assert.equal(statusOf({ section: 'articles', status: 'released' }), 'reviewed');
  assert.equal(statusOf({ essay: true }), 'reviewed');
  assert.equal(statusOf({ section: 'articles', draft: true }), 'provisional');
  assert.equal(statusOf({ section: 'studies' }), 'provisional');
});

test('next: the following piece in order, else the home; essays find their investigation', () => {
  const inv = { title: 'Inv', url: '/investigations/inv/', pieces: [{ path: 'essays/a.md', title: 'A', url: '/essays/a/' }, { path: 'essays/b.md', title: 'B', url: '/essays/b/' }] };
  const a = { path: 'essays/a.md', essay: true, title: 'A', url: '/essays/a/' };
  const b = { path: 'essays/b.md', essay: true, title: 'B', url: '/essays/b/' };
  const c = { path: 'articles/c.md', section: 'articles', title: 'C', url: '/articles/c/', status: 'released', context: {} };
  applyModel({ pieces: [c], essays: [a, b], investigations: [inv], labels: new Map([['articles/c.md', 'Topic']]) });
  assert.deepEqual(a.reader.next, { title: 'B', url: '/essays/b/', kind: 'piece' });
  assert.equal(b.reader.next.kind, 'home');
  assert.equal(b.reader.home.url, '/investigations/inv/');
  assert.equal(c.reader.home.url, '/articles/');
  assert.equal(c.reader.label, 'Topic');
});

test('every released piece and essay in the repository has the whole model', () => {
  const repo = scanRepo(root);
  const missing = repo.warnings.filter((w) => w.includes('no topic label')).map((w) => w.split(':')[0] + ': label');
  for (const p of [...repo.pieces, ...repo.releasedEssays]) {
    if (p.draft || (p.status && p.status !== 'released')) continue;
    const m = p.reader || {};
    for (const field of ['summary', 'status']) if (!m[field]) missing.push(`${p.path}: ${field}`);
    if (!m.home?.url) missing.push(`${p.path}: home`);
    if (!m.next?.url) missing.push(`${p.path}: next`);
  }
  assert.deepEqual(missing, [], 'add a label in site/sections.md (labels: path | label), or the missing field');
});
