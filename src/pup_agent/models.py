from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ActionType = Literal["tool", "respond"]


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str


@dataclass(slots=True)
class ToolCallRecord:
    step: int
    tool_name: str
    tool_input: str
    tool_output: str


@dataclass(slots=True)
class AgentDecision:
    action: ActionType
    response: str = ""
    tool_name: str = ""
    tool_input: str = ""


@dataclass(slots=True)
class AgentResult:
    success: bool
    final_response: str
    steps: list[ToolCallRecord] = field(default_factory=list)
