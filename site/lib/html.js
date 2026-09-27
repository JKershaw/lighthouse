// Rewrites of a rendered page's HTML that Markdown cannot express: notices,
// a piece's opening and date line, and the context the layout places around
// a piece's text.

// A blockquote whose first words are bold "Correction" or "Later evidence",
// as in `> **Later evidence, 27 September 2026.** ...`, is a notice.
const NOTICE = /<blockquote>\s*<p><strong>((?:Correction|Later evidence)\b[^<]*)<\/strong>([\s\S]*?)<\/blockquote>/g;

export function noticeKind(html) {
  const m = String(html).match(/^\s*<blockquote>\s*<p><strong>(Correction|Later evidence)\b/);
  return m ? (m[1] === "Correction" ? "correction" : "later-evidence") : "";
}

export function markNotices(html) {
  return html.replace(NOTICE, (all, lead, rest) => {
    const label = lead.startsWith("Correction") ? "Correction" : "Later evidence";
    const kind = label === "Correction" ? "correction" : "later-evidence";
    return `<aside class="notice notice-${kind}" aria-label="${label}">\n<p><strong>${lead}</strong>${rest}</aside>`;
  });
}

// The blocks after a piece's h1: one to three opening paragraphs, then the
// italic date line, with notices allowed before or after it.
const BLOCK = /^\s*(<p>(?:(?!<\/p>)[\s\S])*<\/p>|<aside class="notice[\s\S]*?<\/aside>)/;
const BYLINE = /^<p><em>([^<]*)<\/em><\/p>$/;

// Marks the opening and byline of a piece. Returns the new HTML and the
// offset just after the byline (or after the h1 when there is none).
export function arrangeOpening(html) {
  const h1End = html.indexOf("</h1>");
  if (h1End < 0) return { html, after: -1 };
  const start = h1End + "</h1>".length;
  let at = start;
  const parts = [];
  let openings = 0;
  let byline = null;
  for (let n = 0; n < 8 && !byline; n++) {
    const m = html.slice(at).match(BLOCK);
    if (!m) break;
    const block = m[1];
    const lead = m[0].slice(0, m[0].length - block.length);
    at += m[0].length;
    if (BYLINE.test(block)) {
      byline = block.replace(BYLINE, '<p class="byline"><em>$1</em></p>');
      parts.push(lead + byline);
    } else if (block.startsWith("<aside")) {
      parts.push(lead + block);
    } else if (!block.startsWith("<p><em>") && openings < 3) {
      openings++;
      parts.push(lead + block.replace(/^<p>/, '<p class="opening">'));
    } else break;
  }
  if (!byline || !openings) return { html, after: start };
  const rebuilt = parts.join("");
  return { html: html.slice(0, start) + rebuilt + html.slice(at), after: start + rebuilt.length };
}

// Pulls out a block the layout wrapped in <!--lh:name--> markers.
function takeMarked(html, name) {
  const re = new RegExp(`<!--lh:${name}-->([\\s\\S]*?)<!--/lh:${name}-->`);
  const m = html.match(re);
  if (!m) return { html, block: "", at: -1 };
  return { html: html.slice(0, m.index) + html.slice(m.index + m[0].length), block: m[1].trim(), at: m.index };
}

// A piece: notices, opening and byline, then the layout's context block
// placed after the byline and its pager before the colophon's rule.
export function arrangePiece(html) {
  html = markNotices(html);
  const top = takeMarked(html, "top");
  html = top.html;
  const end = takeMarked(html, "end");
  html = end.html;
  if (end.block) {
    const proseStart = html.indexOf('<div class="prose">');
    const rule = html.lastIndexOf("<hr>", end.at);
    const at = rule > proseStart && proseStart >= 0 ? rule : end.at;
    html = html.slice(0, at) + end.block + "\n" + html.slice(at);
  }
  const opened = arrangeOpening(html);
  html = opened.html;
  if (top.block) {
    const at = opened.after >= 0 ? opened.after : top.at;
    html = html.slice(0, at) + "\n" + top.block + html.slice(at);
  }
  return html;
}
