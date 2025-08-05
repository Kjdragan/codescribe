"""
Tests for configuration module.
"""

import os
import pytest
from unittest.mock import patch

from src.codescribe.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = Config()
        assert config.PROJECT_NAME == "codescribe"
        assert config.DEBUG is False
        assert config.LOG_LEVEL == "INFO"
    
    @patch.dict(os.environ, {"DEBUG": "true", "LOG_LEVEL": "DEBUG"})
    def test_environment_override(self) -> None:
        """Test environment variable overrides."""
        config = Config()
        assert config.DEBUG is True
        assert config.LOG_LEVEL == "DEBUG"
    
    def test_validate_missing_api_key(self) -> None:
        """Test validation with missing API key."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": ""}, clear=True):
            config = Config()
            with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable is required"):
                config.validate()
    
    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_validate_with_api_key(self) -> None:
        """Test validation with API key present."""
        config = Config()
        # Should not raise an exception
        config.validate()
