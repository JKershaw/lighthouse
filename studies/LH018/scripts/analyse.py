#!/usr/bin/env python3
"""Replay LH018's seven-track summary from the retained first snapshot."""
import csv,hashlib,json,re
from pathlib import Path
from html import unescape
root=Path(__file__).resolve().parents[1]
p=root/'data/snapshot-2026-10-21'
log=list(csv.DictReader((p/'read_log.csv').open()))
for row in log:
 if row['kind']=='auth':continue
 f=root/row['file'];raw=f.read_bytes()
 assert len(raw)==int(row['bytes']) and hashlib.sha256(raw).hexdigest()==row['sha256'],row['file']
 assert str(row['status'])=='200',row['file']

rows=[]
for track,branch,source,version in [('D1','bookworm','php8.2','8.2.35-1~deb12u1'),('D2','trixie','php8.4','8.4.27-1~deb13u1')]:
 for cve in ['CVE-2026-109618','CVE-2026-109619']:
  raw=(p/f'debian_{cve}.raw').read_text()
  hits=[]
  for tr in re.findall(r'<tr[^>]*>.*?</tr>',raw,re.S):
   content=' '.join(unescape(re.sub(r'<[^>]*>',' ',tr)).split())
   if branch+' (security)' in content:hits.append(content)
  assert len(hits)==1 and version in hits[0] and 'fixed' in hits[0],(track,cve,hits)
 rows.append({'track':track,'source':f'Debian {branch} {source}','cves':'both',
              'status':'vendor tracker fixed in security pocket','revision_or_version':version,
              'source_event_utc':'2026-10-21 (advisory date only)','first_seen_utc':next(x['observed_at_utc'] for x in log if x['kind']=='debian'),
              'evidence':'debian_CVE-2026-109618.raw; debian_CVE-2026-109619.raw; '+('advisory_DLA-4848-1.raw' if track=='D1' else 'advisory_DSA-6574-1.raw')})
for cve in ['CVE-2026-109618','CVE-2026-109619']:
 d=json.loads((p/f'ubuntu_{cve}.raw').read_text());pkg=next(x for x in d['packages'] if x['name']=='php8.3')
 s=next(x for x in pkg['statuses'] if x['release_codename']=='noble' and x['pocket']=='security')
 assert s['status']=='released' and s['description']=='8.3.6-0ubuntu0.24.04.13'
 n=next(x for x in d['notices'] if x['id']=='USN-8948-1')
 assert n['published']=='2026-10-21T13:56:19.543268'
 assert any(x['name']=='php8.3' and x.get('is_source') and x['version']==s['description'] for x in n['release_packages']['noble'])
rows.append({'track':'U1','source':'Ubuntu 24.04 noble php8.3','cves':'both','status':'vendor CVE record released; USN names security-pocket revision',
             'revision_or_version':'8.3.6-0ubuntu0.24.04.13','source_event_utc':'2026-10-21T13:56:19.543268 (USN published field)',
             'first_seen_utc':next(x['observed_at_utc'] for x in log if x['kind']=='ubuntu'),
             'evidence':'ubuntu_CVE-2026-109618.raw; ubuntu_CVE-2026-109619.raw; ubuntu_notice_USN-8948-1.raw'})
for track,tag,version in [('I1','8.5.12-apache','8.5.12'),('I2','8.4.27-fpm','8.4.27'),('I3','8.3.36-cli','8.3.36'),('I4','8.2.35-fpm','8.2.35')]:
 key=tag.replace('.','_').replace('-','_')
 d=json.loads((p/f'hubtag_{key}.raw').read_text());conf=json.loads((p/f'config_{key}.raw').read_text())
 manifest=json.loads((p/f'manifest_{key}.raw').read_text())
 platform=next(x for x in d['images'] if x['architecture']=='amd64' and x['os']=='linux')
 assert 'PHP_VERSION='+version in conf['config']['Env']
 assert 'PHP_URL=https://www.php.net/distributions/php-'+version+'.tar.xz' in conf['config']['Env']
 assert manifest['config']['digest'].startswith('sha256:') and platform['digest'].startswith('sha256:')
 rows.append({'track':track,'source':'Docker Hub official php:'+tag+' linux/amd64','cves':'upstream fixed version declared',
              'status':'tag, platform manifest and config available; installed binary uninspected',
              'revision_or_version':version+'; manifest '+platform['digest'],
              'source_event_utc':platform['last_pushed']+' (platform pushed, tag pushed '+d['tag_last_pushed']+')',
              'first_seen_utc':next(x['observed_at_utc'] for x in log if x['kind']=='hubtag' and x['key']==key),
              'evidence':f'hubtag_{key}.raw; manifest_{key}.raw; config_{key}.raw'})
with (root/'data/summary.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('Verified',len(rows),'tracks and',len(log),'HTTP observations; summary.csv written')
for r in rows: print(r['track'],r['source'],r['source_event_utc'])
