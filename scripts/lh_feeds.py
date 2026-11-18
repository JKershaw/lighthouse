#!/usr/bin/env python3
"""Read RSS 2.0 or Atom feeds and print one short JSON record per endpoint."""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request

# Also support python3 -I, like the other Lighthouse collectors.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_fetch import NotFetched, UA, redacted, urlopen  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"
XML_BASE = "{http://www.w3.org/XML/1998/namespace}base"
ORIGINAL_LINK = "{http://rssnamespace.org/feedburner/ext/1.0}origLink"
MAX_BYTES = 2 * 1024 * 1024


def is_web_url(url):
    try:
        parts = urlsplit(url)
        return parts.scheme in {"http", "https"} and bool(parts.hostname) and parts.username is None
    except ValueError:
        return False


def clean_text(element):
    if element is None:
        return None
    return " ".join("".join(element.itertext()).split()) or None


def parse_feed(body, url):
    root = ET.fromstring(body)
    base = urljoin(url, root.get(XML_BASE, ""))
    if root.tag == ATOM + "feed":
        prefix, container, item_tag, date_tag = ATOM, root, "entry", "published"
    elif root.tag == "rss" and (channel := root.find("channel")) is not None:
        prefix, container, item_tag, date_tag = "", channel, "item", "pubDate"
        base = urljoin(base, channel.get(XML_BASE, ""))
    else:
        raise ValueError("expected an RSS or Atom feed")

    entries = []
    skipped = 0
    for item in container.findall(prefix + item_tag):
        item_base = urljoin(base, item.get(XML_BASE, ""))
        title = clean_text(item.find(prefix + "title"))
        article_url = None
        links = item.findall(ORIGINAL_LINK) + item.findall(prefix + "link")
        for link in links:
            if link.tag == ATOM + "link" and link.get("rel", "alternate") != "alternate":
                continue
            target = link.get("href") if link.tag == ATOM + "link" else clean_text(link)
            if target:
                candidate = urljoin(urljoin(item_base, link.get(XML_BASE, "")), target)
                if is_web_url(candidate):
                    article_url = candidate
                    break
        if not title or not article_url:
            skipped += 1
            continue

        published = clean_text(item.find(prefix + date_tag))
        entry = {"title": title, "published": published, "url": article_url}
        if prefix and not published:
            updated = clean_text(item.find(ATOM + "updated"))
            if updated:
                entry["updated"] = updated
        entries.append(entry)

    return entries, skipped


def publication_day(value):
    if not value:
        return None
    try:
        try:
            iso_value = value[:-1] + "+00:00" if value.endswith("Z") else value
            timestamp = datetime.fromisoformat(iso_value)
        except ValueError:
            timestamp = parsedate_to_datetime(value)
        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone(timezone.utc)
        return timestamp.date()
    except (ValueError, OverflowError):
        return None


def read_feed(url, since):
    result = {"url": url, "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    try:
        if not is_web_url(url):
            raise ValueError("expected an HTTP(S) feed URL")
        request = Request(url, headers={"User-Agent": UA})
        with urlopen(request, timeout=15, check_redirects=True) as response:
            result["resolved_url"] = response.geturl()
            body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("feed exceeds the 2 MiB read limit")
        entries, skipped = parse_feed(body, result["resolved_url"])
        dated_entries = [(publication_day(entry["published"]), entry) for entry in entries]
        days = [day for day, _ in dated_entries if day is not None]
        result.update(
            status="ok",
            oldest_published=min(days).isoformat() if days else None,
            newest_published=max(days).isoformat() if days else None,
            skipped_entries=skipped,
            undated_entries=len(entries) - len(days),
            entries=[entry for day, entry in dated_entries if since is None or day is None or day >= since],
        )
    except HTTPError as error:
        result.update(status="unavailable", reason=f"HTTP {error.code}", resolved_url=error.geturl())
        error.close()
    except (NotFetched, URLError, OSError, HTTPException, ET.ParseError, ValueError) as error:
        result.update(status="unavailable", reason=str(error))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="+", help="publisher feed URL")
    parser.add_argument("--since", type=date.fromisoformat, metavar="YYYY-MM-DD",
                        help="include publication days on or after this UTC date, plus undated entries")
    args = parser.parse_args()
    failed = False
    for url in args.url:
        result = read_feed(url, args.since)
        print(redacted(json.dumps(result, ensure_ascii=False).encode("utf-8")).decode("utf-8"), flush=True)
        failed |= result["status"] != "ok"
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
