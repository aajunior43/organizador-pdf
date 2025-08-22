const CACHE_NAME = 'pdf-organizer-v3.0.0';
const STATIC_CACHE = 'pdf-organizer-static-v3.0.0';
const DYNAMIC_CACHE = 'pdf-organizer-dynamic-v3.0.0';

// Files to cache immediately
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  // Add other critical static assets
];

// API endpoints to cache
const API_CACHE_PATTERNS = [
  /\/api\/users\/me$/,
  /\/api\/pdf\/projects\//,
  /\/api\/users\/stats$/,
];

// Install event - cache static files
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('[SW] Static files cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Error caching static files:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Service worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Handle different types of requests
  if (url.origin === location.origin) {
    // Same origin requests
    if (url.pathname.startsWith('/api/')) {
      // API requests
      event.respondWith(handleApiRequest(request));
    } else {
      // Static files and pages
      event.respondWith(handleStaticRequest(request));
    }
  } else {
    // External requests (CDN, etc.)
    event.respondWith(handleExternalRequest(request));
  }
});

// Handle API requests with cache-first strategy for specific endpoints
async function handleApiRequest(request) {
  const url = new URL(request.url);
  const shouldCache = API_CACHE_PATTERNS.some(pattern => pattern.test(url.pathname));
  
  if (shouldCache) {
    try {
      // Try cache first
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        console.log('[SW] Serving API from cache:', url.pathname);
        
        // Update cache in background
        fetch(request)
          .then(response => {
            if (response.ok) {
              const responseClone = response.clone();
              caches.open(DYNAMIC_CACHE)
                .then(cache => cache.put(request, responseClone));
            }
          })
          .catch(() => {}); // Ignore background update errors
        
        return cachedResponse;
      }
      
      // Fetch from network and cache
      const response = await fetch(request);
      if (response.ok) {
        const responseClone = response.clone();
        const cache = await caches.open(DYNAMIC_CACHE);
        await cache.put(request, responseClone);
        console.log('[SW] API response cached:', url.pathname);
      }
      return response;
    } catch (error) {
      console.error('[SW] API request failed:', error);
      
      // Return cached version if available
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        return cachedResponse;
      }
      
      // Return offline response
      return new Response(
        JSON.stringify({ 
          error: 'Offline', 
          message: 'Você está offline. Algumas funcionalidades podem não estar disponíveis.' 
        }),
        {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  }
  
  // For non-cached API requests, just fetch
  return fetch(request);
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
  try {
    // Try cache first
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      console.log('[SW] Serving static from cache:', request.url);
      return cachedResponse;
    }
    
    // Fetch from network
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.ok) {
      const responseClone = response.clone();
      const cache = await caches.open(DYNAMIC_CACHE);
      await cache.put(request, responseClone);
      console.log('[SW] Static file cached:', request.url);
    }
    
    return response;
  } catch (error) {
    console.error('[SW] Static request failed:', error);
    
    // Try to serve from cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // For navigation requests, serve the app shell
    if (request.mode === 'navigate') {
      const appShell = await caches.match('/index.html');
      if (appShell) {
        return appShell;
      }
    }
    
    // Return offline page
    return new Response(
      `<!DOCTYPE html>
      <html>
      <head>
        <title>PDF Organizer - Offline</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
          .offline { color: #666; }
          .icon { font-size: 64px; margin-bottom: 20px; }
        </style>
      </head>
      <body>
        <div class="icon">📄</div>
        <h1>PDF Organizer</h1>
        <p class="offline">Você está offline. Verifique sua conexão com a internet.</p>
        <button onclick="window.location.reload()">Tentar Novamente</button>
      </body>
      </html>`,
      {
        status: 200,
        headers: { 'Content-Type': 'text/html' }
      }
    );
  }
}

// Handle external requests with network-first strategy
async function handleExternalRequest(request) {
  try {
    const response = await fetch(request);
    
    // Cache successful responses from CDNs
    if (response.ok && (request.url.includes('cdn') || request.url.includes('fonts'))) {
      const responseClone = response.clone();
      const cache = await caches.open(DYNAMIC_CACHE);
      await cache.put(request, responseClone);
    }
    
    return response;
  } catch (error) {
    // Try to serve from cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    throw error;
  }
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync triggered:', event.tag);
  
  if (event.tag === 'pdf-upload') {
    event.waitUntil(syncPendingUploads());
  } else if (event.tag === 'pdf-operations') {
    event.waitUntil(syncPendingOperations());
  }
});

// Sync pending uploads when back online
async function syncPendingUploads() {
  try {
    // Get pending uploads from IndexedDB
    const pendingUploads = await getPendingUploads();
    
    for (const upload of pendingUploads) {
      try {
        await fetch('/api/pdf/projects/' + upload.projectId + '/upload', {
          method: 'POST',
          body: upload.formData,
          headers: upload.headers
        });
        
        // Remove from pending uploads
        await removePendingUpload(upload.id);
        
        // Notify user
        self.registration.showNotification('Upload Concluído', {
          body: `Arquivo ${upload.filename} foi enviado com sucesso!`,
          icon: '/icons/icon-192x192.png',
          badge: '/icons/badge-72x72.png',
          tag: 'upload-success'
        });
      } catch (error) {
        console.error('[SW] Failed to sync upload:', error);
      }
    }
  } catch (error) {
    console.error('[SW] Error syncing uploads:', error);
  }
}

// Sync pending operations when back online
async function syncPendingOperations() {
  try {
    // Get pending operations from IndexedDB
    const pendingOps = await getPendingOperations();
    
    for (const operation of pendingOps) {
      try {
        await fetch(operation.url, {
          method: operation.method,
          body: operation.body,
          headers: operation.headers
        });
        
        // Remove from pending operations
        await removePendingOperation(operation.id);
        
        // Notify user
        self.registration.showNotification('Operação Concluída', {
          body: `${operation.type} foi processado com sucesso!`,
          icon: '/icons/icon-192x192.png',
          badge: '/icons/badge-72x72.png',
          tag: 'operation-success'
        });
      } catch (error) {
        console.error('[SW] Failed to sync operation:', error);
      }
    }
  } catch (error) {
    console.error('[SW] Error syncing operations:', error);
  }
}

// Push notification handler
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received');
  
  let data = {};
  if (event.data) {
    data = event.data.json();
  }
  
  const options = {
    body: data.body || 'Nova notificação do PDF Organizer',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: data.data || {},
    actions: [
      {
        action: 'view',
        title: 'Ver',
        icon: '/icons/action-view.png'
      },
      {
        action: 'dismiss',
        title: 'Dispensar',
        icon: '/icons/action-dismiss.png'
      }
    ],
    tag: data.tag || 'general',
    requireInteraction: data.requireInteraction || false
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'PDF Organizer', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'view') {
    // Open the app
    event.waitUntil(
      clients.openWindow(event.notification.data.url || '/')
    );
  } else if (event.action === 'dismiss') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper functions for IndexedDB operations
// (These would need to be implemented based on your offline storage strategy)
async function getPendingUploads() {
  // Implementation for getting pending uploads from IndexedDB
  return [];
}

async function removePendingUpload(id) {
  // Implementation for removing upload from IndexedDB
}

async function getPendingOperations() {
  // Implementation for getting pending operations from IndexedDB
  return [];
}

async function removePendingOperation(id) {
  // Implementation for removing operation from IndexedDB
}

console.log('[SW] Service worker loaded successfully');