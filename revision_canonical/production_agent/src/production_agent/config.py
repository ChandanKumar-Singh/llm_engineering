import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class AgentConfig(BaseModel):
    """Configuration settings for the agent."""
    openai_api_key: str
    model_name: str = "gpt-4o"
    max_steps: int = 10
    work_dir: Path = Path("./work_dir")

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Load configuration from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        
        return cls(
            openai_api_key=api_key,
            model_name=os.getenv("AGENT_MODEL", "gpt-4o-mini"),
            max_steps=int(os.getenv("AGENT_MAX_STEPS", "10")),
            work_dir=Path(os.getenv("AGENT_WORK_DIR", "./work_dir"))
        )

# Global config instance
try:
    config = AgentConfig.from_env()
except ValueError:
    # Allow import without env vars for testing/docs, but warn or set None
    # For now, we rely on the user having the env set up.
    config = None 
