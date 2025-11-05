"""Unit tests for utility functions."""

import pytest

from rapperrok.common.utils import (
    estimate_credits,
    format_duration,
    parse_clip_id,
    sanitize_filename,
    validate_audio_url,
    verify_webhook_signature,
)


def test_format_duration():
    """Test duration formatting."""
    assert format_duration(30) == "30s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(120) == "2m"
    assert format_duration(3661) == "1h 1m 1s"


def test_sanitize_filename():
    """Test filename sanitization."""
    assert sanitize_filename("my:song.mp3") == "my_song.mp3"
    assert sanitize_filename("song/test") == "song_test"
    assert sanitize_filename("   test   ") == "test"
    assert sanitize_filename("") == "unnamed"


def test_parse_clip_id():
    """Test clip ID parsing."""
    assert parse_clip_id("clip_123") == "clip_123"
    assert parse_clip_id("https://example.com/clip/clip_456") == "clip_456"


def test_estimate_credits():
    """Test credit estimation."""
    assert estimate_credits("suno", "create") == 10
    assert estimate_credits("suno", "stems_basic") == 20
    assert estimate_credits("suno", "stems_full") == 50
    assert estimate_credits("producer", "create") == 10
    assert estimate_credits("nuro", "vocal") == 20


def test_validate_audio_url():
    """Test audio URL validation."""
    assert validate_audio_url("https://example.com/song.mp3")
    assert validate_audio_url("https://example.com/song.wav")
    assert not validate_audio_url("https://example.com/image.jpg")


def test_verify_webhook_signature():
    """Test webhook signature verification."""
    payload = {"test": "data"}
    secret = "my_secret"

    # Generate valid signature
    import hashlib
    import hmac
    import json

    payload_str = json.dumps(payload, separators=(",", ":"))
    valid_signature = hmac.new(
        secret.encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Test valid signature
    assert verify_webhook_signature(payload, valid_signature, secret)

    # Test invalid signature
    assert not verify_webhook_signature(payload, "invalid_signature", secret)
