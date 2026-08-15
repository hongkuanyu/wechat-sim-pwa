const CACHE_NAME = 'wechat-sim-v2-cache-v1';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './offline.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// Fetch 策略：
// - 导航请求：优先网络，失败回退到缓存的 index.html 或 offline.html；
// - 静态资源：缓存优先，找不到再网络，网络成功时回写缓存。
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  // 导航请求（页面跳转/刷新）
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(response => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        return response;
      }).catch(() => caches.match('./index.html').then(r => r || caches.match('./offline.html')))
    );
    return;
  }

  // 其他资源：缓存优先
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        try {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        } catch (e) {}
        return response;
      }).catch(() => {
        // 网络失败且缓存没有，若是导航或重要资源可返回 offline.html
        return caches.match('./offline.html');
      });
    })
  );
});
/* 微信聊天模拟 v2 PWA - Service Worker (离线缓存)
 * 缓存策略：cache-first，首次访问后断网也能正常打开
 */
const CACHE_NAME = 'wechat_sim_v2_20260815';
// 只缓存 PWA 目录内同层级的核心资源（保证 scope=./ 下生效）
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.webmanifest'
];

// install：预缓存核心资源，完成后立即激活（跳过等待）
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS).catch(err => {
        // 某一个资源加载失败不要阻止 install（SRI 或不可达资源是预期）
        console.warn('[SW] cache.addAll 部分失败:', err);
        return cache.addAll(PRECACHE_URLS.filter(u => !u.includes('undefined')));
      }))
      .then(() => self.skipWaiting())
  );
});

// activate：清理旧版本缓存，立即接管客户端
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// fetch：导航请求 cache-first；其它资源先查缓存，失败回退 fetch，并把成功的请求放进缓存
self.addEventListener('fetch', event => {
  const req = event.request;
  // 只缓存 GET
  if (req.method !== 'GET') return;
  // 只对同源请求进行缓存（跨域CDN失败不影响）
  const url = new URL(req.url, self.location.href);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req).then(cached => {
      if (cached) return cached;
      return fetch(req).then(resp => {
        // 只缓存 2xx 成功的同源响应
        if (resp && resp.ok && resp.type === 'basic') {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, clone)).catch(()=>{});
        }
        return resp;
      }).catch(() => {
        // 断网下导航请求回退到 index.html
        if (req.mode === 'navigate') return caches.match('./index.html');
        return new Response('', { status: 504, statusText: 'Gateway Timeout' });
      });
    })
  );
});
