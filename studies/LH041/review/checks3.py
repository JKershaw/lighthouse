"""R-0057, third pass: is ChainDrop's first maintainer cluster (post hoc view,
indicator joins) the same 11 packages StepSecurity lists as its carriers (w19,
read live 2026-11-08T20:18:45Z)? And the first new cluster's time. Prints set
equality and counts only; package names are the source's own list.
    python3 -I studies/LH041/review/checks3.py > studies/LH041/review/checks3-output.txt
"""
import contextlib, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    g = {"__file__": os.path.join(HERE, "reproduce.py"), "__name__": "lh041_review"}
    exec(open(os.path.join(HERE, "reproduce.py")).read(), g)
CARRIERS = {"keyv", "flat-cache", "file-entry-cache", "cacheable-request", "@cacheable/utils", "cacheable",
            "@cacheable/memory", "cache-manager", "@cacheable/node-cache", "ecto", "@cacheable/net"}
o, rs, comps, h = g["keep"][("W11", True, True)]
first = set(comps[0][1])
print("first cluster size", len(first), "| equals StepSecurity's 11 carriers:", first == CARRIERS,
      "| in both", len(first & CARRIERS), "| carriers not in first cluster", len(CARRIERS - first))
print("first cluster first publish", comps[0][0], "| second cluster first publish", comps[1][0])
rec_pkgs = {x["pkg"] for x in rs}
print("carriers among ChainDrop's indicator records:", len(CARRIERS & rec_pkgs))
