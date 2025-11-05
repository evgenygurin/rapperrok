"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def api_key():
    """Test API key."""
    return "test_api_key_12345"


@pytest.fixture
def base_url():
    """Test base URL."""
    return "https://api.sunoapi.com"


@pytest.fixture
def mock_task_response():
    """Mock task response data."""
    return {
        "success": True,
        "task_id": "task_test_123",
        "status": "pending",
        "estimated_time": 30,
    }


@pytest.fixture
def mock_completed_response():
    """Mock completed task response."""
    return {
        "success": True,
        "task_id": "task_test_123",
        "status": "completed",
        "clips": [
            {
                "clip_id": "clip_test_456",
                "audio_url": "https://cdn.sunoapi.com/music/clip_test_456.mp3",
                "video_url": "https://cdn.sunoapi.com/video/clip_test_456.mp4",
                "metadata": {
                    "title": "Test Song",
                    "duration": 60,
                    "style": "test",
                    "description": "Test music",
                },
            }
        ],
    }


@pytest.fixture
def mock_credits_response():
    """Mock credits response."""
    return {
        "total": 1000,
        "used": 300,
        "available": 700,
        "monthly_quota": 500,
    }
