# LH000 observation records

Field names follow the observation record in LH F05 (Lighthouse_Study_Templates.md). One row per host reading taken by hand during this study; the take record Harbour returned for the dispatch itself is quoted and tabulated separately in LH000.md's Findings, since it was handed to this study rather than sampled by it.

Two samples were taken, both from inside this container, using `date -u +%FT%TZ`, `cat /proc/loadavg`, `nproc`, `ps -eo pid,pcpu,pmem,etimes,comm --sort=-pcpu | head -12` and a count of lines with TCP state code `01` (ESTABLISHED) in `/proc/net/tcp`, since neither `ss` nor `netstat` is installed in this container. Full raw output for each sample is quoted below the table.

`clock_uncertainty` is left as unknown throughout: the five commands in one sample ran back to back in a single shell invocation and were not individually timestamped, so no specific figure can be given without inventing one. `lighthouse_traffic` is left as unknown throughout for the same reason given in Limits: this container is not yet instrumented to separate Lighthouse's own collection activity from the sandbox's own supervisor processes and the harness's other connections, so a true or false value cannot be assigned without guessing.

| observation_id | study | instrument | source_ref | entity_id_or_connection_id | event_start | event_end | collected_at | clock_uncertainty | metric | unit | value | status | kind | attribution_basis | missingness_flag | lighthouse_traffic |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OBS-000001 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-1.txt | container-host | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | unknown | load_average_1m | load | 0.02 | observed | gauge | read directly from /proc/loadavg inside the container | none | unknown |
| OBS-000002 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-1.txt | container-host | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | unknown | runnable_to_total_tasks | ratio | 1/115 | observed | gauge | third field of /proc/loadavg | none | unknown |
| OBS-000003 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-1.txt | container-host | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | unknown | cpu_count | cores | 4 | observed | gauge | read from nproc inside the container | none | unknown |
| OBS-000004 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-1.txt | container-host | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | unknown | established_tcp_connections_ipv4 | count | 23 | observed | gauge | lines with tcp state code 01 in /proc/net/tcp; not attributed to individual processes or peers | none | unknown |
| OBS-000005 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-1.txt | container-host | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | 2026-09-25T22:23:16Z | unknown | established_tcp_connections_ipv6 | count | | unknown | gauge | /proc/net/tcp6 does not exist in this container | instrument path absent: no IPv6 /proc entry in this container | unknown |
| OBS-000006 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-2.txt | container-host | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | unknown | load_average_1m | load | 0.01 | observed | gauge | read directly from /proc/loadavg inside the container | none | unknown |
| OBS-000007 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-2.txt | container-host | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | unknown | runnable_to_total_tasks | ratio | 1/114 | observed | gauge | third field of /proc/loadavg | none | unknown |
| OBS-000008 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-2.txt | container-host | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | unknown | cpu_count | cores | 4 | observed | gauge | read from nproc inside the container | none | unknown |
| OBS-000009 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-2.txt | container-host | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | unknown | established_tcp_connections_ipv4 | count | 21 | observed | gauge | lines with tcp state code 01 in /proc/net/tcp; not attributed to individual processes or peers | none | unknown |
| OBS-000010 | LH000 | host sample by hand v0 | scratchpad/lh000-study/host-sample-2.txt | container-host | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | 2026-09-25T22:28:32Z | unknown | established_tcp_connections_ipv6 | count | | unknown | gauge | /proc/net/tcp6 does not exist in this container | instrument path absent: no IPv6 /proc entry in this container | unknown |

`source_ref` gives the path inside this session's scratch directory (full path `/tmp/claude-0/-home-user-lighthouse/e91cb0fc-8f0f-5bdf-ba6f-2514687a2e5c/scratchpad/lh000-study/`), not inside this repository. That directory does not survive the session, so the quoted text below is this record's durable copy.

## Sample 1, collected 2026-09-25T22:23:16Z

```
$ date -u +%FT%TZ
2026-09-25T22:23:16Z

$ cat /proc/loadavg
0.02 0.01 0.00 1/115 5423

$ nproc
4

$ ps -eo pid,pcpu,pmem,etimes,comm --sort=-pcpu | head -12
  PID %CPU %MEM ELAPSED COMMAND
 5418 33.3  0.0       0 bash
  163  1.6  2.4    8811 claude
 4661  0.2  0.7     632 node
   86  0.0  0.2    8813 environment-man
    1  0.0  0.0    8816 process_api
   81  0.0  0.0    8814 6
 3393  0.0  0.0    2486 kworker/u16:3-ext4-rsv-conversion
   46  0.0  0.0    8816 kcompactd0
   26  0.0  0.0    8816 migration/2
   31  0.0  0.0    8816 migration/3
   21  0.0  0.0    8816 migration/1

$ awk of /proc/net/tcp state 01 (ESTABLISHED) count
23

$ /proc/net/tcp6 readable check
/bin/bash: line 42: /proc/net/tcp6: No such file or directory
not readable
```

## Sample 2, collected 2026-09-25T22:28:32Z

```
$ date -u +%FT%TZ
2026-09-25T22:28:32Z

$ cat /proc/loadavg
0.01 0.01 0.00 1/114 5603

$ nproc
4

$ ps -eo pid,pcpu,pmem,etimes,comm --sort=-pcpu | head -12
  PID %CPU %MEM ELAPSED COMMAND
 5598 25.0  0.0       0 bash
  163  1.6  2.5    9127 claude
 4661  0.1  0.7     948 node
   86  0.0  0.2    9130 environment-man
    1  0.0  0.0    9133 process_api
   81  0.0  0.0    9130 6
 3393  0.0  0.0    2802 kworker/u16:3-ext4-rsv-conversion
   46  0.0  0.0    9133 kcompactd0
   26  0.0  0.0    9133 migration/2
   31  0.0  0.0    9133 migration/3
   21  0.0  0.0    9133 migration/1

$ awk of /proc/net/tcp state 01 (ESTABLISHED) count
21

$ /proc/net/tcp6 readable check
/bin/bash: line 42: /proc/net/tcp6: No such file or directory
not readable
```

## Process identification

Reading each listed process's command line from `/proc/<pid>/cmdline` inside this container (not an API call) identified:

- PID 163, `claude`: this container's Claude Code CLI harness, launched with `--model claude-fable-5-1` among its arguments. Present and near-identical in both samples (elapsed 8811s then 9127s).
- PID 4661, `node`: `node server.js`, the local Harbour server for this session's workspace. Present in both samples, elapsed 632s then 948s, so it started roughly 316 seconds before sample 1.
- PID 86, `environment-manager`: `environment-manager task-run --stdin --session cse_01FEz9XJ6R91XVA4ErFhTmr8 --session-mode new`, the sandbox process that launched this session.
- PID 1, `process_api`: the sandbox's Firecracker init process.
- PID 81, shown truncated as `6` by `ps`: `sbx-telemetry-collector`, a sandbox supervisor process.
- PID 3393 and the `migration/N` and `kcompactd0` entries: kernel worker threads, not attributable to this dispatch.
- The top `bash` entry in each sample (PID 5418, then PID 5598, each at 0 elapsed seconds and roughly 25 to 33 percent CPU) is the shell that ran the sampling command itself; its high share is an artefact of measuring a process that had existed for under a second, not a sign of load elsewhere.
