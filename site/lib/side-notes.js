// Inline ^[note text] with balanced brackets, so source links remain Markdown.
export default function sideNotes(md) {
  md.inline.ruler.before('link','lighthouse_side_note',(state,silent)=>{
    const start=state.pos;
    if(state.src.slice(start,start+2)!=='^[')return false;
    let end=start+2,depth=1;
    for(;end<state.posMax;end++){
      if(state.src[end]==='\\'){end++;continue;}
      if(state.src[end]==='\n')return false;
      if(state.src[end]==='[')depth++;
      if(state.src[end]===']'){depth--;if(depth===0)break;}
    }
    if(depth!==0 || end===start+2)return false;
    const text=state.src.slice(start+2,end);
    if(text.includes('^['))return false;
    if(!silent){
      state.env.lighthouseSideNotes=(state.env.lighthouseSideNotes||0)+1;
      const token=state.push('lighthouse_side_note','span',0);
      token.meta={text,number:state.env.lighthouseSideNotes};
    }
    state.pos=end+1;return true;
  });
  md.renderer.rules.lighthouse_side_note=(tokens,index,options,env)=>{
    const {text,number}=tokens[index].meta,id=`${env.sideNotePrefix || "side-note"}-${number}`;
    return `<span class="side-note"><button class="side-note-toggle" type="button" aria-controls="${id}" aria-expanded="true" aria-label="Note ${number}" hidden>${number}</button><span class="side-note-body" id="${id}" role="note"><span class="side-note-label">Note ${number}. </span>${md.renderInline(text,env)}</span></span>`;
  };
}
