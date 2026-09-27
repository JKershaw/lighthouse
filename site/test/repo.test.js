// Tests for the repository scan and the HTML rewrites, against a small
// fixture repository with no git history. Run with `npm test` in site/.

import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { scanRepo, bylineDate, longDate, parseRevision } from "../lib/repo.js";
import { parseHeader } from "../lib/header.js";
import { markNotices, arrangeOpening, arrangePiece, noticeKind } from "../lib/html.js";

const fixture = path.join(path.dirname(fileURLToPath(import.meta.url)), "fixtures", "repo");

// A copy outside any git checkout, with fixed file times standing in for git.
function scanCopy({ touch = {}, siteJson } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "lighthouse-fixture-"));
  fs.cpSync(fixture, dir, { recursive: true });
  const at = (iso) => new Date(iso);
  const walk = (d) =>
    fs.readdirSync(d, { withFileTypes: true }).forEach((e) => {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else fs.utimesSync(p, at("2026-09-21T12:00:00Z"), at("2026-09-21T12:00:00Z"));
    });
  walk(dir);
  for (const [rel, iso] of Object.entries(touch)) fs.utimesSync(path.join(dir, rel), at(iso), at(iso));
  const siteFile = path.join(dir, "site.json");
  if (siteJson) fs.writeFileSync(siteFile, JSON.stringify(siteJson));
  try {
    return scanRepo(dir, { siteFile });
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test("a piece header of one known field is read; other single lines are not headers", () => {
  assert.ok(parseHeader("investigation: x\n\n# Title\n"));
  assert.equal(parseHeader("Note: something\n\n# Title\n"), null);
});

test("dates: byline, long dates and revision items", () => {
  assert.equal(longDate("26 September 2026 · Lighthouse").toISOString(), "2026-09-26T00:00:00.000Z");
  assert.equal(longDate("no date"), null);
  assert.equal(bylineDate("# T\n\nOpening.\n\n*3 March 2025 · Lighthouse*\n\nBody.").toISOString().slice(0, 10), "2025-03-03");
  assert.equal(bylineDate("# T\n\nOpening only."), null);
  const r = parseRevision("2026-09-27: A later piece narrows it.");
  assert.equal(r.date, "27 September 2026");
  assert.equal(r.text, "A later piece narrows it.");
});

test("publication date: header, then byline, then file or git time", () => {
  const repo = scanCopy();
  const p = (rel) => repo.byPath[rel];
  assert.equal(p("articles/updated.md").publishedIso, "2026-09-25");
  assert.equal(p("articles/updated.md").publishedFrom, "header");
  assert.equal(p("articles/legacy.md").publishedIso, "2026-09-20");
  assert.equal(p("articles/legacy.md").publishedFrom, "byline");
  assert.equal(p("articles/undated.md").publishedIso, "2026-09-21");
  assert.equal(p("articles/undated.md").publishedFrom, "git");
  // Not a git checkout: no commit, and file times stand in.
  assert.equal(repo.commit, "");
});

test("the fixture inside this repository is not mistaken for its git root", () => {
  const repo = scanRepo(fixture, { siteFile: path.join(fixture, "missing.json") });
  assert.equal(repo.commit, "");
  assert.equal(repo.byPath["articles/legacy.md"].publishedIso, "2026-09-20");
});

test("pieces sort by publication date, each full piece paired with its short form", () => {
  const repo = scanCopy();
  assert.deepEqual(
    repo.pieceGroups.map((g) => [g.lead.path, g.twin ? g.twin.path : null]),
    [
      ["articles/draft.md", null],
      ["articles/current.md", null],
      ["articles/updated.md", "articles/short/updated.md"],
      ["articles/undated.md", null],
      ["articles/legacy.md", "articles/short/legacy.md"],
      ["articles/stray.md", null],
    ],
  );
  assert.deepEqual(repo.pieces.slice(2, 4).map((p) => p.path), ["articles/updated.md", "articles/short/updated.md"]);
  assert.deepEqual(repo.shorts.map((p) => p.path), ["articles/short/updated.md", "articles/short/legacy.md"]);
  assert.equal(repo.byPath["articles/short/legacy.md"].context.twin.url, "/articles/legacy/");
  assert.equal(repo.byPath["articles/legacy.md"].context.twin.url, "/articles/short/legacy/");
});

test("summary: editorial when given, else the opening", () => {
  const repo = scanCopy();
  assert.equal(repo.byPath["articles/updated.md"].summary, "An editorial summary written for listings.");
  assert.equal(repo.byPath["articles/legacy.md"].summary, "The opening paragraph of the legacy piece. It has two sentences.");
  // A piece's header is not shown as a record's facts.
  assert.equal(repo.byPath["articles/updated.md"].header, null);
  assert.equal(repo.byPath["articles/updated.md"].ownH1, true);
});

test("drafts are labelled and left out of the latest list", () => {
  const repo = scanCopy();
  assert.equal(repo.byPath["articles/draft.md"].draft, true);
  assert.equal(repo.byPath["articles/updated.md"].draft, false);
  assert.ok(!repo.latest.some((g) => g.lead.path === "articles/draft.md"));
  assert.equal(repo.latest[0].lead.path, "articles/current.md");
  assert.ok(repo.latest.every((g) => g.lead.section === "articles"));
});

test("a revision is shown; an incidental edit changes neither publication nor revision", () => {
  const repo = scanCopy({ touch: { "articles/legacy.md": "2026-09-27T09:00:00Z" } });
  const legacy = repo.byPath["articles/legacy.md"];
  assert.equal(legacy.publishedIso, "2026-09-20");
  assert.equal(legacy.revised, "");
  assert.equal(legacy.changed, "27 September 2026");
  const updated = repo.byPath["articles/updated.md"];
  assert.equal(updated.revised, "27 September 2026");
  assert.equal(updated.revisions.length, 1);
});

test("investigations: order, current account, neighbours and warnings", () => {
  const repo = scanCopy();
  const inv = repo.investigationsById["fixture-inv"];
  assert.equal(inv.title, "Where does a fixture go?");
  assert.equal(inv.attention, "resting");
  assert.equal(inv.current.url, "/articles/current/");
  assert.deepEqual(inv.pieces.map((p) => p.path), ["articles/legacy.md", "articles/updated.md", "articles/current.md"]);
  assert.equal(inv.pieces[0].twin.url, "/articles/short/legacy/");
  assert.equal(inv.studies[0].study, "LH001");

  const updated = repo.byPath["articles/updated.md"].context;
  assert.equal(updated.investigation.url, "/investigations/fixture-inv/");
  assert.equal(updated.current.url, "/articles/current/");
  assert.equal(updated.prev.url, "/articles/legacy/");
  assert.equal(updated.next.url, "/articles/current/");

  // The current account does not point at itself; the last piece has no next.
  const current = repo.byPath["articles/current.md"].context;
  assert.equal(current.current, null);
  assert.equal(current.next, null);

  // A short form follows its full piece's investigation, among short forms.
  const short = repo.byPath["articles/short/updated.md"].context;
  assert.equal(short.investigation.url, "/investigations/fixture-inv/");
  assert.equal(short.prev.url, "/articles/short/legacy/");
  assert.equal(short.twin.url, "/articles/updated/");

  // A piece without a header gets only its twin link.
  assert.equal(repo.byPath["articles/legacy.md"].context.investigation, null);

  assert.ok(repo.warnings.some((w) => w.includes("no-such-investigation")));
  assert.equal(repo.byPath["articles/stray.md"].context.investigation, null);
  assert.equal(repo.byPath["investigations/fixture-inv.md"].section, "investigations");
  assert.equal(repo.hasInvestigations, true);
});

test("about.md makes AGENTS.md the operating manual; the description falls back to AGENTS.md", () => {
  const repo = scanCopy();
  assert.equal(repo.byPath["about.md"].section, "about");
  assert.equal(repo.byPath["AGENTS.md"].label, "Operating manual");
  assert.equal(repo.byPath["AGENTS.md"].listTitle, "Operating manual");
  assert.equal(repo.strap, "The fixture watches a small made-up repository.");
  assert.equal(scanCopy({ siteJson: { description: "From site.json." } }).strap, "From site.json.");
});

test("notices: Correction and Later evidence blockquotes, not others", () => {
  const later = '<blockquote>\n<p><strong>Later evidence, 27 September 2026.</strong> Text.</p>\n</blockquote>\n';
  const plain = "<blockquote>\n<p>A quotation.</p>\n</blockquote>\n";
  assert.equal(noticeKind(later), "later-evidence");
  assert.equal(noticeKind("<blockquote><p><strong>Correction, 1 May.</strong></p></blockquote>"), "correction");
  assert.equal(noticeKind(plain), "");
  assert.match(markNotices(later), /^<aside class="notice notice-later-evidence" aria-label="Later evidence">/);
  assert.equal(markNotices(plain), plain);
});

const page = (between) =>
  `<h1 id="t">T</h1>\n<p>Opening one.</p>\n<p>Opening two.</p>\n${between}<h2>Body</h2>\n<p>Text.</p>\n<hr>\n<p>Colophon.</p>`;
const notice = '<blockquote>\n<p><strong>Correction, 1 May 2026.</strong> Fixed.</p>\n</blockquote>\n';
const byline = "<p><em>1 May 2026 · Lighthouse</em></p>\n";

test("the opening and byline are marked with a notice before or after the byline", () => {
  for (const between of [byline + notice, notice + byline, byline]) {
    const out = arrangeOpening(markNotices(page(between))).html;
    assert.equal((out.match(/class="opening"/g) || []).length, 2, between);
    assert.match(out, /<p class="byline"><em>1 May 2026 · Lighthouse<\/em><\/p>/);
    assert.ok(!/<p class="opening"><strong>Correction/.test(out));
  }
  // Without a byline nothing is marked.
  assert.ok(!/class="opening"/.test(arrangeOpening(page("")).html));
});

test("the layout's context goes after the byline and its pager before the colophon rule", () => {
  const html =
    '<article><!--lh:top--><aside class="piece-context">C</aside><!--/lh:top--><div class="prose">' +
    page(byline + notice) +
    '</div><!--lh:end--><nav class="piece-pager">P</nav><!--/lh:end--></article>';
  const out = arrangePiece(html);
  assert.ok(!out.includes("<!--lh:"));
  assert.ok(out.indexOf('class="byline"') < out.indexOf("piece-context"));
  assert.ok(out.indexOf("piece-context") < out.indexOf("notice-correction"));
  assert.ok(out.indexOf("piece-pager") < out.indexOf("<hr>"));
  assert.ok(out.indexOf("<p>Text.</p>") < out.indexOf("piece-pager"));
});
