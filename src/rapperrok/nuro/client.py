"""Nuro API client implementation."""

import logging
from typing import Any

from ..common.base import BaseAPIClient
from ..common.models import PollConfig, RetryConfig
from .models import NuroCreateRequest, NuroTaskResponse

logger = logging.getLogger(__name__)


class NuroClient:
    """Client for Nuro music generation API.

    Nuro specializes in generating complete 4-minute songs in ~30 seconds.
    Supports both vocal and instrumental music generation.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.aimusicapi.ai",
        timeout: int = 30,
        retry_config: RetryConfig | None = None,
        poll_config: PollConfig | None = None,
    ) -> None:
        """Initialize Nuro client.

        Args:
            api_key: AI Music API key
            base_url: Base API URL
            timeout: Default timeout in seconds
            retry_config: Retry configuration
            poll_config: Polling configuration
        """
        self._base_client = BaseAPIClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retry_config=retry_config,
        )
        self.poll_config = poll_config or PollConfig()

    async def create_vocal_music(
        self,
        prompt: str,
        *,
        duration: int = 240,
        style: str | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> NuroTaskResponse:
        """Create music with vocals.

        Args:
            prompt: Music generation prompt
            duration: Duration in seconds (30-240)
            style: Musical style
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            result = await client.nuro.create_vocal_music(
                prompt="epic orchestral soundtrack with choir",
                duration=240,
                style="cinematic"
            )
            ```
        """
        request = NuroCreateRequest(
            prompt=prompt,
            duration=duration,
            style=style,
            has_vocals=True,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/nuro/v1/music/create/vocal",
            json=request.model_dump(exclude_none=True),
        )

        response = NuroTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def create_instrumental_music(
        self,
        prompt: str,
        *,
        duration: int = 180,
        style: str | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> NuroTaskResponse:
        """Create instrumental music (no vocals).

        Args:
            prompt: Music generation prompt
            duration: Duration in seconds (30-240)
            style: Musical style
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            result = await client.nuro.create_instrumental_music(
                prompt="ambient electronic atmosphere",
                duration=180
            )
            ```
        """
        request = NuroCreateRequest(
            prompt=prompt,
            duration=duration,
            style=style,
            has_vocals=False,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/nuro/v1/music/create/instrumental",
            json=request.model_dump(exclude_none=True),
        )

        response = NuroTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def get_task(
        self,
        task_id: str,
    ) -> NuroTaskResponse:
        """Get task status and result.

        Args:
            task_id: Task ID to check

        Returns:
            Task response
        """
        data = await self._base_client.get(
            "/nuro/v1/music/get",
            params={"task_id": task_id},
        )

        return NuroTaskResponse(**data)

    async def wait_for_completion(
        self,
        task_id: str,
        *,
        max_attempts: int | None = None,
        interval: float | None = None,
        timeout: int | None = None,
    ) -> NuroTaskResponse:
        """Wait for task to complete.

        Args:
            task_id: Task ID to wait for
            max_attempts: Maximum polling attempts
            interval: Polling interval in seconds
            timeout: Total timeout in seconds

        Returns:
            Completed task response

        Raises:
            TaskFailedError: If task fails
            TimeoutError: If task doesn't complete in time
        """
        import asyncio

        max_attempts = max_attempts or self.poll_config.max_attempts
        interval = interval or self.poll_config.interval
        timeout_val = timeout or self.poll_config.timeout

        start_time = asyncio.get_event_loop().time()

        for attempt in range(max_attempts):
            result = await self.get_task(task_id)

            if result.status.value == "completed":
                return result
            elif result.status.value == "failed":
                from ..common.exceptions import TaskFailedError

                error_msg = result.message or "Task failed"
                raise TaskFailedError(error_msg, task_id=task_id)

            if timeout_val:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed >= timeout_val:
                    from ..common.exceptions import TimeoutError as APITimeoutError

                    raise APITimeoutError(
                        f"Task {task_id} timeout after {elapsed:.0f}s",
                        timeout_seconds=timeout_val,
                    )

            if attempt < max_attempts - 1:
                await asyncio.sleep(interval)

        from ..common.exceptions import TimeoutError as APITimeoutError

        raise APITimeoutError(
            f"Task {task_id} did not complete within {max_attempts} attempts",
            timeout_seconds=int(max_attempts * interval),
        )

    async def close(self) -> None:
        """Close HTTP client."""
        await self._base_client.close()

    async def __aenter__(self) -> "NuroClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
