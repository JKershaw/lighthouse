# LH017 study brief

**Brief, written before any outcome was read, 30 September 2026.**

**study:** LH017
**edition:** 0.1
**status:** fixed before any repository in the frame was cloned, listed or read; its SHA-256 is posted on issue #19 before the first clone
**date opened:** 2026-09-30, after reading AGENTS.md, programme.md's Next (the checkpoint of 29 September 2026 and the notes after it), issue #19 and its comment, notes/R-0022.md and notes/R-0025.md, LH015's record (version 0.3), brief and amendments, the headers of LH015's frame and class tables, and the documentation listed in sources.md
**written by:** the driving session of 30 September 2026, in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), which is also this study's writer and judge of the cases its script leaves; the reviewers are other agents
**grounded at:** repository commit 94fbf09, with this study's uncommitted files in studies/LH017/
**issue:** #19 (JKershaw/lighthouse); programme.md, Next, "Next, for a session before 13 October"

## Question

For the repositories whose pins or lockfiles LH008, LH009 and LH010 timed, at each repository and event pair's snapshot: does the repository keep continuous-integration (CI) workflows, and does some job in them install the library's version from the file that held the pin or lock, in particular from a lockfile, including where the repository's own container recipe leaves that file unread?

**Why it is asked.** The slow road in the current account rests on pins and lockfiles in public repositories, and the frozen-list reading of what keeps older versions downloaded (LH012) is about downloads, which every install makes. LH015 read the container recipes the same repositories keep: where its rules could decide, a recipe installed from the pinned file for 129 of 167 pairs, but for 21 of 37 where a lockfile alone held the version, and a container build read a timed lockfile in 45 of 90 decided pairs with one. LH015 read the CI workflows only for the build settings they give a recipe, never for their own install steps. A CI job is a place where a project's own installs are run again and again, and installs on a CI service are the ones the download log's CI flag can mark: pip and uv send the flag when one of four environment variables, among them `CI`, is set (LH011, from the installers' source), and GitHub Actions and GitLab CI set `CI` to true in every job (G1, G6).

**What it cannot say.** A workflow is a recipe for a run, not a record of one: nothing here shows that a job ran, how often, on which events, with a cache that made no download, or against which index. The study shows whether a road runs from a pin to installs of the kind the download log's CI flag marks, and how often for these projects; it does not show how many of the log's older downloads come down that road, nor whether older downloads are frozen lists rather than unread bounds or an installer's resolution walk. It bears on the frozen-list reading and does not settle it (notes/R-0025.md). A class is a reading of instructions: what a job would be told to install, not what any run installed. Whether the job installs L at all (through extras, groups, markers or another package) is not resolved.

## What the writer already knows of the outcome, disclosed

- **LH015** (record 0.3): every figure, class and reading of its record, including the pair classes of all 469 pairs (data/pair_classes.csv, SHA-256 a120c24f5f6f5c640256d4d66ae7ff547cc070f5b9abad75a2cb1c9942eae5d5), which this study sets beside its own; the reading, made after its counts, that the gap between exact-pin and lockfile pairs lies mostly in where the pin lives, since a pin in a manifest is read by any install of the project, one in a requirements file by an install that names that file, and a lockfile only by lock-aware commands; and that its 68 undetermined pairs lie in 32 repositories, 26 of them in four.
- **LH015's reads of the same workflows.** LH015 read 1,292 workflow files in 145 repositories, at snapshots and heads, for the context, file, target and arguments they give a recipe (its data/read_log.csv), and kept 4,926 lines of 120 files in 73 repositories that name a recipe or give its build settings (its data/aux_lines.csv). The writer counted those files and lines and has read none of them; this study's classifier does not use them.
- **LH006 and LH007** read the workflows of their own repositories, nine of which are in this frame, for image references, at other commits (LH006, Method); no install step was classed.
- **The literature and documentation** (sources.md): uv's own guide to GitHub Actions installs with `uv sync --locked` (U1); setup-python caches pip, Pipenv and Poetry downloads and installs no project requirements (A1); tox installs the project itself unless told not to (T1); tox-uv's lock runner installs from uv.lock (T2). A scan of the workflows of about 343,000 repositories linked from PyPI, in May 2026, found 152,000 with GitHub workflows, Travis CI in 11 per cent and every other CI system below 2 per cent, and astral-sh/setup-uv in about 17,000 (L1). A study of 952 repositories found 266 that cache in their GitHub workflows and 686 that do not (L2), and a study of 49,000 repositories a median of three workflow files each (L3); neither abstract measures which files an install step reads. None of these is a reading of this frame.
- **An expectation, not a reading.** From general knowledge of how projects that use uv or Poetry lay out their CI, the writer expects some CI job to read the lockfile more often than LH015's container recipes did. No figure is expected, and no class is assigned from general knowledge.
- The writer has listed no tree and read no file or commit of any frame repository.

## Population and unit

- **Frame.** LH015's frame, unchanged: data/frame.csv (SHA-256 83eb0f6b751af7a26c4939cd0d49349214390eab9a9a06a8fe85f1e37f523384) and data/frame_files.csv (SHA-256 29b75f95320767e482ad4192a43c465d107b022ed1c34b7a346873ba2896e074), copied from studies/LH015/data/ by scripts/frame.py, which checks both hashes: **469 pairs, 332 repositories, 40 events**, with no new selection. A pair is (repository, library L, threshold release); its snapshot is the last first-parent commit on the default branch at or before the release, as LH008 to LH010 defined it; its **timed files (T)** are the files that pinned or locked L at the snapshot as those studies read them; its **pin class** is lockfile (153), exact pin (199) or both (117).
- **Unit.** The pair, as in LH015, with the distinct repository beside it (Measures). A repository with several pairs counts once per pair, and intervals are clustered by repository.
- **Snapshot check.** The pair's `snapshot_commit` must resolve uniquely in the clone with a committer time equal to `snapshot_time` as an instant; no other commit stands in for it.
- **Heads are not read.** Only snapshots are read.

## Sources and reads in phase 2

- **Git over HTTPS, anonymously.** One blobless clone per repository, `git clone --filter=blob:none --no-checkout https://<repo>.git`, as LH015 made them. Files are listed with `git ls-tree -r --name-only <commit>` and read with `git show <commit>:<path>`; every clone, retry and file read is logged in data/read_log.csv.
- **Read at each snapshot:** the tree listing; every CI file this study classes (below); every file a classed job's install step calls or names, one level deep: local composite actions' `action.yml` or `action.yaml`, shell scripts, Makefile and justfile targets, tox, nox and hatch configuration, requirements and constraints files (with their `-r` and `-c` includes, two levels), conda environment files, and the manifests and lockfiles at the directories an install step resolves to; and, for the secondary measure S5 only, README and CONTRIBUTING files at the repository root.
- **PyPI's JSON API** (https://pypi.org/pypi/<name>/json) only for jobs that install the project's own published package by name, for L's requirement in that release, as LH015 read it.
- **Not read:** any run of any workflow (GitHub's API, run logs and web pages), any registry or image, any download count (ClickPy is not used, so nothing of LH013's weeks is read), OSV, Open Source Insights, and LH015's retained workflow lines. No account, key or token.

## What counts as CI

- **Classed:** GitHub Actions workflow files, `.github/workflows/<name>.yml` or `.yaml` directly in that directory, where GitHub requires them (G2); and GitLab CI's `.gitlab-ci.yml` at the repository root with the files it includes by `include: local:` or by a plain local path (G5), one level. The Nesbitt scan (L1) found every CI system other than GitHub Actions and Travis CI below 2 per cent of the repositories it read.
- **Counted and listed, not classed:** `.travis.yml`, `.circleci/config.yml`, `azure-pipelines.yml` and `.azure-pipelines/`, `Jenkinsfile`, `bitbucket-pipelines.yml`, `appveyor.yml` and `.appveyor.yml`, `.buildkite/`, `.drone.yml`, `.woodpecker.yml` and `.woodpecker/`, `cloudbuild.yaml`, `.cirrus.yml`, `.semaphore/semaphore.yml`, and `.gitea/workflows/` and `.forgejo/workflows/`. A pair whose only CI files are of these kinds is **other CI only**, never "no CI".
- **A job.** In a GitHub workflow, each entry under `jobs:` that has `steps:`; an entry that calls a reusable workflow with `uses:` is a **call**, not a job, and a called workflow in the same repository is read with the caller's `with:` inputs. In GitLab CI, each top-level mapping with a `script:`, after `extends:` is merged one level, whose name does not begin with `.` and is not a global keyword; its commands are `before_script` (its own, else `default:`'s) and then `script`. A workflow that does not parse is one job of class 6 (unreadable).
- **Variants.** A job whose install steps use a matrix value (`${{ matrix.<key> }}`, GitLab's `parallel: matrix`) is expanded over its literal matrix, with `include` and `exclude` applied as GitHub documents them (G2), and each distinct sequence of install commands is one **variant**; a matrix given by an expression makes the job class 6 (build argument). A job without matrix-dependent installs is one variant. "Job" below means a variant.
- **Reusable workflows.** A workflow whose only trigger is `workflow_call` is classed once per distinct set of inputs its callers in the repository give it, or with its inputs' defaults if no caller in the repository calls it. A call to a reusable workflow in another repository is a job of class 6 (external).

## Steps, files and working directories

- **Install step.** A step, taken in the job's order, that (a) runs a command of the installer table below: pip, pip3, `python -m pip`, uv's commands (`uv pip install`, `uv pip sync`, `uv pip compile`, `uv sync`, `uv run`, `uv export`, `uv lock`, `uv add`), `uv tool install`, uvx, pipx, Poetry, Pipenv, PDM, pip-sync, pip-compile, conda, mamba or micromamba with an environment file, `python setup.py install` or `develop`; (b) runs tox, nox or hatch (`hatch run`, `hatch test`, `hatch env create`, `hatch shell`), read as below; (c) runs a Makefile or justfile target, read one level with the prerequisites it names and the targets its recipe calls with make, one level each, or a shell script in the repository (called by path, or with sh, bash or source), read one level, whose install commands are classed as if in the step at the step's working directory, deeper calls being class 6 (script not read) unless the level read already decides; or (d) uses an action: a local composite action (`uses: ./<path>`), read one level with its inputs substituted, whose steps are classed in place; conda-incubator/setup-miniconda, mamba-org/setup-micromamba or mamba-org/provision-with-micromamba with an `environment-file` (A5, A6), read as an install from that file; or another external action whose inputs name a local requirements, constraints, lock, manifest or environment file, or the project directory, for it to install, which is class 6 (external).
- **Not install steps.** actions/checkout, setup-python (A1), setup-uv (A2), snok/install-poetry (A3), pdm-project/setup-pdm (A4) and actions that only install a tool or a Python, whose cache settings are recorded (S2); actions/cache; upload and download of artefacts; a Python script the step runs (not read: a limit); and pre-commit, whose hooks are installed from their own repositories into isolated environments (P1), which counts as other named packages. A **container build** (`docker build`, `docker buildx build`, `docker compose build`, `podman build`, docker/build-push-action, docker/bake-action) is recorded and is not an install step: the installs inside it are the recipe's, which LH015 classed, and Docker's documentation describes build arguments and environment variables as declared in the Dockerfile and set with the build command's flags (D1). On that reading, which the page does not state in these words, a build's own installs see the runner's `CI` only where the recipe or the command passes it; neither is checked here.
- **Files available to a step.** In a GitHub job, the repository's files at the snapshot are available after a step that uses actions/checkout without a `repository:` input naming another repository, in the directory its `path:` input names; before such a step, or in a job without one, no repository file is available, and an install step that names one is class 6 (would not run). A checkout whose `ref:` names another branch, tag or commit leaves the job to be judged. In a GitLab job they are available unless `GIT_STRATEGY` is `none`.
- **Working directory.** The checkout's root, changed by `defaults.run.working-directory` (the workflow's, then the job's), a step's `working-directory` (G2), and a literal `cd`, `pushd` or `popd` within a run script, taken in order; a `cd` to a value the rules cannot substitute leaves the rest of that script's directory undetermined. Every path is resolved against the working directory, and membership of T is by the resolved path in the repository, never by file name alone.
- **Expressions and variables.** `${{ matrix.* }}` from the variant; `${{ inputs.* }}` from the callers or defaults; `${{ env.* }}` and `$VAR` from literal `env:` values of the workflow, job and step; `${{ github.workspace }}` as the checkout root. Anything else (`secrets`, `vars`, `steps.*.outputs`, `needs.*.outputs`, `runner`, other `github.*` values) is unknown, and a job whose class depends on it is class 6 (build argument). `PIP_CONSTRAINT`, `PIP_UPGRADE`, `UV_FROZEN`, `UV_LOCKED`, `UV_NO_SYNC` and `UV_CONSTRAINT` are read as their flags (LH015's D1, D8).
- **Conditions.** A step or job with an `if:` condition is classed as if it runs; the number of pairs whose class rests on a conditional step is reported.

## How installers treat a pinned or locked file

LH015's table (its brief, "How installers treat a pinned or locked file", from its sources D1 to D13) holds unchanged: pip's `-r` and `-c` read the named file and its includes; installing the project reads its manifest and no lockfile, and an exact pin there admits one version; uv's `sync` and `run` read uv.lock where present, keeping locked versions unless the project's constraints exclude them, with `--locked`, `--frozen`, `--upgrade` and the environment variables as tabled, and resolve pyproject.toml afresh without it; `poetry install` and `sync` read poetry.lock where present; Pipenv's `sync`, `install --deploy` and `--ignore-pipfile` read Pipfile.lock; PDM's `install` and `sync` read pdm.lock; pip-compile and `uv pip compile` keep an existing output's pins without an upgrade flag. Added for CI, from the pages read for this brief:

| Command | What it reads, and where L's version comes from |
| --- | --- |
| tox (`tox`, `tox -e`, `tox run`, `python -m tox`, uvx or pipx running tox) | The environments named, else `env_list`: each installs its `deps` (pip requirement lines, so `-r F` and `-c F` read F), its `constraints` files, and the project itself by building it (`package`, default a wheel or sdist), which reads the manifest; `skip_install = true` or `package = skip` installs no project, `deps-only` the project's dependencies from its manifest, and `use_develop` or `package = editable` the project in editable mode (T1). Configuration is read from tox.ini, tox.toml, `[tool.tox]` in pyproject.toml or `[tox:tox]` in setup.cfg; a factor-conditional line counts as possibly installed. |
| tox with tox-uv's `runner = uv-venv-lock-runner` | `uv sync` with uv.lock: "all dependencies will come from the lock file", and `deps` are ignored (T2). |
| nox (`nox`, `nox -s`, `python -m nox`, uvx or pipx running nox) | The sessions named, else those in `nox.options.sessions`, else every session: `session.install(...)` invokes pip (or uv, by backend) in the session's environment, with `-r F`, `.` and names read as pip reads them (N1); `session.run_install(...)` and `session.run(...)` of an installer are read as that command; `session.conda_install` as conda. Arguments that are not literal strings leave the session to be judged. |
| hatch (`hatch run`, `hatch test`, `hatch env create`, `hatch shell`) | The environment named (default `default`; `hatch test` its internal test environment, H2) installs the project in development mode unless `skip-install` or `dev-mode = false` (H1), which reads the manifest, and its `dependencies`, `extra-dependencies` and `features`; with `locked = true` a pylock.toml, which LH008's rules never listed in T (H1). |
| make, just, shell scripts | Their install lines, read one level as above. |
| conda-incubator/setup-miniconda, mamba-org/setup-micromamba with `environment-file` | The environment file: its pip section read as pip requirements; a conda-level L with one version is class 4, with a range class 2, as in LH015. |
| pre-commit (`pre-commit run`, pre-commit/action) | Each hook's own repository, in an isolated environment (P1): other named packages. |

## Classes of a job for a pair

**The project's Python requirements** are LH015's: any local file or directory of the repository that a step installs from (requirements, constraints, manifest, lock, pylock.toml, an environment file's pip section, the project directory, a wheel or sdist built from it in the job or in a job of the same workflow that it needs), the project's own published package named from an index (the frame's package names for the repository, and any package whose source directory is in the repository, after PEP 503 normalisation), and L named by itself. Each job gets one class for the pair:

1. **From the pinned file.** Some install step takes L's version from a file in T, directly or through a file generated from it in the job by a command that keeps its versions, with that file available to the step, and no later step overrides it. Taking L's version from a T file means, as in LH015: `-r`, `-c`, `pip-sync` or `uv pip sync` of the file or of a file that includes it by `-r` or `-c` (two levels); installing the project whose manifest is in T; a lock-reading command whose lock is in T, or whose manifest is in T when no lock applies; `pip-compile` or `uv pip compile` whose existing output file is in T, with no upgrade flag; and, for CI, a tox environment, nox session or hatch environment that does one of these. The deciding T file or files are recorded, with their kind (lockfile or exact pin).
2. **Resolves afresh.** Some install step installs the project's Python requirements, no step takes L's version from T (or the one that did is overridden), and none takes it from another file that pins or locks L. Sub-labels, the first that applies reported: **upgrade** (a step upgrades or re-resolves L); **lock absent** (a lock-reading command runs where no lock applies); **lock unused** (a lock in T is in the checkout and no step reads it); **other file** (installs from a requirements or manifest file not in T); **inline** (L named with a range or none).
3. **From the index.** The project's own published package is installed by name from an index, and no step takes L from T; PyPI's JSON gives L's requirement in that release as LH015 read it (published pin, published range, not listed).
4. **Another pinned file.** L's version comes from a file not in T that pins or locks L by LH008's rules, read at the snapshot, or from an exact pin of L on the command line (**inline pin**), and no step takes it from T.
5. **Nothing of the project's Python requirements.** No install step installs them. Sub-labels: **no Python install**; **other named packages only**; **container build only** (the job's only link to them is a container build).
6. **Undetermined**, with one reason: **script not read** (an install deeper than the level read, or in an external reusable workflow); **build argument** (a deciding value is an expression or variable the rules cannot substitute); **external** (an external action, a call to another repository's workflow, or an artefact from outside the job and its needs decides); **would not run** (the step as read would fail at the deciding point: a lock-requiring flag without the lock, a named file absent, a local install without a checkout); **unreadable**; **other** (with a sentence).

**Precedence and override.** A job is class 1 if a step takes L's version from T and no later step overrides it; else class 4 if a step takes it from another pinned file; else class 3 if a step installs the project's own package from an index; else class 2 if a step installs the project's requirements; else class 5; and class 6 in place of 2 to 5 when a step the rules cannot decide could have made it class 1. A later step overrides a version of L taken from T only as LH015's rule says (it upgrades L, force-reinstalls it from a specifier admitting other versions, syncs the environment exactly to a set resolved without T, or names L with a specifier the pinned version does not satisfy); a later step the rules cannot read does not undo class 1, and such jobs are flagged and counted.

**Hard cases, fixed now.** LH015's hard cases hold where they apply to CI: a `uv sync` or `uv run` without `--frozen` or `--locked` with the T lock applying is class 1 flagged **may re-lock**, as is a bare `pipenv install` (class 2 where a Pipenv older than 2024 is installed by a pinned version) and `pdm install`; `poetry lock` without `--regenerate` is class 1 flagged, and judged and flagged **installer version** where a Poetry older than 2.0 is installed by a pinned version; `pip install -U -r F` still installs what an exact pin or lock in F names; a committed exported requirements file that holds L is itself a T lockfile when LH008 listed it. For CI:

- **Which lock applies.** uv's lock is uv.lock in the directory of the nearest pyproject.toml at or above the working directory (or the directory `--project` or `--directory` names), or in the workspace root's directory where that pyproject.toml is a member of a uv workspace; Poetry's and PDM's the lock beside the pyproject.toml they use; Pipenv's the Pipfile.lock beside the Pipfile.
- **A wheel or sdist built from the project** in the job, or in a job of the same workflow that the job needs and whose artefact it downloads, and then installed with pip or uv, installs the project from its manifest; one whose origin the rules cannot trace is class 6 (external).
- **L named by itself.** `pip install L` with a range or none is class 2 (inline); `pip install L==V` is class 4 (inline pin); for pairs whose library is pip, setuptools or poetry, upgrading or installing that tool by name counts as installing L.
- **Job containers.** An install in a job that runs in a `container:` is classed like any other; what the image already holds is not read.
- **An install inside `docker run`** on the runner is classed by the same rules and flagged, since the container sees the runner's `CI` only if the command passes it.

## Pair class

From all jobs at the pair's snapshot:

- **no CI**: no classed job (sub-labels: **other CI only**, **none**);
- **reads the pin**: at least one job is class 1 (**mixed** where another job is class 2, 3 or 4);
- **does not read the pin**: no job is class 1 or 6, and at least one is class 2, 3 or 4;
- **nothing of the project's requirements**: every job is class 5;
- **undetermined**: no job is class 1, and at least one is class 6.

Unlike LH015's pair rule, one class 1 job suffices, because the question here is whether a road runs from the pin to CI installs, not whether any build bypasses the pin; LH015's rule is a sensitivity. **For the lock** (pairs with a timed lockfile, pin class lockfile or both): **reads the timed lock** when some class 1 job's deciding T file is a lockfile; **does not** when no job reads a T lock, no job is class 6, and at least one is class 1 to 4; **undetermined** when no job reads a T lock and at least one is class 6; pairs with no CI, or whose CI installs nothing of the project's requirements, are outside it and counted.

## Missing evidence

Unknown stays unknown and is never counted as a negative.

- **Clone refused:** a clone that fails twice, at least 60 seconds apart; all the repository's pairs are **not read**.
- **Snapshot absent:** the commit does not resolve, resolves ambiguously, or its committer time differs from `snapshot_time`; the pair is not read.
- **Tree unreadable:** the pair is not read.
- Pairs not read leave every denominator and are counted and listed by pin class, event and study; none is counted as keeping no CI.
- A CI file that cannot be read or parsed: the pair keeps CI, and the file is one job of class 6 (unreadable). A called file that cannot be read makes every class that depends on it class 6.
- PyPI JSON not served leaves class 3's sub-reading unread.

## Classification and its check

1. scripts/collect.py clones, verifies each snapshot, lists its tree, reads the CI files and the files their install steps call or name, and stores, for each job at each snapshot: data/ci_files.csv (the CI files classed and counted per pair); data/jobs.csv (each job and variant: file, job, triggers, checkout, container, cache settings, container builds); data/ci_lines.csv (the job's install-relevant lines only, each cut to 400 characters: run lines that hold an installer, task runner, script call, `cd` or container build, the `uses:` and `with:` of actions, and the `env`, `defaults`, `working-directory` and matrix values those lines use; no whole file is kept); data/aux_lines.csv (the relevant lines of the files called or named: Makefile targets, script install lines, tox, nox and hatch settings, requirements includes); data/file_facts.csv (for every file read that could pin or lock L, whether it does by LH008's rules, and at which versions); and data/tree_paths.csv (every existence query made against a tree).
2. scripts/classify.py applies these rules offline to those stored records where every input is literal, and writes class, sub-label, reason and deciding files, or "to judge". Its rules are tested on synthetic workflows in scripts/test_classify.py.
3. The writer judges, from the stored lines and the files the rules name at that commit only (no run, registry, issue, web page or general knowledge), every "to judge" job in a pair where it could change the pair class or the reading for the lock: a pair with no class 1 job, or, for the lock, with no job reading a T lock. Other "to judge" jobs stay class 6, flagged **not judged: cannot change a primary measure**, and count as undetermined in every description. Each judgement is written with a one-line reason to data/judgements.csv.
4. **Blind sample.** After every job is classed and before any measure is computed, jobs are ordered by the SHA-256 of `LH017-review-20260930:` followed by pair id, file path, job and variant joined by colons; the first 20 decided by the script and the first 20 judged (all, if fewer) go to data/review_sample.csv with their stored lines, L, T and pin class, and without their class. A reviewer who has not seen the classes classes them blind. Agreement is reported per job and per resulting pair class, with each disagreement and its resolution by these rules. If, after resolution, the writer's class was wrong for more than 2 of the 20 judged jobs in a way that changes a pair's class, the reviewer re-judges every judged job and the record gives both readings; if more than 2 of the 20 script-decided jobs were wrong, the script is corrected, every job is classed again, and the change is recorded.

## Measures, conventions and intervals

**Primary, tested, by pair** (the repository view beside each):

- **P1:** among pairs read, the share that keep at least one classed CI job at the snapshot.
- **P2:** among pairs whose class is "reads the pin" or "does not read the pin", the share that reads the pin: over all such pairs, and for each pin class (lockfile, exact pin, both).
- **P3:** among pairs with a timed lockfile whose CI is decided for the lock, the share whose CI reads the timed lock.

**Convention** (LH011's, as LH014 and LH015 used it): **as a rule** at three quarters or more, **for some pairs** from one half to below three quarters, **not as a rule** below one half, applied to the share; its interval is given beside it, and where the interval spans a boundary the record says so. The labels stay in the record; a piece gives the numbers. Six labelled shares in all.

**Described with intervals, not tested:**

- **Beside LH015, pair by pair.** For each of LH015's pair classes (from the pinned file, not from the pinned file, undetermined, nothing of the project's requirements, no recipe), the counts of this study's pair classes; for LH015's 38 pairs "not from the pinned file", and the pairs whose recipes had a "lock unused" build, the share whose CI reads the pin, and for those with a timed lockfile, the lock; for pairs with a timed lockfile decided in both studies, the two-way table of "a container build reads the timed lock" (LH015's `reads_T_lock`) against "a CI job reads it".
- **Either and neither.** Among pairs read, the share where a container build (LH015 class 1) or a CI job (class 1) installs from the pinned file; and the share where both are decided and neither does, which is the part of the timed pins that no build the repository defines, recipe or workflow, would read.
- **Within the pair classes:** among pairs that read the pin, the share **mixed**; among pairs with CI, the shares "nothing of the project's requirements" and "undetermined"; the counts of classes 2, 3 and 4 behind "does not read the pin", by sub-label.
- **Per job and per workflow.** The share of decided jobs that are class 1, and of workflows with a class 1 job, beside the pair's share, since repositories keep very different numbers of jobs (as LH015 gave its shares per build and per recipe after R-0022).

**Repository view.** Each repository counts once: its pairs' values for a measure are averaged within it and the averages across repositories. Beside it, the repositories with CI at any and at every snapshot. If the repository view would carry a different label, the record says so.

**Secondary, described only, fixed now:**

- **S1, mechanisms.** Installer and task-runner families among the steps that decide class 1 and class 2; lock-reading commands with and without `--locked` or `--frozen`; "may re-lock" jobs; tox, nox, hatch, make and script levels; jobs judged.
- **S2, what the log could see.** For pairs that read the pin, whether a deciding install is made by pip or uv, which send the CI flag (LH011), or only by Poetry, PDM or conda, whose flag the log does not carry or whose packages come from elsewhere; and whether the job restores an installer cache (setup-python's `cache` input, setup-uv's `enable-cache` as written, with its default recorded as "auto", an actions/cache step whose path holds a pip, uv, Poetry or PDM cache), which says only whether a fetch could miss the index, not whether one did.
- **S3, triggers.** For pairs that read the pin, whether some class 1 job's workflow runs on `push` or `pull_request`, or only on releases, tags, schedules, dispatch or calls; GitLab jobs are counted apart.
- **S4, container builds in CI.** Pairs with a CI job that builds a container, set beside LH015's recipe class.
- **S5, documented install commands.** For each pair, the classes of the install commands in the README and CONTRIBUTING files at the repository root, in fenced or indented code blocks or after a shell prompt, classed by the script at the repository root, with no judging; undecided commands are counted as undetermined. What a person following the project's own instructions would be told to install, which installs not flagged as CI could follow.
- **S6, pin moves by CI class.** The outcomes LH008 to LH010 read (frame.csv's `outcome` and `lag_release_days`), by pair class: counts moved, censored and removed, and the median and quartiles of the lag among movers. Those outcomes were read before this brief; this is a description, and no cause is read from it.

**Sensitivities** (not tests): routine jobs only (GitHub workflows triggered by `push` or `pull_request`, and GitLab jobs); LH015's pair rule (reads the pin only when every other job is class 1 or 5); every "may re-lock" job counted as class 2; P2 and P3 with every undetermined pair counted as reading, then as not; P1 with "other CI only" pairs counted as keeping CI.

**Intervals.** Percentile intervals at 95 per cent with LH011's `pct` (linear interpolation) over 10,000 resamples of the repositories read, with replacement, each taking all of its read pairs, drawn once as lists of repository indices from one Python `random.Random(20260930)`; every measure, view, difference and sensitivity is computed on the same resamples. A resample with an empty denominator is skipped for that measure, and the number skipped is reported. The interval treats the repositories as draws from pinned repositories like them and describes repository-level variation, not sampling error within this frame. No test compares pin classes or studies, and no difference is a cause.

## Overlap with earlier studies

- **LH008 to LH010:** the frame is entirely theirs, as it was LH015's; their 332 repositories are cloned again. S6 describes their moves by CI class.
- **LH015:** the same frame and snapshots. Its pair classes are read, as disclosed above, only for the comparisons fixed here. Its reads of 1,292 workflow files in 145 repositories were for build settings; the install steps of those files are classed here for the first time, and its retained lines are not used.
- **LH006 and LH007:** nine frame repositories, read at other commits for images and image references; not used.
- **LH011 to LH014:** no download count is read, so nothing is shared, and LH013's weeks are untouched.

## Resource ceiling

- **Clones:** at most 664 attempts (332 repositories, one retry each), anonymous, over HTTPS. **Bytes:** at most 6 GB of clones on disk at any time, and 8 GB in all, measured as each clone's size on disk after its reads. Clones are deleted when phase 2's reads end and never enter the repository.
- **File reads:** at most 20,000 `git show` reads, logged.
- **PyPI JSON:** at most 60 requests. **Documentation:** at most 10 further pages, logged.
- **Wall time:** collection within two hours.
- **Spend:** the collection, classification and record are the driving session's; its own spend is measured with `harbour/hb drivercost`. Review is by other agents inside the drive's bound of twenty dollars of subagent spend at list rates: the blind check and the evidence review by a reviewer on Fable 5.1, within about ten dollars, and the reader-and-inference review with its recheck within its allowance of seven. If the bound cannot hold both, the record says what was cut.
- No registry, download count, ClickPy, GitHub page or API, key or token.

## Stopping condition

Phase 2 checks the frame's hashes before any clone; clones and reads in repository order; classifies; judges; sets the blind sample aside; computes. It closes when every pair is read or classed missing and every job is classed, or at a ceiling, with the unread part stated. The question, frame, CI definition, installer semantics, classes, context, override and pair rules, missing-evidence rules, measures, conventions and seed do not change after any repository is read. A case these rules do not decide is judged by the question's own test (does a job take L's version from a timed file?) and recorded as a dated amendment naming the jobs it affects, labelled as made after workflows were seen.

## What would leave it inconclusive

- Fewer than 313 of the 469 pairs read (two thirds): every measure is reported for the pairs read and called inconclusive for the frame.
- P2 over fewer than 40 pairs in 25 repositories, or a pin class's share, or P3, over fewer than 20 pairs in 12 repositories: the share is given without a label.
- Undetermined pairs above one fifth of the pairs in a primary measure's frame (pairs with CI that installs the project's requirements, for P2; pairs with a timed lockfile and such CI, for P3): the label stands only if both undetermined bounds carry it.
- The blind check failing its threshold, until the re-judging or the correction is done.
- Whatever it finds: a workflow is not a run; whether, how often and with what cache a job ran is not read; whether L is installed at all is not resolved; values only a run supplies are not followed; a class reads instructions, not installed state; nothing here counts downloads or gives a cause.

## Replay and intended output

studies/LH017/replay.sh reruns, offline, frame.py (with its hash checks), classify.py with test_classify.py, and analyse.py, compares every output byte for byte, and checks the logs against these ceilings and this brief against the hash posted on issue #19; judgements.csv is an input, not regenerated. The record keeps: brief.md, sources.md, LH017.md; data/ (frame.csv, frame_files.csv, read_log_phase1.csv, read_log.csv, pairs_read.csv, ci_files.csv, jobs.csv, ci_lines.csv, aux_lines.csv, file_facts.csv, tree_paths.csv, judgements.csv, job_classes.csv, pair_classes.csv, review_sample.csv, pypi.csv, and the measures, intervals, sensitivities and secondary tables); scripts/ (frame.py, collect.py, classify.py, test_classify.py, analyse.py, common.py). Install-relevant lines only, never whole files.

## What was read before this brief

On 30 September 2026, 06:50 to 06:52 UTC, logged in data/read_log_phase1.csv: twenty-two documentation pages and one blog post, and at 07:01 UTC two arXiv abstract pages (sources.md), after five web searches (their queries are in sources.md; a search is not a read). From the repository: the files named in the header, LH015's data/frame.csv, frame_files.csv and pair_classes.csv (their headers, and counts by library, pin class and pair class), and the counts of files, rows and repositories in LH015's data/read_log.csv and data/aux_lines.csv, without reading their lines. Nothing from any repository in the frame.

## Issue #19's design, as taken here

- **Frame, reads, classes, measures:** as the issue proposed, with P3 added for the lockfile, since the issue's title asks about "the lockfile or pin".
- **What it cannot say about downloads, per repository, and the disclosure of LH015's reads:** as notes/R-0025.md and the issue's comment asked, above.
- **The context rule for LH015's recipes** (how a bare `.` source and an unmatched wildcard set a build's starting folder) is not taken here. It is a repair of LH015's own measure, not a reading of CI, and it cannot lift LH015's withheld label: with all 13 pairs it would decide counted as decided, LH015's undetermined pairs would still be 55 of 247, 22.3 per cent, above the one fifth that withholds P2's label. It stays in LH015's Next.
- **Documented install commands** are read for a secondary description (S5), classed by the script alone.

## Choices made by the writer

All made on 30 September 2026, before any repository in the frame was read.

1. The frame is LH015's, copied with its hashes checked; heads are not read.
2. GitHub Actions and GitLab CI are classed; other CI systems are counted and listed, and a pair with only those is "other CI only".
3. The unit of classification is the job, expanded into variants only where a matrix value reaches an install step.
4. One class 1 job makes the pair "reads the pin"; LH015's stricter rule is a sensitivity.
5. P3, the lock, is primary beside P2, because a pin in a manifest is read by any install of the project and a lockfile only by lock-aware commands.
6. Scripts, Makefile and justfile targets, local actions and task-runner configurations are read one level; Python scripts a step runs are not read.
7. Conditions are not evaluated; conditional steps are classed as if they run, and counted.
8. A later step the rules cannot read does not undo class 1, and such jobs are flagged and counted.
9. Container builds in CI are recorded, not classed as installs; LH015 classed their recipes.
10. The writer judges only the jobs that could change a pair's class or its reading for the lock; the rest stay undetermined and flagged.
11. The blind sample is 20 script-decided and 20 judged jobs, with a threshold of more than 2 wrong of 20, the same proportion as LH015's 3 of 30, to fit the round's bound.
12. LH011's labels on P1, P2 and P3 (six labelled shares), with the repository view beside.
13. One set of 10,000 repository resamples from `random.Random(20260930)`; no finite-population correction.
14. S1 to S6 are descriptions; S6 is labelled as using outcomes read before this brief.
15. The context rule for LH015's recipes is left to LH015, for the reason above.
16. Ceilings: 664 clone attempts, 6 GB of clones on disk and 8 GB in all, 20,000 file reads, 60 PyPI requests, two hours.
