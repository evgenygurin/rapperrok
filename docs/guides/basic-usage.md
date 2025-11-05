# Basic Usage

This guide covers the fundamental operations you'll use with RapperRok.

## Client Initialization

### Using Environment Variables

```python
from rapperrok import AIMusicClient

# Loads API key from AIMUSIC_API_KEY environment variable
client = AIMusicClient()
```

### Direct API Key

```python
from rapperrok import AIMusicClient

client = AIMusicClient(api_key="sk_your_api_key")
```

### With Configuration

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    api_key="your_key",
    base_url="https://api.aimusicapi.ai",
    timeout=60.0,
    retry_config=RetryConfig(max_retries=5)
)
```

### Using Context Manager (Recommended)

```python
async with AIMusicClient() as client:
    result = await client.suno.create_music(...)
    # Client automatically closes when done
```

## Creating Music

### From Description

```python
async with AIMusicClient() as client:
    result = await client.suno.create_music(
        description="upbeat electronic dance music with strong bass",
        duration=30,
        voice_gender="female",
        wait_for_completion=True
    )

    for clip in result.clips:
        print(f"Audio: {clip.audio_url}")
        print(f"Video: {clip.video_url}")
```

### With Custom Lyrics

```python
lyrics = """
[Verse 1]
Walking down the street
Life feels so complete

[Chorus]
This is my song
Singing all day long
"""

result = await client.suno.create_music_with_lyrics(
    lyrics=lyrics,
    style="pop, acoustic guitar, upbeat",
    title="My Song",
    voice_gender="male",
    wait_for_completion=True
)
```

### Instrumental Only

```python
result = await client.suno.create_music(
    description="calm piano melody for meditation",
    duration=60,
    instrumental=True,  # No vocals
    wait_for_completion=True
)
```

## Checking Task Status

### Async Polling

```python
# Start generation (non-blocking)
result = await client.suno.create_music(
    description="jazz piano solo",
    duration=30
)

task_id = result.task_id
print(f"Task started: {task_id}")

# Do other work...

# Check status later
status = await client.suno.get_music(task_id)
if status.status == "completed":
    print(f"Audio: {status.clips[0].audio_url}")
elif status.status == "processing":
    print("Still processing...")
elif status.status == "failed":
    print(f"Failed: {status.error}")
```

### Wait for Completion

```python
# Blocking wait until completed
result = await client.suno.create_music(
    description="rock song",
    duration=30,
    wait_for_completion=True  # Polls automatically
)

# Result is completed when returned
print(f"Audio: {result.clips[0].audio_url}")
```

### Custom Polling

```python
import asyncio

result = await client.suno.create_music(description="...")

# Custom polling loop
while True:
    status = await client.suno.get_music(result.task_id)

    if status.status == "completed":
        print("Done!")
        break
    elif status.status == "failed":
        print("Failed!")
        break

    print("Still processing...")
    await asyncio.sleep(5)  # Check every 5 seconds
```

## Managing Credits

### Check Balance

```python
credits = await client.get_credits()

print(f"Available: {credits.available}")
print(f"Total: {credits.total}")
print(f"Used: {credits.used}")
```

### Check Before Operations

```python
credits = await client.get_credits()

if credits.available >= 10:
    result = await client.suno.create_music(...)
else:
    print("Insufficient credits!")
```

### Credit Costs

Different operations consume different amounts of credits:

| Operation | Credits |
|-----------|---------|
| Create music (Suno) | 10 |
| Extend music (Suno) | 10 |
| Concat music (Suno) | 5 |
| Cover music (Suno) | 10 |
| Stems basic (Suno) | 20 |
| Stems full (Suno) | 50 |
| Create persona (Suno) | 50 |
| WAV export (Suno) | 10 |
| MIDI export (Suno) | 5 |
| Create music (Producer) | 10 |
| Swap vocals (Producer) | 15 |
| Create music (Nuro) | 20 |

## Downloading Audio

### Using Utility Function

```python
from rapperrok.utils import download_audio

result = await client.suno.create_music(
    description="...",
    wait_for_completion=True
)

# Download to local file
await download_audio(
    url=result.clips[0].audio_url,
    output_path="my_song.mp3"
)

print("Downloaded to my_song.mp3")
```

### Manual Download

```python
import aiofiles
import httpx

async def download_file(url: str, path: str):
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(url)
        response.raise_for_status()

        async with aiofiles.open(path, 'wb') as f:
            await f.write(response.content)

# Use it
await download_file(result.clips[0].audio_url, "song.mp3")
```

## Batch Operations

### Generate Multiple Tracks

```python
import asyncio

async with AIMusicClient() as client:
    descriptions = [
        "rock song with guitar",
        "jazz piano melody",
        "electronic dance music"
    ]

    # Create tasks concurrently
    tasks = [
        client.suno.create_music(desc, duration=30)
        for desc in descriptions
    ]

    # Start all tasks
    results = await asyncio.gather(*tasks)

    # Wait for all to complete
    completed = await asyncio.gather(*[
        client.suno.wait_for_completion(r.task_id)
        for r in results
    ])

    for i, result in enumerate(completed):
        print(f"Song {i+1}: {result.clips[0].audio_url}")
```

### Controlled Concurrency

```python
import asyncio

async def generate_with_limit(client, descriptions, max_concurrent=5):
    sem = asyncio.Semaphore(max_concurrent)

    async def limited_generate(desc):
        async with sem:
            return await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )

    tasks = [limited_generate(desc) for desc in descriptions]
    return await asyncio.gather(*tasks)

# Use it
results = await generate_with_limit(client, descriptions)
```

## Error Handling

### Basic Try-Catch

```python
from rapperrok.exceptions import AIMusicAPIError

try:
    result = await client.suno.create_music(
        description="...",
        wait_for_completion=True
    )
except AIMusicAPIError as e:
    print(f"Error: {e.message}")
    print(f"Status code: {e.status_code}")
```

### Specific Exceptions

```python
from rapperrok.exceptions import (
    InsufficientCreditsError,
    RateLimitError,
    TaskFailedError,
    InvalidParameterError
)

try:
    result = await client.suno.create_music(...)
except InsufficientCreditsError as e:
    print(f"Not enough credits. Available: {e.credits_available}")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
    await asyncio.sleep(e.retry_after)
    # Retry...
except TaskFailedError as e:
    print(f"Task failed: {e.message}")
except InvalidParameterError as e:
    print(f"Invalid parameter: {e.message}")
```

### Retry on Failure

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_with_retry(client, description):
    return await client.suno.create_music(
        description=description,
        duration=30,
        wait_for_completion=True
    )

# Use it
result = await generate_with_retry(client, "rock song")
```

## Working with Different Models

### Suno (Highest Quality)

```python
# Best for: High-quality music with vocals
result = await client.suno.create_music(
    description="emotional ballad with piano",
    duration=120,
    voice_gender="female",
    wait_for_completion=True
)
```

### Producer (Fastest)

```python
# Best for: Quick generation (30 seconds)
result = await client.producer.create_music(
    description="energetic EDM track",
    operation="create",
    duration=60,
    wait_for_completion=True
)
```

### Nuro (Full Songs)

```python
# Best for: Complete full-length songs (up to 4 minutes)
result = await client.nuro.create_vocal_music(
    prompt="epic orchestral soundtrack",
    duration=240,
    style="cinematic",
    wait_for_completion=True
)
```

## Common Patterns

### Check Credits and Generate

```python
async def safe_generate(client, description):
    # Check credits first
    credits = await client.get_credits()

    if credits.available < 10:
        raise ValueError("Insufficient credits")

    # Generate
    return await client.suno.create_music(
        description=description,
        duration=30,
        wait_for_completion=True
    )
```

### Generate and Download

```python
from rapperrok.utils import download_audio
from pathlib import Path

async def generate_and_download(client, description, output_dir="output"):
    # Generate
    result = await client.suno.create_music(
        description=description,
        duration=30,
        wait_for_completion=True
    )

    # Download all clips
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for i, clip in enumerate(result.clips):
        file_path = output_path / f"{clip.id}.mp3"
        await download_audio(clip.audio_url, str(file_path))
        print(f"Downloaded: {file_path}")

    return result
```

### Batch with Progress

```python
from rich.progress import Progress

async def batch_generate_with_progress(client, descriptions):
    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Generating...",
            total=len(descriptions)
        )

        results = []
        for desc in descriptions:
            result = await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )
            results.append(result)
            progress.update(task, advance=1)

        return results
```

## Best Practices

1. **Use async context managers** for automatic cleanup
2. **Handle errors** explicitly with try-except
3. **Check credits** before batch operations
4. **Use wait_for_completion** for simple scripts
5. **Use webhooks** for long-running tasks in production
6. **Download important files** as URLs may expire
7. **Limit concurrency** to avoid rate limits
8. **Log operations** for debugging and monitoring

## Next Steps

- [Suno Guide](suno.md) - Master Suno V4 features
- [Producer Guide](producer.md) - Fast music generation
- [Nuro Guide](nuro.md) - Full-length songs
- [Webhook Integration](webhooks.md) - Async notifications
- [Error Handling](error-handling.md) - Handle errors gracefully
- [API Reference](../api/overview.md) - Complete API docs
