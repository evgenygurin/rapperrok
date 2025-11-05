"""Suno API client implementation."""

import logging
from pathlib import Path
from typing import Any

from ..common.base import BaseAPIClient
from ..common.models import PollConfig, RetryConfig, TaskResponse, VoiceGender
from .models import (
    SunoConcatRequest,
    SunoCoverRequest,
    SunoCreateRequest,
    SunoCreateWithLyricsRequest,
    SunoDescribeMusicRequest,
    SunoExtendRequest,
    SunoMIDIRequest,
    SunoMIDIResponse,
    SunoMusicResponse,
    SunoPersonaMusicRequest,
    SunoPersonaRequest,
    SunoPersonaResponse,
    SunoStemsBasicResponse,
    SunoStemsFullResponse,
    SunoTaskResponse,
    SunoUploadResponse,
    SunoWAVRequest,
    SunoWAVResponse,
)

logger = logging.getLogger(__name__)


class SunoClient:
    """Client for Suno V4 music generation API.

    Suno is the most advanced model supporting vocals, instrumentals,
    stems separation, persona creation, and various music operations.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.aimusicapi.com",
        timeout: int = 30,
        retry_config: RetryConfig | None = None,
        poll_config: PollConfig | None = None,
    ) -> None:
        """Initialize Suno client.

        Args:
            api_key: AI Music API key
            base_url: Base API URL
            timeout: Default timeout in seconds
            retry_config: Retry configuration
            poll_config: Polling configuration for async operations
        """
        self._base_client = BaseAPIClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retry_config=retry_config,
        )
        self.poll_config = poll_config or PollConfig()

    async def create_music(
        self,
        description: str,
        *,
        duration: int = 30,
        voice_gender: VoiceGender | str | None = None,
        auto_lyrics: bool = False,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Create music from description.

        Args:
            description: Music description/prompt
            duration: Duration in seconds (10-240)
            voice_gender: Voice gender for vocals (male/female/random)
            auto_lyrics: Auto-generate lyrics from description
            webhook_url: Webhook URL for async notification
            wait_for_completion: Wait for task to complete

        Returns:
            Task response with task_id

        Example:
            ```python
            result = await client.suno.create_music(
                description="upbeat electronic dance music",
                duration=60,
                voice_gender="female"
            )
            print(f"Task ID: {result.task_id}")
            ```
        """
        request = SunoCreateRequest(
            description=description,
            duration=duration,
            voice_gender=voice_gender,
            auto_lyrics=auto_lyrics,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/music/create",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def create_music_with_lyrics(
        self,
        lyrics: str,
        style: str,
        *,
        title: str | None = None,
        voice_gender: VoiceGender | str | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Create music with custom lyrics.

        Args:
            lyrics: Song lyrics
            style: Musical style (e.g., "rock, guitar, drums")
            title: Song title
            voice_gender: Voice gender
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            result = await client.suno.create_music_with_lyrics(
                lyrics="Verse 1: Walking down the street...",
                style="indie rock, acoustic guitar",
                title="My Song"
            )
            ```
        """
        request = SunoCreateWithLyricsRequest(
            lyrics=lyrics,
            style=style,
            title=title,
            voice_gender=voice_gender,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/music/create-with-lyrics",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def describe_music(
        self,
        description: str,
        *,
        voice_gender: VoiceGender | str | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Generate music from short description (describe-to-music).

        Args:
            description: Short music description (max 200 chars)
            voice_gender: Voice gender
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response
        """
        request = SunoDescribeMusicRequest(
            description=description,
            voice_gender=voice_gender,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/music/describe",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def extend_music(
        self,
        audio_id: str,
        *,
        duration: int = 30,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Extend existing music track.

        Args:
            audio_id: Clip ID to extend
            duration: Extension duration in seconds (10-120)
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            extended = await client.suno.extend_music(
                audio_id="clip_abc123",
                duration=60
            )
            ```
        """
        request = SunoExtendRequest(
            audio_id=audio_id,
            duration=duration,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/music/extend",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def concat_music(
        self,
        clip_ids: list[str],
        *,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Concatenate multiple music clips into one track.

        Args:
            clip_ids: List of clip IDs to concatenate (2-10)
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            full_track = await client.suno.concat_music(
                clip_ids=["clip_1", "clip_2", "clip_3"]
            )
            ```
        """
        request = SunoConcatRequest(clip_ids=clip_ids, webhook_url=webhook_url)

        data = await self._base_client.post(
            "/suno/v1/music/concat",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def cover_music(
        self,
        audio_url: str,
        *,
        style: str | None = None,
        voice_gender: VoiceGender | str | None = None,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Create a cover version of existing song.

        Args:
            audio_url: Original song URL
            style: Cover style
            voice_gender: Voice gender for cover
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            cover = await client.suno.cover_music(
                audio_url="https://example.com/song.mp3",
                style="acoustic, piano",
                voice_gender="male"
            )
            ```
        """
        request = SunoCoverRequest(
            audio_url=audio_url,
            style=style,
            voice_gender=voice_gender,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/music/cover",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def stems_basic(
        self,
        song_id: str,
        *,
        wait_for_completion: bool = True,
    ) -> SunoStemsBasicResponse:
        """Extract basic stems (vocals + instrumental).

        Args:
            song_id: Song ID to process
            wait_for_completion: Wait for stem separation

        Returns:
            Stems with vocals and instrumental URLs

        Example:
            ```python
            stems = await client.suno.stems_basic("song_abc123")
            print(f"Vocals: {stems.vocals_url}")
            print(f"Instrumental: {stems.instrumental_url}")
            ```
        """
        data = await self._base_client.post(
            "/suno/v1/stems/basic",
            json={"song_id": song_id},
        )

        if wait_for_completion and "task_id" in data:
            result = await self.wait_for_completion(data["task_id"])
            # Extract stems from result
            if result.clips:
                data = result.clips[0].model_dump()

        return SunoStemsBasicResponse(**data)

    async def stems_full(
        self,
        song_id: str,
        *,
        wait_for_completion: bool = True,
    ) -> SunoStemsFullResponse:
        """Extract full stems (12 separate tracks).

        Extracts: lead vocals, backing vocals, drums, bass, piano,
        guitar, strings, synth, brass, woodwinds, fx, other.

        Args:
            song_id: Song ID to process
            wait_for_completion: Wait for stem separation

        Returns:
            Full stems with all track URLs

        Example:
            ```python
            stems = await client.suno.stems_full("song_abc123")
            print(f"Drums: {stems.drums_url}")
            print(f"Bass: {stems.bass_url}")
            ```
        """
        data = await self._base_client.post(
            "/suno/v1/stems/full",
            json={"song_id": song_id},
        )

        if wait_for_completion and "task_id" in data:
            result = await self.wait_for_completion(data["task_id"])
            if result.clips:
                data = result.clips[0].model_dump()

        return SunoStemsFullResponse(**data)

    async def create_persona(
        self,
        audio_url: str,
        persona_name: str,
        *,
        description: str | None = None,
        wait_for_training: bool = True,
    ) -> SunoPersonaResponse:
        """Create custom voice persona from reference audio.

        Args:
            audio_url: Reference audio URL to train persona
            persona_name: Name for the persona
            description: Persona description
            wait_for_training: Wait for persona training to complete

        Returns:
            Persona response with ID and status

        Example:
            ```python
            persona = await client.suno.create_persona(
                audio_url="https://example.com/voice.mp3",
                persona_name="my_voice",
                description="Male singer, soft voice"
            )
            print(f"Persona ID: {persona.persona_id}")
            ```
        """
        request = SunoPersonaRequest(
            audio_url=audio_url,
            persona_name=persona_name,
            description=description,
        )

        data = await self._base_client.post(
            "/suno/v1/persona/create",
            json=request.model_dump(exclude_none=True),
        )

        persona = SunoPersonaResponse(**data)

        if wait_for_training and persona.status != "ready":
            # Poll until training complete
            persona = await self._poll_persona_status(persona.persona_id)

        return persona

    async def _poll_persona_status(
        self,
        persona_id: str,
        max_attempts: int = 60,
        interval: float = 10.0,
    ) -> SunoPersonaResponse:
        """Poll persona training status."""
        import asyncio

        for _ in range(max_attempts):
            data = await self._base_client.get(
                f"/suno/v1/persona/{persona_id}/status",
            )
            persona = SunoPersonaResponse(**data)

            if persona.status == "ready":
                return persona
            elif persona.status == "failed":
                from ..common.exceptions import TaskFailedError

                raise TaskFailedError(f"Persona training failed: {persona_id}")

            await asyncio.sleep(interval)

        from ..common.exceptions import TimeoutError as APITimeoutError

        raise APITimeoutError(f"Persona training timeout: {persona_id}")

    async def create_persona_music(
        self,
        persona_id: str,
        *,
        description: str | None = None,
        lyrics: str | None = None,
        style: str | None = None,
        duration: int = 30,
        webhook_url: str | None = None,
        wait_for_completion: bool = False,
    ) -> SunoTaskResponse:
        """Create music using custom persona voice.

        Args:
            persona_id: Trained persona ID
            description: Music description
            lyrics: Custom lyrics
            style: Musical style
            duration: Duration in seconds
            webhook_url: Webhook URL
            wait_for_completion: Wait for completion

        Returns:
            Task response

        Example:
            ```python
            music = await client.suno.create_persona_music(
                persona_id="persona_abc",
                lyrics="My custom lyrics...",
                style="pop, electronic",
                duration=60
            )
            ```
        """
        request = SunoPersonaMusicRequest(
            persona_id=persona_id,
            description=description,
            lyrics=lyrics,
            style=style,
            duration=duration,
            webhook_url=webhook_url,
        )

        data = await self._base_client.post(
            "/suno/v1/persona/music/create",
            json=request.model_dump(exclude_none=True),
        )

        response = SunoTaskResponse(**data)

        if wait_for_completion:
            return await self.wait_for_completion(response.task_id)

        return response

    async def upload_music(
        self,
        file_path: str | Path,
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> SunoUploadResponse:
        """Upload music file for processing.

        Args:
            file_path: Path to audio file
            title: Track title
            description: Track description

        Returns:
            Upload response with audio_id

        Example:
            ```python
            upload = await client.suno.upload_music(
                file_path="my_song.mp3",
                title="My Song"
            )
            print(f"Audio ID: {upload.audio_id}")
            ```
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "audio/mpeg")}
            data_dict: dict[str, Any] = {}

            if title:
                data_dict["title"] = title
            if description:
                data_dict["description"] = description

            data = await self._base_client.post(
                "/suno/v1/music/upload",
                data=data_dict if data_dict else None,
                files=files,
                timeout=120,
            )

        return SunoUploadResponse(**data)

    async def get_wav(
        self,
        song_id: str,
        *,
        wait_for_conversion: bool = True,
    ) -> SunoWAVResponse:
        """Convert song to high-quality WAV format.

        Args:
            song_id: Song ID to convert
            wait_for_conversion: Wait for conversion to complete

        Returns:
            WAV response with download URL

        Example:
            ```python
            wav = await client.suno.get_wav("song_abc123")
            print(f"WAV URL: {wav.wav_url}")
            ```
        """
        request = SunoWAVRequest(song_id=song_id)

        data = await self._base_client.post(
            "/suno/v1/music/wav",
            json=request.model_dump(),
        )

        if wait_for_conversion and "task_id" in data:
            result = await self.wait_for_completion(data["task_id"])
            if result.clips:
                wav_url = result.clips[0].audio_url
                data = {"song_id": song_id, "wav_url": wav_url}

        return SunoWAVResponse(**data)

    async def get_midi(
        self,
        clip_id: str,
    ) -> SunoMIDIResponse:
        """Extract MIDI data from clip.

        Args:
            clip_id: Clip ID to extract MIDI from

        Returns:
            MIDI response with download URL

        Example:
            ```python
            midi = await client.suno.get_midi("clip_abc123")
            print(f"MIDI URL: {midi.midi_url}")
            ```
        """
        request = SunoMIDIRequest(clip_id=clip_id)

        data = await self._base_client.post(
            "/suno/v1/music/midi",
            json=request.model_dump(),
        )

        return SunoMIDIResponse(**data)

    async def get_task(
        self,
        task_id: str,
    ) -> SunoTaskResponse:
        """Get task status and result.

        Args:
            task_id: Task ID to check

        Returns:
            Task response with status and music data

        Example:
            ```python
            result = await client.suno.get_task("task_abc123")
            if result.status == "completed":
                for clip in result.clips:
                    print(f"Music URL: {clip.audio_url}")
            ```
        """
        data = await self._base_client.get(
            "/suno/v1/music/get",
            params={"task_id": task_id},
        )

        return SunoTaskResponse(**data)

    async def wait_for_completion(
        self,
        task_id: str,
        *,
        max_attempts: int | None = None,
        interval: float | None = None,
        timeout: int | None = None,
    ) -> SunoTaskResponse:
        """Wait for task to complete.

        Args:
            task_id: Task ID to wait for
            max_attempts: Maximum polling attempts (default from config)
            interval: Polling interval in seconds (default from config)
            timeout: Total timeout in seconds (default from config)

        Returns:
            Completed task response

        Raises:
            TaskFailedError: If task fails
            TimeoutError: If task doesn't complete in time

        Example:
            ```python
            result = await client.suno.wait_for_completion("task_abc123")
            ```
        """
        import asyncio

        max_attempts = max_attempts or self.poll_config.max_attempts
        interval = interval or self.poll_config.interval
        timeout_val = timeout or self.poll_config.timeout

        start_time = asyncio.get_event_loop().time()

        for attempt in range(max_attempts):
            result = await self.get_task(task_id)

            if result.status.value == "completed":
                return result
            elif result.status.value == "failed":
                from ..common.exceptions import TaskFailedError

                error_msg = result.message or "Task failed"
                raise TaskFailedError(error_msg, task_id=task_id)

            # Check timeout
            if timeout_val:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed >= timeout_val:
                    from ..common.exceptions import TimeoutError as APITimeoutError

                    raise APITimeoutError(
                        f"Task {task_id} timeout after {elapsed:.0f}s",
                        timeout_seconds=timeout_val,
                    )

            if attempt < max_attempts - 1:
                await asyncio.sleep(interval)

        from ..common.exceptions import TimeoutError as APITimeoutError

        raise APITimeoutError(
            f"Task {task_id} did not complete within {max_attempts} attempts",
            timeout_seconds=int(max_attempts * interval),
        )

    async def close(self) -> None:
        """Close HTTP client."""
        await self._base_client.close()

    async def __aenter__(self) -> "SunoClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
