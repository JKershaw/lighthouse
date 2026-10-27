import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { writeOfflineFiles, scopePath } from '../lib/offline.js';

test('offline shell follows the build, changes with content and supports a Pages prefix', () => {
  const output = fs.mkdtempSync(path.join(os.tmpdir(), 'lighthouse-offline-'));
  try {
    for (const [file, content] of Object.entries({
      'index.html': 'home', 'articles/index.html': 'articles', 'watch/index.html': 'watch',
      'articles/story/index.html': 'story', 'offline/index.html': 'offline',
      'assets/fonts/font.woff2': 'font', 'assets/site.css': 'css', 'assets/fonts/LICENSE.md': 'licence',
    })) {
      fs.mkdirSync(path.dirname(path.join(output, file)), { recursive: true });
      fs.writeFileSync(path.join(output, file), content);
    }
    const config = writeOfflineFiles(output, '/lighthouse', '/* worker */');
    assert.deepEqual(config.pages, ['/lighthouse/', '/lighthouse/offline/', '/lighthouse/articles/', '/lighthouse/watch/']);
    assert.ok(config.assets.includes('/lighthouse/assets/fonts/font.woff2'));
    assert.ok(!config.assets.some((url) => url.endsWith('.md')));
    assert.equal(writeOfflineFiles(output, '/lighthouse/', '/* worker */').version, config.version);
    fs.writeFileSync(path.join(output, 'articles/story/index.html'), 'revised story');
    assert.notEqual(writeOfflineFiles(output, '/lighthouse/', '/* worker */').version, config.version);
    const manifest = JSON.parse(fs.readFileSync(path.join(output, 'manifest.webmanifest')));
    assert.equal(manifest.start_url, '/lighthouse/');
    assert.equal(manifest.scope, '/lighthouse/');
    assert.deepEqual(manifest.icons.map((icon) => icon.sizes), ['192x192', '512x512']);
    assert.ok(manifest.icons.every((icon) => icon.src.startsWith('/lighthouse/')));
    assert.equal(scopePath('/'), '/');
    assert.equal(scopePath('lighthouse///'), '/lighthouse/');
  } finally { fs.rmSync(output, { recursive: true, force: true }); }
});
