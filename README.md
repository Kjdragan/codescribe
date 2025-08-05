# CodeScribe

A Python project for code documentation and analysis.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

### Development

Install development dependencies:
```bash
uv sync --dev
```

### Running the Project

```bash
uv run python main.py
```

## Project Structure

- `src/` - Main source code
- `tests/` - Test files
- `docs/` - Project documentation
- `ai_context/` - AI-related context and configurations
- `.env` - Environment variables (create from `.env.example`)

## Dependencies

- `python-dotenv` - Environment variable management
- `google-genai` - Google Generative AI integration

## Development Tools

- `pytest` - Testing framework
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking
