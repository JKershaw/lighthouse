#!/bin/sh
# R-0172: count-only check that the retained LH043 account texts hold no
# repository-shaped links (host/x/y) naming a party to the incidents.
# Each match is put in exactly one class; no identifier is printed.
# Run from the repository root: sh notes/R-0172-found-nothing-reader/identifier_count.sh
set -e
D=studies/LH043/data/sources
PAT='(github\.com|huggingface\.co|pypi\.org|npmjs\.com)/[A-Za-z0-9_.<>-]+/[A-Za-z0-9_.<>-]+'
for f in "$D"/*.txt; do
  grep -oE "$PAT" "$f" | awk -v F="$(basename "$f")" '
    /</                                   {ph++;   next}
    /^huggingface\.co\/(v1|production)\// {cdn++;  next}
    /^huggingface\.co\/(blog|papers)\//   {site++; next}
                                          {oth++}
    END { if (NR) printf "%s total=%d placeholder=%d avatar_or_upload_cdn=%d site_pages=%d other=%d\n", F, NR, ph, cdn, site, oth }'
done
