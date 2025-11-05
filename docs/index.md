# RapperRok - AI Music API Python Client

<div align="center" markdown>

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

Comprehensive Python client for **AI Music API** supporting **Suno**, **Udio**, **Riffusion**, **Nuro**, and **Producer** models.

[Get Started](getting-started.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/rapperrok/rapperrok){ .md-button }
[API Reference](api/overview.md){ .md-button }

</div>

---

## What is RapperRok?

RapperRok is a modern, type-safe Python client for the AI Music API that makes it easy to generate professional-quality music using state-of-the-art AI models. Whether you're building a music app, creating content, or experimenting with AI-generated music, RapperRok provides a clean, intuitive interface to powerful music generation capabilities.

## Why RapperRok?

### 🎵 Multiple AI Models

Access the best AI music generation models from a single, unified interface:

- **Suno V4** - Studio-quality music with vocals/instrumentals
- **Producer (FUZZ-2.0)** - High-quality tracks in 30 seconds
- **Nuro** - Complete 4-minute songs in 30 seconds
- **Riffusion** - Real-time music generation
- **Udio** - Advanced music creation

### 🚀 Developer-Friendly

- **Modern Python** - Python 3.12+ with full type hints
- **Async/Await** - Non-blocking operations with httpx
- **Type Safe** - Complete type annotations with Pydantic
- **Rich CLI** - Beautiful terminal output with progress tracking
- **Well Documented** - Comprehensive docs and examples

### 🎼 Powerful Features

- **Music Generation**: Create, extend, cover, and remix tracks
- **Vocal Processing**: Swap vocals, create personas, gender control
- **Audio Processing**: Stems separation (basic/full), format conversion
- **Lyrics Generation**: AI-powered lyrics creation
- **MIDI Export**: Extract MIDI data from tracks
- **Webhook Integration**: Async notifications for long-running tasks
- **Credit Management**: Track and manage API credits

### 🛡️ Production-Ready

- **Retry Logic**: Automatic retry with exponential backoff
- **Error Handling**: Comprehensive error messages and recovery
- **Rate Limiting**: Built-in rate limit handling
- **Testing**: Extensive test coverage with pytest

## Quick Example

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

    # Wait for completion
    music = await client.suno.wait_for_completion(result.task_id)
    print(f"Audio URL: {music.audio_url}")
    print(f"Video URL: {music.video_url}")

asyncio.run(main())
```

## Features at a Glance

=== "Suno V4"

    **Studio-Quality Music Generation**

    - Create music from text descriptions
    - Custom lyrics and style
    - Extend and concatenate tracks
    - Cover existing songs
    - Stems separation (2 or 12 tracks)
    - Custom voice personas
    - WAV and MIDI export
    - Voice gender control

    [Learn More →](guides/suno.md)

=== "Producer"

    **Fast Music Generation**

    - Create tracks in 30 seconds
    - Extend existing music
    - Create cover versions
    - Replace sections
    - Swap vocals/instrumentals
    - Create variations
    - Upload and modify audio
    - MP3/WAV export

    [Learn More →](guides/producer.md)

=== "Nuro"

    **Full-Length Songs**

    - Complete 4-minute songs in 30 seconds
    - Vocal and instrumental modes
    - Extensive customization options
    - Fast generation time
    - Professional quality output

    [Learn More →](guides/nuro.md)

=== "Webhooks"

    **Async Notifications**

    - Real-time task updates
    - Signature verification
    - FastAPI integration
    - Event handling
    - Error notifications

    [Learn More →](guides/webhooks.md)

## Installation

=== "Using uv (Recommended)"

    ```bash
    # Install uv if you don't have it
    pip install uv

    # Install rapperrok
    uv pip install rapperrok

    # Or with development dependencies
    uv pip install "rapperrok[dev]"
    ```

=== "Using pip"

    ```bash
    pip install rapperrok

    # Or with development dependencies
    pip install "rapperrok[dev]"
    ```

=== "From Source"

    ```bash
    git clone https://github.com/rapperrok/rapperrok.git
    cd rapperrok

    # Install with uv (recommended)
    make dev
    # Or manually
    uv pip install -e ".[dev]"
    ```

[Full Installation Guide →](getting-started.md)

## Use Cases

### 🎬 Content Creation

Generate background music for videos, podcasts, and social media content.

```python
# Create ambient background music
background = await client.nuro.create_instrumental_music(
    prompt="soft ambient piano for meditation",
    duration=180
)
```

### 🎤 Music Production

Create demos, generate ideas, or produce full tracks with vocals.

```python
# Create a song with custom lyrics
song = await client.suno.create_music_with_lyrics(
    lyrics="Verse 1: Walking down the street...",
    style="indie rock, acoustic guitar, drums",
    title="My Demo Track"
)
```

### 🔊 Audio Processing

Separate stems, swap vocals, or remix existing tracks.

```python
# Extract vocals and instrumentals
stems = await client.suno.stems_basic(song_id="song_abc123")
print(f"Vocals: {stems.vocals_url}")
print(f"Instrumental: {stems.instrumental_url}")
```

### 🎮 Game Development

Generate dynamic soundtracks and sound effects for games.

```python
# Create epic game soundtrack
soundtrack = await client.producer.create_music(
    description="epic orchestral battle theme",
    operation="create",
    duration=120
)
```

## What's Next?

<div class="grid cards" markdown>

- :material-clock-fast:{ .lg .middle } **Quick Start**

    ---

    Get up and running in minutes with our quick start guide.

    [:octicons-arrow-right-24: Quick Start](quickstart.md)

- :material-book-open-variant:{ .lg .middle } **Guides**

    ---

    Learn how to use each API model with detailed guides.

    [:octicons-arrow-right-24: View Guides](guides/basic-usage.md)

- :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Complete API documentation with examples.

    [:octicons-arrow-right-24: API Docs](api/overview.md)

- :material-school:{ .lg .middle } **Tutorials**

    ---

    Step-by-step tutorials for common tasks.

    [:octicons-arrow-right-24: Tutorials](tutorials/first-song.md)

</div>

## Community & Support

- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
- **GitHub**: [https://github.com/rapperrok/rapperrok](https://github.com/rapperrok/rapperrok)
- **Issues**: [Report bugs or request features](https://github.com/rapperrok/rapperrok/issues)
- **AI Music API**: [Official API Documentation](https://docs.aimusicapi.ai)

## License

RapperRok is licensed under the [MIT License](license.md). See the LICENSE file for details.

---

<div align="center" markdown>

Made with ❤️ by the RapperRok Team

[Star on GitHub](https://github.com/rapperrok/rapperrok){ .md-button }

</div>
