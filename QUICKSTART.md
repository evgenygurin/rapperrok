# RapperRok Quick Start Guide

Get started with RapperRok AI Music API client in 5 minutes!

## Installation

```bash
# Clone repository
cd /Users/laptop/dev/rapperrok

# Install with uv (recommended)
pip install uv
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

## Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# AIMUSIC_API_KEY=your_api_key_here
```

## First Music Generation

Create `test.py`:

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    # Initialize client (reads AIMUSIC_API_KEY from .env)
    async with AIMusicClient() as client:
        # Check your credits
        credits = await client.get_credits()
        print(f"💰 Available credits: {credits.available}")

        # Generate music with Suno V4
        print("🎵 Generating music...")
        result = await client.suno.create_music(
            description="upbeat electronic dance music with strong bass",
            duration=30,
            voice_gender="female",
            wait_for_completion=True,
        )

        # Get the audio
        for clip in result.clips:
            print(f"✅ Success!")
            print(f"🎧 Audio URL: {clip.audio_url}")
            print(f"🎬 Video URL: {clip.video_url}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python test.py
```

## Next Steps

### Explore Examples

```bash
# Basic operations (all models)
python examples/01_basic_usage.py

# Advanced Suno features (stems, personas, etc.)
python examples/02_advanced_suno.py

# Producer operations (fast generation)
python examples/03_producer_operations.py

# Webhook integration
python examples/04_webhook_integration.py
```

### Run Tests

```bash
# All tests with coverage
make test

# Unit tests only (fast, no API key needed)
make test-unit
```

### Code Quality

```bash
# Format code
make format

# Lint
make lint

# All checks
make quality
```

## Quick Reference

### Check Credits

```python
credits = await client.get_credits()
print(f"Available: {credits.available}/{credits.total}")
```

### Suno V4 - Create Music

```python
result = await client.suno.create_music(
    description="jazz piano solo",
    duration=60,
    voice_gender="male",
    wait_for_completion=True
)
```

### Suno V4 - Custom Lyrics

```python
result = await client.suno.create_music_with_lyrics(
    lyrics="My custom lyrics...",
    style="rock, electric guitar, drums",
    title="My Song"
)
```

### Suno V4 - Stems Separation

```python
# Basic (vocals + instrumental)
stems = await client.suno.stems_basic("song_id")
print(stems.vocals_url)
print(stems.instrumental_url)

# Full (12 tracks)
stems = await client.suno.stems_full("song_id")
print(stems.drums_url)
print(stems.bass_url)
print(stems.guitar_url)
```

### Producer - Fast Generation (30s)

```python
result = await client.producer.create_music(
    operation="create",
    description="energetic EDM track",
    duration=60,
    wait_for_completion=True
)
```

### Producer - Swap Vocals

```python
result = await client.producer.create_music(
    operation="swap_vocal",
    audio_id="clip_123",
    vocal_style="opera singer, dramatic",
    wait_for_completion=True
)
```

### Nuro - Full Length Song (4 min)

```python
result = await client.nuro.create_vocal_music(
    prompt="epic orchestral soundtrack",
    duration=240,
    style="cinematic",
    wait_for_completion=True
)
```

### Download Audio

```python
from rapperrok import download_audio

await download_audio(
    url=result.clips[0].audio_url,
    output_path="my_song.mp3"
)
```

## Common Patterns

### Wait Later

```python
# Start generation
result = await client.suno.create_music(description="...")
task_id = result.task_id

# Do other work...

# Wait when ready
completed = await client.suno.wait_for_completion(task_id)
```

### Batch Generation

```python
descriptions = ["rock", "jazz", "classical"]

# Create all
tasks = [client.suno.create_music(d) for d in descriptions]
results = await asyncio.gather(*tasks)

# Wait for all
completed = await asyncio.gather(*[
    client.suno.wait_for_completion(r.task_id)
    for r in results
])
```

### Error Handling

```python
from rapperrok import (
    InsufficientCreditsError,
    RateLimitError,
    TaskFailedError
)

try:
    result = await client.suno.create_music(...)
except InsufficientCreditsError:
    print("Not enough credits")
except RateLimitError as e:
    print(f"Rate limit. Wait {e.retry_after}s")
except TaskFailedError as e:
    print(f"Failed: {e.message}")
```

## Development Commands

```bash
make help          # Show all commands
make dev           # Install dev dependencies
make test          # Run tests with coverage
make lint          # Lint code
make format        # Format code
make quality       # Run all checks
make clean         # Clean build artifacts
```

## Project Structure

```text
rapperrok/
├── src/rapperrok/          # Source code
│   ├── __init__.py         # Main AIMusicClient
│   ├── common/             # Shared utilities
│   ├── suno/               # Suno V4 client
│   ├── producer/           # Producer client
│   ├── nuro/               # Nuro client
│   └── webhooks/           # Webhook handling
├── examples/               # Usage examples
├── tests/                  # Test suite
├── docs/                   # Documentation
├── pyproject.toml         # Project config
├── Makefile               # Dev commands
├── README.md              # User docs
└── CLAUDE.md              # AI assistant guide
```

## API Models Overview

| Model | Best For | Generation Time | Max Duration |
|-------|----------|-----------------|--------------|
| **Suno V4** | Most features, stems, personas | ~2 min | 4 min |
| **Producer** | Fast generation, variations | ~30 sec | 4 min |
| **Nuro** | Full-length songs | ~30 sec | 4 min |

## Credits Cost

| Operation | Credits |
|-----------|---------|
| Suno - Create | 10 |
| Suno - Stems Basic | 20 |
| Suno - Stems Full | 50 |
| Producer - Create | 10 |
| Producer - Swap Vocal | 15 |
| Nuro - Vocal | 20 |

## Help & Support

- **Documentation**: [CLAUDE.md](CLAUDE.md) - Comprehensive guide
- **Examples**: [examples/](examples/) - 4 detailed examples
- **API Docs**: https://docs.aimusicapi.ai
- **Issues**: Report bugs on GitHub

## License

MIT License - see [LICENSE](LICENSE)

---

**Happy music generation! 🎵**

For more details, see [CLAUDE.md](CLAUDE.md) or [README.md](README.md).
