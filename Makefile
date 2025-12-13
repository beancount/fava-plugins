# Run tests and linters
.PHONY: all
all: lint test

# Run tests
.PHONY: test
test:
	uv run pytest

# Run linters
.PHONY: lint
lint:
	uv run pre-commit run -a
	uv run mypy

# Build the distribution (sdist and wheel).
.PHONY: dist
dist:
	rm -f dist/*.tar.gz
	rm -f dist/*.whl
	uv build
	twine check dist/*

# Update the lock file.
.PHONY: update
update:
	uv lock --upgrade
	uvx gha-update
	uv run pre-commit autoupdate

# Upload the distribution
.PHONY: upload
upload: dist
	twine upload dist/*
