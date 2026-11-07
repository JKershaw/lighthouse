// Tests for the schedule page's data: links from a row to what it produced,
// and the calendar day of a row without an end date.

import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { buildSchedule, refParts, dayOf } from "../lib/schedule.js";

const HEAD = "id,study,task,earliest,latest,status,updated,by,ref,note";

function withRepo(files, fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "lighthouse-schedule-"));
  try {
    for (const [rel, text] of Object.entries(files)) {
      fs.mkdirSync(path.dirname(path.join(dir, rel)), { recursive: true });
      fs.writeFileSync(path.join(dir, rel), text);
    }
    return fn(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test("a ref links each file it names: a Markdown file to its page, others to their source", () => {
  withRepo({
    "studies/LH001/checkpoints/2026-11-05.md": "# x\n",
    "studies/LH001/scripts/collect.py": "",
    "studies/LH001/data/read-2026-11-05T1414Z/log.json": "{}",
    "programme.md": "# p\n",
  }, (root) => {
    const parts = refParts("studies/LH001/checkpoints/2026-11-05.md (0.2); studies/LH001/scripts/collect.py, programme.md Next; notes/R-0043 to R-0045", root);
    assert.deepEqual(parts.filter((p) => p.href).map((p) => [p.text, p.href]), [
      ["studies/LH001/checkpoints/2026-11-05.md", "/studies/LH001/checkpoints/2026-11-05/"],
      ["studies/LH001/scripts/collect.py", "https://github.com/JKershaw/lighthouse/blob/main/studies/LH001/scripts/collect.py"],
      ["programme.md", "/programme/"],
    ]);
    assert.equal(parts.map((p) => p.text).join(""), "studies/LH001/checkpoints/2026-11-05.md (0.2); studies/LH001/scripts/collect.py, programme.md Next; notes/R-0043 to R-0045");
    const dir = refParts("studies/LH001/data/read-2026-11-05T1414Z", root);
    assert.equal(dir[0].href, "https://github.com/JKershaw/lighthouse/tree/main/studies/LH001/data/read-2026-11-05T1414Z/");
    assert.deepEqual(refParts("", root), []);
    assert.deepEqual(refParts("site/README.md; ../etc/passwd", root).filter((p) => p.href), []);
  });
});

test("a row without an end date sits on the day it was done; a windowed row on the day it opens", () => {
  assert.equal(dayOf({ earliest: "2026-11-05", latest: "2026-11-06", status: "done", updated: "2026-11-06" }), "2026-11-05");
  assert.equal(dayOf({ earliest: "2026-11-06", latest: "", status: "done", updated: "2026-11-06T1450Z" }), "2026-11-06");
  assert.equal(dayOf({ earliest: "2026-11-09", latest: "", status: "open", updated: "2026-11-01" }), "");
  assert.equal(dayOf({ earliest: "2026-11-05", latest: "2026-11-06", status: "cancelled", updated: "" }), "");
});

test("a finished row's chip leads to what it produced; an unfinished one to its study", () => {
  const table = [
    HEAD,
    "LH001-2026-11-05,LH001,Thursday read,2026-11-05,2026-11-06,done,2026-11-05,run,studies/LH001/checkpoints/2026-11-05.md,",
    "LH001-raw,LH001,Re-read the rows,2026-11-06,,done,2026-11-06T1450Z,run,studies/LH001/LH001.md (0.3),",
    "LH001-2026-11-09,LH001,\"Monday read: collect.py --read <label>\",2026-11-09,2026-11-10,open,2026-11-01,,,",
    "LH001-gone,LH001,A read whose file is not here,2026-11-02,2026-11-03,done,2026-11-02,run,studies/LH001/checkpoints/2026-11-02.md,",
  ].join("\r\n") + "\r\n";
  withRepo({
    "schedule/due.csv": table,
    "schedule/runs.csv": "started,by,did,commit\n2026-11-06T1416Z,scheduled run,LH001 re-read,0d10641\n2026-11-05T1414Z,scheduled run,reads,\n",
    "studies/LH001/LH001.md": "# x\n",
    "studies/LH001/checkpoints/2026-11-05.md": "# y\n",
  }, (root) => {
    const s = buildSchedule(root, new Date("2026-11-07T08:00:00Z"));
    const byId = Object.fromEntries(s.weeks.flatMap((w) => w.days).flatMap((d) => d.items.map((r) => [r.id, { href: r.href, date: d.date }])));
    assert.deepEqual(byId["LH001-2026-11-05"], { href: "/studies/LH001/checkpoints/2026-11-05/", date: "2026-11-05" });
    assert.deepEqual(byId["LH001-raw"], { href: "/studies/LH001/LH001/", date: "2026-11-06" });
    assert.deepEqual(byId["LH001-2026-11-09"], { href: "/studies/LH001/", date: "2026-11-09" });
    assert.equal(byId["LH001-gone"].href, "/studies/LH001/", "a ref naming no file present falls back to the study");
    assert.equal(s.recent[0].id, "LH001-raw");
    assert.equal(s.runs[0].commitUrl, "https://github.com/JKershaw/lighthouse/commit/0d10641");
    assert.equal(s.runs[1].commitUrl, "");
  });
});
