"""
Configuration management for CodeScribe.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    def __init__(self) -> None:
        """Initialize configuration with current environment variables."""
        # Project settings
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "codescribe")
        self.DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Google AI settings
        self.GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    def validate(self) -> None:
        """Validate required configuration."""
        if not self.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )


# Global config instance
config = Config()
