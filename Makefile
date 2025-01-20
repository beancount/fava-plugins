# Run tests
.PHONY: test
test:
	tox -e py

# Run linters
.PHONY: lint
lint:
	pre-commit run -a

# Build the distribution (sdist and wheel).
.PHONY: dist
dist:
	rm -f dist/*.tar.gz
	rm -f dist/*.whl
	python -m build
	twine check dist/*

# Upload the distribution
.PHONY: upload
upload: dist
	twine upload dist/*
