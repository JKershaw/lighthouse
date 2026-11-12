import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { loadKnowledgeMap } from '../lib/knowledge-map.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const data=JSON.parse(fs.readFileSync(path.join(root,'notes/knowledge-lineage/overview.json')));

// These assertions describe the frozen corpus, regardless of a local live build.
function snapshotView() {
 const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'knowledge-snapshot-'));
 try {
  const dir=path.join(fixture,'notes/knowledge-lineage');fs.mkdirSync(dir,{recursive:true});
  for(const name of ['overview.json','history-wide.svg','history-mobile.svg'])fs.copyFileSync(path.join(root,'notes/knowledge-lineage',name),path.join(dir,name));
  return loadKnowledgeMap(fixture);
 } finally { fs.rmSync(fixture,{recursive:true,force:true}); }
}

test('the overview keeps the complete frozen catalogue reachable, including unassigned work',()=>{
 assert.deepEqual({...data.counts,references:undefined},{investigations:3,studies:49,findings:18,essays:3,references:undefined});
 const ids=new Set(data.nodes.map(n=>n.id));assert.equal(ids.size,data.nodes.length);
 const reachable=new Set([...data.groups.map(g=>g.path),...data.groups.flatMap(g=>[...g.studies,...g.pieces]),...data.unassigned]);
 assert.deepEqual(reachable,ids);
 assert.equal(data.unassigned.length,10);
 assert.ok(data.nodes.every(n=>n.status!=='draft'&&!n.path.includes('/short/')&&!n.path.includes('/checkpoints/')));
 assert.ok(data.edges.every(e=>e.predicate==='links-to'||e.predicate.startsWith('declares-')));
 assert.ok(data.edges.every(e=>ids.has(e.subject)&&ids.has(e.object)));
});

test('overview references and selected history are grounded in the frozen original passages',()=>{
 const files=new Map(Object.keys(data.inputs).map(p=>[p,execFileSync('git',['show',`${data.input_commit}:${p}`],{cwd:root,encoding:'utf8'})]));
 for(const e of [...data.edges,...data.history.edges,...data.history.nodes,...data.history.nodes.flatMap(n=>n.evidence_spans.map(e=>({id:n.id+' '+e.label,evidence:e})))]){
  const p=e.evidence;assert.ok(files.get(p.path).includes(p.passage),e.id);
  assert.ok(files.get(p.path).split('\n').slice(p.line_start-1,p.line_end).join('\n').includes(p.passage),e.id);
 }
 const historyIds=new Set(data.history.nodes.map(n=>n.id));
 assert.equal(historyIds.size,8);
 assert.ok(data.history.edges.every(e=>historyIds.has(e.subject)&&historyIds.has(e.object)));
 assert.ok(data.history.nodes.every(n=>data.nodes.some(x=>x.id===n.path&&x.kind==='finding')));
 const view=snapshotView();assert.equal(view.groups.length,3);assert.equal(view.unassignedNodes.length,10);
});

test('every study has a bounded explanation with exact supporting passages and every item has a route',()=>{
 const studies=data.nodes.filter(n=>n.kind==='study');assert.equal(studies.length,49);
 for(const n of studies){
  assert.ok(n.explanation?.question&&n.explanation.summary&&n.explanation.limit,n.id);
  assert.ok(['Record available','Protocol only','Interim record','Closed'].includes(n.explanation.state));
  const raw=execFileSync('git',['show',`${data.input_commit}:${n.path}`],{cwd:root,encoding:'utf8'});
  for(const e of n.explanation.evidence)assert.ok(raw.includes(e.passage),n.id);
 }
 const view=snapshotView();assert.equal(view.recordPages.length,70);
 assert.equal(new Set(view.recordPages.map(n=>n.mapUrl)).size,70);
 assert.equal(data.review_archive.length,67);assert.equal(studies.reduce((n,s)=>n+s.checkpoints.length,0),79);
});

test('the map displays new investigations and their study routes beyond the original three',()=>{
 const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'knowledge-groups-'));
 try {
  const dir=path.join(fixture,'notes/knowledge-lineage');fs.mkdirSync(dir,{recursive:true});
  const study={id:'studies/LH999/brief.md',path:'studies/LH999/brief.md',kind:'study',url:'/studies/LH999/brief/'};
  const group={id:'future-inquiry',title:'Another outward question',question:'What changes?',url:'/investigations/future-inquiry/',path:'investigations/future-inquiry.md',studies:[study.id],pieces:[]};
  fs.writeFileSync(path.join(dir,'overview.json'),JSON.stringify({generated_for:'2026-11-12',nodes:[study],edges:[],groups:[group],unassigned:[]}));
  for(const name of ['history-wide.svg','history-mobile.svg'])fs.writeFileSync(path.join(dir,name),'<svg/>');
  const view=loadKnowledgeMap(fixture);
  assert.deepEqual(view.groups.map(g=>g.id),['future-inquiry']);
  assert.equal(view.groups[0].title,group.title);assert.equal(view.groups[0].start,group.url);
  assert.equal(view.groups[0].studyNodes[0].mapUrl,'/map/knowledge-lineage/records/LH999/');
 } finally { fs.rmSync(fixture,{recursive:true,force:true}); }
});
