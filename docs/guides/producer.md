# Producer API Guide

Complete guide to using the Producer API (FUZZ-2.0 model) for fast, high-quality music generation in just 30 seconds.

## Overview

**Producer (FUZZ-2.0)** is optimized for speed and quality:

- ⚡ Generate music in 30 seconds
- 🎵 Create, extend, cover, replace operations
- 🎤 Swap vocals or instrumentals
- 🎨 Create variations
- 📤 Upload and modify audio
- 🎼 MP3/WAV export

**Speed:** ~30 seconds generation time
**Quality:** Comparable to Suno v5

## Operations

### Create New Music

Generate music from scratch:

```python
async with AIMusicClient() as client:
    result = await client.producer.create_music(
        description="energetic EDM track with drops and synth leads",
        operation="create",
        duration=60,
        wait_for_completion=True
    )

    print(f"Audio: {result.audio_url}")
    print(f"Video: {result.video_url}")
```

**Parameters:**

- `description` (str): Music description
- `operation` (str): "create"
- `duration` (int): Length in seconds
- `wait_for_completion` (bool): Wait for completion

### Extend Existing Music

Add more time to existing tracks:

```python
# First, create or upload music
initial = await client.producer.create_music(
    description="calm piano melody",
    operation="create",
    duration=30,
    wait_for_completion=True
)

audio_id = initial.audio_id

# Extend it
extended = await client.producer.create_music(
    audio_id=audio_id,
    operation="extend",
    duration=30,  # Additional 30 seconds
    wait_for_completion=True
)

print(f"Extended: {extended.audio_url}")
```

### Create Cover Version

Transform existing music:

```python
result = await client.producer.create_music(
    audio_id="clip_abc123",
    operation="cover",
    description="transform into jazz piano style",
    wait_for_completion=True
)
```

### Replace Section

Replace a specific section of music:

```python
result = await client.producer.create_music(
    audio_id="clip_abc123",
    operation="replace",
    description="replace middle section with energetic drums",
    start_time=15,  # Start at 15 seconds
    end_time=30,    # End at 30 seconds
    wait_for_completion=True
)
```

### Swap Vocals

Replace vocals while keeping instrumentals:

```python
result = await client.producer.create_music(
    audio_id="clip_abc123",
    operation="swap_vocals",
    description="female vocals, pop style",
    wait_for_completion=True
)
```

**Cost:** 15 credits

### Swap Instrumentals

Replace instrumentals while keeping vocals:

```python
result = await client.producer.create_music(
    audio_id="clip_abc123",
    operation="swap_instrumental",
    description="acoustic guitar and piano backing",
    wait_for_completion=True
)
```

**Cost:** 15 credits

### Create Variations

Generate variations of existing music:

```python
result = await client.producer.create_music(
    audio_id="clip_abc123",
    operation="variation",
    description="create upbeat variation with more energy",
    wait_for_completion=True
)
```

## Upload Music

### Upload Local File

```python
# Upload music file
with open("my_track.mp3", "rb") as f:
    upload_result = await client.producer.upload_music(
        file=f,
        filename="my_track.mp3"
    )

audio_id = upload_result.audio_id

# Now use it in operations
result = await client.producer.create_music(
    audio_id=audio_id,
    operation="extend",
    duration=30,
    wait_for_completion=True
)
```

**Supported Formats:**

- MP3
- WAV
- FLAC
- OGG

**Max Size:** 50MB

### Upload from URL

```python
upload_result = await client.producer.upload_music_from_url(
    url="https://example.com/music.mp3"
)

audio_id = upload_result.audio_id
```

## Download Music

### Download in Different Formats

```python
# Get music metadata
result = await client.producer.get_music(task_id="task_abc123")

audio_id = result.audio_id

# Download as MP3 (default)
mp3_url = await client.producer.download_music(
    audio_id=audio_id,
    format="mp3"
)

# Download as WAV (higher quality)
wav_url = await client.producer.download_music(
    audio_id=audio_id,
    format="wav"
)

print(f"MP3: {mp3_url}")
print(f"WAV: {wav_url}")
```

## Complete Workflows

### Create and Remix

```python
async def create_and_remix():
    async with AIMusicClient() as client:
        # 1. Create initial track
        print("Creating track...")
        initial = await client.producer.create_music(
            description="rock song with electric guitar",
            operation="create",
            duration=60,
            wait_for_completion=True
        )

        audio_id = initial.audio_id

        # 2. Create variation
        print("Creating variation...")
        variation = await client.producer.create_music(
            audio_id=audio_id,
            operation="variation",
            description="add more drums and bass",
            wait_for_completion=True
        )

        # 3. Swap vocals
        print("Swapping vocals...")
        final = await client.producer.create_music(
            audio_id=variation.audio_id,
            operation="swap_vocals",
            description="deep male vocals, powerful",
            wait_for_completion=True
        )

        print(f"✅ Final: {final.audio_url}")
```

### Upload, Modify, Download

```python
async def upload_modify_download():
    async with AIMusicClient() as client:
        # 1. Upload your music
        print("Uploading...")
        with open("original.mp3", "rb") as f:
            upload = await client.producer.upload_music(
                file=f,
                filename="original.mp3"
            )

        audio_id = upload.audio_id

        # 2. Extend it
        print("Extending...")
        extended = await client.producer.create_music(
            audio_id=audio_id,
            operation="extend",
            duration=30,
            wait_for_completion=True
        )

        # 3. Download as WAV
        print("Downloading WAV...")
        wav_url = await client.producer.download_music(
            audio_id=extended.audio_id,
            format="wav"
        )

        # 4. Download the file
        from rapperrok.utils import download_audio
        await download_audio(wav_url, "extended.wav")

        print("✅ Complete!")
```

### Vocal Replacement Workflow

```python
async def replace_vocals():
    async with AIMusicClient() as client:
        # Start with a song
        song = await client.producer.create_music(
            description="pop song with vocals",
            operation="create",
            duration=60,
            wait_for_completion=True
        )

        # Try different vocal styles
        styles = [
            "female vocals, powerful, soulful",
            "male vocals, raspy, rock style",
            "choir vocals, harmonized"
        ]

        results = []
        for style in styles:
            result = await client.producer.create_music(
                audio_id=song.audio_id,
                operation="swap_vocals",
                description=style,
                wait_for_completion=True
            )
            results.append(result)
            print(f"✅ {style}: {result.audio_url}")
```

## Best Practices

### 1. Choose the Right Operation

```python
# Create: Brand new music
create = await client.producer.create_music(
    description="jazz piano",
    operation="create"
)

# Extend: Make it longer
extend = await client.producer.create_music(
    audio_id=audio_id,
    operation="extend"
)

# Variation: Similar but different
variation = await client.producer.create_music(
    audio_id=audio_id,
    operation="variation",
    description="more upbeat"
)

# Swap: Change specific element
swap = await client.producer.create_music(
    audio_id=audio_id,
    operation="swap_vocals",
    description="different vocals"
)
```

### 2. Use Descriptive Prompts

```python
# ❌ Too vague
"change the music"

# ✅ Specific and clear
"add energetic drums and deep bass, increase tempo to 140 BPM, electronic style"
```

### 3. Upload Before Batch Operations

```python
# Upload once
with open("track.mp3", "rb") as f:
    upload = await client.producer.upload_music(f, "track.mp3")

audio_id = upload.audio_id

# Reuse audio_id for multiple operations
tasks = [
    client.producer.create_music(audio_id=audio_id, operation="variation", description="fast tempo"),
    client.producer.create_music(audio_id=audio_id, operation="variation", description="slow tempo"),
    client.producer.create_music(audio_id=audio_id, operation="swap_vocals", description="female vocals"),
]

results = await asyncio.gather(*tasks)
```

### 4. Check Credits

```python
credits = await client.get_credits()

if credits.available < 15:
    print("Not enough credits for vocal swap")
else:
    result = await client.producer.create_music(
        audio_id=audio_id,
        operation="swap_vocals",
        description="..."
    )
```

## Performance Tips

### Speed Comparison

| Model | Generation Time | Quality |
|-------|----------------|---------|
| Producer | ~30 seconds | High (Suno v5 comparable) |
| Suno V4 | ~60 seconds | Highest |
| Nuro | ~30 seconds | High |

### When to Use Producer

- ✅ Need fast generation
- ✅ Creating multiple variations
- ✅ Real-time applications
- ✅ Batch processing
- ✅ Prototyping and demos

### When to Use Suno Instead

- Need stems separation
- Want custom personas
- Need MIDI export
- Require absolute highest quality
- Working on professional productions

## Error Handling

```python
from rapperrok.exceptions import (
    TaskFailedError,
    InsufficientCreditsError,
    InvalidParameterError
)

try:
    result = await client.producer.create_music(
        description="...",
        operation="create",
        wait_for_completion=True
    )
except InsufficientCreditsError:
    print("Not enough credits")
except InvalidParameterError as e:
    print(f"Invalid parameter: {e.message}")
except TaskFailedError as e:
    print(f"Generation failed: {e.message}")
```

## Credit Costs

| Operation | Credits |
|-----------|---------|
| Create | 10 |
| Extend | 10 |
| Cover | 10 |
| Replace | 10 |
| Variation | 10 |
| Swap vocals | 15 |
| Swap instrumental | 15 |
| Upload | 0 (free) |
| Download | 0 (free) |

## API Reference

See [Producer API Reference](../api/producer.md) for complete documentation.

## Next Steps

- [Suno Guide](suno.md) - Studio-quality music
- [Nuro Guide](nuro.md) - Full-length songs
- [Webhook Integration](webhooks.md) - Async notifications
- [API Reference](../api/producer.md) - Complete API docs
