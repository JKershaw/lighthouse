#!/usr/bin/env python3
"""LH006 step 3a: tag lists for every qualifying image repository in data/candidates.csv.

Docker Hub: hub.docker.com's v2 tag API (no pull counted, by Docker's documentation), which gives
last_updated, last_pushed, tag_last_pulled, tag_status, the tag's digest and per-platform images;
and the registry's own /v2/<name>/tags/list with an anonymous token from auth.docker.io.
ghcr.io: /v2/<name>/tags/list with an anonymous token from ghcr.io/token.
Writes data/tags_hub.csv, data/tags_registry.csv. Token values are never written anywhere."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, read_csv, write_csv


def token(host, name):
    if host == 'docker.io':
        url = f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{name}:pull'
        src = 'auth.docker.io (anonymous token)'
    elif host == 'ghcr.io':
        url = f'https://ghcr.io/token?service=ghcr.io&scope=repository:{name}:pull'
        src = 'ghcr.io/token (anonymous token)'
    else:
        raise ValueError(host)
    r = http(src, f'token {host}/{name}', url, note='token value not recorded')
    if r.status_code != 200:
        return None, r.status_code
    j = r.json()
    return j.get('token') or j.get('access_token'), r.status_code


def registry_base(host):
    return 'https://registry-1.docker.io' if host == 'docker.io' else f'https://{host}'


def registry_tags(host, name, tok):
    tags, url = [], f'{registry_base(host)}/v2/{name}/tags/list?n=1000'
    while url:
        r = http(f'{host} registry API', f'tags/list {host}/{name}', url, headers={'Authorization': f'Bearer {tok}'})
        if r.status_code != 200:
            return tags, r.status_code
        tags += r.json().get('tags') or []
        link = r.headers.get('Link', '')
        url = None
        if 'rel="next"' in link:
            nxt = link.split(';')[0].strip('<> ')
            url = registry_base(host) + nxt if nxt.startswith('/') else nxt
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
    for c in read_csv('candidates.csv'):
        if c['qualifies'] != 'yes':
            continue
        host, name = c['image_repository'].split('/', 1)
        if host == 'docker.io':
            res, st = hub_tags(name)
            for t in res:
                hub_rows.append(dict(image=c['image_repository'], package=c['package'], tag=t['name'],
                                     last_updated=t.get('last_updated'), last_pushed=t.get('tag_last_pushed'),
                                     tag_last_pulled=t.get('tag_last_pulled'), tag_status=t.get('tag_status'),
                                     digest=t.get('digest'), media_type=t.get('media_type'), content_type=t.get('content_type'),
                                     images=json.dumps([dict(p=f"{i.get('os')}/{i.get('architecture')}{'/' + i['variant'] if i.get('variant') else ''}",
                                                             d=i.get('digest'), size=i.get('size'), last_pushed=i.get('last_pushed'),
                                                             last_pulled=i.get('last_pulled'), status=i.get('status'))
                                                        for i in t.get('images') or []])))
            print(c['image_repository'], 'hub tags', len(res), st)
        tok, st = token(host, name)
        if not tok:
            reg_rows.append(dict(image=c['image_repository'], package=c['package'], tag='', status=f'token refused {st}'))
            continue
        tags, st = registry_tags(host, name, tok)
        for t in tags:
            reg_rows.append(dict(image=c['image_repository'], package=c['package'], tag=t, status=st))
        if not tags:
            reg_rows.append(dict(image=c['image_repository'], package=c['package'], tag='', status=f'tags/list {st}'))
        print(c['image_repository'], 'registry tags', len(tags), st)
    write_csv('tags_hub.csv', hub_rows, ['image', 'package', 'tag', 'last_updated', 'last_pushed', 'tag_last_pulled',
                                         'tag_status', 'digest', 'media_type', 'content_type', 'images'])
    write_csv('tags_registry.csv', reg_rows, ['image', 'package', 'tag', 'status'])


if __name__ == '__main__':
    main()
