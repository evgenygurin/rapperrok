# Tutorial: Creating Your First Song

In this tutorial, you'll learn how to create your first AI-generated song using RapperRok.

## What You'll Build

By the end of this tutorial, you'll have:

- Generated a complete song with vocals
- Downloaded the audio file
- Learned basic RapperRok operations

**Time:** 10 minutes
**Level:** Beginner

## Prerequisites

- RapperRok installed (`pip install rapperrok`)
- API key from [aimusicapi.ai](https://aimusicapi.ai/dashboard/apikey)
- Basic Python knowledge

## Step 1: Set Up Your Environment

Create a new directory for your project:

```bash
mkdir my-first-song
cd my-first-song
```

Create a `.env` file:

```bash
AIMUSIC_API_KEY=sk_your_api_key_here
```

## Step 2: Create Your First Script

Create a file called `first_song.py`:

```python
import asyncio
from rapperrok import AIMusicClient
from rapperrok.utils import download_audio

async def main():
    # Initialize client
    async with AIMusicClient() as client:
        print("🎵 Starting music generation...")

        # Check credits
        credits = await client.get_credits()
        print(f"💰 Available credits: {credits.available}")

        if credits.available < 10:
            print("❌ Not enough credits!")
            return

        # Generate music
        print("🎼 Generating your first song...")
        result = await client.suno.create_music(
            description="upbeat pop song about coding and technology",
            duration=60,  # 60 seconds
            voice_gender="male",
            wait_for_completion=True
        )

        # Get the first clip
        clip = result.clips[0]

        print("✅ Song generated successfully!")
        print(f"   Title: {clip.title}")
        print(f"   Audio URL: {clip.audio_url}")
        print(f"   Video URL: {clip.video_url}")

        # Download the song
        print("💾 Downloading...")
        await download_audio(clip.audio_url, "my_first_song.mp3")

        print("✅ Done! Check my_first_song.mp3")

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 3: Run Your Script

```bash
python first_song.py
```

You should see:

```
🎵 Starting music generation...
💰 Available credits: 1000
🎼 Generating your first song...
✅ Song generated successfully!
   Title: Tech Vibes
   Audio URL: https://cdn.aimusicapi.ai/abc123.mp3
   Video URL: https://cdn.aimusicapi.ai/abc123.mp4
💾 Downloading...
✅ Done! Check my_first_song.mp3
```

## Step 4: Customize Your Song

Now let's make it more interesting with custom lyrics!

Create `custom_song.py`:

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        # Custom lyrics
        lyrics = """
        [Verse 1]
        Writing code all day and night
        Making apps that work just right
        Python, JavaScript, and more
        Tech is what I'm living for

        [Chorus]
        We are the coders, building dreams
        Creating magic on our screens
        Line by line, we make it real
        That's the programmer's appeal

        [Verse 2]
        Debugging till the morning light
        Finally got the code just right
        Push to prod, it's live today
        Another bug-free release, hooray!

        [Chorus]
        We are the coders, building dreams
        Creating magic on our screens
        Line by line, we make it real
        That's the programmer's appeal
        """

        print("🎵 Creating custom song with lyrics...")

        result = await client.suno.create_music_with_lyrics(
            lyrics=lyrics,
            style="pop rock, upbeat, energetic, guitar and drums",
            title="The Programmer's Anthem",
            voice_gender="male",
            wait_for_completion=True
        )

        clip = result.clips[0]

        print(f"✅ Created: {clip.title}")
        print(f"   Listen: {clip.audio_url}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python custom_song.py
```

## Step 5: Extend Your Song

Want to make it longer? Let's extend it!

Create `extend_song.py`:

```python
import asyncio
from rapperrok import AIMusicClient

async def main():
    async with AIMusicClient() as client:
        # First, create a short song
        print("🎵 Creating initial song...")
        initial = await client.suno.create_music(
            description="calm piano melody, peaceful",
            duration=30,
            instrumental=True,
            wait_for_completion=True
        )

        audio_id = initial.clips[0].id
        print(f"✅ Created: {initial.clips[0].audio_url}")

        # Extend it
        print("🎼 Extending song...")
        extended = await client.suno.extend_music(
            audio_id=audio_id,
            duration=60,  # Add 60 more seconds
            wait_for_completion=True
        )

        print(f"✅ Extended: {extended.clips[0].audio_url}")
        print(f"   Total duration: ~90 seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 6: Separate Vocals and Instrumental

Let's separate the vocals from the instrumental:

Create `separate_stems.py`:

```python
import asyncio
from rapperrok import AIMusicClient
from rapperrok.utils import download_audio

async def main():
    async with AIMusicClient() as client:
        # Create a song with vocals
        print("🎵 Creating song with vocals...")
        song = await client.suno.create_music(
            description="rock song with powerful vocals",
            duration=30,
            wait_for_completion=True
        )

        song_id = song.clips[0].id
        print(f"✅ Song created: {song.clips[0].audio_url}")

        # Separate vocals and instrumental
        print("🎼 Separating stems...")
        stems = await client.suno.stems_basic(song_id=song_id)

        print("✅ Stems separated!")
        print(f"   Vocals: {stems.vocals_url}")
        print(f"   Instrumental: {stems.instrumental_url}")

        # Download both
        print("💾 Downloading stems...")
        await download_audio(stems.vocals_url, "vocals.mp3")
        await download_audio(stems.instrumental_url, "instrumental.mp3")

        print("✅ Done! Check vocals.mp3 and instrumental.mp3")

if __name__ == "__main__":
    asyncio.run(main())
```

## What You Learned

In this tutorial, you learned how to:

- ✅ Set up RapperRok and authenticate
- ✅ Check your credit balance
- ✅ Generate music from a description
- ✅ Create music with custom lyrics
- ✅ Extend existing songs
- ✅ Separate vocals and instrumentals
- ✅ Download generated audio files

## Next Steps

Now that you've created your first song, try:

- [Batch Generation Tutorial](batch-generation.md) - Generate multiple songs
- [Webhook Tutorial](webhook-server.md) - Set up async notifications
- [Suno Guide](../guides/suno.md) - Master all Suno features
- [Producer Guide](../guides/producer.md) - Fast 30-second generation

## Troubleshooting

### "Not enough credits"

Purchase credits at [aimusicapi.ai/pricing](https://aimusicapi.ai/pricing)

### "Authentication failed"

Check your API key is correct in `.env` file

### "Generation failed"

Try a different description or check the error message

### "Timeout error"

Increase timeout or use webhooks for long operations

## Get Help

- [Documentation](/) - Full documentation
- [Examples](../examples.md) - More code examples
- [GitHub Issues](https://github.com/rapperrok/rapperrok/issues) - Report bugs
