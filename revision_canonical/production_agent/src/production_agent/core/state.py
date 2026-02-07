from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None  # For tool outputs

class AgentState(BaseModel):
    """Maintains the history and context of the agent's execution."""
    messages: List[Message] = Field(default_factory=list)
    scratchpad: List[str] = Field(default_factory=list)

    def add_message(self, role: str, content: str = None, tool_calls: list = None, tool_call_id: str = None, name: str = None):
        self.messages.append(Message(
            role=role, 
            content=content, 
            tool_calls=tool_calls,
            tool_call_id=tool_call_id,
            name=name
        ))

    def get_openai_messages(self) -> List[Dict[str, Any]]:
        """Convert state to OpenAI API format."""
        # Simple conversion - in prod, might verify handling of function calls more strictly
        return [msg.model_dump(exclude_none=True) for msg in self.messages]
