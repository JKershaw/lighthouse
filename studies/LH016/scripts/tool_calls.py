"""LH016: list the tool calls in a subagent's transcript (name and the path or
command it was given, shortened), to check what a blind or stage 1 reviewer
opened. Usage: python3 scripts/tool_calls.py <transcript.jsonl> [marker]
With a marker, a line is printed where a user message containing it begins,
so that stage 1's calls can be told from stage 2's.
"""
import json
import sys

path = sys.argv[1]
marker = sys.argv[2] if len(sys.argv) > 2 else None
for line in open(path):
    try:
        e = json.loads(line)
    except ValueError:
        continue
    msg = e.get("message") or {}
    content = msg.get("content")
    if e.get("type") == "user" and marker:
        text = content if isinstance(content, str) else " ".join(
            c.get("text", "") for c in (content or []) if isinstance(c, dict))
        if marker in text:
            print(f"---- a user message containing {marker!r} begins here ----")
    if e.get("type") != "assistant" or not isinstance(content, list):
        continue
    for c in content:
        if isinstance(c, dict) and c.get("type") == "tool_use":
            inp = c.get("input", {})
            arg = inp.get("file_path") or inp.get("command") or inp.get("pattern") or inp.get("path") or ""
            print(f"{c.get('name')}: {str(arg)[:160]}")
