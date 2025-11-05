# Nuro API Guide

Complete guide to using the Nuro music generation model for creating full-length songs up to 4 minutes in just 30 seconds.

## Overview

**Nuro** is optimized for full-length song generation:

- 🎼 Complete 4-minute songs in 30 seconds
- 🎤 Vocal and instrumental modes
- 🎨 Extensive customization options
- ⚡ Fast generation time
- 🎵 Professional quality output

**Speed:** ~30 seconds generation time
**Max Duration:** 240 seconds (4 minutes)
**Quality:** High-quality, production-ready

## Vocal Music

### Create Song with Vocals

Generate complete songs with AI vocals:

```python
async with AIMusicClient() as client:
    result = await client.nuro.create_vocal_music(
        prompt="epic orchestral soundtrack with powerful choir vocals",
        duration=240,  # 4 minutes
        style="cinematic, dramatic, Hans Zimmer style",
        tempo=120,  # BPM
        key="C major",
        wait_for_completion=True
    )

    print(f"Audio: {result.audio_url}")
    print(f"Title: {result.title}")
    print(f"Duration: {result.duration}s")
```

**Parameters:**

- `prompt` (str): Description of the music
- `duration` (int): Length in seconds (30-240)
- `style` (str, optional): Musical style/genre
- `tempo` (int, optional): Beats per minute (60-200)
- `key` (str, optional): Musical key
- `mood` (str, optional): Emotional mood
- `instruments` (list, optional): Specific instruments
- `vocals_style` (str, optional): Vocal characteristics
- `wait_for_completion` (bool): Wait for generation

### Vocal Style Options

Customize vocal characteristics:

```python
result = await client.nuro.create_vocal_music(
    prompt="emotional ballad about lost love",
    duration=180,
    vocals_style="female, powerful, soulful, emotional",
    mood="melancholic",
    wait_for_completion=True
)
```

**Vocal Styles:**

- **Gender**: male, female, mixed
- **Character**: powerful, soft, raspy, smooth, breathy
- **Style**: operatic, pop, rock, jazz, folk
- **Effect**: layered, harmonized, solo

## Instrumental Music

### Create Instrumental Tracks

Generate music without vocals:

```python
async with AIMusicClient() as client:
    result = await client.nuro.create_instrumental_music(
        prompt="ambient electronic atmosphere for meditation",
        duration=240,
        style="ambient, electronic, peaceful",
        tempo=60,
        instruments=["synthesizer", "piano", "strings"],
        wait_for_completion=True
    )

    print(f"Audio: {result.audio_url}")
```

**Parameters:**

- `prompt` (str): Description of the music
- `duration` (int): Length in seconds (30-240)
- `style` (str, optional): Musical style
- `tempo` (int, optional): BPM
- `key` (str, optional): Musical key
- `mood` (str, optional): Emotional mood
- `instruments` (list, optional): Instrument list
- `wait_for_completion` (bool): Wait for completion

### Instrument Specification

Be specific about instruments:

```python
result = await client.nuro.create_instrumental_music(
    prompt="jazz composition",
    duration=180,
    instruments=[
        "piano",
        "double bass",
        "drums",
        "saxophone",
        "trumpet"
    ],
    style="jazz, bebop, 1950s",
    tempo=160,
    wait_for_completion=True
)
```

**Available Instruments:**

- **Strings**: violin, viola, cello, double bass, guitar, bass guitar
- **Brass**: trumpet, trombone, french horn, tuba
- **Woodwinds**: saxophone, clarinet, flute, oboe
- **Keys**: piano, organ, synthesizer, harpsichord
- **Percussion**: drums, congas, bongos, timpani
- **Electronic**: synth, drum machine, sampler

## Advanced Customization

### Musical Key

Specify the key of the composition:

```python
result = await client.nuro.create_vocal_music(
    prompt="uplifting pop song",
    duration=120,
    key="G major",  # Bright, happy key
    wait_for_completion=True
)
```

**Common Keys:**

- **Major** (happy): C, G, D, A, E, F major
- **Minor** (sad): A, E, D, G, C, F minor

### Tempo Control

Set specific BPM (beats per minute):

```python
# Slow ballad
slow = await client.nuro.create_vocal_music(
    prompt="emotional ballad",
    tempo=60,  # Slow
    duration=180,
    wait_for_completion=True
)

# Medium pop
medium = await client.nuro.create_vocal_music(
    prompt="pop song",
    tempo=120,  # Medium
    duration=180,
    wait_for_completion=True
)

# Fast dance
fast = await client.nuro.create_vocal_music(
    prompt="dance track",
    tempo=140,  # Fast
    duration=180,
    wait_for_completion=True
)
```

**Tempo Guidelines:**

- **Slow** (60-80 BPM): Ballads, ambient, meditation
- **Medium** (90-120 BPM): Pop, rock, folk
- **Fast** (130-160 BPM): Dance, electronic, punk
- **Very Fast** (170-200 BPM): Drum & bass, speed metal

### Mood Setting

Define the emotional character:

```python
result = await client.nuro.create_vocal_music(
    prompt="song about triumph",
    duration=180,
    mood="triumphant, uplifting, energetic, inspiring",
    wait_for_completion=True
)
```

**Mood Options:**

- **Happy**: joyful, uplifting, cheerful, playful
- **Sad**: melancholic, somber, nostalgic, reflective
- **Energetic**: powerful, aggressive, intense, driving
- **Calm**: peaceful, relaxing, ambient, serene
- **Dark**: ominous, mysterious, haunting, brooding

## Complete Workflows

### Full-Length Album Track

```python
async def create_album_track():
    async with AIMusicClient() as client:
        print("Creating full-length song...")

        result = await client.nuro.create_vocal_music(
            prompt="""
            A powerful rock anthem about overcoming adversity.
            Epic guitar solos, driving drums, anthemic vocals.
            Build from quiet intro to powerful chorus.
            """,
            duration=240,  # 4 minutes
            style="rock, anthem, epic, stadium rock",
            tempo=130,
            key="E minor",
            mood="powerful, inspiring, triumphant",
            vocals_style="male, powerful, raspy, rock vocals",
            instruments=[
                "electric guitar",
                "bass guitar",
                "drums",
                "piano",
                "strings"
            ],
            wait_for_completion=True
        )

        print(f"✅ Album track: {result.audio_url}")
        print(f"Title: {result.title}")
        print(f"Duration: {result.duration}s")

        # Download
        from rapperrok.utils import download_audio
        await download_audio(result.audio_url, "album_track.mp3")
```

### Background Music for Video

```python
async def create_background_music():
    async with AIMusicClient() as client:
        result = await client.nuro.create_instrumental_music(
            prompt="upbeat background music for product video",
            duration=90,
            style="corporate, uplifting, modern",
            tempo=120,
            mood="optimistic, professional",
            instruments=["piano", "guitar", "strings", "light percussion"],
            wait_for_completion=True
        )

        print(f"✅ Background music: {result.audio_url}")
```

### Meditation Music

```python
async def create_meditation_music():
    async with AIMusicClient() as client:
        result = await client.nuro.create_instrumental_music(
            prompt="calming meditation music with nature sounds",
            duration=240,  # 4 minutes
            style="ambient, new age, meditation",
            tempo=60,
            mood="peaceful, relaxing, tranquil",
            instruments=[
                "synthesizer",
                "piano",
                "tibetan singing bowls",
                "nature sounds"
            ],
            wait_for_completion=True
        )

        print(f"✅ Meditation music: {result.audio_url}")
```

### Genre-Specific Creation

```python
async def create_genre_specific():
    async with AIMusicClient() as client:
        # Jazz
        jazz = await client.nuro.create_instrumental_music(
            prompt="smooth jazz for evening lounge",
            duration=180,
            style="jazz, smooth jazz, bebop",
            tempo=120,
            instruments=["piano", "double bass", "drums", "saxophone"],
            mood="sophisticated, smooth",
            wait_for_completion=True
        )

        # Classical
        classical = await client.nuro.create_instrumental_music(
            prompt="romantic classical piano piece",
            duration=240,
            style="classical, romantic era, Chopin style",
            tempo=80,
            key="F minor",
            instruments=["piano"],
            mood="romantic, emotional, expressive",
            wait_for_completion=True
        )

        # EDM
        edm = await client.nuro.create_instrumental_music(
            prompt="high-energy EDM drop",
            duration=120,
            style="EDM, big room house, festival",
            tempo=128,
            instruments=["synthesizer", "drum machine", "bass synth"],
            mood="energetic, euphoric, intense",
            wait_for_completion=True
        )

        print("✅ All genres created!")
```

## Best Practices

### 1. Detailed Prompts

```python
# ❌ Too vague
prompt="a song"

# ✅ Detailed and specific
prompt="""
A cinematic orchestral piece that builds from a quiet piano intro
to a full orchestra climax. Inspired by Hans Zimmer. Features
sweeping strings, powerful brass, and epic percussion.
"""
```

### 2. Match Duration to Use Case

```python
# Social media clips
short = await client.nuro.create_instrumental_music(
    prompt="...",
    duration=30  # 30 seconds
)

# Background music
medium = await client.nuro.create_instrumental_music(
    prompt="...",
    duration=120  # 2 minutes
)

# Full songs
long = await client.nuro.create_vocal_music(
    prompt="...",
    duration=240  # 4 minutes
)
```

### 3. Use Style References

```python
result = await client.nuro.create_vocal_music(
    prompt="epic fantasy soundtrack",
    style="cinematic, orchestral, Howard Shore (LOTR), epic fantasy",
    mood="adventurous, majestic",
    duration=180,
    wait_for_completion=True
)
```

### 4. Batch Generation

```python
import asyncio

async def batch_create_music():
    async with AIMusicClient() as client:
        prompts = [
            ("upbeat pop", "pop", 120),
            ("calm jazz", "jazz", 100),
            ("epic rock", "rock", 140),
        ]

        tasks = [
            client.nuro.create_vocal_music(
                prompt=prompt,
                style=style,
                tempo=tempo,
                duration=180,
                wait_for_completion=False
            )
            for prompt, style, tempo in prompts
        ]

        # Start all tasks
        results = await asyncio.gather(*tasks)

        # Wait for completion
        completed = await asyncio.gather(*[
            client.nuro.wait_for_completion(r.task_id)
            for r in results
        ])

        return completed
```

## Error Handling

```python
from rapperrok.exceptions import (
    TaskFailedError,
    InsufficientCreditsError,
    InvalidParameterError
)

try:
    result = await client.nuro.create_vocal_music(
        prompt="...",
        duration=240,
        wait_for_completion=True
    )
except InsufficientCreditsError:
    print("Not enough credits for Nuro generation")
except InvalidParameterError as e:
    print(f"Invalid parameter: {e.message}")
except TaskFailedError as e:
    print(f"Generation failed: {e.message}")
```

## Performance Tips

### Speed Optimization

- Nuro generates in ~30 seconds regardless of duration
- Use batch operations for multiple tracks
- Don't wait_for_completion if you don't need immediate results

### Quality Optimization

- Be specific in prompts
- Use detailed style descriptions
- Specify instruments explicitly
- Set appropriate tempo and key

## Credit Costs

| Operation | Duration | Credits |
|-----------|----------|---------|
| Vocal music | 30-240s | 20 |
| Instrumental | 30-240s | 15 |

## Limitations

- **Max Duration**: 240 seconds (4 minutes)
- **Generation Time**: ~30 seconds
- **Prompt Length**: ~500 words
- **Rate Limits**: Subject to API limits

## Nuro vs Other Models

| Feature | Nuro | Suno V4 | Producer |
|---------|------|---------|----------|
| Max Duration | 240s | 240s | varies |
| Generation Time | ~30s | ~60s | ~30s |
| Vocals | ✅ | ✅ | ✅ |
| Instrumental | ✅ | ✅ | ✅ |
| Stems | ❌ | ✅ | ❌ |
| Personas | ❌ | ✅ | ❌ |
| MIDI Export | ❌ | ✅ | ❌ |
| Best For | Full songs | Professional production | Fast iterations |

## Use Cases

- **Full-length songs** for albums
- **Background music** for videos
- **Game soundtracks** and ambience
- **Meditation/relaxation** music
- **Podcast intros/outros**
- **Film scores** and trailers

## Next Steps

- [Suno Guide](suno.md) - Studio-quality with more features
- [Producer Guide](producer.md) - Fast iterations
- [Webhook Integration](webhooks.md) - Async notifications
- [API Reference](../api/nuro.md) - Complete API docs
