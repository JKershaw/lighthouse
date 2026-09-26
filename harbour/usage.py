#!/usr/bin/env python3
"""Sum what a Claude Code transcript spent and price it.

usage: usage.py <transcript.jsonl> [--since ISO] [--until ISO] [--prices prices.json] [--effort label]

Every API call in a Claude Code transcript is stored once per content block, each
copy carrying the same usage object, so calls are deduplicated by message id. The
input side (input, cache read, cache creation) is exact. The output_tokens field in
the transcript is the placeholder from the start of the stream, not the final
count, so output is estimated from the characters the model produced at four per
token and labelled as such. Cost uses prices.json; a call whose model has no row,
or that used a cache tier with no published rate, makes costUsd null rather than a
guess. Nothing here reads the transcript's text into the caller's context: only
totals are printed.
"""
import json, sys, os, math, collections, datetime

def parse_ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None

def base_model(m):
    parts = (m or "").split("-")
    if parts and len(parts[-1]) == 8 and parts[-1].isdigit():
        parts = parts[:-1]
    return "-".join(parts)

def main(argv):
    path = argv[1]
    opts = {"--since": None, "--until": None, "--prices": os.path.join(os.path.dirname(os.path.abspath(__file__)), "prices.json"), "--effort": None}
    i = 2
    while i < len(argv):
        opts[argv[i]] = argv[i + 1]; i += 2
    since, until = parse_ts(opts["--since"]), parse_ts(opts["--until"])
    prices = json.load(open(opts["--prices"]))["models"]

    calls = collections.OrderedDict()
    for line in open(path):
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") != "assistant": continue
        m = d.get("message") or {}
        u = m.get("usage")
        if not isinstance(u, dict) or not m.get("id"): continue
        ts = parse_ts(d.get("timestamp"))
        if since and ts and ts < since: continue
        if until and ts and ts > until: continue
        c = calls.setdefault(m["id"], {"u": u, "model": m.get("model"), "ts": ts, "chars": 0, "tools": 0, "effort": d.get("effort")})
        for b in m.get("content") or []:
            t = b.get("type")
            if t == "text": c["chars"] += len(b.get("text") or "")
            elif t == "thinking": c["chars"] += len(b.get("thinking") or "")
            elif t == "tool_use": c["chars"] += len(json.dumps(b.get("input") or {})); c["tools"] += 1

    if not calls:
        print(json.dumps({"error": "no assistant calls in range"})); return 1

    tot = collections.Counter(); models = collections.Counter(); cost = 0.0; priced = True
    for c in calls.values():
        u = c["u"]; m = base_model(c["model"]); models[m] += 1
        inp = u.get("input_tokens") or 0; rd = u.get("cache_read_input_tokens") or 0
        cc = u.get("cache_creation") or {}
        w5 = cc.get("ephemeral_5m_input_tokens"); w1 = cc.get("ephemeral_1h_input_tokens") or 0
        wr = u.get("cache_creation_input_tokens") or 0
        if w5 is None: w5 = wr - w1
        out = math.ceil(c["chars"] / 4)
        tot["inputTokens"] += inp; tot["cacheReadInputTokens"] += rd; tot["cacheCreationInputTokens"] += wr
        tot["cacheCreation1hInputTokens"] += w1; tot["outputTokens"] += out; tot["toolCalls"] += c["tools"]
        p = prices.get(m)
        if not p or (w1 and "cacheWrite1h" not in p):
            priced = False; continue
        cost += (inp * p["input"] + rd * p["cacheRead"] + w5 * p["cacheWrite"] + w1 * p.get("cacheWrite1h", 0) + out * p["output"]) / 1e6

    stamps = [c["ts"] for c in calls.values() if c["ts"]]
    effort = opts["--effort"] or next((c["effort"] for c in calls.values() if c.get("effort")), None)
    main_model = models.most_common(1)[0][0]
    result = {
        "model": main_model, "harness": "claude-code", "effort": effort or "subagent",
        "inputTokens": tot["inputTokens"], "outputTokens": tot["outputTokens"],
        "cacheReadInputTokens": tot["cacheReadInputTokens"], "cacheCreationInputTokens": tot["cacheCreationInputTokens"],
        "cacheCreation1hInputTokens": tot["cacheCreation1hInputTokens"],
        "costUsd": round(cost, 4) if priced else None,
        "calls": len(calls), "toolCalls": tot["toolCalls"],
        "wallSeconds": int((max(stamps) - min(stamps)).total_seconds()) if len(stamps) > 1 else 0,
        "outputTokensBasis": "estimated from characters produced, four per token; the transcript carries only the stream-start placeholder",
        "pricesReadAt": json.load(open(opts["--prices"]))["readAt"],
    }
    if len(models) > 1: result["models"] = dict(models)
    print(json.dumps(result)); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
