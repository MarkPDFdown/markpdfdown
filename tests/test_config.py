"""
Tests for markpdfdown.config module
"""

import pytest
from pydantic import ValidationError

from markpdfdown.config import Config


class TestConfig:
    """Tests for Config class"""

    def test_default_values(self):
        """Test default configuration values"""
        config = Config()
        assert config.model_name == "gpt-4o"
        assert config.temperature == 0.3
        assert config.max_tokens == 8192
        assert config.retry_times == 3

    def test_custom_values(self):
        """Test custom configuration values"""
        config = Config(
            model_name="claude-3-opus",
            temperature=0.7,
            max_tokens=4096,
            retry_times=5,
        )
        assert config.model_name == "claude-3-opus"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096
        assert config.retry_times == 5

    def test_temperature_validation_min(self):
        """Test temperature minimum validation"""
        with pytest.raises(ValidationError):
            Config(temperature=-0.1)

    def test_temperature_validation_max(self):
        """Test temperature maximum validation"""
        with pytest.raises(ValidationError):
            Config(temperature=2.5)

    def test_temperature_boundary_values(self):
        """Test temperature boundary values"""
        config_min = Config(temperature=0.0)
        assert config_min.temperature == 0.0

        config_max = Config(temperature=2.0)
        assert config_max.temperature == 2.0

    def test_max_tokens_validation(self):
        """Test max_tokens must be positive"""
        with pytest.raises(ValidationError):
            Config(max_tokens=0)

        with pytest.raises(ValidationError):
            Config(max_tokens=-100)

    def test_retry_times_validation(self):
        """Test retry_times must be positive"""
        with pytest.raises(ValidationError):
            Config(retry_times=0)

        with pytest.raises(ValidationError):
            Config(retry_times=-1)


class TestConfigFromEnv:
    """Tests for Config.from_env class method"""

    def test_from_env_defaults(self, monkeypatch):
        """Test from_env with no environment variables"""
        # Clear relevant env vars
        for key in ["MODEL_NAME", "TEMPERATURE", "MAX_TOKENS", "RETRY_TIMES"]:
            monkeypatch.delenv(key, raising=False)

        config = Config.from_env()
        assert config.model_name == "gpt-4o"
        assert config.temperature == 0.3
        assert config.max_tokens == 8192
        assert config.retry_times == 3

    def test_from_env_custom_values(self, monkeypatch):
        """Test from_env with custom environment variables"""
        monkeypatch.setenv("MODEL_NAME", "gpt-4-turbo")
        monkeypatch.setenv("TEMPERATURE", "0.5")
        monkeypatch.setenv("MAX_TOKENS", "16384")
        monkeypatch.setenv("RETRY_TIMES", "5")

        config = Config.from_env()
        assert config.model_name == "gpt-4-turbo"
        assert config.temperature == 0.5
        assert config.max_tokens == 16384
        assert config.retry_times == 5

    def test_from_env_partial_override(self, monkeypatch):
        """Test from_env with partial environment variables"""
        for key in ["MODEL_NAME", "TEMPERATURE", "MAX_TOKENS", "RETRY_TIMES"]:
            monkeypatch.delenv(key, raising=False)

        monkeypatch.setenv("MODEL_NAME", "custom-model")

        config = Config.from_env()
        assert config.model_name == "custom-model"
        assert config.temperature == 0.3  # default
        assert config.max_tokens == 8192  # default
        assert config.retry_times == 3  # default

    def test_from_env_openrouter_model(self, monkeypatch):
        """Test from_env with OpenRouter model name"""
        for key in ["MODEL_NAME", "TEMPERATURE", "MAX_TOKENS", "RETRY_TIMES"]:
            monkeypatch.delenv(key, raising=False)

        monkeypatch.setenv("MODEL_NAME", "openrouter/anthropic/claude-3.5-sonnet")

        config = Config.from_env()
        assert config.model_name == "openrouter/anthropic/claude-3.5-sonnet"
