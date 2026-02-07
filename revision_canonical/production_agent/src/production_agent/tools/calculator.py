from pydantic import BaseModel, Field
from .base import BaseTool

class CalculatorArgs(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate (e.g., '2 + 2')")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Useful for performing mathematical calculations."
    args_schema = CalculatorArgs

    def run(self, expression: str) -> str:
        try:
            # Dangerous in real prod without sanitization, but standard for demos
            # In a real app, use a safer math parser like `numexpr`
            return str(eval(expression, {"__builtins__": None}, {}))
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
