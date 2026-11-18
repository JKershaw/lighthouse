// Where an investigation stands, from hand-built schedule rows: the answer and
// its status, the newest piece beside a provisional answer, the next read and
// how a waiting one is labelled, and what counts as under way.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { investigationNow } from '../lib/investigation-now.js';

const r = (id, study, state, extra = {}) => ({ id, study, state, kind: 'observe', readiness: 'ok', earliest: '', updated: '', ref: '', reasons: [], task: id, ...extra });
const studies = [{ id: 'LH001', url: '/studies/LH001/', lead: { title: 'One' }, checkpoints: [] }, { id: 'LH002', url: '/studies/LH002/', lead: { title: 'Two' }, checkpoints: [] }];
const inv = (extra = {}) => ({ studies: [{ study: 'LH001' }, { study: 'LH002' }], pieces: [], ...extra });

test('no investigation, no account', () => {
  assert.equal(investigationNow(null, {}, {}), null);
});

test('a current account is the answer, reviewed; otherwise the newest piece is shown as reading', () => {
  const repo = { studies, byPath: {
    'articles/a.md': { title: 'The account', url: '/articles/a/', pubTime: 1 },
    'articles/b.md': { title: 'Newer piece', url: '/articles/b/', pubTime: 2 },
    'essays/c.md': { title: 'An essay', url: '/essays/c/', pubTime: 3, essay: true },
  } };
  const schedule = { rows: [], today: '2026-11-18' };
  const withCurrent = investigationNow(inv({ current: { path: 'articles/a.md' }, pieces: [{ path: 'articles/b.md' }] }), repo, schedule);
  assert.deepEqual(withCurrent.answer, { title: 'The account', url: '/articles/a/', status: 'reviewed', kind: 'Current account' });
  assert.equal(withCurrent.reading, null);
  const without = investigationNow(inv({ pieces: [{ path: 'articles/b.md' }, { path: 'essays/c.md' }, { path: 'articles/a.md', draft: true }] }), repo, schedule);
  assert.equal(without.answer.status, 'provisional');
  assert.deepEqual(without.reading, { title: 'An essay', url: '/essays/c/', kind: 'Latest essay' });
  assert.equal(without.pieces, 2);
});

test('the next read is dated, today when due, and labelled waiting when it waits', () => {
  const at = (rows) => investigationNow(inv(), { studies, byPath: {} }, { rows, today: '2026-11-18' }).next;
  assert.equal(at([r('later', 'LH001', 'calendar_wait', { earliest: '2026-11-21' })]).day, '21 November');
  assert.equal(at([r('due', 'LH001', 'ready', { earliest: '2026-11-18' })]).day, 'today');
  const blocked = at([r('held', 'LH002', 'blocked', { earliest: '2026-11-25', reasons: ['Needs a report'] })]);
  assert.deepEqual([blocked.day, blocked.waiting, blocked.reason], ['25 November (waiting)', true, 'Needs a report']);
  assert.equal(at([r('held-now', 'LH002', 'dependency_wait', { reasons: ['After the read'] })]).day, 'waiting');
  assert.equal(at([r('analysis', 'LH001', 'ready', { kind: 'analyse' })]), null, 'only observation rows are reads');
});

test('finished, cancelled and invalid rows do not make a study under way', () => {
  const now = investigationNow(inv(), { studies, byPath: {} }, { rows: [
    r('done', 'LH001', 'done', { updated: '2026-11-17T10:00:00Z' }),
    r('cancelled', 'LH001', 'cancelled'),
    r('broken', 'LH002', 'ready', { readiness: 'invalid' }),
  ], today: '2026-11-18' });
  assert.equal(now.underway, 0);
  assert.equal(now.latestRead.day, '17 November');
  assert.deepEqual(now.studyList.map((s) => [s.id, s.active]), [['LH001', false], ['LH002', false]]);
});
