from __future__ import annotations

from pup_agent.models import AgentResult, ToolCallRecord
from pup_agent.providers.base import BaseProvider
from pup_agent.tools import ToolRegistry


class PupAgent:
    def __init__(self, provider: BaseProvider, max_steps: int = 6) -> None:
        self.provider = provider
        self.max_steps = max_steps
        self.tools = ToolRegistry()

    def run(self, task: str, *, max_steps: int | None = None) -> AgentResult:
        history: list[ToolCallRecord] = []
        limit = max_steps or self.max_steps

        for step in range(1, limit + 1):
            decision = self.provider.decide(task=task, history=history, tools=self.tools.specs())

            if decision.action == "respond":
                final = decision.response.strip() or "Done."
                return AgentResult(success=True, final_response=final, steps=history)

            if decision.action == "tool":
                tool_output = self.tools.execute(decision.tool_name, decision.tool_input)
                history.append(
                    ToolCallRecord(
                        step=step,
                        tool_name=decision.tool_name,
                        tool_input=decision.tool_input,
                        tool_output=tool_output,
                    )
                )
                continue

            return AgentResult(
                success=False,
                final_response=f"Unsupported action from provider: {decision.action}",
                steps=history,
            )

        return AgentResult(
            success=False,
            final_response=f"Stopped after {limit} steps without final response.",
            steps=history,
        )
