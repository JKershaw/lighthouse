import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildNow } from '../lib/clock.js';

test('the build clock is the real time unless LIGHTHOUSE_NOW fixes it', () => {
  const before = Date.now();
  const real = buildNow({}).getTime();
  assert.ok(real >= before && real <= Date.now());
  assert.equal(buildNow({ LIGHTHOUSE_NOW: '2026-11-19T00:05:00Z' }).toISOString(), '2026-11-19T00:05:00.000Z');
  assert.throws(() => buildNow({ LIGHTHOUSE_NOW: 'tomorrow' }), /LIGHTHOUSE_NOW is not a date/);
});
