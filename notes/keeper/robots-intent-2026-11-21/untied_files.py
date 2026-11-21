#!/usr/bin/env python3
"""List the files that sweep_may_keep.py counted as untied to any logged URL, offline (no request).

Reuses sweep_may_keep.py's own functions and tie rule, so the list is the one it counted; prints JSON
lines {study, file, bytes, head} where head is the first 80 bytes (decompressed for .gz).
Usage, from the repository root: python3 -I notes/keeper/robots-intent-2026-11-21/untied_files.py OUT.jsonl
"""
import gzip, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep_may_keep as S  # noqa: E402


def tied_and_dirs():
    tied, dirs = S.tie_all()
    return {fp for fp, _ in tied}, dirs


def head(fp):
    with open(fp, 'rb') as f:
        b = f.read(4096)
    if b[:2] == b'\x1f\x8b':
        try:
            b = gzip.open(fp).read(4096)
        except Exception:
            pass
    return b[:80].decode('utf-8', 'replace')


def main():
    seen, dirs = tied_and_dirs()
    with open(sys.argv[1], 'w') as out:
        for d in sorted(dirs):
            for f in sorted(os.listdir(d)):
                fp = os.path.join(d, f)
                if S.is_body(d, f) and fp not in seen and not os.path.exists(S.stem_of(fp) + '.derived.json'):
                    st = fp.split('/')[1] if fp.startswith('studies/') else 'notes'
                    out.write(json.dumps({'study': st, 'file': fp, 'bytes': os.path.getsize(fp), 'head': head(fp)}) + '\n')


if __name__ == '__main__':
    main()
