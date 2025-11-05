# Client API Reference

Main client class for interacting with AI Music API.

## AIMusicClient

Main entry point for all API operations.

### Initialization

```python
from rapperrok import AIMusicClient

client = AIMusicClient(
    api_key="your_api_key",
    base_url="https://api.aimusicapi.ai",
    timeout=60.0,
    retry_config=RetryConfig(max_retries=3)
)
```

**Parameters:**

- `api_key` (str, optional): API key. Defaults to `AIMUSIC_API_KEY` environment variable
- `base_url` (str, optional): API base URL
- `timeout` (float, optional): Request timeout in seconds
- `retry_config` (RetryConfig, optional): Retry configuration

### Properties

#### suno

Access Suno V4 API operations:

```python
result = await client.suno.create_music(...)
```

See [Suno API Reference](suno.md) for details.

#### producer

Access Producer API operations:

```python
result = await client.producer.create_music(...)
```

See [Producer API Reference](producer.md) for details.

#### nuro

Access Nuro API operations:

```python
result = await client.nuro.create_vocal_music(...)
```

See [Nuro API Reference](nuro.md) for details.

### Methods

#### get_credits()

Get current credit balance:

```python
credits = await client.get_credits()
print(f"Available: {credits.available}")
```

**Returns:** `Credits` object

#### close()

Close the client and cleanup resources:

```python
await client.close()
```

### Context Manager

Use as async context manager (recommended):

```python
async with AIMusicClient() as client:
    result = await client.suno.create_music(...)
# Client automatically closed
```

### Examples

See [Examples](../examples.md) for complete usage examples.

## Next Steps

- [Suno API Reference](suno.md)
- [Producer API Reference](producer.md)
- [Nuro API Reference](nuro.md)
- [Common Module](common.md)
