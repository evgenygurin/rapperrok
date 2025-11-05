"""RapperRok - Comprehensive Python client for AI Music API.

Supports Suno, Udio, Riffusion, Nuro, and Producer models.
"""

import logging
import os
from typing import Any

from dotenv import load_dotenv

from .common import (
    AIMusicAPIError,
    AuthenticationError,
    BaseAPIClient,
    CreditsInfo,
    InsufficientCreditsError,
    InvalidParameterError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    RetryConfig,
    TaskFailedError,
    TimeoutError,
    ValidationError,
    VoiceGender,
    download_audio,
)
from .nuro import NuroClient
from .producer import ProducerClient
from .suno import SunoClient
from .webhooks import WebhookHandler

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class AIMusicClient:
    """Main client for AI Music API.

    Provides unified access to all music generation models:
    - Suno V4: Most advanced, supports vocals, stems, personas
    - Producer: Fast generation (30s), high quality
    - Nuro: Full-length songs (4 minutes)

    Example:
        ```python
        import asyncio
        from rapperrok import AIMusicClient

        async def main():
            client = AIMusicClient(api_key="your_api_key")

            # Create music with Suno
            result = await client.suno.create_music(
                description="upbeat electronic dance music",
                duration=60
            )

            # Wait for completion
            completed = await client.suno.wait_for_completion(result.task_id)
            print(f"Music URL: {completed.clips[0].audio_url}")

            await client.close()

        asyncio.run(main())
        ```
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 30,
        retry_config: RetryConfig | None = None,
    ) -> None:
        """Initialize AI Music API client.

        Args:
            api_key: AI Music API key (or set AIMUSIC_API_KEY env var)
            base_url: Base API URL (or set AIMUSIC_BASE_URL env var)
            timeout: Default timeout in seconds
            retry_config: Retry configuration

        Raises:
            ValueError: If API key is not provided
        """
        self.api_key = api_key or os.getenv("AIMUSIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide via api_key parameter or AIMUSIC_API_KEY env var"
            )

        self.base_url = base_url or os.getenv(
            "AIMUSIC_BASE_URL",
            "https://api.aimusicapi.ai",
        )
        self.timeout = timeout
        self.retry_config = retry_config

        # Initialize API clients
        self._base_client = BaseAPIClient(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            retry_config=self.retry_config,
        )

        # Initialize model-specific clients
        self.suno = SunoClient(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            retry_config=self.retry_config,
        )

        self.producer = ProducerClient(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            retry_config=self.retry_config,
        )

        self.nuro = NuroClient(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            retry_config=self.retry_config,
        )

    async def get_credits(self) -> CreditsInfo:
        """Get current credit balance.

        Returns:
            Credits information

        Example:
            ```python
            credits = await client.get_credits()
            print(f"Available: {credits.available}")
            print(f"Used: {credits.used}")
            ```
        """
        data = await self._base_client.get("/api/v1/credits")
        return CreditsInfo(**data)

    async def generate_lyrics(
        self,
        prompt: str,
        *,
        num_variations: int = 1,
    ) -> list[str]:
        """Generate song lyrics from prompt.

        Args:
            prompt: Lyrics generation prompt
            num_variations: Number of lyric variations to generate

        Returns:
            List of generated lyrics

        Example:
            ```python
            lyrics_list = await client.generate_lyrics(
                prompt="love song about summer nights",
                num_variations=3
            )
            for lyrics in lyrics_list:
                print(lyrics)
            ```
        """
        data = await self._base_client.post(
            "/api/v1/lyrics/generate",
            json={
                "prompt": prompt,
                "num_variations": num_variations,
            },
        )

        return data.get("lyrics", [])

    async def close(self) -> None:
        """Close all HTTP clients."""
        await self._base_client.close()
        await self.suno.close()
        await self.producer.close()
        await self.nuro.close()

    async def __aenter__(self) -> "AIMusicClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()


__version__ = "0.1.0"

__all__ = [
    # Main client
    "AIMusicClient",
    # Model clients
    "SunoClient",
    "ProducerClient",
    "NuroClient",
    # Common
    "BaseAPIClient",
    "RetryConfig",
    "VoiceGender",
    "CreditsInfo",
    # Exceptions
    "AIMusicAPIError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "InvalidParameterError",
    "NetworkError",
    "RateLimitError",
    "ResourceNotFoundError",
    "TaskFailedError",
    "TimeoutError",
    "ValidationError",
    # Utils
    "download_audio",
    # Webhooks
    "WebhookHandler",
    # Version
    "__version__",
]
