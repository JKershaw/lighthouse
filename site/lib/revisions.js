import { headerField } from './header.js';
import { datedNotices } from './updates.js';
const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
const display=time=>{const d=new Date(time);return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;};
function earlierEdition(markdown) {
 for(const link of String(markdown||'').matchAll(/\[([^\]]+)\]\(([^)\s]+)\)/g)){
  const context=markdown.slice(Math.max(0,link.index-40),link.index);
  if(/earlier|previous|prior|\b(?:version|edition)\s+[v\d]/i.test(link[1]) || /(?:earlier|previous|prior) (?:edition|version)[^.!?]*$/i.test(context))return {label:link[1],target:link[2]};
 }
 return null;
}
export function revisionInfo(header,body,revisions=[],draft=false) {
 const value=name=>headerField(header?.fields,name)?.value || '';
 const history=[...revisions.filter(r=>r.time).map(r=>({time:r.time,iso:r.iso,date:r.date,kind:'revised',label:'Revised',markdown:r.text,earlierEdition:earlierEdition(r.text)})),
  ...datedNotices(body).map(n=>({...n,date:display(n.time),earlierEdition:earlierEdition(n.markdown)}))].sort((a,b)=>b.time-a.time);
 const developing=/^(true|yes|developing)$/i.test(value('developing'));
 return {displayState:draft?'Draft':developing?'Developing':history.length?'Revised':'Released',developing,nextRevision:value('next-revision'),revisionHistory:history};
}
