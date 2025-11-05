# API Reference Overview

Complete API reference for RapperRok Python client.

## Client

Main entry point for all API operations:

```python
from rapperrok import AIMusicClient

client = AIMusicClient(api_key="your_key")
```

See [Client Reference](client.md) for complete documentation.

## API Modules

### Suno V4

Studio-quality music generation with vocals, stems, personas, and more.

**Key Methods:**

- `create_music()` - Generate music from description
- `create_music_with_lyrics()` - Generate with custom lyrics
- `extend_music()` - Extend existing tracks
- `concat_music()` - Merge multiple clips
- `stems_basic()` - 2-track stem separation
- `stems_full()` - 12-track stem separation
- `create_persona()` - Train custom voice model
- `get_wav()` - Export to WAV format
- `get_midi()` - Export MIDI data

[→ Suno API Reference](suno.md)

### Producer (FUZZ-2.0)

Fast music generation in 30 seconds.

**Key Methods:**

- `create_music()` - Create, extend, cover, replace operations
- `upload_music()` - Upload audio files
- `download_music()` - Download in MP3/WAV

[→ Producer API Reference](producer.md)

### Nuro

Full-length songs up to 4 minutes.

**Key Methods:**

- `create_vocal_music()` - Generate with vocals
- `create_instrumental_music()` - Generate instrumentals
- `get_music()` - Get task status

[→ Nuro API Reference](nuro.md)

### Webhooks

Handle async notifications.

**Key Classes:**

- `WebhookHandler` - Verify and parse webhooks
- `WebhookEvent` - Event data structure

[→ Webhook API Reference](webhooks.md)

## Common Module

Shared utilities and base classes.

**Key Classes:**

- `RetryConfig` - Configure retry behavior
- `BaseHTTPClient` - Base HTTP client
- Utility functions

[→ Common API Reference](common.md)

## Exceptions

Error handling and exception types.

**Key Exceptions:**

- `AIMusicAPIError` - Base exception
- `AuthenticationError` - Auth failures
- `RateLimitError` - Rate limiting
- `InsufficientCreditsError` - Not enough credits
- `TaskFailedError` - Generation failed

[→ Exceptions Reference](exceptions.md)

## Quick Reference

### Creating Music

```python
# Suno V4
result = await client.suno.create_music(
    description="upbeat pop song",
    duration=60,
    voice_gender="female"
)

# Producer
result = await client.producer.create_music(
    description="energetic EDM",
    operation="create",
    duration=60
)

# Nuro
result = await client.nuro.create_vocal_music(
    prompt="epic orchestral",
    duration=240
)
```

### Checking Status

```python
status = await client.suno.get_music(task_id="abc123")

if status.status == "completed":
    print(status.clips[0].audio_url)
```

### Managing Credits

```python
credits = await client.get_credits()
print(f"Available: {credits.available}")
```

## Type Definitions

All API responses use Pydantic models for type safety:

```python
from rapperrok.suno.models import (
    CreateMusicResponse,
    MusicClip,
    StemsBasicResponse,
    StemsFullResponse
)

result: CreateMusicResponse = await client.suno.create_music(...)
clip: MusicClip = result.clips[0]
```

See individual API references for complete type definitions.

## Next Steps

- [Client Reference](client.md) - Main client documentation
- [Suno Reference](suno.md) - Suno API methods
- [Producer Reference](producer.md) - Producer API methods
- [Nuro Reference](nuro.md) - Nuro API methods
