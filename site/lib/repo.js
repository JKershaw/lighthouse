// Reads the repository once per build: which Markdown files become pages,
// their titles, headers and git dates, which images are copied, and the
// indexes built from them. Nothing here is a registry; it is all found.

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { parseHeader, headerField } from "./header.js";

export const REPO_URL = "https://github.com/JKershaw/lighthouse";
export const REPO_BRANCH = "main";

// Paths the site never reads, relative to the repository root.
export const IGNORED_DIRS = ["harbour", "site", "node_modules", ".claude", ".github", ".git"];
export const IGNORED_FILES = ["CLAUDE.md"];
export const IMAGE_EXT = [".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"];

// Directories that get an index page of their own.
const SECTION_DIRS = ["articles", "articles/short", "investigations", "studies", "notes"];

// Root files with a label of their own. When about.md exists it is the About
// page and AGENTS.md is labelled as the operating manual it is.
const ROOT_LABELS = {
  "about.md": "About",
  "AGENTS.md": "About",
  "observations.md": "Observations",
  "charter.md": "Charter",
  "design.md": "Research design",
  "programme.md": "Programme",
  "releases.md": "Releases",
  "sources.md": "Sources",
};

const dateFormat = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "UTC",
});

export function formatDate(value) {
  if (value === undefined || value === null || value === "") return "";
  const d = value instanceof Date ? value : new Date(value);
  return Number.isNaN(d.getTime()) ? "" : dateFormat.format(d);
}

// "2026-09-26; corrected the same day" gives 26 September 2026.
export function headerDate(value) {
  const m = String(value || "").match(/\b(\d{4}-\d{2}-\d{2})\b/);
  return m ? new Date(m[1] + "T00:00:00Z") : null;
}

export function isIgnored(rel) {
  const parts = rel.split("/");
  if (parts.some((p) => p === "node_modules")) return true;
  if (IGNORED_DIRS.includes(parts[0])) return true;
  return IGNORED_FILES.includes(rel);
}

export function pageUrl(rel) {
  if (rel === "README.md") return "/";
  const noExt = rel.replace(/\.md$/i, "");
  if (path.posix.basename(noExt) === "index") {
    const dir = path.posix.dirname(noExt);
    return dir === "." ? "/" : `/${dir}/`;
  }
  return `/${noExt}/`;
}

export function sourceUrl(rel, isDir = false) {
  const clean = rel.replace(/\/$/, "");
  return `${REPO_URL}/${isDir ? "tree" : "blob"}/${REPO_BRANCH}/${clean}${isDir && clean ? "/" : ""}`;
}

function walk(root) {
  const files = [];
  const dirs = [];
  const visit = (dir) => {
    for (const entry of fs.readdirSync(path.join(root, dir), { withFileTypes: true })) {
      const rel = dir ? `${dir}/${entry.name}` : entry.name;
      if (isIgnored(rel)) continue;
      if (entry.isDirectory()) {
        dirs.push(rel);
        visit(rel);
      } else if (entry.isFile()) {
        files.push(rel);
      }
    }
  };
  visit("");
  return { files: files.sort(), dirs: dirs.sort() };
}

// True when root is the top of a git checkout, so that git's paths are
// relative to it (a fixture directory inside this repository is not).
function isGitRoot(root) {
  try {
    const top = execFileSync("git", ["rev-parse", "--show-toplevel"], {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    return fs.realpathSync(top) === fs.realpathSync(root);
  } catch {
    return false;
  }
}

// One `git log` for the whole repository: the newest commit that touched each
// path, and the oldest, when it was added.
function gitDates(root) {
  const dates = new Map();
  const added = new Map();
  if (!isGitRoot(root)) return { dates, added };
  try {
    const out = execFileSync("git", ["log", "--format=%x1e%ct", "--name-only", "--no-renames"], {
      cwd: root,
      encoding: "utf8",
      maxBuffer: 64 * 1024 * 1024,
      stdio: ["ignore", "pipe", "ignore"],
    });
    for (const chunk of out.split("\x1e")) {
      const lines = chunk.split("\n").filter(Boolean);
      if (!lines.length) continue;
      const time = Number(lines[0]) * 1000;
      for (const file of lines.slice(1)) {
        if (!dates.has(file)) dates.set(file, time);
        added.set(file, time);
      }
    }
  } catch {
    // Not a git checkout: fall back to file times below.
  }
  return { dates, added };
}

function gitCommit(root) {
  if (!isGitRoot(root)) return "";
  try {
    return execFileSync("git", ["rev-parse", "--short", "HEAD"], {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch {
    return "";
  }
}

// Markdown inline syntax reduced to plain words, for titles and summaries.
export function plainText(md) {
  return String(md || "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/`([^`]*)`/g, "$1")
    .replace(/(\*\*|__)(.*?)\1/g, "$2")
    .replace(/(^|[^\w*])[*_]([^*_]+)[*_](?=[^\w*]|$)/g, "$1$2")
    .replace(/\s+/g, " ")
    .trim();
}

function firstHeading(body) {
  let fenced = false;
  for (const line of body.split("\n")) {
    if (/^(```|~~~)/.test(line)) fenced = !fenced;
    if (fenced) continue;
    const m = line.match(/^(#{1,6})\s+(.*?)\s*#*\s*$/);
    if (m) return { level: m[1].length, text: plainText(m[2]) };
  }
  return null;
}

// The first paragraph after the first heading: a piece's standfirst.
function firstParagraph(body) {
  const lines = body.split("\n");
  let i = lines.findIndex((l) => /^#\s/.test(l));
  i = i < 0 ? 0 : i + 1;
  while (i < lines.length && lines[i].trim() === "") i++;
  const para = [];
  for (; i < lines.length && lines[i].trim() !== ""; i++) para.push(lines[i]);
  const text = para.join(" ");
  if (!text || /^([#|>!]|---)/.test(text.trim())) return "";
  // At most two sentences, so that an index entry stays short.
  const sentences = plainText(text).split(/(?<=[.?!])\s+(?=["'A-Z0-9])/);
  const first = sentences[0] || "";
  return first.split(" ").length >= 30 || sentences.length < 2 ? first : `${first} ${sentences[1]}`;
}

const MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];

// "26 September 2026" as a date at midnight UTC, or null.
export function longDate(text) {
  const m = String(text || "").match(/\b(\d{1,2}) ([A-Za-z]+) (\d{4})\b/);
  if (!m) return null;
  const month = MONTHS.indexOf(m[2].toLowerCase());
  return month < 0 ? null : new Date(Date.UTC(Number(m[3]), month, Number(m[1])));
}

// A piece's italic date line, `*26 September 2026 · Lighthouse*`, among the
// first few paragraphs after its title: the day it was published.
export function bylineDate(body) {
  const blocks = body.split(/\n\s*\n/);
  let start = blocks.findIndex((b) => /^#\s/.test(b.trim()));
  start = start < 0 ? 0 : start + 1;
  for (const block of blocks.slice(start, start + 6)) {
    const m = block.trim().match(/^[*_]([^*_\n]+)[*_]$/);
    if (m && longDate(m[1])) return longDate(m[1]);
  }
  return null;
}

// A `revised` item, `2026-09-27: sentence`: a substantive revision.
export function parseRevision(item) {
  const m = String(item || "").match(/^(\d{4}-\d{2}-\d{2})\s*:?\s*([\s\S]*)$/);
  const date = m ? headerDate(m[1]) : null;
  return { date: formatDate(date), iso: m ? m[1] : "", time: date ? date.getTime() : 0, text: m ? m[2].trim() : String(item || "").trim() };
}

// What the site reads from a piece: its header if it has one, else its byline
// and first paragraph, else git.
export function pieceInfo(header, body, time) {
  const field = (name) => headerField(header && header.fields, name);
  const value = (name) => (field(name) ? field(name).value.trim() : "");
  const fromHeader = headerDate(value("published"));
  const fromByline = fromHeader ? null : bylineDate(body);
  const published = fromHeader || fromByline || new Date(time);
  const revisions = (field("revised") ? field("revised").items : []).map(parseRevision);
  const latestRevision = revisions.filter((r) => r.time).sort((a, b) => b.time - a.time)[0] || null;
  const status = value("status").toLowerCase() || "released";
  return {
    pubTime: published.getTime(),
    published: formatDate(published),
    publishedIso: published.toISOString().slice(0, 10),
    publishedFrom: fromHeader ? "header" : fromByline ? "byline" : "git",
    summary: plainText(value("summary")) || firstParagraph(body),
    status,
    draft: status === "draft",
    investigationId: value("investigation"),
    revisions,
    revised: latestRevision ? latestRevision.date : "",
    revisedTime: latestRevision ? latestRevision.time : 0,
  };
}

function titleFromName(rel) {
  const base = path.posix.basename(rel, ".md").replace(/[-_]+/g, " ");
  return base.charAt(0).toUpperCase() + base.slice(1);
}

function describe(rel, { hasAbout = false } = {}) {
  if (rel.startsWith("articles/short/")) return { section: "articles", label: "Short form", short: true };
  if (rel.startsWith("articles/")) return { section: "articles", label: "Piece", short: false };
  if (rel.startsWith("studies/")) {
    const id = rel.split("/")[1];
    return { section: "studies", label: rel.split("/").length > 2 ? `Study ${id}` : "Studies", study: id };
  }
  if (rel.startsWith("notes/")) return { section: "notes", label: "Note" };
  if (/^investigations\/[^/]+\.md$/.test(rel)) return { section: "investigations", label: "Investigation" };
  if (rel === "AGENTS.md") return { section: "about", label: hasAbout ? "Operating manual" : ROOT_LABELS[rel] };
  if (rel === "about.md") return { section: "about", label: ROOT_LABELS[rel] };
  if (ROOT_LABELS[rel]) return { section: rel.replace(/\.md$/, ""), label: ROOT_LABELS[rel] };
  return { section: "", label: "" };
}

// A path named in an investigation's header, from the root (articles/x.md) or
// from the investigation (../articles/x.md), or written as a Markdown link.
function namedPath(text, from) {
  let t = String(text || "").trim();
  const link = t.match(/\]\(([^)\s]+)\)/);
  if (link) t = link[1];
  t = t.replace(/^`|`$/g, "").split(/\s/)[0].replace(/[#?].*$/, "");
  if (!t) return "";
  const joined = /^\.\.?\//.test(t) ? path.posix.join(path.posix.dirname(from), t) : t.replace(/^\/+/, "");
  return path.posix.normalize(joined).replace(/\/$/, "");
}

const link = (p) => (p ? { title: p.title, url: p.url, path: p.path } : null);

// Options: `siteFile`, the JSON file holding the site's description
// (site/site.json by default).
export function scanRepo(root, { siteFile = path.join(root, "site", "site.json") } = {}) {
  const { files, dirs } = walk(root);
  const { dates, added } = gitDates(root);
  const commit = gitCommit(root);
  const buildDate = new Date();
  const hasAbout = files.includes("about.md");
  const warnings = [];

  const pages = [];
  const byPath = {};
  for (const rel of files.filter((f) => f.toLowerCase().endsWith(".md"))) {
    const raw = fs.readFileSync(path.join(root, rel), "utf8");
    const header = parseHeader(raw);
    const body = header ? header.body : raw.replace(/\r\n?/g, "\n");
    const heading = firstHeading(body);
    const info = describe(rel, { hasAbout });
    const isPiece = info.section === "articles";
    let time = dates.get(rel);
    if (!time) time = fs.statSync(path.join(root, rel)).mtimeMs;
    const title = plainText(header && header.title) || (heading && heading.text) || titleFromName(rel);
    const startsWithH1 = Boolean(heading && heading.level === 1 && /^\s*#\s/.test(body.trimStart().split("\n")[0]));
    const page = {
      path: rel,
      url: pageUrl(rel),
      source: sourceUrl(rel),
      title,
      // A piece's header is read by the site, not shown as a record's facts.
      header: header && !isPiece ? header.fields.filter((f) => f.key.toLowerCase() !== "title") : null,
      kind: header ? header.kind : "",
      version: header ? header.version : "",
      docDate: header ? formatDate(headerDate(header.date)) : "",
      ownH1: (!header || isPiece) && startsWithH1,
      summary: "",
      time,
      added: added.get(rel) || time,
      changed: formatDate(time),
      ...info,
      ...(isPiece ? pieceInfo(header, body, time) : {}),
    };
    // In lists, AGENTS.md (titled "Lighthouse") reads as its label.
    page.listTitle = title === "Lighthouse" && page.label ? page.label : title;
    page.showLabel = Boolean(page.label) && page.listTitle.toLowerCase().replace(/^the /, "") !== page.label.toLowerCase();
    if (info.section === "investigations" && header) {
      page.fields = header.fields;
    }
    pages.push(page);
    byPath[rel] = page;
  }

  const images = files.filter((f) => IMAGE_EXT.includes(path.posix.extname(f).toLowerCase()));

  // Pieces by publication date, newest first (on the same day, the one added
  // to the repository last); each full piece is paired with the short form of
  // the same file name.
  const byPublished = (a, b) => b.pubTime - a.pubTime || b.added - a.added || a.path.localeCompare(b.path);
  const shorts = pages.filter((p) => p.short).sort(byPublished);
  const fulls = pages.filter((p) => p.section === "articles" && !p.short).sort(byPublished);
  const twinOf = new Map();
  for (const full of fulls) {
    const twin = shorts.find((s) => path.posix.basename(s.path) === path.posix.basename(full.path));
    if (twin) {
      twinOf.set(full.path, twin);
      twinOf.set(twin.path, full);
    }
  }
  const pieceGroups = [
    ...fulls.map((full) => ({ lead: full, twin: twinOf.get(full.path) || null })),
    ...shorts.filter((s) => !twinOf.has(s.path)).map((s) => ({ lead: s, twin: null })),
  ].sort((a, b) => byPublished(a.lead, b.lead));
  // The flat list, each full piece followed by its short form.
  const pieces = pieceGroups.flatMap((g) => (g.twin ? [g.lead, g.twin] : [g.lead]));

  // Investigations: investigations/<id>.md with a header naming its question,
  // current account, pieces in reading order and studies.
  const investigations = [];
  const investigationsById = {};
  for (const page of pages.filter((p) => p.section === "investigations" && p.fields)) {
    const field = (name) => headerField(page.fields, name);
    const value = (name) => (field(name) ? field(name).value.trim() : "");
    const resolve = (text, what) => {
      const rel = namedPath(text, page.path);
      const found = byPath[rel];
      if (!found) warnings.push(`${page.path}: ${what} ${text} is not a page in the repository`);
      return found || null;
    };
    const id = value("id") || path.posix.basename(page.path, ".md");
    const current = value("current") ? resolve(value("current"), "current account") : null;
    const inv = {
      id,
      path: page.path,
      url: page.url,
      title: page.title,
      question: value("question"),
      attention: value("attention").toLowerCase(),
      started: formatDate(headerDate(value("started"))),
      current: link(current),
      pieces: (field("pieces") ? field("pieces").items : [])
        .map((item) => resolve(item, "piece"))
        .filter(Boolean)
        .map((p) => ({ ...link(p), short: p.short, draft: p.draft, published: p.published, twin: link(twinOf.get(p.path)) })),
      studies: (field("studies") ? field("studies").items : [])
        .map((item) => resolve(item, "study"))
        .filter(Boolean)
        .map((p) => ({ ...link(p), study: p.study || "" })),
    };
    page.investigation = inv;
    page.summary = plainText(inv.question);
    if (investigationsById[id]) warnings.push(`${page.path}: investigation id ${id} is also used by ${investigationsById[id].path}`);
    else {
      investigationsById[id] = inv;
      investigations.push(inv);
    }
  }
  investigations.sort((a, b) => a.title.localeCompare(b.title));

  // What a piece shows around its text: its twin, and, when it or its full
  // form names an investigation, the investigation, its current account and
  // the pieces before and after it in the investigation's order.
  for (const p of pieces) {
    const twin = twinOf.get(p.path) || null;
    const full = p.short ? twin : p;
    const id = p.investigationId || (twin && twin.investigationId) || "";
    const context = { twin: twin ? { ...link(twin), short: twin.short } : null, investigation: null };
    if (id && !investigationsById[id]) {
      if (p.investigationId) warnings.push(`${p.path}: investigation ${id} has no investigations/${id}.md with a header`);
    } else if (id) {
      const inv = investigationsById[id];
      const order = inv.pieces.map((x) => x.path);
      const at = order.indexOf(full ? full.path : p.path);
      // A short form's neighbours are the other short forms where they exist.
      const near = (x) => (x ? (p.short && x.twin ? x.twin : link(x)) : null);
      const isCurrent = inv.current && (inv.current.path === p.path || (full && inv.current.path === full.path));
      context.investigation = { title: inv.title, url: inv.url };
      context.current = isCurrent ? null : inv.current;
      context.prev = at > 0 ? near(inv.pieces[at - 1]) : null;
      context.next = at >= 0 && at < order.length - 1 ? near(inv.pieces[at + 1]) : null;
    }
    p.context = context;
  }

  // One entry per study directory: the write-up first, then the other files.
  const studies = dirs
    .filter((d) => /^studies\/[^/]+$/.test(d))
    .map((d) => {
      const id = d.split("/")[1];
      const inDir = pages.filter((p) => path.posix.dirname(p.path) === d);
      const writeup =
        inDir.find((p) => path.posix.basename(p.path, ".md") === id) || inDir.find((p) => p.header) || null;
      const sorted = inDir.sort((a, b) => a.path.localeCompare(b.path));
      // Without a write-up yet, the study is led by its brief or first file.
      const lead = writeup || sorted.find((p) => path.posix.basename(p.path) === "brief.md") || sorted[0];
      const others = sorted.filter((p) => p !== lead);
      const time = Math.max(0, ...inDir.map((p) => p.time));
      return { id, dir: d, url: `/${d}/`, source: sourceUrl(d, true), writeup, lead, others, time, changed: formatDate(time) };
    })
    .filter((s) => s.lead)
    .sort((a, b) => b.id.localeCompare(a.id, "en", { numeric: true }));

  const notes = pages
    .filter((p) => p.section === "notes")
    .map((p) => {
      // By the day the note gives in its header, else the day it last changed.
      const day = headerDate(p.header && p.header.find((f) => f.key.toLowerCase() === "date")?.value) || new Date(p.time);
      return { ...p, sortDay: Math.floor(day.getTime() / 86400000) };
    })
    .sort((a, b) => b.sortDay - a.sortDay || b.time - a.time || b.path.localeCompare(a.path));

  // The front page's latest: released pieces by publication date, each full
  // piece with its short form. Drafts, records and notes are left out.
  const latest = pieceGroups
    .filter((g) => !g.lead.draft)
    .map((g) => ({ lead: g.lead, twin: g.twin && !g.twin.draft ? g.twin : null }))
    .slice(0, 8);

  // Directories with an index page, so that links to them resolve.
  const siteDirs = new Set(SECTION_DIRS.filter((d) => dirs.includes(d)));
  for (const s of studies) siteDirs.add(s.dir);

  // The site's description, from site/site.json; else the first sentence of
  // AGENTS.md's first paragraph.
  let strap = "";
  try {
    strap = String(JSON.parse(fs.readFileSync(siteFile, "utf8")).description || "").trim();
  } catch {
    // No site.json: fall back to AGENTS.md below.
  }
  if (!strap && byPath["AGENTS.md"]) {
    const agents = fs.readFileSync(path.join(root, "AGENTS.md"), "utf8").replace(/\r\n?/g, "\n");
    const para = agents.split(/\n\s*\n/).find((b) => b.trim() && !/^#/.test(b.trim())) || "";
    const m = plainText(para).match(/^(.+?[.!?])(\s|$)/);
    strap = m ? m[1] : plainText(para);
  }

  return {
    root,
    pages,
    byPath,
    images,
    fileSet: new Set(files),
    dirSet: new Set(dirs),
    siteDirs,
    pieces,
    pieceGroups,
    shorts,
    investigations,
    investigationsById,
    hasInvestigations: dirs.includes("investigations"),
    hasAbout,
    studies,
    notes,
    latest,
    strap,
    warnings,
    commit,
    commitUrl: commit ? `${REPO_URL}/commit/${commit}` : "",
    repoUrl: REPO_URL,
    buildDate: formatDate(buildDate),
    buildIso: buildDate.toISOString(),
  };
}
