# RapperRok - AI Music API Python Client

<div align="center">

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

Comprehensive Python client for AI Music API supporting **Suno**, **Udio**, **Riffusion**, **Nuro**, and **Producer** models.

[Documentation](https://rapperrok.readthedocs.io) | [Examples](./examples) | [API Reference](https://docs.aimusicapi.ai) | [Models](./docs/MODELS.md) | [Endpoints](./docs/ENDPOINTS.md)

</div>

## Features

### Supported Models

- **Suno V4** - Studio-quality music generation with vocals/instrumentals
- **Producer (FUZZ-2.0)** - High-quality music in 30 seconds
- **Nuro** - Complete 4-minute songs in 30 seconds
- **Riffusion** - Real-time music generation (deprecated)
- **Udio** - Advanced music creation

### Core Capabilities

- **Music Generation**: Create, extend, cover, and remix tracks
- **Vocal Processing**: Swap vocals, create personas, gender control
- **Audio Processing**: Stems separation (basic/full), format conversion (MP3/WAV)
- **Lyrics Generation**: AI-powered lyrics creation
- **MIDI Export**: Extract MIDI data from tracks
- **Webhook Integration**: Async notifications for long-running tasks
- **Credit Management**: Track and manage API credits

### Developer Experience

- **Modern Python**: Python 3.12+ with type hints
- **Async/Await**: Full async support with httpx
- **Type Safe**: Complete type annotations with Pydantic
- **Rich CLI**: Beautiful terminal output with progress tracking
- **Retry Logic**: Automatic retry with exponential backoff
- **Error Handling**: Comprehensive error messages and recovery

## Installation

### Using uv (recommended)

```bash
# Install uv if you don't have it
pip install uv

# Install rapperrok
uv pip install rapperrok

# Or with development dependencies
uv pip install "rapperrok[dev]"
```

### Using pip

```bash
pip install rapperrok

# Or with development dependencies
pip install "rapperrok[dev]"
```

### From source (with uv)

```bash
git clone https://github.com/rapperrok/rapperrok.git
cd rapperrok

# Install with uv (recommended for development)
make dev
# Or manually
uv pip install -e ".[dev]"
```

## Quick Start

### Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# AIMUSIC_API_KEY=your_api_key_here
```

### Basic Usage

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    # Initialize client
    client = AIMusicClient(api_key="your_api_key")

    # Generate music with Suno
    result = await client.suno.create_music(
        description="upbeat electronic dance music with strong bass",
        duration=30,
        voice_gender="female"
    )

    print(f"Task ID: {result.task_id}")
    print(f"Status: {result.status}")

    # Wait for completion and get result
    music = await client.suno.wait_for_completion(result.task_id)
    print(f"Audio URL: {music.audio_url}")
    print(f"Video URL: {music.video_url}")

asyncio.run(main())
```

### CLI Usage

```bash
# Generate music (via uv run if installed from source)
uv run rapperrok suno create --description "jazz piano solo" --duration 60

# Check credits
uv run rapperrok credits

# Get task status
uv run rapperrok suno get --task-id abc123

# Create with custom lyrics
uv run rapperrok suno create --lyrics "path/to/lyrics.txt" --style "rock"
```

## Examples

### Suno: Create Music with Vocals

```python
from rapperrok import AIMusicClient

client = AIMusicClient()

# Create music from description
result = await client.suno.create_music(
    description="emotional piano ballad about lost love",
    duration=120,
    voice_gender="male",
    auto_lyrics=True
)

# Or with custom lyrics
result = await client.suno.create_music_with_lyrics(
    lyrics="Verse 1: Walking down the street...",
    style="indie rock, acoustic guitar, drums",
    title="My Song"
)
```

### Suno: Extend and Concatenate

```python
# Extend existing track
extended = await client.suno.extend_music(
    audio_id="clip_abc123",
    duration=60
)

# Concatenate multiple clips
full_track = await client.suno.concat_music(
    clip_ids=["clip_1", "clip_2", "clip_3"]
)
```

### Suno: Stems Separation

```python
# Basic stems (vocals + instrumental)
stems_basic = await client.suno.stems_basic(song_id="song_abc123")
print(f"Vocals: {stems_basic.vocals_url}")
print(f"Instrumental: {stems_basic.instrumental_url}")

# Full stems (12 tracks)
stems_full = await client.suno.stems_full(song_id="song_abc123")
print(f"Lead Vocals: {stems_full.lead_vocals_url}")
print(f"Drums: {stems_full.drums_url}")
print(f"Bass: {stems_full.bass_url}")
# ... and 9 more stems
```

### Producer: Fast Music Generation

```python
# Create music with Producer (30 seconds generation time)
result = await client.producer.create_music(
    description="energetic EDM track with drops",
    operation="create",
    duration=60
)

# Extend existing track
extended = await client.producer.create_music(
    audio_id="clip_xyz",
    operation="extend",
    duration=30
)
```

### Nuro: Full Songs

```python
# Generate complete 4-minute song
song = await client.nuro.create_vocal_music(
    prompt="epic orchestral soundtrack with choir",
    duration=240,
    style="cinematic"
)

# Instrumental only
instrumental = await client.nuro.create_instrumental_music(
    prompt="ambient electronic atmosphere",
    duration=180
)
```

### Credits Management

```python
# Check available credits
credits = await client.get_credits()
print(f"Available: {credits.available}")
print(f"Total: {credits.total}")
print(f"Used: {credits.used}")
```

### Webhook Integration

```python
from rapperrok.webhooks import WebhookHandler

handler = WebhookHandler(secret="your_webhook_secret")

# Verify and parse webhook
@app.post("/webhooks/aimusic")
async def handle_webhook(request: Request):
    payload = await request.json()
    signature = request.headers.get("X-Webhook-Signature")

    if handler.verify_signature(payload, signature):
        event = handler.parse_event(payload)

        if event.status == "completed":
            print(f"Music ready: {event.audio_url}")
        elif event.status == "failed":
            print(f"Generation failed: {event.error}")

    return {"status": "ok"}
```

## Advanced Features

### Retry Logic

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    retry_config=RetryConfig(
        max_retries=5,
        initial_delay=2.0,
        max_delay=60.0,
        exponential_base=2.0
    )
)
```

### Custom Timeout

```python
result = await client.suno.create_music(
    description="long orchestral piece",
    timeout=600  # 10 minutes
)
```

### Batch Operations

```python
# Generate multiple tracks concurrently
descriptions = [
    "rock song",
    "jazz melody",
    "classical piano"
]

tasks = [
    client.suno.create_music(desc)
    for desc in descriptions
]

results = await asyncio.gather(*tasks)
```

### Download Audio

```python
from rapperrok.utils import download_audio

# Download generated music
await download_audio(
    url=music.audio_url,
    output_path="my_song.mp3"
)
```

## API Models Overview

### Suno V4

- Create, extend, concat, cover music
- Stems separation (basic: 2 tracks, full: 12 tracks)
- Persona creation and custom voices
- WAV/MIDI export
- Voice gender control

### Producer (FUZZ-2.0)

- Fast generation (30 seconds)
- Create, extend, cover, replace operations
- Vocal/instrumental swapping
- Variations generation

### Nuro

- Full-length songs (up to 4 minutes)
- Vocal and instrumental modes
- Extensive customization

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/rapperrok/rapperrok.git
cd rapperrok

# Install with dev dependencies (via uv - recommended)
make dev
# Or manually
uv pip install -e ".[dev]"

# Install pre-commit hooks
uv run pre-commit install
```

### Run Tests

```bash
# Run all tests (via make)
make test

# Or manually with uv run
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration
```

### Code Quality

```bash
# Format code
make format
# Or manually
uv run ruff format .

# Lint
make lint
# Or manually
uv run ruff check .

# Type check
uv run mypy src/

# All checks
make quality
```

## Project Structure

```text
rapperrok/
├── src/rapperrok/
│   ├── __init__.py          # Main client
│   ├── common/              # Shared utilities
│   │   ├── base.py          # Base HTTP client
│   │   ├── models.py        # Common data models
│   │   ├── exceptions.py    # Error handling
│   │   └── utils.py         # Helper functions
│   ├── suno/                # Suno API client
│   │   ├── client.py
│   │   └── models.py
│   ├── producer/            # Producer API client
│   │   ├── client.py
│   │   └── models.py
│   ├── nuro/                # Nuro API client
│   │   ├── client.py
│   │   └── models.py
│   └── webhooks/            # Webhook handling
│       ├── handler.py
│       └── models.py
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── examples/                # Usage examples
└── docs/                    # Documentation
```

## Documentation

### Comprehensive Guides

- **[API Reference](./docs/API_REFERENCE.md)** - Complete API documentation with all endpoints and official docs
- **[Models Guide](./docs/MODELS.md)** - Detailed comparison of Suno, Producer, Nuro, and Riffusion models
- **[Endpoints Reference](./docs/ENDPOINTS.md)** - All API endpoints with request/response examples
- **[Quick Start](./QUICKSTART.md)** - Get started quickly with examples
- **[Contributing Guide](./CONTRIBUTING.md)** - How to contribute to the project

### Official AI Music API Docs

- **Official Docs**: [https://docs.aimusicapi.ai](https://docs.aimusicapi.ai)
- **Main Website**: [https://aimusicapi.ai](https://aimusicapi.ai)
- **Dashboard**: [https://aimusicapi.ai/dashboard](https://aimusicapi.ai/dashboard)

### Quick Links by Model

#### Suno V4
- [Suno API Overview](https://docs.aimusicapi.ai/suno-api-instructions.md)
- [Create Music](https://docs.aimusicapi.ai/create-suno-music.md)
- [Stems Separation](https://docs.aimusicapi.ai/stems-basic.md)
- [Custom Personas](https://docs.aimusicapi.ai/create-suno-persona.md)

#### Producer (FUZZ-2.0)
- [Producer API Overview](https://docs.aimusicapi.ai/producer-api-overview.md)
- [Create Music](https://docs.aimusicapi.ai/create-producer-music.md)
- [Request Examples](https://docs.aimusicapi.ai/producer-api-examples.md)

#### Nuro
- [Nuro API Overview](https://docs.aimusicapi.ai/nuro-api-overview.md)
- [Create Vocal Music](https://docs.aimusicapi.ai/create-vocal-music-nuro.md)
- [Create Instrumental](https://docs.aimusicapi.ai/create-instrument-music-nuro.md)

### More Resources

- **Examples**: See [examples/](./examples) directory for code samples
- **API Status**: Check [API_STATUS.md](./API_STATUS.md) for service status
- **Changelog**: [https://aimusicapi.featurebase.app/en/changelog](https://aimusicapi.featurebase.app/en/changelog)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### SSL/Connection Errors

If you encounter `SSL: TLSV1_UNRECOGNIZED_NAME` errors:

1. **Check your .env file** - Make sure you're using the correct API base URL:

   ```bash
   grep AIMUSIC_BASE_URL .env
   # Should show: AIMUSIC_BASE_URL=https://api.sunoapi.com
   ```

2. **Clear environment variables**:

   ```bash
   unset AIMUSIC_BASE_URL
   ```

3. **Verify connectivity**:

   ```bash
   curl -I https://api.sunoapi.com
   # Should return: HTTP/1.1 with SSL OK
   ```

### API Key Issues

- Get your API key from: <https://aimusicapi.ai/dashboard/apikey>
- Make sure it's set in `.env` or passed to the client
- API keys start with `sk_`

### Rate Limiting

The API may rate limit requests. Use retry configuration:

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    retry_config=RetryConfig(max_retries=5, initial_delay=2.0)
)
```

### API Service Status (November 2025)

**Note**: As of November 5, 2025, the AI Music API endpoints may not be fully deployed. If you receive 404/405 errors, this is a server-side issue, not a problem with the library.

**Current Status**:
- ✅ SSL/TLS connection works
- ✅ API domain resolves correctly
- ⏸️ Backend endpoints return 404/405 (not yet deployed)

**What to do**:
1. Join their [Discord](https://discord.gg/UFT2J2XK7d) for updates
2. Check the [Changelog](https://aimusicapi.featurebase.app/en/changelog) for service updates
3. Use mock testing for development (see `tests/` directory for examples)

The library is ready and will work immediately once the API service is fully operational.

See [API_STATUS.md](./API_STATUS.md) for detailed investigation results.

## Acknowledgments

- [AI Music API](https://docs.aimusicapi.ai) for providing the API
- Built with modern Python tools: [uv](https://github.com/astral-sh/uv), [ruff](https://github.com/astral-sh/ruff), [httpx](https://www.python-httpx.org/), [pydantic](https://docs.pydantic.dev/)

## Support

- Documentation: <https://rapperrok.readthedocs.io>
- Issues: <https://github.com/rapperrok/rapperrok/issues>
- API Docs: <https://docs.aimusicapi.ai>
- Main Website: <https://aimusicapi.ai>

---

Made with ❤️ by the RapperRok Team
