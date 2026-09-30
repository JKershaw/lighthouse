"""LH017's frame: LH015's frame and timed files, copied unchanged after checking the hashes the brief fixes.

python3 frame.py     writes data/frame.csv and data/frame_files.csv, or stops if a hash differs
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, STUDY  # noqa: E402

SRC = os.path.join(os.path.dirname(STUDY), 'LH015', 'data')
FIXED = {
    'frame.csv': '83eb0f6b751af7a26c4939cd0d49349214390eab9a9a06a8fe85f1e37f523384',
    'frame_files.csv': '29b75f95320767e482ad4192a43c465d107b022ed1c34b7a346873ba2896e074',
}


def main():
    os.makedirs(DATA, exist_ok=True)
    for name, want in FIXED.items():
        b = open(os.path.join(SRC, name), 'rb').read()
        got = hashlib.sha256(b).hexdigest()
        if got != want:
            sys.exit(f'{name}: SHA-256 {got} is not the brief\'s {want}; stopping')
        open(os.path.join(DATA, name), 'wb').write(b)
        print(f'{name}: {got} (as fixed); copied')


if __name__ == '__main__':
    main()
