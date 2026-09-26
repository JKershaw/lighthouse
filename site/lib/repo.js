// Reads the repository once per build: which Markdown files become pages,
// their titles, headers and git dates, which images are copied, and the
// indexes built from them. Nothing here is a registry; it is all found.

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { parseHeader } from "./header.js";

export const REPO_URL = "https://github.com/JKershaw/lighthouse";
export const REPO_BRANCH = "main";

// Paths the site never reads, relative to the repository root.
export const IGNORED_DIRS = ["harbour", "site", "node_modules", ".claude", ".github", ".git"];
export const IGNORED_FILES = ["CLAUDE.md"];
export const IMAGE_EXT = [".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"];

// Directories that get an index page of their own.
const SECTION_DIRS = ["articles", "articles/short", "studies", "notes"];

const ROOT_LABELS = {
  "AGENTS.md": "About",
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

// One `git log` for the whole repository: the newest commit that touched each path.
function gitDates(root) {
  const dates = new Map();
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
      }
    }
  } catch {
    // Not a git checkout: fall back to file times below.
  }
  return dates;
}

function gitCommit(root) {
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

function titleFromName(rel) {
  const base = path.posix.basename(rel, ".md").replace(/[-_]+/g, " ");
  return base.charAt(0).toUpperCase() + base.slice(1);
}

function describe(rel) {
  if (rel.startsWith("articles/short/")) return { section: "articles", label: "Short form", short: true };
  if (rel.startsWith("articles/")) return { section: "articles", label: "Piece", short: false };
  if (rel.startsWith("studies/")) {
    const id = rel.split("/")[1];
    return { section: "studies", label: rel.split("/").length > 2 ? `Study ${id}` : "Studies", study: id };
  }
  if (rel.startsWith("notes/")) return { section: "notes", label: "Note" };
  if (ROOT_LABELS[rel]) return { section: rel === "AGENTS.md" ? "about" : rel.replace(/\.md$/, ""), label: ROOT_LABELS[rel] };
  return { section: "", label: "" };
}

export function scanRepo(root) {
  const { files, dirs } = walk(root);
  const dates = gitDates(root);
  const commit = gitCommit(root);
  const buildDate = new Date();

  const pages = [];
  const byPath = {};
  for (const rel of files.filter((f) => f.toLowerCase().endsWith(".md"))) {
    const raw = fs.readFileSync(path.join(root, rel), "utf8");
    const header = parseHeader(raw);
    const body = header ? header.body : raw.replace(/\r\n?/g, "\n");
    const heading = firstHeading(body);
    const info = describe(rel);
    let time = dates.get(rel);
    if (!time) time = fs.statSync(path.join(root, rel)).mtimeMs;
    const title = plainText(header && header.title) || (heading && heading.text) || titleFromName(rel);
    const page = {
      path: rel,
      url: pageUrl(rel),
      source: sourceUrl(rel),
      title,
      header: header ? header.fields.filter((f) => f.key.toLowerCase() !== "title") : null,
      kind: header ? header.kind : "",
      version: header ? header.version : "",
      docDate: header ? formatDate(headerDate(header.date)) : "",
      ownH1: !header && heading && heading.level === 1 && /^\s*#\s/.test(body.trimStart().split("\n")[0]),
      summary: info.section === "articles" ? firstParagraph(body) : "",
      time,
      changed: formatDate(time),
      ...info,
    };
    // In lists, AGENTS.md (titled "Lighthouse") reads as About.
    page.listTitle = title === "Lighthouse" && page.label ? page.label : title;
    page.showLabel = Boolean(page.label) && page.listTitle.toLowerCase().replace(/^the /, "") !== page.label.toLowerCase();
    pages.push(page);
    byPath[rel] = page;
  }

  const images = files.filter((f) => IMAGE_EXT.includes(path.posix.extname(f).toLowerCase()));

  // Pieces, each followed by its short form when it has one.
  const newestFirst = (a, b) => b.time - a.time || a.path.localeCompare(b.path);
  const shorts = pages.filter((p) => p.short).sort(newestFirst);
  const fulls = pages.filter((p) => p.section === "articles" && !p.short).sort(newestFirst);
  const pieces = [];
  const paired = new Set();
  for (const full of fulls) {
    pieces.push(full);
    const twin = shorts.find((s) => path.posix.basename(s.path) === path.posix.basename(full.path));
    if (twin) {
      pieces.push(twin);
      paired.add(twin.path);
    }
  }
  pieces.push(...shorts.filter((s) => !paired.has(s.path)));

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

  const latest = pages
    .filter((p) => p.path !== "README.md")
    .sort(newestFirst)
    .slice(0, 10);

  // Directories with an index page, so that links to them resolve.
  const siteDirs = new Set(SECTION_DIRS.filter((d) => dirs.includes(d)));
  for (const s of studies) siteDirs.add(s.dir);

  // The strap: the first sentence of AGENTS.md's first paragraph.
  let strap = "";
  if (byPath["AGENTS.md"]) {
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
    shorts,
    studies,
    notes,
    latest,
    strap,
    commit,
    commitUrl: commit ? `${REPO_URL}/commit/${commit}` : "",
    repoUrl: REPO_URL,
    buildDate: formatDate(buildDate),
    buildIso: buildDate.toISOString(),
  };
}
