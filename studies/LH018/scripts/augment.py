#!/usr/bin/env python3
"""Read the notice references named by the fixed initial snapshot."""
import csv,hashlib,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'data'/'snapshot-2026-10-21'; log=out/'read_log.csv'
with log.open() as f: rows=list(csv.DictReader(f))
assert len(rows)+4<=60
urls=[('debian_notice','DLA-4848-1','https://security-tracker.debian.org/tracker/DLA-4848-1'),
('debian_notice','DSA-6574-1','https://security-tracker.debian.org/tracker/DSA-6574-1'),
('ubuntu_notice','USN-8948-1','https://ubuntu.com/security/notices/USN-8948-1'),
('foundation','2026-10-21','https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/')]
for kind,key,url in urls:
 at=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z');status='';data=b'';headers={};error=''
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Lighthouse-LH018/0.1'}),timeout=22) as r:
   status=r.status;headers=dict(r.headers);data=r.read(1024*1024+1)
   if len(data)>1024*1024:data=data[:1024*1024];error='truncated at 1 MiB'
 except urllib.error.HTTPError as e:status=e.code;headers=dict(e.headers);data=e.read(4096);error='HTTP error'
 except Exception as e:error=f'{type(e).__name__}: {e}'
 p=out/f'{kind}_{key}.raw';p.write_bytes(data)
 rows.append({'observed_at_utc':at,'kind':kind,'key':key,'url':url,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'file':p.relative_to(root).as_posix(),'last_modified':headers.get('Last-Modified',''),'etag':headers.get('ETag',''),'ratelimit_remaining':'','error':error})
 with log.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 print(kind,key,status,len(data),error,flush=True)
