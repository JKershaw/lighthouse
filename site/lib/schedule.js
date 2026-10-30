// The schedule page's data: schedule/due.csv, read at build time and arranged
// into a calendar of weeks and short lists. "Today" is the build's UTC date,
// so the page is as current as the last build of main.

import fs from "node:fs";
import path from "node:path";

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
const PLACES = { media: "/notes/php-media-sweep/plan/", log: "/notes/php-watch-log/", articles: "/articles/", essays: "/essays/" };
export function hrefFor(study) {
  return /^LH\d+$/.test(study) ? `/studies/${study}/` : PLACES[study] || "";
}

export function buildSchedule(root, now = new Date()) {
  const file = path.join(root, SCHEDULE_TABLE);
  if (!fs.existsSync(file)) return null;
  const today = iso(now);
  const rows = parseCsv(fs.readFileSync(file, "utf8")).map((r) => ({
    ...r, state: stateOf(r, today), stateLabel: LABELS[stateOf(r, today)] || r.status, href: hrefFor(r.study),
  }));

  // Weeks from the Monday of last week to six weeks ahead, each a row of seven days.
  const start = addDays(now, -((now.getUTCDay() + 6) % 7) - 7);
  const weeks = [];
  for (let w = 0; w < 8; w++) {
    const days = [];
    for (let d = 0; d < 7; d++) {
      const date = iso(addDays(start, w * 7 + d));
      const items = rows.filter((r) => r.earliest === date && r.latest && r.status !== "cancelled");
      days.push({ date, day: Number(date.slice(8)), month: date.slice(5, 7), isToday: date === today, isPast: date < today, items });
    }
    weeks.push({ label: weeks.length === 0 ? "Last week" : "", days });
  }
  const first = weeks[0].days[0].date, last = weeks.at(-1).days[6].date;

  const counts = {};
  for (const r of rows) counts[r.state] = (counts[r.state] || 0) + 1;
  const pick = (states) => rows.filter((r) => states.includes(r.state));
  return {
    today,
    total: rows.length,
    counts: Object.entries(LABELS).filter(([k]) => counts[k]).map(([k, label]) => ({ state: k, label, n: counts[k] })),
    weeks,
    attention: pick(["overdue", "keeper", "blocked", "running"]),
    due: pick(["due"]).filter((r) => r.latest),
    openEnded: rows.filter((r) => !r.latest && ["due", "upcoming", "running", "keeper", "blocked"].includes(r.state)),
    beyond: rows.filter((r) => r.latest && r.earliest > last && r.state === "upcoming"),
    recent: rows.filter((r) => ["done", "missed"].includes(r.state)).sort((a, b) => (b.updated || "").localeCompare(a.updated || "")).slice(0, 12),
    range: { first, last },
  };
}
