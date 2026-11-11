import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
test('current catalogue admits new work, excludes unreleased pieces and withholds changed-source summaries',()=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'knowledge-live-'));
 const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']});
 const write=(p,s)=>{fs.mkdirSync(path.dirname(path.join(root,p)),{recursive:true});fs.writeFileSync(path.join(root,p),s);};
 const commit=()=>{git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture','commit','-m','Fixture source');return git('rev-parse','HEAD').trim();};
 try{
  git('init');write('site/sections.md','# Labels\n');
  write('studies/LH999/LH999.md','# Fixture question\n\nFirst retained answer.\n');
  for(const state of ['released','draft','withdrawn'])write(`articles/${state}.md`,`published: 2026-11-10\nstatus: ${state}\nsummary: Fixture summary\n\n# ${state}\n\nFixture text.\n`);
  const sha=commit();write('notes/knowledge-lineage/curation-ref.json',JSON.stringify({input_commit:sha}));
  write('notes/knowledge-lineage/backfill-a.json',JSON.stringify([{path:'studies/LH999/LH999.md',question:'Fixture question',summary:'A retained answer.',limit:'Fixture only.',state:'Record available',evidence:[{label:'Answer',passage:'First retained answer.'}]}]));
  const run=(...args)=>execFileSync(process.execPath,[path.join(repo,'scripts/lineage/overview.mjs'),'--root',root,...args],{encoding:'utf8'});
  run();const snapshot=JSON.parse(fs.readFileSync(path.join(root,'notes/knowledge-lineage/overview.json')));
  assert.equal(snapshot.nodes.filter(n=>n.kind==='finding').length,1);
  assert.ok(snapshot.nodes.find(n=>n.kind==='study').explanation);
  write('studies/LH999/LH999.md','# Fixture question\n\nFirst retained answer.\n\nLater evidence changes its interpretation.\n');
  write('studies/LH998/brief.md','# A new question\n\nA protocol without results.\n');commit();run('--live');
  const live=JSON.parse(fs.readFileSync(path.join(root,'site/.generated/knowledge-map.json')));
  assert.equal(live.counts.studies,2);assert.notEqual(live.input_commit,sha);
  const old=live.nodes.find(n=>n.path==='studies/LH999/LH999.md');assert.equal(old.needs_review,true);assert.equal(old.explanation,undefined);
  assert.deepEqual(live.stale_annotations,['studies/LH999/LH999.md']);
  assert.equal(JSON.parse(fs.readFileSync(path.join(root,'notes/knowledge-lineage/overview.json'))).input_commit,sha);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
