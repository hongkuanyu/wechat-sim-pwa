/* 微信聊天模拟 PWA - Service Worker (离线缓存)
 * 策略：
 *   - 导航请求：网络优先，失败回退缓存，再失败回退 offline.html
 *   - 静态资源（CSS/JS/图标）：缓存优先，后台更新
 *   - 首次安装时预缓存所有核心资源
 */
const CACHE_NAME = 'wechat_sim_v3_20260815';
const OFFLINE_URL = './offline.html';

const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './offline.html',
  './favicon.png',
  './icons/icon-72x72.png',
  './icons/icon-96x96.png',
  './icons/icon-120x120.png',
  './icons/icon-128x128.png',
  './icons/icon-152x152.png',
  './icons/icon-180x180.png',
  './icons/icon-192x192.png',
  './icons/icon-192x192-maskable.png',
  './icons/icon-512x512.png',
  './icons/icon-512x512-maskable.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.allSettled(
        PRECACHE_URLS.map(url => cache.add(url))
      ))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url, self.location.href);
  if (url.origin !== self.location.origin) return;

  // 导航请求：网络优先 → 缓存 → offline.html
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then(resp => {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, clone)).catch(() => {});
          return resp;
        })
        .catch(() => caches.match(req))
        .then(cached => cached || caches.match('./index.html'))
        .catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // 静态资源：缓存优先，后台更新
  event.respondWith(
    caches.match(req).then(cached => {
      const fetchPromise = fetch(req).then(resp => {
        if (resp && resp.ok && resp.type === 'basic') {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, clone)).catch(() => {});
        }
        return resp;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});

// 接收来自页面的消息，触发立即更新
self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});
