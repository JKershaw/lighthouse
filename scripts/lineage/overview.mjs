#!/usr/bin/env node
// Offline catalogue of a declared repository boundary. Links never imply support.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHeader, headerField } from '../../site/lib/header.js';
import { pageUrl, pieceInfo, inShortOf } from '../../site/lib/repo.js';

const rootArg=process.argv.indexOf('--root');
const root=rootArg>=0?path.resolve(process.argv[rootArg+1]):path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const dir=path.join(root,'notes/knowledge-lineage');
const refFile=fs.existsSync(path.join(dir,'curation-ref.json'))?'curation-ref.json':'baseline.json';
const frozen=JSON.parse(fs.readFileSync(path.join(dir,refFile))).input_commit;
const live=process.argv.includes('--live');
const base=live?execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim():frozen;
const stale=[];
const git=(...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'});
const all=git('ls-tree','-r','--name-only',base).trim().split('\n');
const inputs={};
const read=p=>{const s=git('show',`${base}:${p}`);inputs[p]=createHash('sha256').update(s).digest('hex');return s;};
const plain=s=>String(s||'').replace(/\[([^\]]+)\]\([^)]+\)/g,'$1').replace(/[*_`]/g,'').replace(/^LH\d+:\s*/,'').trim();
const describe=(p,kind)=>{
  const raw=read(p),header=parseHeader(raw),body=header?.body||raw;
  const field=n=>headerField(header?.fields,n);
  const heading=body.match(/^#\s+(.+)$/m)?.[1];
  const info=['finding','essay'].includes(kind)?pieceInfo(header,body,0,0):{};
  return {id:p,path:p,url:pageUrl(p),kind,title:plain(header?.title||heading||path.basename(p,'.md')),summary:plain(field('summary')?.value||inShortOf(body).inShort||''),status:info.status||'working record',publication_date:field('published')?.value||null,investigation_id:field('investigation')?.value||null,header,body,raw};
};
const studyDirs=[...new Set(all.filter(p=>/^studies\/LH\d+\/[^/]+\.md$/.test(p)).map(p=>path.posix.dirname(p)))].sort();
const studies=studyDirs.map(d=>{const id=d.split('/')[1];return all.includes(`${d}/${id}.md`)?`${d}/${id}.md`:all.includes(`${d}/brief.md`)?`${d}/brief.md`:all.filter(p=>path.posix.dirname(p)===d&&p.endsWith('.md')).sort()[0];});
const nodes=[...all.filter(p=>/^investigations\/[^/]+\.md$/.test(p)).map(p=>describe(p,'investigation')),...studies.map(p=>describe(p,'study')),...all.filter(p=>/^articles\/[^/]+\.md$/.test(p)).map(p=>describe(p,'finding')).filter(p=>p.status==='released'),...all.filter(p=>/^essays\/[^/]+\.md$/.test(p)).map(p=>describe(p,'essay')).filter(p=>p.status==='released')];
const byPath=new Map(nodes.map(n=>[n.path,n]));
const studyByDir=new Map(nodes.filter(n=>n.kind==='study').map(n=>[path.posix.dirname(n.path),n]));
function target(from,href){
  if(/^(?:[a-z]+:|\/\/|#)/i.test(href))return null;
  const without=decodeURIComponent(href.split(/[?#]/)[0]);
  const p=path.posix.normalize(path.posix.join(without.startsWith('/')?'':path.posix.dirname(from),without.replace(/^\//,''))).replace(/\/$/,'');
  return byPath.get(p)||studyByDir.get(p)||(/^studies\/LH\d+\/(?:brief|LH\d+)\.md$/.test(p)?studyByDir.get(path.posix.dirname(p)):null);
}
function evidence(p,passage){
  const raw=read(p),line=raw.indexOf(passage);
  if(line<0)throw new Error(`Missing passage ${p}`);
  const start=raw.slice(0,line).split('\n').length;
  return {path:p,passage,line_start:start,line_end:start+passage.split('\n').length-1,sha256:inputs[p],input_commit:base,url:`https://github.com/JKershaw/lighthouse/blob/${base}/${p}#L${start}`};
}
const edges=[],seen=new Set(),unresolvedReferences=[];
function edge(from,to,predicate,passage){
  if(!to||from.id===to.id)return;
  const key=[from.id,predicate,to.id].join('|');if(seen.has(key))return;seen.add(key);
  edges.push({id:`reference-${edges.length+1}`,subject:from.id,predicate,object:to.id,status:'explicit reference',evidence:evidence(from.path,passage),scope:'A retained reference or declared membership, not verified support, influence or causation.'});
}
for(const node of nodes){
  // A study is represented once, but both its protocol and write-up may carry links.
  const pths=[node.path];
  if(node.kind==='study'){
    const brief=path.posix.dirname(node.path)+'/brief.md';if(all.includes(brief)&&brief!==node.path)pths.push(brief);
  }
  for(const p of pths){
    const raw=read(p),lines=raw.split('\n');
    for(const line of lines)for(const match of line.matchAll(/\[[^\]]+\]\(([^\s)]+)(?:\s+"[^"]*")?\)/g)){
      const found=target(p,match[1]);
      if(!found && !/^(?:[a-z]+:|\/\/|#)/i.test(match[1])) {
        const normalized=path.posix.normalize(path.posix.join(match[1].startsWith('/')?'':path.posix.dirname(p),match[1].replace(/^\//,'').split(/[?#]/)[0])).replace(/\/$/,'');
        if(/^(?:(?:articles|essays|investigations)\/[^/]+\.md|studies\/LH\d+(?:\/(?:brief|LH\d+)\.md)?)$/.test(normalized)&&!all.includes(normalized)&&!studyByDir.has(normalized))unresolvedReferences.push({from:p,target:normalized,evidence:evidence(p,line)});
      }
      if(found){
        const proxy={...node,path:p};edge(proxy,found,'links-to',line);
      }
    }
  }
  if(node.kind==='investigation')for(const fieldName of ['studies','pieces','current']){
    const field=headerField(node.header?.fields,fieldName);
    for(const item of field?.items?.length?field.items:field?.value?[field.value]:[]){
      const p=item.trim();edge(node,byPath.get(p)||studyByDir.get(path.posix.dirname(p)),'declares-'+fieldName,(fieldName==='current'?'current: ':'- ')+item);
    }
  }
  if(node.investigation_id){const inv=nodes.find(n=>n.kind==='investigation'&&headerField(n.header?.fields,'id')?.value===node.investigation_id);edge(node,inv,'declares-investigation','investigation: '+node.investigation_id);}
}
const groups=nodes.filter(n=>n.kind==='investigation').map(n=>{
 const related=new Set(edges.filter(e=>e.subject===n.id).map(e=>e.object));
 for(const e of edges.filter(e=>e.object===n.id&&e.predicate==='declares-investigation'))related.add(e.subject);
 return {id:headerField(n.header?.fields,'id')?.value,path:n.path,title:n.title,url:n.url,question:headerField(n.header?.fields,'question')?.value,attention:headerField(n.header?.fields,'attention')?.value,studies:nodes.filter(s=>s.kind==='study'&&related.has(s.id)).map(s=>s.id),pieces:nodes.filter(s=>['finding','essay'].includes(s.kind)&&related.has(s.id)).map(s=>s.id),basis:'Explicit links in the investigation, its declared lists, or a publication’s investigation metadata. Membership can overlap.'};
});
const grouped=new Set(groups.flatMap(g=>[...g.studies,...g.pieces]));
const unassigned=nodes.filter(n=>n.kind!=='investigation'&&!grouped.has(n.id)).map(n=>n.id);
let history=null;
const annotations=path.join(dir,'overview-history.json');
if(live){
 history=JSON.parse(fs.readFileSync(path.join(dir,'overview.json'),'utf8')).history;
 if(history)history.stale=[...history.nodes.flatMap(n=>n.evidence_spans),...history.edges.map(e=>e.evidence)].some(e=>!all.includes(e.path)||createHash('sha256').update(read(e.path)).digest('hex')!==e.sha256);
}else if(fs.existsSync(annotations)){
 const h=JSON.parse(fs.readFileSync(annotations));
 history={...h,nodes:h.nodes.map(n=>{
   if(!byPath.has(n.path))throw new Error(`History node outside corpus: ${n.path}`);
   return {...n,url:byPath.get(n.path).url,evidence:evidence(n.path,n.passage),evidence_spans:(n.passages||[{label:'Retained basis',passage:n.passage}]).map(p=>({label:p.label,...evidence(n.path,p.passage)}))};
 }),edges:h.edges.map(e=>({...e,evidence:evidence(e.path,e.passage)}))};
}
const labelSource=read('site/sections.md');
const labels=new Map([...labelSource.matchAll(/^- (studies\/LH\d+) \| (.+)$/gm)].map(m=>[m[1],m[2]]));
for(const n of nodes)if(n.kind==='study')n.label=labels.get(path.posix.dirname(n.path))||n.title;
const backfillFiles=['backfill-a.json','backfill-b.json','backfill-c.json'];
const backfill=backfillFiles.flatMap(name=>fs.existsSync(path.join(dir,name))?JSON.parse(fs.readFileSync(path.join(dir,name),'utf8')):[]);
for(const node of nodes){
 const curated=backfill.find(c=>c.path===node.path);
 if(curated){
  if((!live||createHash('sha256').update(node.raw).digest('hex')===JSON.parse(fs.readFileSync(path.join(dir,'overview.json'))).inputs[node.path])&&curated.evidence.every(e=>node.raw.includes(e.passage)))node.explanation={...curated,evidence:curated.evidence.map(e=>({label:e.label,...evidence(node.path,e.passage)}))};
  else {node.needs_review=true;stale.push(node.path);}
 }
 if(['finding','essay'].includes(node.kind))node.summary=labelSource.split('\n').find(line=>line.startsWith('- '+node.path+' | '))?.split(' | ').slice(1).join(' | ')||node.summary;
 node.review_records=[];
 for(const match of node.raw.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  const rel=path.posix.normalize(path.posix.join(path.posix.dirname(node.path),match[1].split('#')[0]));
  if(/^notes\/R-[^/]+\.md$/.test(rel)&&all.includes(rel)&&!node.review_records.some(r=>r.path===rel)){
   const text=read(rel);node.review_records.push({path:rel,title:plain(text.match(/^# (.+)$/m)?.[1]||'Source review'),url:pageUrl(rel)});
  }
 }
 const studyDir=node.kind==='study'?path.posix.dirname(node.path):null;
 node.checkpoints=studyDir?all.filter(p=>p.startsWith(studyDir+'/checkpoints/')&&p.endsWith('.md')).map(p=>({path:p,url:pageUrl(p),title:path.basename(p,'.md')})):[];
 node.notices=[...node.raw.matchAll(/^> \*\*(Correction|Later evidence), ([^*]+)\*\*/gm)].map(m=>({kind:m[1],date:m[2]}));
}
const reviewArchive=all.filter(p=>/^notes\/R-[^/]+\.md$/.test(p)).map(p=>{const raw=read(p);return {path:p,title:plain(raw.match(/^# (.+)$/m)?.[1]||path.basename(p,'.md')),url:pageUrl(p)};});
const result={review_archive:reviewArchive,schema_version:'0.2',input_commit:base,mode:live?'current catalogue':'retained snapshot',stale_annotations:stale,generated_for:live?git('show','-s','--format=%cs',base).trim():'2026-11-10',boundary:'Every investigation declaration, study directory with a top-level Markdown lead, and released top-level finding/essay at the frozen commit. Short forms, drafts, checkpoints and raw evidence are excluded.',counts:{investigations:groups.length,studies:studyDirs.length,findings:nodes.filter(n=>n.kind==='finding').length,essays:nodes.filter(n=>n.kind==='essay').length,references:edges.length},nodes:nodes.map(({header,body,raw,...n})=>n),edges,unresolved_references:unresolvedReferences,groups,unassigned,history,inputs:Object.fromEntries(Object.entries(inputs).sort())};
const output=JSON.stringify(result,null,2)+'\n',file=live?path.join(root,'site/.generated/knowledge-map.json'):path.join(dir,'overview.json');
fs.mkdirSync(path.dirname(file),{recursive:true});
if(process.argv.includes('--check')){if(!fs.existsSync(file)||fs.readFileSync(file,'utf8')!==output)throw new Error('Overview differs; regenerate with node scripts/lineage/overview.mjs');}
else fs.writeFileSync(file,output);
console.log(JSON.stringify({counts:result.counts,unassigned:unassigned.length,history:history?.nodes.length||0}));
