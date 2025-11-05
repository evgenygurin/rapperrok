# Advanced Features Guide

Master advanced RapperRok features for production applications.

## Async Operations

### Concurrent Generation

Generate multiple tracks simultaneously:

```python
import asyncio

async def concurrent_generation():
    async with AIMusicClient() as client:
        # Start all tasks concurrently
        tasks = [
            client.suno.create_music(description="rock", duration=30),
            client.suno.create_music(description="jazz", duration=30),
            client.suno.create_music(description="electronic", duration=30),
        ]

        # Wait for all to start
        results = await asyncio.gather(*tasks)

        # Wait for all to complete
        completed = await asyncio.gather(*[
            client.suno.wait_for_completion(r.task_id)
            for r in results
        ])

        return completed
```

### Controlled Concurrency

Limit concurrent requests to avoid rate limits:

```python
import asyncio

async def controlled_concurrent_generation(descriptions, max_concurrent=5):
    """Generate with concurrency limit"""
    sem = asyncio.Semaphore(max_concurrent)

    async def limited_generate(desc):
        async with sem:
            return await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )

    async with AIMusicClient() as client:
        tasks = [limited_generate(desc) for desc in descriptions]
        return await asyncio.gather(*tasks)

# Usage
descriptions = ["rock", "jazz", "pop", "electronic", "classical"]
results = await controlled_concurrent_generation(descriptions, max_concurrent=3)
```

## Retry Strategies

### Exponential Backoff

```python
import asyncio
from rapperrok.exceptions import RateLimitError, NetworkError

async def generate_with_exponential_backoff(description, max_retries=5):
    for attempt in range(max_retries):
        try:
            return await client.suno.create_music(
                description=description,
                wait_for_completion=True
            )
        except (RateLimitError, NetworkError) as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff: 2, 4, 8, 16, 32 seconds
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s...")
            await asyncio.sleep(wait_time)
```

### Smart Retry with Jitter

```python
import random
import asyncio

async def smart_retry(description, max_retries=5):
    for attempt in range(max_retries):
        try:
            return await client.suno.create_music(
                description=description,
                wait_for_completion=True
            )
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff with jitter
            base_wait = 2 ** attempt
            jitter = random.uniform(0, 0.1 * base_wait)
            wait_time = base_wait + jitter

            print(f"Retry {attempt + 1}/{max_retries} in {wait_time:.1f}s...")
            await asyncio.sleep(wait_time)
```

### Using Tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging

logger = logging.getLogger(__name__)

@retry(
    retry=retry_if_exception_type((RateLimitError, NetworkError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def robust_generate(description):
    return await client.suno.create_music(
        description=description,
        wait_for_completion=True
    )
```

## Caching

### Result Caching

Cache generated music to avoid regenerating:

```python
from functools import lru_cache
import hashlib
import json

class MusicCache:
    def __init__(self):
        self.cache = {}

    def _hash_params(self, **kwargs):
        """Create hash of parameters"""
        key = json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(key.encode()).hexdigest()

    async def get_or_generate(self, client, **kwargs):
        cache_key = self._hash_params(**kwargs)

        if cache_key in self.cache:
            print(f"✅ Cache hit: {cache_key[:8]}")
            return self.cache[cache_key]

        print(f"🔄 Cache miss, generating...")
        result = await client.suno.create_music(**kwargs)

        self.cache[cache_key] = result
        return result

# Usage
cache = MusicCache()

# First call - generates
result1 = await cache.get_or_generate(
    client,
    description="rock song",
    duration=30
)

# Second call - cached
result2 = await cache.get_or_generate(
    client,
    description="rock song",
    duration=30
)
```

### File-Based Caching

```python
import aiofiles
import json
from pathlib import Path

class FileCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _cache_path(self, key):
        return self.cache_dir / f"{key}.json"

    async def get(self, key):
        path = self._cache_path(key)
        if path.exists():
            async with aiofiles.open(path, 'r') as f:
                content = await f.read()
                return json.loads(content)
        return None

    async def set(self, key, value):
        path = self._cache_path(key)
        async with aiofiles.open(path, 'w') as f:
            await f.write(json.dumps(value, indent=2))

    async def cached_generate(self, client, description, **kwargs):
        cache_key = hashlib.md5(description.encode()).hexdigest()

        # Check cache
        cached = await self.get(cache_key)
        if cached:
            print("✅ Loaded from cache")
            return cached

        # Generate
        result = await client.suno.create_music(
            description=description,
            wait_for_completion=True,
            **kwargs
        )

        # Cache result
        await self.set(cache_key, {
            "description": description,
            "audio_url": result.clips[0].audio_url,
            "video_url": result.clips[0].video_url,
        })

        return result
```

## Connection Pooling

### Custom HTTP Client

```python
import httpx
from rapperrok import AIMusicClient

async def with_custom_pool():
    # Custom connection limits
    limits = httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20,
        keepalive_expiry=30.0
    )

    # Custom timeout
    timeout = httpx.Timeout(10.0, connect=5.0)

    # Note: RapperRok uses httpx internally
    # For advanced customization, you may need to modify the client
    async with AIMusicClient() as client:
        # Client uses default connection pool
        results = await asyncio.gather(*[
            client.suno.create_music(f"song {i}")
            for i in range(10)
        ])
```

## Progress Tracking

### Rich Progress Bar

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

async def generate_with_progress(descriptions):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(
            "[cyan]Generating music...",
            total=len(descriptions)
        )

        results = []
        async with AIMusicClient() as client:
            for desc in descriptions:
                progress.update(task, description=f"[cyan]Generating: {desc}")

                result = await client.suno.create_music(
                    description=desc,
                    duration=30,
                    wait_for_completion=True
                )
                results.append(result)

                progress.advance(task)

        return results
```

### Custom Progress Callback

```python
from typing import Callable

async def generate_with_callback(
    descriptions,
    progress_callback: Callable[[int, int], None]
):
    """Generate with custom progress callback"""
    results = []

    async with AIMusicClient() as client:
        for i, desc in enumerate(descriptions):
            # Call progress callback
            progress_callback(i, len(descriptions))

            result = await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )
            results.append(result)

    # Final callback
    progress_callback(len(descriptions), len(descriptions))
    return results

# Usage
def my_progress(current, total):
    percent = (current / total) * 100
    print(f"Progress: {percent:.1f}% ({current}/{total})")

results = await generate_with_callback(
    ["rock", "jazz", "pop"],
    progress_callback=my_progress
)
```

## Queue-Based Processing

### Work Queue

```python
import asyncio
from asyncio import Queue

async def worker(queue: Queue, results: list):
    """Worker that processes items from queue"""
    async with AIMusicClient() as client:
        while True:
            description = await queue.get()
            if description is None:  # Sentinel value
                break

            try:
                result = await client.suno.create_music(
                    description=description,
                    duration=30,
                    wait_for_completion=True
                )
                results.append(result)
                print(f"✅ Generated: {description}")
            except Exception as e:
                print(f"❌ Failed: {description} - {e}")
            finally:
                queue.task_done()

async def queue_based_generation(descriptions, num_workers=3):
    """Process descriptions using worker queue"""
    queue = Queue()
    results = []

    # Start workers
    workers = [
        asyncio.create_task(worker(queue, results))
        for _ in range(num_workers)
    ]

    # Add tasks to queue
    for desc in descriptions:
        await queue.put(desc)

    # Wait for all tasks to complete
    await queue.join()

    # Stop workers
    for _ in range(num_workers):
        await queue.put(None)

    await asyncio.gather(*workers)

    return results

# Usage
descriptions = ["rock", "jazz", "pop", "electronic", "classical"]
results = await queue_based_generation(descriptions, num_workers=3)
```

## Rate Limiting

### Token Bucket

```python
import asyncio
import time

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def consume(self, tokens=1):
        async with self.lock:
            now = time.time()
            # Add tokens based on time passed
            elapsed = now - self.last_update
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Wait if not enough tokens
            if self.tokens < tokens:
                wait_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= tokens

async def rate_limited_generation(descriptions):
    """Generate with rate limiting"""
    # 5 requests per minute
    bucket = TokenBucket(rate=5/60, capacity=5)

    results = []
    async with AIMusicClient() as client:
        for desc in descriptions:
            await bucket.consume(1)  # Wait for token

            result = await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )
            results.append(result)

    return results
```

## Batch Processing Patterns

### Chunked Processing

```python
def chunk_list(lst, chunk_size):
    """Split list into chunks"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

async def chunked_generation(descriptions, chunk_size=10):
    """Process in chunks"""
    all_results = []

    async with AIMusicClient() as client:
        for chunk in chunk_list(descriptions, chunk_size):
            print(f"Processing chunk of {len(chunk)}...")

            # Process chunk
            tasks = [
                client.suno.create_music(desc, duration=30)
                for desc in chunk
            ]
            results = await asyncio.gather(*tasks)

            # Wait for completion
            completed = await asyncio.gather(*[
                client.suno.wait_for_completion(r.task_id)
                for r in results
            ])

            all_results.extend(completed)

            # Small delay between chunks
            await asyncio.sleep(5)

    return all_results
```

### Pipeline Processing

```python
async def pipeline_processing(descriptions):
    """Multi-stage processing pipeline"""
    async with AIMusicClient() as client:
        # Stage 1: Generate music
        print("Stage 1: Generating...")
        music_results = []
        for desc in descriptions:
            result = await client.suno.create_music(
                description=desc,
                duration=30,
                wait_for_completion=True
            )
            music_results.append(result)

        # Stage 2: Extract stems
        print("Stage 2: Extracting stems...")
        stems_results = []
        for music in music_results:
            stems = await client.suno.stems_basic(
                song_id=music.clips[0].id
            )
            stems_results.append(stems)

        # Stage 3: Download files
        print("Stage 3: Downloading...")
        for i, stems in enumerate(stems_results):
            await download_audio(
                stems.vocals_url,
                f"track_{i}_vocals.mp3"
            )
            await download_audio(
                stems.instrumental_url,
                f"track_{i}_instrumental.mp3"
            )

        return stems_results
```

## Context Managers

### Custom Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def music_generation_session(api_key, log_file="session.log"):
    """Custom context manager for music generation session"""
    # Setup
    client = AIMusicClient(api_key=api_key)
    start_credits = await client.get_credits()
    start_time = time.time()

    try:
        yield client
    finally:
        # Cleanup and logging
        end_credits = await client.get_credits()
        end_time = time.time()
        duration = end_time - start_time

        # Log session details
        with open(log_file, 'a') as f:
            f.write(f"Session duration: {duration:.1f}s\n")
            f.write(f"Credits used: {start_credits.available - end_credits.available}\n")

        await client.close()

# Usage
async with music_generation_session("api_key") as client:
    result = await client.suno.create_music(...)
```

## Testing Strategies

### Mock Client

```python
from unittest.mock import AsyncMock, Mock

class MockAIMusicClient:
    def __init__(self):
        self.suno = Mock()
        self.suno.create_music = AsyncMock(return_value=Mock(
            task_id="test_123",
            status="completed",
            clips=[Mock(
                audio_url="https://example.com/audio.mp3",
                video_url="https://example.com/video.mp4"
            )]
        ))

# Usage in tests
async def test_generation():
    client = MockAIMusicClient()
    result = await client.suno.create_music(description="test")
    assert result.task_id == "test_123"
```

### Integration Tests

```python
import pytest

@pytest.mark.integration
async def test_real_generation():
    """Test with real API (requires API key)"""
    async with AIMusicClient() as client:
        result = await client.suno.create_music(
            description="test song",
            duration=30,
            wait_for_completion=True
        )

        assert result.clips
        assert result.clips[0].audio_url
```

## Best Practices

1. **Use async context managers** for resource management
2. **Implement retry logic** for transient failures
3. **Cache results** to avoid redundant API calls
4. **Control concurrency** to avoid rate limits
5. **Monitor credits** in production
6. **Use webhooks** for long-running tasks
7. **Log all operations** for debugging
8. **Test with mocks** in development

## Next Steps

- [Error Handling](error-handling.md) - Handle errors gracefully
- [Webhook Integration](webhooks.md) - Async notifications
- [Credits Management](credits.md) - Optimize credit usage
- [API Reference](../api/overview.md) - Complete API docs
