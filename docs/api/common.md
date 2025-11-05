# Common Module Reference

Shared utilities and base classes.

## RetryConfig

Configuration for retry behavior.

**Parameters:**

- `max_retries` (int): Maximum retry attempts
- `initial_delay` (float): Initial delay in seconds
- `max_delay` (float): Maximum delay in seconds
- `exponential_base` (float): Exponential backoff multiplier
- `jitter` (bool): Add random jitter

**Example:**

```python
from rapperrok import RetryConfig

config = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=60.0,
    exponential_base=2.0
)
```

See [Configuration Guide](../configuration.md) for more details.
