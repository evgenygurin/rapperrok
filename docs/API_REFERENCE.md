# AI Music API - Complete Reference

Comprehensive API reference for the AI Music API with links to official documentation.

## Table of Contents

- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [Suno API](#suno-api)
- [Producer API](#producer-api)
- [Nuro API](#nuro-api)
- [Riffusion API (Deprecated)](#riffusion-api-deprecated)
- [Shared Features](#shared-features)
- [Support & Resources](#support--resources)

---

## Getting Started

### Introduction & Overview

- **[AI Music API - Generate Music with Suno, Udio, Riffusion, Nuro Models](https://docs.aimusicapi.ai/ai-music-api-introduction.md)**
  Discover how the AI Music API allows you to generate music using 4 advanced models (Suno, Udio, Riffusion, Nuro). Supports multi-language, vocal/pure music creation with custom and random modes.

### Credits & Billing

- **[AI Music API Credits Usage Guide](https://docs.aimusicapi.ai/ai-music-api-credits-usage-guide.md)**
  Learn how to manage your credits with the AI Music API. Understand the unified credit system, monthly subscriptions, extra credits, and consumption rules for Suno, Riffusion, and Nuro models.

- **[Get Credits API](https://docs.aimusicapi.ai/get-credits.md)**
  Check your available credits for the AI Music API. Keep track of your usage and manage your subscription effectively.

### Error Handling

- **[AI Music API Error Handling Guide](https://docs.aimusicapi.ai/ai-music-api-error-handling-guide.md)**
  Learn how to handle errors efficiently while using the AI Music API. Explore common error codes, troubleshooting tips, and best practices to ensure smooth integration and usage.

### Webhooks

- **[Webhook Integration Guide](https://docs.aimusicapi.ai/webhook-guide.md)**
  Set up webhook notifications for asynchronous task completion.

---

## Core Concepts

### Models Overview

The AI Music API supports four powerful AI music generation models:

| Model | Speed | Max Duration | Best For |
|-------|-------|--------------|----------|
| **Suno V4** | 2 min | 2 min | Studio-quality vocals, stems separation, personas |
| **Producer (FUZZ-2.0)** | 30 sec | 2 min | Fast generation, professional mixing |
| **Nuro** | 30 sec | 4 min | Full-length songs, extensive customization |
| **Riffusion** | 60 sec | 2 min | Real-time generation (deprecated) |

### API Patterns

All models support:
- **Text-to-Music**: Generate from descriptions
- **Custom Lyrics**: Create songs with your own lyrics
- **Voice Control**: Male/female vocals, custom personas
- **Audio Manipulation**: Extend, cover, remix existing tracks

---

## Suno API

### Overview

- **[Suno AI Music Generation API | Studio-Quality Tracks in 2 min](https://docs.aimusicapi.ai/suno-api-instructions.md)**
  Create studio-level tracks with vocals or instrumentals in under 2 mins, customize lyrics & styles, and license everything commercially.

### Music Generation

#### Create Music

- **[Create Music API](https://docs.aimusicapi.ai/create-suno-music.md)**
  Use the `POST /create-music` API to generate AI-powered music with Suno V4. Convert text prompts into professional-quality music and AI vocals. Learn about request parameters, audio formats, and API best practices.

- **[Describe to Music API](https://docs.aimusicapi.ai/describe-music.md)**
  Use the `POST /describe-music` API to generate AI songs directly from a short text description. Leverage Suno and Riffusion models to turn your ideas into high-quality music with ease.

#### Customization

- **[Voice Gender API](https://docs.aimusicapi.ai/music-voice-gender.md)**
  Use the `voice-gender` parameter to select male or female vocals in AI-generated music. Works seamlessly with Suno and Riffusion models to give you full control over vocal character and tone.

- **[Lyrics & Style Generator](https://docs.aimusicapi.ai/custom-lyrics-style.md)**
  Enable `auto_lyrics` to let Suno or Riffusion generate lyrics and musical style from a description. Ideal for creating full custom songs from scratch using powerful AI models.

### Audio Manipulation

#### Extend Music

- **[Extend Music API](https://docs.aimusicapi.ai/extend-suno-music.md)**
  Use the `POST /extend-music` API to seamlessly extend AI-generated music with Suno V4. Maintain musical coherence and enhance audio quality with professional AI music generation.

#### Concatenate

- **[Concat Music API](https://docs.aimusicapi.ai/concat-suno-music.md)**
  Use the `POST /concat-music` API to merge AI-generated music segments into a seamless full-length track with Suno V4. Ensure smooth transitions and high-quality audio for professional music production.

#### Cover Music

- **[Cover Music API](https://docs.aimusicapi.ai/cover-suno-music.md)**
  Use the `POST /cover-music` API to create AI-generated song covers with Suno V4. Transform existing tracks with AI vocal synthesis and professional-quality audio.

### Audio Separation & Export

#### Stems Separation

- **[AI Music API – Stems Basic: Extract Vocals and Instrumental (2 Tracks)](https://docs.aimusicapi.ai/stems-basic.md)**
  Use AI Music API's Stems Basic feature to split any song by Song ID into two high-quality audio tracks: isolated vocals and pure instrumental. Perfect for karaoke, remixes, podcasts, and content creation.

- **[AI Music API – Stems Full: Extract 12 Detailed Tracks](https://docs.aimusicapi.ai/stems-full.md)**
  AI Music API's Stems Full feature extracts up to 12 individual stems from a song by Song ID, including lead vocals, backing vocals, drums, bass, piano, guitar, and more — giving creators maximum control for mixing and production.

#### Format Conversion

- **[AI Music API – Get WAV from Song ID](https://docs.aimusicapi.ai/wav.md)**
  Convert any generated song from MP3 to lossless WAV format by Song ID. Perfect for professional audio editing, mastering, and high-fidelity playback.

- **[Get MIDI Data](https://docs.aimusicapi.ai/get-midi.md)**
  Get the MIDI data of the specified clip id in Suno. Extract musical notation and composition data.

### Custom Voices (Personas)

- **[Create Persona API](https://docs.aimusicapi.ai/create-suno-persona.md)**
  Use the `POST /create-persona` API to generate a custom AI voice model from any song URL with Suno V4. Create your unique persona and use its vocal characteristics to generate new AI-powered music.

- **[Create Persona Music API](https://docs.aimusicapi.ai/create-suno-persona-music.md)**
  Use the `POST /create-persona-music` API to generate AI songs using your custom persona voice with Suno V4. Transform text into music with personalized AI vocals.

### Upload & Retrieve

- **[Upload Music API](https://docs.aimusicapi.ai/upload-suno-music.md)**
  Use the `POST /upload-music` API to upload and process your own music files with Suno V4. Enable AI-powered enhancements, remixing, and transformations.

- **[Get Music API](https://docs.aimusicapi.ai/get-suno-music.md)**
  Use the `GET /get-music` API to retrieve AI-generated music details using a task ID with Suno V4. Access metadata, download links, and processing status for your generated tracks.

---

## Producer API

### Overview

- **[Producer API Documentation - High-Quality Music Generation](https://docs.aimusicapi.ai/producer-api-overview.md)**
  Complete Producer API documentation for AI music generation. Create, extend, and remix professional tracks with Suno v5 quality in 30 seconds. FUZZ-2.0 model with studio-grade output.

- **[Producer API Request Examples - Complete Integration Guide](https://docs.aimusicapi.ai/producer-api-examples.md)**
  Comprehensive Producer API request examples for all operations: create, extend, cover, replace, swap vocals, swap instrumentals, and variations. Production-ready code samples with best practices.

### API Endpoints

- **[POST Create Music - Producer API Endpoint](https://docs.aimusicapi.ai/create-producer-music.md)**
  Producer API endpoint to generate AI music tracks. Supports create, extend, cover, replace, swap vocals/instrumentals, and variations. FUZZ-2.0 model with 30-second generation time.

- **[Upload Music to Producer API](https://docs.aimusicapi.ai/upload-music-producer.md)**
  Upload music to Producer API, get the audio ID, and use the clip ID to create music.

- **[Download Producer Music](https://docs.aimusicapi.ai/download-producer-music.md)**
  Download music files in specified format according to clip ID (mp3/wav).

- **[GET Music Task Status - Producer API Endpoint](https://docs.aimusicapi.ai/get-producer-music.md)**
  Query Producer API task status and retrieve generated music. Returns audio_url, video_url, metadata, and generation details. Free polling with no credit cost.

---

## Nuro API

### Overview

- **[Nuro API Overview - AI Music API](https://docs.aimusicapi.ai/nuro-api-overview.md)**
  Discover the Nuro music generation model, developed by MusicAPI and a tech company. Learn how it can generate a complete 4-minute song in just 30 seconds with extensive customization options.

### Music Generation

- **[Create Vocal Music - Nuro API](https://docs.aimusicapi.ai/create-vocal-music-nuro.md)**
  Generate high-quality vocal music using the Nuro API. Create customized vocal tracks tailored to your needs with fast, efficient processing.

- **[Create Instrumental Music - Nuro API](https://docs.aimusicapi.ai/create-instrument-music-nuro.md)**
  Generate instrument-only music using the Nuro API. Ideal for background scores, instrumental tracks, and more.

- **[Get Music - Nuro API](https://docs.aimusicapi.ai/get-music-nuro.md)**
  Retrieve the music generated by the Nuro API. Access your created tracks and explore various music generation options.

### Error Handling

- **[Nuro API Error Handling - AI Music API](https://docs.aimusicapi.ai/nuro-api-error-handling.md)**
  Learn how to handle errors when using the Nuro API. Get detailed information on common error codes and troubleshooting tips to ensure smooth integration with the AI music API.

---

## Riffusion API (Deprecated)

### Overview

- **[Riffusion AI Music Generation API | Studio-Quality Tracks in 60s](https://docs.aimusicapi.ai/riffusion-api-instructions.md)**
  Discover the Riffusion AI Music Generation API—create studio-level tracks with vocals or instrumentals in under 60 seconds, swap vocals & styles, and license everything commercially.

**Note**: Riffusion API is deprecated. Please use Suno V4 or Producer API for new projects.

### API Endpoints

- **[Create Music with Lyrics - Riffusion API](https://docs.aimusicapi.ai/create-music-with-lyrics-riffusion.md)**
  Generate unique music tracks with lyrics using the Riffusion API.

- **[Create Music with Description - Riffusion API](https://docs.aimusicapi.ai/create-music-with-description-riffusion.md)**
  Generate music based on a detailed description using Riffusion's API.

- **[Cover Music - Riffusion API](https://docs.aimusicapi.ai/cover-music-riffusion.md)**
  Easily create music covers with the Riffusion API for a new musical experience.

- **[Extend Music - Riffusion API](https://docs.aimusicapi.ai/extend-music-riffusion.md)**
  Extend existing music tracks with new elements using Riffusion's API.

- **[Replace Music Section - Riffusion API](https://docs.aimusicapi.ai/replace-music-section-riffusion.md)**
  Seamlessly replace sections of music to create a new version with Riffusion's API.

- **[Swap Music Sound - Riffusion API](https://docs.aimusicapi.ai/swap-music-sound-riffusion.md)**
  Swap different sounds in your music tracks using Riffusion's advanced API.

- **[Swap Music Vocals - Riffusion API](https://docs.aimusicapi.ai/swap-music-vocals-riffusion.md)**
  Replace vocals in music tracks while keeping the background music intact with Riffusion's API.

- **[Upload Music - Riffusion API](https://docs.aimusicapi.ai/upload-music-riffusion.md)**
  Upload your own music for further processing with the Riffusion API.

- **[Get Music - Riffusion API](https://docs.aimusicapi.ai/get-music-riffusion.md)**
  Retrieve generated music tracks with the Riffusion API to use in your projects.

---

## Shared Features

### Lyrics Generation

- **[Lyrics Generation - AI Music API](https://docs.aimusicapi.ai/lyrics-generation.md)**
  Generate song lyrics using the AI Music API. Create meaningful lyrics tailored to your music tracks with multiple variations.

### Credits Management

- **[Get Credits - AI Music API](https://docs.aimusicapi.ai/get-credits.md)**
  Check your available credits for the AI Music API. Keep track of your usage and manage your subscription effectively.

---

## Support & Resources

### Official Documentation

- **Main Website**: [https://aimusicapi.ai](https://aimusicapi.ai)
- **API Documentation**: [https://docs.aimusicapi.ai](https://docs.aimusicapi.ai)
- **Dashboard**: [https://aimusicapi.ai/dashboard](https://aimusicapi.ai/dashboard)
- **API Keys**: [https://aimusicapi.ai/dashboard/apikey](https://aimusicapi.ai/dashboard/apikey)

### Community & Support

- **Discord**: [https://discord.gg/UFT2J2XK7d](https://discord.gg/UFT2J2XK7d)
- **Changelog**: [https://aimusicapi.featurebase.app/en/changelog](https://aimusicapi.featurebase.app/en/changelog)

### RapperRok Client Library

- **GitHub**: [https://github.com/rapperrok/rapperrok](https://github.com/rapperrok/rapperrok)
- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
- **Issues**: [https://github.com/rapperrok/rapperrok/issues](https://github.com/rapperrok/rapperrok/issues)

---

## Quick Reference

### API Base URL

```
https://api.aimusicapi.ai
```

### Authentication

All API requests require an API key in the header:

```http
Authorization: Bearer sk_your_api_key_here
```

### Common Response Format

```json
{
  "task_id": "string",
  "status": "pending|processing|completed|failed",
  "clips": [
    {
      "id": "string",
      "audio_url": "string",
      "video_url": "string",
      "metadata": {}
    }
  ]
}
```

### Rate Limiting

- Automatic retry with exponential backoff recommended
- Use webhooks for long-running tasks
- Monitor credit usage with `/get-credits` endpoint

---

**Last Updated**: November 2025
**API Version**: v1
