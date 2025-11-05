"""Data models for Suno API."""

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from ..common.models import MusicResult, TaskResponse, VoiceGender


class SunoCreateRequest(BaseModel):
    """Request to create music with Suno."""

    description: str = Field(..., description="Music description or prompt")
    duration: int = Field(default=30, ge=10, le=240, description="Duration in seconds")
    voice_gender: VoiceGender | None = Field(None, description="Voice gender for vocals")
    auto_lyrics: bool = Field(
        default=False,
        description="Auto-generate lyrics from description",
    )
    webhook_url: str | None = Field(None, description="Webhook URL for completion")


class SunoCreateWithLyricsRequest(BaseModel):
    """Request to create music with custom lyrics."""

    lyrics: str = Field(..., description="Song lyrics")
    style: str = Field(..., description="Musical style (e.g., 'rock, guitar, drums')")
    title: str | None = Field(None, description="Song title")
    voice_gender: VoiceGender | None = Field(None, description="Voice gender")
    webhook_url: str | None = Field(None, description="Webhook URL")


class SunoDescribeMusicRequest(BaseModel):
    """Request to generate music from short description."""

    description: str = Field(
        ...,
        max_length=200,
        description="Short music description",
    )
    voice_gender: VoiceGender | None = None
    webhook_url: str | None = None


class SunoExtendRequest(BaseModel):
    """Request to extend existing music."""

    audio_id: str = Field(..., description="Clip ID to extend")
    duration: int = Field(default=30, ge=10, le=120, description="Extension duration")
    webhook_url: str | None = None


class SunoConcatRequest(BaseModel):
    """Request to concatenate music clips."""

    clip_ids: list[str] = Field(
        ...,
        min_length=2,
        max_length=10,
        description="List of clip IDs to concatenate",
    )
    webhook_url: str | None = None


class SunoCoverRequest(BaseModel):
    """Request to create song cover."""

    audio_url: HttpUrl | str = Field(..., description="Original song URL")
    style: str | None = Field(None, description="Cover style")
    voice_gender: VoiceGender | None = None
    webhook_url: str | None = None


class SunoStemsBasicResponse(BaseModel):
    """Response from stems basic separation (2 tracks)."""

    song_id: str
    vocals_url: HttpUrl | str = Field(..., description="Isolated vocals URL")
    instrumental_url: HttpUrl | str = Field(..., description="Instrumental track URL")


class SunoStemsFullResponse(BaseModel):
    """Response from stems full separation (12 tracks)."""

    song_id: str
    lead_vocals_url: HttpUrl | str
    backing_vocals_url: HttpUrl | str
    drums_url: HttpUrl | str
    bass_url: HttpUrl | str
    piano_url: HttpUrl | str
    guitar_url: HttpUrl | str
    strings_url: HttpUrl | str
    synth_url: HttpUrl | str
    brass_url: HttpUrl | str
    woodwinds_url: HttpUrl | str
    fx_url: HttpUrl | str
    other_url: HttpUrl | str


class SunoPersonaRequest(BaseModel):
    """Request to create voice persona."""

    audio_url: HttpUrl | str = Field(
        ...,
        description="Reference audio URL to train persona",
    )
    persona_name: str = Field(..., description="Name for the persona")
    description: str | None = Field(None, description="Persona description")


class SunoPersonaResponse(BaseModel):
    """Response with created persona."""

    persona_id: str
    persona_name: str
    status: Literal["training", "ready", "failed"]
    training_progress: int | None = Field(
        None,
        ge=0,
        le=100,
        description="Training progress percentage",
    )


class SunoPersonaMusicRequest(BaseModel):
    """Request to create music with persona voice."""

    persona_id: str = Field(..., description="ID of trained persona")
    description: str | None = Field(None, description="Music description")
    lyrics: str | None = Field(None, description="Custom lyrics")
    style: str | None = Field(None, description="Musical style")
    duration: int = Field(default=30, ge=10, le=240)
    webhook_url: str | None = None


class SunoUploadRequest(BaseModel):
    """Request to upload music file."""

    file_path: str = Field(..., description="Path to audio file to upload")
    title: str | None = Field(None, description="Track title")
    description: str | None = Field(None, description="Track description")


class SunoUploadResponse(BaseModel):
    """Response with uploaded music ID."""

    audio_id: str = Field(..., description="Uploaded audio clip ID")
    audio_url: HttpUrl | str


class SunoWAVRequest(BaseModel):
    """Request to convert to WAV format."""

    song_id: str = Field(..., description="Song ID to convert")


class SunoWAVResponse(BaseModel):
    """Response with WAV file URL."""

    song_id: str
    wav_url: HttpUrl | str = Field(..., description="High-quality WAV file URL")
    file_size: int | None = Field(None, description="File size in bytes")


class SunoMIDIRequest(BaseModel):
    """Request to get MIDI data."""

    clip_id: str = Field(..., description="Clip ID to extract MIDI from")


class SunoMIDIResponse(BaseModel):
    """Response with MIDI data."""

    clip_id: str
    midi_url: HttpUrl | str = Field(..., description="MIDI file URL")
    has_vocals: bool | None = None
    has_drums: bool | None = None
    has_bass: bool | None = None


class SunoMusicResponse(MusicResult):
    """Extended music result for Suno with additional metadata."""

    model_version: str | None = Field(None, description="Suno model version (e.g., v4)")
    has_vocals: bool | None = None
    voice_gender: VoiceGender | None = None
    persona_id: str | None = None


class SunoTaskResponse(TaskResponse):
    """Suno-specific task response."""

    clips: list[SunoMusicResponse] = Field(default_factory=list)
