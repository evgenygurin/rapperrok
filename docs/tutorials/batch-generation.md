# Tutorial: Batch Music Generation

Learn how to generate multiple music tracks efficiently using batch operations.

Coming soon! In the meantime, see the [Advanced Features Guide](../guides/advanced.md) for batch processing patterns.

## Quick Example

```python
import asyncio
from rapperrok import AIMusicClient

async def batch_generate():
    descriptions = ["rock", "jazz", "pop", "electronic"]

    async with AIMusicClient() as client:
        tasks = [
            client.suno.create_music(desc, duration=30)
            for desc in descriptions
        ]
        results = await asyncio.gather(*tasks)

        for result in results:
            music = await client.suno.wait_for_completion(result.task_id)
            print(f"Generated: {music.clips[0].audio_url}")

asyncio.run(batch_generate())
```

See [Advanced Features Guide](../guides/advanced.md) for more details.
