// The schedule page's data: schedule/due.csv, read at build time and arranged
// into a calendar of weeks and short lists. "Today" is the build's UTC date,
// so the page is as current as the last build of main.

import fs from "node:fs";
import path from "node:path";
import { REPO_URL, formatDate, isIgnored, pageUrl, plainText, sourceUrl } from "./repo.js";
import { slugify } from "./markdown.js";

export const SCHEDULE_TABLE = "schedule/due.csv";

// A small CSV reader: quoted fields may hold commas, quotes ("") and newlines.
export function parseCsv(text) {
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = "";
      if (row.some((v) => v !== "")) rows.push(row);
      row = [];
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); if (row.some((v) => v !== "")) rows.push(row); }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head.map((k, i) => [k, r[i] ?? ""])));
}

const iso = (d) => d.toISOString().slice(0, 10);
const addDays = (d, n) => new Date(d.getTime() + n * 86400000);

// What a row's status means today: open rows become due, overdue or upcoming.
export function stateOf(row, today) {
  if (row.status !== "open") return row.status;
  if (row.latest && row.latest < today) return "overdue";
  if (!row.earliest || row.earliest <= today) return "due";
  return "upcoming";
}

const LABELS = {
  due: "Due now", overdue: "Overdue", upcoming: "Upcoming", running: "In progress", done: "Done",
  missed: "Missed", blocked: "Blocked", keeper: "Waiting on the keeper", cancelled: "Cancelled",
};

// Where a row's study label leads: a study's directory, or the page its work lives on.
const PLACES = { media: "/notes/php-media-sweep/plan/", horizon: "/notes/horizon/plan/", log: "/notes/php-watch-log/", articles: "/articles/", essays: "/essays/" };
export function hrefFor(study) {
  return /^LH\d+$/.test(study) ? `/studies/${study}/` : PLACES[study] || "";
}

// A row's ref split into text and links, for what the work produced: a
// Markdown file in the repository links to its page, any other file or a
// directory to its source on GitHub. Text that names nothing present stays text.
export function refParts(ref, root) {
  const text = String(ref || "");
  const parts = [];
  let last = 0;
  for (const m of text.matchAll(/[\w./-]+/g)) {
    const token = m[0].replace(/[.,;:]+$/, "");
    const rel = token.replace(/^\/+/, "").replace(/\/$/, "");
    if (!rel || !(rel.includes("/") || /\.md$/i.test(rel)) || rel.split("/").includes("..") || isIgnored(rel)) continue;
    const full = path.join(root, rel);
    if (!fs.existsSync(full)) continue;
    const isDir = fs.statSync(full).isDirectory();
    const page = !isDir && /\.md$/i.test(rel);
    if (m.index > last) parts.push({ text: text.slice(last, m.index) });
    parts.push({ text: token, href: page ? pageUrl(rel) : sourceUrl(rel, isDir), page });
    last = m.index + token.length;
  }
  if (last < text.length) parts.push({ text: text.slice(last) });
  return parts;
}

// The calendar day a row sits on: the day its window opens, or, for a row
// without an end date, the day it was claimed or done.
export function dayOf(row) {
  if (row.status === "cancelled") return "";
  if (row.latest) return row.earliest;
  return ["done", "missed", "running"].includes(row.status) ? (row.updated || "").slice(0, 10) : "";
}

// A page's title as a reader sees it: its header's title, else its first heading.
function titleOf(root, rel) {
  try {
    const text = fs.readFileSync(path.join(root, rel), "utf8");
    const m = text.match(/^title:\s*(.+)$/m) || text.match(/^#\s+(.+)$/m);
    return m ? plainText(m[1].trim()) : rel;
  } catch {
    return rel;
  }
}

// "2026-11-06T1416Z" as a time and as words.
function runTime(label) {
  const m = String(label || "").match(/^(\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})Z$/);
  if (!m) return { iso: "", words: label || "" };
  return { iso: `${m[1]}T${m[2]}:${m[3]}Z`, words: `${formatDate(new Date(`${m[1]}T00:00:00Z`))}, ${m[2]}:${m[3]} UTC` };
}

// The front page's view of the newest run: when it started and what it
// finished, each linked to what it produced, newest work being unreviewed.
export function latestRun(run, rows, root, shown = 4) {
  if (!run) return null;
  const seen = new Set();
  const done = [];
  for (const r of rows) {
    if (!["done", "missed"].includes(r.status) || !run.started || !(r.by || "").includes(run.started)) continue;
    const made = r.refs.find((p) => p.page);
    const href = made ? made.href : r.href;
    if (href && seen.has(href)) continue;
    if (href) seen.add(href);
    const rel = made ? made.text.replace(/^\/+/, "") : "";
    done.push({ text: r.status === "missed" ? `${r.id} (missed)` : rel ? titleOf(root, rel) : r.id, href });
  }
  const t = runTime(run.started);
  const more = Math.max(0, done.length - shown);
  const last = more ? "" : (done.length ? done[Math.min(done.length, shown) - 1].text : run.did || "");
  // The sentence's full stop, unless the last title already ends one.
  const stop = /[.?!]$/.test(last) ? "" : ".";
  return { started: run.started, iso: t.iso, when: t.words, by: run.by, did: run.did, done: done.slice(0, shown), more, count: done.length, stop };
}

// What proposals.md says is being looked into: the proposals under its
// "Started without review" and "Agreed by the keeper" headings.
export const PROPOSALS = "proposals.md";
export function proposalsNow(root) {
  const file = path.join(root, PROPOSALS);
  if (!fs.existsSync(file)) return null;
  const text = fs.readFileSync(file, "utf8").replace(/\r\n?/g, "\n");
  const section = (name) => {
    const m = text.match(new RegExp(`^## ${name}\\s*$([\\s\\S]*?)(?=^## |(?![\\s\\S]))`, "m"));
    if (!m) return [];
    return [...m[1].matchAll(/^### (P-\d+) (.+)$/gm)].map((h) => {
      const heading = `${h[1]} ${h[2].trim()}`;
      return { id: h[1], title: plainText(h[2].trim()), href: `${pageUrl(PROPOSALS)}#${slugify(plainText(heading))}` };
    });
  };
  // Waiting for the keeper: every proposal whose status says so, wherever it sits.
  const waiting = [...text.matchAll(/^### (P-\d+) (.+)$([\s\S]*?)(?=^### |^## |(?![\s\S]))/gm)]
    .filter((m) => /Status:\s*waiting for the keeper/i.test(m[3]))
    .map((m) => ({ id: m[1], title: plainText(m[2].trim()), href: `${pageUrl(PROPOSALS)}#${slugify(plainText(`${m[1]} ${m[2].trim()}`))}` }));
  return { started: section("Started without review"), agreed: section("Agreed by the keeper"), waiting, url: pageUrl(PROPOSALS) };
}

export function buildSchedule(root, now = new Date()) {
  const file = path.join(root, SCHEDULE_TABLE);
  if (!fs.existsSync(file)) return null;
  const today = iso(now);
  const rows = parseCsv(fs.readFileSync(file, "utf8")).map((r) => {
    const state = stateOf(r, today);
    const refs = refParts(r.ref, root);
    // A finished row leads to what it produced; any other to its study.
    const made = ["done", "missed"].includes(state) && refs.find((p) => p.page);
    return { ...r, state, stateLabel: LABELS[state] || r.status, refs, href: made ? made.href : hrefFor(r.study), day: dayOf(r) };
  });

  // Weeks from the Monday of last week to six weeks ahead, each a row of seven days.
  const start = addDays(now, -((now.getUTCDay() + 6) % 7) - 7);
  const weeks = [];
  for (let w = 0; w < 8; w++) {
    const days = [];
    for (let d = 0; d < 7; d++) {
      const date = iso(addDays(start, w * 7 + d));
      const items = rows.filter((r) => r.day === date);
      days.push({ date, day: Number(date.slice(8)), month: date.slice(5, 7), isToday: date === today, isPast: date < today, items });
    }
    weeks.push({ label: weeks.length === 0 ? "Last week" : "", days });
  }
  const first = weeks[0].days[0].date, last = weeks.at(-1).days[6].date;

  const runsFile = path.join(root, "schedule/runs.csv");
  const runs = fs.existsSync(runsFile) ? parseCsv(fs.readFileSync(runsFile, "utf8")).sort((a, b) => b.started.localeCompare(a.started)) : [];

  const counts = {};
  for (const r of rows) counts[r.state] = (counts[r.state] || 0) + 1;
  const pick = (states) => rows.filter((r) => states.includes(r.state));
  return {
    today,
    total: rows.length,
    counts: Object.entries(LABELS).filter(([k]) => counts[k]).map(([k, label]) => ({ state: k, label, n: counts[k] })),
    weeks,
    attention: pick(["overdue", "keeper", "blocked", "running"]),
    keeperRows: pick(["keeper"]),
    due: pick(["due"]).filter((r) => r.latest),
    openEnded: rows.filter((r) => !r.latest && ["due", "upcoming", "running", "keeper", "blocked"].includes(r.state)),
    beyond: rows.filter((r) => r.latest && r.earliest > last && r.state === "upcoming"),
    recent: rows.filter((r) => ["done", "missed"].includes(r.state)).sort((a, b) => (b.updated || "").localeCompare(a.updated || "")).slice(0, 12),
    range: { first, last },
    lastRun: runs[0] || null,
    latestRun: latestRun(runs[0], rows, root),
    proposals: proposalsNow(root),
    runs: runs.slice(0, 8).map((r) => ({ ...r, commitUrl: /^[0-9a-f]{7,40}$/.test(r.commit || "") ? `${REPO_URL}/commit/${r.commit}` : "" })),
  };
}
