from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pup_agent.models import ToolSpec

MAX_READ_CHARS = 4000
MAX_LIST_ITEMS = 120


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[str, callable]] = {
            "current_time": ("Get current local date/time.", self._current_time),
            "list_files": ("List files inside a directory (workspace only).", self._list_files),
            "read_file": ("Read a text file (workspace only, capped output).", self._read_file),
        }

    def specs(self) -> list[ToolSpec]:
        return [ToolSpec(name=name, description=desc) for name, (desc, _) in self._tools.items()]

    def execute(self, name: str, tool_input: str) -> str:
        if name not in self._tools:
            return f"Unknown tool: {name}"
        _, fn = self._tools[name]
        try:
            return fn(tool_input)
        except Exception as exc:
            return f"Tool error ({name}): {exc}"

    @staticmethod
    def _resolve_workspace_path(raw: str) -> Path:
        candidate = (Path.cwd() / (raw or ".")).resolve()
        cwd = Path.cwd().resolve()
        if candidate != cwd and cwd not in candidate.parents:
            raise ValueError("path outside workspace is blocked")
        return candidate

    @staticmethod
    def _current_time(_: str) -> str:
        return datetime.now().astimezone().isoformat()

    @classmethod
    def _list_files(cls, tool_input: str) -> str:
        path = cls._resolve_workspace_path(tool_input or ".")
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        lines = []
        for entry in items[:MAX_LIST_ITEMS]:
            marker = "/" if entry.is_dir() else ""
            lines.append(f"{entry.name}{marker}")
        if len(items) > MAX_LIST_ITEMS:
            lines.append(f"... and {len(items) - MAX_LIST_ITEMS} more")
        return "\n".join(lines) if lines else "(empty directory)"

    @classmethod
    def _read_file(cls, tool_input: str) -> str:
        if not tool_input:
            raise ValueError("read_file requires a path")
        path = cls._resolve_workspace_path(tool_input)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Expected file, got directory: {path}")

        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) <= MAX_READ_CHARS:
            return text
        return text[:MAX_READ_CHARS] + "\n... [truncated]"
