// Nunjucks looks a filter up only when the branch using it renders, so a
// template can name a filter that no longer exists and still build until that
// branch is reached. Every filter the layouts use must be registered.
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const BUILT_IN = new Set(["capitalize", "dump", "first", "join", "last", "length", "lower", "replace", "safe", "string", "title", "trim", "upper", "url", "urlencode", "default", "escape", "sort", "reverse", "int", "float"]);

test("every filter a layout uses is built in or registered in eleventy.config.js", () => {
  const config = fs.readFileSync(path.join(site, "eleventy.config.js"), "utf8");
  const registered = new Set([...config.matchAll(/addFilter\(\s*"([A-Za-z_]\w*)"/g)].map((m) => m[1]));
  const dir = path.join(site, "_includes");
  const missing = [];
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".njk"))) {
    const text = fs.readFileSync(path.join(dir, file), "utf8");
    for (const tag of text.matchAll(/\{\{[\s\S]*?\}\}|\{%[\s\S]*?%\}/g)) {
      for (const use of tag[0].matchAll(/\|\s*([A-Za-z_]\w*)/g)) {
        if (!BUILT_IN.has(use[1]) && !registered.has(use[1])) missing.push(`${file}: ${use[1]}`);
      }
    }
  }
  assert.deepEqual(missing, []);
});
