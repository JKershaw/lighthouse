#!/usr/bin/env python3
"""Read the notice references named by the fixed initial snapshot.

The record of 21 October 2026's added reads. From 21 November 2026 (the keeper's decision,
notes/keeper/2026-11-21-robots-intent.md) a body is saved only through scripts/lh_fetch.py's save_body
(which withholds email addresses, as before); where it may not be kept no .raw is written, `file` is empty
and `error` ends "body_kept: no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH018/scripts/augment.py`."""
import csv,hashlib,urllib.request,urllib.error
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
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
 at=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z');status='';data=b'';headers={};error='';final=url
 try:
  # robots.txt-gated (scripts/lh_fetch.py): a URL not allowed raises NotFetched, logged in 'error' as not fetched
  with urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=22) as r:
   status=r.status;headers=dict(r.headers);final=r.geturl() or url;data=r.read(1024*1024+1)
   if len(data)>1024*1024:data=data[:1024*1024];error='truncated at 1 MiB'
 except urllib.error.HTTPError as e:status=e.code;headers=dict(e.headers);data=e.read(4096);error='HTTP error'
 except Exception as e:error=f'{type(e).__name__}: {e}'
 p=out/f'{kind}_{key}.raw';kept,why=save_body(p,data,final,headers)  # sha256 is of the bytes received
 if not kept:error=(error+'; ' if error else '')+'body_kept: no: '+why
 rows.append({'observed_at_utc':at,'kind':kind,'key':key,'url':url,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'file':p.relative_to(root).as_posix() if kept else '','last_modified':headers.get('Last-Modified',''),'etag':headers.get('ETag',''),'ratelimit_remaining':'','error':error})
 with log.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n");w.writeheader();w.writerows(rows)
 print(kind,key,status,len(data),error,flush=True)
