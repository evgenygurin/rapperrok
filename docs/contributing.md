# Contributing to RapperRok

Thank you for your interest in contributing to RapperRok! This document provides guidelines and instructions for contributing.

For detailed contribution guidelines, please see [CONTRIBUTING.md](https://github.com/rapperrok/rapperrok/blob/main/CONTRIBUTING.md) in the repository.

## Quick Start

1. **Fork the repository**
   ```bash
   # Visit https://github.com/rapperrok/rapperrok and click "Fork"
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rapperrok.git
   cd rapperrok
   ```

3. **Set up development environment**
   ```bash
   # Install with uv (recommended)
   make dev
   # Or manually
   uv pip install -e ".[dev]"

   # Install pre-commit hooks
   uv run pre-commit install
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

6. **Run tests and quality checks**
   ```bash
   # Run tests
   make test

   # Format code
   make format

   # Lint
   make lint

   # Type check
   uv run mypy src/

   # All checks
   make quality
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

8. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Then create PR on GitHub
   ```

## Development Setup

### Prerequisites

- Python 3.12+
- uv (recommended) or pip
- git

### Installation

```bash
# Clone repository
git clone https://github.com/rapperrok/rapperrok.git
cd rapperrok

# Install dependencies
make dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# All tests
make test

# Unit tests only
uv run pytest -m unit

# Integration tests
uv run pytest -m integration

# With coverage
uv run pytest --cov
```

### Code Quality

```bash
# Format code
make format

# Lint
make lint

# Type check
uv run mypy src/

# All quality checks
make quality
```

## Contribution Areas

### Code Contributions

- **Bug fixes** - Fix issues and improve stability
- **New features** - Add functionality
- **Performance** - Optimize code
- **Tests** - Improve test coverage

### Documentation

- **Guides** - Write tutorials and how-tos
- **API docs** - Document code
- **Examples** - Add code examples
- **Translations** - Translate documentation

### Other

- **Bug reports** - Report issues
- **Feature requests** - Suggest improvements
- **Reviews** - Review pull requests
- **Community** - Help others

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

**Examples:**

```
feat(suno): add support for MIDI export
fix(client): handle connection timeout properly
docs(guide): add webhook integration examples
test(producer): add integration tests
```

## Code Style

- **Format**: Use ruff for formatting
- **Linting**: Follow ruff rules
- **Type hints**: Add type annotations
- **Docstrings**: Use Google style
- **Imports**: Sort with isort (via ruff)

## Testing

- **Coverage**: Maintain >80% coverage
- **Unit tests**: Test individual components
- **Integration tests**: Test API integration
- **Mocks**: Use for external services

## Pull Request Process

1. **Check for existing PR** - Avoid duplicates
2. **Update documentation** - Document changes
3. **Add tests** - Test new features
4. **Pass all checks** - CI must pass
5. **Request review** - Wait for feedback
6. **Address comments** - Make requested changes
7. **Merge** - Maintainer will merge when ready

## Questions?

- **Documentation**: [https://rapperrok.readthedocs.io](https://rapperrok.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/rapperrok/rapperrok/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rapperrok/rapperrok/discussions)

## Code of Conduct

Be respectful, inclusive, and professional. We want RapperRok to be a welcoming community for everyone.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

For complete contribution guidelines, see [CONTRIBUTING.md](https://github.com/rapperrok/rapperrok/blob/main/CONTRIBUTING.md).
