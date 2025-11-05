"""Producer API advanced operations examples."""

import asyncio

from rapperrok import AIMusicClient


async def all_producer_operations():
    """Demonstrate all Producer operations."""
    print("\n=== Producer API Operations ===\n")

    async with AIMusicClient() as client:
        # 1. Create new music
        print("1. Creating new music...")
        create_result = await client.producer.create_music(
            operation="create",
            description="electronic dance music with heavy bass drops",
            duration=60,
            style="EDM, dubstep",
            wait_for_completion=True,
        )
        audio_id = create_result.clips[0].clip_id
        print(f"   Created: {audio_id}")
        print(f"   Audio URL: {create_result.clips[0].audio_url}")

        # 2. Extend existing track
        print("\n2. Extending track...")
        extend_result = await client.producer.create_music(
            operation="extend",
            audio_id=audio_id,
            duration=30,
            wait_for_completion=True,
        )
        print(f"   Extended: {extend_result.clips[0].clip_id}")

        # 3. Create cover version
        print("\n3. Creating cover version...")
        cover_result = await client.producer.create_music(
            operation="cover",
            audio_url=create_result.clips[0].audio_url,
            style="acoustic, piano",
            wait_for_completion=True,
        )
        print(f"   Cover: {cover_result.clips[0].clip_id}")

        # 4. Replace section
        print("\n4. Replacing section...")
        replace_result = await client.producer.create_music(
            operation="replace",
            audio_id=audio_id,
            replace_section={"start": 10, "end": 20},
            description="calm ambient interlude",
            wait_for_completion=True,
        )
        print(f"   Replaced: {replace_result.clips[0].clip_id}")

        # 5. Swap vocals
        print("\n5. Swapping vocals...")
        swap_vocal_result = await client.producer.create_music(
            operation="swap_vocal",
            audio_id=audio_id,
            vocal_style="opera singer, dramatic, powerful",
            wait_for_completion=True,
        )
        print(f"   Vocals swapped: {swap_vocal_result.clips[0].clip_id}")

        # 6. Swap instrumental
        print("\n6. Swapping instrumental...")
        swap_instr_result = await client.producer.create_music(
            operation="swap_instrumental",
            audio_id=audio_id,
            instrumental_style="jazz band, saxophone, piano",
            wait_for_completion=True,
        )
        print(f"   Instrumental swapped: {swap_instr_result.clips[0].clip_id}")

        # 7. Create variation
        print("\n7. Creating variation...")
        variation_result = await client.producer.create_music(
            operation="variation",
            audio_id=audio_id,
            variation_intensity=0.7,
            wait_for_completion=True,
        )
        print(f"   Variation: {variation_result.clips[0].clip_id}")


async def upload_and_modify():
    """Example: Upload existing audio and modify it."""
    print("\n=== Upload and Modify ===\n")

    async with AIMusicClient() as client:
        # Upload your audio file
        print("Uploading audio file...")
        upload = await client.producer.upload_music("path/to/your/audio.mp3")
        print(f"Uploaded: {upload.audio_id}")

        # Extend the uploaded audio
        print("Extending uploaded audio...")
        result = await client.producer.create_music(
            operation="extend",
            audio_id=upload.audio_id,
            duration=30,
            wait_for_completion=True,
        )
        print(f"Extended: {result.clips[0].audio_url}")


async def download_formats():
    """Example: Download music in different formats."""
    print("\n=== Download in Different Formats ===\n")

    async with AIMusicClient() as client:
        # Create music
        result = await client.producer.create_music(
            operation="create",
            description="chill lo-fi hip hop beat",
            duration=60,
            wait_for_completion=True,
        )

        clip_id = result.clips[0].clip_id

        # Download as MP3
        print("Downloading as MP3...")
        mp3 = await client.producer.download_music(clip_id, format="mp3")
        print(f"MP3 URL: {mp3.download_url}")

        # Download as WAV
        print("Downloading as WAV...")
        wav = await client.producer.download_music(clip_id, format="wav")
        print(f"WAV URL: {wav.download_url}")
        print(f"File size: {wav.file_size} bytes")


async def main():
    """Run all Producer examples."""
    try:
        await all_producer_operations()
        # await upload_and_modify()  # Requires actual audio file
        await download_formats()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
