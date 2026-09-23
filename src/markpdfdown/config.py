"""
Configuration management for MarkPDFDown
"""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class Config(BaseModel):
    """Configuration settings for MarkPDFDown"""

    # Model configuration
    model_name: str = Field(
        default="gpt-4o",
        description="LLM model name (e.g., gpt-4o, openrouter/anthropic/claude-3.5-sonnet, requesty/openai/gpt-4o)",
    )

    fallback_models: list[str] = Field(
        default_factory=list,
        description="Fallback LLM models to use when rate limits or errors occur",
    )

    # Checkpoint and resume configuration
    cache_dir: Optional[str] = Field(
        default=None,
        description="Directory for caching page conversions to enable resuming",
    )

    resume: bool = Field(
        default=True,
        description="Whether to reuse completed page conversions from cache",
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
        fallback_env = os.getenv("FALLBACK_MODELS", "")
        fallbacks = (
            [m.strip() for m in fallback_env.split(",") if m.strip()]
            if fallback_env
            else []
        )
        cache_env = os.getenv("CACHE_DIR")
        resume_env = os.getenv("RESUME", "true").lower() in ("true", "1", "yes")

        return cls(
            model_name=os.getenv("MODEL_NAME", "gpt-4o"),
            fallback_models=fallbacks,
            cache_dir=cache_env if cache_env else None,
            resume=resume_env,
            temperature=float(os.getenv("TEMPERATURE", "0.3")),
            max_tokens=int(os.getenv("MAX_TOKENS", "8192")),
            retry_times=int(os.getenv("RETRY_TIMES", "3")),
        )


config = Config.from_env()
