# API Endpoints Reference

Complete reference of all AI Music API endpoints organized by model and functionality.

## Table of Contents

- [Base URL & Authentication](#base-url--authentication)
- [Suno API Endpoints](#suno-api-endpoints)
- [Producer API Endpoints](#producer-api-endpoints)
- [Nuro API Endpoints](#nuro-api-endpoints)
- [Riffusion API Endpoints (Deprecated)](#riffusion-api-endpoints-deprecated)
- [Shared Endpoints](#shared-endpoints)
- [Response Formats](#response-formats)

---

## Base URL & Authentication

### Base URL

```
https://api.aimusicapi.ai
```

### Authentication

All API requests require an API key in the Authorization header:

```http
Authorization: Bearer sk_your_api_key_here
```

Get your API key from: [https://aimusicapi.ai/dashboard/apikey](https://aimusicapi.ai/dashboard/apikey)

---

## Suno API Endpoints

### Music Generation

#### POST /v1/suno/create-music

Generate AI-powered music with Suno V4 from text prompts.

**Request:**
```json
{
  "description": "upbeat electronic dance music with strong bass",
  "duration": 30,
  "voice_gender": "female",
  "auto_lyrics": true,
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "status": "pending",
  "estimated_time": 120
}
```

**Credits Cost:** 10 credits

**Documentation:** [Create Music API](https://docs.aimusicapi.ai/create-suno-music.md)

---

#### POST /v1/suno/describe-music

Generate music directly from a short text description.

**Request:**
```json
{
  "description": "a sad piano ballad",
  "duration": 60,
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_xyz789",
  "status": "pending"
}
```

**Credits Cost:** 10 credits

**Documentation:** [Describe to Music API](https://docs.aimusicapi.ai/describe-music.md)

---

#### POST /v1/suno/create-music-with-lyrics

Create music with custom lyrics and style.

**Request:**
```json
{
  "lyrics": "Verse 1: Walking down the street...\nChorus: Life is beautiful...",
  "style": "indie rock, acoustic guitar, drums",
  "title": "My Song",
  "voice_gender": "male"
}
```

**Response:**
```json
{
  "task_id": "task_def456",
  "status": "pending"
}
```

**Credits Cost:** 10 credits

**Documentation:** [Custom Lyrics & Style](https://docs.aimusicapi.ai/custom-lyrics-style.md)

---

### Audio Manipulation

#### POST /v1/suno/extend-music

Extend existing AI-generated music tracks.

**Request:**
```json
{
  "audio_id": "clip_abc123",
  "duration": 60,
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_ext789",
  "status": "pending"
}
```

**Credits Cost:** 10 credits

**Documentation:** [Extend Music API](https://docs.aimusicapi.ai/extend-suno-music.md)

---

#### POST /v1/suno/concat-music

Concatenate multiple music clips into one seamless track.

**Request:**
```json
{
  "clip_ids": ["clip_1", "clip_2", "clip_3"]
}
```

**Response:**
```json
{
  "task_id": "task_concat456",
  "status": "pending"
}
```

**Credits Cost:** 5 credits

**Documentation:** [Concat Music API](https://docs.aimusicapi.ai/concat-suno-music.md)

---

#### POST /v1/suno/cover-music

Create AI-generated cover versions of existing songs.

**Request:**
```json
{
  "audio_url": "https://example.com/song.mp3",
  "style": "jazz version with piano",
  "voice_gender": "female"
}
```

**Response:**
```json
{
  "task_id": "task_cover123",
  "status": "pending"
}
```

**Credits Cost:** 10 credits

**Documentation:** [Cover Music API](https://docs.aimusicapi.ai/cover-suno-music.md)

---

### Audio Separation & Export

#### POST /v1/suno/stems-basic

Split song into 2 tracks: vocals and instrumental.

**Request:**
```json
{
  "song_id": "song_abc123"
}
```

**Response:**
```json
{
  "task_id": "task_stems_basic",
  "status": "pending"
}
```

**Completed Response:**
```json
{
  "status": "completed",
  "vocals_url": "https://cdn.aimusicapi.ai/vocals.mp3",
  "instrumental_url": "https://cdn.aimusicapi.ai/instrumental.mp3"
}
```

**Credits Cost:** 20 credits

**Documentation:** [Stems Basic API](https://docs.aimusicapi.ai/stems-basic.md)

---

#### POST /v1/suno/stems-full

Extract up to 12 individual stems from a song.

**Request:**
```json
{
  "song_id": "song_abc123"
}
```

**Response:**
```json
{
  "task_id": "task_stems_full",
  "status": "pending"
}
```

**Completed Response:**
```json
{
  "status": "completed",
  "stems": {
    "lead_vocals_url": "https://cdn.aimusicapi.ai/lead_vocals.mp3",
    "backing_vocals_url": "https://cdn.aimusicapi.ai/backing_vocals.mp3",
    "drums_url": "https://cdn.aimusicapi.ai/drums.mp3",
    "bass_url": "https://cdn.aimusicapi.ai/bass.mp3",
    "piano_url": "https://cdn.aimusicapi.ai/piano.mp3",
    "guitar_url": "https://cdn.aimusicapi.ai/guitar.mp3",
    "synth_url": "https://cdn.aimusicapi.ai/synth.mp3",
    "strings_url": "https://cdn.aimusicapi.ai/strings.mp3",
    "brass_url": "https://cdn.aimusicapi.ai/brass.mp3",
    "other_url": "https://cdn.aimusicapi.ai/other.mp3",
    "mix_url": "https://cdn.aimusicapi.ai/mix.mp3",
    "background_url": "https://cdn.aimusicapi.ai/background.mp3"
  }
}
```

**Credits Cost:** 50 credits

**Documentation:** [Stems Full API](https://docs.aimusicapi.ai/stems-full.md)

---

#### POST /v1/suno/wav

Convert MP3 to WAV format (lossless).

**Request:**
```json
{
  "song_id": "song_abc123"
}
```

**Response:**
```json
{
  "task_id": "task_wav",
  "status": "pending"
}
```

**Completed Response:**
```json
{
  "status": "completed",
  "wav_url": "https://cdn.aimusicapi.ai/song.wav"
}
```

**Credits Cost:** 10 credits

**Documentation:** [WAV Export API](https://docs.aimusicapi.ai/wav.md)

---

#### GET /v1/suno/get-midi

Get MIDI data from a generated clip.

**Request:**
```http
GET /v1/suno/get-midi?clip_id=clip_abc123
```

**Response:**
```json
{
  "clip_id": "clip_abc123",
  "midi_url": "https://cdn.aimusicapi.ai/song.mid",
  "midi_data": "base64_encoded_midi_data"
}
```

**Credits Cost:** 5 credits

**Documentation:** [Get MIDI API](https://docs.aimusicapi.ai/get-midi.md)

---

### Custom Voices (Personas)

#### POST /v1/suno/create-persona

Create a custom AI voice model from a song URL.

**Request:**
```json
{
  "song_url": "https://example.com/reference-song.mp3",
  "persona_name": "My Custom Voice"
}
```

**Response:**
```json
{
  "task_id": "task_persona",
  "status": "pending",
  "estimated_time": 300
}
```

**Completed Response:**
```json
{
  "status": "completed",
  "persona_id": "persona_abc123",
  "persona_name": "My Custom Voice"
}
```

**Credits Cost:** 50 credits

**Documentation:** [Create Persona API](https://docs.aimusicapi.ai/create-suno-persona.md)

---

#### POST /v1/suno/create-persona-music

Generate music using a custom persona voice.

**Request:**
```json
{
  "persona_id": "persona_abc123",
  "description": "upbeat pop song",
  "lyrics": "Verse 1: ...",
  "duration": 60
}
```

**Response:**
```json
{
  "task_id": "task_persona_music",
  "status": "pending"
}
```

**Credits Cost:** 10 credits

**Documentation:** [Create Persona Music API](https://docs.aimusicapi.ai/create-suno-persona-music.md)

---

### Upload & Retrieve

#### POST /v1/suno/upload-music

Upload your own music for AI processing.

**Request (multipart/form-data):**
```http
POST /v1/suno/upload-music
Content-Type: multipart/form-data

file: [audio file]
```

**Response:**
```json
{
  "audio_id": "uploaded_abc123",
  "duration": 180,
  "format": "mp3"
}
```

**Credits Cost:** Free (upload only)

**Documentation:** [Upload Music API](https://docs.aimusicapi.ai/upload-suno-music.md)

---

#### GET /v1/suno/get-music

Retrieve generated music details by task ID.

**Request:**
```http
GET /v1/suno/get-music?task_id=task_abc123
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "clips": [
    {
      "id": "clip_1",
      "audio_url": "https://cdn.aimusicapi.ai/clip_1.mp3",
      "video_url": "https://cdn.aimusicapi.ai/clip_1.mp4",
      "title": "Generated Song",
      "duration": 120,
      "metadata": {
        "style": "electronic",
        "voice_gender": "female"
      }
    }
  ]
}
```

**Credits Cost:** Free (polling)

**Documentation:** [Get Music API](https://docs.aimusicapi.ai/get-suno-music.md)

---

## Producer API Endpoints

### Music Generation

#### POST /v1/producer/create-music

Generate, extend, cover, or manipulate music with Producer (FUZZ-2.0).

**Create New Music:**
```json
{
  "operation": "create",
  "description": "energetic EDM track with drops",
  "duration": 60,
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Extend Music:**
```json
{
  "operation": "extend",
  "audio_id": "clip_xyz",
  "duration": 30
}
```

**Cover Music:**
```json
{
  "operation": "cover",
  "audio_id": "clip_xyz",
  "style": "jazz version"
}
```

**Replace Section:**
```json
{
  "operation": "replace",
  "audio_id": "clip_xyz",
  "start_time": 30,
  "end_time": 45,
  "description": "guitar solo"
}
```

**Swap Vocals:**
```json
{
  "operation": "swap_vocals",
  "audio_id": "clip_xyz",
  "voice_description": "female pop vocals"
}
```

**Swap Instrumentals:**
```json
{
  "operation": "swap_instrumentals",
  "audio_id": "clip_xyz",
  "instrumental_description": "acoustic guitar backing"
}
```

**Create Variation:**
```json
{
  "operation": "variation",
  "audio_id": "clip_xyz",
  "variation_type": "style"
}
```

**Response:**
```json
{
  "task_id": "task_producer_123",
  "status": "pending",
  "estimated_time": 30
}
```

**Credits Cost:**
- Create/Extend/Cover/Replace/Variation: 10 credits
- Swap Vocals/Instrumentals: 15 credits

**Documentation:**
- [Create Producer Music API](https://docs.aimusicapi.ai/create-producer-music.md)
- [Producer API Examples](https://docs.aimusicapi.ai/producer-api-examples.md)

---

### Upload & Download

#### POST /v1/producer/upload-music

Upload music to Producer API.

**Request (multipart/form-data):**
```http
POST /v1/producer/upload-music
Content-Type: multipart/form-data

file: [audio file]
```

**Response:**
```json
{
  "audio_id": "producer_audio_abc123",
  "clip_id": "clip_xyz",
  "duration": 120
}
```

**Credits Cost:** Free (upload only)

**Documentation:** [Upload Music Producer](https://docs.aimusicapi.ai/upload-music-producer.md)

---

#### GET /v1/producer/download

Download music files in specified format (mp3/wav).

**Request:**
```http
GET /v1/producer/download?clip_id=clip_xyz&format=wav
```

**Response:**
```json
{
  "clip_id": "clip_xyz",
  "format": "wav",
  "download_url": "https://cdn.aimusicapi.ai/clip_xyz.wav"
}
```

**Credits Cost:** Free (download only, format conversion included in generation)

**Documentation:** [Download Producer Music](https://docs.aimusicapi.ai/download-producer-music.md)

---

### Task Status

#### GET /v1/producer/get-music

Query task status and retrieve generated music.

**Request:**
```http
GET /v1/producer/get-music?task_id=task_producer_123
```

**Response:**
```json
{
  "task_id": "task_producer_123",
  "status": "completed",
  "audio_url": "https://cdn.aimusicapi.ai/audio.mp3",
  "video_url": "https://cdn.aimusicapi.ai/video.mp4",
  "metadata": {
    "duration": 60,
    "operation": "create",
    "model": "FUZZ-2.0"
  }
}
```

**Credits Cost:** Free (polling)

**Documentation:** [Get Producer Music](https://docs.aimusicapi.ai/get-producer-music.md)

---

## Nuro API Endpoints

### Music Generation

#### POST /v1/nuro/create-vocal-music

Generate vocal music with Nuro (up to 4 minutes).

**Request:**
```json
{
  "prompt": "epic orchestral soundtrack with choir",
  "duration": 240,
  "style": "cinematic",
  "voice_gender": "mixed",
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_nuro_vocal",
  "status": "pending",
  "estimated_time": 30
}
```

**Credits Cost:** 20 credits

**Documentation:** [Create Vocal Music - Nuro](https://docs.aimusicapi.ai/create-vocal-music-nuro.md)

---

#### POST /v1/nuro/create-instrumental-music

Generate instrumental-only music with Nuro.

**Request:**
```json
{
  "prompt": "ambient electronic atmosphere for meditation",
  "duration": 180,
  "style": "ambient",
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "task_id": "task_nuro_instrumental",
  "status": "pending",
  "estimated_time": 30
}
```

**Credits Cost:** 15 credits

**Documentation:** [Create Instrumental Music - Nuro](https://docs.aimusicapi.ai/create-instrument-music-nuro.md)

---

### Task Status

#### GET /v1/nuro/get-music

Retrieve generated Nuro music by task ID.

**Request:**
```http
GET /v1/nuro/get-music?task_id=task_nuro_vocal
```

**Response:**
```json
{
  "task_id": "task_nuro_vocal",
  "status": "completed",
  "audio_url": "https://cdn.aimusicapi.ai/nuro_song.mp3",
  "duration": 240,
  "metadata": {
    "prompt": "epic orchestral soundtrack with choir",
    "style": "cinematic",
    "model": "nuro"
  }
}
```

**Credits Cost:** Free (polling)

**Documentation:** [Get Music - Nuro](https://docs.aimusicapi.ai/get-music-nuro.md)

---

## Riffusion API Endpoints (Deprecated)

⚠️ **Riffusion API is deprecated.** Use Suno V4 or Producer instead for new projects.

### Legacy Endpoints

| Endpoint | Replacement |
|----------|-------------|
| POST /v1/riffusion/create-music-with-lyrics | ➡️ Suno: `/v1/suno/create-music-with-lyrics` |
| POST /v1/riffusion/create-music-with-description | ➡️ Producer: `/v1/producer/create-music` |
| POST /v1/riffusion/cover-music | ➡️ Producer: `/v1/producer/create-music` (operation="cover") |
| POST /v1/riffusion/extend-music | ➡️ Suno: `/v1/suno/extend-music` |
| POST /v1/riffusion/replace-music-section | ➡️ Producer: `/v1/producer/create-music` (operation="replace") |
| POST /v1/riffusion/swap-music-sound | ➡️ Producer: `/v1/producer/create-music` (operation="swap_instrumentals") |
| POST /v1/riffusion/swap-music-vocals | ➡️ Producer: `/v1/producer/create-music` (operation="swap_vocals") |
| POST /v1/riffusion/upload-music | ➡️ Suno or Producer upload endpoints |
| GET /v1/riffusion/get-music | ➡️ Suno or Producer get endpoints |

**Documentation:** [Riffusion API Instructions](https://docs.aimusicapi.ai/riffusion-api-instructions.md)

---

## Shared Endpoints

### Lyrics Generation

#### POST /v1/lyrics/generate

Generate song lyrics using AI.

**Request:**
```json
{
  "prompt": "a song about friendship and adventure",
  "style": "pop",
  "num_variations": 3
}
```

**Response:**
```json
{
  "variations": [
    {
      "lyrics": "Verse 1: ...\nChorus: ...\nVerse 2: ...",
      "structure": "verse-chorus-verse-chorus-bridge-chorus"
    }
  ]
}
```

**Credits Cost:** 5 credits

**Documentation:** [Lyrics Generation](https://docs.aimusicapi.ai/lyrics-generation.md)

---

### Credits Management

#### GET /v1/credits

Check available API credits.

**Request:**
```http
GET /v1/credits
```

**Response:**
```json
{
  "total": 1000,
  "used": 250,
  "available": 750,
  "subscription": {
    "tier": "pro",
    "monthly_credits": 1000,
    "renewal_date": "2025-12-01"
  }
}
```

**Credits Cost:** Free

**Documentation:** [Get Credits](https://docs.aimusicapi.ai/get-credits.md)

---

## Response Formats

### Task Response (Pending)

```json
{
  "task_id": "task_abc123",
  "status": "pending",
  "estimated_time": 120,
  "created_at": "2025-11-05T10:30:00Z"
}
```

### Task Response (Processing)

```json
{
  "task_id": "task_abc123",
  "status": "processing",
  "progress": 45,
  "estimated_remaining": 60
}
```

### Task Response (Completed)

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "clips": [
    {
      "id": "clip_1",
      "audio_url": "https://cdn.aimusicapi.ai/clip_1.mp3",
      "video_url": "https://cdn.aimusicapi.ai/clip_1.mp4",
      "title": "Generated Song",
      "duration": 120,
      "metadata": {}
    }
  ],
  "completed_at": "2025-11-05T10:32:00Z"
}
```

### Task Response (Failed)

```json
{
  "task_id": "task_abc123",
  "status": "failed",
  "error": {
    "code": "insufficient_credits",
    "message": "Not enough credits to complete this operation",
    "details": {
      "required": 10,
      "available": 5
    }
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request parameters",
    "details": {
      "field": "duration",
      "issue": "Duration must be between 10 and 240 seconds"
    }
  }
}
```

---

## Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created (task initiated) |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid API key |
| 402 | Payment Required | Insufficient credits |
| 404 | Not Found | Task or resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Rate Limiting

### Rate Limits by Tier

| Tier | Requests/Minute | Concurrent Tasks |
|------|----------------|------------------|
| Free | 10 | 2 |
| Starter | 30 | 5 |
| Pro | 60 | 10 |
| Enterprise | Custom | Custom |

### Rate Limit Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1699200000
```

### Retry Strategy

When rate limited (429 response), implement exponential backoff:

```python
import time

def retry_with_backoff(func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if i == max_retries - 1:
                raise
            wait_time = 2 ** i  # 1s, 2s, 4s, 8s, 16s
            time.sleep(wait_time)
```

---

## Webhooks

### Webhook Configuration

Include `webhook_url` in your request to receive notifications:

```json
{
  "description": "upbeat pop song",
  "webhook_url": "https://your-domain.com/webhook"
}
```

### Webhook Payload

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "clips": [...],
  "timestamp": "2025-11-05T10:32:00Z",
  "signature": "sha256_hmac_signature"
}
```

### Webhook Signature Verification

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

**Documentation:** [Webhook Integration Guide](https://docs.aimusicapi.ai/webhook-guide.md)

---

## Best Practices

### 1. Always Check Credits First

```python
credits = await client.get_credits()
if credits.available < 10:
    print("Insufficient credits")
```

### 2. Use Webhooks for Long Tasks

```python
result = await client.suno.create_music(
    description="...",
    webhook_url="https://your-domain.com/webhook"
)
# Don't poll - wait for webhook notification
```

### 3. Implement Retry Logic

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    retry_config=RetryConfig(
        max_retries=5,
        initial_delay=2.0
    )
)
```

### 4. Handle Errors Gracefully

```python
try:
    result = await client.suno.create_music(...)
except InsufficientCreditsError:
    # Handle insufficient credits
except RateLimitError:
    # Handle rate limiting
except AIMusicAPIError:
    # Handle other errors
```

### 5. Download Important Files

Generated URLs may expire after 24-48 hours. Download important files immediately:

```python
from rapperrok.utils import download_audio

await download_audio(
    url=music.audio_url,
    output_path="my_song.mp3"
)
```

---

**Last Updated**: November 2025
**API Version**: v1
**Base URL**: `https://api.aimusicapi.ai`
