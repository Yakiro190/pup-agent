# Contributing to Pup Agent

Thanks for your interest in improving Pup Agent 🐶

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Development Workflow

1. Fork the repository
2. Create a branch from `main`
3. Make your changes
4. Run quality checks locally
5. Open a Pull Request

## Quality Checks (required)

```bash
ruff check src tests
pytest
```

## Commit Style

Please use clear, conventional-style commit messages when possible:

- `feat: add x`
- `fix: handle y`
- `docs: improve z`

## Pull Request Checklist

- [ ] Focused change (one purpose per PR)
- [ ] `ruff check src tests` passes
- [ ] `pytest` passes
- [ ] README/docs updated (if needed)
- [ ] No secrets or tokens committed

## Reporting Bugs

Open an issue and include:
- expected behavior,
- actual behavior,
- steps to reproduce,
- environment details (OS, Python version).

