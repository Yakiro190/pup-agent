# Pup Agent Architecture

Pup Agent is intentionally small and modular:

1. **CLI (`cli.py`)**
   - entrypoint for `run`, `chat`, and `tools`.

2. **Agent Core (`agent.py`)**
   - iterative decision loop (respond or use a tool)
   - max-step guard for predictable execution.

3. **Providers (`providers/`)**
   - `mock_provider.py`: deterministic, zero-dependency default
   - `openai_provider.py`: JSON decisioning via OpenAI Responses API.

4. **Tools (`tools.py`)**
   - workspace-safe file system tools
   - easy extension via `ToolRegistry`.

5. **Models (`models.py`)**
   - typed dataclasses for decisions, tool specs, and run results.
