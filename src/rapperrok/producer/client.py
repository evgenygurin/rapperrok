"""Producer API client implementation (FUZZ-2.0 model)."""

import logging
from pathlib import Path
from typing import Any

from ..common.base import BaseAPIClient
from ..common.models import PollConfig, RetryConfig
from .models import (
    ProducerCreateRequest,
    ProducerDownloadRequest,
    ProducerDownloadResponse,
    ProducerOperation,
    ProducerTaskResponse,
    ProducerUploadResponse,
)

logger = logging.getLogger(__name__)


class ProducerClient:
    """Client for Producer API (FUZZ-2.0 model).

    Producer specializes in fast, high-quality music generation
    with 30-second generation time. Supports various operations:
    create, extend, cover, replace, swap vocals/instrumentals, variations.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.aimusicapi.ai",
        timeout: int = 30,
        retry_config: RetryConfig | None = None,
        poll_config: PollConfig | None = None,
    ) -> None:
        """Initialize Producer client.

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

    async def create_music(
        self,
        *,
        operation: ProducerOperation = "create",
        description: str | None = None,
        audio_id: str | None = None,
        audio_url: str | None = None,
        duration: int = 60,
        style: str | None = None,
        vocal_style: str | None = None,
        instrumental_style: str | None = None,
        replace_section: dict[str, int] | None = None,
        variation_intensity: float | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> ProducerTaskResponse:
        """Create or modify music with Producer.

        This is a unified endpoint that handles all Producer operations.

        Args:
            operation: Operation type (create, extend, cover, etc.)
            description: Music description (for create operation)
            audio_id: Audio ID (for extend/modify operations)
            audio_url: Audio URL (for cover operation)
            duration: Duration in seconds (10-240)
            style: Musical style
            vocal_style: Vocal style (for swap_vocal)
            instrumental_style: Instrumental style (for swap_instrumental)
            replace_section: Section to replace {start: int, end: int}
            variation_intensity: Variation intensity 0.0-1.0
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Examples:
            Create new music:
            ```python
            result = await client.producer.create_music(
                operation="create",
                description="energetic EDM track",
                duration=60
            )
            ```

            Extend existing track:
            ```python
            result = await client.producer.create_music(
                operation="extend",
                audio_id="clip_abc123",
                duration=30
            )
            ```

            Swap vocals:
            ```python
            result = await client.producer.create_music(
                operation="swap_vocal",
                audio_id="clip_abc123",
                vocal_style="opera singer, dramatic"
            )
            ```
        """
        request = ProducerCreateRequest(
            operation=operation,
            description=description,
            audio_id=audio_id,
            audio_url=audio_url,
            duration=duration,
            style=style,
            vocal_style=vocal_style,
            instrumental_style=instrumental_style,
            replace_section=replace_section,
            variation_intensity=variation_intensity,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/producer/v1/music/create",
            json=request.model_dump(exclude_none=True),
        )

        response = ProducerTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def upload_music(
        self,
        file_path: str | Path,
    ) -> ProducerUploadResponse:
        """Upload music file to Producer.

        Args:
            file_path: Path to audio file

        Returns:
            Upload response with audio_id

        Example:
            ```python
            upload = await client.producer.upload_music("my_song.mp3")
            print(f"Audio ID: {upload.audio_id}")

            # Use audio_id for operations
            extended = await client.producer.create_music(
                operation="extend",
                audio_id=upload.audio_id,
                duration=30
            )
            ```
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "audio/mpeg")}

            data = await self._base_client.post(
                "/producer/v1/music/upload",
                files=files,
                timeout=120,
            )

        return ProducerUploadResponse(**data)

    async def download_music(
        self,
        clip_id: str,
        *,
        format: str = "mp3",
    ) -> ProducerDownloadResponse:
        """Download music in specified format.

        Args:
            clip_id: Clip ID to download
            format: Audio format (mp3 or wav)

        Returns:
            Download response with URL

        Example:
            ```python
            download = await client.producer.download_music(
                clip_id="clip_abc123",
                format="wav"
            )
            print(f"Download URL: {download.download_url}")
            ```
        """
        request = ProducerDownloadRequest(clip_id=clip_id, format=format)

        data = await self._base_client.post(
            "/producer/v1/music/download",
            json=request.model_dump(),
        )

        return ProducerDownloadResponse(**data)

    async def get_task(
        self,
        task_id: str,
    ) -> ProducerTaskResponse:
        """Get task status and result.

        Args:
            task_id: Task ID to check

        Returns:
            Task response

        Example:
            ```python
            result = await client.producer.get_task("task_abc123")
            if result.status == "completed":
                print(f"Audio URL: {result.clips[0].audio_url}")
            ```
        """
        data = await self._base_client.get(
            "/producer/v1/music/get",
            params={"task_id": task_id},
        )

        return ProducerTaskResponse(**data)

    async def wait_for_completion(
        self,
        task_id: str,
        *,
        max_attempts: int | None = None,
        interval: float | None = None,
        timeout: int | None = None,
    ) -> ProducerTaskResponse:
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

    async def __aenter__(self) -> "ProducerClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
