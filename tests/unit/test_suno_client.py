"""Unit tests for Suno client."""

import pytest
import respx
from httpx import Response

from rapperrok.suno import SunoClient


@pytest.mark.asyncio
@respx.mock
async def test_create_music(api_key, base_url, mock_task_response):
    """Test creating music with Suno."""
    route = respx.post(f"{base_url}/suno/v1/music/create").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music(
            description="test music",
            duration=30,
        )

    assert result.task_id == "task_test_123"
    assert result.status.value == "pending"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_create_music_with_lyrics(api_key, base_url, mock_task_response):
    """Test creating music with custom lyrics."""
    route = respx.post(f"{base_url}/suno/v1/music/create-with-lyrics").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music_with_lyrics(
            lyrics="Test lyrics",
            style="rock",
        )

    assert result.task_id == "task_test_123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_extend_music(api_key, base_url, mock_task_response):
    """Test extending music."""
    route = respx.post(f"{base_url}/suno/v1/music/extend").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.extend_music(
            audio_id="clip_123",
            duration=30,
        )

    assert result.task_id == "task_test_123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_concat_music(api_key, base_url, mock_task_response):
    """Test concatenating music clips."""
    route = respx.post(f"{base_url}/suno/v1/music/concat").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.concat_music(
            clip_ids=["clip_1", "clip_2"],
        )

    assert result.task_id == "task_test_123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_get_task(api_key, base_url, mock_completed_response):
    """Test getting task status."""
    route = respx.get(f"{base_url}/suno/v1/music/get").mock(
        return_value=Response(200, json=mock_completed_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.get_task("task_test_123")

    assert result.status.value == "completed"
    assert len(result.clips) == 1
    assert result.clips[0].clip_id == "clip_test_456"
    assert route.called
