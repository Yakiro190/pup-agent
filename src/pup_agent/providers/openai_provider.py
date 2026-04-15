from __future__ import annotations

import json
import os
import re

from pup_agent.models import AgentDecision, ToolCallRecord, ToolSpec
from pup_agent.providers.base import BaseProvider

SYSTEM_PROMPT = """You are Pup Agent, a compact assistant with tool-use.
You must decide either:
1) use a tool, or
2) respond to user directly.

Return STRICT JSON only.
Schema:
{
  "action": "tool" | "respond",
  "tool_name": "string",
  "tool_input": "string",
  "response": "string"
}

Rules:
- If you need external facts from local workspace, use a tool.
- If enough info is available, respond directly.
- Never include markdown fences.
"""


class OpenAIProvider(BaseProvider):
    name = "openai"

    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.model = model

    def decide(
        self,
        *,
        task: str,
        history: list[ToolCallRecord],
        tools: list[ToolSpec],
    ) -> AgentDecision:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return AgentDecision(
                action="respond",
                response="OPENAI_API_KEY is missing. Set it or use --provider mock.",
            )

        try:
            from openai import OpenAI
        except Exception:
            return AgentDecision(
                action="respond",
                response="OpenAI SDK not installed. Run: pip install -e .[openai]",
            )

        tool_lines = "\n".join(f"- {t.name}: {t.description}" for t in tools)
        history_lines = "\n".join(
            "Step "
            f"{h.step} | tool={h.tool_name} | input={h.tool_input!r} "
            f"| output={h.tool_output!r}"
            for h in history
        ) or "(empty)"

        user_prompt = (
            f"Task:\n{task}\n\n"
            f"Available tools:\n{tool_lines}\n\n"
            f"History:\n{history_lines}\n"
        )

        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )

        raw = (response.output_text or "").strip()
        data = self._parse_json(raw)
        if not data:
            return AgentDecision(
                action="respond",
                response=f"Model returned unparsable output: {raw[:400]}",
            )

        action = data.get("action", "respond")
        if action not in {"tool", "respond"}:
            action = "respond"

        return AgentDecision(
            action=action,
            tool_name=str(data.get("tool_name", "")),
            tool_input=str(data.get("tool_input", "")),
            response=str(data.get("response", "")),
        )

    @staticmethod
    def _parse_json(raw: str) -> dict | None:
        if not raw:
            return None

        try:
            return json.loads(raw)
        except Exception:
            pass

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return None

        try:
            return json.loads(match.group(0))
        except Exception:
            return None
