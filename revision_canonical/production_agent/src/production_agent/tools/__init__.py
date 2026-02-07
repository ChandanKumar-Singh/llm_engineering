from typing import Dict, List
from .base import BaseTool
from .calculator import CalculatorTool
from .search import WebSearchTool

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool
        
    def get_tools(self) -> List[BaseTool]:
        return list(self.tools.values())
    
    def get(self, name: str) -> BaseTool:
        return self.tools.get(name)

# Default registry with standard tools
default_registry = ToolRegistry()
default_registry.register(CalculatorTool())
default_registry.register(WebSearchTool())
