# Suno V4 Guide

Comprehensive guide to using Suno V4, the highest quality AI music generation model supporting vocals, instrumentals, stems separation, and more.

## Overview

**Suno V4** provides studio-quality music generation with:

- 🎤 Vocals and instrumental tracks
- ✍️ Custom lyrics and auto-generation
- 🎵 Extend and concatenate music
- 🎨 Cover existing songs
- 🎼 Stems separation (2 or 12 tracks)
- 🗣️ Custom voice personas
- 📊 WAV and MIDI export
- ⚡ Voice gender control

## Creating Music

### From Description

Generate music from a text description:

```python
async with AIMusicClient() as client:
    result = await client.suno.create_music(
        description="upbeat electronic dance music with strong bass",
        duration=30,  # seconds (30, 60, 120, 180, or 240)
        voice_gender="female",  # "male", "female", or None
        wait_for_completion=True
    )

    print(f"Audio: {result.clips[0].audio_url}")
    print(f"Video: {result.clips[0].video_url}")
```

**Parameters:**

- `description` (str): Text description of the music
- `duration` (int): Length in seconds (30-240)
- `voice_gender` (str, optional): "male" or "female"
- `instrumental` (bool): True for no vocals
- `wait_for_completion` (bool): Wait for generation to complete

### With Custom Lyrics

Create music with your own lyrics:

```python
lyrics = """
[Verse 1]
Walking down the street today
Everything seems bright and gay

[Chorus]
This is my happy song
Singing all day long

[Verse 2]
Birds are chirping in the trees
Feeling such a gentle breeze

[Chorus]
This is my happy song
Singing all day long
"""

result = await client.suno.create_music_with_lyrics(
    lyrics=lyrics,
    style="pop, acoustic guitar, upbeat, cheerful",
    title="My Happy Song",
    voice_gender="male",
    wait_for_completion=True
)
```

**Parameters:**

- `lyrics` (str): Song lyrics with verse/chorus markers
- `style` (str): Musical style and instruments
- `title` (str, optional): Song title
- `voice_gender` (str, optional): Voice gender
- `instrumental` (bool): Instrumental version

### Auto-Generate Lyrics

Let Suno create lyrics from a description:

```python
result = await client.suno.describe_to_music(
    description="a sad breakup song about lost love",
    voice_gender="female",
    auto_lyrics=True,  # Suno generates lyrics
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

## Extending Music

### Extend Existing Track

Add more time to an existing track while maintaining musical coherence:

```python
# First, create a song
initial = await client.suno.create_music(
    description="rock song with electric guitar",
    duration=30,
    wait_for_completion=True
)

audio_id = initial.clips[0].id

# Extend it by 60 seconds
extended = await client.suno.extend_music(
    audio_id=audio_id,
    duration=60,  # Additional duration
    wait_for_completion=True
)

print(f"Extended: {extended.clips[0].audio_url}")
```

**Use Cases:**

- Make songs longer
- Continue the musical theme
- Create variations

## Concatenating Tracks

### Merge Multiple Clips

Seamlessly merge multiple clips into one track:

```python
# Create multiple clips
clip1 = await client.suno.create_music(
    description="intro with soft piano",
    duration=30,
    wait_for_completion=True
)

clip2 = await client.suno.create_music(
    description="energetic rock section",
    duration=60,
    wait_for_completion=True
)

clip3 = await client.suno.create_music(
    description="calm outro with strings",
    duration=30,
    wait_for_completion=True
)

# Concatenate them
full_track = await client.suno.concat_music(
    clip_ids=[
        clip1.clips[0].id,
        clip2.clips[0].id,
        clip3.clips[0].id
    ],
    wait_for_completion=True
)

print(f"Full track: {full_track.audio_url}")
```

**Benefits:**

- Create complex arrangements
- Build dynamic songs with different sections
- Smooth transitions between clips

## Cover Versions

### Create AI Cover

Transform an existing song with AI:

```python
result = await client.suno.cover_music(
    audio_url="https://example.com/original_song.mp3",
    style="jazz piano, smooth vocals",
    wait_for_completion=True
)
```

**Parameters:**

- `audio_url` (str): URL of the original song
- `style` (str): Target musical style
- `voice_gender` (str, optional): Voice gender for cover

## Stems Separation

### Basic Stems (2 Tracks)

Separate vocals and instrumentals:

```python
# First, create a song
song = await client.suno.create_music(
    description="rock song with vocals",
    duration=30,
    wait_for_completion=True
)

song_id = song.clips[0].id

# Separate stems
stems = await client.suno.stems_basic(song_id=song_id)

print(f"Vocals: {stems.vocals_url}")
print(f"Instrumental: {stems.instrumental_url}")
```

**Cost:** 20 credits

**Use Cases:**

- Karaoke tracks
- Remixing
- Vocal analysis
- Background music

### Full Stems (12 Tracks)

Extract 12 individual instrument/vocal tracks:

```python
stems = await client.suno.stems_full(song_id=song_id)

# Available stems:
print(f"Lead Vocals: {stems.lead_vocals_url}")
print(f"Backing Vocals: {stems.backing_vocals_url}")
print(f"Drums: {stems.drums_url}")
print(f"Bass: {stems.bass_url}")
print(f"Piano: {stems.piano_url}")
print(f"Guitar: {stems.guitar_url}")
print(f"Strings: {stems.strings_url}")
print(f"Synth: {stems.synth_url}")
print(f"Brass: {stems.brass_url}")
print(f"Woodwinds: {stems.woodwinds_url}")
print(f"Percussion: {stems.percussion_url}")
print(f"Effects: {stems.effects_url}")
```

**Cost:** 50 credits

**Use Cases:**

- Professional mixing
- Full remixing control
- Music production
- Educational purposes

## Custom Voice Personas

### Create Persona from Song

Train a custom AI voice model from any song:

```python
# Create persona from a song URL
persona = await client.suno.create_persona(
    song_url="https://example.com/reference_song.mp3",
    persona_name="My Custom Voice",
    wait_for_completion=True
)

persona_id = persona.persona_id
print(f"Persona created: {persona_id}")
```

**Cost:** 50 credits

### Use Persona in Generation

```python
# Generate music with custom persona
result = await client.suno.create_persona_music(
    persona_id=persona_id,
    lyrics="Your custom lyrics here...",
    style="pop, upbeat",
    title="Song with My Voice",
    wait_for_completion=True
)
```

**Use Cases:**

- Clone a specific voice style
- Create consistent voice across songs
- Personalized AI vocals

## File Upload and Processing

### Upload Your Own Music

Upload and process your own audio files:

```python
# Upload from local file
with open("my_music.mp3", "rb") as f:
    upload_result = await client.suno.upload_music(
        file=f,
        filename="my_music.mp3"
    )

audio_id = upload_result.audio_id

# Now use it for operations (extend, cover, stems, etc.)
extended = await client.suno.extend_music(
    audio_id=audio_id,
    duration=60,
    wait_for_completion=True
)
```

**Supported Formats:**

- MP3
- WAV
- FLAC
- OGG

## Format Conversion

### Export to WAV

Convert generated music to high-quality WAV format:

```python
# Create music
song = await client.suno.create_music(
    description="orchestral symphony",
    duration=60,
    wait_for_completion=True
)

song_id = song.clips[0].id

# Export to WAV
wav_result = await client.suno.get_wav(song_id=song_id)

print(f"WAV file: {wav_result.wav_url}")
```

**Cost:** 10 credits

**Benefits:**

- Lossless audio quality
- Professional production
- Audio editing compatibility

### Export to MIDI

Extract MIDI data from generated music:

```python
midi_result = await client.suno.get_midi(song_id=song_id)

print(f"MIDI file: {midi_result.midi_url}")
```

**Cost:** 5 credits

**Use Cases:**

- Music notation
- MIDI sequencing
- Music theory analysis
- DAW integration

## Advanced Operations

### Voice Gender Control

Control the gender of AI-generated vocals:

```python
# Male vocals
male_song = await client.suno.create_music(
    description="powerful rock ballad",
    voice_gender="male",
    wait_for_completion=True
)

# Female vocals
female_song = await client.suno.create_music(
    description="emotional pop song",
    voice_gender="female",
    wait_for_completion=True
)

# Random/auto-selected gender
auto_song = await client.suno.create_music(
    description="jazz melody",
    voice_gender=None,  # or omit parameter
    wait_for_completion=True
)
```

### Style and Genre Specification

Be specific about musical style:

```python
result = await client.suno.create_music_with_lyrics(
    lyrics="Your lyrics...",
    style="indie rock, acoustic guitar, lo-fi, melancholic, 90s alt-rock",
    wait_for_completion=True
)
```

**Style Tips:**

- Be specific: "indie rock" vs "rock"
- Include instruments: "acoustic guitar, piano, strings"
- Add mood: "melancholic", "upbeat", "aggressive"
- Reference eras: "90s", "80s synthwave"
- Include production style: "lo-fi", "studio quality"

## Complete Workflow Examples

### Create, Extend, and Export

```python
async def complete_song_workflow():
    async with AIMusicClient() as client:
        # 1. Create initial track
        print("Creating initial track...")
        initial = await client.suno.create_music(
            description="epic orchestral intro",
            duration=30,
            instrumental=True,
            wait_for_completion=True
        )

        audio_id = initial.clips[0].id

        # 2. Extend the track
        print("Extending track...")
        extended = await client.suno.extend_music(
            audio_id=audio_id,
            duration=90,
            wait_for_completion=True
        )

        song_id = extended.clips[0].id

        # 3. Export to WAV for production
        print("Exporting to WAV...")
        wav = await client.suno.get_wav(song_id=song_id)

        # 4. Get MIDI for editing
        print("Exporting MIDI...")
        midi = await client.suno.get_midi(song_id=song_id)

        print(f"✅ Complete!")
        print(f"Audio: {extended.clips[0].audio_url}")
        print(f"WAV: {wav.wav_url}")
        print(f"MIDI: {midi.midi_url}")
```

### Vocal Removal and Remix

```python
async def vocal_remix_workflow():
    async with AIMusicClient() as client:
        # 1. Create song with vocals
        song = await client.suno.create_music(
            description="pop song with vocals",
            duration=60,
            wait_for_completion=True
        )

        song_id = song.clips[0].id

        # 2. Separate vocals and instrumental
        stems = await client.suno.stems_basic(song_id=song_id)

        print(f"✅ Separated!")
        print(f"Vocals: {stems.vocals_url}")
        print(f"Instrumental: {stems.instrumental_url}")

        # Now you can download and remix them separately
```

### Multi-Section Song Creation

```python
async def create_multi_section_song():
    async with AIMusicClient() as client:
        # Create different sections
        print("Creating intro...")
        intro = await client.suno.create_music(
            description="soft piano intro, ambient",
            duration=20,
            instrumental=True,
            wait_for_completion=True
        )

        print("Creating verse...")
        verse = await client.suno.create_music_with_lyrics(
            lyrics="[Verse]\nYour lyrics here...",
            style="pop, acoustic",
            duration=30,
            wait_for_completion=True
        )

        print("Creating chorus...")
        chorus = await client.suno.create_music_with_lyrics(
            lyrics="[Chorus]\nChorus lyrics...",
            style="pop, energetic, full band",
            duration=30,
            wait_for_completion=True
        )

        print("Creating outro...")
        outro = await client.suno.create_music(
            description="fade out with strings",
            duration=20,
            instrumental=True,
            wait_for_completion=True
        )

        # Concatenate all sections
        print("Merging sections...")
        full_song = await client.suno.concat_music(
            clip_ids=[
                intro.clips[0].id,
                verse.clips[0].id,
                chorus.clips[0].id,
                verse.clips[0].id,
                chorus.clips[0].id,
                outro.clips[0].id
            ],
            wait_for_completion=True
        )

        print(f"✅ Complete song: {full_song.audio_url}")
```

## Best Practices

### 1. Lyrics Formatting

Use standard song structure markers:

```
[Intro]
[Verse 1]
[Pre-Chorus]
[Chorus]
[Verse 2]
[Chorus]
[Bridge]
[Chorus]
[Outro]
```

### 2. Description Writing

Be specific and descriptive:

```python
# ❌ Not specific enough
"a song"

# ✅ Good description
"upbeat indie rock with jangly guitars, driving drums, and nostalgic 90s alt-rock vibes"
```

### 3. Duration Selection

Choose appropriate durations:

- **30s**: Quick demos, social media clips
- **60s**: Short songs, intro/outro
- **120s**: Full songs
- **180-240s**: Extended tracks, ambient music

### 4. Credit Management

Check costs before operations:

```python
# Check credits
credits = await client.get_credits()
print(f"Available: {credits.available}")

# Plan operations based on costs
if credits.available >= 50:
    # Can afford full stems
    stems = await client.suno.stems_full(song_id)
elif credits.available >= 20:
    # Can afford basic stems
    stems = await client.suno.stems_basic(song_id)
else:
    print("Insufficient credits")
```

### 5. Error Handling

Always handle potential failures:

```python
from rapperrok.exceptions import TaskFailedError, InsufficientCreditsError

try:
    result = await client.suno.create_music(
        description="...",
        wait_for_completion=True
    )
except InsufficientCreditsError:
    print("Not enough credits")
except TaskFailedError as e:
    print(f"Generation failed: {e.message}")
```

## Credit Costs Summary

| Operation | Credits |
|-----------|---------|
| Create music | 10 |
| Extend music | 10 |
| Concat music | 5 |
| Cover music | 10 |
| Stems basic (2 tracks) | 20 |
| Stems full (12 tracks) | 50 |
| Create persona | 50 |
| Persona music | 10 |
| WAV export | 10 |
| MIDI export | 5 |
| Upload music | 0 (free) |

## Limitations

- **Duration**: Maximum 240 seconds per generation
- **Lyrics**: ~500 words maximum
- **File Upload**: Max 50MB
- **Rate Limits**: Subject to API rate limiting
- **Concurrent Tasks**: Limited by your plan

## Troubleshooting

### Generation Failed

- Check your description is clear and specific
- Ensure lyrics are properly formatted
- Verify sufficient credits
- Try shorter duration

### Poor Quality Output

- Be more specific in description
- Use detailed style parameters
- Try different voice_gender settings
- Regenerate with different prompt

### Stems Separation Issues

- Ensure song has clear vocals/instruments
- Try with different songs
- Use basic stems first to test

## Next Steps

- [Producer Guide](producer.md) - Fast music generation
- [Nuro Guide](nuro.md) - Full-length songs
- [Webhook Integration](webhooks.md) - Async notifications
- [Error Handling](error-handling.md) - Handle errors
- [API Reference](../api/suno.md) - Complete Suno API docs
