# LH014 amendments

brief.md is kept byte-identical to the snapshot whose SHA-256, 31c19166af2ce7410e8ce10ab9f34d0b437b7cdcf73b8e07965b3377cb1c9c7b, the driving session posted on issue #16 and committed at 353f17f with snapshot_sha256.txt. Later changes are recorded here, dated and numbered, and labelled post hoc when made after any count was seen.

## Amendment 1, 29 September 2026: the frame

Written by the research subagent (Opus 5.5, claude-opus-5-5, as reported by its harness) in phase 2, after the snapshot and before any daily, per-version, installer or CI count was read, with LH014_PHASE=2: scripts/common.py's gate refused every query that counts except the August monthly sums. It records what the brief left to be read and fixes nothing new. The cases the brief did not foresee are listed at the end, each with its handling, decided before any count was read. Not post hoc.

**What was read, and when** (29 September 2026, UTC; data/read_log.csv; scripts/collect_frame.py, then scripts/frame.py offline).

- ClickPy, 23 queries reading 171,550,081 rows, every one HTTP 200:
  - R01 at 12:52:12: the August ranking, 5,100 rows. data/clickpy_month_2026_08.csv keeps the result as read. Its sums enter only as the list's order and are reported nowhere.
  - I01, 8 queries from 12:53:38 to 12:53:45: the installer table's distinct installer names for the drawn projects, with no counts.
  - K01 to K03, 14 queries from 12:53:46 to 12:53:56: first and last day held, 25 March to 27 September, per drawn project, in `pypi_downloads_per_day`, `pypi_downloads_per_day_by_version` and `pypi_downloads_per_day_by_version_by_installer_by_type`.
- PyPI JSON: 160 requests from 12:52:24 to 12:53:11, every one HTTP 200. No field describing downloads was kept.
- No documentation page.
- In all phases so far: 28 ClickPy queries and 171,552,209 rows read (ceilings 800 and 60 billion); 160 PyPI requests (ceiling 400); 2 documentation reads (ceiling 5).

**The list** (data/frame.csv, frame_checks.csv). 5,100 rows, already in the brief's order (sum descending, then name ascending).

- The 17 tools removed, with raw ranks: setuptools 9, pip 44, wheel 66, virtualenv 81, hatchling 82, uv 218, poetry-core 256, build 273, setuptools-scm 291, poetry 433, flit-core 593, pipenv 908, maturin 981, pdm 1,390, scikit-build-core 1,425, pipx 1,852 and pdm-backend 2,035.
- LH011's 50 are all in the list, as its first 50 projects after the tooling: none is displaced.
- No tie in the August sum at any edge. The projects either side are rpds-py and yarl (positions 50 and 51), langgraph-prebuilt and pandocfilters (500 and 501), and flameprof and sigstore-models (5,000 and 5,001).
- No two names collide under PEP 503.
- Band A has 450 projects and band B 4,500.

**Against the rankings earlier studies kept** (data/ranking_comparison.csv; a description). Three rankings were compared: LH008's top 200 and LH010's top 500, both read on 27 September, and LH011's top 80, read on 28 September. In all three, every project is at the same rank and every sum is identical. ClickPy's August table did not change between those reads and this one.

**The draw** (data/pypi_walk.csv, drawn.csv).

- In each band, 80 projects were walked, none was skipped as not served or not read, and all 80 were drawn.
- PyPI's canonical name matches each drawn name under PEP 503.
- Drawn positions run from 60 to 500 in band A and from 547 to 4,974 in band B.

The drawn projects in draw order, an asterisk marking those with no qualifying release:

- A: joblib, matplotlib-inline, synchronicity, markdownify, google-cloud-dataform, cyclopts, parso, zstandard*, google-cloud-speech, uc-micro-py*, fastapi-cloud-cli, transformers, xmltodict*, google-cloud-bigtable, jaraco-functools, sentry-sdk, psycopg2-binary, argon2-cffi-bindings, itsdangerous*, sortedcontainers*, pytest-json-ctrf, modal, editables, pytokens*, httpcore2, ghapi, httplib2, cfgv*, google-api-core, lz4*, flatbuffers*, identify, pyasn1-modules*, deepdiff, cachecontrol*, invoke, setproctitle*, paramiko, tomli*, types-protobuf, langchain, jsonref*, colorama*, nest-asyncio*, tiktoken, jedi, gunicorn, toml*, tomlkit, ast-serialize, datasets, pillow, tzdata, authlib, pathable, aiohappyeyeballs, zipp, dnspython*, exceptiongroup*, langgraph-prebuilt, cfn-lint, fonttools, pkginfo, psycopg2, azure-storage-blob, libcst, tenacity*, backports-tarfile*, distro*, nodeenv*, networkx*, prometheus-client, fastapi-cli, google-resumable-media, typeguard, croniter, msal-extensions*, toolz*, opentelemetry-instrumentation-fastapi*, tinycss2*.
- B: ib-insync*, opentelemetry-instrumentation-logging*, gnupg*, pypandoc*, jwskate*, django-timezone-field, check-jsonschema, socketswap*, djlint, thop*, webdataset*, businesstimedelta*, social-auth-core, sudachidict-core, log-symbols*, torch-geometric, py-cpuinfo*, swig, mkdocs-click*, azure-mgmt-containerinstance*, hatch, webtest*, snitun, hubspot-api-client*, service-identity, python-whois*, nvidia-nvtx, mini-racer*, cligj*, recurring-ical-events, recommonmark*, pytelegrambotapi, statsforecast, astropy, zensical, functions-framework, w3lib*, skia-python*, libsass*, wasabi*, xattr*, simple-gcp-object-downloader*, python-decouple*, nab-index, dlib-bin*, aioresponses, pysimdjson*, gremlinpython, cli-exit-tools*, pyrect*, pydyf*, manhole*, junitparser, red-black-tree-mod*, dropbox-sign, dagster-shared, dydantic*, standardwebhooks, glob2*, pydantic-ai-shields, plaid-python, pyomo, pyserial*, pynose*, itypes*, apache-airflow-providers-snowflake, simple-websocket*, mapbox-earcut*, warcio*, pytest-bdd*, azureml-dataprep, zarr, opencv-contrib-python-headless, fnvhash*, reportportal-client, types-python-dateutil, pylsqpack*, tensorboard, pylint-pydantic*, orbax-checkpoint.

**Releases and the CI subsample** (data/pypi_versions.csv, releases.csv, releases_first_excluded.csv, project_order.csv).

| | band A | band B |
| --- | --- | --- |
| drawn projects with a qualifying release | 52 | 35 |
| qualifying releases | 295 | 196 |
| first releases excluded (choice 4) | 1: httpcore2 0.0.0, uploaded 11 May | 1: nab-index 0.0.1, uploaded 15 May |
| CI subsample | 125 | 84 |
| day 0 on 29 to 31 August, so Δ unknown by the cut | 5 | 1 |
| yanked now, kept and flagged | 3 | 1 |

- The most releases in one project: in band A, cyclopts 28, transformers 26, langchain 23 and cfn-lint 23; in band B, djlint 33, zensical 26, dagster-shared 22 and nab-index 14.
- Eighteen old version strings do not parse as PEP 440 (gnupg 3, jedi 2, joblib 5, paramiko 8) and take no part.
- The reading order alternates between the bands: A1, B1, A2 and so on (project_order.csv).

**Overlap** (data/overlap.csv).

- **The overlap set.** Five drawn projects are in it, all in band A: authlib, httplib2, langchain, pillow and transformers, all libraries of LH010. Every band A result is also given without them. None is in band B, and `mcp` was not drawn.
- **LH012's dependents.** 48 of band A's 80, and none of band B's: joblib, matplotlib-inline, synchronicity, google-cloud-dataform, cyclopts, parso, zstandard, google-cloud-speech, uc-micro-py, fastapi-cloud-cli, transformers, xmltodict, google-cloud-bigtable, jaraco-functools, sentry-sdk, argon2-cffi-bindings, pytest-json-ctrf, modal, pytokens, httpcore2, google-api-core, lz4, deepdiff, cachecontrol, paramiko, langchain, tiktoken, jedi, gunicorn, datasets, pillow, authlib, zipp, dnspython, exceptiongroup, cfn-lint, pkginfo, azure-storage-blob, libcst, tenacity, backports-tarfile, nodeenv, networkx, prometheus-client, fastapi-cli, google-resumable-media, typeguard and tinycss2.
- **Their late-August releases.** 19 of the 48 projects' releases have day 0 from 22 to 31 August, so their later days fall in LH012's week. They belong to 16 projects: joblib 1, google-cloud-dataform 1, cyclopts 2, fastapi-cloud-cli 1, transformers 2, google-cloud-bigtable 1, sentry-sdk 1, modal 1, google-api-core 1, langchain 2, gunicorn 1, authlib 1, cfn-lint 1, pkginfo 1, azure-storage-blob 1 and google-resumable-media 1. As the brief fixes, they are named, not removed.

**Mirror installers** (data/installer_names.csv, mirror_installers.csv).

- The installer table holds 21 distinct names for the drawn projects from 25 March to 27 September 2026: the empty name, Artifactory, Bazel, Browser, Homebrew, Nexus, OS, bandersnatch, chaquopy, conda, devpi, distribute, pdm, pex, pip, `pip` followed by U+200B (a zero-width space), poetry, requests, setuptools, uv and wv.
- Matched to the mirror class: exactly `Artifactory`, `bandersnatch` and `devpi`. `z3c.pypimirror` does not occur.
- Listed but left out, as a name containing one of the four without equalling it: none.

**Coverage** (data/coverage.csv).

- In all three tables read, all 160 drawn projects hold 27 September 2026.
- Three projects hold no day before a date after 25 March: httpcore2 (from 11 May), nab-index (from 13 May) and pydantic-ai-shields (from 28 March), all projects that began within the read window.

**What could not be read.** Everything the brief asked for was read except `pypi.pypi`'s own coverage (case 1 below). Every walked project was served.

**Cases the brief did not foresee, with their handling, decided before any count was read.**

1. **`pypi.pypi`'s coverage.** Any read of that table scans one row per download. Even a query that returns only dates would therefore log a rows-read statistic that is in effect a download count, so it was not read. Handling: the three tables read above are filled from `pypi.pypi`'s inserts, and neither they nor it have a TTL (data/clickpy_schema.csv). So their coverage stands for it on the CI subsample's days, 1 April to 2 September. A CI read that returns no row on a day the by-version table holds for that project makes that day a gap for the release's CI share.
2. **Unexpected installer names.** An installer is named `pip` followed by U+200B. By the brief's rule (exactly `pip` or `uv`), it is not `pip`: its downloads are "flag not known", and it is outside the mirror class. `wv` is likewise an installer of its own. `Nexus`, a repository manager that can proxy PyPI, is not among the four names pypistats gives. It stays outside the mirror class, as the brief fixes, and M1 and M2 do not separate it.
3. **Packaging tools outside LH011's list.** Two were drawn: hatch, a project manager (band B), and editables, a library for editable installs (band A). They stay, since the brief fixes LH011's list. They are named here so a reader can weigh them.

**Frame files**, as written by this amendment's scripts (SHA-256):

- data/drawn.csv 39b92fd463b75288f0481e5366ff6eb9cb781b4e56901ca17587e6d37cdf4b56
- data/releases.csv 85c3a607610f388ccc01d4e58d5bf8efd614ab0beec9925dfc19e53fa65b6e91
- data/releases_first_excluded.csv 62406e43fd04498da918e3839c5961d05d0294102f98b1de84239cc08bb99796
- data/project_order.csv c55cd9ae9488820d355583c84cad5adb41a59d896e3fea571ab07a2e248ea458
- data/pypi_versions.csv 14c6a3a822422e1636692bd8b93896aafabdfb9a47f99780584ace26de6bf15f
- data/pypi_walk.csv f2d6fb1b5d53dff40d34d7cbc2fb8c1771667517a8f91329ad5bb6c489048358
- data/frame.csv 4b36db097ebfc12d55c665264b292da150f8538cb2df0997169deef6794d5942
- data/clickpy_month_2026_08.csv 4f803f4eb94b46cc67b4113c834171f7892b5bd3d385c15acfc8ac1a8d27681a
- data/mirror_installers.csv 6b2c3a894603a8cb32dbecfbe7874d1ad02cb9f1cda35726943eb632cddda274
- data/coverage.csv d585443fb158eac4a523212c6cb96adc4eadbd2894098e352b44e50be49ef9f8
- data/overlap.csv 1fc6858e57346498d3aafd65f33162eed7158b778dbc4234c635ce735af1848f
