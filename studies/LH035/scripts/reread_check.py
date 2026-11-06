# Checks rows I01 to I40 of data/instruments.json against the raw bodies in data/reads-2026-11-06/:
# every double-quoted phrase (split at ellipses) must occur verbatim, after HTML unescaping and
# normalising quotes, dashes and whitespace; then numbers outside quotes. Offline. Run from studies/LH035.
import json,re,html,csv,sys
rs=json.load(open('data/instruments.json'))['rows'][:40]
d='data/reads-2026-11-06'
log={r['url']:r for r in csv.DictReader(open(f'{d}/readlog.csv'))}
def norm(s):
    s=html.unescape(html.unescape(s))
    s=s.replace('\\u0026','&').replace('\\"','"').replace('\\n',' ')
    s=re.sub(r'[‘’‛′]',"'",s); s=re.sub(r'[“”″]','"',s)
    s=re.sub(r'[‐-―−]','-',s); s=s.replace(' ',' ').replace('…','...')
    s=re.sub(r'\s+',' ',s); return s.lower()
def text(raw):
    t=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',raw,flags=re.S|re.I)
    t=re.sub(r'<[^>]+>',' ',t); return norm(t)
fields=['counts','vantage','cadence','history','access','page_date','window','cannot_see','note']
res=[]
for r in rs:
    bodies=[]
    for u in r['urls_read']:
        L=log[u.split(' ')[0]]
        try: raw=open(f"{d}/{L['file']}",encoding="utf-8",errors="replace").read()
        except FileNotFoundError: raw=""
        bodies.append((L['file'],text(raw),norm(raw)))
    for f in fields:
        for q in re.findall(r'"([^"]+)"',r.get(f,'') or ''):
            segs=[s.strip(' .,;') for s in re.split(r'\.\.\.|…',q) if s.strip(' .,;')]
            found=[]
            for s in segs:
                ns=norm(s); hit=[fn for fn,t,rw in bodies if ns in t] or [fn+'(raw)' for fn,t,rw in bodies if ns in rw]
                found.append(hit)
            ok=all(found)
            res.append((r['id'],f,q,ok,';'.join(sorted({h for x in found for h in x}))))
json.dump(res,open('data/reads-2026-11-06/quote_check.json','w'),indent=0)
print('quotes',len(res),'found',sum(x[3] for x in res))
for x in res:
    if not x[3]: print('MISS',x[0],x[1],repr(x[2]))
print('--- numbers outside quotes')
months='january february march april may june july august september october november december'.split()
for r in rs:
    bodies=[]
    for u in r['urls_read']:
        L=log[u.split(' ')[0]]
        try: raw=open(f"{d}/{L['file']}",encoding='utf-8',errors='replace').read()
        except FileNotFoundError: raw=''
        bodies.append(text(raw)+' '+norm(raw))
    allb=' '.join(bodies)
    for f in fields:
        v=re.sub(r'"[^"]+"','',r.get(f,'') or '')
        for num in re.findall(r'\d[\d,\.]*\d|\d',v):
            n=num.rstrip('.,')
            if n not in allb and n.replace(',','') not in allb:
                print(r['id'],f,n,'|',v[:160])
