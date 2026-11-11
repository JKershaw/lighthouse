#!/usr/bin/env python3
"""Offline, deterministic pilot export from a frozen repository, not a support classifier."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'notes/knowledge-lineage'
BASE = json.loads((OUT / 'baseline.json').read_text())['input_commit']
DATE = '2026-11-10'
INPUTS = {}

def read(path):
    body = subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT).decode()
    INPUTS[path] = hashlib.sha256(body.encode()).hexdigest()
    return body

def pinpoint(path, passage):
    body = read(path)
    if passage not in body:
        raise ValueError(f'Missing retained passage: {path}: {passage}')
    start = body[:body.index(passage)].count('\n') + 1
    end = start + passage.count('\n')
    return dict(path=path, passage=passage, line_start=start, line_end=end,
                sha256=INPUTS[path], input_commit=BASE,
                url=f'https://github.com/JKershaw/lighthouse/blob/{BASE}/{path}#L{start}-L{end}')

def record_url(path):
    return '/' + path[:-3] + '/' if path.endswith('.md') else f'https://github.com/JKershaw/lighthouse/blob/{BASE}/{path}'

def build():
    nodes, edges, candidates, claims, external = [], [], [], [], []
    table_path = 'notes/it-was-only-a-test/claims-table.md'
    table = read(table_path)
    refs = dict(re.findall(r'^\[([^\]]+)\]:\s*(\S+)', table, re.M))
    rows = [line for line in table.splitlines() if re.match(r'^\| R\d+ \|', line)]
    selected = [(i+1, row) for i,row in enumerate(rows) if i % 5 == 0 and i < 81]
    def addnode(id, kind, title, url, **kw):
        if not any(n['id'] == id for n in nodes):
            nodes.append(dict(id=id, kind=kind, title=title, url=url, **kw))
    def edge(id, subject, predicate, object, evidence, status='reported', **kw):
        edges.append(dict(id=id, subject=subject, predicate=predicate, object=object,
            evidence=evidence, status=status, asserted_by='Codex pilot annotation' if id.startswith('trail-') else 'retained Lighthouse record',
            extraction_agent='OpenAI Codex; exact model unavailable', ai_role='indexing and annotation',
            assertion_date=DATE, pilot_read_date=DATE, event_date=None, source_read_date=None,
            scope='A relationship in retained records, not independent confirmation of the underlying event.', **kw))
    for ordinal,row in selected:
        cells = [c.strip() for c in row.strip('|').split('|')]
        id, text, source, anchor, status = cells
        pin = pinpoint(table_path,row)
        addnode(id,'claim',text,record_url(table_path), evidence_status=status, ordinal=ordinal)
        claim = dict(id=id,ordinal=ordinal,text=text,source_pinpoint=source,quote_anchor=anchor,evidence_status=status,evidence=pin,sources=[])
        for ref in dict.fromkeys(re.findall(r'\[([A-Z]\d+[a-z]?)\]', source)):
            target = refs.get(ref)
            if not target:
                candidates.append(dict(id=f'missing-{id}-{ref}',subject=id,predicate='attributes-to',object=ref,status='unresolved',reason='No source definition found',evidence=pin))
                continue
            url = target if target.startswith('https:') else record_url('notes/it-was-only-a-test/'+target) if not target.startswith('#') else record_url(table_path)+target
            addnode(ref,'source',ref,url,access='linked in retained record; not refetched by pilot',source_read_date=None,event_date=None)
            edge(f'claim-{id}-{ref}',id,'attributes-to',ref,pin)
            claim['sources'].append(dict(id=ref,url=url))
        claims.append(claim)
    # A small source panel. Listing a URL is not a successful read.
    seen=set()
    for file in ['studies/LH036/panel.json','studies/LH038/policies.json']:
        raw=read(file)
        urls=list(dict.fromkeys(re.findall(r'https://[^"\s]+',raw)))
        picked=[u for u in urls if u not in seen][:6]
        for url in picked:
            seen.add(url)
            id='external-'+str(len(external)+1)
            pin=pinpoint(file,url)
            addnode(id,'source',url.split('/')[2],url,access='panel membership only; read availability not inferred',event_date=None,source_read_date=None)
            addnode(file,'protocol source panel',file,record_url(file))
            edge('panel-'+id,file,'lists-source',id,pin)
            external.append(dict(id=id,url=url,evidence=pin,access='not fetched by pilot; panel membership is not access evidence'))
    annotations=json.loads((OUT/'annotations.json').read_text())
    # Dates, actors and access history are assertions with retained provenance.
    for node in nodes:
        metadata=annotations.get('source_metadata',{}).get(node['id'])
        if metadata:
            m=metadata.copy()
            m['date_evidence']=pinpoint(m.pop('path'),m.pop('passage'))
            node.update(m)
    review_path='notes/it-was-only-a-test/claims-check-claude.md'
    review=read(review_path)
    for claim in claims:
        review_row=next((line for line in review.splitlines() if line.startswith('| '+claim['id']+' |')),None)
        claim['primary_passage_access']='Original full source pack not indexed here; historical review row available (may record an access failure)' if review_row else 'Original full source pack not indexed here; no matching reviewer row'
        if review_row:
            pin=pinpoint(review_path,review_row)
            claim['historical_review']=pin
            activity='historical-review-'+claim['id']
            addnode(activity,'review','Historical review of '+claim['id'],record_url(review_path),source_read_date='2026-11-08',event_date='2026-11-08',actor='Claude Opus 5.5')
            edge('review-'+claim['id'],activity,'reviews-earlier-version-of',claim['id'],pin,'reported',qualification='Historical verdict against the earlier version. Not automatically a verdict on the current corrected row.')
    access_path='notes/it-was-only-a-test/claims-check-claude.md'
    access_passage='Could not read | R17, R18, R19, R20, R21, R23, R77'
    addnode('australia-failed-read','access activity','Claude review could not read the Australia account',record_url(access_path),actor='Claude Opus 5.5',event_date='2026-11-08')
    edge('access-failure','australia-failed-read','could-not-read','O1',pinpoint(access_path,access_passage),'checked',qualification='HTTP 403 access history, not evidence the source claim is false.')
    verify_path='notes/it-was-only-a-test/australia-verification.md'
    addnode('australia-later-verification','review','Separate Australia verification',record_url(verify_path),actor='OpenAI Codex authoring session; exact model unavailable',event_date='2026-11-08')
    edge('access-resolution','australia-later-verification','checks-source-account','O1',pinpoint(verify_path,'This resolves an access gap, not an independent forensic investigation of the underlying incident.'),'checked',qualification='A separate source-account verification preserves the earlier failed read.')
    trails=[]
    for trail in annotations['trails']:
        steps=[]
        for step in trail['steps']:
            s=step.copy()
            pin=pinpoint(s.pop('path'),s.pop('passage'))
            s['evidence']=pin
            s['record_url']=record_url(pin['path'])
            addnode(s['id'],s['kind'],s['title'],s.get('primary_url') or s['record_url'],event_date=s['event_date'],source_read_date=s['source_read_date'],ai_role=s['ai_role'])
            steps.append(s)
        links=[]
        for link in trail['links']:
            l=link.copy()
            pin=pinpoint(l.pop('path'),l.pop('passage'))
            edge(l['id'],l['subject'],l['predicate'],l['object'],pin,l['status'],qualification=l['qualification'])
            edges[-1].update({key:l[key] for key in ['event_date','source_read_date','date_kind','source_actor']})
            links.append({**l,'evidence':pin})
        trails.append({**trail,'steps':steps,'links':links})
    related=[]
    for item in annotations['related']:
        item=item.copy()
        pin=pinpoint(item.pop('path'),item.pop('passage'))
        related.append({**item,'evidence':pin,'record_url':record_url(pin['path'])})
    for c in annotations['candidates']:
        c=c.copy()
        c['evidence']=pinpoint(c.pop('path'),c.pop('passage'))
        c.update(assertion_date=DATE,pilot_read_date=DATE,asserted_by='OpenAI Codex pilot; exact model unavailable',ai_role='candidate suggestion, not verified influence')
        candidates.append(c)
    for e in edges:
        if e['id'].startswith(('claim-','review-','access-')):
            e['event_date']='2026-11-08'
            e['date_kind']='claim-map version or review date, not the underlying incident date'
            e['source_read_date']='2026-11-08'
            e['asserted_by']='OpenAI Codex claims-map author' if e['id'].startswith('claim-') else 'Claude Opus 5.5 historical review' if e['id'].startswith('review-') or e['id']=='access-failure' else 'OpenAI Codex separate source verification'
            e['date_basis']='Retained evidence-directory README and dated review/verification headers; all read by pilot on 2026-11-10'
        if e['id'].startswith('claim-'):
            target=next(n for n in nodes if n['id']==e['object'])
            e['source_actor']=target.get('actor','Unknown')
            e['source_publication_date']=target.get('publication_date')
    for e in edges:
        if e['id'] in ['review-R21','access-failure']:
            e['attempted_read_date']='2026-11-08'
            e['source_read_date']=None
            e['read_qualification']='The historical reviewer could not read O1; the separate later verification is a different activity.'
    return dict(schema_version='0.2',input_commit=BASE,assertion_date=DATE,
        protocol='notes/knowledge-lineage/protocol.md',active_external_rule=json.loads((OUT/'baseline.json').read_text())['external_rule'],
        limits=['Retrospective sample, not a research landscape census.', 'Source access is not independent event confirmation.', 'No measured deployment, influence or social benefit edges.', 'Original authoring-pack paths are not reconstructed.', 'Same-day order in a trail is logical, not a measured within-day sequence.'],
        sampling=dict(total_claim_rows=len(rows),selected_ordinals=[i for i,_ in selected],selected_claim_rows=len(claims),external_panel_records=len(external)),
        annotations_sha256=hashlib.sha256((OUT/'annotations.json').read_bytes()).hexdigest(),
        related=related,inputs=dict(sorted(INPUTS.items())),claims=claims,external=external,nodes=nodes,edges=edges,candidates=candidates,trails=trails,
        standards=dict(note='Local JSON borrows entity/activity/provenance distinctions from the proposal. Not an RDF or PROV conformance claim.',proposal='https://github.com/JKershaw/lighthouse/pull/47'))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    graph=build()
    payload=json.dumps(graph,ensure_ascii=False,indent=2)+'\n'
    path=OUT/'graph.json'
    if args.check:
        if not path.exists() or path.read_text()!=payload:
            raise SystemExit('Export differs: run python3 scripts/lineage/extract.py')
    else:
        path.write_text(payload)
    print(json.dumps(dict(claim_rows=graph['sampling'],nodes=len(graph['nodes']),edges=len(graph['edges']),candidates=len(graph['candidates']),input_commit=BASE)))

if __name__=='__main__': main()
