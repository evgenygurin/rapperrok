"""Common utilities and base classes."""

from .base import BaseAPIClient
from .exceptions import (
    AIMusicAPIError,
    AuthenticationError,
    InsufficientCreditsError,
    InvalidParameterError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    TaskFailedError,
    TimeoutError,
    ValidationError,
    WebhookError,
)
from .models import (
    AudioFormat,
    BaseResponse,
    CreditsInfo,
    ErrorResponse,
    MusicMetadata,
    MusicModel,
    MusicResult,
    PollConfig,
    RetryConfig,
    TaskResponse,
    TaskResult,
    TaskStatus,
    VoiceGender,
    WebhookConfig,
)
from .utils import (
    download_audio,
    download_file,
    estimate_credits,
    format_duration,
    parse_clip_id,
    sanitize_filename,
    validate_audio_url,
    verify_webhook_signature,
)

__all__ = [
    # Base client
    "BaseAPIClient",
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
    "WebhookError",
    # Models
    "AudioFormat",
    "BaseResponse",
    "CreditsInfo",
    "ErrorResponse",
    "MusicMetadata",
    "MusicModel",
    "MusicResult",
    "PollConfig",
    "RetryConfig",
    "TaskResponse",
    "TaskResult",
    "TaskStatus",
    "VoiceGender",
    "WebhookConfig",
    # Utils
    "download_audio",
    "download_file",
    "estimate_credits",
    "format_duration",
    "parse_clip_id",
    "sanitize_filename",
    "validate_audio_url",
    "verify_webhook_signature",
]
