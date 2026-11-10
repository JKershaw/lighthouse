import fs from 'node:fs';
import path from 'node:path';

const intros = {
 'software-updates': { title: 'How software updates travel', question: 'A release is available. What happens next?', state: 'Findings to explore', summary: 'Follow releases through downloads, pinned versions and build instructions.', start: '/articles/where-software-updates-go/' },
 'model-found-bugs': { title: 'When a model finds a flaw', question: 'How does a reported discovery reach defenders?', state: 'An ongoing investigation', summary: 'Keep the discovery report, fixes, disclosure dates and public signals in view.', start: '/map/knowledge-lineage/trails/#topic' },
 'ai-cost-and-spread': { title: 'AI and the shared internet', question: 'What does this activity leave behind?', state: 'Working records to explore', summary: 'Explore services closing access, exposed systems and the evidence for spread.', start: '/investigations/ai-cost-and-spread/' },
};
export function loadKnowledgeMap(root) {
 const p=path.join(root,'notes/knowledge-lineage/overview.json');
 if(!fs.existsSync(p))return null;
 const data=JSON.parse(fs.readFileSync(p,'utf8'));
 const nodes=new Map(data.nodes.map(n=>[n.id,n]));
 const groups=['software-updates','model-found-bugs','ai-cost-and-spread'].map(id=>{
  const g=data.groups.find(g=>g.id===id);if(!g)return null;
  return {...g,...intros[id],studyNodes:g.studies.map(id=>nodes.get(id)),pieceNodes:g.pieces.map(id=>nodes.get(id))};
 }).filter(Boolean);
 return {...data,drawings:{wide:fs.readFileSync(path.join(root,'notes/knowledge-lineage/history-wide.svg'),'utf8'),phone:fs.readFileSync(path.join(root,'notes/knowledge-lineage/history-mobile.svg'),'utf8')},groups,unassignedNodes:data.unassigned.map(id=>nodes.get(id))};
}
