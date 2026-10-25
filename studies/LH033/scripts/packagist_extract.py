#!/usr/bin/env python3
"""Keep only Packagist's two embedded PHP-version series (daily and monthly) from a php-statistics page.

The page also embeds the site's public search key, which Lighthouse does not write into the repository,
so the raw body is not kept; its SHA-256 stays in the read log. Usage: packagist_extract.py <read dir>.
"""
from pathlib import Path
import gzip
import json
import sys


def series(text, marker):
    start = text.index('{', text.index(marker))
    return json.JSONDecoder().raw_decode(text[start:])[0]


def extract(read_dir):
    read_dir = Path(read_dir)
    raw = read_dir / 'packagist.raw.gz'
    text = gzip.decompress(raw.read_bytes()).decode()
    out = {'daily': series(text, "initGlobalPhpStats('.js-php-daily-stats'"),
           'monthly': series(text, "initGlobalPhpStats('.js-php-monthly-stats'")}
    (read_dir / 'packagist.json').write_text(json.dumps(out) + '\n')
    raw.unlink()


if __name__ == '__main__':
    extract(sys.argv[1])
