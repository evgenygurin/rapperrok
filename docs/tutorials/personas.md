# Tutorial: Custom Voice Personas

Learn how to create and use custom voice personas for unique AI vocals.

See the [Suno Guide](../guides/suno.md#custom-voice-personas) for complete persona documentation.

## Quick Example

```python
import asyncio
from rapperrok import AIMusicClient

async def use_persona():
    async with AIMusicClient() as client:
        # Create persona from song
        persona = await client.suno.create_persona(
            song_url="https://example.com/reference.mp3",
            persona_name="My Custom Voice",
            wait_for_completion=True
        )

        # Use persona in generation
        result = await client.suno.create_persona_music(
            persona_id=persona.persona_id,
            lyrics="Your custom lyrics...",
            style="pop, upbeat",
            wait_for_completion=True
        )

        print(f"Song with persona: {result.clips[0].audio_url}")

asyncio.run(use_persona())
```

See [Suno Guide](../guides/suno.md) for full documentation.
