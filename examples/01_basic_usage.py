"""Basic usage examples for RapperRok AI Music API client."""

import asyncio
import os

from rapperrok import AIMusicClient


async def basic_suno_example():
    """Basic example: Create music with Suno."""
    print("\n=== Basic Suno Music Generation ===\n")

    async with AIMusicClient() as client:
        # Create music from description
        result = await client.suno.create_music(
            description="upbeat electronic dance music with strong bass",
            duration=30,
            voice_gender="female",
            wait_for_completion=True,
        )

        print(f"Status: {result.status}")
        print(f"Generated {len(result.clips)} clip(s)")

        for clip in result.clips:
            print(f"\nClip ID: {clip.clip_id}")
            print(f"Audio URL: {clip.audio_url}")
            if clip.video_url:
                print(f"Video URL: {clip.video_url}")


async def producer_fast_generation():
    """Example: Fast music generation with Producer."""
    print("\n=== Producer Fast Generation (30 seconds) ===\n")

    async with AIMusicClient() as client:
        result = await client.producer.create_music(
            operation="create",
            description="energetic rock track with guitar solos",
            duration=60,
            wait_for_completion=True,
        )

        print(f"Generation time: {result.generation_time}s")
        print(f"Audio URL: {result.clips[0].audio_url}")


async def nuro_full_song():
    """Example: Generate full-length song with Nuro."""
    print("\n=== Nuro Full-Length Song (4 minutes) ===\n")

    async with AIMusicClient() as client:
        result = await client.nuro.create_vocal_music(
            prompt="epic orchestral soundtrack with choir",
            duration=240,
            style="cinematic",
            wait_for_completion=True,
        )

        print(f"Duration: {result.clips[0].metadata.duration}s")
        print(f"Audio URL: {result.clips[0].audio_url}")


async def check_credits():
    """Example: Check credit balance."""
    print("\n=== Credit Balance ===\n")

    async with AIMusicClient() as client:
        credits = await client.get_credits()

        print(f"Total Credits: {credits.total}")
        print(f"Used: {credits.used}")
        print(f"Available: {credits.available}")
        if credits.monthly_quota:
            print(f"Monthly Quota: {credits.monthly_quota}")


async def main():
    """Run all basic examples."""
    # Set API key from environment
    if not os.getenv("AIMUSIC_API_KEY"):
        print("Please set AIMUSIC_API_KEY environment variable")
        return

    try:
        await check_credits()
        await basic_suno_example()
        await producer_fast_generation()
        await nuro_full_song()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
