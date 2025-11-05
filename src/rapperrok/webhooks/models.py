"""Webhook data models."""

from datetime import datetime

from pydantic import BaseModel, Field

from ..common.models import TaskStatus


class WebhookEvent(BaseModel):
    """Webhook event payload."""

    event_type: str = Field(..., description="Event type (task.completed, task.failed)")
    task_id: str = Field(..., description="Task ID")
    status: TaskStatus = Field(..., description="Task status")
    model: str | None = Field(None, description="Model used (suno, producer, nuro)")
    clip_id: str | None = Field(None, description="Generated clip ID")
    audio_url: str | None = Field(None, description="Audio URL")
    video_url: str | None = Field(None, description="Video URL")
    error: str | None = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, str] | None = Field(None, description="Additional metadata")
