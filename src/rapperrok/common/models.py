"""Common data models for AI Music API."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class TaskStatus(str, Enum):
    """Status of music generation task."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VoiceGender(str, Enum):
    """Voice gender for vocal generation."""

    MALE = "male"
    FEMALE = "female"
    RANDOM = "random"


class AudioFormat(str, Enum):
    """Supported audio formats."""

    MP3 = "mp3"
    WAV = "wav"


class MusicModel(str, Enum):
    """Supported music generation models."""

    SUNO = "suno"
    SUNO_V4 = "suno-v4"
    PRODUCER = "producer"
    NURO = "nuro"
    RIFFUSION = "riffusion"
    UDIO = "udio"


class BaseResponse(BaseModel):
    """Base response model."""

    success: bool = True
    message: str | None = None


class TaskResponse(BaseResponse):
    """Response with task ID for async operations."""

    task_id: str = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    estimated_time: int | None = Field(
        None,
        description="Estimated completion time in seconds",
    )


class MusicMetadata(BaseModel):
    """Metadata for generated music."""

    title: str | None = None
    duration: int | None = Field(None, description="Duration in seconds")
    style: str | None = None
    description: str | None = None
    lyrics: str | None = None
    model: MusicModel | None = None
    created_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)


class MusicResult(BaseModel):
    """Result of music generation."""

    clip_id: str = Field(..., description="Unique clip identifier")
    audio_url: HttpUrl | str = Field(..., description="URL to audio file")
    video_url: HttpUrl | str | None = Field(
        None,
        description="URL to video file (if available)",
    )
    image_url: HttpUrl | str | None = Field(
        None,
        description="URL to cover image",
    )
    metadata: MusicMetadata = Field(default_factory=MusicMetadata)
    status: TaskStatus = TaskStatus.COMPLETED


class TaskResult(BaseResponse):
    """Complete task result with music data."""

    task_id: str
    status: TaskStatus
    music: list[MusicResult] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None


class CreditsInfo(BaseModel):
    """Information about API credits."""

    credits: int = Field(..., description="Available credits")
    extra_credits: int = Field(0, description="Extra credits purchased")
    reset_date: datetime | None = Field(
        None,
        description="Date when monthly quota resets",
    )


class RetryConfig(BaseModel):
    """Configuration for retry logic."""

    max_retries: int = Field(default=3, ge=0, le=10)
    initial_delay: float = Field(default=1.0, ge=0.1, le=10.0)
    max_delay: float = Field(default=60.0, ge=1.0, le=300.0)
    exponential_base: float = Field(default=2.0, ge=1.0, le=5.0)
    retry_statuses: set[int] = Field(
        default_factory=lambda: {408, 429, 500, 502, 503, 504},
    )


class PollConfig(BaseModel):
    """Configuration for polling operations."""

    max_attempts: int = Field(default=60, ge=1, le=600)
    interval: float = Field(default=5.0, ge=1.0, le=30.0)
    timeout: int | None = Field(default=300, ge=10, le=3600)


class WebhookConfig(BaseModel):
    """Webhook configuration."""

    url: HttpUrl | str = Field(..., description="Webhook endpoint URL")
    secret: str | None = Field(None, description="Webhook signing secret")
    events: list[str] = Field(
        default_factory=lambda: ["task.completed", "task.failed"],
    )


class ErrorResponse(BaseModel):
    """Error response from API."""

    error: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Error code")
    details: dict[str, Any] | None = Field(None, description="Additional error details")
    request_id: str | None = Field(None, description="Request ID for debugging")
