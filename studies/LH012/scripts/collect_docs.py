#!/usr/bin/env python3
"""LH012 phase 1: documentation and literature, each read logged in data/read_log.csv; the pages
themselves are kept in scratch space only, and what the brief relies on is quoted in sources.md.
D reads are documentation of what PyPI's log records (the Python Packaging User Guide, linehaul's
and ClickPy's public repositories where they answer); L reads are the literature the programme names.
The installers' source is read from PyPI's source distributions (pip 26.2.1 and uv 0.12.8, the
versions LH011 read) for the fields they send besides the CI flag.
New for LH012; the logging is common.py's. Usage: python3 collect_docs.py"""
import os, sys
from common import get_text, download, SCRATCH

PAGES = [
    ('D01', 'Python Packaging User Guide', 'https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/'),
    ('D02', 'linehaul-cloud-function README (raw)', 'https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/README.md'),
    ('D03', 'linehaul-cloud-function UA parser (raw)', 'https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/ua/parser.py'),
    ('D04', 'linehaul-cloud-function BigQuery schema (raw)', 'https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/schema.json'),
    ('D05', 'ClickPy README (raw)', 'https://raw.githubusercontent.com/ClickHouse/clickpy/main/README.md'),
    ('L01', 'SPEC 0', 'https://scientific-python.org/specs/spec-0000/'),
    ('L02', 'NEP 29', 'https://numpy.org/neps/nep-0029-deprecation_policy.html'),
    ('L03', 'Decan, Mens and Constantinou 2018 (PDF)', 'https://decan.lexpage.net/files/ICSME-2018.pdf'),
    ('L04', 'Technical lag across package managers, APSEC 2020 (PDF)', 'https://kblincoe.github.io/publications/2020_APSEC_tech_lag.pdf'),
]
SDISTS = [
    ('S01', 'pip 26.2.1 sdist', 'https://files.pythonhosted.org/packages/source/p/pip/pip-26.2.1.tar.gz'),
    ('S02', 'uv 0.12.8 sdist', 'https://files.pythonhosted.org/packages/source/u/uv/uv-0.12.8.tar.gz'),
]
only = sys.argv[1:] or None
d = os.path.join(SCRATCH, 'docs')
os.makedirs(d, exist_ok=True)
for label, name, url in PAGES:
    if only and label not in only:
        continue
    ext = '.pdf' if url.endswith('.pdf') else '.txt'
    path = os.path.join(d, label + ext)
    if ext == '.pdf':
        print(label, download('Documentation and literature', f'{label} {name}', url, path), path)
    else:
        status, body = get_text('Documentation and literature', f'{label} {name}', url, path)
        print(label, status, len(body), path)
for label, name, url in SDISTS:
    if only and label not in only:
        continue
    path = os.path.join(d, os.path.basename(url))
    print(label, download('PyPI source distribution (files.pythonhosted.org)', f'{label} {name}', url, path), path)
