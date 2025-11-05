# Error Handling Guide

Comprehensive guide to handling errors and exceptions in RapperRok.

## Exception Hierarchy

RapperRok provides a hierarchy of exceptions for different error scenarios:

```
AIMusicAPIError (base)
├── AuthenticationError
├── RateLimitError
├── InsufficientCreditsError
├── InvalidParameterError
├── TaskFailedError
├── NetworkError
└── TimeoutError
```

## Common Exceptions

### AIMusicAPIError

Base exception for all API errors:

```python
from rapperrok.exceptions import AIMusicAPIError

try:
    result = await client.suno.create_music(...)
except AIMusicAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Error Code: {e.error_code}")
```

**Attributes:**

- `message`: Human-readable error message
- `status_code`: HTTP status code
- `error_code`: API-specific error code
- `details`: Additional error details

### AuthenticationError

Invalid or missing API key:

```python
from rapperrok.exceptions import AuthenticationError

try:
    client = AIMusicClient(api_key="invalid_key")
    result = await client.suno.create_music(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Get new API key or check configuration
```

**Common Causes:**

- Invalid API key
- Expired API key
- Missing API key
- API key lacks permissions

**Solution:**

- Verify API key in dashboard
- Check environment variables
- Ensure API key starts with `sk_`

### RateLimitError

Too many requests:

```python
from rapperrok.exceptions import RateLimitError
import asyncio

try:
    result = await client.suno.create_music(...)
except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    print(f"Retry after: {e.retry_after}s")

    # Wait and retry
    await asyncio.sleep(e.retry_after)
    result = await client.suno.create_music(...)
```

**Attributes:**

- `retry_after`: Seconds to wait before retry
- `limit`: Rate limit cap
- `remaining`: Remaining requests

**Solutions:**

- Implement exponential backoff
- Use rate limiting in your code
- Upgrade plan for higher limits

### InsufficientCreditsError

Not enough credits for operation:

```python
from rapperrok.exceptions import InsufficientCreditsError

try:
    result = await client.suno.create_music(...)
except InsufficientCreditsError as e:
    print(f"Need {e.credits_required} credits")
    print(f"Have {e.credits_available} credits")
    print(f"Deficit: {e.credits_required - e.credits_available}")

    # Purchase more credits or wait for renewal
```

**Attributes:**

- `credits_required`: Credits needed
- `credits_available`: Current balance

**Solutions:**

- Check credits before operations
- Purchase additional credits
- Wait for monthly renewal

### InvalidParameterError

Invalid request parameters:

```python
from rapperrok.exceptions import InvalidParameterError

try:
    result = await client.suno.create_music(
        description="",  # Empty description
        duration=-1      # Invalid duration
    )
except InvalidParameterError as e:
    print(f"Invalid parameter: {e.parameter_name}")
    print(f"Error: {e.message}")
    print(f"Valid values: {e.valid_values}")
```

**Attributes:**

- `parameter_name`: Name of invalid parameter
- `valid_values`: List of valid values

**Solutions:**

- Check parameter requirements
- Validate input before API call
- See API documentation

### TaskFailedError

Music generation task failed:

```python
from rapperrok.exceptions import TaskFailedError

try:
    result = await client.suno.create_music(
        description="...",
        wait_for_completion=True
    )
except TaskFailedError as e:
    print(f"Task failed: {e.message}")
    print(f"Task ID: {e.task_id}")
    print(f"Failure reason: {e.failure_reason}")

    # Retry with different parameters
```

**Attributes:**

- `task_id`: Failed task ID
- `failure_reason`: Why it failed

**Common Causes:**

- Invalid prompt/description
- Service error
- Timeout
- Content policy violation

**Solutions:**

- Retry with different prompt
- Simplify description
- Check content guidelines
- Contact support if persists

### NetworkError

Connection or network issues:

```python
from rapperrok.exceptions import NetworkError
import asyncio

try:
    result = await client.suno.create_music(...)
except NetworkError as e:
    print(f"Network error: {e.message}")

    # Retry with exponential backoff
    for attempt in range(3):
        await asyncio.sleep(2 ** attempt)
        try:
            result = await client.suno.create_music(...)
            break
        except NetworkError:
            if attempt == 2:
                raise
```

**Solutions:**

- Check internet connection
- Verify API endpoint is accessible
- Implement retry logic
- Check firewall settings

### TimeoutError

Request took too long:

```python
from rapperrok.exceptions import TimeoutError

try:
    result = await client.suno.create_music(
        description="...",
        timeout=30.0  # 30 second timeout
    )
except TimeoutError as e:
    print(f"Request timed out after {e.timeout}s")

    # Retry with longer timeout
    result = await client.suno.create_music(
        description="...",
        timeout=120.0  # 2 minutes
    )
```

**Solutions:**

- Increase timeout for long operations
- Use webhooks instead of polling
- Check network connection

## Error Handling Patterns

### Basic Try-Except

```python
from rapperrok.exceptions import AIMusicAPIError

async def generate_music(description: str):
    try:
        result = await client.suno.create_music(
            description=description,
            duration=60,
            wait_for_completion=True
        )
        return result
    except AIMusicAPIError as e:
        print(f"Error: {e.message}")
        return None
```

### Specific Exception Handling

```python
from rapperrok.exceptions import (
    InsufficientCreditsError,
    RateLimitError,
    TaskFailedError,
    InvalidParameterError
)

async def safe_generate(description: str):
    try:
        result = await client.suno.create_music(
            description=description,
            wait_for_completion=True
        )
        return result

    except InsufficientCreditsError as e:
        print(f"❌ Not enough credits: {e.credits_available}/{e.credits_required}")
        # Handle insufficient credits
        return None

    except RateLimitError as e:
        print(f"⏱️ Rate limited, retry after {e.retry_after}s")
        await asyncio.sleep(e.retry_after)
        return await safe_generate(description)  # Retry

    except TaskFailedError as e:
        print(f"❌ Generation failed: {e.failure_reason}")
        # Try with different prompt
        return None

    except InvalidParameterError as e:
        print(f"❌ Invalid {e.parameter_name}: {e.message}")
        return None
```

### Retry with Exponential Backoff

```python
import asyncio
from rapperrok.exceptions import RateLimitError, NetworkError

async def generate_with_retry(description: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = await client.suno.create_music(
                description=description,
                wait_for_completion=True
            )
            return result

        except (RateLimitError, NetworkError) as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s...")
            await asyncio.sleep(wait_time)

    raise Exception(f"Failed after {max_retries} attempts")
```

### Using Tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from rapperrok.exceptions import RateLimitError, NetworkError

@retry(
    retry=retry_if_exception_type((RateLimitError, NetworkError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60)
)
async def generate_with_tenacity(description: str):
    return await client.suno.create_music(
        description=description,
        wait_for_completion=True
    )
```

### Check Credits Before Operations

```python
from rapperrok.exceptions import InsufficientCreditsError

async def safe_batch_generate(descriptions: list):
    # Check credits first
    credits = await client.get_credits()
    required = len(descriptions) * 10  # 10 credits per generation

    if credits.available < required:
        print(f"Need {required} credits, have {credits.available}")
        return []

    # Generate
    results = []
    for desc in descriptions:
        try:
            result = await client.suno.create_music(
                description=desc,
                wait_for_completion=True
            )
            results.append(result)
        except InsufficientCreditsError:
            # Stop if we run out mid-batch
            print("Ran out of credits during batch")
            break
        except Exception as e:
            print(f"Skipped '{desc}': {e}")
            continue

    return results
```

### Graceful Degradation

```python
async def generate_with_fallback(description: str):
    """Try Suno, fallback to Producer if it fails"""
    try:
        # Try Suno first (highest quality)
        return await client.suno.create_music(
            description=description,
            duration=60,
            wait_for_completion=True
        )
    except (TaskFailedError, InsufficientCreditsError) as e:
        print(f"Suno failed: {e.message}, trying Producer...")

        try:
            # Fallback to Producer (faster, cheaper)
            return await client.producer.create_music(
                description=description,
                operation="create",
                duration=60,
                wait_for_completion=True
            )
        except Exception as e2:
            print(f"Producer also failed: {e2}")
            raise
```

### Logging Errors

```python
import logging
from rapperrok.exceptions import AIMusicAPIError

logger = logging.getLogger(__name__)

async def generate_with_logging(description: str):
    try:
        logger.info(f"Generating: {description}")
        result = await client.suno.create_music(
            description=description,
            wait_for_completion=True
        )
        logger.info(f"✅ Generated: {result.clips[0].id}")
        return result

    except AIMusicAPIError as e:
        logger.error(
            f"❌ Generation failed",
            extra={
                "description": description,
                "error": e.message,
                "error_code": e.error_code,
                "status_code": e.status_code
            }
        )
        raise
```

## Best Practices

### 1. Always Handle Exceptions

```python
# ❌ Don't
result = await client.suno.create_music(...)

# ✅ Do
try:
    result = await client.suno.create_music(...)
except AIMusicAPIError as e:
    print(f"Error: {e.message}")
```

### 2. Be Specific

```python
# ❌ Too broad
try:
    result = await client.suno.create_music(...)
except Exception:
    pass

# ✅ Specific handling
try:
    result = await client.suno.create_music(...)
except InsufficientCreditsError:
    # Handle insufficient credits
    pass
except RateLimitError:
    # Handle rate limit
    pass
except AIMusicAPIError as e:
    # Handle other API errors
    print(e.message)
```

### 3. Validate Input

```python
def validate_description(description: str) -> bool:
    if not description or len(description) < 10:
        raise ValueError("Description too short")
    if len(description) > 500:
        raise ValueError("Description too long")
    return True

async def generate(description: str):
    # Validate before API call
    validate_description(description)

    try:
        return await client.suno.create_music(description=description)
    except InvalidParameterError as e:
        print(f"Invalid: {e.message}")
```

### 4. Monitor and Log

```python
import logging

logger = logging.getLogger(__name__)

async def monitored_generate(description: str):
    try:
        result = await client.suno.create_music(description=description)
        logger.info(f"Success: {result.task_id}")
        return result
    except AIMusicAPIError as e:
        logger.error(f"Failed: {e.message}", exc_info=True)
        # Also send to monitoring service (Sentry, etc.)
        raise
```

### 5. Use Context Managers

```python
# ✅ Proper cleanup
async with AIMusicClient() as client:
    try:
        result = await client.suno.create_music(...)
    except AIMusicAPIError as e:
        print(e.message)
# Client automatically closed
```

## Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

client = AIMusicClient(log_level=logging.DEBUG)
```

### Inspect Errors

```python
try:
    result = await client.suno.create_music(...)
except AIMusicAPIError as e:
    print(f"Message: {e.message}")
    print(f"Status: {e.status_code}")
    print(f"Code: {e.error_code}")
    print(f"Details: {e.details}")
    print(f"Request ID: {e.request_id}")  # For support
```

## Testing Error Handling

```python
import pytest
from rapperrok.exceptions import InsufficientCreditsError

@pytest.mark.asyncio
async def test_insufficient_credits(mock_client):
    mock_client.suno.create_music.side_effect = InsufficientCreditsError(
        message="Insufficient credits",
        credits_required=10,
        credits_available=5
    )

    with pytest.raises(InsufficientCreditsError) as exc_info:
        await generate_music(mock_client, "test")

    assert exc_info.value.credits_required == 10
    assert exc_info.value.credits_available == 5
```

## Next Steps

- [Webhook Integration](webhooks.md) - Async notifications
- [Advanced Features](advanced.md) - Advanced patterns
- [API Reference](../api/exceptions.md) - Complete exception docs
