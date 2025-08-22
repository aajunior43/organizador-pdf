import logging
import time
import psutil
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from functools import wraps
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import json
import os
from pathlib import Path

# Performance monitoring
@dataclass
class PerformanceMetric:
    timestamp: datetime
    endpoint: str
    method: str
    duration: float
    status_code: int
    memory_usage: float
    cpu_usage: float
    user_id: Optional[str] = None
    error: Optional[str] = None

class PerformanceMonitor:
    def __init__(self, max_metrics: int = 10000):
        self.metrics: deque = deque(maxlen=max_metrics)
        self.endpoint_stats: Dict[str, Dict] = defaultdict(lambda: {
            'count': 0,
            'total_duration': 0,
            'avg_duration': 0,
            'min_duration': float('inf'),
            'max_duration': 0,
            'error_count': 0
        })
        self.logger = logging.getLogger('performance')
    
    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric"""
        self.metrics.append(metric)
        
        # Update endpoint statistics
        key = f"{metric.method} {metric.endpoint}"
        stats = self.endpoint_stats[key]
        stats['count'] += 1
        stats['total_duration'] += metric.duration
        stats['avg_duration'] = stats['total_duration'] / stats['count']
        stats['min_duration'] = min(stats['min_duration'], metric.duration)
        stats['max_duration'] = max(stats['max_duration'], metric.duration)
        
        if metric.error:
            stats['error_count'] += 1
        
        # Log slow requests
        if metric.duration > 5.0:  # 5 seconds threshold
            self.logger.warning(
                f"Slow request detected: {key} took {metric.duration:.2f}s",
                extra={
                    'endpoint': metric.endpoint,
                    'method': metric.method,
                    'duration': metric.duration,
                    'user_id': metric.user_id
                }
            )
    
    def get_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics for the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff]
        
        if not recent_metrics:
            return {}
        
        total_requests = len(recent_metrics)
        avg_duration = sum(m.duration for m in recent_metrics) / total_requests
        error_count = sum(1 for m in recent_metrics if m.error)
        
        return {
            'total_requests': total_requests,
            'avg_response_time': avg_duration,
            'error_rate': error_count / total_requests if total_requests > 0 else 0,
            'slowest_endpoints': self._get_slowest_endpoints(recent_metrics),
            'error_endpoints': self._get_error_endpoints(recent_metrics),
            'system_metrics': self._get_system_metrics()
        }
    
    def _get_slowest_endpoints(self, metrics: list, limit: int = 10) -> list:
        """Get the slowest endpoints"""
        endpoint_times = defaultdict(list)
        for metric in metrics:
            key = f"{metric.method} {metric.endpoint}"
            endpoint_times[key].append(metric.duration)
        
        avg_times = {
            endpoint: sum(times) / len(times)
            for endpoint, times in endpoint_times.items()
        }
        
        return sorted(avg_times.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _get_error_endpoints(self, metrics: list, limit: int = 10) -> list:
        """Get endpoints with most errors"""
        endpoint_errors = defaultdict(int)
        endpoint_total = defaultdict(int)
        
        for metric in metrics:
            key = f"{metric.method} {metric.endpoint}"
            endpoint_total[key] += 1
            if metric.error:
                endpoint_errors[key] += 1
        
        error_rates = {
            endpoint: endpoint_errors[endpoint] / endpoint_total[endpoint]
            for endpoint in endpoint_total
            if endpoint_errors[endpoint] > 0
        }
        
        return sorted(error_rates.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'load_average': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
        }

# Request monitoring decorator
def monitor_performance(monitor: PerformanceMonitor):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            start_cpu = psutil.cpu_percent()
            
            error = None
            status_code = 200
            
            try:
                result = await func(*args, **kwargs)
                if hasattr(result, 'status_code'):
                    status_code = result.status_code
                return result
            except Exception as e:
                error = str(e)
                status_code = 500
                raise
            finally:
                duration = time.time() - start_time
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                memory_usage = end_memory - start_memory
                cpu_usage = psutil.cpu_percent() - start_cpu
                
                # Extract endpoint info from request if available
                endpoint = getattr(args[0], 'url', {}).get('path', 'unknown') if args else 'unknown'
                method = getattr(args[0], 'method', 'unknown') if args else 'unknown'
                user_id = None
                
                # Try to extract user_id from request
                if args and hasattr(args[0], 'state') and hasattr(args[0].state, 'user'):
                    user_id = getattr(args[0].state.user, 'id', None)
                
                metric = PerformanceMetric(
                    timestamp=datetime.now(),
                    endpoint=endpoint,
                    method=method,
                    duration=duration,
                    status_code=status_code,
                    memory_usage=memory_usage,
                    cpu_usage=cpu_usage,
                    user_id=user_id,
                    error=error
                )
                
                monitor.record_metric(metric)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            start_cpu = psutil.cpu_percent()
            
            error = None
            status_code = 200
            
            try:
                result = func(*args, **kwargs)
                if hasattr(result, 'status_code'):
                    status_code = result.status_code
                return result
            except Exception as e:
                error = str(e)
                status_code = 500
                raise
            finally:
                duration = time.time() - start_time
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                memory_usage = end_memory - start_memory
                cpu_usage = psutil.cpu_percent() - start_cpu
                
                endpoint = getattr(args[0], 'url', {}).get('path', 'unknown') if args else 'unknown'
                method = getattr(args[0], 'method', 'unknown') if args else 'unknown'
                user_id = None
                
                if args and hasattr(args[0], 'state') and hasattr(args[0].state, 'user'):
                    user_id = getattr(args[0].state.user, 'id', None)
                
                metric = PerformanceMetric(
                    timestamp=datetime.now(),
                    endpoint=endpoint,
                    method=method,
                    duration=duration,
                    status_code=status_code,
                    memory_usage=memory_usage,
                    cpu_usage=cpu_usage,
                    user_id=user_id,
                    error=error
                )
                
                monitor.record_metric(metric)
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Health check system
class HealthChecker:
    def __init__(self):
        self.checks = {}
        self.logger = logging.getLogger('health')
    
    def register_check(self, name: str, check_func, critical: bool = False):
        """Register a health check"""
        self.checks[name] = {
            'func': check_func,
            'critical': critical,
            'last_result': None,
            'last_check': None
        }
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {}
        overall_status = 'healthy'
        
        for name, check in self.checks.items():
            try:
                start_time = time.time()
                if asyncio.iscoroutinefunction(check['func']):
                    result = await check['func']()
                else:
                    result = check['func']()
                
                duration = time.time() - start_time
                
                check['last_result'] = result
                check['last_check'] = datetime.now()
                
                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'duration': duration,
                    'critical': check['critical'],
                    'timestamp': check['last_check'].isoformat()
                }
                
                if not result and check['critical']:
                    overall_status = 'critical'
                elif not result and overall_status == 'healthy':
                    overall_status = 'degraded'
                    
            except Exception as e:
                self.logger.error(f"Health check {name} failed: {e}")
                results[name] = {
                    'status': 'error',
                    'error': str(e),
                    'critical': check['critical'],
                    'timestamp': datetime.now().isoformat()
                }
                
                if check['critical']:
                    overall_status = 'critical'
                elif overall_status == 'healthy':
                    overall_status = 'degraded'
        
        return {
            'status': overall_status,
            'checks': results,
            'timestamp': datetime.now().isoformat()
        }

# Structured logging
class StructuredLogger:
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.setup_logger(log_file)
    
    def setup_logger(self, log_file: Optional[str]):
        """Setup structured logging"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        self.logger.setLevel(logging.INFO)
    
    def log_event(self, level: str, message: str, **kwargs):
        """Log a structured event"""
        extra_data = {
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        log_message = f"{message} | {json.dumps(extra_data)}"
        
        getattr(self.logger, level.lower())(log_message)
    
    def log_request(self, method: str, endpoint: str, user_id: Optional[str] = None, **kwargs):
        """Log an API request"""
        self.log_event('info', f'API Request: {method} {endpoint}', 
                      method=method, endpoint=endpoint, user_id=user_id, **kwargs)
    
    def log_error(self, error: Exception, context: Optional[str] = None, **kwargs):
        """Log an error with context"""
        self.log_event('error', f'Error: {str(error)}',
                      error_type=type(error).__name__,
                      context=context,
                      **kwargs)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        self.log_event('info', f'Performance: {operation}',
                      operation=operation,
                      duration=duration,
                      **kwargs)

# Metrics collector
class MetricsCollector:
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.timers = defaultdict(list)
    
    def increment(self, name: str, value: int = 1, tags: Optional[Dict] = None):
        """Increment a counter"""
        key = self._make_key(name, tags)
        self.counters[key] += value
    
    def gauge(self, name: str, value: float, tags: Optional[Dict] = None):
        """Set a gauge value"""
        key = self._make_key(name, tags)
        self.gauges[key] = value
    
    def histogram(self, name: str, value: float, tags: Optional[Dict] = None):
        """Add a value to histogram"""
        key = self._make_key(name, tags)
        self.histograms[key].append(value)
        
        # Keep only last 1000 values
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
    
    def timer(self, name: str, tags: Optional[Dict] = None):
        """Context manager for timing operations"""
        return TimerContext(self, name, tags)
    
    def _make_key(self, name: str, tags: Optional[Dict] = None) -> str:
        """Create a key from name and tags"""
        if not tags:
            return name
        
        tag_str = ','.join(f'{k}={v}' for k, v in sorted(tags.items()))
        return f'{name}[{tag_str}]'
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        histogram_stats = {}
        for key, values in self.histograms.items():
            if values:
                histogram_stats[key] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'p95': self._percentile(values, 95),
                    'p99': self._percentile(values, 99)
                }
        
        return {
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': histogram_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def _percentile(self, values: list, percentile: int) -> float:
        """Calculate percentile"""
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

class TimerContext:
    def __init__(self, collector: MetricsCollector, name: str, tags: Optional[Dict] = None):
        self.collector = collector
        self.name = name
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.collector.histogram(self.name, duration, self.tags)

# Global instances
performance_monitor = PerformanceMonitor()
health_checker = HealthChecker()
structured_logger = StructuredLogger('app')
metrics_collector = MetricsCollector()

# Register default health checks
async def database_health_check():
    """Check database connectivity"""
    try:
        from app.models.database import engine
        with engine.connect() as conn:
            conn.execute('SELECT 1')
        return True
    except Exception:
        return False

def disk_space_check():
    """Check available disk space"""
    try:
        usage = psutil.disk_usage('/')
        return usage.percent < 90  # Alert if disk usage > 90%
    except Exception:
        return False

def memory_check():
    """Check memory usage"""
    try:
        memory = psutil.virtual_memory()
        return memory.percent < 85  # Alert if memory usage > 85%
    except Exception:
        return False

# Register health checks
health_checker.register_check('database', database_health_check, critical=True)
health_checker.register_check('disk_space', disk_space_check, critical=False)
health_checker.register_check('memory', memory_check, critical=False)

# Export monitoring utilities
__all__ = [
    'performance_monitor',
    'health_checker', 
    'structured_logger',
    'metrics_collector',
    'monitor_performance',
    'PerformanceMetric',
    'PerformanceMonitor',
    'HealthChecker',
    'StructuredLogger',
    'MetricsCollector'
]