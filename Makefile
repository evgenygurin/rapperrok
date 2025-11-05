.PHONY: help install dev test lint format quality clean docs

help:  ## Show this help message
	@echo "RapperRok - AI Music API Python Client"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	uv pip install -e .

dev:  ## Install with development dependencies
	uv pip install -e ".[dev]"

test:  ## Run tests with coverage
	uv run pytest --cov=src/rapperrok --cov-report=term-missing --cov-report=html

test-unit:  ## Run unit tests only
	uv run pytest tests/unit -v

test-integration:  ## Run integration tests (requires API key)
	uv run pytest tests/integration -v

lint:  ## Run linters
	uv run ruff check src/ tests/
	uv run mypy src/

format:  ## Format code
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

quality: lint test  ## Run all quality checks

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	uv build

publish-test:  ## Publish to TestPyPI
	uv run twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	uv run twine upload dist/*

docs:  ## Build documentation
	cd docs && uv run make html

docs-serve:  ## Serve documentation locally
	cd docs && uv run make livehtml

pre-commit:  ## Install pre-commit hooks
	uv run pre-commit install

run-examples:  ## Run all examples (requires API key)
	uv run python examples/01_basic_usage.py
