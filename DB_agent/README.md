# DB Agent - CRUD Database Agent with PydanticAI

A natural language interface for database operations using PydanticAI, Supabase, and OpenAI GPT models.

## Overview

This project implements a conversational AI agent that can perform CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database using natural language commands. The agent leverages PydanticAI for the agent framework, Supabase for database operations, and OpenAI's GPT models for natural language understanding.

**Status**: **Fully Functional** - Middle ground implementation successfully deployed (as of 2025-08-06)

## Features

- **Natural Language Interface**: Interact with your database using plain English
- **CRUD Operations**: Create, retrieve, update, and delete customer records
- **AI-Powered**: Uses OpenAI GPT-4o-mini for intelligent query processing
- **Docker Integration**: Simplified Supabase stack running locally without complex auth
- **Type Safety**: Built with Pydantic for robust data validation
- **Colorful CLI**: User-friendly command-line interface with colored output
- **Middle Ground Architecture**: Keeps Supabase client benefits without authentication complexity

## Architecture

### Current Implementation (Middle Ground)

**What We Keep:**
- Supabase client SDK for clean database operations
- PostgREST API (running on port 3001)
- All CRUD tools using `ctx.deps` (Supabase client)
- Docker orchestration with management scripts
- Optional Supabase Studio for database management

**What We Removed:**
- GoTrue auth service (eliminated authentication complexity)
- Complex JWT validation and user management
- Auth-related database schemas and migrations
- User authentication requirements

## Prerequisites

- Python 3.13+
- UV package manager
- Docker and Docker Compose
- OpenAI API key

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd DB_agent

# Install dependencies using UV
uv sync
```

### 2. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env
   - PostgreSQL: localhost:5432

📖 **See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker instructions**

### Option 2: Supabase CLI (Alternative)

1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

2. **Install Supabase CLI**:
   ```bash
   npm install supabase --save-dev
   ```

3. **Initialize and Start**:
   ```bash
   npx supabase init
   npx supabase start
   ```

4. **Configure Environment**:
   Copy the API URL and anon key from terminal output to your `.env` file

5. **Database Schema Setup**:
   - Open Supabase Studio (usually at http://127.0.0.1:54323)
   - Go to Table# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here

**Key Environment Variables:**
```bash
OPENAI_API_KEY=your_key_here
SUPABASE_URL=http://localhost:3001  # PostgREST API
SUPABASE_KEY=not_needed_for_development
POSTGRES_PASSWORD=auto_generated_secure_password
```

### 3. Start the Docker Stack

```bash
# Make the script executable
chmod +x docker-stack.sh

# Start the Supabase stack
./docker-stack.sh start

# Setup the database schema
./docker-stack.sh setup-db
```

### 4. Run the Agent

```bash
# Start the interactive agent
uv run python agent.py
```

## Usage Examples

Once the agent is running, you can use natural language commands:

```
>> Create a customer with email john@example.com, name John Smith, and bio Software Engineer
>> Get the customer with email john@example.com
>> Update customer john@example.com with name John Doe and bio Senior Engineer
>> Delete customer with email john@example.com
```

## Project Structure

```
DB_agent/
├── agent.py                 # Main agent implementation
├── models.py               # Pydantic data models
├── database.py             # Database connection and utilities
├── tools/                  # CRUD operation tools
├── models.py             # Pydantic data models
├── database.py           # Database connection and utilities
├── tools/                # CRUD operation tools
│   ├── __init__.py
│   ├── create.py
│   ├── retrieve.py
│   ├── update.py
│   └── delete.py
├── docker-compose.yml    # Supabase Docker stack configuration
├── docker-stack.sh       # Docker management script
├── kong/                 # Kong API gateway configuration
│   └── kong.yml
├── volumes/              # Docker volume mounts
│   └── db/               # PostgreSQL data persistence
├── .env.example          # Environment template
├── .env                  # Your environment variables (not in git)
├── DOCKER_SETUP.md       # Detailed Docker setup guide
├── test_agent.py         # Automated testing script
├── setup.py              # Environment setup automation
├── pyproject.toml        # UV project configuration
└── README.md             # This file
```

## Development

This project uses UV for dependency management. Key commands:

- `uv sync` - Install/update dependencies
- `uv run python agent.py` - Run the agent
- `uv add <package>` - Add new dependency
- `uv remove <package>` - Remove dependency

## Next Steps

From this foundation, you can:

- Add more complex database operations
- Integrate with FastAPI to create a REST API
- Build a web interface with Streamlit
- Add authentication and authorization
- Implement more sophisticated data models
- Add logging and monitoring

## Troubleshooting

- **OpenAI API errors**: Verify your API key in `.env`
- **Database connection issues**: Ensure Supabase is running with `npx supabase start`
- **Import errors**: Run `uv sync` to ensure all dependencies are installed
- **Permission errors**: Check that RLS is disabled on the customers table for development