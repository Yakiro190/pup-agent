from __future__ import annotations

from abc import ABC, abstractmethod

from pup_agent.models import AgentDecision, ToolCallRecord, ToolSpec


class BaseProvider(ABC):
    name: str

    @abstractmethod
    def decide(
        self,
        *,
        task: str,
        history: list[ToolCallRecord],
        tools: list[ToolSpec],
    ) -> AgentDecision:
        """Return the next agent decision."""
