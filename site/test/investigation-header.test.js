// The top of an investigation page, rendered: studies under way are listed
// open with a count, so screen readers and browser-driven agents meet them
// without expanding anything; finished or paused ones are collapsed, counted.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import nunjucks from 'nunjucks';

const includes = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../_includes');

function render(now) {
  const env = new nunjucks.Environment(new nunjucks.FileSystemLoader(includes), { autoescape: true });
  env.addFilter('investigationNow', () => now);
  env.addFilter('mdInline', (s) => s);
  return env.render('investigation-header.njk', { doc: { investigation: { question: 'Where does it go?', started: '26 September 2026', pieces: [] } }, repo: {}, schedule: {} });
}

const base = { answer: { title: 'No reviewed finding yet', url: '', status: 'provisional', kind: '' }, reading: null, waiting: [], pieces: 0, latestRead: null, next: null, running: 0 };
const study = (id, extra) => ({ id, title: `Study ${id}`, url: `/studies/${id}/`, running: false, active: false, scheduled: false, waiting: [], latest: null, ...extra });
const details = (html) => [...html.matchAll(/<details class="inv-studies"([^>]*)>\s*<summary>([^<]*)<\/summary>([\s\S]*?)<\/details>/g)]
  .map((m) => ({ open: /\bopen\b/.test(m[1]), summary: m[2].trim(), body: m[3] }));

test('studies under way are listed open with a count; earlier ones collapsed and counted', () => {
  const html = render({ ...base, studies: 3, underway: 2, studyList: [
    study('LH002', { active: true, scheduled: true, latest: { day: '18 November', url: '/studies/LH002/checkpoints/2026-11-18/' } }),
    study('LH003', { active: true, waiting: [{ id: 'gate' }] }),
    study('LH001'),
  ] });
  assert.match(html, /3 studies, 2 under way/);
  const [underway, earlier, extra] = details(html);
  assert.equal(extra, undefined);
  assert.deepEqual([underway.open, underway.summary], [true, 'Studies under way (2)']);
  assert.match(underway.body, /Study LH002<\/a> <span class="when">scheduled · <a href="\/studies\/LH002\/checkpoints\/2026-11-18\/">latest read 18 November/);
  assert.match(underway.body, /Study LH003<\/a> <span class="when">waiting</);
  assert.doesNotMatch(underway.body, /LH001/);
  assert.deepEqual([earlier.open, earlier.summary], [false, 'Earlier studies (1, finished or paused)']);
  assert.match(earlier.body, /Study LH001<\/a> <span class="when">finished or paused</);
});

test('with nothing under way the one list is collapsed but says what it holds', () => {
  const html = render({ ...base, studies: 1, underway: 0, studyList: [study('LH001')] });
  assert.match(html, /1 study, 0 under way/);
  const lists = details(html);
  assert.equal(lists.length, 1);
  assert.deepEqual([lists[0].open, lists[0].summary], [false, 'The studies (1, finished or paused)']);
});

test('a study a run holds now says so', () => {
  const html = render({ ...base, studies: 1, underway: 1, studyList: [study('LH001', { active: true, running: true, scheduled: true })] });
  assert.match(details(html)[0].body, /<span class="when">in progress now</);
});
