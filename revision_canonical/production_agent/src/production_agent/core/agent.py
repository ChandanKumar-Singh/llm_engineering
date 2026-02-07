import json
from typing import Optional
from rich.console import Console
from .llm import LLMService
from .state import AgentState
from ..tools import ToolRegistry, default_registry
from ..config import config

console = Console()

class Agent:
    def __init__(self, tools: ToolRegistry = default_registry, system_prompt: str = "You are a helpful AI assistant."):
        self.llm = LLMService()
        self.tools = tools
        self.system_prompt = system_prompt
        self.state = AgentState()
        
        # Initialize state with system prompt
        self.state.add_message("system", self.system_prompt)

    def run(self, user_query: str) -> str:
        """Run the agent loop on a user query."""
        self.state.add_message("user", user_query)
        console.print(f"[bold green]User:[/bold green] {user_query}")

        for step in range(config.max_steps if config else 10):
            # 1. THINK
            openai_msgs = self.state.get_openai_messages()
            tool_schemas = [t.to_openai_schema() for t in self.tools.get_tools()]
            
            response = self.llm.chat_completion(
                messages=openai_msgs,
                tools=tool_schemas if tool_schemas else None
            )
            
            content = response.content
            tool_calls = response.tool_calls

            # Store the assistant's response
            tool_dicts = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in tool_calls
            ] if tool_calls else None

            self.state.add_message("assistant", content=content, tool_calls=tool_dicts)

            if content:
                console.print(f"[bold blue]Assistant:[/bold blue] {content}")

            # 2. ACT & OBSERVE
            if tool_calls:
                for tc in tool_calls:
                    func_name = tc.function.name
                    func_args = json.loads(tc.function.arguments)
                    console.print(f"[yellow]Tool Call:[/yellow] {func_name}({func_args})")

                    tool = self.tools.get(func_name)
                    if tool:
                        try:
                            # Validate args with Pydantic model (flexible)
                            validated_args = tool.args_schema(**func_args)
                            result = tool.run(**validated_args.model_dump())
                        except Exception as e:
                            result = f"Error executing tool: {str(e)}"
                    else:
                        result = f"Error: Tool '{func_name}' not found."

                    console.print(f"[dim]Observation: {str(result)[:200]}...[/dim]")
                    
                    # 3. UPDATE STATE
                    self.state.add_message(
                        role="tool",
                        content=str(result),
                        tool_call_id=tc.id,
                        name=func_name
                    )
            else:
                # No tool calls usually means we are done or asking a clarification question
                return content or "No response generated."

        return "Max steps reached."
