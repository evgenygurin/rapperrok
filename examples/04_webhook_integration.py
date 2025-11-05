"""Webhook integration examples."""

import asyncio

from rapperrok import AIMusicClient, WebhookHandler


# Example 1: Basic webhook handler
def basic_webhook_example():
    """Basic webhook handler setup."""
    print("\n=== Basic Webhook Handler ===\n")

    handler = WebhookHandler(secret="your_webhook_secret")

    @handler.on("task.completed")
    async def handle_completed(event):
        print(f"Task completed: {event.task_id}")
        print(f"Audio URL: {event.audio_url}")
        print(f"Model: {event.model}")

    @handler.on("task.failed")
    async def handle_failed(event):
        print(f"Task failed: {event.task_id}")
        print(f"Error: {event.error}")

    print("Webhook handlers registered!")
    return handler


# Example 2: FastAPI webhook endpoint
def fastapi_webhook_example():
    """FastAPI webhook endpoint example."""
    print("\n=== FastAPI Webhook Integration ===\n")

    code = '''
from fastapi import FastAPI, Request, HTTPException
from rapperrok import WebhookHandler

app = FastAPI()
webhook_handler = WebhookHandler(secret="your_webhook_secret")

@webhook_handler.on("task.completed")
async def handle_completed(event):
    print(f"Music ready: {event.audio_url}")
    # Store in database, notify user, etc.

@webhook_handler.on("task.failed")
async def handle_failed(event):
    print(f"Generation failed: {event.error}")
    # Log error, notify user, etc.

@app.post("/webhooks/aimusic")
async def aimusic_webhook(request: Request):
    """Handle AI Music API webhooks."""
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    try:
        # Verify signature
        if not webhook_handler.verify_signature(payload, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Handle event
        await webhook_handler.handle_request(payload, signature)

        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    print("FastAPI webhook endpoint code:")
    print(code)


# Example 3: Using webhooks with music generation
async def webhook_with_generation():
    """Example: Generate music with webhook notification."""
    print("\n=== Music Generation with Webhooks ===\n")

    webhook_url = "https://your-domain.com/webhooks/aimusic"

    async with AIMusicClient() as client:
        # Generate music with webhook notification
        result = await client.suno.create_music(
            description="epic cinematic trailer music",
            duration=60,
            webhook_url=webhook_url,
        )

        print(f"Task ID: {result.task_id}")
        print(f"Status: {result.status}")
        print(
            f"Webhook will be called at {webhook_url} when complete"
        )


# Example 4: Manual webhook processing
async def manual_webhook_processing():
    """Example: Manually process webhook payload."""
    print("\n=== Manual Webhook Processing ===\n")

    # Simulate received webhook payload
    payload = {
        "event_type": "task.completed",
        "task_id": "task_abc123",
        "status": "completed",
        "model": "suno",
        "clip_id": "clip_xyz789",
        "audio_url": "https://cdn.aimusicapi.com/music/clip_xyz789.mp3",
        "video_url": "https://cdn.aimusicapi.com/video/clip_xyz789.mp4",
        "timestamp": "2025-01-15T10:30:00Z",
    }

    signature = "fake_signature_for_example"

    handler = WebhookHandler(secret="your_webhook_secret")

    @handler.on("task.completed")
    async def handle_event(event):
        print(f"Received event: {event.event_type}")
        print(f"Task: {event.task_id}")
        print(f"Clip: {event.clip_id}")
        print(f"Audio: {event.audio_url}")

    # Process webhook (in production, verify signature first)
    try:
        event = handler.parse_event(payload)
        await handler.dispatch(event)
    except Exception as e:
        print(f"Error processing webhook: {e}")


async def main():
    """Run webhook examples."""
    basic_webhook_example()
    fastapi_webhook_example()
    await webhook_with_generation()
    await manual_webhook_processing()


if __name__ == "__main__":
    asyncio.run(main())
