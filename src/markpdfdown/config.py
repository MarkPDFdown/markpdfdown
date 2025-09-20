"""
Configuration management for MarkPDFDown
"""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class Config(BaseModel):
    """Configuration settings for MarkPDFDown"""

    # Model configuration
    model_name: str = Field(
        default="gpt-4o",
        description="LLM model name (e.g., gpt-4o, openrouter/anthropic/claude-3.5-sonnet)",
    )

    # Generation parameters
    temperature: float = Field(
        default=0.3, ge=0.0, le=2.0, description="Temperature for text generation"
    )

    max_tokens: int = Field(
        default=8192, gt=0, description="Maximum number of tokens for generated text"
    )

    retry_times: int = Field(
        default=3, gt=0, description="Number of retries for API calls"
    )

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables"""
        return cls(
            model_name=os.getenv("MODEL_NAME", "gpt-4o"),
            temperature=float(os.getenv("TEMPERATURE", "0.3")),
            max_tokens=int(os.getenv("MAX_TOKENS", "8192")),
            retry_times=int(os.getenv("RETRY_TIMES", "3")),
        )


# Global configuration instance
config = Config.from_env()
