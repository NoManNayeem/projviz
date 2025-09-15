# Project VizTree Makefile

.PHONY: help install install-dev test lint format clean build publish

help:  ## Show this help message
	@echo "Project VizTree Development Commands"
	@echo "===================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pip install -e .

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=src/projviz --cov-report=html --cov-report=term

lint:  ## Run linting
	flake8 src/ tests/
	mypy src/

format:  ## Format code
	black src/ tests/
	isort src/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python -m build

publish:  ## Publish to PyPI (requires twine)
	twine upload dist/*

scan-example:  ## Scan current project as example
	python -m projviz.cli scan --output example_structure.json

serve-example:  ## Serve example structure
	python -m projviz.cli serve --json-file example_structure.json --port 8000

run-example:  ## Scan and serve in one command
	python -m projviz.cli run --port 8000
