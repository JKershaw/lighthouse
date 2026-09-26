// A markdown-it plugin that makes the repository's Markdown work as a site:
// GitHub-style heading ids, relative links rewritten to page URLs, relative
// images pointed at their copies, and bare repository paths in the text of
// records (studies/LH004/, notes/R-0001.md) linked to their pages.

import path from "node:path";
import fs from "node:fs";
import { IMAGE_EXT, sourceUrl } from "./repo.js";
import { KEY_LINE } from "./header.js";

// The same slugs GitHub gives headings, so anchors written for GitHub work.
export function slugify(text) {
  return String(text)
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{M}\p{N}\p{Pc} -]/gu, "")
    .replace(/ /g, "-");
}

const EXTERNAL = /^([a-z][a-z0-9+.-]*:|\/\/)/i;
const BARE_PATH =
  /(?<![\w/.@:#%-])((?:[A-Za-z0-9_][A-Za-z0-9_.-]*\/)*(?:[A-Za-z0-9_][A-Za-z0-9_.-]*\.md|[A-Za-z0-9_][A-Za-z0-9_.-]*\/))(?![\w/-])/g;

export const unresolved = [];

function currentPath(env, root) {
  const input = env && env.page && env.page.inputPath;
  if (!input) return "README.md";
  const abs = path.resolve(input);
  return path.relative(root, abs).split(path.sep).join("/");
}

// Resolve a link target written in `from` to what the site serves.
// Returns { href } or { missing: true }.
export function resolveTarget(repo, from, target, { image = false } = {}) {
  if (!target || EXTERNAL.test(target) || target.startsWith("#")) return { href: target };
  const hashAt = target.search(/[?#]/);
  const rawPath = hashAt >= 0 ? target.slice(0, hashAt) : target;
  const suffix = hashAt >= 0 ? target.slice(hashAt) : "";
  let decoded;
  try {
    decoded = decodeURIComponent(rawPath);
  } catch {
    decoded = rawPath;
  }
  const base = decoded.startsWith("/") ? "" : path.posix.dirname(from);
  const joined = path.posix.normalize(path.posix.join(base === "." ? "" : base, decoded.replace(/^\/+/, "")));
  if (joined.startsWith("..") || path.posix.isAbsolute(joined)) return { missing: true };
  const rel = joined === "." ? "" : joined.replace(/\/$/, "");
  const wantsDir = decoded.endsWith("/") || rel === "";

  const page = repo.byPath[rel];
  if (page && !wantsDir) return { href: page.url + suffix };
  if (!wantsDir && IMAGE_EXT.includes(path.posix.extname(rel).toLowerCase()) && repo.fileSet.has(rel)) {
    return { href: "/" + rel + suffix };
  }
  if (image) return { missing: true };
  if (rel === "") return { href: "/" + suffix };
  if (repo.siteDirs.has(rel)) return { href: `/${rel}/` + suffix };
  // A file or folder that exists but is not part of the site goes to GitHub.
  const abs = path.join(repo.root, rel);
  if (fs.existsSync(abs)) {
    return { href: sourceUrl(rel, fs.statSync(abs).isDirectory()) + suffix };
  }
  return { missing: true };
}

// A bare path in running text: tried beside the current file, then at the root.
function resolveBare(repo, from, text) {
  const here = path.posix.dirname(from);
  const candidates = [here === "." ? text : `${here}/${text}`, text];
  for (const cand of candidates) {
    const norm = path.posix.normalize(cand);
    if (norm.endsWith("/")) {
      const dir = norm.replace(/\/$/, "");
      if (repo.siteDirs.has(dir)) return `/${dir}/`;
    } else if (repo.byPath[norm] && norm !== from) {
      return repo.byPath[norm].url;
    }
  }
  return null;
}

// Blocks of `key: value` lines led by `title:` inside a body (the records'
// question-register entries) are set like the header block, not run on.
function fieldsBlock(md) {
  md.block.ruler.before("paragraph", "lighthouse_fields", (state, startLine, endLine, silent) => {
    if (state.sCount[startLine] - state.blkIndent >= 4) return false;
    const lineText = (n) => state.src.slice(state.bMarks[n] + state.tShift[n], state.eMarks[n]);
    const first = lineText(startLine).match(KEY_LINE);
    if (!first || first[1].trim().toLowerCase() !== "title") return false;
    const fields = [];
    let next = startLine;
    for (; next < endLine && !state.isEmpty(next) && state.sCount[next] >= state.blkIndent; next++) {
      const text = lineText(next);
      const key = text.match(KEY_LINE);
      const item = text.match(/^[-*]\s+(.*)$/);
      if (key) fields.push({ key: key[1].trim(), value: (key[2] || "").trim(), items: [] });
      else if (item && fields.length) fields[fields.length - 1].items.push(item[1].trim());
      else return false;
    }
    if (fields.length < 2) return false;
    if (silent) return true;
    const token = state.push("lighthouse_fields", "dl", 0);
    token.block = true;
    token.map = [startLine, next];
    token.meta = { fields };
    state.line = next;
    return true;
  });
  md.renderer.rules.lighthouse_fields = (tokens, idx, options, env) => {
    const esc = md.utils.escapeHtml;
    const rows = tokens[idx].meta.fields.map((f) => {
      const items = f.items.length ? `<ul>${f.items.map((i) => `<li>${md.renderInline(i, env)}</li>`).join("")}</ul>` : "";
      return `<div><dt>${esc(f.key.replace(/_/g, " "))}</dt><dd>${f.value ? md.renderInline(f.value, env) : ""}${items}</dd></div>`;
    });
    return `<dl class="meta fields">\n${rows.join("\n")}\n</dl>\n`;
  };
}

export default function lighthousePlugin(md, { getRepo }) {
  fieldsBlock(md);
  md.core.ruler.push("lighthouse", (state) => {
    const repo = getRepo();
    if (!repo) return;
    const from = currentPath(state.env, repo.root);
    const seen = new Map();

    for (let i = 0; i < state.tokens.length; i++) {
      const token = state.tokens[i];

      if (token.type === "heading_open" && !token.attrGet("id")) {
        const inline = state.tokens[i + 1];
        const text = (inline.children || [])
          .filter((c) => c.type === "text" || c.type === "code_inline")
          .map((c) => c.content)
          .join("");
        let slug = slugify(text);
        const count = seen.get(slug) || 0;
        seen.set(slug, count + 1);
        if (count) slug = `${slug}-${count}`;
        if (slug) token.attrSet("id", slug);
      }

      if (token.type !== "inline" || !token.children) continue;
      const out = [];
      const openLinks = [];
      for (const child of token.children) {
        if (child.type === "link_open") {
          openLinks.push(child);
          const href = child.attrGet("href");
          const result = resolveTarget(repo, from, href);
          if (result.missing) {
            unresolved.push({ from, target: href });
            child.tag = "span";
            child.attrs = [["class", "unresolved"], ["title", `Link in the source does not resolve: ${href}`]];
            child.markup = "unresolved";
          } else if (result.href !== href) {
            child.attrSet("href", result.href);
          }
        } else if (child.type === "link_close") {
          const opener = openLinks.pop();
          if (opener && opener.markup === "unresolved") child.tag = "span";
        } else if (child.type === "image") {
          const src = child.attrGet("src");
          const result = resolveTarget(repo, from, src, { image: true });
          if (result.missing) unresolved.push({ from, target: src });
          else if (result.href !== src) child.attrSet("src", result.href);
        } else if (child.type === "text" && !openLinks.length && /\.md|\//.test(child.content)) {
          const parts = [];
          let last = 0;
          const text = child.content;
          for (const m of text.matchAll(BARE_PATH)) {
            const href = resolveBare(repo, from, m[1]);
            if (!href) continue;
            if (m.index > last) parts.push(["text", text.slice(last, m.index)]);
            parts.push(["link", m[1], href]);
            last = m.index + m[1].length;
          }
          if (parts.length) {
            if (last < text.length) parts.push(["text", text.slice(last)]);
            for (const part of parts) {
              if (part[0] === "text") {
                const t = new state.Token("text", "", 0);
                t.content = part[1];
                out.push(t);
              } else {
                const open = new state.Token("link_open", "a", 1);
                open.attrs = [["href", part[2]]];
                open.markup = "autopath";
                const t = new state.Token("text", "", 0);
                t.content = part[1];
                const close = new state.Token("link_close", "a", -1);
                close.markup = "autopath";
                out.push(open, t, close);
              }
            }
            continue;
          }
        }
        out.push(child);
      }
      token.children = out;
    }
  });
}
