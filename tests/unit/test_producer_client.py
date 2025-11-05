"""Unit tests for Producer client."""

import pytest
import respx
from httpx import Response

from rapperrok.producer import ProducerClient


@pytest.mark.asyncio
@respx.mock
async def test_create_music(api_key, base_url, mock_task_response):
    """Test creating music with Producer."""
    route = respx.post(f"{base_url}/producer/v1/music/create").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with ProducerClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music(
            operation="create",
            description="test music",
            duration=60,
        )

    assert result.task_id == "task_test_123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_extend_operation(api_key, base_url, mock_task_response):
    """Test extend operation."""
    route = respx.post(f"{base_url}/producer/v1/music/create").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with ProducerClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music(
            operation="extend",
            audio_id="clip_123",
            duration=30,
        )

    assert result.task_id == "task_test_123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_swap_vocal(api_key, base_url, mock_task_response):
    """Test swap vocal operation."""
    route = respx.post(f"{base_url}/producer/v1/music/create").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with ProducerClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music(
            operation="swap_vocal",
            audio_id="clip_123",
            vocal_style="opera singer",
        )

    assert result.task_id == "task_test_123"
    assert route.called
