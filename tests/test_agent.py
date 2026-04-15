from __future__ import annotations

from pathlib import Path

from pup_agent.agent import PupAgent
from pup_agent.providers.mock_provider import MockProvider


def test_time_query_uses_time_tool() -> None:
    agent = PupAgent(provider=MockProvider(), max_steps=4)
    result = agent.run("What time is it?")

    assert result.success
    assert result.steps
    assert result.steps[0].tool_name == "current_time"
    assert "Current local time" in result.final_response


def test_list_files_query_uses_list_tool(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("world", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    agent = PupAgent(provider=MockProvider(), max_steps=4)
    result = agent.run("list files")

    assert result.success
    assert result.steps
    assert result.steps[0].tool_name == "list_files"
    assert "a.txt" in result.final_response


def test_read_file_query_works(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "README.md").write_text("# Demo", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    agent = PupAgent(provider=MockProvider(), max_steps=4)
    result = agent.run("read README.md")

    assert result.success
    assert result.steps
    assert result.steps[0].tool_name == "read_file"
    assert "# Demo" in result.final_response
