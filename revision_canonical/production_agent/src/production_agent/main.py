import typer
from rich.console import Console
from production_agent.core.agent import Agent

app = typer.Typer()
console = Console()

@app.command()
def run(query: str):
    """
    Run the AI agent with a query.
    """
    console.print(f"[bold]Starting Agent with query:[/bold] {query}")
    agent = Agent()
    result = agent.run(query)
    console.print(f"\n[bold green]Final Result:[/bold green]\n{result}")

if __name__ == "__main__":
    app()
