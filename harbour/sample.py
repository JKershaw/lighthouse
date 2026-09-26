#!/usr/bin/env python3
"""sample.py -- one-shot host sampler for Lighthouse (instrument I-0002).

Standard library only, no dependencies, no network requests. Reads /proc on
Linux and prints one JSON object of numeric fields per sample, the shape
Harbour's resources feedback parser accepts (harbour/requests.md, "resources
producer", LIN-1788). The Lighthouse tag is its own argv, sample.py, visible
in the process table; it carries no other tag.

Fields printed (all numeric, exact names from harbour/requests.md):
  sampledAtEpochSeconds   epoch second when this sample finished (the end of
                          the interval below, once every read is in hand)
  sampleIntervalSeconds   the --interval value used for this sample
  busyCoreSeconds         sum over cores of busy time, from two reads of the
                          aggregate "cpu" line in /proc/stat taken interval
                          seconds apart, converted from jiffies with
                          os.sysconf('SC_CLK_TCK'); busy = total - idle -
                          iowait. The aggregate line already sums every
                          core's ticks, so this one delta is the sum over
                          cores without reading the per-core cpuN lines.
  loadAvg1                first field of /proc/loadavg
  cpuCount                os.cpu_count()
  hostMemTotalBytes       MemTotal from /proc/meminfo, converted to bytes
  hostMemAvailableBytes   MemAvailable from /proc/meminfo, converted to bytes
  hostSwapUsedBytes       SwapTotal - SwapFree from /proc/meminfo, in bytes
  processCount            count of numeric entries under /proc, i.e. every
                          process (and kernel thread) with a /proc/<pid>
  establishedTcpConnections  lines in state 01 (ESTABLISHED) across
                          /proc/net/tcp and /proc/net/tcp6
  agentRssBytes           resident memory of "the agent process", identified
                          as the single /proc/<pid>/comm reading exactly
                          "claude" (the Claude Code CLI binary this
                          container runs as PID 103 in the run this script
                          was calibrated against; see registers/instruments.md
                          I-0002). Left out entirely, rather than guessed,
                          when zero or more than one process match, since
                          then there is no single process the field could
                          honestly name.
  samplerCpuSeconds       this process's own user+system CPU time from
                          resource.getrusage(RUSAGE_SELF) at the moment of
                          the sample: the sampler's own overhead, cumulative
                          since this python3 process started, so on a
                          one-shot run it is the overhead of that one sample,
                          and on a --repeat run it grows sample over sample.

Not measured here, and not printed: requestsOut, bytesOut and
requestsByDestination (outbound traffic goes through an agent proxy on
localhost whose status endpoint reports configuration, not traffic counts,
and there is no `ss` on this host to read sockets by destination another
way). The limit is recorded in registers/instruments.md and, in a sample,
shows only as these fields' absence; nothing prints a null in their place.

With --label <text>, each sample is also appended, as its own JSON line,
to harbour/samples/<label>.jsonl, alongside a non-numeric connectionsByRemote
map (remote "ip:port" string to count, decoded from the established rows
above). That extra field is Lighthouse's own record; it is never printed to
stdout and never posted to Harbour, whose resources parser takes numbers
only (harbour/requests.md).

With --repeat N, N consecutive samples are taken back to back, each printed
as its own line and, with --label, each appended as its own line.
"""
import argparse
import json
import os
import resource
import socket
import sys
import time

CLK_TCK = os.sysconf("SC_CLK_TCK")


def read_cpu_busy():
    """Return (busy, total) jiffies from the aggregate 'cpu' line of /proc/stat."""
    with open("/proc/stat") as f:
        line = f.readline()
    parts = line.split()
    vals = [int(x) for x in parts[1:]]
    idle = vals[3] if len(vals) > 3 else 0
    iowait = vals[4] if len(vals) > 4 else 0
    total = sum(vals)
    busy = total - idle - iowait
    return busy, total


def read_meminfo():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, rest = line.split(":", 1)
            info[key] = int(rest.split()[0]) * 1024  # kB -> bytes
    total = info.get("MemTotal", 0)
    available = info.get("MemAvailable", 0)
    swap_total = info.get("SwapTotal", 0)
    swap_free = info.get("SwapFree", 0)
    return total, available, swap_total - swap_free


def count_processes():
    return sum(1 for e in os.listdir("/proc") if e.isdigit())


def _decode_ipv4(hexip):
    b = bytes.fromhex(hexip)[::-1]  # /proc/net/tcp stores each word little-endian
    return socket.inet_ntoa(b)


def _decode_ipv6(hexip):
    raw = bytes.fromhex(hexip)
    words = [raw[i : i + 4][::-1] for i in range(0, 16, 4)]
    return socket.inet_ntop(socket.AF_INET6, b"".join(words))


def _decode_endpoint(hex_addr, is_v6):
    ip_hex, port_hex = hex_addr.split(":")
    port = int(port_hex, 16)
    try:
        ip = _decode_ipv6(ip_hex) if is_v6 else _decode_ipv4(ip_hex)
    except (ValueError, OSError):
        ip = ip_hex
    return f"{ip}:{port}"


def read_established(path, is_v6):
    """Count ESTABLISHED (state 01) rows in a /proc/net/tcp[6] file and
    tally them by decoded remote endpoint. Returns (count, {endpoint: n})."""
    count = 0
    remotes = {}
    try:
        with open(path) as f:
            next(f, None)  # header row
            for line in f:
                parts = line.split()
                if len(parts) < 4:
                    continue
                if parts[3] != "01":
                    continue
                count += 1
                remote = _decode_endpoint(parts[2], is_v6)
                remotes[remote] = remotes.get(remote, 0) + 1
    except FileNotFoundError:
        pass
    return count, remotes


def find_agent_rss():
    """Find /proc/<pid> whose comm is exactly 'claude'. Returns a list of
    (pid, rss_bytes); the caller only trusts a list of length 1."""
    matches = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/comm") as f:
                comm = f.read().strip()
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
        if comm != "claude":
            continue
        rss_kb = None
        try:
            with open(f"/proc/{entry}/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        rss_kb = int(line.split()[1])
                        break
        except (FileNotFoundError, PermissionError):
            continue
        if rss_kb is not None:
            matches.append((entry, rss_kb * 1024))
    return matches


def take_sample(interval):
    busy0, _ = read_cpu_busy()
    time.sleep(interval)
    busy1, _ = read_cpu_busy()
    busy_core_seconds = (busy1 - busy0) / CLK_TCK

    sampled_at = int(time.time())
    load_avg1 = float(open("/proc/loadavg").read().split()[0])
    cpu_count = os.cpu_count()
    mem_total, mem_available, swap_used = read_meminfo()
    process_count = count_processes()

    est4, remotes4 = read_established("/proc/net/tcp", False)
    est6, remotes6 = read_established("/proc/net/tcp6", True)
    established = est4 + est6
    remotes = dict(remotes4)
    for k, v in remotes6.items():
        remotes[k] = remotes.get(k, 0) + v

    rss_matches = find_agent_rss()

    ru = resource.getrusage(resource.RUSAGE_SELF)
    sampler_cpu_seconds = ru.ru_utime + ru.ru_stime

    numeric = {
        "sampledAtEpochSeconds": sampled_at,
        "sampleIntervalSeconds": interval,
        "busyCoreSeconds": round(busy_core_seconds, 4),
        "loadAvg1": load_avg1,
        "cpuCount": cpu_count,
        "hostMemTotalBytes": mem_total,
        "hostMemAvailableBytes": mem_available,
        "hostSwapUsedBytes": swap_used,
        "processCount": process_count,
        "establishedTcpConnections": established,
    }
    if len(rss_matches) == 1:
        numeric["agentRssBytes"] = rss_matches[0][1]
    numeric["samplerCpuSeconds"] = round(sampler_cpu_seconds, 6)

    return numeric, remotes


def main():
    parser = argparse.ArgumentParser(description="One-shot host sampler (Lighthouse I-0002).")
    parser.add_argument("--interval", type=float, default=5.0,
                         help="seconds between the two /proc/stat reads (default 5)")
    parser.add_argument("--label", type=str, default=None,
                         help="append each sample to harbour/samples/<label>.jsonl")
    parser.add_argument("--repeat", type=int, default=1,
                         help="take N consecutive samples (default 1)")
    args = parser.parse_args()

    samples_dir = None
    if args.label:
        samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
        os.makedirs(samples_dir, exist_ok=True)

    for _ in range(args.repeat):
        numeric, remotes = take_sample(args.interval)
        print(json.dumps(numeric), flush=True)
        if samples_dir:
            record = dict(numeric)
            record["connectionsByRemote"] = remotes
            path = os.path.join(samples_dir, f"{args.label}.jsonl")
            with open(path, "a") as f:
                f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
