// Eleventy builds the Lighthouse site from the repository's Markdown.
// Run from the repository root (the npm scripts do this): the input is the
// repository and the output is site/_site. Every Markdown file outside the
// ignored paths becomes a page at a URL mirroring its path; there is no list
// of pages to maintain.

import path from "node:path";
import { fileURLToPath } from "node:url";
import { HtmlBasePlugin } from "@11ty/eleventy";
import { scanRepo, pageUrl, IGNORED_DIRS, IGNORED_FILES } from "./lib/repo.js";
import { stripHeader } from "./lib/header.js";
import lighthousePlugin, { unresolved } from "./lib/markdown.js";

const siteDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(siteDir, "..");

let repo = null;
const getRepo = () => repo || (repo = scanRepo(root));
const relPath = (inputPath) => path.relative(root, path.resolve(inputPath)).split(path.sep).join("/");
const docFor = (data) => (data.page && data.page.inputPath ? getRepo().byPath[relPath(data.page.inputPath)] : null) || null;

export default function (eleventyConfig) {
  for (const dir of IGNORED_DIRS) eleventyConfig.ignores.add(`${dir}/**`);
  for (const file of IGNORED_FILES) eleventyConfig.ignores.add(file);
  eleventyConfig.ignores.add("**/node_modules/**");

  // Rescan at the start of every build, so serve mode sees new files.
  eleventyConfig.on("eleventy.before", () => {
    repo = scanRepo(root);
    unresolved.length = 0;
  });
  eleventyConfig.on("eleventy.after", () => {
    const seen = new Set();
    for (const { from, target } of unresolved) {
      const key = `${from} -> ${target}`;
      if (seen.has(key)) continue;
      seen.add(key);
      console.warn(`[lighthouse] link does not resolve, shown as text: ${key}`);
    }
  });

  // Images and illustrations beside the Markdown, and the site's own assets.
  for (const image of getRepo().images) eleventyConfig.addPassthroughCopy(image);
  eleventyConfig.addPassthroughCopy({ "site/assets": "assets" });

  // Markdown: no raw HTML (the records quote angle brackets as text), bare
  // URLs linked as GitHub does, and the repository-aware plugin.
  let md = null;
  eleventyConfig.amendLibrary("md", (lib) => {
    md = lib;
    lib.set({ html: false, linkify: true, typographer: false });
    lib.linkify.set({ fuzzyLink: false, fuzzyEmail: false });
    lib.use(lighthousePlugin, { getRepo });
  });

  // Study records and notes open with a header block; it is shown as metadata.
  eleventyConfig.addPreprocessor("lighthouse-header", "md", (data, content) => stripHeader(content));

  eleventyConfig.addGlobalData("repo", () => getRepo());
  eleventyConfig.addGlobalData("layout", "page.njk");
  eleventyConfig.addGlobalData("permalink", () => (data) => pageUrl(relPath(data.page.inputPath)));
  eleventyConfig.addGlobalData("eleventyComputed", {
    doc: (data) => docFor(data),
    pageTitle: (data) => {
      const doc = docFor(data);
      return (doc ? doc.listTitle : data.title) || "Lighthouse";
    },
    navSection: (data) => {
      const doc = docFor(data);
      return doc ? doc.section : data.section || "";
    },
  });

  eleventyConfig.addFilter("mdInline", (value, page) => (md ? md.renderInline(String(value || ""), { page }) : value));

  // README.md above its rule is the front page; below it, one section per h2.
  eleventyConfig.addFilter("homeParts", (html) => {
    const at = html.search(/<hr\s*\/?>/);
    let front = at >= 0 ? html.slice(0, at) : html;
    const rest = at >= 0 ? html.slice(at).replace(/^<hr\s*\/?>/, "") : "";
    front = front.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>\s*/, "");
    const sections = rest.split(/(?=<h2[\s>])/).filter((s) => s.trim());
    return { front, sections };
  });

  // Illustrations become figures with their italic captions, each linked to
  // its file so that a phone reader can open it at full size; tables scroll.
  const linked = (img) => {
    const src = (img.match(/\ssrc="([^"]+)"/) || [])[1];
    return src ? `<a class="figure-link" href="${src}">${img}</a>` : img;
  };
  eleventyConfig.addTransform("lighthouse-html", function (content) {
    if (!(this.page.outputPath || "").endsWith(".html")) return content;
    // In a piece, the paragraphs before the italic date line are its opening.
    if (/^\.?\/?articles\//.test(this.page.inputPath || "")) {
      content = content.replace(
        /(<\/h1>\s*)((?:<p>(?!<em>)[\s\S]*?<\/p>\s*){1,3})<p><em>([^<]*)<\/em><\/p>/,
        (all, h1, opening, byline) =>
          `${h1}${opening.replace(/<p>/g, '<p class="opening">')}<p class="byline"><em>${byline}</em></p>`,
      );
    }
    return content
      .replace(/<p>(<img [^>]*>)<\/p>(\s*<p><em>((?:(?!<\/p>)[\s\S])*?)<\/em><\/p>)?/g, (all, img, capBlock, caption) => {
        if (caption !== undefined && !caption.includes("</em>")) {
          return `<figure>${linked(img)}<figcaption>${caption}</figcaption></figure>`;
        }
        return `<figure>${linked(img)}</figure>${capBlock || ""}`;
      })
      .replace(/<table>([\s\S]*?)<\/table>/g, (all, inner) => {
        // A table of six or more columns may use more of a wide screen.
        const firstRow = (inner.match(/<tr>([\s\S]*?)<\/tr>/) || ["", ""])[1];
        const columns = (firstRow.match(/<t[hd][\s>]/g) || []).length;
        return `<div class="table-scroll${columns >= 6 ? " table-wide" : ""}"><table>${inner}</table></div>`;
      });
  });

  // Section indexes and study pages, built from the scan rather than listed.
  const indexes = [
    ["articles", { permalink: "/articles/", title: "Pieces", section: "articles" }],
    ["short", { permalink: "/articles/short/", title: "Short forms", section: "articles" }],
    ["studies", { permalink: "/studies/", title: "Studies", section: "studies" }],
    ["notes", { permalink: "/notes/", title: "Notes", section: "notes" }],
    ["notfound", { permalink: "/404.html", title: "Not found", section: "" }],
  ];
  for (const [name, data] of indexes) {
    eleventyConfig.addTemplate(`_lighthouse/${name}.njk`, "", { ...data, layout: `index-${name}.njk` });
  }
  eleventyConfig.addTemplate("_lighthouse/study.njk", "", {
    layout: "index-study.njk",
    section: "studies",
    pagination: { data: "repo.studies", size: 1, alias: "study" },
    eleventyComputed: { title: (data) => (data.study ? `${data.study.id}: ${data.study.lead.title}` : "Study") },
    permalink: (data) => `/studies/${data.study.id}/`,
  });

  eleventyConfig.addPlugin(HtmlBasePlugin);

  return {
    dir: {
      input: ".",
      output: "site/_site",
      includes: "site/_includes",
      data: "site/_data",
    },
    templateFormats: ["md", "njk"],
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
    // GitHub Pages without a custom domain serves the site under /<repository>/.
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
}
