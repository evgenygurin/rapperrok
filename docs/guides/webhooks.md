# Webhook Integration Guide

Learn how to set up and use webhooks for async notifications when music generation tasks complete.

## Overview

Webhooks provide real-time notifications when long-running tasks complete, avoiding the need for polling.

**Benefits:**

- ⚡ Instant notifications when tasks complete
- 🔒 Secure signature verification
- 📊 Detailed event data
- 🚀 Better performance than polling
- 💰 No credit cost for webhook deliveries

## Quick Start

### 1. Set Up Webhook Handler

```python
from rapperrok.webhooks import WebhookHandler

handler = WebhookHandler(secret="your_webhook_secret")
```

### 2. Create Webhook Endpoint

=== "FastAPI"

    ```python
    from fastapi import FastAPI, Request, HTTPException
    from rapperrok.webhooks import WebhookHandler

    app = FastAPI()
    handler = WebhookHandler(secret="your_webhook_secret")

    @app.post("/webhooks/aimusic")
    async def handle_webhook(request: Request):
        # Get payload and signature
        payload = await request.json()
        signature = request.headers.get("X-Webhook-Signature")

        # Verify signature
        if not handler.verify_signature(payload, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse event
        event = handler.parse_event(payload)

        # Handle based on status
        if event.status == "completed":
            print(f"✅ Music ready: {event.audio_url}")
        elif event.status == "failed":
            print(f"❌ Failed: {event.error}")

        return {"status": "ok"}
    ```

=== "Flask"

    ```python
    from flask import Flask, request, jsonify
    from rapperrok.webhooks import WebhookHandler

    app = Flask(__name__)
    handler = WebhookHandler(secret="your_webhook_secret")

    @app.route("/webhooks/aimusic", methods=["POST"])
    def handle_webhook():
        # Get payload and signature
        payload = request.json
        signature = request.headers.get("X-Webhook-Signature")

        # Verify signature
        if not handler.verify_signature(payload, signature):
            return jsonify({"error": "Invalid signature"}), 401

        # Parse event
        event = handler.parse_event(payload)

        # Handle event
        if event.status == "completed":
            print(f"✅ Music ready: {event.audio_url}")
        elif event.status == "failed":
            print(f"❌ Failed: {event.error}")

        return jsonify({"status": "ok"})
    ```

=== "Django"

    ```python
    from django.http import JsonResponse, HttpResponseForbidden
    from django.views.decorators.csrf import csrf_exempt
    from rapperrok.webhooks import WebhookHandler
    import json

    handler = WebhookHandler(secret="your_webhook_secret")

    @csrf_exempt
    def handle_webhook(request):
        if request.method != "POST":
            return HttpResponseForbidden()

        # Get payload and signature
        payload = json.loads(request.body)
        signature = request.headers.get("X-Webhook-Signature")

        # Verify signature
        if not handler.verify_signature(payload, signature):
            return HttpResponseForbidden("Invalid signature")

        # Parse event
        event = handler.parse_event(payload)

        # Handle event
        if event.status == "completed":
            print(f"✅ Music ready: {event.audio_url}")
        elif event.status == "failed":
            print(f"❌ Failed: {event.error}")

        return JsonResponse({"status": "ok"})
    ```

### 3. Register Webhook URL

Configure your webhook URL in the AI Music API dashboard:

1. Go to [AI Music API Dashboard](https://aimusicapi.ai/dashboard/webhooks)
2. Add your webhook URL (e.g., `https://yourdomain.com/webhooks/aimusic`)
3. Set your webhook secret
4. Enable webhook notifications

### 4. Generate Music with Webhook

```python
async with AIMusicClient() as client:
    result = await client.suno.create_music(
        description="upbeat electronic dance music",
        duration=60,
        webhook_url="https://yourdomain.com/webhooks/aimusic",
        wait_for_completion=False  # Don't wait, use webhook
    )

    print(f"Task started: {result.task_id}")
    print("Webhook will notify when complete")
```

## Webhook Events

### Event Structure

```python
{
    "event_type": "music.completed",
    "task_id": "task_abc123",
    "status": "completed",
    "model": "suno",
    "operation": "create_music",
    "audio_url": "https://cdn.aimusicapi.ai/audio.mp3",
    "video_url": "https://cdn.aimusicapi.ai/video.mp4",
    "duration": 60,
    "created_at": "2024-01-01T12:00:00Z",
    "completed_at": "2024-01-01T12:01:30Z"
}
```

### Event Types

#### music.completed

Task completed successfully:

```python
event = handler.parse_event(payload)

if event.event_type == "music.completed":
    print(f"Audio: {event.audio_url}")
    print(f"Video: {event.video_url}")
    print(f"Duration: {event.duration}s")
```

#### music.failed

Task failed:

```python
if event.event_type == "music.failed":
    print(f"Error: {event.error}")
    print(f"Error code: {event.error_code}")
```

#### music.processing

Task is still processing (optional):

```python
if event.event_type == "music.processing":
    print(f"Progress: {event.progress}%")
```

## Security

### Signature Verification

Always verify webhook signatures to ensure authenticity:

```python
from rapperrok.webhooks import WebhookHandler

handler = WebhookHandler(secret="your_webhook_secret")

# Verify signature
payload = request.json
signature = request.headers.get("X-Webhook-Signature")

if not handler.verify_signature(payload, signature):
    # Reject invalid webhooks
    raise HTTPException(status_code=401, detail="Invalid signature")

# Signature valid, process event
event = handler.parse_event(payload)
```

### HTTPS Only

Always use HTTPS for webhook endpoints:

```
✅ https://yourdomain.com/webhooks/aimusic
❌ http://yourdomain.com/webhooks/aimusic
```

### Secret Management

Store webhook secrets securely:

```python
import os
from rapperrok.webhooks import WebhookHandler

# Load from environment variable
webhook_secret = os.getenv("WEBHOOK_SECRET")
handler = WebhookHandler(secret=webhook_secret)
```

## Complete Workflows

### Generate and Process with Webhooks

```python
from fastapi import FastAPI, Request
from rapperrok import AIMusicClient
from rapperrok.webhooks import WebhookHandler
import asyncio

app = FastAPI()
handler = WebhookHandler(secret="your_secret")

# Storage for completed tasks
completed_tasks = {}

@app.post("/webhooks/aimusic")
async def webhook_handler(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if not handler.verify_signature(payload, signature):
        return {"error": "Invalid signature"}, 401

    event = handler.parse_event(payload)

    if event.status == "completed":
        # Store completed task
        completed_tasks[event.task_id] = {
            "audio_url": event.audio_url,
            "video_url": event.video_url,
            "duration": event.duration
        }

        # Process the music
        await process_music(event)

    return {"status": "ok"}

async def process_music(event):
    """Process completed music"""
    print(f"Processing: {event.task_id}")

    # Download the file
    from rapperrok.utils import download_audio
    await download_audio(event.audio_url, f"{event.task_id}.mp3")

    # Your processing logic here
    # - Upload to cloud storage
    # - Send to user
    # - Trigger next workflow step
    # etc.

@app.post("/generate")
async def generate_music(description: str):
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description=description,
            duration=60,
            webhook_url="https://yourdomain.com/webhooks/aimusic",
            wait_for_completion=False
        )

        return {
            "task_id": result.task_id,
            "status": "processing"
        }

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id in completed_tasks:
        return {
            "status": "completed",
            "data": completed_tasks[task_id]
        }
    return {"status": "processing"}
```

### Batch Generation with Webhooks

```python
import asyncio
from collections import defaultdict

# Track batch progress
batch_tasks = defaultdict(list)
batch_callbacks = {}

async def batch_generate_with_webhook(descriptions, batch_id):
    """Generate multiple tracks and wait for all via webhooks"""
    async with AIMusicClient() as client:
        tasks = []

        for desc in descriptions:
            result = await client.suno.create_music(
                description=desc,
                duration=60,
                webhook_url="https://yourdomain.com/webhooks/aimusic",
                wait_for_completion=False
            )
            tasks.append(result.task_id)
            batch_tasks[batch_id].append(result.task_id)

        print(f"Batch {batch_id}: Started {len(tasks)} tasks")
        return tasks

@app.post("/webhooks/aimusic")
async def webhook_handler(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if not handler.verify_signature(payload, signature):
        return {"error": "Invalid signature"}, 401

    event = handler.parse_event(payload)
    task_id = event.task_id

    # Find which batch this task belongs to
    for batch_id, tasks in batch_tasks.items():
        if task_id in tasks:
            # Mark as completed
            tasks.remove(task_id)

            # Check if batch is complete
            if len(tasks) == 0:
                print(f"✅ Batch {batch_id} complete!")

                # Call batch callback if registered
                if batch_id in batch_callbacks:
                    await batch_callbacks[batch_id]()

            break

    return {"status": "ok"}
```

### Retry Failed Webhooks

```python
from datetime import datetime
from typing import Dict

# Track failed webhooks
failed_webhooks: Dict[str, dict] = {}

@app.post("/webhooks/aimusic")
async def webhook_handler(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if not handler.verify_signature(payload, signature):
        return {"error": "Invalid signature"}, 401

    event = handler.parse_event(payload)

    try:
        # Process event
        await process_event(event)

        # Remove from failed list if it was there
        failed_webhooks.pop(event.task_id, None)

    except Exception as e:
        # Store failed webhook for retry
        failed_webhooks[event.task_id] = {
            "event": payload,
            "error": str(e),
            "timestamp": datetime.utcnow(),
            "retry_count": failed_webhooks.get(event.task_id, {}).get("retry_count", 0) + 1
        }
        print(f"❌ Failed to process webhook: {e}")

    return {"status": "ok"}

async def retry_failed_webhooks():
    """Periodically retry failed webhooks"""
    for task_id, data in list(failed_webhooks.items()):
        if data["retry_count"] < 3:  # Max 3 retries
            try:
                event = handler.parse_event(data["event"])
                await process_event(event)
                failed_webhooks.pop(task_id)
                print(f"✅ Retry successful for {task_id}")
            except Exception as e:
                print(f"❌ Retry failed for {task_id}: {e}")
                data["retry_count"] += 1
```

## Testing Webhooks

### Local Testing with ngrok

1. Install ngrok:
   ```bash
   brew install ngrok  # macOS
   # or download from ngrok.com
   ```

2. Start your webhook server locally:
   ```bash
   uvicorn app:app --port 8000
   ```

3. Create ngrok tunnel:
   ```bash
   ngrok http 8000
   ```

4. Use the ngrok URL as your webhook URL:
   ```
   https://abc123.ngrok.io/webhooks/aimusic
   ```

### Mock Webhook Events

```python
import pytest
from rapperrok.webhooks import WebhookHandler

@pytest.fixture
def webhook_handler():
    return WebhookHandler(secret="test_secret")

@pytest.fixture
def completed_event():
    return {
        "event_type": "music.completed",
        "task_id": "test_123",
        "status": "completed",
        "audio_url": "https://example.com/audio.mp3",
        "video_url": "https://example.com/video.mp4"
    }

async def test_webhook_handler(webhook_handler, completed_event):
    # Parse event
    event = webhook_handler.parse_event(completed_event)

    # Verify event
    assert event.status == "completed"
    assert event.task_id == "test_123"
    assert event.audio_url == "https://example.com/audio.mp3"

async def test_signature_verification(webhook_handler, completed_event):
    # Generate signature
    signature = webhook_handler.generate_signature(completed_event)

    # Verify
    assert webhook_handler.verify_signature(completed_event, signature)

    # Invalid signature should fail
    assert not webhook_handler.verify_signature(completed_event, "invalid")
```

## Best Practices

1. **Always verify signatures** to ensure webhook authenticity
2. **Use HTTPS** for webhook endpoints
3. **Return 200 OK quickly** - process in background if needed
4. **Implement retries** for failed webhook processing
5. **Store webhook secrets securely** in environment variables
6. **Log webhook events** for debugging
7. **Handle duplicate events** idempotently
8. **Set timeouts** for webhook processing

## Troubleshooting

### Webhooks Not Received

- Check webhook URL is correct and publicly accessible
- Verify HTTPS is used
- Check firewall/security group settings
- Ensure webhook endpoint returns 200 OK

### Signature Verification Fails

- Verify webhook secret is correct
- Check payload hasn't been modified
- Ensure using the correct signature header

### Missing Event Data

- Check event type matches expected format
- Verify API version compatibility
- Update RapperRok to latest version

## Next Steps

- [Error Handling Guide](error-handling.md) - Handle errors gracefully
- [Advanced Features](advanced.md) - Advanced usage patterns
- [API Reference](../api/webhooks.md) - Complete webhook API docs
