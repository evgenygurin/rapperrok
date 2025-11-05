# Changelog

All notable changes to RapperRok will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-05

### Added

- Initial release of RapperRok Python client
- Support for Suno V4 API operations
  - Create music from description
  - Create music with custom lyrics
  - Extend and concatenate tracks
  - Cover existing songs
  - Stems separation (basic 2-track and full 12-track)
  - Custom voice persona creation and usage
  - WAV and MIDI export
  - Upload music files
- Support for Producer (FUZZ-2.0) API
  - Create, extend, cover, replace operations
  - Swap vocals and instrumentals
  - Create variations
  - Upload and download in multiple formats
- Support for Nuro API
  - Create vocal music (up to 4 minutes)
  - Create instrumental music
  - Extensive customization options
- Webhook integration
  - WebhookHandler for signature verification
  - Event parsing and processing
  - Example integrations for FastAPI, Flask, Django
- Credits management
  - Check credit balance
  - Track usage
- Error handling
  - Comprehensive exception hierarchy
  - Specific exceptions for common errors
  - Retry logic with exponential backoff
- CLI tool
  - Generate music from command line
  - Check credits
  - Get task status
- Documentation
  - Complete user guides
  - API reference
  - Tutorials and examples
- Testing
  - Unit tests with pytest
  - Integration tests
  - Mock clients for testing
- Development tools
  - Ruff for linting and formatting
  - mypy for type checking
  - pre-commit hooks
  - uv for dependency management

### Fixed

- SSL/TLS connection issues with API base URL
- API endpoint compatibility with updated base URL (api.aimusicapi.ai)

### Changed

- Migrated all commands to use `uv` for consistent dependency management
- Updated base URL from aimusicapi.com to aimusicapi.ai

## [Unreleased]

### Planned

- Additional model support (Udio, Riffusion updates)
- Enhanced caching mechanisms
- Batch operation optimizations
- More comprehensive examples
- Video generation features
- Advanced audio processing options

## Version History

- **0.1.0** (2024-11-05) - Initial release

---

For detailed commit history, see [GitHub Releases](https://github.com/rapperrok/rapperrok/releases).

## Contributing

See [CONTRIBUTING.md](contributing.md) for information on how to contribute to RapperRok.

## Support

- **Issues**: [GitHub Issues](https://github.com/rapperrok/rapperrok/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rapperrok/rapperrok/discussions)
- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
