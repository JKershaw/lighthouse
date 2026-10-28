// Without JavaScript, every note remains inline and readable.
const notes=[...document.querySelectorAll('.side-note')];
const wide=matchMedia('(min-width: 1450px)');
function placeNotes(){
 let previousBottom=-Infinity;
 for(const note of notes){
  const body=note.querySelector('.side-note-body'),button=note.querySelector('button');
  body.style.top='';
  if(!wide.matches || body.hidden)continue;
  const paragraph=note.closest('p,li') || note.parentElement;
  paragraph.classList.add('has-side-note');
  const parent=paragraph.getBoundingClientRect(),anchor=button.getBoundingClientRect();
  const top=Math.max(anchor.top,previousBottom+12);
  body.style.top=`${top-parent.top}px`;
  previousBottom=top+body.getBoundingClientRect().height;
 }
}
function mode(){
 for(const note of notes){const body=note.querySelector('.side-note-body'),button=note.querySelector('button');button.hidden=false;body.hidden=!wide.matches;button.setAttribute('aria-expanded',String(wide.matches));}
 placeNotes();
}
for(const note of notes){
 const button=note.querySelector('button'),body=note.querySelector('.side-note-body');
 button.addEventListener('click',()=>{body.hidden=!body.hidden;button.setAttribute('aria-expanded',String(!body.hidden));placeNotes();});
}
wide.addEventListener('change',mode);addEventListener('resize',placeNotes);document.fonts?.ready.then(placeNotes);mode();
