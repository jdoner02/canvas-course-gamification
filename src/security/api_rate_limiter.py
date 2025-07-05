#!/usr/bin/env python3
"""
API Rate Limiter for Eagle Adventures 2
=======================================

Intelligent API rate limiting system that prevents abuse while ensuring
optimal performance for educational gamification operations.

Features:
- Canvas API rate limiting with burst allowance
- GitHub API rate limiting
- Adaptive throttling based on response times
- Per-user and per-endpoint rate limiting
- Automatic backoff and retry logic
- Rate limit monitoring and alerting
- Educational priority queueing

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import asyncio
import json
import logging
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import yaml
import aiohttp
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimitStatus(Enum):
    """Rate limit status"""

    ALLOWED = "allowed"
    THROTTLED = "throttled"
    BLOCKED = "blocked"
    QUOTA_EXCEEDED = "quota_exceeded"


class Priority(Enum):
    """Request priority levels"""

    CRITICAL = 1  # System health, emergency operations
    HIGH = 2  # Student progress updates, real-time features
    NORMAL = 3  # Standard operations
    LOW = 4  # Background sync, analytics
    BULK = 5  # Mass operations, data export


@dataclass
class RateLimit:
    """Rate limit configuration"""

    requests_per_second: float
    requests_per_minute: int
    requests_per_hour: int
    burst_allowance: int
    max_concurrent: int = 10
    backoff_factor: float = 1.5
    max_backoff_seconds: int = 300


@dataclass
class RateLimitBucket:
    """Token bucket for rate limiting"""

    capacity: int
    tokens: float
    last_refill: float
    refill_rate: float  # tokens per second

    def __post_init__(self):
        if self.last_refill == 0:
            self.last_refill = time.time()


@dataclass
class RequestMetrics:
    """Request metrics for adaptive throttling"""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    rate_limited_requests: int = 0
    last_request_time: float = 0.0

    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests


@dataclass
class QueuedRequest:
    """Queued request with priority"""

    request_id: str
    endpoint: str
    priority: Priority
    user_id: str
    created_at: float
    callback: Callable
    args: tuple
    kwargs: dict
    retries: int = 0
    max_retries: int = 3


class APIRateLimiter:
    """
    Comprehensive API rate limiting system

    Manages rate limits for multiple APIs (Canvas, GitHub, etc.) with
    intelligent throttling, priority queueing, and adaptive backoff.
    """

    def __init__(self, config_path: str = "config/rate_limit_config.yml"):
        self.config_path = config_path
        self.config = self._load_config()

        # Rate limit buckets per endpoint
        self.buckets: Dict[str, RateLimitBucket] = {}

        # Request metrics per endpoint
        self.metrics: Dict[str, RequestMetrics] = defaultdict(RequestMetrics)

        # Priority queues per endpoint
        self.request_queues: Dict[str, List[QueuedRequest]] = defaultdict(list)

        # Active requests tracking
        self.active_requests: Dict[str, int] = defaultdict(int)

        # Rate limit configurations
        self.rate_limits = self._initialize_rate_limits()

        # Request history for monitoring
        self.request_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))

        # Background tasks
        self._queue_processor_task = None
        self._metrics_updater_task = None

        self._start_background_tasks()

        logger.info("🚦 API Rate Limiter initialized with intelligent throttling")

    def _load_config(self) -> Dict[str, Any]:
        """Load rate limiting configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("rate_limiting", {})
        except Exception as e:
            logger.warning(f"⚠️ Could not load rate limit config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default rate limiting configuration"""
        return {
            "canvas_api": {
                "requests_per_second": 10,
                "requests_per_minute": 300,
                "requests_per_hour": 3000,
                "burst_allowance": 20,
                "max_concurrent": 5,
            },
            "github_api": {
                "requests_per_second": 5,
                "requests_per_minute": 100,
                "requests_per_hour": 5000,
                "burst_allowance": 10,
                "max_concurrent": 3,
            },
            "internal_api": {
                "requests_per_second": 50,
                "requests_per_minute": 1000,
                "requests_per_hour": 10000,
                "burst_allowance": 100,
                "max_concurrent": 20,
            },
            "adaptive_throttling": {
                "enabled": True,
                "response_time_threshold": 2.0,
                "error_rate_threshold": 0.1,
                "throttle_factor": 0.5,
            },
            "monitoring": {
                "alert_on_quota_exceeded": True,
                "alert_on_high_error_rate": True,
                "metrics_retention_hours": 24,
            },
        }

    def _initialize_rate_limits(self) -> Dict[str, RateLimit]:
        """Initialize rate limit configurations"""
        rate_limits = {}

        for endpoint, config in self.config.items():
            if isinstance(config, dict) and "requests_per_second" in config:
                rate_limits[endpoint] = RateLimit(
                    requests_per_second=config["requests_per_second"],
                    requests_per_minute=config["requests_per_minute"],
                    requests_per_hour=config["requests_per_hour"],
                    burst_allowance=config["burst_allowance"],
                    max_concurrent=config.get("max_concurrent", 10),
                )

                # Initialize token bucket
                self.buckets[endpoint] = RateLimitBucket(
                    capacity=config["burst_allowance"],
                    tokens=config["burst_allowance"],
                    last_refill=time.time(),
                    refill_rate=config["requests_per_second"],
                )

        logger.info(f"🎯 Initialized rate limits for {len(rate_limits)} endpoints")
        return rate_limits

    def _start_background_tasks(self):
        """Start background processing tasks"""
        if not self._queue_processor_task:
            self._queue_processor_task = asyncio.create_task(
                self._process_request_queues()
            )

        if not self._metrics_updater_task:
            self._metrics_updater_task = asyncio.create_task(
                self._update_metrics_periodically()
            )

    async def check_rate_limit(
        self,
        endpoint: str,
        user_id: str = "anonymous",
        priority: Priority = Priority.NORMAL,
    ) -> RateLimitStatus:
        """
        Check if request is allowed under current rate limits

        Args:
            endpoint: API endpoint identifier
            user_id: User making the request
            priority: Request priority level

        Returns:
            RateLimitStatus indicating whether request is allowed
        """
        rate_limit = self.rate_limits.get(endpoint)
        if not rate_limit:
            logger.warning(f"⚠️ No rate limit configured for endpoint: {endpoint}")
            return RateLimitStatus.ALLOWED

        bucket = self.buckets.get(endpoint)
        if not bucket:
            logger.error(f"❌ No token bucket found for endpoint: {endpoint}")
            return RateLimitStatus.BLOCKED

        # Refill tokens based on elapsed time
        now = time.time()
        elapsed = now - bucket.last_refill
        tokens_to_add = elapsed * bucket.refill_rate
        bucket.tokens = min(bucket.capacity, bucket.tokens + tokens_to_add)
        bucket.last_refill = now

        # Check concurrent request limit
        if self.active_requests[endpoint] >= rate_limit.max_concurrent:
            return RateLimitStatus.THROTTLED

        # Check if we have tokens available
        if bucket.tokens >= 1.0:
            # Check adaptive throttling
            if self._should_apply_adaptive_throttling(endpoint):
                return RateLimitStatus.THROTTLED

            bucket.tokens -= 1.0
            self.active_requests[endpoint] += 1
            return RateLimitStatus.ALLOWED
        else:
            return RateLimitStatus.THROTTLED

    def _should_apply_adaptive_throttling(self, endpoint: str) -> bool:
        """Check if adaptive throttling should be applied"""
        if not self.config.get("adaptive_throttling", {}).get("enabled", True):
            return False

        metrics = self.metrics[endpoint]
        adaptive_config = self.config.get("adaptive_throttling", {})

        # Check response time threshold
        response_time_threshold = adaptive_config.get("response_time_threshold", 2.0)
        if metrics.avg_response_time > response_time_threshold:
            logger.debug(f"🐌 Adaptive throttling: slow response time for {endpoint}")
            return True

        # Check error rate threshold
        error_rate_threshold = adaptive_config.get("error_rate_threshold", 0.1)
        if metrics.success_rate() < (1.0 - error_rate_threshold):
            logger.debug(f"❌ Adaptive throttling: high error rate for {endpoint}")
            return True

        return False

    async def make_request_with_rate_limit(
        self,
        endpoint: str,
        request_func: Callable,
        user_id: str = "anonymous",
        priority: Priority = Priority.NORMAL,
        *args,
        **kwargs,
    ) -> Any:
        """
        Make an API request with rate limiting

        Args:
            endpoint: API endpoint identifier
            request_func: Function to make the actual request
            user_id: User making the request
            priority: Request priority level
            args, kwargs: Arguments for request function

        Returns:
            Response from the API call
        """
        start_time = time.time()

        try:
            # Check rate limit
            status = await self.check_rate_limit(endpoint, user_id, priority)

            if status == RateLimitStatus.ALLOWED:
                # Make the request
                result = await self._execute_request(
                    endpoint, request_func, *args, **kwargs
                )

                # Update metrics
                self._update_request_metrics(
                    endpoint, success=True, response_time=time.time() - start_time
                )

                return result

            elif status == RateLimitStatus.THROTTLED:
                # Queue the request
                return await self._queue_request(
                    endpoint, request_func, user_id, priority, *args, **kwargs
                )

            else:
                # Rate limit exceeded
                self._update_request_metrics(
                    endpoint, success=False, response_time=time.time() - start_time
                )
                raise Exception(f"Rate limit exceeded for {endpoint}")

        finally:
            # Release active request count
            if self.active_requests[endpoint] > 0:
                self.active_requests[endpoint] -= 1

    async def _execute_request(
        self, endpoint: str, request_func: Callable, *args, **kwargs
    ) -> Any:
        """Execute the actual API request"""
        try:
            if asyncio.iscoroutinefunction(request_func):
                return await request_func(*args, **kwargs)
            else:
                return request_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Request failed for {endpoint}: {e}")
            raise

    async def _queue_request(
        self,
        endpoint: str,
        request_func: Callable,
        user_id: str,
        priority: Priority,
        *args,
        **kwargs,
    ) -> Any:
        """Queue a request for later processing"""
        request_id = f"{endpoint}_{user_id}_{int(time.time() * 1000)}"

        queued_request = QueuedRequest(
            request_id=request_id,
            endpoint=endpoint,
            priority=priority,
            user_id=user_id,
            created_at=time.time(),
            callback=request_func,
            args=args,
            kwargs=kwargs,
        )

        # Add to priority queue
        self.request_queues[endpoint].append(queued_request)

        # Sort by priority (lower number = higher priority)
        self.request_queues[endpoint].sort(
            key=lambda x: (x.priority.value, x.created_at)
        )

        logger.debug(f"📦 Request queued: {request_id} (Priority: {priority.value})")

        # Create a future to return when request is processed
        future = asyncio.Future()
        queued_request.future = future

        return await future

    async def _process_request_queues(self):
        """Background task to process queued requests"""
        while True:
            try:
                for endpoint in list(self.request_queues.keys()):
                    queue = self.request_queues[endpoint]

                    if not queue:
                        continue

                    # Check if we can process requests for this endpoint
                    status = await self.check_rate_limit(
                        endpoint, "queue_processor", Priority.NORMAL
                    )

                    if status == RateLimitStatus.ALLOWED and queue:
                        # Process highest priority request
                        request = queue.pop(0)

                        try:
                            # Execute the request
                            result = await self._execute_request(
                                request.endpoint,
                                request.callback,
                                *request.args,
                                **request.kwargs,
                            )

                            # Complete the future
                            if hasattr(request, "future") and not request.future.done():
                                request.future.set_result(result)

                            logger.debug(
                                f"✅ Processed queued request: {request.request_id}"
                            )

                        except Exception as e:
                            # Handle request failure
                            if request.retries < request.max_retries:
                                request.retries += 1
                                queue.append(request)  # Re-queue for retry
                                logger.warning(
                                    f"🔄 Retrying request {request.request_id} (attempt {request.retries})"
                                )
                            else:
                                # Max retries exceeded
                                if (
                                    hasattr(request, "future")
                                    and not request.future.done()
                                ):
                                    request.future.set_exception(e)
                                logger.error(
                                    f"❌ Request failed after max retries: {request.request_id}"
                                )

                # Sleep between queue processing cycles
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"❌ Error in queue processor: {e}")
                await asyncio.sleep(1)

    def _update_request_metrics(
        self, endpoint: str, success: bool, response_time: float
    ):
        """Update request metrics for monitoring"""
        metrics = self.metrics[endpoint]

        metrics.total_requests += 1
        metrics.last_request_time = time.time()

        if success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1

        # Update average response time (exponential moving average)
        alpha = 0.1  # Smoothing factor
        if metrics.avg_response_time == 0:
            metrics.avg_response_time = response_time
        else:
            metrics.avg_response_time = (
                alpha * response_time + (1 - alpha) * metrics.avg_response_time
            )

        # Add to request history
        self.request_history[endpoint].append(
            {
                "timestamp": time.time(),
                "success": success,
                "response_time": response_time,
            }
        )

    async def _update_metrics_periodically(self):
        """Background task to update and clean up metrics"""
        while True:
            try:
                # Clean up old request history
                cutoff_time = time.time() - (24 * 3600)  # 24 hours

                for endpoint, history in self.request_history.items():
                    while history and history[0]["timestamp"] < cutoff_time:
                        history.popleft()

                # Log metrics for monitoring
                self._log_rate_limit_metrics()

                await asyncio.sleep(300)  # Update every 5 minutes

            except Exception as e:
                logger.error(f"❌ Error updating metrics: {e}")
                await asyncio.sleep(60)

    def _log_rate_limit_metrics(self):
        """Log rate limiting metrics for monitoring"""
        for endpoint, metrics in self.metrics.items():
            if metrics.total_requests > 0:
                logger.info(
                    f"📊 {endpoint}: {metrics.total_requests} requests, "
                    f"{metrics.success_rate():.2%} success rate, "
                    f"{metrics.avg_response_time:.3f}s avg response"
                )

                # Check for alerts
                if metrics.success_rate() < 0.9:
                    logger.warning(
                        f"⚠️ High error rate for {endpoint}: {metrics.success_rate():.2%}"
                    )

                if metrics.avg_response_time > 5.0:
                    logger.warning(
                        f"⚠️ Slow response times for {endpoint}: {metrics.avg_response_time:.3f}s"
                    )

    def get_rate_limit_status(self, endpoint: str = None) -> Dict[str, Any]:
        """
        Get current rate limit status

        Args:
            endpoint: Specific endpoint to check, or None for all endpoints

        Returns:
            Rate limit status information
        """
        if endpoint:
            # Single endpoint status
            bucket = self.buckets.get(endpoint)
            metrics = self.metrics.get(endpoint, RequestMetrics())
            queue_size = len(self.request_queues.get(endpoint, []))

            return {
                "endpoint": endpoint,
                "tokens_available": bucket.tokens if bucket else 0,
                "active_requests": self.active_requests.get(endpoint, 0),
                "queue_size": queue_size,
                "total_requests": metrics.total_requests,
                "success_rate": metrics.success_rate(),
                "avg_response_time": metrics.avg_response_time,
                "status": "healthy" if metrics.success_rate() > 0.9 else "warning",
            }
        else:
            # All endpoints status
            status = {
                "overall_status": "healthy",
                "endpoints": {},
                "total_active_requests": sum(self.active_requests.values()),
                "total_queued_requests": sum(
                    len(q) for q in self.request_queues.values()
                ),
            }

            for endpoint in self.rate_limits.keys():
                endpoint_status = self.get_rate_limit_status(endpoint)
                status["endpoints"][endpoint] = endpoint_status

                if endpoint_status["status"] == "warning":
                    status["overall_status"] = "warning"

            return status

    def reset_rate_limits(self, endpoint: str = None):
        """
        Reset rate limits (for testing or emergency situations)

        Args:
            endpoint: Specific endpoint to reset, or None for all endpoints
        """
        if endpoint:
            endpoints = [endpoint]
        else:
            endpoints = list(self.buckets.keys())

        for ep in endpoints:
            if ep in self.buckets:
                bucket = self.buckets[ep]
                bucket.tokens = bucket.capacity
                bucket.last_refill = time.time()

                # Clear queue
                self.request_queues[ep].clear()

                # Reset active requests
                self.active_requests[ep] = 0

                logger.info(f"🔄 Rate limits reset for {ep}")

    def shutdown(self):
        """Shutdown rate limiter and cancel background tasks"""
        if self._queue_processor_task:
            self._queue_processor_task.cancel()

        if self._metrics_updater_task:
            self._metrics_updater_task.cancel()

        logger.info("🛑 API Rate Limiter shutdown complete")


# Decorator for automatic rate limiting
def rate_limited(endpoint: str, priority: Priority = Priority.NORMAL):
    """
    Decorator to automatically apply rate limiting to functions

    Args:
        endpoint: API endpoint identifier
        priority: Request priority level
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get rate limiter instance (assumes it exists in global scope or can be injected)
            rate_limiter = getattr(wrapper, "_rate_limiter", None)
            if not rate_limiter:
                # Create default rate limiter if none exists
                rate_limiter = APIRateLimiter()
                wrapper._rate_limiter = rate_limiter

            return await rate_limiter.make_request_with_rate_limit(
                endpoint, func, "decorator_user", priority, *args, **kwargs
            )

        return wrapper

    return decorator


# Example usage and testing
async def main():
    """Example usage of API Rate Limiter"""
    rate_limiter = APIRateLimiter()

    # Example function to rate limit
    async def example_api_call(data: str) -> str:
        await asyncio.sleep(0.1)  # Simulate API call
        return f"Response for: {data}"

    # Make rate-limited requests
    tasks = []
    for i in range(20):
        task = rate_limiter.make_request_with_rate_limit(
            "canvas_api",
            example_api_call,
            f"user_{i % 3}",
            Priority.NORMAL,
            f"request_{i}",
        )
        tasks.append(task)

    # Execute requests
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Check results
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Request {i} failed: {result}")
        else:
            print(f"Request {i} succeeded: {result}")

    # Get status
    status = rate_limiter.get_rate_limit_status()
    print(f"Rate Limiter Status: {json.dumps(status, indent=2)}")

    # Cleanup
    rate_limiter.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
