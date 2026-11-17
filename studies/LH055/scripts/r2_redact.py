#!/usr/bin/env python3
"""LH055 round 2: withhold personal identifiers that the collector's patterns do not catch.

Usage (from the repository root, once, after collection):
  python3 -I studies/LH055/scripts/r2_redact.py studies/LH055/data/round2-2026-11-17T2124Z

The brief withholds personal identifiers from retained extracts. CrowdStrike's report (R03) prints
personal details that it says likely belong to the threat actor but that it cannot definitively
associate with them (a name, a phone number, a messaging username, an age and a date of birth,
education and skills). This script replaces that list, and each later mention of the username, with
a marker in R03's retained body and text, and writes redactions.json with the retained hashes before
and after. Nothing is printed except counts and hashes. The fetch log is left as written; the replay
(r2_tables.py) checks each retained file against redactions.json where an entry exists.
"""
import gzip, hashlib, json, os, re, sys

MARK = "[personal details withheld by Lighthouse]"
UMARK = "[username withheld by Lighthouse]"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(d):
    out = {}
    bp = os.path.join(d, "bodies", "R03.raw.gz")
    tp = os.path.join(d, "text", "R03.txt")
    body = gzip.open(bp).read()
    text = open(tp, "rb").read()
    rec = {"id": "R03", "reason": "personal identifiers of a possible individual, published by CrowdStrike; withheld under the brief",
           "body_sha256_before": sha(body), "text_sha256_before": sha(text)}
    s = body.decode("utf-8")
    i = s.find("following personal details")
    a = s.find("<ul>", i)
    b = s.find("</ul>", a)
    assert i > 0 and 0 < a < b and a - i < 200, "list not found where expected"
    s = s[:a] + "<ul><li>" + MARK + "</li></ul>" + s[b + 5:]
    user = re.search(r"Telegram username (\w+)", s)
    assert user, "username not found"
    n_user_body = s.count(user.group(1))
    s = s.replace(user.group(1), UMARK)
    body2 = s.encode("utf-8")
    t = text.decode("utf-8").split("\n")
    k = next(n for n, l in enumerate(t) if "following personal details" in l)
    e = next(n for n in range(k + 1, len(t)) if not t[n].startswith("- "))
    removed = e - (k + 1)
    t = t[:k + 1] + ["- " + MARK] + t[e:]
    t = "\n".join(t)
    n_user_text = t.count(user.group(1)) + t.count("@" + user.group(1))
    t = t.replace(user.group(1), UMARK)
    text2 = t.encode("utf-8")
    gzip.open(bp, "wb").write(body2)
    open(tp, "wb").write(text2)
    rec.update(body_sha256_after=sha(body2), text_sha256_after=sha(text2),
               text_list_lines_replaced=removed, username_mentions_body=n_user_body,
               username_mentions_text=n_user_text)
    out["R03"] = rec
    json.dump(out, open(os.path.join(d, "redactions.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in rec.items() if k != "reason"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
