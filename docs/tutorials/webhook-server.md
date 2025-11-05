# Tutorial: Setting Up a Webhook Server

Learn how to set up a webhook server for async music generation notifications.

See the [Webhook Integration Guide](../guides/webhooks.md) for complete webhook documentation.

## Quick Example (FastAPI)

```python
from fastapi import FastAPI, Request
from rapperrok.webhooks import WebhookHandler

app = FastAPI()
handler = WebhookHandler(secret="your_secret")

@app.post("/webhooks/aimusic")
async def webhook_handler(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if not handler.verify_signature(payload, signature):
        return {"error": "Invalid signature"}, 401

    event = handler.parse_event(payload)

    if event.status == "completed":
        print(f"Music ready: {event.audio_url}")

    return {"status": "ok"}
```

See [Webhook Guide](../guides/webhooks.md) for full documentation.
