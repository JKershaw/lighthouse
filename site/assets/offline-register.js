// The script's URL keeps registration correct below a GitHub Pages prefix.
if ("serviceWorker" in navigator) {
  const root = new URL("../", document.currentScript.src);
  const savedWith = new WeakSet();
  const saveCurrentPage = () => {
    const worker = navigator.serviceWorker.controller;
    if (!worker || savedWith.has(worker)) return;
    savedWith.add(worker);
    worker.postMessage({ type: "SAVE_PAGE", url: location.href,
      assets: [...document.images].map((image) => image.currentSrc || image.src) });
  };
  // Re-save any illustrations loaded during an update's takeover as well.
  navigator.serviceWorker.addEventListener("controllerchange", saveCurrentPage);
  window.addEventListener("load", () => {
    navigator.serviceWorker.register(new URL("sw.js", root), {
      scope: root.pathname,
      updateViaCache: "none",
    }).then(() => navigator.serviceWorker.ready).then(() => {
      // The first visit finished before a worker controlled it. Save that
      // document and its illustrations too, without requiring a second visit.
      saveCurrentPage();
    }).catch(() => { /* Reading remains available if offline setup is refused. */ });
  });
}
