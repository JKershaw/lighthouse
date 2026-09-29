# LH015 study brief

**Brief, written before any outcome was read, 29 September 2026.**

**study:** LH015
**edition:** 0.1
**status:** written in phase 1 of three, before any repository in the frame was cloned, listed or read; to be committed, with scripts/frame.py and the frame it writes, before phase 2 clones anything
**date opened:** 2026-09-29, after reading AGENTS.md, programme.md's Next (checkpoint of 29 September 2026), LH014's brief, LH006's and LH007's Answer, Findings and Method where they concern Dockerfiles and lockfiles, LH007's install classes (its brief and scripts/analyse.py), the Method and Limits of LH008, LH009 and LH010, LH008's screening code, the retained tables scripts/frame.py reads, and the phase 1 reads in sources.md
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), for issue #18, to a design the driving session fixed (the frame, the reads, the unit, clustering by repository, no registry and no download count, the budget); the writer's own choices are listed at the end
**grounded at:** repository commit 8d21cdd, with this study's uncommitted files in studies/LH015/
**issue:** #18 (JKershaw/lighthouse); programme.md, Next, "Until LH013 can run"

## Question

For the repositories whose pins or lockfiles LH008, LH009 and LH010 timed, at each repository and event pair's snapshot (the last first-parent commit on the default branch at or before the event's release, as those studies defined it): does the repository keep a container recipe, and does that recipe install the project's Python requirements from the file that held the pin or lock, or resolve them afresh at build time, so that an image built from it would take whatever the ranges allow when it is built, whatever the pin says?

Why it is asked. The slow road in the current account (articles/where-software-updates-go.md) rests on pins and lockfiles in public repositories: pinned software held what it named and moved over weeks. A lockfile governs only the builds that install from it. LH006 (agentcrew) and LH007 (all three open-range image repositories that keep a lockfile) found images built without the lockfile their own repository keeps. If that is common among pinned repositories, the timed moves describe less of what gets built than they seem to, and a census of lockfiles, the planned test of the frozen-list reading, would overstate how much of what is built is frozen.

What it cannot say. A recipe is not a build. No registry is read, so no image is shown to exist, and nothing here says which recipe, if any, makes an image that anyone runs. A class is a reading of instructions: what a build from the recipe would be told to install, not what any build installed.

## What the writer already knows of the outcome, disclosed

- **LH006** (record 0.2): agentcrew's images held `mcp` 1.27.0 from 8 April 2026, 16 days before its lockfile moved, because its Dockerfile copies a Docker-specific `pyproject.docker.toml` (`mcp>=1.24.0`) and runs `uv pip install .[cpu,redis]` without the lockfile; serena installs with `uv pip install -r pyproject.toml -e .` against an exact pin in pyproject.toml; mcp-snowflake-server's Dockerfile, committed on 6 May 2026, runs `uv sync --frozen`; jesse's installs from requirements.txt. Of LH006's 37 packages, 7 named a published image of their own and 7 more kept a Dockerfile without naming one.
- **LH007** (record 0.2): every lockfile and exact-pin image read held what its lock or pin said; all three open-range image repositories that keep a lockfile (mcp-proxy-for-aws, mcp-pinot, alation's MCP server) install with pip, not from the lock; browser-use runs `uv sync` with no uv.lock committed (it is in .gitignore), so uv resolved pyproject.toml, which pinned `mcp` exactly; mcp-proxy-for-aws and seclab-taskflow-agent install their own package by name from PyPI; mcp-pinot moved from `pip install .` to `uv sync --frozen` on 27 July 2026. Of 120 screened dependents of `mcp`, 22 named a published image of their own and 14 kept a Dockerfile or built an image only locally. In both studies some lock-keeping image repositories installed from the lock and some did not; neither was designed to say how common either is, and both read only projects that publish images, a selected group.
- **Nine frame repositories, 17 pairs, were read by LH006 or LH007**, at their heads as cloned on 26 September 2026 and at commits of May to July 2026, not at this study's snapshots: agentcrew (the `mcp` 1.27.2 pair; LH006's reading above), serena (python-multipart 0.0.27 and starlette 1.0.1; `uv pip install -r pyproject.toml -e .` in LH006's period), mcp-snowflake-server (`mcp` 1.27.2; `uv sync --frozen` from 6 May), browser-use (python-dotenv 1.2.2, aiohttp 3.13.4 and pillow 12.2.0; `uv sync` without a committed lock, at LH007's build commits of June and July), seclab-taskflow-agent (urllib3 2.7.0; its own package from PyPI, June and July), cognirepo (pyjwt 2.13.0 and starlette 1.0.1; a Dockerfile present, install lines not recorded), and mistral-vibe (five pairs), prosuite-mcp and relay-shell (one each), in which the study that read them found no Dockerfile at the head or at its period-end commit, by its own search rules. These readings are not used to class anything; every measure is also given without these nine repositories.
- **The retained tables** (derived by this writer with scripts/frame.py, data/frame_counts.csv): 469 pairs in 332 repositories; pin class by the timed files, lockfile 153, exact pin 199, both 117; the 887 timed files are uv.lock 286, requirements files 257, pyproject.toml 233, poetry.lock 62, setup.py 24, Pipfile.lock 20, setup.cfg 2, Pipfile 2 and pdm.lock 1; 595 lie at the repository root, 111 one directory down, 146 two and 35 three; 369 pairs have every timed file at the root. Two timed paths name a container or deployment use: `requirements_docker.txt` (a lockfile; centurion_erp's cryptography 48.0.1 pair) and `deployment/requirements.txt` (an exact pin; datawrapper-mcp's fastmcp 3.2.0 pair); no other contains "docker", "container" or "deploy". The three repositories with most pairs are docassemble (10), grimoirelab (8) and aider (8). LH008's, LH009's and LH010's scripts have no rule for recipes (none mentions Dockerfile, Containerfile or .dockerignore), so their tables hold no recipe reading.
- **The literature** (sources.md, L1 to L5): L1 tests pinning in Dockerfiles through hadolint's rules, among them DL3013, and the two smell studies whose abstracts were read rest on hadolint; DL3013 never looks inside a requirements file, is not raised for `pip install .`, `-r` or `-c`, and counts a lower bound as a pin (L5), so a figure built on it measures neither exact pinning nor lockfile use. In L1, images rebuilt less than two years after builds of 2023 had, in half of those compared, at least 22.6 per cent of their packages at another version (all packages, not Python's alone). No published measure of how often a repository's recipe installs from its own lockfile was found.
- **General knowledge.** The writer's training includes general knowledge of some widely used public repositories, possibly some in this frame. It is not a reading at any snapshot, and no class is assigned from it.
- The writer has listed no tree and read no file or commit of any frame repository, and has no expectation of the shares beyond the above.

## Population and unit

- **Frame** (scripts/frame.py, offline, reading only LH008's, LH009's and LH010's data/): every row of the three lags.csv tables (193, 257 and 232 rows) is mapped to one moves.csv row: LH008's by frame and repository; LH009's rows, and LH010's reused rows, whose `source` is LH008 or LH009, to that study's `<library>:fix` frame; LH010's own rows by frame and repository. A **pair** is (repository, lower-cased; library; threshold release, the release whose upload time set the snapshot); an **event** is (library, threshold release). Rows with one key are one pair, and the earliest study's moves row (LH008, then LH009, then LH010) gives its frame, package, snapshot commit and timed files. The result is **469 pairs, 332 repositories, 40 events**. Seventeen pairs were read twice with the same snapshot commit: LH010's within-library second fixes of cryptography 48.0.1 (14, LH008's fix frame) and aiohttp 3.14.3 (3, LH009's). A row that does not map, a duplicate with another snapshot, or a pair without pinned files stops the script; none occurred.
- **Snapshot.** The pair's `snapshot_commit` (12 hexadecimal digits) from that moves row; `snapshot_time` from the same study's screen.csv is kept to check the commit found. No other commit stands in for it.
- **Timed files (T).** The pair's rows in that study's snapshot_files.csv (data/frame_files.csv, 887 files): every file at the snapshot that pinned or locked the library, as those studies read them (at most three directories deep, outside test, example and documentation directories, at most 80 candidate files per repository, shallowest first). Every one holds a version below the pair's fix (LH010's `pair_fix` where given, else the threshold), by PEP 440 order. The library is **L**.
- **Pin class.** Lockfile if every timed file is a lockfile, exact pin if every one is an exact pin, both otherwise: 153, 199 and 117 pairs.
- **Unit.** The pair. The distinct repository is reported beside it (Measures). Repositories: 330 on github.com, one on gitlab.com, one on bitbucket.org; 265 have one pair and the largest ten.
- **Head.** For secondary measure S2 only, the default branch's head in phase 2's clone; the head LH008 to LH010 recorded on 27 September is kept beside it.
- frame.csv's SHA-256 is 83eb0f6b751af7a26c4939cd0d49349214390eab9a9a06a8fe85f1e37f523384 (data/frame_counts.csv). Phase 2 reruns frame.py and checks it before any clone.

## Sources and reads in phase 2

- **Git over HTTPS, anonymously.** One blobless clone per repository, `git clone --filter=blob:none --no-checkout https://<repo>.git`, as LH008 to LH010 made them (full history of commits and trees, not shallow, so that every snapshot can be found). Files are read with `git ls-tree -r --name-only <commit>` and `git show <commit>:<path>`, which fetch blobs on demand. Every clone, retry and file read is logged in data/read_log.csv, file reads counted by repository and commit.
- **Read at each snapshot:** the tree listing; every recipe candidate, primary or not; ignore files (`.dockerignore` at candidate contexts, and Dockerfile-specific ignore files); compose files; CI workflow files (`.github/workflows/*`, `.gitlab-ci.yml`), only for the context, file, target and arguments they give a recipe; the scripts, Makefiles and requirements files a recipe's install steps call or name (scripts one level deep, requirements includes to two levels); the manifests a recipe resolves from (for S1). **At the head,** the same for S2.
- **PyPI's JSON API** (https://pypi.org/pypi/<name>/json) only for recipes that install the project's own published package by name.
- **Not read:** any container registry or image, any download count (ClickPy is not used, so nothing of LH013's weeks is read), GitHub's web pages and API, OSV, Open Source Insights. No account, key or token.

## What counts as a container recipe

- **Primary.** A file whose name, ignoring case, is `Dockerfile` or `Containerfile`, begins with `Dockerfile` or `Containerfile` followed by `.`, `-` or `_`, or ends with `.Dockerfile`, `-Dockerfile` or `_Dockerfile` (or the same with `Containerfile`) (D15, D19); not a name ending in `.dockerignore` or in `.md`, `.rst`, `.txt`, `.sh`, `.py`, `.yml`, `.yaml`, `.json`, `.toml`, `.lock`, `.orig`, `.bak` or `.patch`. Templates (`.j2`, `.jinja`, `.jinja2`, `.tmpl`, `.tpl`, `.template`, `.in`) count and are flagged. A compose file's `dockerfile_inline` (D18) counts, located at the compose file.
- **Where.** Anywhere in the tree at any depth, except under a directory that LH008's pinned-file rule skipped (`tests`, `test`, `testing`, `test_*`, `*_test`, `*_tests`, `examples`, `example`, `*_example`, `*_examples`, `docs`, `doc`, `.venv`, `venv`, `site-packages`, `vendor`, `node_modules`, `third_party`) or under `.devcontainer` or `.github` (development containers and CI actions). The exclusions follow the pinned files' own frame.
- **Not recipes:** compose files themselves (read for contexts), Kubernetes and Helm files, CI workflows. Other build definitions (`Earthfile`, `Singularity`, `Singularity.*`, `apptainer.def`, `cog.yaml`, `bentofile.yaml`, `Procfile`, `nixpacks.toml`) are counted and listed, not classed.
- **Sensitivities:** R1 counts recipes in the excluded directories too; R2 counts only files named `Dockerfile` or `Containerfile`, ignoring case.
- A pair **keeps a recipe** if its snapshot tree holds at least one primary recipe.

## How installers treat a pinned or locked file

Fixed from the documentation read before any recipe (sources.md, D1 to D19). "L from F" means the installer takes L's version from what file F says.

| Command | What it reads, and where L's version comes from |
| --- | --- |
| `pip install -r F`, `-c F` (and `uv pip install` likewise) | F, and the files F includes by `-r` or `-c` (D1, D2); a constraints file limits versions without installing (D3). pip installs the newest version the requirements admit (D1). |
| `pip install .`, `-e .`, a local path, a wheel built from it in the build, `uv pip install -r pyproject.toml`, `python setup.py install` | The project's own manifest, through its build backend (D1, D6); no lockfile is read. An exact pin there admits one version. |
| pip, already installed | A plain install does not change an installed package that satisfies it; `--upgrade` upgrades the packages named, and their dependencies only as `--upgrade-strategy` says, by default only if needed (D3). `uv pip install` keeps installed packages unless they conflict; `uv pip sync F` and `pip-sync F` make the environment exactly F (D7, D13). |
| `uv sync`, `uv run`, `uv export`, `uv lock` | With uv.lock present: the locked versions, which change only if the project's constraints exclude them; `--locked` fails on an outdated lock; `--frozen` uses it unchecked; `--upgrade` and `--upgrade-package` re-resolve (D4). Without it: pyproject.toml, resolved afresh. `UV_FROZEN`, `UV_LOCKED`, `UV_NO_SYNC`, `UV_CONSTRAINT` equal their flags (D8). `uv run` in ENTRYPOINT or CMD syncs when the container starts (D4, D5). |
| `poetry install`, `poetry sync`, `poetry export` | With poetry.lock present, its exact versions; without, pyproject.toml resolved and a lock written (D9); export writes the locked packages (D10). `poetry lock` keeps locked versions unless `--regenerate` (Poetry 2, D9); `poetry update` re-resolves. |
| `pipenv sync`, `pipenv install --deploy`, `--ignore-pipfile`, `pipenv requirements` | Pipfile.lock; `sync` never re-locks; `--deploy` fails on an outdated lock; `--ignore-pipfile` alone may re-lock; `requirements` writes the lock out (D11). A bare `pipenv install` has, since Pipenv 2024, updated the lock only when adding or changing a package, and before 2024 re-locked on every run (D11). |
| `pdm install`, `pdm sync`, `pdm export` | pdm.lock: `install` reuses a fresh lock and refreshes an outdated one keeping compatible pins, or creates a missing one; `sync` never writes it; `export` writes it out (D12). |
| `pip-compile`, `uv pip compile -o F` | An existing F's pins are kept unless an upgrade flag is given; without F, resolved afresh (D7, D13). |

Docker (D14 to D18): the build context is the set of files a build can access; `.dockerignore` at the context root, or `<recipe name>.dockerignore` beside the recipe, which takes precedence, removes files from it, by Go `filepath.Match` after `filepath.Clean`, with `**`, `!` exceptions and the last matching line deciding; COPY and ADD take local paths relative to the context; `COPY --exclude` leaves files out; a bind mount's source defaults to the context; BuildKit builds only the stages the target depends on; compose's `context` is relative to the project directory and `dockerfile` to the context.

## Classes of a recipe for a pair

**Terms.** A recipe's **final path** is the last stage, the one a build without `--target` produces (D16), with every stage it depends on through `FROM <stage>`, `COPY --from=<stage>` or `RUN --mount=...,from=<stage>` (D17). Where a compose file or CI workflow at the snapshot builds the recipe with a `target`, that target's path is classed as a further **build** of the recipe. An **install step** is a RUN in the final path that runs an installer (pip, pip3, `python -m pip`, uv's commands above, `uv tool install`, pipx, Poetry, Pipenv, PDM, pip-sync, pip-compile, conda, mamba or micromamba with an environment file, `python setup.py install` or `develop`), or a script, Makefile target or task-runner task in the repository that such a RUN calls, read one level deep; an ENTRYPOINT or CMD that runs `uv run` without `--no-sync`, or installs, is an install step flagged **at start**. **The project's Python requirements** are any local file or directory of the repository that a step installs from (requirements, constraints, manifest, lock, pylock.toml, an environment file's pip section, the project directory, a wheel built from it in the build), the project's own published package named from an index (the frame's package names for the repository, and any package whose source directory is in the repository, compared after PEP 503 normalisation), and L named by itself.

Each build of each recipe gets one class for the pair:

1. **From the pinned file.** Some install step in the final path takes L's version from a file in T, directly or through a file generated from it in the build by a command that keeps its versions, with that file in the build context and available to the step (below), and no later step overrides it (below). Taking L's version from a T file means: `-r`, `-c`, `pip-sync` or `uv pip sync` of the file, or of a file that includes it by `-r` or `-c` (two levels); installing the project whose manifest is in T; a lock-reading command (uv, Poetry, Pipenv, PDM as tabled) whose lock is in T, or whose manifest is in T when no lock is in the context; `pip-compile` or `uv pip compile` whose existing output file is in T, with no upgrade flag.
2. **Resolves afresh.** Some install step installs the project's Python requirements, no step takes L's version from T (or the one that did is overridden), and none takes it from another file that pins or locks L. Sub-labels: **lock unused** (a lock in T is in the context, and no step reads it); **lock absent** (a lock-reading command runs without the T lock in the context: not copied, outside the context, or excluded); **other file** (installs from a requirements or manifest file not in T); **upgrade** (a step upgrades or re-resolves L); **inline** (L named with a range). Whether the build installs L at all (directly, only through another package, or not in the groups or extras chosen) is not resolved.
3. **From the index.** The project's own published package is installed by name from an index, with or without a version, and no step takes L from T. PyPI's JSON then gives L's requirement in that release (the version named, else an ARG default, else the newest non-pre-release uploaded at or before the snapshot commit's time): **published pin** (one version), **published range**, or **not listed**.
4. **Another pinned file.** L's version comes from a file not in T that pins or locks L by LH008's rules (deeper than three directories, in a skipped directory, beyond LH008's 80-file cap, or a pylock.toml), read at the snapshot, and no step takes it from T. The image would take a pin whose moves were not timed.
5. **Nothing of the project's Python requirements.** No install step in the final path installs them as defined. Sub-labels: **no Python install**; **other named packages only**.
6. **Undetermined**, with one reason: **script not read** (an install deeper than one level of calls, or in a file outside the repository); **build argument** (a deciding file, package, installer or flag comes from an ARG with no default, or a template placeholder); **context** (the class depends on a context the rule cannot fix); **external** (a prebuilt environment, wheel or site-packages copied from an image, another file's stage or an artefact built outside the recipe decides the class); **would not build** (the recipe as read would fail at the deciding step, as `uv sync --frozen` or `COPY uv.lock` without the file); **unreadable**; **other** (with a sentence).

**Hard cases, fixed now.**

- **Multi-stage builds:** only the final path counts. A virtual environment, site-packages or wheel copied from a stage in the path carries that stage's class; an install in a stage outside the path is recorded and not counted.
- **Install steps in scripts:** a script, Makefile target or task the RUN calls is read one level deep and its install commands are classed as if in the RUN, in its working directory; deeper calls are class 6 (script not read) unless the level read already decides.
- **A lockfile exported to a requirements file:** `uv export`, `poetry export`, `pdm export`, `pipenv requirements` or pip-compile with the T output present, run in the build and then installed, is class 1 when the lock is in T and in the context. A committed exported file (a requirements file whose header says an export or compile command made it) is itself a T lockfile when it holds L, and installing it is class 1.
- **An exact pin in pyproject.toml, setup.py or setup.cfg with `pip install .` or `-e .`** (or `uv pip install .`, or uv, Poetry or PDM without a lock): the installer must satisfy `==`, so L takes the pinned version, and the class is 1 when that manifest is in T.
- **A lock not copied into the context, or excluded by `.dockerignore` or `COPY --exclude`:** class 2 (lock absent) where the command then resolves afresh; class 6 (would not build) where its flags require the lock (`--frozen`, `--locked`, `--deploy`, `pipenv sync`, `pdm sync`). `COPY . .` carries the lock only if the context holds it and does not exclude it.
- **`uv sync` without `--frozen` or `--locked`** (and without `UV_FROZEN` or `UV_LOCKED`): with the T lock in the context, class 1, flagged **may re-lock** (locked versions are kept unless the project's constraints exclude them, D4); without it, class 1 if pyproject.toml is in T, else class 2 (lock absent).
- **The project's own published package from PyPI:** class 3, never 1, since no file of the repository is read.
- **`--upgrade`:** `pip install -U -r F` still installs the version an exact pin or lock in F names. `uv lock --upgrade`, `uv sync --upgrade`, `poetry update`, `pdm update` and `pip-compile --upgrade` re-resolve: class 2 (upgrade), unless an exact pin of L in a T manifest still binds, then class 1. Upgrading pip, setuptools or wheel alone is not an upgrade of L.
- **A pinned file in a different directory from the recipe:** every path is resolved against the build context by the rule below; membership of T is by the resolved path in the repository, never by file name alone.
- **Order and override:** steps are taken in build order through the final path. A later step overrides a version of L taken from T only if it upgrades L (by name, or with `--upgrade-strategy eager` on a package that depends on L, or an upgrade flag of uv, Poetry or PDM covering L), force-reinstalls from a specifier admitting other versions, syncs the environment exactly to a set resolved without T, or names L with a specifier the pinned version does not satisfy; otherwise pip and uv keep an installed version that satisfies later requirements (D3, D7). A step from T after a fresh one gives class 1.
- **Arguments and environment:** ARG defaults and ENV values are substituted; `PIP_CONSTRAINT`, `PIP_REQUIREMENT`, `PIP_UPGRADE`, `UV_FROZEN`, `UV_LOCKED`, `UV_NO_SYNC` and `UV_CONSTRAINT` are read as their flags (D1, D8). A deciding value that only a build command gives is class 6 (build argument), unless every value that compose files and workflows at the snapshot give decides it the same way.
- **Installs at start:** classed by the same rules and flagged; a sensitivity drops recipes whose only install is at start.
- **Conda:** an environment file's pip section is read as pip requirements; a conda-level L with one version is class 4, with a range class 2.
- **Installer versions:** a bare `pipenv install` with the T lock in the context is class 1 flagged **may re-lock**, but class 2 when the recipe installs a Pipenv older than 2024 (D11). `poetry lock` without `--regenerate` is class 1 flagged, by Poetry 2's documentation (D9); where the recipe installs a Poetry older than 2.0, whose behaviour the documentation read does not describe, the build is judged and flagged **installer version**.

**Build context.** (1) A compose file or CI workflow at the snapshot that builds the recipe gives its context (compose's `context`, relative to the project directory, D18, which is taken to be the compose file's own directory, an assumption the pages read do not state, and `dockerfile`, relative to the context; a workflow's `docker build` or `buildx` path and `-f`, or docker/build-push-action's `context` and `file`); if several give different contexts, each is a build. (2) Otherwise, the recipe's own directory if every local source of COPY, ADD and bind mounts in the final path exists there at the snapshot, else the nearest ancestor directory, up to the repository root, where every one exists. (3) Otherwise the context is undetermined, and so is the class, unless the class is the same in the recipe's directory and in every ancestor. The ignore file is `<recipe name>.dockerignore` beside the recipe if present, else `.dockerignore` at the context's root (D14). A T file is **available to a step** when it is in the context, not excluded, copied (by its path, a directory holding it, or a pattern matching it) or bind-mounted into the stage before the step, and the installer's argument or working directory resolves to it after WORKDIR and the copy destinations.

**Pair class.** From all builds of the pair's primary recipes: **no recipe** when there is none; **nothing of the project's requirements** when every build is class 5; **not from the pinned file** when at least one build is class 2, 3 or 4 (called **mixed** when a class 1 build is also present); **from the pinned file** when at least one build is class 1 and every other is class 1 or 5; **undetermined** otherwise (a class 6 build and no class 2 to 4). Sensitivity: the **main recipe** alone decides: the primary recipe with fewest directories in its path, then a default name (`Dockerfile`, then `Containerfile`) before a variant, then byte order of the path.

## Missing evidence

Unknown stays unknown and is never counted as a negative.

- **Clone refused:** a clone that fails twice, at least 60 seconds apart; all the repository's pairs are **not read**.
- **Snapshot absent:** the commit does not resolve (`git rev-parse --verify <commit>^{commit}`), resolves ambiguously, or its committer time differs from `snapshot_time`; the pair is not read.
- **Tree unreadable:** the pair is not read.
- Pairs not read leave every denominator and are counted and listed by pin class, event and study; none is counted as keeping no recipe.
- A recipe that cannot be read: the pair keeps a recipe (P1), and the build is class 6 (unreadable). An ignore file, script, compose file or requirements include that cannot be read makes every class that depends on it class 6.
- A head that cannot be read leaves S2 unknown for its pairs; PyPI JSON not served leaves class 3's sub-reading unread.

## Classification and its check

1. scripts/collect.py stores, for each build of each recipe at each snapshot and head: data/recipes.csv (pair, commit, path, name form, location, primary or not, template, stages, final path, context and how it was fixed, ignore file); data/recipe_lines.csv (the FROM, ARG, ENV, WORKDIR, COPY, ADD, RUN, ENTRYPOINT and CMD lines of the final path and of any other stage that installs, each cut to 400 characters; no whole file is kept); data/aux_lines.csv (ignore-file lines, compose build stanzas, workflow lines that name the recipe, install lines of the scripts read).
2. scripts/classify.py applies these rules where every input is literal and stored: one final path, literal install arguments, a context fixed by rule (1) or (2), and membership of T decided by path. It writes class, sub-label and reason, or "to judge". Its rules are tested on synthetic recipes in scripts/test_classify.py.
3. The writer judges every "to judge" build against these rules, from the stored lines and the files the rules name at that commit only (no registry, image, issue, or general knowledge), and writes class, sub-label and a one-line reason to data/judgements.csv.
4. **Blind sample.** After every build is classed and before any measure is computed, builds are ordered by the SHA-256 of `LH015-review-20260929:` followed by pair id, commit and path; the first 30 that the script decided and the first 30 judged (all, if fewer) go to data/review_sample.csv with their stored lines, L, T and pin class, and without their class. The reviewer classes them blind. Agreement is reported per build and per resulting pair class, with each disagreement and its resolution by these rules. If, after resolution, the writer's class was wrong for more than 3 of the 30 judged builds in a way that changes a pair's class, the reviewer re-judges every judged build and the record gives both readings; if more than 3 of the 30 script-decided builds were wrong, the script is corrected, every build is classed again, and the change is recorded.

## Measures, conventions and intervals

**Primary, tested, by pair** (the repository view beside each):

- **P1:** among pairs read, the share that keep a recipe at the snapshot.
- **P2:** among pairs whose pair class is "from the pinned file" or "not from the pinned file", the share from the pinned file: over all such pairs, and for each pin class (lockfile, exact pin, both).

**Convention** (LH011's, as LH014 used it): **as a rule** at three quarters or more, **for some pairs** from one half to below three quarters, **not as a rule** below one half, applied to the share; its interval is given beside it, and where the interval spans a boundary the record says so. The labels stay in the record; a piece gives the numbers. Five labelled shares in all.

**Described with intervals, not tested:** P2's difference between exact-pin and lockfile pairs, and between exact-pin pairs and all pairs with a lockfile (lockfile and both); among pairs with a recipe, the shares "nothing of the project's requirements", "undetermined" and "mixed", and the counts of classes 2, 3 and 4 behind "not from the pinned file"; for pairs with a lockfile, the share whose recipes read the lockfile itself; the share of pairs read whose recipe would not take the pinned file ("not from the pinned file" over pairs read), the part of the timed pins that a build from the repository's own recipe would bypass.

**Repository view.** Each repository counts once: its pairs' values for a measure are averaged within it and the averages across repositories (a repository with a recipe at one of its two snapshots counts one half). Beside it, the repositories with a recipe at any and at every snapshot. If the repository view would carry a different label, the record says so.

**Secondary, described only, fixed now:**

- **S1, would a fresh build take the fix?** For pairs "not from the pinned file" where L is named in what the recipe resolves (the files and arguments of any class 2 build; for class 3, the release's requirement from PyPI), whether the specifiers of L admit the pair's fix (`pair_fix`, by PEP 440): admits, excludes, or not determined (L unnamed, only through another package, or decided by markers or extras). An estimate under the assumption that the resolver takes the newest version the specifiers admit and that nothing else in the resolution (other packages, the Python version, markers, yanked releases, another index) holds L lower. No build is made.
- **S2, head against snapshot.** The pair class at the head as cloned in phase 2, with T at the head taken as the snapshot's T paths that still exist there, and any other file a head recipe installs from checked against LH008's rules for L; a table of snapshot class against head class.
- **S3, pin moves by recipe class.** The outcomes LH008 to LH010 read (frame.csv's `outcome` and `lag_release_days`): by pair class, the counts moved, censored and removed, and the median and quartiles of the lag among movers. Those outcomes were read before this brief; this is a description fixed now, and no cause.
- **S4, mechanisms.** Installer families; lock unused against lock absent; recipes per pair; depth and name forms; templates; at-start installs; other build definitions; pairs whose only recipes lie in excluded directories.

**Sensitivities** (not tests): R1 and R2; the main-recipe pair rule; without the nine repositories LH006 or LH007 read; every build flagged "may re-lock" counted as class 2; recipes whose only install is at start dropped; P2 with every undetermined pair counted as from the pinned file, then as not.

**Intervals.** Percentile intervals at 95 per cent with LH011's `pct` (linear interpolation) over 10,000 resamples of the repositories read, with replacement, each taking all of its read pairs, drawn once as lists of repository indices from one Python `random.Random(20260929)`; every measure, view, difference and sensitivity is computed on the same resamples. A resample with an empty denominator for a measure is skipped for that measure, and the number skipped is reported. The frame is the whole of LH008 to LH010's kept pairs; the interval treats their repositories as draws from pinned repositories like them and describes repository-level variation, not sampling error within this frame. No test compares pin classes, and no difference is a cause.

## Overlap with earlier studies

- **LH008 to LH010:** the frame is entirely theirs. They read pins, locks and moves, and by their scripts no recipe. This study reads no move; S3 describes their moves by recipe class. It clones their 332 repositories again.
- **LH006 and LH007:** the nine repositories and 17 pairs named above, read at other commits; every measure is also given without them.
- **LH011 to LH014:** no download count is read, so nothing is shared, and LH013's weeks are untouched.
- A repository with several pairs counts once per pair, and the intervals are clustered by repository.

## Resource ceiling

- **Clones:** at most 664 attempts (332 repositories, one retry each), anonymous, over HTTPS. **Bytes:** at most 6 GB of clones on disk at any time, checked before each clone, and 8 GB in all, measured as each clone's size on disk after its reads, as LH008 to LH010 logged theirs; their 624 successful clones held 2.88 GB between them (their read summaries). Clones are deleted when phase 2's reads end and never enter the repository.
- **File reads:** at most 15,000 `git show` reads in all phases, logged.
- **PyPI JSON:** at most 150 requests. **Documentation:** at most 10 further pages in phases 2 and 3, logged.
- **Wall time:** collection within two hours.
- **Spend:** about nine dollars of the research agent's own model spend at list rates across the three phases, of which phase 1 was meant to use about two; the driving session measures it.
- No registry, download count, ClickPy, GitHub page or API, key or token.

## Stopping condition

Phase 2 reruns frame.py and checks frame.csv's hash before any clone; clones and reads in repository order; classifies; sets the blind sample aside; computes. It closes when every pair is read or classed missing and every build is classed, or at a ceiling, with the unread part stated. The question, frame, recipe definition, installer semantics, classes, context, override and pair rules, missing-evidence rules, measures, conventions and seed do not change after any repository is read. A case these rules do not decide is judged by the question's own test (does a build from the recipe take L's version from a timed file?) and recorded as a dated amendment naming the builds it affects, labelled as made after recipes were seen.

## What would leave it inconclusive

- Fewer than 313 of the 469 pairs read (two thirds): every measure is reported for the pairs read and called inconclusive for the frame.
- P2 over fewer than 40 pairs in 25 repositories, or a pin class's share over fewer than 20 pairs in 12 repositories: the share is given without a label.
- Undetermined pairs above one fifth of pairs with a recipe: P2's label stands only if both undetermined bounds carry it.
- The blind check failing its threshold, until the re-judging is done.
- Whatever it finds: a recipe is not a build; which recipe, if any, makes the images anyone runs is not read; whether L is installed at all (groups, extras, markers, other packages) is not resolved; build arguments beyond the snapshot's files are not followed; a class reads instructions, not installed state; nothing here gives a cause.

## Replay and intended output

studies/LH015/replay.sh reruns, offline, frame.py, classify.py with test_classify.py, and analyse.py, compares every output byte for byte, and checks the logs against these ceilings and this brief against its committed hash; judgements.csv is an input, not regenerated. The record keeps: brief.md, sources.md, LH015.md (version 0.1); data/ (frame.csv, frame_files.csv, frame_counts.csv, read_log_phase1.csv, read_log.csv, recipes.csv, recipe_lines.csv, aux_lines.csv, judgements.csv, recipe_classes.csv, pair_classes.csv, review_sample.csv, and the measures, intervals, sensitivities and secondary tables); scripts/ (frame.py, collect.py, classify.py, test_classify.py, analyse.py, common.py). Install lines only, never whole recipe files.

## What was read before this brief (phase 1)

On 29 September 2026, 15:26 to 15:33 UTC: five web searches (their queries are in sources.md; a search is not a read and is not logged); and, logged in data/read_log_phase1.csv, four arXiv abstract pages and two full texts, hadolint's DL3013 source, and nineteen documentation pages, two of them PyPI JSON descriptions (sources.md). From the repository beyond the files named in the header: LH006's and LH007's candidates tables and LH007's build table, for repository names and their Dockerfile columns. Nothing from any repository in the frame.

## Choices made by the writer

All made on 29 September 2026, before any repository in the frame was read.

1. Distinct pairs are keyed by repository, library and threshold release, and take the earliest study's row.
2. The frame is fixed in code now (scripts/frame.py) and its hash recorded, so that it can be committed with this brief.
3. T is every pinned file the earlier studies listed for the pair; all hold a version below the fix.
4. Pin class has three values; the two-way contrasts are described, not tested.
5. Recipes: Dockerfile and Containerfile names and their variants, templates, and compose's inline recipes, at any depth, outside LH008's skipped directories, `.devcontainer` and `.github`; R1 and R2 show the other choices.
6. Compose files and CI workflows are read only for contexts, files, targets and arguments.
7. The final path is the default target's; compose and workflow targets are further builds.
8. The project's own published package from an index is its own class, never "from the pinned file", with PyPI's requirement as a sub-reading.
9. A pin in a file the earlier studies did not list is its own class.
10. A bare `pipenv install` and a `uv sync` without `--frozen` or `--locked` count as from the pinned file when the lock is in the context, flagged, with a sensitivity counting them as afresh.
11. One pair is "not from the pinned file" if any of its builds resolves afresh, installs from the index or from another pin; the main recipe is the sensitivity.
12. Missing pairs are dropped from denominators and counted, never read as having no recipe.
13. The script decides only literal cases; the writer judges the rest with a reason kept; 30 and 30 builds go blind to the reviewer, chosen by a salted hash.
14. LH011's labels on P1 and P2 (five labelled shares), with the repository view beside.
15. One set of 10,000 repository resamples from `random.Random(20260929)` for every measure; no finite-population correction.
16. S1 to S4 are descriptions, and S3 is labelled as using outcomes read before this brief.
17. The nine repositories LH006 or LH007 read are kept in the frame and removed in a sensitivity.
18. Ceilings: 664 clone attempts, 6 GB of clones on disk and 8 GB in all, 15,000 file reads, 150 PyPI requests, two hours.

## Added by the driving session before the snapshot

Written on 29 September 2026 after reading this brief and before any repository in the frame was read.

1. **Sensitivity R3, the library's source not shown.** A class 2 build with the sub-label "other file" whose files (with their includes, to two levels) and arguments never name L, and a class 3 build whose release's requirement of L is "not listed", do not show that the build installs L at all. P2 is also given with such builds set aside: a pair whose only builds "not from the pinned file" are of this kind leaves P2's denominator. The record says for how many pairs "not from the pinned file" rests only on such builds. The primary P2 stays as fixed above.
2. **Who runs phases 2 and 3.** A fresh research agent on the same model, working from this brief, the frame and the files it names, because the phase 1 agent's whole context would be re-read on every call. Its judgements are "the writer's" in the rules above.
