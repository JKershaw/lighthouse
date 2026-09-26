#!/usr/bin/env python3
"""LH007 step 3a: tag lists for every sampled image repository in data/sample.csv.

Docker Hub: hub.docker.com's v2 tag API (no pull counted, by Docker's documentation), which gives
push and pull times, the tag's digest and per-platform digests; and the registry's /v2/<name>/tags/list.
Other registries: /v2/<name>/tags/list with the anonymous token their challenge names.
Writes data/tags_hub.csv, data/tags_registry.csv. Token values are never written anywhere."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, read_csv, write_csv
from registry import token, base


def registry_tags(host, name, tok):
    tags, url = [], f'{base(host)}/v2/{name}/tags/list?n=1000'
    while url:
        r = http(f'{host} registry API', f'tags/list {host}/{name}', url, headers={'Authorization': f'Bearer {tok}'} if tok else {})
        if r.status_code != 200:
            return tags, r.status_code
        tags += r.json().get('tags') or []
        link = r.headers.get('Link', '')
        url = None
        if 'rel="next"' in link:
            nxt = link.split(';')[0].strip('<> ')
            url = base(host) + nxt if nxt.startswith('/') else nxt
    return tags, 200


def hub_tags(name):
    ns, repo = name.split('/', 1)
    out, url = [], f'https://hub.docker.com/v2/namespaces/{ns}/repositories/{repo}/tags?page_size=100'
    while url:
        r = http('hub.docker.com v2 API', f'hub tags {name}', url)
        if r.status_code != 200:
            return out, r.status_code
        j = r.json()
        out += j['results']
        url = j.get('next')
    return out, 200


def main():
    hub_rows, reg_rows = [], []
    for c in read_csv('sample.csv'):
        host, name = c['registry'], c['image']
        img = f'{host}/{name}'
        if host == 'docker.io':
            res, st = hub_tags(name)
            for t in res:
                hub_rows.append(dict(image=img, package=c['package'], tag=t['name'],
                                     last_updated=t.get('last_updated'), last_pushed=t.get('tag_last_pushed'),
                                     tag_last_pulled=t.get('tag_last_pulled'), tag_status=t.get('tag_status'),
                                     digest=t.get('digest'), media_type=t.get('media_type'),
                                     images=json.dumps([dict(p=f"{i.get('os')}/{i.get('architecture')}{'/' + i['variant'] if i.get('variant') else ''}",
                                                             d=i.get('digest'), size=i.get('size'), last_pushed=i.get('last_pushed'))
                                                        for i in t.get('images') or []])))
            print(img, 'hub tags', len(res), st, flush=True)
            continue  # Docker Hub's registry tag list adds nothing to the hub records; not read
        try:
            tok = token(host, name)
        except Exception as ex:
            reg_rows.append(dict(image=img, package=c['package'], tag='', status=f'unreachable: {str(ex)[:80]}'))
            print(img, 'unreachable', flush=True)
            continue
        if not tok:
            reg_rows.append(dict(image=img, package=c['package'], tag='', status='anonymous token refused'))
            print(img, 'token refused', flush=True)
            continue
        tags, st = registry_tags(host, name, tok)
        for t in tags:
            reg_rows.append(dict(image=img, package=c['package'], tag=t, status=st))
        if not tags:
            reg_rows.append(dict(image=img, package=c['package'], tag='', status=f'tags/list {st}'))
        print(img, 'registry tags', len(tags), st, flush=True)
    write_csv('tags_hub.csv', hub_rows, ['image', 'package', 'tag', 'last_updated', 'last_pushed', 'tag_last_pulled',
                                         'tag_status', 'digest', 'media_type', 'images'])
    write_csv('tags_registry.csv', reg_rows, ['image', 'package', 'tag', 'status'])


if __name__ == '__main__':
    main()
