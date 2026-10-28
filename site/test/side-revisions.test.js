import { test } from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {createRequire} from 'node:module';
import sideNotes from '../lib/side-notes.js';import {revisionInfo} from '../lib/revisions.js';import {parseHeader} from '../lib/header.js';
// markdown-it is Eleventy's installed Markdown engine.
const require=createRequire(import.meta.url),MarkdownIt=require('markdown-it');
test('inline side notes retain Markdown links, controls and no-script note text',()=>{
 const md=new MarkdownIt({html:false}).use(sideNotes),source=fs.readFileSync(new URL('./fixtures/markdown/side-notes.md',import.meta.url),'utf8');
 const html=md.render(source);assert.match(html,/aria-controls="side-note-1"/);assert.match(html,/id="side-note-1" role="note"/);assert.match(html,/href="legacy.md"/);assert.match(html,/hidden>1<\/button>/);assert.ok(!html.includes('^['));
 assert.ok(md.render('Broken ^[unclosed').includes('^[unclosed'));assert.ok(md.render('Nested ^[outer ^[inner]]').includes('^['));
 const a=md.render('Text.^[A note.]',{sideNotePrefix:'source-entry-a'}),b=md.render('Text.^[A note.]',{sideNotePrefix:'source-entry-b'});assert.match(a,/source-entry-a-1/);assert.match(b,/source-entry-b-1/);
});
test('status is explicit, notices and header revisions combine, and earlier editions are never invented',()=>{
 const body='> **Correction, 27 October 2026.** Changed a claim. [Earlier edition](https://example.test/v1).\n\n> **Later evidence, 23 October 2026.** More evidence, with a [source](https://example.test/source).';
 const header=parseHeader('status: released\ndeveloping: true\nnext-revision: After reviewed evidence changes.\n\n# T');
 const info=revisionInfo(header,body,[{time:Date.UTC(2026,9,24),iso:'2026-10-24',date:'24 October 2026',text:'An explicit header revision.'}]);
 assert.equal(info.displayState,'Developing');assert.equal(info.nextRevision,'After reviewed evidence changes.');assert.deepEqual(info.revisionHistory.map(r=>r.iso),['2026-10-27','2026-10-24','2026-10-23']);assert.equal(info.revisionHistory[0].earlierEdition.target,'https://example.test/v1');assert.equal(info.revisionHistory[2].earlierEdition,null);
 assert.equal(revisionInfo(null,body).displayState,'Revised');assert.equal(revisionInfo(null,'# A piece').displayState,'Released');assert.equal(revisionInfo(header,body,[],true).displayState,'Draft');assert.equal(revisionInfo(null,'Will be revised at day 30.').nextRevision,'');
});
