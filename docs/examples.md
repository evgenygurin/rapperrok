# Examples

Comprehensive code examples for RapperRok.

## Quick Examples

### Basic Music Generation

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description="upbeat electronic dance music",
            duration=60,
            wait_for_completion=True
        )

        print(f"Audio: {result.clips[0].audio_url}")

asyncio.run(main())
```

### Custom Lyrics

```python
async def main():
    async with AIMusicClient() as client:
        lyrics = """
        [Verse 1]
        Walking down the street
        Life is so complete

        [Chorus]
        This is my song
        Singing all day long
        """

        result = await client.suno.create_music_with_lyrics(
            lyrics=lyrics,
            style="pop, acoustic guitar",
            wait_for_completion=True
        )

        print(f"Song: {result.clips[0].audio_url}")
```

### Batch Generation

```python
import asyncio

async def batch_generate():
    descriptions = ["rock", "jazz", "pop", "electronic"]

    async with AIMusicClient() as client:
        tasks = [
            client.suno.create_music(desc, duration=30)
            for desc in descriptions
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            music = await client.suno.wait_for_completion(result.task_id)
            print(f"Generated: {music.clips[0].audio_url}")
```

### Stems Separation

```python
async def separate_stems():
    async with AIMusicClient() as client:
        # Create song
        song = await client.suno.create_music(
            description="rock song with vocals",
            duration=60,
            wait_for_completion=True
        )

        # Separate stems
        stems = await client.suno.stems_basic(song_id=song.clips[0].id)

        print(f"Vocals: {stems.vocals_url}")
        print(f"Instrumental: {stems.instrumental_url}")
```

## Full Example Scripts

The repository includes complete example scripts:

### 01_basic_usage.py

Basic operations with all models (Suno, Producer, Nuro).

[View Source](https://github.com/rapperrok/rapperrok/blob/main/examples/01_basic_usage.py)

**Features:**

- Create music with Suno
- Fast generation with Producer
- Full songs with Nuro
- Check credit balance

**Run it:**

```bash
python examples/01_basic_usage.py
```

### 02_advanced_suno.py

Advanced Suno V4 features.

[View Source](https://github.com/rapperrok/rapperrok/blob/main/examples/02_advanced_suno.py)

**Features:**

- Custom lyrics
- Extend and concatenate
- Stems separation (basic and full)
- Custom voice personas
- WAV and MIDI export
- Download generated music

**Run it:**

```bash
python examples/02_advanced_suno.py
```

### 03_producer_operations.py

All Producer API operations.

[View Source](https://github.com/rapperrok/rapperrok/blob/main/examples/03_producer_operations.py)

**Features:**

- Create new music
- Extend tracks
- Create covers
- Replace sections
- Swap vocals/instrumentals
- Create variations
- Upload and modify audio
- Download MP3/WAV

**Run it:**

```bash
python examples/03_producer_operations.py
```

### 04_webhook_integration.py

Webhook handling and integration.

[View Source](https://github.com/rapperrok/rapperrok/blob/main/examples/04_webhook_integration.py)

**Features:**

- Basic webhook handler
- FastAPI webhook endpoint
- Generate with webhooks
- Manual webhook processing

**Run it:**

```bash
python examples/04_webhook_integration.py
```

## Use Case Examples

### Content Creation

Background music for videos:

```python
async def create_background_music():
    async with AIMusicClient() as client:
        music = await client.nuro.create_instrumental_music(
            prompt="upbeat background music for product video",
            duration=120,
            style="corporate, modern",
            wait_for_completion=True
        )

        # Download
        from rapperrok.utils import download_audio
        await download_audio(music.audio_url, "background.mp3")
```

### Music Production

Create song demo:

```python
async def create_demo():
    async with AIMusicClient() as client:
        # Create verse
        verse = await client.suno.create_music_with_lyrics(
            lyrics="[Verse]\nYour lyrics...",
            style="indie rock",
            duration=30,
            wait_for_completion=True
        )

        # Create chorus
        chorus = await client.suno.create_music_with_lyrics(
            lyrics="[Chorus]\nChorus lyrics...",
            style="indie rock, energetic",
            duration=30,
            wait_for_completion=True
        )

        # Concatenate
        full_song = await client.suno.concat_music(
            clip_ids=[
                verse.clips[0].id,
                chorus.clips[0].id,
                verse.clips[0].id,
                chorus.clips[0].id
            ],
            wait_for_completion=True
        )

        print(f"Demo: {full_song.audio_url}")
```

### Remixing

Create remix with new vocals:

```python
async def create_remix():
    async with AIMusicClient() as client:
        # Upload original track
        with open("original.mp3", "rb") as f:
            upload = await client.producer.upload_music(f, "original.mp3")

        # Swap vocals
        remix = await client.producer.create_music(
            audio_id=upload.audio_id,
            operation="swap_vocals",
            description="electronic vocals with autotune",
            wait_for_completion=True
        )

        print(f"Remix: {remix.audio_url}")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, BackgroundTasks
from rapperrok import AIMusicClient

app = FastAPI()
client = AIMusicClient()

@app.post("/generate")
async def generate_music(
    description: str,
    background_tasks: BackgroundTasks
):
    result = await client.suno.create_music(
        description=description,
        duration=60,
        wait_for_completion=False
    )

    # Process in background
    background_tasks.add_task(
        process_when_ready,
        result.task_id
    )

    return {"task_id": result.task_id}

async def process_when_ready(task_id: str):
    music = await client.suno.wait_for_completion(task_id)
    # Process music...
```

### Discord Bot

```python
import discord
from discord.ext import commands
from rapperrok import AIMusicClient

bot = commands.Bot(command_prefix="!")
music_client = AIMusicClient()

@bot.command()
async def generate(ctx, *, description: str):
    """Generate music from description"""
    await ctx.send(f"🎵 Generating: {description}")

    result = await music_client.suno.create_music(
        description=description,
        duration=30,
        wait_for_completion=True
    )

    await ctx.send(f"✅ Done: {result.clips[0].audio_url}")

bot.run("YOUR_DISCORD_TOKEN")
```

### Flask Integration

```python
from flask import Flask, request, jsonify
from rapperrok import AIMusicClient
import asyncio

app = Flask(__name__)
client = AIMusicClient()

@app.route("/generate", methods=["POST"])
def generate_music():
    description = request.json["description"]

    # Run async function
    result = asyncio.run(
        client.suno.create_music(
            description=description,
            duration=60,
            wait_for_completion=True
        )
    )

    return jsonify({
        "audio_url": result.clips[0].audio_url
    })
```

## CLI Examples

RapperRok provides a CLI for quick operations:

### Generate Music

```bash
# Suno
rapperrok suno create \
    --description "jazz piano solo" \
    --duration 60 \
    --voice-gender female

# Producer
rapperrok producer create \
    --description "electronic dance music" \
    --duration 60

# Nuro
rapperrok nuro create-vocal \
    --prompt "epic orchestral" \
    --duration 240
```

### Check Credits

```bash
rapperrok credits
```

### Get Task Status

```bash
rapperrok suno get --task-id abc123
```

### With Custom Configuration

```bash
rapperrok --api-key sk_your_key \
    --base-url https://api.aimusicapi.ai \
    suno create --description "rock song"
```

## Testing Examples

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_client():
    client = AsyncMock()
    client.suno.create_music.return_value = AsyncMock(
        task_id="test_123",
        status="completed"
    )
    return client

@pytest.mark.asyncio
async def test_generation(mock_client):
    result = await mock_client.suno.create_music(
        description="test",
        duration=30
    )

    assert result.task_id == "test_123"
    assert result.status == "completed"
```

### Integration Tests

```python
import pytest
from rapperrok import AIMusicClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_generation():
    """Test with real API"""
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description="test song",
            duration=30,
            wait_for_completion=True
        )

        assert result.clips
        assert result.clips[0].audio_url.startswith("https://")
```

## More Examples

For more examples, see:

- [Tutorials](tutorials/first-song.md) - Step-by-step guides
- [Guides](guides/basic-usage.md) - Comprehensive guides
- [GitHub Examples](https://github.com/rapperrok/rapperrok/tree/main/examples) - Full scripts

## Contributing Examples

Have a great example? Contribute it!

1. Fork the repository
2. Add your example to `examples/`
3. Update `examples/README.md`
4. Submit a pull request

See [Contributing Guide](contributing.md) for details.
