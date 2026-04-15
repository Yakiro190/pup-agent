from __future__ import annotations

import re
from pathlib import Path

from pup_agent.models import AgentDecision, ToolCallRecord, ToolSpec
from pup_agent.providers.base import BaseProvider


class MockProvider(BaseProvider):
    """Deterministic provider for local development and tests."""

    name = "mock"

    def decide(
        self,
        *,
        task: str,
        history: list[ToolCallRecord],
        tools: list[ToolSpec],
    ) -> AgentDecision:
        lower = task.lower()

        if history:
            last = history[-1]
            if last.tool_name == "current_time":
                return AgentDecision(
                    action="respond",
                    response=f"Current local time: {last.tool_output}",
                )
            if last.tool_name == "list_files":
                return AgentDecision(
                    action="respond",
                    response=f"Here is what I found:\n{last.tool_output}",
                )
            if last.tool_name == "read_file":
                return AgentDecision(
                    action="respond",
                    response=f"I read the file. Preview:\n\n{last.tool_output}",
                )

        if any(k in lower for k in ["time", "date", "clock"]):
            return AgentDecision(action="tool", tool_name="current_time", tool_input="")

        if any(k in lower for k in ["list", "files", "folder", "directory"]):
            return AgentDecision(action="tool", tool_name="list_files", tool_input=".")

        read_match = re.search(r"read\s+([\w\-./]+)", lower)
        if read_match:
            file_candidate = read_match.group(1)
            # Keep original case if likely present in cwd
            for entry in Path.cwd().iterdir():
                if entry.name.lower() == file_candidate.lower():
                    file_candidate = entry.name
                    break
            return AgentDecision(action="tool", tool_name="read_file", tool_input=file_candidate)

        return AgentDecision(
            action="respond",
            response=(
                "I'm Pup Agent (mock mode). I can use tools: current_time, list_files, read_file. "
                "Try: 'What time is it?' or 'Read README.md'."
            ),
        )
