"""Data models for Producer API (FUZZ-2.0 model)."""

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from ..common.models import MusicResult, TaskResponse


ProducerOperation = Literal[
    "create",
    "extend",
    "cover",
    "replace",
    "swap_vocal",
    "swap_instrumental",
    "variation",
]


class ProducerCreateRequest(BaseModel):
    """Request to create music with Producer."""

    operation: ProducerOperation = Field(
        ...,
        description="Operation type: create, extend, cover, replace, swap_vocal, swap_instrumental, variation",
    )
    description: str | None = Field(None, description="Music description for create operation")
    audio_id: str | None = Field(None, description="Audio ID for extend/modify operations")
    audio_url: HttpUrl | str | None = Field(None, description="Audio URL for cover operation")
    duration: int = Field(
        default=60,
        ge=10,
        le=240,
        description="Duration in seconds",
    )
    style: str | None = Field(None, description="Musical style")
    vocal_style: str | None = Field(None, description="Vocal style for swap_vocal")
    instrumental_style: str | None = Field(
        None,
        description="Instrumental style for swap_instrumental",
    )
    replace_section: dict[str, int] | None = Field(
        None,
        description="Section to replace: {start: seconds, end: seconds}",
    )
    variation_intensity: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Variation intensity (0.0-1.0)",
    )
    webhook_url: str | None = Field(None, description="Webhook URL for completion")


class ProducerUploadResponse(BaseModel):
    """Response from upload operation."""

    audio_id: str = Field(..., description="Uploaded audio ID")
    audio_url: HttpUrl | str
    duration: int | None = Field(None, description="Audio duration in seconds")


class ProducerDownloadRequest(BaseModel):
    """Request to download music in specific format."""

    clip_id: str = Field(..., description="Clip ID to download")
    format: Literal["mp3", "wav"] = Field(default="mp3", description="Audio format")


class ProducerDownloadResponse(BaseModel):
    """Response with download URL."""

    clip_id: str
    format: str
    download_url: HttpUrl | str
    file_size: int | None = Field(None, description="File size in bytes")


class ProducerMusicResponse(MusicResult):
    """Extended music result for Producer."""

    model_version: str = Field(default="FUZZ-2.0", description="Producer model version")
    generation_time: int | None = Field(
        None,
        description="Generation time in seconds",
    )
    operation: ProducerOperation | None = None


class ProducerTaskResponse(TaskResponse):
    """Producer-specific task response."""

    clips: list[ProducerMusicResponse] = Field(default_factory=list)
    generation_time: int | None = Field(None, description="Actual generation time")
