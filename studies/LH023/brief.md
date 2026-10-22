# LH023: Exploratory Drupal 10.6 image chain

**Protocol 0.1, fixed 22 October 2026 UTC before reading this tag's production Dockerfile, current registry response or matched build logs.** Writer: Codex, GPT-6 Sol. The tag `10.6-php8.3-fpm` was selected **after** LH022's exact `11.3-php8.3-fpm` rule failed: LH022's retained official-images manifest showed a matching first stanza, GitCommit `2ecfbed5dd6aa9d5555753c0a5afb883fe8706a4`, Directory `10.6/php8.3/fpm-trixie`. This is a disclosed post hoc feasibility case, not a preselected estimate.

## Question and fixed reads

Can this known production tag's manifest commit and recipe, a public run and its resolved PHP base digest, and the current derived image artifact be linked? Use exactly the `10.6-php8.3-fpm` stanza already seen, the two Drupal source commits selected by LH022 (latest before 21 October 00:00 UTC and current head at its read), and the same 20 recent runs. Read the production Dockerfile at the official-images GitCommit, and that path at both frozen source commits if present. Inspect the run jobs of at most two runs whose head equals one of those commits after the PHP image publication; at most two job logs, only if their job is a plausible image build. Read the one derived Docker Hub tag, then its linux/amd64 manifest and config if present, with anonymous bearer handling as in LH019. Compare a log's explicit base digest to the same `php:8.3-fpm-trixie` variant only if present. A successful run without a resolved digest is unresolved.

## Boundaries and stop

Use at most 24 new GitHub and six Hub or OCI calls, 10 MiB retained bytes, two job logs; stop on rate shortage or binding ceiling. Preserve bodies, hashes, UTC times, statuses and failure cases. No layers or executable builds. If the current tag exists, its digest shows present publication, not when it first changed, and its config may omit any base reference. No deployment or pull-share measure is possible. Finish after one attempted reading at each reachable boundary and report unknowns.
