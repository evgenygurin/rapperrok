# Quick Start

Get started with RapperRok in 5 minutes! This guide will walk you through creating your first AI-generated music.

## Prerequisites

Make sure you have:

- [x] RapperRok installed (`pip install rapperrok` or `uv pip install rapperrok`)
- [x] API key from [aimusicapi.ai](https://aimusicapi.ai/dashboard/apikey)

## Step 1: Set Up Your Environment

Create a `.env` file in your project:

```bash
AIMUSIC_API_KEY=sk_your_api_key_here
```

## Step 2: Your First Music Generation

Create a file called `first_song.py`:

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    # Initialize the client
    async with AIMusicClient() as client:
        # Generate music
        print("🎵 Generating music...")

        result = await client.suno.create_music(
            description="upbeat electronic dance music with strong bass",
            duration=30,
            wait_for_completion=True
        )

        # Print results
        print("✅ Music generated!")
        for i, clip in enumerate(result.clips):
            print(f"\nClip {i+1}:")
            print(f"  Title: {clip.title}")
            print(f"  Audio: {clip.audio_url}")
            print(f"  Video: {clip.video_url}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python first_song.py
```

Output:

```
🎵 Generating music...
✅ Music generated!

Clip 1:
  Title: Electronic Dance Beat
  Audio: https://cdn.aimusicapi.ai/abc123.mp3
  Video: https://cdn.aimusicapi.ai/abc123.mp4
```

## Step 3: Create Music with Custom Lyrics

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        result = await client.suno.create_music_with_lyrics(
            lyrics="""
            [Verse 1]
            Walking down the street today
            Everything seems bright and gay

            [Chorus]
            This is my happy song
            Singing all day long
            """,
            style="pop, upbeat, acoustic guitar, cheerful",
            title="My Happy Song",
            wait_for_completion=True
        )

        print(f"✅ Song created: {result.clips[0].audio_url}")

asyncio.run(main())
```

## Step 4: Extend Your Music

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        # First, create a song
        result = await client.suno.create_music(
            description="calm piano melody",
            duration=30,
            wait_for_completion=True
        )

        audio_id = result.clips[0].id

        # Now extend it
        extended = await client.suno.extend_music(
            audio_id=audio_id,
            duration=60,
            wait_for_completion=True
        )

        print(f"✅ Extended music: {extended.clips[0].audio_url}")

asyncio.run(main())
```

## Step 5: Separate Vocals and Instrumentals

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        # Create a song with vocals
        result = await client.suno.create_music(
            description="rock song with powerful vocals",
            duration=30,
            wait_for_completion=True
        )

        song_id = result.clips[0].id

        # Separate stems
        stems = await client.suno.stems_basic(song_id=song_id)

        print(f"✅ Vocals: {stems.vocals_url}")
        print(f"✅ Instrumental: {stems.instrumental_url}")

asyncio.run(main())
```

## Step 6: Use Producer for Fast Generation

Producer generates music in just 30 seconds!

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        result = await client.producer.create_music(
            description="energetic EDM track with drops",
            operation="create",
            duration=60,
            wait_for_completion=True
        )

        print(f"✅ Fast track: {result.audio_url}")

asyncio.run(main())
```

## Step 7: Generate Full-Length Songs with Nuro

Nuro can generate complete 4-minute songs:

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        song = await client.nuro.create_vocal_music(
            prompt="epic orchestral soundtrack with choir",
            duration=240,  # 4 minutes
            style="cinematic",
            wait_for_completion=True
        )

        print(f"✅ Full song: {song.audio_url}")

asyncio.run(main())
```

## Common Patterns

### Check Credits Before Generation

```python
async with AIMusicClient() as client:
    # Check credits
    credits = await client.get_credits()
    print(f"Available credits: {credits.available}")

    if credits.available >= 10:
        result = await client.suno.create_music(...)
    else:
        print("Not enough credits!")
```

### Download Generated Music

```python
from rapperrok.utils import download_audio

async with AIMusicClient() as client:
    result = await client.suno.create_music(
        description="...",
        wait_for_completion=True
    )

    # Download the audio file
    await download_audio(
        url=result.clips[0].audio_url,
        output_path="my_song.mp3"
    )

    print("✅ Downloaded to my_song.mp3")
```

### Batch Generation

```python
import asyncio

async with AIMusicClient() as client:
    descriptions = [
        "rock song with guitar",
        "jazz piano melody",
        "electronic dance music"
    ]

    # Create all tasks
    tasks = [
        client.suno.create_music(desc, duration=30)
        for desc in descriptions
    ]

    # Wait for all to start
    results = await asyncio.gather(*tasks)

    # Wait for all to complete
    completed = await asyncio.gather(*[
        client.suno.wait_for_completion(r.task_id)
        for r in results
    ])

    for i, result in enumerate(completed):
        print(f"Song {i+1}: {result.clips[0].audio_url}")
```

### Error Handling

```python
from rapperrok.exceptions import (
    InsufficientCreditsError,
    RateLimitError,
    TaskFailedError
)

async with AIMusicClient() as client:
    try:
        result = await client.suno.create_music(
            description="...",
            wait_for_completion=True
        )
    except InsufficientCreditsError:
        print("❌ Not enough credits!")
    except RateLimitError as e:
        print(f"❌ Rate limited. Retry after {e.retry_after}s")
    except TaskFailedError as e:
        print(f"❌ Generation failed: {e.message}")
```

## Using the CLI

RapperRok also provides a CLI:

```bash
# Generate music
rapperrok suno create --description "jazz piano solo" --duration 60

# Check credits
rapperrok credits

# Get task status
rapperrok suno get --task-id abc123

# Create with lyrics from file
rapperrok suno create --lyrics lyrics.txt --style "rock"
```

## What's Next?

Now that you've created your first AI music, explore more:

- [**Basic Usage Guide**](guides/basic-usage.md) - Learn essential operations
- [**Suno Guide**](guides/suno.md) - Master Suno V4 features
- [**Producer Guide**](guides/producer.md) - Fast music generation
- [**Nuro Guide**](guides/nuro.md) - Full-length songs
- [**Webhook Guide**](guides/webhooks.md) - Async notifications
- [**API Reference**](api/overview.md) - Complete API documentation

## Tips

1. **Start small**: Begin with 30-second tracks to test and iterate quickly
2. **Wait for completion**: Use `wait_for_completion=True` for simple scripts
3. **Use webhooks**: For long-running tasks, webhooks are more efficient than polling
4. **Download important files**: Generated URLs may expire after some time
5. **Handle errors**: Always wrap API calls in try-except blocks for production
6. **Check credits**: Monitor your credit balance, especially for batch operations

## Need Help?

- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
- **Examples**: [View code examples](examples.md)
- **GitHub Issues**: [Report bugs](https://github.com/rapperrok/rapperrok/issues)
- **AI Music API Docs**: [https://docs.aimusicapi.ai](https://docs.aimusicapi.ai)
