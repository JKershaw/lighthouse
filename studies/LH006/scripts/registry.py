"""LH006: registry reads through the OCI distribution API, with anonymous tokens only.

Manifests, image indexes and configuration blobs are cached in the scratch directory so that a rerun
does not repeat a counted Docker Hub pull. Layers are streamed, decompressed and walked as tar
entries as they arrive, and the connection is closed as soon as the wanted entries are seen or the
byte cap is reached; no layer is written to disk."""
import gzip, hashlib, io, json, os, re, tarfile, time, zlib
from common import http, SCRATCH, log, now, S

ACCEPT = ', '.join(['application/vnd.oci.image.index.v1+json',
                    'application/vnd.docker.distribution.manifest.list.v2+json',
                    'application/vnd.oci.image.manifest.v1+json',
                    'application/vnd.docker.distribution.manifest.v2+json'])
CACHE = os.path.join(SCRATCH, 'cache')
os.makedirs(CACHE, exist_ok=True)
_tokens = {}
BUDGET = {'docker.io_manifest_gets': 0}
HUB_FLOOR = 10          # stop Docker Hub manifest GETs below this remaining count (brief.md)
HUB_MAX_GETS = 30       # in all, for the study (brief.md, amendment point 1)


def _prior_hub_gets():
    from common import LOG
    import csv
    if not os.path.exists(LOG):
        return 0
    return sum(1 for r in csv.DictReader(open(LOG)) if r['label'].startswith('GET manifest docker.io') and r['http_status'] == '200')


class HubBudgetExhausted(Exception):
    pass


def base(host):
    return 'https://registry-1.docker.io' if host == 'docker.io' else f'https://{host}'


def token(host, name):
    k = (host, name)
    if k in _tokens and time.time() - _tokens[k][1] < 240:
        return _tokens[k][0]
    if host == 'docker.io':
        url = f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{name}:pull'
    else:
        url = f'https://{host}/token?service={host}&scope=repository:{name}:pull'
    r = http(f'{host} token endpoint (anonymous)', f'token {host}/{name}', url, note='token value not recorded')
    if r.status_code != 200:
        return None
    j = r.json()
    _tokens[k] = (j.get('token') or j.get('access_token'), time.time())
    return _tokens[k][0]


def head(host, name, ref):
    """HEAD on a manifest: the digest and, on Docker Hub, the rate-limit headers. Not a pull."""
    tok = token(host, name)
    r = http(f'{host} registry API', f'HEAD manifest {host}/{name}:{ref}', f'{base(host)}/v2/{name}/manifests/{ref}',
             method='HEAD', headers={'Authorization': f'Bearer {tok}', 'Accept': ACCEPT},
             note='HEAD; not a pull by Docker documentation')
    rem = r.headers.get('ratelimit-remaining', '')
    return dict(status=r.status_code, digest=r.headers.get('docker-content-digest', ''),
                content_type=r.headers.get('content-type', ''), ratelimit_limit=r.headers.get('ratelimit-limit', ''),
                ratelimit_remaining=rem, ratelimit_source=r.headers.get('docker-ratelimit-source', ''))


def hub_remaining(name):
    h = head('docker.io', name, 'latest')
    try:
        return int(h['ratelimit_remaining'].split(';')[0]), h
    except ValueError:
        return None, h


def manifest(host, name, ref):
    """GET a manifest or index by digest (cached). On Docker Hub each uncached GET is counted."""
    path = os.path.join(CACHE, f'{host}_{name.replace("/", "_")}_{ref.replace(":", "_")}.json')
    if os.path.exists(path):
        return json.load(open(path))
    if host == 'docker.io':
        if _prior_hub_gets() >= HUB_MAX_GETS:  # every counted GET, this run's included, is in the read log
            raise HubBudgetExhausted('run budget reached')
        if BUDGET['docker.io_manifest_gets'] % 20 == 0:
            rem, h = hub_remaining(name)
            if rem is not None and rem < HUB_FLOOR:
                raise HubBudgetExhausted(f'ratelimit-remaining {h["ratelimit_remaining"]} (limit {h["ratelimit_limit"]})')
        BUDGET['docker.io_manifest_gets'] += 1
    tok = token(host, name)
    r = http(f'{host} registry API', f'GET manifest {host}/{name}@{ref[:19]}', f'{base(host)}/v2/{name}/manifests/{ref}',
             headers={'Authorization': f'Bearer {tok}', 'Accept': ACCEPT},
             note='GET; counts as a pull on Docker Hub' if host == 'docker.io' else 'GET')
    if r.status_code == 429:
        raise HubBudgetExhausted('429 from registry')
    if r.status_code != 200:
        return {'_status': r.status_code}
    j = r.json()
    j['_digest'] = r.headers.get('docker-content-digest', '')
    j['_content_type'] = r.headers.get('content-type', '')
    json.dump(j, open(path, 'w'))
    return j


def platform_manifest(host, name, index):
    """From an index, the linux/amd64 manifest descriptor digest; from a manifest, itself."""
    if 'manifests' in index:
        for m in index['manifests']:
            p = m.get('platform') or {}
            if p.get('os') == 'linux' and p.get('architecture') == 'amd64':
                return m['digest']
        return None
    return index.get('_digest')


def blob_json(host, name, digest):
    path = os.path.join(CACHE, f'blob_{digest.replace(":", "_")}.json')
    if os.path.exists(path):
        return json.load(open(path))
    tok = token(host, name)
    r = http(f'{host} registry API', f'GET config blob {host}/{name}@{digest[:19]}', f'{base(host)}/v2/{name}/blobs/{digest}',
             headers={'Authorization': f'Bearer {tok}'})
    if r.status_code != 200:
        return {'_status': r.status_code}
    j = r.json()
    json.dump(j, open(path, 'w'))
    return j


class Capped(io.RawIOBase):
    def __init__(self, resp, cap):
        self.it = resp.iter_content(1 << 16)
        self.buf = b''
        self.n = 0
        self.cap = cap
        self.hit_cap = False

    def readable(self):
        return True

    def readinto(self, b):
        while not self.buf:
            if self.n >= self.cap:
                self.hit_cap = True
                return 0
            try:
                self.buf = next(self.it)
            except StopIteration:
                return 0
            self.n += len(self.buf)
        k = min(len(b), len(self.buf))
        b[:k] = self.buf[:k]
        self.buf = self.buf[k:]
        return k


DIST = re.compile(r'(^|/)(site-packages|dist-packages)/([A-Za-z0-9_.]+)-([^/]+)\.dist-info/METADATA$')
LOCKS = re.compile(r'(^|/)(uv\.lock|poetry\.lock|requirements[^/]*\.txt|pylock[^/]*\.toml)$')


def norm(n):
    return re.sub(r'[-_.]+', '-', n).lower()


def scan_layer(host, name, digest, media_type, want_pkgs, cap):
    """Stream one layer; return dict with dist-info versions seen for want_pkgs, lockfile pins of mcp,
    bytes read, whether the layer ended or the cap/stop cut it short."""
    tok = token(host, name)
    t = now()
    r = S.get(f'{base(host)}/v2/{name}/blobs/{digest}', headers={'Authorization': f'Bearer {tok}'},
              stream=True, timeout=300)
    out = dict(read_utc=t, status=r.status_code, bytes_read=0, ended='', found={}, mcp_paths=[], lock_pins=[], entries=0)
    if r.status_code != 200:
        log(read_utc=t, source=f'{host} registry API', label=f'stream layer {name}@{digest[:19]}', method='GET stream',
            endpoint=f'{base(host)}/v2/{name}/blobs/{digest}', http_status=r.status_code, bytes=0, note='refused')
        return out
    raw = Capped(r, cap)
    mode = 'r|gz' if 'gzip' in media_type or media_type.endswith('tar.gzip') or media_type.endswith('.tar+gzip') or 'rootfs.diff.tar.gzip' in media_type else 'r|'
    if 'zstd' in media_type:
        out['ended'] = 'zstd layer not readable (no zstd module)'
        r.close()
        return out
    want = {norm(p) for p in want_pkgs}
    try:
        tf = tarfile.open(fileobj=io.BufferedReader(raw, 1 << 16), mode=mode)
        for m in tf:
            out['entries'] += 1
            mm = DIST.search(m.name)
            if mm:
                pkg = norm(mm.group(3))
                if pkg in want:
                    out['found'].setdefault(pkg, []).append(mm.group(4))
                    if pkg == 'mcp':
                        out['mcp_paths'].append(m.name)
            lm = LOCKS.search(m.name)
            if lm and m.isfile() and m.size < 5_000_000 and '/site-packages/' not in m.name:
                f = tf.extractfile(m)
                txt = f.read().decode('utf-8', 'replace') if f else ''
                pin = ''
                if m.name.endswith('uv.lock') or m.name.endswith('poetry.lock'):
                    x = re.search(r'\[\[package\]\]\s*\nname = "mcp"\s*\nversion = "([^"]+)"', txt)
                    pin = x.group(1) if x else ''
                else:
                    x = re.search(r'(?im)^\s*mcp(\[[^\]]*\])?\s*==\s*([^\s;#]+)', txt)
                    pin = x.group(2) if x else ''
                out['lock_pins'].append(f'{m.name}={pin or "no mcp pin"}')
            if 'mcp' in out['found']:
                out['ended'] = 'stopped: mcp dist-info seen'
                break
        else:
            out['ended'] = 'layer end'
    except (tarfile.ReadError, EOFError, zlib.error, OSError) as ex:
        out['ended'] = 'cap reached' if raw.hit_cap else f'read error: {str(ex)[:80]}'
    if raw.hit_cap and not out['ended'].startswith('stopped'):
        out['ended'] = 'cap reached'
    out['bytes_read'] = raw.n
    r.close()
    log(read_utc=t, source=f'{host} registry API', label=f'stream layer {name}@{digest[:19]}', method='GET stream',
        endpoint=f'{base(host)}/v2/{name}/blobs/{digest}', http_status=r.status_code, bytes=raw.n, note=out['ended'])
    return out
