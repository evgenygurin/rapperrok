"""Data models for Nuro API."""

from pydantic import BaseModel, Field

from ..common.models import MusicResult, TaskResponse


class NuroCreateRequest(BaseModel):
    """Request to create music with Nuro."""

    prompt: str = Field(..., description="Music generation prompt")
    duration: int = Field(
        default=240,
        ge=30,
        le=240,
        description="Duration in seconds (30-240)",
    )
    style: str | None = Field(None, description="Musical style")
    has_vocals: bool = Field(default=True, description="Include vocals")
    webhook_url: str | None = None


class NuroMusicResponse(MusicResult):
    """Extended music result for Nuro."""

    model_version: str = Field(default="Nuro-1.0", description="Nuro model version")
    has_vocals: bool | None = None
    generation_time: int | None = Field(None, description="Generation time in seconds")


class NuroTaskResponse(TaskResponse):
    """Nuro-specific task response."""

    clips: list[NuroMusicResponse] = Field(default_factory=list)
