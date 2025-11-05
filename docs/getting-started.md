# Getting Started

Welcome to RapperRok! This guide will help you install and set up the RapperRok AI Music API client.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.12 or higher** installed
- **An AI Music API key** from [aimusicapi.ai](https://aimusicapi.ai)
- **pip** or **uv** package manager

## Installation

### Option 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. It's significantly faster than pip and handles dependencies better.

```bash
# Install uv if you don't have it
pip install uv

# Install rapperrok
uv pip install rapperrok
```

For development with testing and linting tools:

```bash
uv pip install "rapperrok[dev]"
```

For documentation building:

```bash
uv pip install "rapperrok[docs]"
```

### Option 2: Using pip

```bash
# Install rapperrok
pip install rapperrok

# Or with development dependencies
pip install "rapperrok[dev]"

# Or with documentation dependencies
pip install "rapperrok[docs]"
```

### Option 3: From Source

If you want to contribute or work with the latest development version:

```bash
# Clone the repository
git clone https://github.com/rapperrok/rapperrok.git
cd rapperrok

# Install in development mode (with uv)
make dev
# Or manually
uv pip install -e ".[dev]"

# Install pre-commit hooks (for contributors)
uv run pre-commit install
```

## Getting Your API Key

1. Visit [AI Music API Dashboard](https://aimusicapi.ai/dashboard/apikey)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Generate a new API key (starts with `sk_`)
5. Copy your API key securely

!!! warning "Keep Your API Key Secret"
    Never commit your API key to version control or share it publicly. Always use environment variables or secure configuration management.

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
# Required
AIMUSIC_API_KEY=sk_your_api_key_here

# Optional (defaults shown)
AIMUSIC_BASE_URL=https://api.aimusicapi.ai
LOG_LEVEL=INFO
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
```

### Using .env File

Install `python-dotenv` (included with RapperRok):

```python
from dotenv import load_dotenv
load_dotenv()

from rapperrok import AIMusicClient

# API key will be loaded from environment
client = AIMusicClient()
```

### Direct API Key

You can also pass the API key directly:

```python
from rapperrok import AIMusicClient

client = AIMusicClient(api_key="sk_your_api_key_here")
```

### Configuration Options

You can configure various client options:

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    api_key="your_api_key",
    base_url="https://api.aimusicapi.ai",  # Custom base URL
    timeout=60.0,  # Request timeout in seconds
    retry_config=RetryConfig(
        max_retries=5,
        initial_delay=2.0,
        max_delay=60.0,
        exponential_base=2.0
    )
)
```

## Verify Installation

Test your installation with this simple script:

```python
import asyncio
from rapperrok import AIMusicClient

async def test_connection():
    """Test connection to AI Music API"""
    client = AIMusicClient()

    try:
        # Check credits
        credits = await client.get_credits()
        print(f"✅ Connection successful!")
        print(f"Available credits: {credits.available}")
        print(f"Total credits: {credits.total}")
        print(f"Used credits: {credits.used}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        await client.close()

asyncio.run(test_connection())
```

Save this as `test_connection.py` and run:

```bash
python test_connection.py
```

Expected output:

```
✅ Connection successful!
Available credits: 1000
Total credits: 1000
Used credits: 0
```

## Quick Test

Generate your first AI music:

```python
import asyncio
from rapperrok import AIMusicClient

async def first_song():
    """Generate your first AI music"""
    async with AIMusicClient() as client:
        print("🎵 Generating music...")

        result = await client.suno.create_music(
            description="happy upbeat pop song with piano",
            duration=30,
            wait_for_completion=True
        )

        print(f"✅ Music generated!")
        print(f"Audio URL: {result.clips[0].audio_url}")
        print(f"Video URL: {result.clips[0].video_url}")

asyncio.run(first_song())
```

## Troubleshooting

### SSL/TLS Errors

If you encounter `SSL: TLSV1_UNRECOGNIZED_NAME` errors:

1. Check your base URL in `.env`:
   ```bash
   grep AIMUSIC_BASE_URL .env
   # Should show: AIMUSIC_BASE_URL=https://api.aimusicapi.ai
   ```

2. Clear any environment variables:
   ```bash
   unset AIMUSIC_BASE_URL
   ```

3. Test connectivity:
   ```bash
   curl -I https://api.aimusicapi.ai
   ```

### Import Errors

If you get import errors:

```bash
# Verify installation
pip show rapperrok

# Reinstall if needed
pip uninstall rapperrok
pip install rapperrok
```

### Python Version Issues

Check your Python version:

```bash
python --version
# Should be 3.12 or higher

# If using multiple Python versions
python3.12 -m pip install rapperrok
```

### API Key Issues

- Ensure your API key starts with `sk_`
- Check if it's properly set in environment variables:
  ```bash
  echo $AIMUSIC_API_KEY
  ```
- Verify it's not expired in your dashboard

### Connection Timeouts

If requests timeout:

```python
from rapperrok import AIMusicClient

# Increase timeout
client = AIMusicClient(timeout=120.0)  # 2 minutes
```

### Rate Limiting

If you hit rate limits:

```python
from rapperrok import AIMusicClient, RetryConfig

client = AIMusicClient(
    retry_config=RetryConfig(
        max_retries=5,
        initial_delay=2.0,
        max_delay=60.0
    )
)
```

## API Service Status

!!! info "Current Status (November 2025)"
    As of November 5, 2025, some AI Music API endpoints may not be fully deployed. If you receive 404/405 errors, this is a server-side issue, not a problem with the library.

    **Current Status:**
    - ✅ SSL/TLS connection works
    - ✅ API domain resolves correctly
    - ⏸️ Backend endpoints return 404/405 (not yet deployed)

    **What to do:**
    1. Join their [Discord](https://discord.gg/UFT2J2XK7d) for updates
    2. Check the [Changelog](https://aimusicapi.featurebase.app/en/changelog)
    3. Use mock testing for development

    The library is ready and will work immediately once the API service is fully operational.

See [API_STATUS.md](https://github.com/rapperrok/rapperrok/blob/main/API_STATUS.md) for detailed investigation results.

## Next Steps

Now that you have RapperRok installed, you can:

1. **[Follow the Quick Start Guide](quickstart.md)** - Create your first AI music in minutes
2. **[Read the Basic Usage Guide](guides/basic-usage.md)** - Learn essential operations
3. **[Explore Examples](examples.md)** - See real-world usage examples
4. **[Check API Reference](api/overview.md)** - Dive into detailed API documentation

## Getting Help

- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
- **GitHub Issues**: [Report bugs or request features](https://github.com/rapperrok/rapperrok/issues)
- **AI Music API Docs**: [https://docs.aimusicapi.ai](https://docs.aimusicapi.ai)
- **Discord**: [Join the community](https://discord.gg/UFT2J2XK7d)

## Example Projects

Check out these example projects to see RapperRok in action:

- **[Basic Usage](https://github.com/rapperrok/rapperrok/blob/main/examples/01_basic_usage.py)** - Simple music generation
- **[Advanced Suno](https://github.com/rapperrok/rapperrok/blob/main/examples/02_advanced_suno.py)** - Stems, personas, MIDI
- **[Producer Operations](https://github.com/rapperrok/rapperrok/blob/main/examples/03_producer_operations.py)** - Fast generation
- **[Webhook Integration](https://github.com/rapperrok/rapperrok/blob/main/examples/04_webhook_integration.py)** - Async notifications
