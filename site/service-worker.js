/* CONFIG is inserted by the build. No requests leave this site's scope. */
const ROOT = new URL(CONFIG.scope, self.location.origin);
const PREFIX = `lighthouse:${ROOT.pathname}:`;
const ASSETS = `${PREFIX}assets:${CONFIG.version}`;
// Visited pages survive a new build; online navigation always reads the network.
const PAGES = `${PREFIX}pages`;
const ownURL = (value) => {
  const url = new URL(value, ROOT);
  return url.origin === ROOT.origin && url.pathname.startsWith(ROOT.pathname);
};

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    // Fetch the whole shell before storing any page. An incomplete new build
    // must not replace a working installation.
    const fetchAll = async (urls) => Promise.all(urls.map(async (url) => {
      const response = await fetch(new Request(url, { cache: "reload" }));
      if (!response.ok) throw new Error(`Offline shell unavailable: ${url}`);
      return [url, response];
    }));
    const [assets, pages] = await Promise.all([fetchAll(CONFIG.assets), fetchAll(CONFIG.pages)]);
    const assetCache = await caches.open(ASSETS);
    const pageCache = await caches.open(PAGES);
    await Promise.all(assets.map(([url, response]) => assetCache.put(url, response)));
    // Keep illustrations from earlier reading sessions. Refresh them for this
    // build when possible, retaining the saved copy if its source disappeared.
    const shellAssets = new Set(CONFIG.assets.map((url) => new URL(url, ROOT).href));
    for (const name of (await caches.keys()).filter((key) => key.startsWith(`${PREFIX}assets:`) && key !== ASSETS)) {
      const previous = await caches.open(name);
      for (const request of await previous.keys()) {
        if (shellAssets.has(request.url)) continue;
        let response;
        try { response = await fetch(request, { cache: "reload" }); } catch { /* Use the saved copy. */ }
        if (!response?.ok) response = await previous.match(request);
        if (response) await remember(ASSETS, request, response, 120);
      }
    }
    await Promise.all(pages.map(([url, response]) => pageCache.put(url, response)));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    await Promise.all((await caches.keys())
      .filter((key) => key.startsWith(PREFIX) && key !== ASSETS && key !== PAGES)
      .map((key) => caches.delete(key)));
    await self.clients.claim();
  })());
});

async function remember(cacheName, request, response, limit) {
  if (!response.ok || response.type === "opaque") return;
  const cache = await caches.open(cacheName);
  await cache.put(request, response);
  const keys = await cache.keys();
  // The shell stays available even after a long reading session.
  const protectedURLs = new Set([...CONFIG.pages, ...CONFIG.assets].map((url) => new URL(url, ROOT).href));
  const removable = keys.filter((key) => !protectedURLs.has(key.url));
  for (const key of removable.slice(0, Math.max(0, keys.length - limit))) await cache.delete(key);
}

self.addEventListener("message", (event) => {
  if (event.data?.type !== "SAVE_PAGE" || !ownURL(event.data.url)) return;
  event.waitUntil((async () => {
    try {
      const url = new URL(event.data.url); url.hash = "";
      const response = await fetch(url, { cache: "no-store" });
      await remember(PAGES, url.href, response, 80);
      await Promise.all((event.data.assets || []).filter(ownURL).map(async (asset) => {
        try { await remember(ASSETS, asset, await fetch(asset), 120); } catch { /* Available on a later visit. */ }
      }));
    } catch { /* Do not disturb reading if the connection disappears. */ }
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET" || request.headers.has("range") || !ownURL(request.url)) return;
  if (request.mode === "navigate") {
    event.respondWith((async () => {
      try {
        // Bypass HTTP caches too: an online reader gets the current account,
        // including server error pages rather than a cached success.
        const response = await fetch(request, { cache: "no-store" });
        event.waitUntil(remember(PAGES, request, response.clone(), 80));
        return response;
      } catch {
        const cache = await caches.open(PAGES);
        return (await cache.match(request)) || (await cache.match(new URL("offline/", ROOT).href));
      }
    })());
  } else if (/\.(?:css|js|woff2?|ttf|svg|png|jpe?g|webp|ico)$/.test(new URL(request.url).pathname)) {
    event.respondWith((async () => {
      const cache = await caches.open(ASSETS);
      const cached = await cache.match(request);
      if (cached) return cached;
      const response = await fetch(request);
      event.waitUntil(remember(ASSETS, request, response.clone(), 120));
      return response;
    })());
  }
});
