"""
CodeScribe - Main Entry Point

A Python project for code documentation and analysis.
"""

import os
from dotenv import load_dotenv


def main() -> None:
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    project_name = os.getenv("PROJECT_NAME", "codescribe")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 Starting {project_name}")
    print(f"📊 Debug mode: {debug}")
    
    # Add your main application logic here
    print("✅ Project setup complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your environment variables")
    print("2. Add your Google API key to the .env file")
    print("3. Start building your application in the src/ directory")


if __name__ == "__main__":
    main()
