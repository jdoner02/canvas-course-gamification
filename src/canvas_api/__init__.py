"""
Canvas API Client Module

Provides a clean, robust interface for interacting with the Canvas LMS REST API.
Includes error handling, rate limiting, and authentication management.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from functools import wraps

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from canvasapi import Canvas
    from canvasapi.exceptions import CanvasException

    CANVASAPI_AVAILABLE = True
except ImportError:
    CANVASAPI_AVAILABLE = False


logger = logging.getLogger(__name__)


class CanvasAPIError(Exception):
    """Custom exception for Canvas API errors."""

    pass


class RateLimitError(CanvasAPIError):
    """Exception raised when API rate limit is exceeded."""

    pass


def retry_on_rate_limit(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator to retry API calls when rate limited."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        raise e
                    delay = base_delay * (2**attempt)
                    logger.warning(
                        f"Rate limited, retrying in {delay}s (attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class CanvasAPIClient:
    """
    Enhanced Canvas API client with error handling and rate limiting.

    Provides both high-level methods for common operations and low-level
    access to the Canvas API for advanced use cases.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        course_id: Optional[str] = None,
    ):
        """
        Initialize the Canvas API client.

        Args:
            api_url: Canvas instance URL (defaults to CANVAS_API_URL env var)
            api_token: Canvas API token (defaults to CANVAS_API_TOKEN env var)
            course_id: Default course ID (defaults to CANVAS_COURSE_ID env var)
        """
        self.api_url = api_url or os.getenv("CANVAS_API_URL")
        self.api_token = api_token or os.getenv("CANVAS_API_TOKEN")
        self.course_id = course_id or os.getenv("CANVAS_COURSE_ID")

        if not self.api_url or not self.api_token:
            raise CanvasAPIError(
                "Canvas API URL and token are required. "
                "Set CANVAS_API_URL and CANVAS_API_TOKEN environment variables."
            )

        # Initialize HTTP session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }
        )

        # Initialize canvasapi client if available
        self.canvas = None
        if CANVASAPI_AVAILABLE:
            try:
                self.canvas = Canvas(self.api_url, self.api_token)
                logger.info("Canvas API client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize canvasapi client: {e}")

    def get_course(self, course_id: Optional[str] = None):
        """Get a Canvas course object."""
        if not CANVASAPI_AVAILABLE:
            raise CanvasAPIError(
                "canvasapi library not available. Install with: pip install canvasapi"
            )

        target_course_id = course_id or self.course_id
        if not target_course_id:
            raise CanvasAPIError("Course ID is required")

        try:
            return self.canvas.get_course(int(target_course_id))
        except (ValueError, CanvasException) as e:
            raise CanvasAPIError(f"Failed to get course {target_course_id}: {e}")

    @retry_on_rate_limit()
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a raw API request to Canvas.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            CanvasAPIError: For API errors
            RateLimitError: When rate limited
        """
        url = f"{self.api_url.rstrip('/')}/api/v1/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, **kwargs)

            # Check for rate limiting
            if response.status_code == 429:
                raise RateLimitError("API rate limit exceeded")

            # Check for other errors
            response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:
            raise CanvasAPIError(f"API request failed: {e}")

    def get(self, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make a GET request and return JSON response."""
        response = self.make_request("GET", endpoint, **kwargs)
        return response.json()

    def post(self, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make a POST request and return JSON response."""
        response = self.make_request("POST", endpoint, **kwargs)
        return response.json()

    def put(self, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make a PUT request and return JSON response."""
        response = self.make_request("PUT", endpoint, **kwargs)
        return response.json()

    def delete(self, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make a DELETE request and return JSON response."""
        response = self.make_request("DELETE", endpoint, **kwargs)
        return response.json() if response.content else {}

    # Course Management Methods

    def create_module(
        self, course_id: Optional[str] = None, **module_data
    ) -> Dict[Any, Any]:
        """Create a new module in the course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/modules"
        return self.post(endpoint, json={"module": module_data})

    def create_assignment(
        self, course_id: Optional[str] = None, **assignment_data
    ) -> Dict[Any, Any]:
        """Create a new assignment in the course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/assignments"
        return self.post(endpoint, json={"assignment": assignment_data})

    def create_page(
        self, course_id: Optional[str] = None, **page_data
    ) -> Dict[Any, Any]:
        """Create a new page in the course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/pages"
        return self.post(endpoint, json={"wiki_page": page_data})

    def create_quiz(
        self, course_id: Optional[str] = None, **quiz_data
    ) -> Dict[Any, Any]:
        """Create a new quiz in the course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/quizzes"
        return self.post(endpoint, json={"quiz": quiz_data})

    def get_modules(self, course_id: Optional[str] = None) -> List[Dict[Any, Any]]:
        """Get all modules for a course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/modules"
        return self.get(endpoint)

    def get_assignments(self, course_id: Optional[str] = None) -> List[Dict[Any, Any]]:
        """Get all assignments for a course."""
        target_course_id = course_id or self.course_id
        endpoint = f"courses/{target_course_id}/assignments"
        return self.get(endpoint)

    def validate_connection(self) -> bool:
        """Test the Canvas API connection."""
        try:
            self.get("users/self")
            return True
        except Exception as e:
            logger.error(f"Canvas API connection failed: {e}")
            return False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if hasattr(self.session, "close"):
            self.session.close()


# Backward compatibility
def get_course(course_id: Optional[str] = None):
    """Legacy function for backward compatibility."""
    client = CanvasAPIClient()
    return client.get_course(course_id)


# Module-level client instance for simple usage
_default_client = None


def get_client() -> CanvasAPIClient:
    """Get the default Canvas API client instance."""
    global _default_client
    if _default_client is None:
        _default_client = CanvasAPIClient()
    return _default_client
