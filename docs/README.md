# RapperRok Documentation

Welcome to the RapperRok documentation! This directory contains comprehensive guides for using the RapperRok Python client with the AI Music API.

## 📚 Documentation Index

### Core Documentation

#### [API Reference](./API_REFERENCE.md)
Complete API reference with links to all official AI Music API documentation, organized by model and functionality. Includes:
- Getting Started guides (Introduction, Credits, Error Handling, Webhooks)
- Suno API documentation (Create, Extend, Stems, Personas, etc.)
- Producer API documentation (FUZZ-2.0 model)
- Nuro API documentation (Full-length songs)
- Riffusion API documentation (Deprecated)
- Shared features (Lyrics generation, Credits management)

#### [Models Guide](./MODELS.md)
Detailed comparison and guide to all AI music generation models. Includes:
- Complete feature matrices and performance comparisons
- Decision trees for choosing the right model
- Use case recommendations for different scenarios
- Credits cost optimization strategies
- Technical specifications and audio formats
- Code examples for each model

#### [Endpoints Reference](./ENDPOINTS.md)
Complete API endpoints reference with practical examples. Includes:
- All endpoints organized by model
- Request/response examples in JSON
- Credits costs per operation
- HTTP status codes and error handling
- Rate limiting details and retry strategies
- Webhook integration and verification
- Best practices for production use

---

## 🚀 Quick Start

New to RapperRok? Start here:

1. **[Installation Guide](../README.md#installation)** - Install RapperRok with uv or pip
2. **[Quick Start Guide](../QUICKSTART.md)** - Get up and running in 5 minutes
3. **[Examples](../examples/README.md)** - Working code examples for all features
4. **[API Reference](./API_REFERENCE.md)** - Complete API documentation

---

## 🎵 Choose Your Model

Not sure which AI model to use? Here's a quick guide:

### Suno V4 - Best for Professional Quality
- ⭐ Studio-quality vocals
- 🎹 MIDI and WAV export
- 🎚️ Stems separation (2 or 12 tracks)
- 🎤 Custom voice personas
- **Use when**: You need the highest quality, stems, or custom voices

**[Suno Documentation →](./API_REFERENCE.md#suno-api)**

### Producer (FUZZ-2.0) - Best for Speed
- ⚡ 30-second generation time
- 🎚️ Professional mixing
- 🔄 Vocal/instrumental swapping
- 🎞️ Includes video generation
- **Use when**: You need fast turnaround with high quality

**[Producer Documentation →](./API_REFERENCE.md#producer-api)**

### Nuro - Best for Long Tracks
- 📻 Up to 4-minute songs
- ⚡ Fast generation (30 seconds)
- 🎼 Vocal and instrumental modes
- 🎮 Perfect for game soundtracks
- **Use when**: You need longer tracks or full songs

**[Nuro Documentation →](./API_REFERENCE.md#nuro-api)**

**[Detailed Model Comparison →](./MODELS.md)**

---

## 📖 Documentation by Topic

### Music Generation
- [Create Music from Text](./ENDPOINTS.md#post-v1sunocreate-music) (Suno)
- [Create Music with Custom Lyrics](./ENDPOINTS.md#post-v1sunocreate-music-with-lyrics) (Suno)
- [Fast Music Generation](./ENDPOINTS.md#post-v1producercreate-music) (Producer)
- [Full-Length Songs](./ENDPOINTS.md#post-v1nurocreate-vocal-music) (Nuro)

### Audio Manipulation
- [Extend Music Tracks](./ENDPOINTS.md#post-v1sunoextend-music)
- [Concatenate Multiple Clips](./ENDPOINTS.md#post-v1sunoconcat-music)
- [Create Cover Versions](./ENDPOINTS.md#post-v1sunocover-music)
- [Swap Vocals](./ENDPOINTS.md#post-v1producercreate-music) (Producer - swap_vocals)
- [Swap Instrumentals](./ENDPOINTS.md#post-v1producercreate-music) (Producer - swap_instrumentals)

### Advanced Features
- [Stems Separation (Basic - 2 tracks)](./ENDPOINTS.md#post-v1sunostems-basic)
- [Stems Separation (Full - 12 tracks)](./ENDPOINTS.md#post-v1sunostems-full)
- [Create Custom Voice Personas](./ENDPOINTS.md#post-v1sunocreate-persona)
- [WAV Export](./ENDPOINTS.md#post-v1sunowav)
- [MIDI Export](./ENDPOINTS.md#get-v1sunoget-midi)

### Integration & Management
- [Webhook Integration](./API_REFERENCE.md#webhooks)
- [Credits Management](./ENDPOINTS.md#get-v1credits)
- [Error Handling](./API_REFERENCE.md#error-handling)
- [Rate Limiting](./ENDPOINTS.md#rate-limiting)

---

## 💻 Code Examples

### Basic Usage

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        # Generate music with Suno
        result = await client.suno.create_music(
            description="upbeat electronic dance music",
            duration=60,
            wait_for_completion=True
        )
        print(f"Audio URL: {result.clips[0].audio_url}")

asyncio.run(main())
```

### More Examples

- [Basic Usage Examples](../examples/01_basic_usage.py)
- [Advanced Suno Features](../examples/02_advanced_suno.py)
- [Producer Operations](../examples/03_producer_operations.py)
- [Webhook Integration](../examples/04_webhook_integration.py)

**[See All Examples →](../examples/README.md)**

---

## 🔧 API Configuration

### Base URL
```
https://api.aimusicapi.ai
```

### Authentication
```python
from rapperrok import AIMusicClient

client = AIMusicClient(api_key="sk_your_api_key_here")
```

Get your API key: [https://aimusicapi.ai/dashboard/apikey](https://aimusicapi.ai/dashboard/apikey)

### Rate Limits

| Tier | Requests/Min | Concurrent Tasks |
|------|--------------|------------------|
| Free | 10 | 2 |
| Starter | 30 | 5 |
| Pro | 60 | 10 |
| Enterprise | Custom | Custom |

**[Full Rate Limiting Documentation →](./ENDPOINTS.md#rate-limiting)**

---

## 💰 Credits Pricing

### Suno V4
| Operation | Credits |
|-----------|---------|
| Create/Extend/Cover | 10 |
| Concat | 5 |
| Stems Basic | 20 |
| Stems Full | 50 |
| Create Persona | 50 |
| WAV/MIDI Export | 5-10 |

### Producer
| Operation | Credits |
|-----------|---------|
| Create/Extend/Cover | 10 |
| Swap Vocals/Instrumentals | 15 |

### Nuro
| Operation | Credits |
|-----------|---------|
| Vocal Music | 20 |
| Instrumental | 15 |

**[Complete Credits Guide →](./API_REFERENCE.md#credits--billing)**

---

## 🔍 Need Help?

### Finding Specific Information

- **API Endpoints**: See [ENDPOINTS.md](./ENDPOINTS.md)
- **Model Comparison**: See [MODELS.md](./MODELS.md)
- **Official Docs Links**: See [API_REFERENCE.md](./API_REFERENCE.md)
- **Code Examples**: See [../examples/](../examples/)
- **Getting Started**: See [../QUICKSTART.md](../QUICKSTART.md)
- **Contributing**: See [../CONTRIBUTING.md](../CONTRIBUTING.md)

### External Resources

- **Official API Docs**: [https://docs.aimusicapi.ai](https://docs.aimusicapi.ai)
- **Main Website**: [https://aimusicapi.ai](https://aimusicapi.ai)
- **Dashboard**: [https://aimusicapi.ai/dashboard](https://aimusicapi.ai/dashboard)
- **Discord**: [https://discord.gg/UFT2J2XK7d](https://discord.gg/UFT2J2XK7d)
- **Changelog**: [https://aimusicapi.featurebase.app/en/changelog](https://aimusicapi.featurebase.app/en/changelog)

### Support

- **GitHub Issues**: [https://github.com/rapperrok/rapperrok/issues](https://github.com/rapperrok/rapperrok/issues)
- **API Status**: [../API_STATUS.md](../API_STATUS.md)

---

## 📝 Documentation Structure

```
docs/
├── README.md           # This file - documentation index
├── API_REFERENCE.md    # Complete API reference with official docs links
├── MODELS.md          # Detailed model comparison and guide
└── ENDPOINTS.md       # All API endpoints with examples
```

---

## 🤝 Contributing to Documentation

Found an error or want to improve the documentation?

1. Read the [Contributing Guide](../CONTRIBUTING.md)
2. Fork the repository
3. Make your changes
4. Submit a pull request

We welcome:
- Typo fixes and clarifications
- Additional code examples
- Better explanations
- New use case documentation
- Translations

---

## 📜 License

This documentation is part of the RapperRok project and is licensed under the MIT License.
See [../LICENSE](../LICENSE) for details.

---

**Last Updated**: November 2025
**Version**: 1.0.0
