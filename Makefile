.PHONY: install-dev test lint check

install-dev:
	python -m venv .venv
	. .venv/bin/activate && pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check src tests

check: lint test

