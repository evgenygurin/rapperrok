# Contributing to RapperRok

Thank you for your interest in contributing to RapperRok! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- uv package manager (recommended)
- Git

### Getting Started

1. **Fork and clone the repository**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/rapperrok.git
   cd rapperrok
   ```

2. **Install uv** (if not already installed):

   ```bash
   pip install uv
   ```

3. **Install development dependencies**:

   ```bash
   make dev
   # Or manually
   uv pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:

   ```bash
   uv run pre-commit install
   ```

5. **Set up environment**:

   ```bash
   cp .env.example .env
   # Edit .env and add your AIMUSIC_API_KEY
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests with coverage
make test

# Run unit tests only (no API key needed)
make test-unit

# Run integration tests (requires API key)
make test-integration

# Run specific test file
uv run pytest tests/unit/test_suno_client.py -v

# Run specific test
uv run pytest tests/unit/test_suno_client.py::test_create_music -v
```

### Code Quality

```bash
# Format code (auto-fix)
make format

# Lint code
make lint

# Type check
uv run mypy src/

# Run all quality checks
make quality
```

### Running Examples

```bash
export AIMUSIC_API_KEY="your_key"
uv run python examples/01_basic_usage.py
```

## Code Style

- **Line length**: 88 characters (Ruff/Black standard)
- **Type hints**: Required for all public functions and methods
- **Docstrings**: Google style with examples
- **Imports**: Auto-sorted via ruff
- **Async**: Use async/await, never blocking calls

### Example Function

```python
async def create_music(
    self,
    description: str,
    *,
    duration: int = 30,
    voice_gender: VoiceGender | str | None = None,
) -> TaskResponse:
    """Create music from description.

    Args:
        description: Music description/prompt
        duration: Duration in seconds (10-240)
        voice_gender: Voice gender for vocals (male/female/random)

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
```

## Testing Guidelines

### Unit Tests

- Mock all API calls using `respx`
- Test happy path and error cases
- Use fixtures from `tests/conftest.py`
- All tests should be fast (<1 second)

Example:

```python
import pytest
import respx
from httpx import Response

@pytest.mark.asyncio
@respx.mock
async def test_suno_create(api_key, base_url, mock_task_response):
    route = respx.post(f"{base_url}/suno/v1/music/create").mock(
        return_value=Response(200, json=mock_task_response)
    )

    async with SunoClient(api_key=api_key, base_url=base_url) as client:
        result = await client.create_music(description="test")

    assert result.task_id == "task_test_123"
    assert route.called
```

### Integration Tests

- Mark with `@pytest.mark.integration`
- Only run when API key is available
- Test actual API calls (use minimal credits)
- May be slow (>5 seconds)

## Adding New Features

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/my-feature
   ```

2. **Write tests first** (TDD approach):
   - Add unit tests in `tests/unit/`
   - Add integration tests if needed

3. **Implement the feature**:
   - Update relevant client (Suno, Producer, Nuro)
   - Update Pydantic models if needed
   - Add type hints and docstrings

4. **Add example**:
   - Create or update example in `examples/`
   - Show practical usage

5. **Update documentation**:
   - Update README.md if user-facing feature
   - Update CONTRIBUTING.md if development workflow changes
   - Update QUICKSTART.md if affects quick start

6. **Run quality checks**:

   ```bash
   make quality
   ```

7. **Commit with conventional commit**:

   ```bash
   git commit -m "feat(suno): add stems full separation

   - Add stems_full() method to SunoClient
   - Returns 12 separate audio tracks
   - Add comprehensive tests
   - Update examples/02_advanced_suno.py"
   ```

8. **Push and create PR**:

   ```bash
   git push origin feature/my-feature
   ```

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:

```bash
git commit -m "feat(producer): add swap_instrumental operation"
git commit -m "fix(suno): handle timeout in wait_for_completion"
git commit -m "docs: update installation instructions"
git commit -m "test: add tests for webhook signature verification"
```

## Pull Request Process

1. **Update documentation** (README, CLAUDE.md if needed)
2. **Ensure tests pass**: `make quality`
3. **Add examples** if user-facing feature
4. **Update CHANGELOG.md** (if exists)
5. **Create PR** with clear description
6. **Address review comments**
7. **Wait for CI to pass**

### PR Checklist

- [ ] Tests added/updated
- [ ] Type hints complete
- [ ] Docstrings with examples
- [ ] Examples demonstrate feature
- [ ] Documentation updated (README, QUICKSTART, etc.)
- [ ] `make quality` passes
- [ ] No new linter warnings
- [ ] PR description is clear

## Project Structure

```text
src/rapperrok/
├── __init__.py              # Main AIMusicClient
├── common/
│   ├── base.py             # BaseAPIClient - HTTP with retry logic
│   ├── models.py           # Common Pydantic models
│   ├── exceptions.py       # Exception hierarchy
│   └── utils.py            # Utilities
├── suno/                   # Suno V4 client
├── producer/               # Producer client
├── nuro/                   # Nuro client
└── webhooks/               # Webhook handling

tests/
├── conftest.py             # Shared fixtures
├── unit/                   # Unit tests (fast, mocked)
└── integration/            # Integration tests (slow, real API)

examples/                   # Usage examples
docs/                       # Documentation
```

## Adding a New API Client

If adding support for a new AI music model:

1. Create `src/rapperrok/{model}/` directory
2. Create `client.py` with model client class
3. Create `models.py` with Pydantic models
4. Create `__init__.py` exporting client and models
5. Add client to `AIMusicClient` in `src/rapperrok/__init__.py`
6. Add tests in `tests/unit/test_{model}_client.py`
7. Add examples in `examples/`
8. Update documentation

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to RapperRok! 🎵
