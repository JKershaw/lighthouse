// Build the offline shell after Eleventy has written the current site.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

export function scopePath(prefix = "/") {
  return `/${prefix.split("/").filter(Boolean).join("/")}${prefix.split("/").filter(Boolean).length ? "/" : ""}`;
}

function filesIn(dir, base = dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(dir, entry.name);
    return entry.isDirectory() ? filesIn(file, base) : [path.relative(base, file).split(path.sep).join("/")];
  }).sort();
}

export function writeOfflineFiles(output, prefix = "/", template) {
  const scope = scopePath(prefix);
  const files = filesIn(output);
  const assetFiles = files.filter((file) => file.startsWith("assets/") && !file.endsWith(".md"));
  // Every top-level section front, including sections added by future builds.
  const fronts = files.filter((file) => /^[^/]+\/index\.html$/.test(file));
  const pages = [...new Set(["index.html", "offline/index.html", ...fronts])];
  const url = (file) => scope + file.replace(/index\.html$/, "");
  const hash = createHash("sha256");
  for (const file of files.filter((f) => f.endsWith(".html") || assetFiles.includes(f))) {
    hash.update(file).update(fs.readFileSync(path.join(output, file)));
  }
  hash.update(template).update(scope);
  const version = hash.digest("hex").slice(0, 20);
  const config = { scope, version, pages: pages.map(url), assets: assetFiles.map(url) };
  fs.writeFileSync(path.join(output, "sw.js"), `const CONFIG = ${JSON.stringify(config)};\n${template}`);
  fs.writeFileSync(path.join(output, "manifest.webmanifest"), JSON.stringify({
    id: scope, name: "Lighthouse", short_name: "Lighthouse",
    description: "A standing watch on the computational world.",
    lang: "en-GB", start_url: scope, scope, display: "standalone",
    theme_color: "#fbfaf7", background_color: "#fbfaf7",
    icons: [192, 512].map((size) => ({ src: `${scope}assets/icons/icon-${size}.png`, sizes: `${size}x${size}`, type: "image/png", purpose: "any" })),
  }, null, 2) + "\n");
  return config;
}
