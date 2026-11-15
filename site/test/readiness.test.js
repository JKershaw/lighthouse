// Contract tests: the site's adapter retains the offline model's decisions.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import nunjucks from 'nunjucks';
import { buildSchedule, latestRun } from '../lib/schedule.js';
import { investigationNow } from '../lib/investigation-now.js';

const FIELDS = 'id,study,task,earliest,latest,status,updated,by,ref,note,kind,depends_on,run_id'.split(',');
const CLI = fileURLToPath(new URL('../../schedule/check.py', import.meta.url));
const NOW = new Date('2026-11-14T12:00:00Z');
const cell = (s) => `"${String(s || '').replaceAll('"', '""')}"`;
const row = (id, extra = {}) => ({ id, study: 'LH001', task: id, status: 'open', kind: 'analyse', ...extra });
const csv = (rows) => [FIELDS.join(','), ...rows.map((r) => FIELDS.map((f) => cell(r[f])).join(','))].join('\n') + '\n';
function fixture(table, fn) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'lighthouse-readiness-site-'));
  try {
    fs.mkdirSync(path.join(root, 'schedule'));
    fs.writeFileSync(path.join(root, 'schedule/due.csv'), table);
    return fn(root);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
function engine(root) {
  const result = spawnSync('python3', [CLI, '--root', root, '--now', NOW.toISOString(), '--json'], { encoding: 'utf8' });
  assert.ifError(result.error);
  return JSON.parse(result.stdout);
}
function sameDecisions(site, model) {
  const project = (r) => Object.fromEntries([...FIELDS, 'state', 'readiness', 'actionable', 'reasons', 'unmet_dependencies', 'calendar_state', 'stale'].map((k) => [k, r[k]]));
  assert.equal(site.valid, model.valid);
  assert.equal(site.evaluatedAt, model.evaluated_at);
  assert.deepEqual(site.diagnostics, model.diagnostics);
  assert.deepEqual(site.groups, model.groups);
  assert.deepEqual(site.rows.map(project), model.rows.map(project));
  assert.deepEqual(site.ready.map((r) => r.id), model.groups.ready);
  assert.deepEqual(site.overdue.map((r) => r.id), model.groups.overdue);
}

test('site conforms to the shared frozen readiness v1 fixture', () => {
  const root = fileURLToPath(new URL('../../schedule/fixtures/readiness-v1/', import.meta.url));
  const expected = JSON.parse(fs.readFileSync(path.join(root, 'expected.json'), 'utf8'));
  sameDecisions(buildSchedule(root, NOW), expected);
});

test('site and CLI share dependency, open-ended, calendar and stale-claim decisions', () => {
  fixture(csv([
    row('evidence', { kind: 'observe', status: 'done', updated: '2026-11-13', ref: 'https://example.test/evidence' }),
    row('frontier', { depends_on: 'evidence' }),
    row('future-read', { kind: 'observe', earliest: '2026-12-01', latest: '2026-12-02' }),
    row('waiting-final', { depends_on: 'future-read', latest: '2026-11-13' }),
    row('ready-late', { depends_on: 'evidence', latest: '2026-11-13' }),
    row('manual', { status: 'blocked', note: 'Substantive report still unavailable' }),
    row('old-claim', { status: 'running', updated: '2026-11-14T05:59:59Z', by: 'test owner', run_id: 'test-run-1' }),
  ]), (root) => {
    const site = buildSchedule(root, NOW);
    sameDecisions(site, engine(root));
    assert.equal(site.valid, true, site.diagnostics.join('\n'));
    assert.deepEqual(site.ready.map((r) => r.id), ['frontier']);
    assert.deepEqual(site.overdue.map((r) => r.id), ['ready-late']);
    const waiting = site.rows.find((r) => r.id === 'waiting-final');
    assert.equal(waiting.readiness, 'dependency_wait');
    assert.equal(waiting.calendar_state, 'overdue');
    assert.deepEqual(waiting.unmet_dependencies, ['future-read']);
    assert.match(waiting.reasons.join(' '), /future-read/);
    assert.deepEqual(site.stale.map((r) => r.id), ['old-claim']);
    assert.ok(!site.attention.some((r) => r.id === 'evidence'));
    assert.ok(site.openEnded.some((r) => r.id === 'frontier'));
    assert.equal(site.rows.find((r) => r.id === 'frontier').day, '');
  });
});

test('malformed queues keep model diagnostics and never invent ready work', () => {
  for (const table of [
    'wrong,header\n',
    FIELDS.join(',') + '\na,LH001,short\n',
    FIELDS.join(',') + '\n' + Array(14).fill('extra').join(',') + '\n',
    csv([row('bad-date', { earliest: '20261114' })]),
    csv([row('unknown', { depends_on: 'missing' })]),
    csv([row('cycle-a', { depends_on: 'cycle-b' }), row('cycle-b', { depends_on: 'cycle-a' })]),
    csv([row('bad-ref', { ref: '../outside.md' })]),
  ]) fixture(table, (root) => {
    const site = buildSchedule(root, NOW);
    sameDecisions(site, engine(root));
    assert.equal(site.valid, false);
    assert.ok(site.diagnostics.length);
    assert.deepEqual(site.ready, []);
    assert.deepEqual(site.overdue, []);
    assert.ok(site.rows.every((r) => !r.actionable && r.readiness === 'invalid'));
  });
});

test('new run identity overrides free-form attribution and historical rows retain their narrative', () => {
  const rows = [
    { ...row('claimed'), status: 'done', run_id: 'run-public-2', by: 'different wording', refs: [], href: '/claimed/' },
    { ...row('owned-wait'), status: 'open', earliest: '', run_id: 'run-public-2', refs: [], href: '/wait/' },
    { ...row('setup-only'), status: 'done', run_id: '', by: 'setup run 2026-11-14T1200Z', refs: [], href: '/setup/' },
    { ...row('other-run'), status: 'done', run_id: 'run-public-20', by: 'run 2026-11-14T1200Z', refs: [], href: '/other/' },
  ];
  fixture(csv([]), (root) => {
    const run = latestRun({ started: '2026-11-14T1200Z', run_id: 'run-public-2' }, rows, root);
    assert.deepEqual(run.done.map((r) => r.id), ['claimed']);
    assert.deepEqual(run.waiting.map((r) => r.id), ['owned-wait']);
    const historical = latestRun({ started: '2026-11-14T1200Z', plain: 'The retained original account.' }, rows, root);
    assert.equal(historical.count, 0);
    assert.equal(historical.waitingCount, 0);
    assert.equal(historical.plain, 'The retained original account.');
  });
});

test('investigations count observations as reads and expose named work waits', () => {
  fixture(csv([
    row('read-then', { kind: 'observe', status: 'done', updated: '2026-11-10', ref: 'https://example.test/read' }),
    row('untyped-today', { kind: '', status: 'done', updated: '2026-11-14', ref: 'https://example.test/unknown' }),
    row('maintenance-today', { kind: 'maintain', status: 'done', updated: '2026-11-14', ref: 'https://example.test/maintenance' }),
    row('analysis-today', { kind: 'analyse', status: 'done', updated: '2026-11-14', ref: 'https://example.test/analysis' }),
    row('review-tomorrow', { kind: 'review', earliest: '2026-11-15' }),
    row('read-next', { kind: 'observe', earliest: '2026-11-17' }),
    row('final-record', { depends_on: 'read-next' }),
  ]), (root) => {
    const schedule = buildSchedule(root, NOW);
    const study = { id: 'LH001', url: '/studies/LH001/', lead: { title: 'Study one' }, checkpoints: [{ key: '2026-11-14', url: '/analysis-checkpoint/' }] };
    const now = investigationNow({ studies: [{ study: 'LH001' }], pieces: [] }, { studies: [study], byPath: {} }, schedule);
    assert.equal(now.latestRead.iso, '2026-11-10');
    assert.equal(now.studyList[0].latest.day, '10 November');
    assert.equal(now.next.id, 'read-next');
    assert.equal(now.next.day, '17 November');
    assert.equal(now.running, 0);
    assert.deepEqual(now.waiting.map((r) => r.id), ['final-record']);
    assert.match(now.waiting[0].reasons.join(' '), /read-next/);
    assert.equal(investigationNow({ studies: [{ study: 'LH001' }], pieces: [] }, { studies: [study], byPath: {} }, { ...schedule, rows: schedule.rows.filter((r) => r.kind !== 'observe') }).latestRead, null);
  });
});

test('a blocked next observation says waiting and retains its named reason', () => {
  fixture(csv([row('blocked-read', { kind: 'observe', status: 'blocked', note: 'Access permission is required' })]), (root) => {
    const schedule = buildSchedule(root, NOW);
    const inv = { studies: [{ study: 'LH001' }], pieces: [] };
    const now = investigationNow(inv, { studies: [], byPath: {} }, schedule);
    assert.equal(now.next.day, 'waiting');
    assert.equal(now.next.waiting, true);
    assert.match(now.next.reason, /Access permission is required/);
    assert.deepEqual(now.waiting.map((r) => r.id), ['blocked-read']);
  });
});

test('the schedule renders invalid diagnostics and dependency/calendar reasons without JavaScript', () => {
  const source = fs.readFileSync(new URL('../_includes/index-schedule.njk', import.meta.url), 'utf8');
  const env = new nunjucks.Environment(null, { autoescape: true });
  fixture(csv([row('waiting-final', { depends_on: 'missing', latest: '2026-11-13' })]), (root) => {
    const html = env.renderString(source, { schedule: buildSchedule(root, NOW) });
    assert.match(html, /role="alert"/);
    assert.match(html, /Invalid queue/);
    assert.match(html, /missing dependency/);
    assert.match(html, /Waiting for missing/);
    assert.match(html, /chip-overdue/);
    assert.ok(!html.includes('<h2>Ready now</h2>'));
    assert.ok(!html.includes('<h2>Ready, past deadline</h2>'));
  });
});
