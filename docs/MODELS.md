# AI Music Generation Models

Comprehensive comparison and guide to all AI music generation models supported by the AI Music API.

## Table of Contents

- [Models Overview](#models-overview)
- [Suno V4](#suno-v4)
- [Producer (FUZZ-2.0)](#producer-fuzz-20)
- [Nuro](#nuro)
- [Riffusion (Deprecated)](#riffusion-deprecated)
- [Model Comparison](#model-comparison)
- [Choosing the Right Model](#choosing-the-right-model)

---

## Models Overview

The AI Music API provides four distinct AI music generation models, each optimized for different use cases:

| Model | Status | Generation Time | Max Duration | Quality | Best Use Case |
|-------|--------|----------------|--------------|---------|---------------|
| **Suno V4** | ✅ Active | ~2 min | 2 min | Studio-quality | Professional vocals, stems separation |
| **Producer** | ✅ Active | ~30 sec | 2 min | High-quality | Fast generation, mixing, remixing |
| **Nuro** | ✅ Active | ~30 sec | 4 min | High-quality | Full-length songs, instrumentals |
| **Riffusion** | ⚠️ Deprecated | ~60 sec | 2 min | Good | Legacy projects only |

---

## Suno V4

### Overview

Suno V4 is the flagship model for studio-quality music generation with advanced vocal synthesis and comprehensive audio manipulation capabilities.

**Generation Time**: ~2 minutes
**Max Duration**: 2 minutes per generation
**Quality**: Studio-grade
**Commercial Use**: ✅ Licensed

### Key Features

#### 1. Music Generation
- **Text-to-Music**: Generate from descriptions
- **Custom Lyrics**: Create songs with your own lyrics
- **Auto-Lyrics**: AI-generated lyrics from descriptions
- **Voice Gender Control**: Male, female, or neutral vocals
- **Instrumental Mode**: Pure instrumental tracks

#### 2. Audio Manipulation
- **Extend**: Seamlessly extend existing tracks
- **Concatenate**: Merge multiple clips into one track
- **Cover**: Create cover versions of existing songs
- **Replace**: Replace sections of music

#### 3. Advanced Features
- **Stems Separation**:
  - **Basic**: 2 tracks (vocals + instrumental)
  - **Full**: 12 tracks (lead vocals, backing vocals, drums, bass, piano, guitar, synth, strings, brass, other, mix, background)
- **Custom Personas**: Create AI voice models from any song
- **Format Export**: WAV and MIDI export
- **Upload Processing**: Process your own audio files

### Use Cases

- 🎤 Professional vocal tracks
- 🎵 Complete song composition
- 🎧 Music remixing and stems extraction
- 🎹 MIDI composition export
- 🎬 Video soundtracks
- 🎙️ Podcast intros and outros

### Credits Cost

| Operation | Credits |
|-----------|---------|
| Create music | 10 |
| Extend music | 10 |
| Concat music | 5 |
| Cover music | 10 |
| Stems basic | 20 |
| Stems full | 50 |
| Create persona | 50 |
| WAV export | 10 |
| MIDI export | 5 |

### Example

```python
from rapperrok import AIMusicClient

client = AIMusicClient()

# Create studio-quality vocal track
result = await client.suno.create_music(
    description="emotional piano ballad about lost love",
    duration=120,
    voice_gender="female",
    auto_lyrics=True
)

# Extract stems for remixing
stems = await client.suno.stems_full(song_id=result.clips[0].id)
print(f"Lead vocals: {stems.lead_vocals_url}")
print(f"Drums: {stems.drums_url}")
print(f"Bass: {stems.bass_url}")
```

### Documentation

- [Suno API Instructions](https://docs.aimusicapi.ai/suno-api-instructions.md)
- [Complete Suno Endpoints](https://docs.aimusicapi.ai/create-suno-music.md)

---

## Producer (FUZZ-2.0)

### Overview

Producer is powered by the FUZZ-2.0 model and optimized for ultra-fast, high-quality music generation with professional mixing capabilities.

**Generation Time**: ~30 seconds
**Max Duration**: 2 minutes per generation
**Quality**: Professional studio-grade (Suno v5 quality)
**Commercial Use**: ✅ Licensed

### Key Features

#### 1. Fast Generation
- **30-Second Turnaround**: Fastest model available
- **High Quality**: Suno v5-level quality output
- **Professional Mixing**: Studio-grade audio balance

#### 2. Operations
- **Create**: Generate new tracks from scratch
- **Extend**: Extend existing tracks
- **Cover**: Create cover versions
- **Replace**: Replace sections
- **Swap Vocals**: Replace vocal tracks
- **Swap Instrumentals**: Replace instrumental backing
- **Variations**: Generate variations of existing tracks

#### 3. Audio Processing
- **Upload Support**: Process your own audio
- **Multi-Format Download**: MP3 and WAV export
- **Video Generation**: Includes video URL in responses

### Use Cases

- ⚡ Rapid prototyping
- 🎚️ Professional mixing and mastering
- 🔄 Quick remixes and variations
- 🎤 Vocal replacement and swapping
- 🎼 Instrumental backing track generation
- 🎞️ Content creation (includes video)

### Credits Cost

| Operation | Credits |
|-----------|---------|
| Create music | 10 |
| Extend music | 10 |
| Cover music | 10 |
| Replace section | 10 |
| Swap vocals | 15 |
| Swap instrumental | 15 |
| Create variation | 10 |

### Example

```python
from rapperrok import AIMusicClient

client = AIMusicClient()

# Ultra-fast music generation
result = await client.producer.create_music(
    description="energetic EDM track with drops",
    operation="create",
    duration=60
)
# Ready in ~30 seconds!

# Swap vocals while keeping instrumentals
swapped = await client.producer.create_music(
    audio_id="clip_xyz",
    operation="swap_vocals",
    description="female pop vocals"
)
```

### Documentation

- [Producer API Overview](https://docs.aimusicapi.ai/producer-api-overview.md)
- [Producer API Examples](https://docs.aimusicapi.ai/producer-api-examples.md)
- [Create Producer Music](https://docs.aimusicapi.ai/create-producer-music.md)

---

## Nuro

### Overview

Nuro is designed for generating complete, full-length songs with extensive customization options. Can generate up to 4 minutes in just 30 seconds.

**Generation Time**: ~30 seconds
**Max Duration**: 4 minutes per generation
**Quality**: High-quality
**Commercial Use**: ✅ Licensed

### Key Features

#### 1. Full-Length Songs
- **4-Minute Tracks**: Longest generation support
- **Fast Generation**: Complete songs in 30 seconds
- **Continuous Composition**: Coherent full-length tracks

#### 2. Mode Support
- **Vocal Music**: Songs with AI-generated vocals
- **Instrumental Music**: Pure instrumental tracks
- **Style Variety**: Wide range of genres and styles

#### 3. Customization
- **Extensive Style Control**: Detailed genre and mood specification
- **Prompt Engineering**: Advanced text-to-music prompts
- **Duration Flexibility**: From short clips to 4-minute songs

### Use Cases

- 📻 Full-length song creation
- 🎼 Background music for videos (long-form)
- 🎮 Game soundtracks
- 📺 TV and film background scores
- 🏪 Commercial background music
- 🎧 Ambient and atmospheric tracks

### Credits Cost

| Operation | Credits |
|-----------|---------|
| Create vocal music | 20 |
| Create instrumental | 15 |

### Example

```python
from rapperrok import AIMusicClient

client = AIMusicClient()

# Generate complete 4-minute song
song = await client.nuro.create_vocal_music(
    prompt="epic orchestral soundtrack with choir and dramatic crescendos",
    duration=240,  # 4 minutes
    style="cinematic"
)

# Generate long instrumental
instrumental = await client.nuro.create_instrumental_music(
    prompt="ambient electronic atmosphere for meditation",
    duration=240
)
```

### Documentation

- [Nuro API Overview](https://docs.aimusicapi.ai/nuro-api-overview.md)
- [Create Vocal Music - Nuro](https://docs.aimusicapi.ai/create-vocal-music-nuro.md)
- [Create Instrumental Music - Nuro](https://docs.aimusicapi.ai/create-instrument-music-nuro.md)
- [Nuro Error Handling](https://docs.aimusicapi.ai/nuro-api-error-handling.md)

---

## Riffusion (Deprecated)

### Overview

⚠️ **Riffusion is deprecated and not recommended for new projects.** Use Suno V4 or Producer instead.

**Generation Time**: ~60 seconds
**Max Duration**: 2 minutes
**Status**: Deprecated - maintenance mode only

### Migration Path

| Riffusion Feature | Recommended Alternative |
|------------------|------------------------|
| Create with lyrics | ➡️ Suno V4: `create_music_with_lyrics` |
| Create with description | ➡️ Producer: `create_music` |
| Extend music | ➡️ Suno V4: `extend_music` |
| Cover music | ➡️ Producer: `create_music(operation="cover")` |
| Swap vocals | ➡️ Producer: `create_music(operation="swap_vocals")` |

### Documentation (Legacy)

- [Riffusion API Instructions](https://docs.aimusicapi.ai/riffusion-api-instructions.md)

---

## Model Comparison

### Feature Matrix

| Feature | Suno V4 | Producer | Nuro | Riffusion |
|---------|---------|----------|------|-----------|
| **Generation Speed** | 2 min | **30 sec** | **30 sec** | 60 sec |
| **Max Duration** | 2 min | 2 min | **4 min** | 2 min |
| **Vocal Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Custom Lyrics** | ✅ | ✅ | ✅ | ✅ |
| **Voice Gender Control** | ✅ | ✅ | ✅ | ✅ |
| **Stems Separation** | ✅ (2 or 12) | ❌ | ❌ | ❌ |
| **Custom Personas** | ✅ | ❌ | ❌ | ❌ |
| **MIDI Export** | ✅ | ❌ | ❌ | ❌ |
| **WAV Export** | ✅ | ✅ | ❌ | ❌ |
| **Video Generation** | ✅ | ✅ | ❌ | ❌ |
| **Extend Music** | ✅ | ✅ | ❌ | ✅ |
| **Cover Music** | ✅ | ✅ | ❌ | ✅ |
| **Swap Vocals** | ❌ | ✅ | ❌ | ✅ |
| **Swap Instrumentals** | ❌ | ✅ | ❌ | ❌ |
| **Status** | Active | Active | Active | Deprecated |

### Performance Comparison

```
Generation Time (seconds)
┌─────────────────────────────────────────┐
│ Producer    [████] 30s                  │
│ Nuro        [████] 30s                  │
│ Riffusion   [████████] 60s              │
│ Suno V4     [████████████████] 120s     │
└─────────────────────────────────────────┘

Max Track Duration (minutes)
┌─────────────────────────────────────────┐
│ Suno V4     [████████] 2 min            │
│ Producer    [████████] 2 min            │
│ Riffusion   [████████] 2 min            │
│ Nuro        [████████████████] 4 min    │
└─────────────────────────────────────────┘

Quality (1-5 stars)
┌─────────────────────────────────────────┐
│ Suno V4     [⭐⭐⭐⭐⭐] Studio           │
│ Producer    [⭐⭐⭐⭐⭐] Studio           │
│ Nuro        [⭐⭐⭐⭐] High-quality       │
│ Riffusion   [⭐⭐⭐] Good                │
└─────────────────────────────────────────┘
```

---

## Choosing the Right Model

### Decision Tree

```
Need full 4-minute songs?
├─ YES → Use Nuro
└─ NO → Continue

Need stems separation or MIDI?
├─ YES → Use Suno V4
└─ NO → Continue

Need fastest generation (<30s)?
├─ YES → Use Producer
└─ NO → Continue

Need vocal swapping or professional mixing?
├─ YES → Use Producer
└─ NO → Use Suno V4 (most versatile)
```

### Use Case Recommendations

#### For Content Creators
- **YouTube/TikTok Videos**: Producer (fast turnaround)
- **Podcast Intros**: Suno V4 (best vocal quality)
- **Long-form Content**: Nuro (4-minute tracks)

#### For Musicians
- **Song Composition**: Suno V4 (MIDI export, stems)
- **Quick Demos**: Producer (30-second generation)
- **Remixing**: Suno V4 (stems separation)
- **Cover Songs**: Producer or Suno V4

#### For Developers
- **Rapid Prototyping**: Producer (fastest)
- **High Volume**: Producer (best speed/cost ratio)
- **Complex Features**: Suno V4 (most capabilities)

#### For Businesses
- **Background Music**: Nuro (long tracks)
- **Commercials**: Producer (fast + high quality)
- **Custom Jingles**: Suno V4 (custom personas)

### Credits Optimization

**Most Economical**:
- Simple creation: Any model (10 credits)
- Batch operations: Producer (fastest = lowest cost per hour of content)

**Best Value**:
- Complex projects: Suno V4 (most features per credit)
- Long tracks: Nuro (4 min for 20 credits vs 2×2 min for 20 credits)

**Most Expensive**:
- Stems Full: 50 credits (but provides 12 separate tracks)
- Custom Personas: 50 credits (but reusable for multiple songs)

---

## Model Roadmap

### Current Status (November 2025)

- ✅ **Suno V4**: Fully operational
- ✅ **Producer (FUZZ-2.0)**: Fully operational
- ✅ **Nuro**: Fully operational
- ⚠️ **Riffusion**: Deprecated, maintenance mode

### Upcoming Features

Check the [Changelog](https://aimusicapi.featurebase.app/en/changelog) for the latest updates.

---

## Technical Specifications

### Audio Formats

| Model | Default Format | Available Formats | Sample Rate | Bit Rate |
|-------|---------------|-------------------|-------------|----------|
| Suno V4 | MP3 | MP3, WAV | 44.1 kHz | 320 kbps |
| Producer | MP3 | MP3, WAV | 44.1 kHz | 320 kbps |
| Nuro | MP3 | MP3 | 44.1 kHz | 192 kbps |
| Riffusion | MP3 | MP3 | 44.1 kHz | 192 kbps |

### API Limits

- **Rate Limiting**: Automatic retry recommended
- **Concurrent Requests**: Depends on subscription tier
- **Max File Upload**: 100 MB
- **Timeout**: 600 seconds (10 minutes) recommended

### Regional Availability

All models available in all regions. API hosted at:
```
https://api.aimusicapi.ai
```

---

**Last Updated**: November 2025
