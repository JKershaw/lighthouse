// Shared dated-source metadata for threads, feeds and revision histories.
const MONTHS = ['january','february','march','april','may','june','july','august','september','october','november','december'];
export function datedDay(value) {
  const match=String(value).match(/\b(\d{1,2}) ([A-Za-z]+) (\d{4})\b/);
  if(!match)return null;
  const month=MONTHS.indexOf(match[2].toLowerCase()),day=Number(match[1]),year=Number(match[3]);
  if(month<0)return null;
  const date=new Date(Date.UTC(year,month,day));
  if(date.getUTCDate()!==day)return null;
  return {time:date.getTime(),iso:date.toISOString().slice(0,10),label:`${day} ${match[2]} ${year}`};
}
export const noticeId=(kind,iso,index=0)=>`notice-${iso}-${kind}${index ? '-'+index : ''}`;
export function datedNotices(body) {
  const out=[],counts=new Map();
  for(const match of String(body||'').matchAll(/^>\s*\*\*(Correction|Later evidence)\b([^*\n]*)\*\*[^\n]*(?:\n>[^\n]*)*/gm)) {
    const day=datedDay(match[2]);if(!day)continue;
    const kind=match[1]==='Correction'?'correction':'later-evidence';
    const key=`${day.iso}-${kind}`,index=counts.get(key)||0;counts.set(key,index+1);
    out.push({...day,kind,id:noticeId(kind,day.iso,index),label:match[1],reviewed:true,markdown:match[0].replace(/^> ?/gm,'').trim()});
  }
  return out;
}
export function dailyEntries(body) {
  const out=[];
  for(const match of String(body||'').matchAll(/^## (\d{1,2} [A-Za-z]+ \d{4})[ \t]*\n([\s\S]*?)(?=^## |(?![\s\S]))/gm)) {
    const day=datedDay(match[1]);if(!day)continue;
    out.push({...day,kind:'unreviewed-log',id:`log-${day.iso}`,label:'Unreviewed daily log',reviewed:false,markdown:match[2].trim()});
  }
  return out;
}
export function combinedThread(account,log) {
  return [...datedNotices(account),...dailyEntries(log)].sort((a,b)=>b.time-a.time || Number(b.reviewed)-Number(a.reviewed) || a.id.localeCompare(b.id));
}
