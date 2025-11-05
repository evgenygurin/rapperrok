# RapperRok Examples

Comprehensive examples demonstrating all features of the RapperRok AI Music API client.

## 📚 Documentation

Before running these examples, check out the comprehensive documentation:

- **[API Reference](../docs/API_REFERENCE.md)** - Complete API documentation with all endpoints
- **[Models Guide](../docs/MODELS.md)** - Detailed comparison of Suno, Producer, Nuro, Riffusion
- **[Endpoints Reference](../docs/ENDPOINTS.md)** - All API endpoints with request/response examples
- **[Quick Start](../QUICKSTART.md)** - Get started quickly

Not sure which model to use? See the [Model Selection Guide](../docs/MODELS.md#choosing-the-right-model).

## Setup

1. Install dependencies:
```bash
cd /Users/laptop/dev/rapperrok
uv pip install -e .
```

2. Set your API key:
```bash
export AIMUSIC_API_KEY="your_api_key_here"
```

3. Run examples:
```bash
python examples/01_basic_usage.py
```

## Examples Overview

### 01_basic_usage.py
**Basic operations with all models**

- Create music with Suno
- Fast generation with Producer (30 seconds)
- Full-length songs with Nuro (4 minutes)
- Check credit balance

```bash
python examples/01_basic_usage.py
```

### 02_advanced_suno.py
**Advanced Suno V4 features**

- Custom lyrics
- Extend and concatenate tracks
- Stems separation (basic and full)
- Custom voice personas
- WAV and MIDI export
- Download generated music

```bash
python examples/02_advanced_suno.py
```

### 03_producer_operations.py
**Producer API all operations**

- Create new music
- Extend existing tracks
- Create cover versions
- Replace sections
- Swap vocals
- Swap instrumentals
- Create variations
- Upload and modify audio
- Download in different formats (MP3/WAV)

```bash
python examples/03_producer_operations.py
```

### 04_webhook_integration.py
**Webhook handling and integration**

- Basic webhook handler
- FastAPI webhook endpoint
- Generate music with webhook notifications
- Manual webhook processing

```bash
python examples/04_webhook_integration.py
```

## Common Patterns

### Using Async Context Manager

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description="your music description",
            duration=60,
            wait_for_completion=True
        )
        print(result.clips[0].audio_url)

asyncio.run(main())
```

### Manual Client Management

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    client = AIMusicClient(api_key="your_key")

    try:
        result = await client.suno.create_music(...)
        print(result.clips[0].audio_url)
    finally:
        await client.close()

asyncio.run(main())
```

### Polling for Completion

```python
# Option 1: Wait immediately
result = await client.suno.create_music(
    description="...",
    wait_for_completion=True
)

# Option 2: Poll later
result = await client.suno.create_music(description="...")
task_id = result.task_id

# Do other work...

# Poll when ready
completed = await client.suno.wait_for_completion(task_id)
```

### Batch Generation

```python
import asyncio

async def generate_multiple():
    async with AIMusicClient() as client:
        descriptions = [
            "rock song with guitar",
            "jazz piano melody",
            "electronic dance music"
        ]

        # Create all tasks concurrently
        tasks = [
            client.suno.create_music(desc)
            for desc in descriptions
        ]

        results = await asyncio.gather(*tasks)

        # Wait for all to complete
        completed = await asyncio.gather(*[
            client.suno.wait_for_completion(r.task_id)
            for r in results
        ])

        for result in completed:
            print(result.clips[0].audio_url)
```

### Error Handling

```python
from rapperrok import (
    AIMusicClient,
    AIMusicAPIError,
    InsufficientCreditsError,
    RateLimitError,
    TaskFailedError
)

async def safe_generation():
    async with AIMusicClient() as client:
        try:
            result = await client.suno.create_music(
                description="...",
                wait_for_completion=True
            )
        except InsufficientCreditsError as e:
            print(f"Not enough credits: {e.credits_available}")
        except RateLimitError as e:
            print(f"Rate limit hit. Retry after: {e.retry_after}s")
        except TaskFailedError as e:
            print(f"Generation failed: {e.message}")
        except AIMusicAPIError as e:
            print(f"API error: {e.message}")
```

### Download and Save

```python
from pathlib import Path
from rapperrok import AIMusicClient, download_audio

async def download_example():
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description="...",
            wait_for_completion=True
        )

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        for i, clip in enumerate(result.clips):
            output_path = output_dir / f"song_{i}.mp3"
            await download_audio(clip.audio_url, output_path)
            print(f"Downloaded: {output_path}")
```

## Environment Variables

Set these in your `.env` file:

```bash
# Required
AIMUSIC_API_KEY=your_api_key_here

# Optional
AIMUSIC_BASE_URL=https://api.sunoapi.com
LOG_LEVEL=INFO
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
```

## Output Directory

Examples that download files save them to `examples/output/`. This directory is gitignored.

```bash
mkdir -p examples/output
```

## Tips

1. **Start with basic examples**: Run `01_basic_usage.py` first
2. **Check credits**: Always check your balance before batch operations
3. **Use webhooks for long tasks**: Avoid polling for tasks longer than 60 seconds
4. **Download important files**: Generated URLs may expire
5. **Handle errors**: Wrap operations in try-except for production code

## Credits Cost

Approximate credit costs per operation:

| Operation | Model | Credits |
|-----------|-------|---------|
| Create music | Suno | 10 |
| Extend music | Suno | 10 |
| Concat music | Suno | 5 |
| Cover music | Suno | 10 |
| Stems basic | Suno | 20 |
| Stems full | Suno | 50 |
| Create persona | Suno | 50 |
| WAV export | Suno | 10 |
| MIDI export | Suno | 5 |
| Create music | Producer | 10 |
| Swap vocal | Producer | 15 |
| Swap instrumental | Producer | 15 |
| Create music | Nuro | 20 |
| Create instrumental | Nuro | 15 |

## API Documentation by Model

Each example uses specific AI models. Learn more about each model:

### Suno V4 (Examples 01, 02)
- **[Model Overview](../docs/MODELS.md#suno-v4)** - Features, pricing, use cases
- **[API Endpoints](../docs/ENDPOINTS.md#suno-api-endpoints)** - All Suno endpoints
- **[Official Docs](https://docs.aimusicapi.ai/suno-api-instructions.md)**

### Producer/FUZZ-2.0 (Examples 01, 03)
- **[Model Overview](../docs/MODELS.md#producer-fuzz-20)** - Features, pricing, use cases
- **[API Endpoints](../docs/ENDPOINTS.md#producer-api-endpoints)** - All Producer endpoints
- **[Official Docs](https://docs.aimusicapi.ai/producer-api-overview.md)**

### Nuro (Example 01)
- **[Model Overview](../docs/MODELS.md#nuro)** - Features, pricing, use cases
- **[API Endpoints](../docs/ENDPOINTS.md#nuro-api-endpoints)** - All Nuro endpoints
- **[Official Docs](https://docs.aimusicapi.ai/nuro-api-overview.md)**

### Webhooks (Example 04)
- **[Webhook Guide](../docs/ENDPOINTS.md#webhooks)** - Integration and verification
- **[Official Docs](https://docs.aimusicapi.ai/webhook-guide.md)**

## Support

- **Documentation**: https://rapperrok.readthedocs.io
- **API Docs**: https://docs.aimusicapi.ai
- **GitHub Issues**: https://github.com/rapperrok/rapperrok/issues
- **Discord**: https://discord.gg/UFT2J2XK7d

## License

MIT License - see LICENSE file for details
