// Analytics and metrics service
interface AnalyticsEvent {
  name: string;
  properties?: Record<string, any>;
  timestamp?: number;
  userId?: string;
  sessionId?: string;
}

interface UserMetrics {
  userId: string;
  sessionId: string;
  pageViews: number;
  timeSpent: number;
  actionsPerformed: number;
  lastActivity: number;
  userAgent: string;
  screenResolution: string;
  language: string;
}

class AnalyticsService {
  private apiUrl: string;
  private userId: string | null = null;
  private sessionId: string;
  private metrics: UserMetrics;
  private eventQueue: AnalyticsEvent[] = [];
  private isOnline: boolean = navigator.onLine;
  private flushInterval: number = 30000; // 30 seconds
  private maxQueueSize: number = 100;

  constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    this.sessionId = this.generateSessionId();
    this.metrics = this.initializeMetrics();
    
    this.setupEventListeners();
    this.startPeriodicFlush();
    this.trackPageView();
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private initializeMetrics(): UserMetrics {
    return {
      userId: this.userId || 'anonymous',
      sessionId: this.sessionId,
      pageViews: 0,
      timeSpent: 0,
      actionsPerformed: 0,
      lastActivity: Date.now(),
      userAgent: navigator.userAgent,
      screenResolution: `${screen.width}x${screen.height}`,
      language: navigator.language,
    };
  }

  private setupEventListeners(): void {
    // Track online/offline status
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.flushEvents();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });

    // Track page visibility changes
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.track('page_hidden');
        this.flushEvents();
      } else {
        this.track('page_visible');
      }
    });

    // Track user activity
    ['click', 'scroll', 'keypress', 'mousemove'].forEach(event => {
      document.addEventListener(event, this.throttle(() => {
        this.updateLastActivity();
      }, 1000));
    });

    // Track page unload
    window.addEventListener('beforeunload', () => {
      this.track('page_unload');
      this.flushEvents(true); // Force immediate flush
    });

    // Track errors
    window.addEventListener('error', (event) => {
      this.track('javascript_error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        stack: event.error?.stack,
      });
    });

    // Track unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      this.track('unhandled_promise_rejection', {
        reason: event.reason?.toString(),
        stack: event.reason?.stack,
      });
    });
  }

  private startPeriodicFlush(): void {
    setInterval(() => {
      this.flushEvents();
    }, this.flushInterval);
  }

  private updateLastActivity(): void {
    this.metrics.lastActivity = Date.now();
    this.metrics.actionsPerformed++;
  }

  private throttle(func: Function, limit: number): Function {
    let inThrottle: boolean;
    return function(this: any, ...args: any[]) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  // Public methods
  setUserId(userId: string): void {
    this.userId = userId;
    this.metrics.userId = userId;
    this.track('user_identified', { userId });
  }

  track(eventName: string, properties?: Record<string, any>): void {
    const event: AnalyticsEvent = {
      name: eventName,
      properties: {
        ...properties,
        sessionId: this.sessionId,
        timestamp: Date.now(),
        url: window.location.href,
        referrer: document.referrer,
        userAgent: navigator.userAgent,
      },
      timestamp: Date.now(),
      userId: this.userId || undefined,
      sessionId: this.sessionId,
    };

    this.eventQueue.push(event);

    // Flush immediately if queue is full
    if (this.eventQueue.length >= this.maxQueueSize) {
      this.flushEvents();
    }

    // Store in localStorage as backup
    this.storeEventLocally(event);
  }

  trackPageView(page?: string): void {
    this.metrics.pageViews++;
    this.track('page_view', {
      page: page || window.location.pathname,
      title: document.title,
      referrer: document.referrer,
    });
  }

  trackUserAction(action: string, target?: string, properties?: Record<string, any>): void {
    this.track('user_action', {
      action,
      target,
      ...properties,
    });
  }

  trackPerformance(): void {
    if ('performance' in window) {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      const paint = performance.getEntriesByType('paint');
      
      this.track('performance_metrics', {
        loadTime: navigation.loadEventEnd - navigation.loadEventStart,
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime,
        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
        connectionType: (navigator as any).connection?.effectiveType,
      });
    }
  }

  trackError(error: Error, context?: string): void {
    this.track('application_error', {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now(),
    });
  }

  trackFeatureUsage(feature: string, properties?: Record<string, any>): void {
    this.track('feature_usage', {
      feature,
      ...properties,
    });
  }

  trackConversion(goal: string, value?: number, properties?: Record<string, any>): void {
    this.track('conversion', {
      goal,
      value,
      ...properties,
    });
  }

  private async flushEvents(immediate: boolean = false): Promise<void> {
    if (this.eventQueue.length === 0) return;

    const eventsToSend = [...this.eventQueue];
    this.eventQueue = [];

    if (!this.isOnline && !immediate) {
      // Store events locally if offline
      eventsToSend.forEach(event => this.storeEventLocally(event));
      return;
    }

    try {
      const response = await fetch(`${this.apiUrl}/api/analytics/events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          events: eventsToSend,
          metrics: this.metrics,
        }),
      });

      if (!response.ok) {
        throw new Error(`Analytics API error: ${response.status}`);
      }

      // Clear stored events on successful send
      this.clearStoredEvents();
    } catch (error) {
      console.warn('Failed to send analytics events:', error);
      // Re-queue events for retry
      this.eventQueue.unshift(...eventsToSend);
      
      // Store events locally as backup
      eventsToSend.forEach(event => this.storeEventLocally(event));
    }
  }

  private storeEventLocally(event: AnalyticsEvent): void {
    try {
      const stored = localStorage.getItem('analytics_events');
      const events = stored ? JSON.parse(stored) : [];
      events.push(event);
      
      // Keep only last 1000 events
      if (events.length > 1000) {
        events.splice(0, events.length - 1000);
      }
      
      localStorage.setItem('analytics_events', JSON.stringify(events));
    } catch (error) {
      console.warn('Failed to store analytics event locally:', error);
    }
  }

  private clearStoredEvents(): void {
    try {
      localStorage.removeItem('analytics_events');
    } catch (error) {
      console.warn('Failed to clear stored analytics events:', error);
    }
  }

  // Load and send stored events (for offline recovery)
  async loadStoredEvents(): Promise<void> {
    try {
      const stored = localStorage.getItem('analytics_events');
      if (stored) {
        const events = JSON.parse(stored);
        this.eventQueue.push(...events);
        await this.flushEvents();
      }
    } catch (error) {
      console.warn('Failed to load stored analytics events:', error);
    }
  }

  // Get current session metrics
  getMetrics(): UserMetrics {
    return {
      ...this.metrics,
      timeSpent: Date.now() - (this.metrics.lastActivity - this.metrics.timeSpent),
    };
  }

  // Enable/disable analytics
  setEnabled(enabled: boolean): void {
    if (enabled) {
      this.track('analytics_enabled');
    } else {
      this.track('analytics_disabled');
      this.flushEvents(true);
    }
  }
}

// Create singleton instance
const analytics = new AnalyticsService();

// Export convenience functions
export const trackEvent = (name: string, properties?: Record<string, any>) => {
  analytics.track(name, properties);
};

export const trackPageView = (page?: string) => {
  analytics.trackPageView(page);
};

export const trackUserAction = (action: string, target?: string, properties?: Record<string, any>) => {
  analytics.trackUserAction(action, target, properties);
};

export const trackError = (error: Error, context?: string) => {
  analytics.trackError(error, context);
};

export const trackFeatureUsage = (feature: string, properties?: Record<string, any>) => {
  analytics.trackFeatureUsage(feature, properties);
};

export const trackConversion = (goal: string, value?: number, properties?: Record<string, any>) => {
  analytics.trackConversion(goal, value, properties);
};

export const setUserId = (userId: string) => {
  analytics.setUserId(userId);
};

export const getMetrics = () => {
  return analytics.getMetrics();
};

export default analytics;