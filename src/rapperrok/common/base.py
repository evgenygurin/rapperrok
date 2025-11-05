"""Base HTTP client for AI Music API."""

import asyncio
import logging
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .exceptions import (
    AIMusicAPIError,
    AuthenticationError,
    InsufficientCreditsError,
    InvalidParameterError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    TaskFailedError,
)
from .models import ErrorResponse, RetryConfig

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Base HTTP client with retry logic and error handling."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.aimusicapi.com",
        timeout: int = 30,
        retry_config: RetryConfig | None = None,
    ) -> None:
        """Initialize base API client.

        Args:
            api_key: AI Music API key
            base_url: Base URL for API endpoints
            timeout: Default timeout in seconds
            retry_config: Retry configuration
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig()

        self._client: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers=self._get_headers(),
            )
        return self._client

    def _get_headers(self) -> dict[str, str]:
        """Get default headers for requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "rapperrok-python/0.1.0",
        }

    async def _handle_error(self, response: httpx.Response) -> None:
        """Handle error responses.

        Args:
            response: HTTP response object

        Raises:
            AIMusicAPIError: Appropriate exception based on error type
        """
        try:
            error_data = response.json()
            error_resp = ErrorResponse(**error_data)
            error_msg = error_resp.error
            error_code = error_resp.error_code
        except Exception:
            error_msg = response.text or f"HTTP {response.status_code}"
            error_code = None

        # Map status codes to specific exceptions
        if response.status_code == 401:
            raise AuthenticationError(error_msg)
        elif response.status_code == 402:
            raise InsufficientCreditsError(error_msg)
        elif response.status_code == 400:
            raise InvalidParameterError(error_msg)
        elif response.status_code == 404:
            raise ResourceNotFoundError(error_msg)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                error_msg,
                retry_after=int(retry_after) if retry_after else None,
            )
        elif response.status_code >= 500:
            raise TaskFailedError(error_msg, error_code=error_code)
        else:
            raise AIMusicAPIError(error_msg, status_code=response.status_code)

    def _create_retry_decorator(self) -> Any:
        """Create retry decorator with configured settings."""
        return retry(
            stop=stop_after_attempt(self.retry_config.max_retries),
            wait=wait_exponential(
                multiplier=self.retry_config.initial_delay,
                max=self.retry_config.max_delay,
                exp_base=self.retry_config.exponential_base,
            ),
            retry=retry_if_exception_type((RateLimitError, NetworkError)),
            reraise=True,
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json: JSON request body
            data: Form data
            files: Files to upload
            params: Query parameters
            timeout: Request timeout (overrides default)

        Returns:
            Parsed JSON response

        Raises:
            AIMusicAPIError: On API errors
            NetworkError: On network errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        request_kwargs: dict[str, Any] = {
            "method": method,
            "url": url,
            "params": params,
        }

        if json is not None:
            request_kwargs["json"] = json
        elif data is not None or files is not None:
            # For file uploads, use multipart
            request_kwargs["data"] = data
            request_kwargs["files"] = files
            # Remove Content-Type header for multipart
            headers = self._get_headers()
            headers.pop("Content-Type", None)
            request_kwargs["headers"] = headers

        if timeout:
            request_kwargs["timeout"] = httpx.Timeout(timeout)

        try:
            logger.debug(f"{method} {url}")
            response = await self.client.request(**request_kwargs)

            if response.status_code >= 400:
                await self._handle_error(response)

            return response.json()

        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {e}", original_error=e) from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}", original_error=e) from e
        except AIMusicAPIError:
            raise
        except Exception as e:
            raise NetworkError(f"Unexpected error: {e}", original_error=e) from e

    async def get(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Make GET request."""
        return await self._request("GET", endpoint, params=params, timeout=timeout)

    async def post(
        self,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Make POST request."""
        return await self._request(
            "POST",
            endpoint,
            json=json,
            data=data,
            files=files,
            params=params,
            timeout=timeout,
        )

    async def put(
        self,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Make PUT request."""
        return await self._request("PUT", endpoint, json=json, timeout=timeout)

    async def delete(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Make DELETE request."""
        return await self._request("DELETE", endpoint, params=params, timeout=timeout)

    async def poll_task(
        self,
        task_id: str,
        get_endpoint: str,
        max_attempts: int = 60,
        interval: float = 5.0,
    ) -> dict[str, Any]:
        """Poll task until completion.

        Args:
            task_id: Task ID to poll
            get_endpoint: Endpoint to check task status
            max_attempts: Maximum number of polling attempts
            interval: Interval between polls in seconds

        Returns:
            Final task result

        Raises:
            TaskFailedError: If task fails
            TimeoutError: If polling exceeds max attempts
        """
        for attempt in range(max_attempts):
            result = await self.get(get_endpoint, params={"task_id": task_id})

            status = result.get("status", "").lower()

            if status == "completed":
                return result
            elif status == "failed":
                error_msg = result.get("error", "Task failed")
                raise TaskFailedError(error_msg, task_id=task_id)
            elif status in ("pending", "processing"):
                if attempt < max_attempts - 1:
                    await asyncio.sleep(interval)
                    continue

        from .exceptions import TimeoutError as APITimeoutError

        raise APITimeoutError(
            f"Task {task_id} did not complete within {max_attempts * interval} seconds",
            timeout_seconds=int(max_attempts * interval),
        )

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "BaseAPIClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
