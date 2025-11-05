# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Comprehensive Documentation (2025-11-05)

- **docs/API_REFERENCE.md**: Complete API reference with links to all official AI Music API documentation
  - Organized by model (Suno, Producer, Nuro, Riffusion)
  - Getting Started guides (Introduction, Credits, Error Handling, Webhooks)
  - Quick reference tables and authentication examples
  - Links to official documentation and support resources

- **docs/MODELS.md**: Detailed comparison and guide to all AI music generation models
  - Complete feature matrices comparing all 4 models
  - Performance comparisons (generation time, quality, duration)
  - Decision trees for choosing the right model
  - Use case recommendations for Content Creators, Musicians, Developers, Businesses
  - Credits cost breakdown and optimization strategies
  - Technical specifications (audio formats, API limits)
  - Code examples for each model

- **docs/ENDPOINTS.md**: Complete API endpoints reference with practical examples
  - All endpoints organized by model with request/response examples
  - JSON examples for every operation
  - Credits costs per operation
  - HTTP status codes and error responses
  - Rate limiting details and retry strategies
  - Webhook integration and signature verification
  - Best practices for production use

- **docs/README.md**: Documentation index and quick start guide
  - Quick navigation to all documentation files
  - Model selection guide
  - Code examples and common patterns
  - Credits pricing table
  - External resources and support links

#### Documentation Improvements

- **README.md**: Added comprehensive Documentation section
  - Links to all new documentation files
  - Quick links organized by model (Suno, Producer, Nuro)
  - Official AI Music API resources
  - Enhanced navigation with badges linking to docs

- **examples/README.md**: Enhanced with documentation references
  - Links to comprehensive API documentation at the top
  - Model selection guide reference
  - API documentation section organized by model
  - Links to specific documentation for each example

### Fixed

- Fixed base URL references to use `api.aimusicapi.ai` (previous commit)
- Fixed credits endpoint documentation (previous commit)

## [0.1.0] - 2025-11-05

### Added

- Initial release of RapperRok Python client
- Support for Suno V4 API
- Support for Producer (FUZZ-2.0) API
- Support for Nuro API
- Support for Riffusion API (deprecated)
- Async/await support with httpx
- Type-safe models with Pydantic
- Retry logic with exponential backoff
- Rich CLI with progress tracking
- Comprehensive error handling
- Webhook integration support
- Examples for all major features

### Documentation

- README.md with feature overview
- QUICKSTART.md for getting started
- CONTRIBUTING.md for contributors
- API_STATUS.md for service status
- Examples in examples/ directory

---

## Version History

### Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

### Release Notes

See [GitHub Releases](https://github.com/rapperrok/rapperrok/releases) for detailed release notes.

---

## Links

- [GitHub Repository](https://github.com/rapperrok/rapperrok)
- [Documentation](https://rapperrok.readthedocs.io)
- [AI Music API Docs](https://docs.aimusicapi.ai)
- [AI Music API Changelog](https://aimusicapi.featurebase.app/en/changelog)

---

**Last Updated**: November 5, 2025
