// Harbour-style header blocks: `key: value` lines at the very top of a file,
// with no YAML delimiters, ending at the first blank line or first heading.
// A line starting "- " adds an item to the key above it; any other line
// continues the value above it.

export const KEY_LINE = /^([A-Za-z][A-Za-z0-9_ ()-]{0,48}?):(?:[ \t]+(.*))?$/;

// A piece's header may be a single line, such as `published: 2026-09-27`,
// when its key is one the site reads on pieces.
export const PIECE_KEYS = ["published", "summary", "status", "investigation", "revised"];

function isHeading(line) {
  return /^#{1,6}(\s|$)/.test(line);
}

export function parseHeader(source) {
  const text = source.replace(/^﻿/, "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  const first = lines[0] || "";
  if (!KEY_LINE.test(first) || isHeading(first)) return null;

  const fields = [];
  let i = 0;
  for (; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === "" || isHeading(line)) break;
    const item = line.match(/^\s*[-*]\s+(.*)$/);
    const key = !item && line.match(KEY_LINE);
    if (key) {
      fields.push({ key: key[1].trim(), value: (key[2] || "").trim(), items: [] });
    } else if (item && fields.length) {
      fields[fields.length - 1].items.push(item[1].trim());
    } else if (fields.length) {
      const last = fields[fields.length - 1];
      if (last.items.length) {
        last.items[last.items.length - 1] += " " + line.trim();
      } else {
        last.value = (last.value + " " + line.trim()).trim();
      }
    } else {
      return null;
    }
  }

  const hasTitle = fields.some((f) => f.key.toLowerCase() === "title");
  const known = fields.length === 1 && PIECE_KEYS.includes(fields[0].key.toLowerCase());
  if (!hasTitle && fields.length < 2 && !known) return null;

  const get = (name) => {
    const f = fields.find((x) => x.key.toLowerCase() === name);
    return f ? f.value : "";
  };

  return {
    fields,
    title: get("title"),
    kind: get("kind"),
    version: get("version"),
    date: get("date"),
    lineCount: i,
    body: lines.slice(i).join("\n").replace(/^\n+/, ""),
  };
}

// The field named `name` (case-insensitive) in a parsed header's fields.
export function headerField(fields, name) {
  return (fields || []).find((f) => f.key.toLowerCase() === name) || null;
}

// The content with any header block removed, for rendering.
export function stripHeader(source) {
  const header = parseHeader(source);
  return header ? header.body : source;
}
