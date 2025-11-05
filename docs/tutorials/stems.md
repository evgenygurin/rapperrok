# Tutorial: Stems Separation

Learn how to separate vocals and instrumentals from your music.

See the [Suno Guide](../guides/suno.md#stems-separation) for complete stems separation documentation.

## Quick Example

```python
import asyncio
from rapperrok import AIMusicClient

async def separate_stems():
    async with AIMusicClient() as client:
        # Create song
        song = await client.suno.create_music(
            description="rock song with vocals",
            duration=30,
            wait_for_completion=True
        )

        # Separate basic stems (vocals + instrumental)
        stems = await client.suno.stems_basic(song_id=song.clips[0].id)

        print(f"Vocals: {stems.vocals_url}")
        print(f"Instrumental: {stems.instrumental_url}")

asyncio.run(separate_stems())
```

See [Suno Guide](../guides/suno.md) for full documentation.
