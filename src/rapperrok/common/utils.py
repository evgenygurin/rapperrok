"""Utility functions for AI Music API client."""

import hashlib
import hmac
import json
import logging
from pathlib import Path
from typing import Any

import aiofiles
import httpx

logger = logging.getLogger(__name__)


async def download_file(
    url: str,
    output_path: str | Path,
    *,
    chunk_size: int = 8192,
    timeout: int = 120,
) -> Path:
    """Download file from URL.

    Args:
        url: URL to download from
        output_path: Path to save file
        chunk_size: Size of chunks to download
        timeout: Download timeout in seconds

    Returns:
        Path to downloaded file

    Raises:
        Exception: On download errors
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading {url} to {output_path}")

    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()

            async with aiofiles.open(output_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size):
                    await f.write(chunk)

    logger.info(f"Downloaded {output_path.stat().st_size} bytes")
    return output_path


async def download_audio(
    url: str,
    output_path: str | Path,
    *,
    timeout: int = 120,
) -> Path:
    """Download audio file from URL.

    Args:
        url: Audio URL
        output_path: Path to save audio file
        timeout: Download timeout

    Returns:
        Path to downloaded audio file
    """
    return await download_file(url, output_path, timeout=timeout)


def verify_webhook_signature(
    payload: str | dict[str, Any],
    signature: str,
    secret: str,
) -> bool:
    """Verify webhook signature.

    Args:
        payload: Webhook payload (string or dict)
        signature: Signature from X-Webhook-Signature header
        secret: Webhook secret

    Returns:
        True if signature is valid
    """
    if isinstance(payload, dict):
        payload_str = json.dumps(payload, separators=(",", ":"))
    else:
        payload_str = payload

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration (e.g., "2m 30s", "1h 15m 30s")
    """
    if seconds < 60:
        return f"{seconds}s"

    minutes = seconds // 60
    seconds = seconds % 60

    if minutes < 60:
        return f"{minutes}m {seconds}s" if seconds else f"{minutes}m"

    hours = minutes // 60
    minutes = minutes % 60

    parts = [f"{hours}h"]
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for filesystem
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove leading/trailing spaces and dots
    filename = filename.strip(". ")

    return filename or "unnamed"


def parse_clip_id(identifier: str) -> str:
    """Parse clip ID from various formats.

    Args:
        identifier: Clip ID, URL, or other identifier

    Returns:
        Extracted clip ID
    """
    # If it's a URL, extract clip ID
    if "://" in identifier:
        parts = identifier.split("/")
        for i, part in enumerate(parts):
            if part == "clip" and i + 1 < len(parts):
                return parts[i + 1]

    # Otherwise assume it's already a clip ID
    return identifier


def estimate_credits(
    model: str,
    operation: str,
    duration: int | None = None,
) -> int:
    """Estimate credits required for operation.

    Args:
        model: Model name (suno, producer, nuro, etc.)
        operation: Operation type (create, extend, etc.)
        duration: Duration in seconds

    Returns:
        Estimated credits required
    """
    # Credit costs based on API documentation
    costs = {
        "suno": {
            "create": 10,
            "extend": 10,
            "concat": 5,
            "cover": 10,
            "stems_basic": 20,
            "stems_full": 50,
            "persona": 50,
            "wav": 10,
            "midi": 5,
        },
        "producer": {
            "create": 10,
            "extend": 10,
            "cover": 10,
            "replace": 10,
            "swap_vocal": 15,
            "swap_instrumental": 15,
            "variation": 10,
        },
        "nuro": {
            "vocal": 20,
            "instrumental": 15,
        },
        "riffusion": {
            "create": 5,
            "extend": 5,
            "cover": 5,
        },
    }

    model_lower = model.lower()
    operation_lower = operation.lower()

    return costs.get(model_lower, {}).get(operation_lower, 10)


def validate_audio_url(url: str) -> bool:
    """Validate if URL points to an audio file.

    Args:
        url: URL to validate

    Returns:
        True if URL appears to be valid audio URL
    """
    audio_extensions = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"}
    url_lower = url.lower()

    return any(url_lower.endswith(ext) or ext in url_lower for ext in audio_extensions)


def chunks(lst: list[Any], n: int) -> list[list[Any]]:
    """Split list into chunks of size n.

    Args:
        lst: List to split
        n: Chunk size

    Returns:
        List of chunks
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]
