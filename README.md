# Pup Agent 🐶

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

A clean, production-style starter repository for a **working AI agent CLI**.

Pup Agent can:
- run simple autonomous tool-use loops,
- switch between a local mock provider and OpenAI,
- inspect local files with safe built-in tools,
- run in a friendly terminal chat mode.

---

## Project Structure

```text
.
├── docs/
│   └── architecture.md
├── examples/
│   └── sample-prompts.md
├── src/pup_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── cli.py
│   ├── config.py
│   ├── models.py
│   ├── tools.py
│   └── providers/
│       ├── __init__.py
│       ├── base.py
│       ├── mock_provider.py
│       └── openai_provider.py
└── tests/
    └── test_agent.py
```

---

## Quick Start

### 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

### 2) Run with mock provider (works out of the box)

```bash
pup-agent run "What time is it?"
```

### 3) Chat mode

```bash
pup-agent chat
```

### 4) Use OpenAI provider (optional)

```bash
pip install -e '.[openai]'
export OPENAI_API_KEY="your_key"
export OPENAI_MODEL="gpt-4.1-mini"
pup-agent run "List files in this folder" --provider openai
```

---

## Commands

```bash
pup-agent run "<task>" [--provider mock|openai] [--max-steps 6] [--verbose]
pup-agent chat [--provider mock|openai]
pup-agent tools
```

---

## Safety

Built-in tools are workspace-scoped:
- `list_files`
- `read_file`
- `current_time`

`read_file` is capped to prevent huge outputs.

---

## Tests

```bash
pytest
```

## Lint

```bash
ruff check src tests
```

## Community & Governance

- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)

---

## License

MIT
