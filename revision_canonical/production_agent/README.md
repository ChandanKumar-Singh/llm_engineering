# Production Agent Framework

This module represents a "canonical" implementation of a production-ready AI agent, incorporating best practices from the LLM Engineering course.

## Features
- **Typed Interfaces**: All components use `Pydantic` for strict type validation.
- **Structured Logic**: Separates `Model`, `Tools`, and `Orchestration`.
- **Observability**: Uses `rich` for terminal output to visualize the "Thought -> Act -> Observe" loop.
- **Extensible**: Easy to add new tools by subclassing `BaseTool`.

## Structure
- `src/core/`: The brain. Contains the LLM wrapper and the React Loop.
- `src/tools/`: The hands. Contains tool definitions.
- `src/config.py`: Configuration and environment management.

## Usage

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run the agent:
   ```bash
   python -m production_agent.main "Find the latest paper on 'Chain of Thought' and summarize it."
   ```
