from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pup_agent.agent import PupAgent
from pup_agent.config import DEFAULT_MAX_STEPS, DEFAULT_PROVIDER
from pup_agent.providers import create_provider
from pup_agent.tools import ToolRegistry

app = typer.Typer(add_completion=False, help="Pup Agent CLI")
console = Console()


def _build_agent(provider_name: str, model: str | None, max_steps: int) -> PupAgent:
    provider = create_provider(provider_name, model=model)
    return PupAgent(provider=provider, max_steps=max_steps)


@app.command()
def run(
    task: str = typer.Argument(..., help="Task for the agent"),
    provider: str = typer.Option(DEFAULT_PROVIDER, "--provider", "-p", help="mock | openai"),
    model: str | None = typer.Option(None, "--model", help="Override model (OpenAI provider)"),
    max_steps: int = typer.Option(DEFAULT_MAX_STEPS, "--max-steps", min=1, max=20),
    verbose: bool = typer.Option(False, "--verbose", help="Show tool steps"),
) -> None:
    """Run one agent task and exit."""
    agent = _build_agent(provider, model, max_steps)
    result = agent.run(task)

    if verbose and result.steps:
        table = Table(title="Tool Calls")
        table.add_column("Step")
        table.add_column("Tool")
        table.add_column("Input")
        table.add_column("Output")
        for s in result.steps:
            table.add_row(str(s.step), s.tool_name, s.tool_input or "-", s.tool_output[:1200])
        console.print(table)

    style = "green" if result.success else "red"
    console.print(Panel(result.final_response, title="Pup Agent", border_style=style))
    raise typer.Exit(code=0 if result.success else 1)


@app.command()
def chat(
    provider: str = typer.Option(DEFAULT_PROVIDER, "--provider", "-p", help="mock | openai"),
    model: str | None = typer.Option(None, "--model", help="Override model (OpenAI provider)"),
    max_steps: int = typer.Option(DEFAULT_MAX_STEPS, "--max-steps", min=1, max=20),
) -> None:
    """Start interactive chat mode."""
    agent = _build_agent(provider, model, max_steps)
    console.print("[bold green]Pup Agent chat[/bold green] — type [bold]:quit[/bold] to exit.")

    while True:
        try:
            text = typer.prompt("you").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye 👋")
            return

        if text in {":quit", ":q", "exit", "quit"}:
            console.print("Bye 👋")
            return

        if not text:
            continue

        result = agent.run(text)
        style = "green" if result.success else "red"
        console.print(Panel(result.final_response, title="pup", border_style=style))


@app.command(name="tools")
def list_tools() -> None:
    """List built-in tools."""
    registry = ToolRegistry()
    table = Table(title="Built-in Tools")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    for spec in registry.specs():
        table.add_row(spec.name, spec.description)
    console.print(table)


if __name__ == "__main__":
    app()
