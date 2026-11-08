"""LH047: find HTTP requests made in this session's agent transcripts outside any logging
collector (brief, section 3, "unlogged requests").

Reads the transcripts given on the command line (JSONL, one event per line) and writes
studies/LH047/data/transcripts/tool-calls.csv: one row per tool call that could reach the
network, with transcript, line, UTC time, tool, kind, the URLs written literally in it, and the
first 400 characters of the call and of its result (email addresses withheld).

kind:
  adhoc-curl     a Bash command that runs curl or wget on literal URLs
  adhoc-inline   a Bash command with an inline HTTP client (python -c / heredoc with urllib,
                 requests or http.client; node fetch) and literal URLs
  collector      a Bash command that runs a script under studies/, essays/ or notes/ (its
                 requests are in that study's fetch log, if it keeps one)
  scratch-script a Bash command that runs a script outside the repository (its URLs are not
                 visible in the command; listed for reading by hand)
  webfetch       a WebFetch tool call
  websearch      a WebSearch tool call (a search provider's request, not Lighthouse's to a site)
  git            git fetch, clone, push or ls-remote
  write-netcode  a Write of a file outside the repository that contains network code and URLs
Run: python3 -I studies/LH047/scripts/transcript_requests.py <transcript.jsonl>...
Only events up to UNTIL (20:27 UTC, the end of part C's window) are read.
The transcripts themselves live outside the repository and are not copied into it.
"""
import csv, json, os, re, sys

sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
from redact_emails import redact_bytes  # noqa: E402

URL = re.compile(r'https?://[^\s\'"<>()|;`,\\]+')
LOCAL = ('127.0.0.1', 'localhost', '__agentproxy', '0.0.0.0')
NETCODE = re.compile(r'urllib\.request|urlopen|requests\.(get|post|head|Session)|http\.client|httpx|\bfetch\(|aiohttp')
OUT = os.path.join(os.getcwd(), 'studies/LH047/data/transcripts/tool-calls.csv')


SECRETS = re.compile(r'session_[A-Za-z0-9]+|sk-ant-[A-Za-z0-9_-]+|gh[pousr]_[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9._-]{16,}')


def red(s):
    """Withhold email addresses, session ids and anything shaped like a key or token."""
    s = redact_bytes(s.encode('utf-8', 'replace'))[0].decode('utf-8', 'replace')
    return SECRETS.sub('[withheld by Lighthouse]', s)


def urls_of(text):
    return [u.rstrip('.') for u in URL.findall(text) if not any(l in u for l in LOCAL)]


def classify_bash(cmd):
    c = cmd
    if re.search(r'\bgit\s+(fetch|clone|push|pull|ls-remote)\b', c):
        return 'git'
    if re.search(r'(^|[\s;&|(])(curl|wget)\s', c) and urls_of(c):
        return 'adhoc-curl'
    if NETCODE.search(c) and urls_of(c):
        return 'adhoc-inline'
    if re.search(r'python3?\s+(-I\s+)?(-u\s+)?(\S*/)?(studies|essays|notes)/\S+\.py', c) or re.search(r'python3?\s+(-I\s+)?\S*scripts/\S+\.py', c):
        return 'collector'
    if re.search(r'python3?\s+(-I\s+)?(/tmp|/root)\S*\.py', c):
        return 'scratch-script'
    if re.search(r'(^|[\s;&|(])(curl|wget)\s', c):
        return 'adhoc-curl-indirect'
    return None


UNTIL = '2026-11-08T20:27:00'  # end of part C's window (brief, section 3: "to the time of the run")


def main(paths):
    rows = []
    for p in paths:
        name = os.path.basename(p)
        pending = {}
        with open(p, encoding='utf-8', errors='replace') as f:
            for ln, line in enumerate(f, 1):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get('timestamp', '')[:19] > UNTIL:
                    continue
                msg = d.get('message') or {}
                content = msg.get('content')
                if not isinstance(content, list):
                    continue
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get('type') == 'tool_use':
                        tool = item.get('name')
                        inp = item.get('input') or {}
                        kind, text, urls = None, '', []
                        if tool == 'Bash':
                            text = inp.get('command', '')
                            kind = classify_bash(text)
                            urls = urls_of(text) if kind in ('adhoc-curl', 'adhoc-inline', 'adhoc-curl-indirect', 'git') else []
                        elif tool == 'WebFetch':
                            text = inp.get('url', '') + ' ' + inp.get('prompt', '')[:200]
                            kind, urls = 'webfetch', [inp.get('url', '')]
                        elif tool == 'WebSearch':
                            text = inp.get('query', '')
                            kind = 'websearch'
                        elif tool == 'Write':
                            fp = inp.get('file_path', '')
                            body = inp.get('content', '')
                            if not fp.startswith('/home/user/lighthouse') and NETCODE.search(body) and urls_of(body):
                                kind, text, urls = 'write-netcode', fp + '\n' + body, urls_of(body)
                        if kind:
                            row = dict(transcript=name, line=ln, utc=d.get('timestamp', ''), tool=tool, kind=kind,
                                       n_urls=len(urls), urls=red(' '.join(urls)), call=red(text[:400]), result='')
                            rows.append(row)
                            pending[item.get('id')] = row
                    elif item.get('type') == 'tool_result':
                        row = pending.get(item.get('tool_use_id'))
                        if row is not None:
                            c = item.get('content')
                            if isinstance(c, list):
                                c = ' '.join(x.get('text', '') for x in c if isinstance(x, dict))
                            row['result'] = red(str(c)[:400])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['transcript', 'line', 'utc', 'tool', 'kind', 'n_urls', 'urls', 'call', 'result'])
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(Counter(r['kind'] for r in rows))


if __name__ == '__main__':
    main(sys.argv[1:])
