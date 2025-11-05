"""Advanced Suno API examples."""

import asyncio
from pathlib import Path

from rapperrok import AIMusicClient, download_audio


async def custom_lyrics_example():
    """Example: Create music with custom lyrics."""
    print("\n=== Custom Lyrics ===\n")

    lyrics = """
    Verse 1:
    Walking down the street on a sunny day
    Feeling all the vibes in every way

    Chorus:
    This is my song, sing along
    Life is beautiful, nothing's wrong
    """

    async with AIMusicClient() as client:
        result = await client.suno.create_music_with_lyrics(
            lyrics=lyrics,
            style="indie rock, acoustic guitar, drums",
            title="My Sunny Day",
            voice_gender="male",
            wait_for_completion=True,
        )

        print(f"Created: {result.clips[0].metadata.title}")
        print(f"Audio URL: {result.clips[0].audio_url}")


async def extend_and_concat_example():
    """Example: Extend music and concatenate clips."""
    print("\n=== Extend and Concatenate ===\n")

    async with AIMusicClient() as client:
        # Create initial clip
        print("Creating initial clip...")
        result1 = await client.suno.create_music(
            description="calm piano melody",
            duration=30,
            wait_for_completion=True,
        )
        clip1_id = result1.clips[0].clip_id
        print(f"Clip 1: {clip1_id}")

        # Extend the clip
        print("Extending clip...")
        result2 = await client.suno.extend_music(
            audio_id=clip1_id,
            duration=30,
            wait_for_completion=True,
        )
        clip2_id = result2.clips[0].clip_id
        print(f"Clip 2 (extended): {clip2_id}")

        # Concatenate both clips
        print("Concatenating clips...")
        final = await client.suno.concat_music(
            clip_ids=[clip1_id, clip2_id],
            wait_for_completion=True,
        )

        print(f"Final concatenated track: {final.clips[0].audio_url}")


async def stems_separation_example():
    """Example: Separate music into stems."""
    print("\n=== Stems Separation ===\n")

    async with AIMusicClient() as client:
        # Create a song
        print("Creating song...")
        result = await client.suno.create_music(
            description="rock song with vocals, guitar, drums, bass",
            duration=30,
            voice_gender="male",
            wait_for_completion=True,
        )

        song_id = result.clips[0].clip_id
        print(f"Song ID: {song_id}")

        # Basic stems (vocals + instrumental)
        print("\nExtracting basic stems...")
        basic_stems = await client.suno.stems_basic(song_id)
        print(f"Vocals: {basic_stems.vocals_url}")
        print(f"Instrumental: {basic_stems.instrumental_url}")

        # Full stems (12 tracks)
        print("\nExtracting full stems...")
        full_stems = await client.suno.stems_full(song_id)
        print(f"Lead Vocals: {full_stems.lead_vocals_url}")
        print(f"Drums: {full_stems.drums_url}")
        print(f"Bass: {full_stems.bass_url}")
        print(f"Guitar: {full_stems.guitar_url}")


async def persona_voice_example():
    """Example: Create and use custom voice persona."""
    print("\n=== Custom Voice Persona ===\n")

    async with AIMusicClient() as client:
        # Upload reference audio to create persona
        print("Creating persona from reference audio...")

        # Note: You need to provide a reference audio URL
        reference_audio_url = "https://example.com/my_voice.mp3"

        persona = await client.suno.create_persona(
            audio_url=reference_audio_url,
            persona_name="my_custom_voice",
            description="Male singer, soft voice",
            wait_for_training=True,
        )

        print(f"Persona ID: {persona.persona_id}")
        print(f"Status: {persona.status}")

        # Use persona to generate music
        print("\nGenerating music with custom persona...")
        result = await client.suno.create_persona_music(
            persona_id=persona.persona_id,
            lyrics="This is my song with my custom voice",
            style="pop, electronic",
            duration=30,
            wait_for_completion=True,
        )

        print(f"Audio URL: {result.clips[0].audio_url}")


async def wav_and_midi_export():
    """Example: Export to WAV and MIDI formats."""
    print("\n=== WAV and MIDI Export ===\n")

    async with AIMusicClient() as client:
        # Create music
        result = await client.suno.create_music(
            description="piano melody",
            duration=30,
            wait_for_completion=True,
        )

        song_id = result.clips[0].clip_id

        # Get WAV version
        print("Converting to WAV...")
        wav = await client.suno.get_wav(song_id)
        print(f"WAV URL: {wav.wav_url}")

        # Get MIDI data
        print("Extracting MIDI...")
        midi = await client.suno.get_midi(song_id)
        print(f"MIDI URL: {midi.midi_url}")


async def download_music_example():
    """Example: Download generated music."""
    print("\n=== Download Music ===\n")

    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)

    async with AIMusicClient() as client:
        # Create music
        result = await client.suno.create_music(
            description="happy ukulele music",
            duration=30,
            wait_for_completion=True,
        )

        audio_url = result.clips[0].audio_url
        output_path = output_dir / "my_song.mp3"

        # Download
        print(f"Downloading to {output_path}...")
        await download_audio(audio_url, output_path)
        print("Download complete!")


async def main():
    """Run all advanced Suno examples."""
    examples = [
        ("Custom Lyrics", custom_lyrics_example),
        ("Extend and Concatenate", extend_and_concat_example),
        ("Stems Separation", stems_separation_example),
        ("WAV and MIDI Export", wav_and_midi_export),
        ("Download Music", download_music_example),
        # ("Persona Voice", persona_voice_example),  # Requires reference audio
    ]

    for name, example_func in examples:
        try:
            await example_func()
        except Exception as e:
            print(f"Error in {name}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
