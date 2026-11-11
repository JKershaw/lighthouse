import fs from 'node:fs';
import path from 'node:path';

const intros = {
 'software-updates': { title: 'How software updates travel', question: 'A release is available. What happens next?', state: 'Findings to explore', summary: 'Follow releases through downloads, pinned versions and build instructions.', start: '/articles/where-software-updates-go/' },
 'model-found-bugs': { title: 'When a model finds a flaw', question: 'How does a reported discovery reach defenders?', state: 'An ongoing investigation', summary: 'Keep the discovery report, fixes, disclosure dates and public signals in view.', start: '/map/knowledge-lineage/trails/#topic' },
 'ai-cost-and-spread': { title: 'AI and the shared internet', question: 'What does this activity leave behind?', state: 'Working records to explore', summary: 'Explore services closing access, exposed systems and the evidence for spread.', start: '/investigations/ai-cost-and-spread/' },
};
export function loadKnowledgeMap(root) {
 const generated=path.join(root,'site/.generated/knowledge-map.json');
 const p=fs.existsSync(generated)?generated:path.join(root,'notes/knowledge-lineage/overview.json');
 if(!fs.existsSync(p))return null;
 const data=JSON.parse(fs.readFileSync(p,'utf8'));
 for(const n of data.nodes)n.mapUrl=n.kind==='investigation'?n.url:'/map/knowledge-lineage/records/'+(n.kind==='study'?n.path.split('/')[1]:n.kind+'-'+path.basename(n.path,'.md'))+'/';
 data.asOf=new Date(data.generated_for+'T00:00:00Z').toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
 const nodes=new Map(data.nodes.map(n=>[n.id,n]));
 for(const n of data.nodes){
 n.outgoing=[...new Set(data.edges.filter(e=>e.subject===n.id).map(e=>e.object))].map(id=>nodes.get(id));
 n.incoming=[...new Set(data.edges.filter(e=>e.object===n.id).map(e=>e.subject))].map(id=>nodes.get(id));
 }
 const groups=['software-updates','model-found-bugs','ai-cost-and-spread'].map(id=>{
  const g=data.groups.find(g=>g.id===id);if(!g)return null;
  return {...g,...intros[id],studyNodes:g.studies.map(id=>nodes.get(id)),pieceNodes:g.pieces.map(id=>nodes.get(id))};
 }).filter(Boolean);
 return {...data,recordPages:data.nodes.filter(n=>n.kind!=='investigation'),drawings:{wide:fs.readFileSync(path.join(root,'notes/knowledge-lineage/history-wide.svg'),'utf8'),phone:fs.readFileSync(path.join(root,'notes/knowledge-lineage/history-mobile.svg'),'utf8')},groups,unassignedNodes:data.unassigned.map(id=>nodes.get(id))};
}
