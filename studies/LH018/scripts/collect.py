#!/usr/bin/env python3
"""One bounded LH018 public-source snapshot. No image layers or binaries."""
import csv,hashlib,json,sys,time,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'snapshot-2026-10-21'
OUT.mkdir(parents=True,exist_ok=True)
LOG=OUT/'read_log.csv'
if LOG.exists():
 raise SystemExit('snapshot already exists; refusing to overwrite time-sensitive evidence')
MAX_CALLS=60; MAX_BYTES=50*1024*1024
calls=0; size=0
records=[]


def now():return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def save(kind,key,url,headers=None,limit=1024*1024):
 global calls,size
 if calls>=MAX_CALLS or size>=MAX_BYTES:raise RuntimeError('collection ceiling reached')
 calls+=1; started=now(); status=None; data=b''; hdr={}; error=''
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Lighthouse-LH018/0.1',**(headers or {})})
  with urllib.request.urlopen(req,timeout=22) as r:
   status=r.status;hdr=dict(r.headers);data=r.read(min(limit,MAX_BYTES-size)+1)
   if len(data)>min(limit,MAX_BYTES-size):error='response exceeds byte limit; truncated';data=data[:min(limit,MAX_BYTES-size)]
 except urllib.error.HTTPError as e:
  status=e.code;hdr=dict(e.headers);data=e.read(min(limit,4096));error='HTTP error'
 except Exception as e:error=f'{type(e).__name__}: {e}'
 size+=len(data);digest=hashlib.sha256(data).hexdigest()
 path=OUT/f'{kind}_{key}.raw';path.write_bytes(data)
 row={'observed_at_utc':started,'kind':kind,'key':key,'url':url,'status':status or '',
      'bytes':len(data),'sha256':digest,'file':path.relative_to(ROOT).as_posix(),
      'last_modified':hdr.get('Last-Modified',''),'etag':hdr.get('ETag',''),
      'ratelimit_remaining':hdr.get('Ratelimit-Remaining',hdr.get('RateLimit-Remaining','')),
      'error':error}
 records.append(row)
 with LOG.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerows(records)
 print(kind,key,status,'bytes',len(data),'error',error,flush=True)
 return status,data,hdr

for cve in ['CVE-2026-109618','CVE-2026-109619']:
 save('debian',cve,f'https://security-tracker.debian.org/tracker/{cve}')
 save('ubuntu',cve,f'https://ubuntu.com/security/cves/{cve}.json')

# Hub tag metadata does not fetch image layers. One manifest GET per tag only.
tags=['8.5.12-apache','8.4.27-fpm','8.3.36-cli','8.2.35-fpm']
for tag in tags:
 key=tag.replace('.','_').replace('-','_')
 status,data,h=save('hubtag',key,f'https://hub.docker.com/v2/namespaces/library/repositories/php/tags/{tag}')
 if status!=200:continue
 try:
  obj=json.loads(data);platform=next(i for i in obj.get('images',[]) if i.get('architecture')=='amd64' and i.get('os')=='linux')
  digest=platform['digest']
  if not digest.startswith('sha256:'):raise ValueError('missing per-platform digest')
 except Exception as e:
  print('No linux/amd64 digest for',tag,type(e).__name__,str(e),flush=True);continue
 auth_url='https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/php:pull'
 status,auth,_=save('auth',key,auth_url)
 if status!=200:continue
 try:token=json.loads(auth)['token']
 except Exception as e:print('No anonymous bearer token:',e,flush=True);continue
 # Anonymous bearer is temporary access, not evidence; erase its raw response immediately.
 (OUT/f'auth_{key}.raw').unlink(missing_ok=True)
 records[-1]['file']='[ephemeral anonymous bearer discarded]'
 records[-1]['sha256']=''
 with LOG.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=records[-1].keys());w.writeheader();w.writerows(records)
 headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json'}
 status,manifest,mh=save('manifest',key,f'https://registry-1.docker.io/v2/library/php/manifests/{digest}',headers)
 remain=mh.get('Ratelimit-Remaining','')
 if status!=200 or status==429:continue
 if remain:
  try:
   if int(remain.split(';')[0])<10:
    print('Stopping registry reads: rate limit below ten',flush=True);break
  except ValueError:pass
 try:config=json.loads(manifest)['config']['digest']
 except Exception as e:print('No configuration digest',e,flush=True);continue
 save('config',key,f'https://registry-1.docker.io/v2/library/php/blobs/{config}',{'Authorization':'Bearer '+token},limit=2*1024*1024)

print('COMPLETE',now(),'requests',calls,'downloaded bytes',size,flush=True)
