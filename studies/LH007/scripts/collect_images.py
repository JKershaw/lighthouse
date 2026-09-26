#!/usr/bin/env python3
"""LH007 step 3b, adapted from LH006: for each sampled image repository (data/sample.csv, with the
mirrors of brief.md's amendment), the images (distinct digests) in the period and the nearest outside
it on each side: manifest, linux/amd64 configuration, and then the installed mcp version streamed from
the layers, in the priority order of data/layer_plan.csv and within the byte caps of brief.md.

Usage: LH007_SCRATCH=<dir> python3 collect_images.py meta|layers [image ...]
meta   writes data/images.csv (one row per image digest: tags, push time, created, labels)
layers writes data/layer_reads.csv, data/image_mcp.csv, data/image_configs.csv, data/image_history.csv
"""
import csv, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, DATA, now, log
import registry as R

P0, P1 = '2026-05-19T21:37:16Z', '2026-07-14T21:37:16Z'
RELEASE = '2026-06-16T21:37:16Z'
REPO_CAP = 400 * 1024 * 1024
TOTAL_CAP = 3 * 1024 * 1024 * 1024
INSTALL = re.compile(r'pip |pip3 |uv |uv\.|poetry|pdm |venv|site-packages|requirements|pyproject|COPY', re.I)
BASE = re.compile(r'ADD file:|ADD rootfs|apt-get|apk add|dnf |yum |GPG_KEY|PYTHON_VERSION|python\.tar|/bin/sh -c #\(nop\)|^\s*(ENV|CMD|LABEL|ARG|WORKDIR|EXPOSE|ENTRYPOINT|USER|SHELL)\b', re.I)


def iso_utc(s):
    """An RFC 3339 time with any offset and fraction, as UTC to the second."""
    if not s:
        return ''
    import datetime
    m = re.match(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(\.\d+)?(Z|[+-]\d\d:\d\d)?$', s)
    t = datetime.datetime.fromisoformat(m.group(1) + (m.group(3) or 'Z').replace('Z', '+00:00'))
    return t.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


MIRRORS = {'ghcr.io/langflow-ai/langflow': 'docker.io/langflowai/langflow',
           'ghcr.io/langflow-ai/langflow-nightly': 'docker.io/langflowai/langflow-nightly',
           'ghcr.io/browser-use/browser-use': 'docker.io/browseruse/browseruse'}  # brief.md, amendment point 2


def own_pkg(package):
    return {'modulector-sdk': 'modulector'}.get(package, package)


def sampled():
    """(image repository, package, sample rank), with the amendment's mirrors substituted."""
    return [(MIRRORS.get(f"{c['registry']}/{c['image']}", f"{c['registry']}/{c['image']}"), c['package'], int(c['sample_rank']))
            for c in read_csv('sample.csv')]


def hub_images():
    """Docker Hub: one row per distinct index digest, from the hub API's tag records."""
    by = collections.defaultdict(lambda: dict(tags=[], pushed=[]))
    for t in read_csv('tags_hub.csv'):
        k = (t['image'], t['package'], t['digest'])
        by[k]['tags'].append(t['tag'])
        by[k]['pushed'].append(t['last_pushed'] or t['last_updated'])
        by[k]['images'] = json.loads(t['images'])
        by[k]['media_type'] = t['media_type']
        by[k]['tag_last_pulled'] = max(by[k].get('tag_last_pulled', ''), t['tag_last_pulled'] or '')
    rows = []
    for (img, pkg, dig), v in by.items():
        amd = [i for i in v['images'] if i['p'] == 'linux/amd64']
        rows.append(dict(image=img, package=pkg, index_digest=dig, media_type=v['media_type'], tags=' '.join(sorted(v['tags'])),
                         first_pushed=min(v['pushed'])[:19] + 'Z', last_pushed=max(v['pushed'])[:19] + 'Z',
                         tag_last_pulled=(v['tag_last_pulled'] or '')[:19],
                         amd64_digest=amd[0]['d'] if amd else '', platforms=' '.join(i['p'] for i in v['images'])))
    return rows


def ghcr_images(img, pkg):
    host, name = img.split('/', 1)
    by = collections.defaultdict(list)
    from concurrent.futures import ThreadPoolExecutor
    tags = [t['tag'] for t in read_csv('tags_registry.csv') if t['image'] == img and t['tag']]
    R.token(host, name)
    with ThreadPoolExecutor(1 if host == 'public.ecr.aws' else 4) as ex:
        heads = list(ex.map(lambda t: R.head(host, name, t), tags))
    for t, h in zip(tags, heads):
        if h['digest']:
            by[h['digest']].append(t)
    rows = []
    for dig, tags in by.items():
        idx = R.manifest(host, name, dig)
        rows.append(dict(image=img, package=pkg, index_digest=dig, media_type=idx.get('mediaType', idx.get('_content_type', '')),
                         tags=' '.join(sorted(tags)), first_pushed='', last_pushed='', tag_last_pulled='',
                         amd64_digest=R.platform_manifest(host, name, idx) or '',
                         platforms=' '.join(f"{(m.get('platform') or {}).get('os')}/{(m.get('platform') or {}).get('architecture')}"
                                            for m in idx.get('manifests', [])) or 'single'))
    return rows


def in_scope(rows):
    """Images whose time (push time on Docker Hub, created on ghcr) falls in the period, plus the
    nearest on each side."""
    key = lambda r: r['first_pushed'] or r.get('created', '')
    rs = sorted([r for r in rows if key(r)], key=key)
    inside = [r for r in rs if P0 <= key(r) <= P1]
    before = [r for r in rs if key(r) < P0][-1:]
    after = [r for r in rs if key(r) > P1][:1]
    for r in before:
        r['position'] = 'nearest before period'
    for r in after:
        r['position'] = 'nearest after period'
    for r in inside:
        r['position'] = 'in period, before release' if key(r) < RELEASE else 'in period, after release'
    return before + inside + after


def config_fields(host, name, amd):
    m = R.manifest(host, name, amd)
    if '_status' in m:
        return dict(config_status=m['_status']), m
    cfg = R.blob_json(host, name, m['config']['digest'])
    labels = (cfg.get('config') or {}).get('Labels') or {}
    return dict(created=iso_utc(cfg.get('created')), created_raw=cfg.get('created') or '',
                label_created=labels.get('org.opencontainers.image.created', ''),
                label_revision=labels.get('org.opencontainers.image.revision', '')[:12],
                label_version=labels.get('org.opencontainers.image.version', ''),
                label_source=labels.get('org.opencontainers.image.source', ''),
                history_entries=len(cfg.get('history') or []), layers=len(m.get('layers') or []),
                layers_bytes=sum(l.get('size', 0) for l in m.get('layers') or []), config_status=200), m


def meta(images):
    out = []
    hub = hub_images()
    for img, package, rank in sampled():
        if images and img not in images:
            continue
        host, name = img.split('/', 1)
        if host != 'docker.io':
            try:
                tok = R.token(host, name)
            except Exception:
                tok = None
            if not tok:
                out.append(dict(image=img, package=package, position='not readable', config_status='anonymous token refused'))
                continue
            rows = ghcr_images(img, package)
            for r in rows:
                if r['amd64_digest']:
                    f, _ = config_fields(host, name, r['amd64_digest'])
                    r.update(f)
            sel = in_scope(rows)
            chosen = {id(r) for r in sel}
            for r in rows:
                if id(r) not in chosen:
                    r['position'] = 'outside period'
            out += sorted(rows, key=lambda r: r.get('created', ''))
        else:
            rows = [r for r in hub if r['image'] == img]
            sel = in_scope(rows)
            chosen = {id(r) for r in sel}
            for r in rows:
                r.setdefault('position', 'outside period (not read)')
                if id(r) not in chosen:
                    r['position'] = 'outside period (not read)'
            out += sorted(rows, key=lambda r: r['first_pushed'])
    fields = ['image', 'package', 'position', 'tags', 'index_digest', 'media_type', 'platforms', 'amd64_digest',
              'first_pushed', 'last_pushed', 'tag_last_pulled', 'created', 'label_created', 'label_revision',
              'label_version', 'label_source', 'history_entries', 'layers', 'layers_bytes', 'config_status']
    old = [r for r in (read_csv('images.csv') if os.path.exists(os.path.join(DATA, 'images.csv')) else [])
           if images and r['image'] not in images]
    write_csv('images.csv', old + out, fields)


def choose_layers(m, cfg):
    """Layer order to scan: top down, skipping layers whose history line is a base-image step."""
    hist = [h for h in (cfg.get('history') or []) if not h.get('empty_layer')]
    layers = m.get('layers') or []
    pairs = []
    for i, l in enumerate(layers):
        cb = hist[i].get('created_by', '') if i < len(hist) and len(hist) == len(layers) else ''
        pairs.append((i, l, cb))
    base = lambda cb: BASE.search(cb or '') and not INSTALL.search(cb or '')
    top = [p for p in reversed(pairs) if not base(p[2])]
    rest = [p for p in reversed(pairs) if base(p[2])]
    return top, rest


def layers(images, order):
    """order: list of (image, index_digest) in priority order, from data/layer_plan.csv."""
    results = [r for r in (read_csv('image_mcp.csv') if os.path.exists(os.path.join(DATA, 'image_mcp.csv')) else [])
               if not r['method'].startswith('not read')]
    done = {(r['image'], r['index_digest']) for r in results}
    reads = read_csv('layer_reads.csv') if os.path.exists(os.path.join(DATA, 'layer_reads.csv')) else []
    per_repo = collections.Counter()
    for r in reads:
        per_repo[r['image']] += int(r['bytes_read'] or 0)
    total = sum(per_repo.values())
    imgs = {(r['image'], r['index_digest']): r for r in read_csv('images.csv')}
    for img, dig in order:
        if images and img not in images:
            continue
        if (img, dig) in done:
            continue
        row = imgs[(img, dig)]
        host, name = img.split('/', 1)
        capped = per_repo[img] >= REPO_CAP or total >= TOTAL_CAP  # configuration still read (brief.md, amendment 2)
        try:
            m = R.manifest(host, name, row['amd64_digest'])
        except R.HubBudgetExhausted as ex:
            print('stop Docker Hub:', ex)
            results.append(dict(image=img, index_digest=dig, tags=row['tags'], mcp_installed='', method='not read: ' + str(ex)))
            break
        if '_status' in m:
            results.append(dict(image=img, index_digest=dig, tags=row['tags'], mcp_installed='', method=f'manifest {m["_status"]}'))
            continue
        cfg = R.blob_json(host, name, m['config']['digest'])
        labels = (cfg.get('config') or {}).get('Labels') or {}
        hist = [h for h in (read_csv('image_history.csv') if os.path.exists(os.path.join(DATA, 'image_history.csv')) else [])
                if (h['image'], h['index_digest']) != (img, dig)]
        for k, h in enumerate(cfg.get('history') or []):
            hist.append(dict(image=img, index_digest=dig, step=k, empty_layer='yes' if h.get('empty_layer') else '',
                             created=h.get('created', ''), created_by=(h.get('created_by') or '').replace('\n', ' ')[:600]))
        write_csv('image_history.csv', hist, ['image', 'index_digest', 'step', 'empty_layer', 'created', 'created_by'])
        cfgs = [c for c in (read_csv('image_configs.csv') if os.path.exists(os.path.join(DATA, 'image_configs.csv')) else [])
                if (c['image'], c['index_digest']) != (img, dig)]
        cfgs.append(dict(image=img, index_digest=dig, amd64_digest=row['amd64_digest'],
                         created=iso_utc(cfg.get('created')), created_raw=cfg.get('created') or '',
                         label_created=labels.get('org.opencontainers.image.created', ''),
                         label_revision=labels.get('org.opencontainers.image.revision', '')[:12],
                         label_version=labels.get('org.opencontainers.image.version', ''),
                         label_source=labels.get('org.opencontainers.image.source', ''),
                         history_entries=len(cfg.get('history') or []), layers=len(m.get('layers') or []),
                         layers_bytes=sum(l.get('size', 0) for l in m.get('layers') or [])))
        write_csv('image_configs.csv', cfgs, list(cfgs[-1].keys()))
        top, rest = choose_layers(m, cfg)
        found, locks, own, bytes_img, note = {}, [], '', 0, ''
        if capped:
            top, note = [], 'layers not read: byte cap reached before the image'
        for i, l, cb in top:  # base-image layers (rest) are not read; see brief.md
            if per_repo[img] >= REPO_CAP or total >= TOTAL_CAP:
                note = 'byte cap reached'
                break
            cap = min(REPO_CAP - per_repo[img], TOTAL_CAP - total)
            s = R.scan_layer(host, name, l['digest'], l.get('mediaType', ''), ['mcp', own_pkg(row['package'])], cap)
            per_repo[img] += s['bytes_read']
            total += s['bytes_read']
            bytes_img += s['bytes_read']
            reads.append(dict(image=img, index_digest=dig, layer_index=i, layer_digest=l['digest'], layer_size=l.get('size'),
                              created_by=(cb or '')[:160].replace('\n', ' '), read_utc=s['read_utc'], http_status=s['status'],
                              bytes_read=s['bytes_read'], ended=s['ended'], entries=s['entries'],
                              mcp_found=';'.join(s['found'].get('mcp', [])), own_found=';'.join(s['found'].get(R.norm(own_pkg(row['package'])), [])),
                              mcp_paths=';'.join(s['mcp_paths'])[:300], lock_pins=';'.join(s['lock_pins'])[:300]))
            for k, v in s['found'].items():
                found.setdefault(k, v)
            locks += s['lock_pins']
            if 'mcp' in found:
                break
        results.append(dict(image=img, index_digest=dig, tags=row['tags'],
                            mcp_installed=';'.join(found.get('mcp', [])),
                            own_installed=';'.join(found.get(R.norm(own_pkg(row['package'])), [])),
                            lock_pins=';'.join(locks)[:300], bytes_read=bytes_img,
                            method=('dist-info in layers' if 'mcp' in found else ('no dist-info; requirements or lock file seen' if locks else 'not found in layers read')) + (f'; {note}' if note else '')))
        print(img, row['tags'][:40], found.get('mcp'), found.get(R.norm(own_pkg(row['package']))), bytes_img, note)
        write_csv('layer_reads.csv', reads, ['image', 'index_digest', 'layer_index', 'layer_digest', 'layer_size', 'created_by', 'read_utc',
                                             'http_status', 'bytes_read', 'ended', 'entries', 'mcp_found', 'own_found', 'mcp_paths', 'lock_pins'])
        write_csv('image_mcp.csv', results, ['image', 'index_digest', 'tags', 'mcp_installed', 'own_installed', 'lock_pins', 'bytes_read', 'method'])
    write_csv('image_mcp.csv', results, ['image', 'index_digest', 'tags', 'mcp_installed', 'own_installed', 'lock_pins', 'bytes_read', 'method'])
    print('bytes per repository', dict(per_repo), 'total', total, 'hub manifest GETs this run', R.BUDGET)


def configs():
    """Rebuild data/image_configs.csv for every Docker Hub image read, from the cached manifests and
    configurations (no counted request is repeated; a missing cache entry would be fetched)."""
    imgs = {(r['image'], r['index_digest']): r for r in read_csv('images.csv')}
    out = []
    for r in read_csv('image_mcp.csv'):
        if r['method'].startswith('not read') or not r['image'].startswith('docker.io/'):
            continue
        row = imgs[(r['image'], r['index_digest'])]
        host, name = r['image'].split('/', 1)
        f, _ = config_fields(host, name, row['amd64_digest'])
        out.append(dict(image=r['image'], index_digest=r['index_digest'], amd64_digest=row['amd64_digest'], **f))
    write_csv('image_configs.csv', out, ['image', 'index_digest', 'amd64_digest', 'created', 'created_raw', 'label_created',
                                         'label_revision', 'label_version', 'label_source', 'history_entries', 'layers',
                                         'layers_bytes', 'config_status'])


if __name__ == '__main__':
    stage, images = sys.argv[1], sys.argv[2:]
    if stage == 'meta':
        meta(images)
    elif stage == 'configs':
        configs()
    else:
        plan = [(r['image'], r['index_digest']) for r in read_csv('layer_plan.csv')]
        layers(images, plan)
