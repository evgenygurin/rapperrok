# Configuration

Learn how to configure RapperRok for different environments and use cases.

## Environment Variables

RapperRok supports configuration via environment variables, `.env` files, or direct instantiation.

### Required Variables

```bash
# Your API key from aimusicapi.ai
AIMUSIC_API_KEY=sk_your_api_key_here
```

### Optional Variables

```bash
# API base URL (default: https://api.aimusicapi.ai)
AIMUSIC_BASE_URL=https://api.aimusicapi.ai

# Logging level (default: INFO)
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Default request timeout in seconds (default: 30)
DEFAULT_TIMEOUT=30

# Maximum retry attempts (default: 3)
MAX_RETRIES=3

# Initial retry delay in seconds (default: 1.0)
RETRY_INITIAL_DELAY=1.0

# Maximum retry delay in seconds (default: 60.0)
RETRY_MAX_DELAY=60.0
```

### Using .env Files

Create a `.env` file in your project root:

```bash
# .env
AIMUSIC_API_KEY=sk_your_api_key_here
AIMUSIC_BASE_URL=https://api.aimusicapi.ai
LOG_LEVEL=INFO
DEFAULT_TIMEOUT=60
MAX_RETRIES=5
```

Load it in your code:

```python
from dotenv import load_dotenv
load_dotenv()

from rapperrok import AIMusicClient

# Configuration loaded from .env automatically
client = AIMusicClient()
```

## Client Configuration

### Basic Configuration

```python
from rapperrok import AIMusicClient

client = AIMusicClient(
    api_key="your_api_key",           # Required
    base_url="https://api.aimusicapi.ai",  # Optional
    timeout=60.0,                     # Optional (seconds)
)
```

### Advanced Configuration

```python
from rapperrok import AIMusicClient, RetryConfig
import logging

client = AIMusicClient(
    api_key="your_api_key",
    base_url="https://api.aimusicapi.ai",
    timeout=120.0,  # 2 minutes

    # Configure retry behavior
    retry_config=RetryConfig(
        max_retries=5,
        initial_delay=2.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True
    ),

    # Configure logging
    log_level=logging.DEBUG
)
```

## Retry Configuration

Control how RapperRok handles failed requests:

```python
from rapperrok import RetryConfig

retry_config = RetryConfig(
    max_retries=5,          # Maximum retry attempts
    initial_delay=2.0,      # Initial delay between retries (seconds)
    max_delay=60.0,         # Maximum delay between retries (seconds)
    exponential_base=2.0,   # Exponential backoff multiplier
    jitter=True             # Add random jitter to avoid thundering herd
)

client = AIMusicClient(retry_config=retry_config)
```

### Retry Strategy

RapperRok uses exponential backoff with jitter:

```
Attempt 1: Wait 2.0s
Attempt 2: Wait 4.0s (±jitter)
Attempt 3: Wait 8.0s (±jitter)
Attempt 4: Wait 16.0s (±jitter)
Attempt 5: Wait 32.0s (±jitter)
```

### Disable Retries

```python
from rapperrok import RetryConfig

# No retries
client = AIMusicClient(
    retry_config=RetryConfig(max_retries=0)
)
```

## Timeout Configuration

### Global Timeout

Set a default timeout for all requests:

```python
client = AIMusicClient(timeout=60.0)  # 60 seconds
```

### Per-Request Timeout

Override timeout for specific operations:

```python
# Long timeout for music generation
result = await client.suno.create_music(
    description="...",
    timeout=300.0  # 5 minutes
)

# Short timeout for quick operations
credits = await client.get_credits(timeout=10.0)
```

### Infinite Timeout

```python
# Wait indefinitely (not recommended)
result = await client.suno.create_music(
    description="...",
    timeout=None
)
```

## Logging Configuration

### Set Log Level

```python
import logging
from rapperrok import AIMusicClient

# Via environment variable
# LOG_LEVEL=DEBUG

# Or directly in code
client = AIMusicClient(log_level=logging.DEBUG)
```

### Log Levels

- **DEBUG**: Detailed information, typically of interest only when diagnosing problems
- **INFO**: Confirmation that things are working as expected
- **WARNING**: An indication that something unexpected happened
- **ERROR**: A more serious problem occurred
- **CRITICAL**: A serious error, the program may not be able to continue

### Custom Logger

```python
import logging

# Create custom logger
logger = logging.getLogger("rapperrok")
logger.setLevel(logging.DEBUG)

# Add handler
handler = logging.FileHandler("rapperrok.log")
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(handler)

# Use client (will use custom logger)
client = AIMusicClient()
```

## Proxy Configuration

### HTTP/HTTPS Proxy

```python
import httpx
from rapperrok import AIMusicClient

# Configure proxy via httpx
transport = httpx.AsyncHTTPTransport(
    proxy="http://proxy.example.com:8080"
)

# Note: You'll need to create a custom client
# RapperRok uses httpx internally
```

### Environment Variables

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=https://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1
```

## Multiple Environments

### Development

```python
# .env.development
AIMUSIC_API_KEY=sk_dev_key
AIMUSIC_BASE_URL=https://api-dev.aimusicapi.ai
LOG_LEVEL=DEBUG
DEFAULT_TIMEOUT=120
MAX_RETRIES=1
```

### Production

```python
# .env.production
AIMUSIC_API_KEY=sk_prod_key
AIMUSIC_BASE_URL=https://api.aimusicapi.ai
LOG_LEVEL=WARNING
DEFAULT_TIMEOUT=60
MAX_RETRIES=5
```

### Load Environment-Specific Config

```python
import os
from dotenv import load_dotenv

# Load environment-specific .env file
env = os.getenv("ENVIRONMENT", "development")
load_dotenv(f".env.{env}")

from rapperrok import AIMusicClient

client = AIMusicClient()
```

## Connection Pooling

RapperRok uses httpx connection pooling automatically:

```python
from rapperrok import AIMusicClient

# Connections are pooled and reused automatically
async with AIMusicClient() as client:
    # All requests use the same connection pool
    result1 = await client.suno.create_music(...)
    result2 = await client.producer.create_music(...)
    result3 = await client.nuro.create_vocal_music(...)
```

## Context Manager Usage

### Recommended: Async Context Manager

```python
async with AIMusicClient() as client:
    # Client automatically closes connections when done
    result = await client.suno.create_music(...)
```

### Manual Management

```python
client = AIMusicClient()

try:
    result = await client.suno.create_music(...)
finally:
    # Always close the client
    await client.close()
```

## API Key Management

### Best Practices

1. **Never hardcode API keys** in your source code
2. **Use environment variables** or secure vaults
3. **Rotate keys regularly** for security
4. **Use different keys** for dev/staging/production
5. **Restrict key permissions** in your AI Music API dashboard

### Secure Key Storage

=== "Environment Variables"

    ```bash
    # .env (gitignored)
    AIMUSIC_API_KEY=sk_your_key
    ```

    ```python
    from rapperrok import AIMusicClient
    client = AIMusicClient()  # Loads from environment
    ```

=== "AWS Secrets Manager"

    ```python
    import boto3
    from rapperrok import AIMusicClient

    # Fetch from AWS Secrets Manager
    secrets = boto3.client('secretsmanager')
    secret = secrets.get_secret_value(SecretId='aimusic/api_key')
    api_key = secret['SecretString']

    client = AIMusicClient(api_key=api_key)
    ```

=== "Azure Key Vault"

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    from rapperrok import AIMusicClient

    # Fetch from Azure Key Vault
    credential = DefaultAzureCredential()
    vault_client = SecretClient(
        vault_url="https://myvault.vault.azure.net/",
        credential=credential
    )
    api_key = vault_client.get_secret("aimusic-api-key").value

    client = AIMusicClient(api_key=api_key)
    ```

=== "Google Secret Manager"

    ```python
    from google.cloud import secretmanager
    from rapperrok import AIMusicClient

    # Fetch from Google Secret Manager
    client_sm = secretmanager.SecretManagerServiceClient()
    name = "projects/my-project/secrets/aimusic-api-key/versions/latest"
    response = client_sm.access_secret_version(request={"name": name})
    api_key = response.payload.data.decode("UTF-8")

    client = AIMusicClient(api_key=api_key)
    ```

## Testing Configuration

### Mock Client for Tests

```python
import pytest
from unittest.mock import AsyncMock
from rapperrok import AIMusicClient

@pytest.fixture
async def mock_client():
    client = AIMusicClient(api_key="test_key")

    # Mock methods
    client.suno.create_music = AsyncMock(return_value=...)

    return client

async def test_music_generation(mock_client):
    result = await mock_client.suno.create_music(description="test")
    assert result is not None
```

### Test Environment

```python
# .env.test
AIMUSIC_API_KEY=sk_test_key
AIMUSIC_BASE_URL=https://api-test.aimusicapi.ai
LOG_LEVEL=DEBUG
MAX_RETRIES=0  # No retries in tests
DEFAULT_TIMEOUT=5  # Fast timeouts
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variables (use build args)
ARG AIMUSIC_API_KEY
ENV AIMUSIC_API_KEY=$AIMUSIC_API_KEY

CMD ["python", "app.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - AIMUSIC_API_KEY=${AIMUSIC_API_KEY}
      - AIMUSIC_BASE_URL=https://api.aimusicapi.ai
      - LOG_LEVEL=INFO
    env_file:
      - .env
```

## Performance Tuning

### Connection Limits

```python
import httpx
from rapperrok import AIMusicClient

# Custom connection limits
limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20
)

# Note: RapperRok uses default httpx settings
# For custom limits, you may need to modify the client
```

### Batch Operations

```python
import asyncio
from rapperrok import AIMusicClient

async with AIMusicClient() as client:
    # Generate multiple tracks concurrently
    tasks = [
        client.suno.create_music(desc)
        for desc in descriptions
    ]

    # Control concurrency with semaphore
    sem = asyncio.Semaphore(5)  # Max 5 concurrent requests

    async def limited_task(task):
        async with sem:
            return await task

    results = await asyncio.gather(*[
        limited_task(task) for task in tasks
    ])
```

## Summary

- **Use environment variables** for configuration
- **Enable retries** for production resilience
- **Set appropriate timeouts** based on operation type
- **Configure logging** for debugging and monitoring
- **Use async context managers** for proper cleanup
- **Secure API keys** with proper secret management
- **Test with mocks** in development

## Next Steps

- [Quick Start Guide](quickstart.md) - Start generating music
- [Error Handling](guides/error-handling.md) - Handle errors gracefully
- [Webhook Integration](guides/webhooks.md) - Set up async notifications
- [API Reference](api/overview.md) - Complete API documentation
