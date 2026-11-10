#!/usr/bin/env python3
"""Offline integrity checks for the built pilot, not a browser interaction test."""
import json
import argparse
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'site/_site'
class Tags(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='img':self.images.append(a)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prefix', default='')
    prefix=parser.parse_args().prefix.rstrip('/')
    subprocess.run(['python3','scripts/lineage/extract.py','--check'],cwd=ROOT,check=True)
    graph=json.loads((ROOT/'notes/knowledge-lineage/graph.json').read_text())
    failures=[];count=0
    for route in ['map/knowledge-lineage','notes/knowledge-lineage/README','notes/knowledge-lineage/evaluation']:
        file=SITE/route/'index.html'
        if not file.exists(): failures.append(str(file));continue
        tags=Tags();tags.feed(file.read_text())
        for href in tags.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            route_path=u.path[len(prefix):] if prefix and u.path.startswith(prefix+'/') else u.path
            target=SITE/unquote(route_path).lstrip('/') if route_path.startswith('/') else file.parent/unquote(route_path)
            if not u.path:target=file
            if target.is_dir():target=target/'index.html'
            if not target.exists():failures.append(f'{route}: {href}');continue
            if u.fragment and target.suffix=='.html':
                other=Tags();other.feed(target.read_text())
                if unquote(u.fragment) not in other.ids:failures.append(f'{route}: missing fragment {href}')
            count+=1
        for img in tags.images:
            src=img.get('src','')
            if src.startswith('/'):
                relative=src[len(prefix):] if prefix and src.startswith(prefix+'/') else src
                if not (SITE/relative.lstrip('/')).exists():failures.append(f'{route}: missing image {src}')
            if not img.get('alt'):failures.append(f'{route}: image lacks alt')
    ids={n['id'] for n in graph['nodes']}
    for edge in graph['edges']:
        if edge['subject'] not in ids or edge['object'] not in ids:failures.append(edge['id'])
    scores=json.loads((ROOT/'notes/knowledge-lineage/adjudication.json').read_text())
    result=dict(path_prefix=prefix or '/',local_links_checked=count,failures=failures,baseline_score=sum(q['baseline'] for q in scores['items']),assisted_score=sum(q['assisted'] for q in scores['items']),score_denominator=len(scores['items']),nodes=len(ids),edges=len(graph['edges']),candidates=len(graph['candidates']),browser_test='not completed: browser launch/socket and cloud-localhost access unavailable')
    (ROOT/('notes/knowledge-lineage/check-results-prefix.json' if prefix else 'notes/knowledge-lineage/check-results.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    if failures:raise SystemExit(1)
if __name__=='__main__':main()
