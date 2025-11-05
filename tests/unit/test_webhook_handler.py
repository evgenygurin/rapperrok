"""Unit tests for webhook handler."""

import pytest

from rapperrok.webhooks import WebhookEvent, WebhookHandler


@pytest.mark.asyncio
async def test_webhook_event_parsing():
    """Test webhook event parsing."""
    payload = {
        "event_type": "task.completed",
        "task_id": "task_123",
        "status": "completed",
        "model": "suno",
        "audio_url": "https://example.com/audio.mp3",
    }

    handler = WebhookHandler()
    event = handler.parse_event(payload)

    assert isinstance(event, WebhookEvent)
    assert event.event_type == "task.completed"
    assert event.task_id == "task_123"
    assert event.status.value == "completed"


@pytest.mark.asyncio
async def test_webhook_handler_registration():
    """Test webhook handler registration."""
    handler = WebhookHandler(secret="test_secret")
    called = []

    @handler.on("task.completed")
    async def handle_completed(event):
        called.append(event.event_type)

    assert "task.completed" in handler._event_handlers
    assert len(handler._event_handlers["task.completed"]) == 1


@pytest.mark.asyncio
async def test_webhook_dispatch():
    """Test webhook event dispatching."""
    handler = WebhookHandler()
    events_received = []

    @handler.on("task.completed")
    async def handle_completed(event):
        events_received.append(event)

    event = WebhookEvent(
        event_type="task.completed",
        task_id="task_123",
        status="completed",
    )

    await handler.dispatch(event)

    assert len(events_received) == 1
    assert events_received[0].task_id == "task_123"
