// Весела азбука — офлайн кеш (само за уеб версията; Android приложението носи файловете в себе си).
// Показва веднага кешираното копие и обновява кеша на заден план.
const C = "happy-alphabet-v1";
const FONTS = ["600","800","900"].flatMap(w => ["cyrillic","latin"].map(s => `fonts/rubik-${s}-${w}-normal.woff2`))
  .concat(["700","800","900"].flatMap(w => ["cyrillic","latin"].map(s => `fonts/nunito-${s}-${w}-normal.woff2`)));
const CORE = ["./", "index.html", "privacy.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"].concat(FONTS);

self.addEventListener("install", e => { e.waitUntil(caches.open(C).then(c => c.addAll(CORE))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== C).map(x => caches.delete(x)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  const key = req.mode === "navigate" ? "index.html" : req;
  const cacheP = caches.open(C);
  const update = cacheP.then(cache => fetch(req).then(r => (r && r.ok) ? cache.put(key, r.clone()).then(() => r) : r));
  e.waitUntil(update.catch(() => {}));
  e.respondWith(cacheP.then(cache => cache.match(key, { ignoreSearch: true })).then(hit => hit || update));
});
