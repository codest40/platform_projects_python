// Service Worker for Timzap
// Provides offline functionality and caching

const CACHE_NAME = 'timzap-v1.0.0';
const STATIC_CACHE = 'timzap-static-v1.0.0';
const DYNAMIC_CACHE = 'timzap-dynamic-v1.0.0';

// Files to cache for offline functionality
const STATIC_FILES = [
  '/',
  '/index.html',
  '/html/calendar.html',
  '/css/theme.css',
  '/css/styles.css',
  '/css/calendar.css',
  '/js/main.js',
  '/js/time.js',
  '/js/search.js',
  '/js/timezoneSelector.js',
  '/js/theme.js',
  '/js/clock.js',
  '/js/reminderManager.js',
  '/js/reminderSortView.js',
  '/js/calendarRender.js',
  '/js/calendarNavigation.js',
  '/js/paginate.js',
  '/json/time_list.json',
  'https://cdn.jsdelivr.net/npm/luxon@3.4.4/build/global/luxon.min.js'
];

// Install event - cache static files
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker: Error caching static files:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve cached files or fetch from network
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Only handle HTTP/HTTPS requests
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Handle different types of requests
  if (STATIC_FILES.includes(url.pathname) || url.pathname === '/') {
    // Static files - cache first strategy
    event.respondWith(cacheFirst(request));
  } else if (url.hostname === 'cdn.jsdelivr.net') {
    // CDN resources - cache first strategy
    event.respondWith(cacheFirst(request));
  } else {
    // Dynamic content - network first strategy
    event.respondWith(networkFirst(request));
  }
});

// Cache first strategy - for static files
async function cacheFirst(request) {
  try {
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    
    const response = await fetch(request);
    
    if (response.status === 200) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.error('Cache first strategy failed:', error);
    
    // Return offline page if available
    if (request.destination === 'document') {
      const offlineResponse = await caches.match('/index.html');
      return offlineResponse || new Response('Offline - Please check your connection', {
        status: 503,
        statusText: 'Service Unavailable'
      });
    }
    
    return new Response('Network error', {
      status: 408,
      statusText: 'Request Timeout'
    });
  }
}

// Network first strategy - for dynamic content
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    
    if (response.status === 200) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('Network request failed, trying cache:', request.url);
    
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    
    // Return a meaningful offline response
    return new Response(JSON.stringify({
      error: 'Network unavailable',
      message: 'This feature requires an internet connection'
    }), {
      status: 503,
      statusText: 'Service Unavailable',
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}

// Background sync for reminder updates (when supported)
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync triggered:', event.tag);
  
  if (event.tag === 'reminder-sync') {
    event.waitUntil(syncReminders());
  }
});

// Sync reminders in the background
async function syncReminders() {
  try {
    // Get pending reminders from IndexedDB (if implemented)
    // Send them to server when connection is restored
    console.log('Service Worker: Syncing reminders...');
    
    // This would integrate with a backend API
    // For now, just log the sync attempt
    
    return Promise.resolve();
  } catch (error) {
    console.error('Service Worker: Reminder sync failed:', error);
    throw error;
  }
}

// Push notification handling (for future reminder notifications)
self.addEventListener('push', event => {
  console.log('Service Worker: Push message received');
  
  const options = {
    body: 'You have a reminder!',
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'view',
        title: 'View Reminder',
        icon: '/favicon.ico'
      },
      {
        action: 'close',
        title: 'Dismiss',
        icon: '/favicon.ico'
      }
    ]
  };
  
  let promiseChain;
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.title = data.title || 'Timzap Reminder';
  }
  
  promiseChain = self.registration.showNotification('Timzap', options);
  
  event.waitUntil(promiseChain);
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();
  
  let promiseChain;
  
  if (event.action === 'view') {
    promiseChain = clients.openWindow('/html/calendar.html');
  } else if (event.action === 'close') {
    // Just close the notification
    promiseChain = Promise.resolve();
  } else {
    // Default action - open the app
    promiseChain = clients.openWindow('/');
  }
  
  event.waitUntil(promiseChain);
});

// Message handling for communication with main thread
self.addEventListener('message', event => {
  console.log('Service Worker: Message received:', event.data);
  
  if (event.data && event.data.type) {
    switch (event.data.type) {
      case 'CACHE_UPDATE':
        handleCacheUpdate(event.data.payload);
        break;
      case 'CLEAR_CACHE':
        handleClearCache();
        break;
      case 'GET_CACHE_SIZE':
        handleGetCacheSize().then(size => {
          event.ports[0].postMessage({ size });
        });
        break;
      default:
        console.log('Service Worker: Unknown message type:', event.data.type);
    }
  }
});

// Handle cache update requests
async function handleCacheUpdate(payload) {
  try {
    const cache = await caches.open(DYNAMIC_CACHE);
    if (payload.url && payload.data) {
      const response = new Response(JSON.stringify(payload.data), {
        headers: { 'Content-Type': 'application/json' }
      });
      await cache.put(payload.url, response);
      console.log('Service Worker: Cache updated for:', payload.url);
    }
  } catch (error) {
    console.error('Service Worker: Cache update failed:', error);
  }
}

// Handle cache clearing
async function handleClearCache() {
  try {
    await caches.delete(DYNAMIC_CACHE);
    console.log('Service Worker: Dynamic cache cleared');
  } catch (error) {
    console.error('Service Worker: Cache clear failed:', error);
  }
}

// Get cache size information
async function handleGetCacheSize() {
  try {
    const cacheNames = await caches.keys();
    let totalSize = 0;
    
    for (const cacheName of cacheNames) {
      const cache = await caches.open(cacheName);
      const requests = await cache.keys();
      
      for (const request of requests) {
        const response = await cache.match(request);
        if (response) {
          const blob = await response.blob();
          totalSize += blob.size;
        }
      }
    }
    
    return {
      totalSize,
      cacheCount: cacheNames.length,
      caches: cacheNames
    };
  } catch (error) {
    console.error('Service Worker: Error calculating cache size:', error);
    return { totalSize: 0, cacheCount: 0, caches: [] };
  }
}

// Error handling
self.addEventListener('error', event => {
  console.error('Service Worker: Error occurred:', event.error);
});

self.addEventListener('unhandledrejection', event => {
  console.error('Service Worker: Unhandled promise rejection:', event.reason);
});

// Periodic background sync (when supported)
self.addEventListener('periodicsync', event => {
  console.log('Service Worker: Periodic sync triggered:', event.tag);
  
  if (event.tag === 'reminder-check') {
    event.waitUntil(checkUpcomingReminders());
  }
});

// Check for upcoming reminders
async function checkUpcomingReminders() {
  try {
    // This would check for reminders that are due soon
    // and potentially show notifications
    console.log('Service Worker: Checking upcoming reminders...');
    
    // Implementation would depend on how reminders are stored
    // For localStorage-based reminders, we'd need to communicate with the main thread
    
    return Promise.resolve();
  } catch (error) {
    console.error('Service Worker: Reminder check failed:', error);
    throw error;
  }
}

// Network status change handling
self.addEventListener('online', event => {
  console.log('Service Worker: Network is online');
  // Could trigger sync operations here
});

self.addEventListener('offline', event => {
  console.log('Service Worker: Network is offline');
  // Could queue operations for later sync here
});

console.log('Service Worker: Script loaded successfully');