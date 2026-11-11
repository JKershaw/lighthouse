import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { loadKnowledgeMap } from '../lib/knowledge-map.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const data=JSON.parse(fs.readFileSync(path.join(root,'notes/knowledge-lineage/overview.json')));

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
 const view=loadKnowledgeMap(root);assert.equal(view.groups.length,3);assert.equal(view.unassignedNodes.length,10);
});

test('every study has a bounded explanation with exact supporting passages and every item has a route',()=>{
 const studies=data.nodes.filter(n=>n.kind==='study');assert.equal(studies.length,49);
 for(const n of studies){
  assert.ok(n.explanation?.question&&n.explanation.summary&&n.explanation.limit,n.id);
  assert.ok(['Record available','Protocol only','Interim record','Closed'].includes(n.explanation.state));
  const raw=execFileSync('git',['show',`${data.input_commit}:${n.path}`],{cwd:root,encoding:'utf8'});
  for(const e of n.explanation.evidence)assert.ok(raw.includes(e.passage),n.id);
 }
 const view=loadKnowledgeMap(root);assert.equal(view.recordPages.length,70);
 assert.equal(new Set(view.recordPages.map(n=>n.mapUrl)).size,70);
 assert.equal(data.review_archive.length,67);assert.equal(studies.reduce((n,s)=>n+s.checkpoints.length,0),79);
});
