# Supabase Docker Stack Setup Guide

This guide will help you set up a complete Supabase environment using Docker for the DB Agent project.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: The containerization platform
- **Docker Compose**: Tool for defining multi-container applications
- **OpenSSL**: For generating secure secrets (usually pre-installed on Linux/macOS)

## Quick Start

1. **Generate Environment Configuration**:
   ```bash
   ./docker-stack.sh generate
   ```

2. **Copy and Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add the generated secrets plus your OpenAI API key
   ```

3. **Start the Supabase Stack**:
   ```bash
   ./docker-stack.sh start
   ```

4. **Setup Database Schema**:
   ```bash
   ./docker-stack.sh setup-db
   ```

5. **Access Supabase Studio**:
   Open http://localhost:3000 in your browser

## Detailed Setup Instructions

### Step 1: Environment Configuration

The Supabase Docker stack requires several environment variables for security and configuration:

```bash
# Generate secure secrets
./docker-stack.sh generate
```

This will generate:
- `POSTGRES_PASSWORD`: Secure password for PostgreSQL database
- `JWT_SECRET`: Secret for signing JSON Web Tokens

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

Edit `.env` and configure:
- `OPENAI_API_KEY`: Your OpenAI API key
- `POSTGRES_PASSWORD`: Generated secure password
- `JWT_SECRET`: Generated JWT secret
- Other values can use the defaults provided

### Step 2: Start the Stack

Start all Supabase services:

```bash
./docker-stack.sh start
```

This will start the following services:
- **PostgreSQL Database** (port 5432)
- **Kong API Gateway** (port 8000)
- **Supabase Studio** (port 3000)
- **GoTrue Authentication** (internal)
- **PostgREST API** (internal)
- **Realtime Server** (internal)
- **Storage API** (internal)
- **pg-meta** (internal)

### Step 3: Setup Database Schema

Create the required database schema for the DB Agent:

```bash
./docker-stack.sh setup-db
```

This creates the `customers` table with proper permissions.

### Step 4: Access Services

Once started, you can access:

- **Supabase Studio**: http://localhost:3000
  - Username: Not required for local development
  - This is your database management interface

- **API Endpoint**: http://localhost:8000
  - This is the main API gateway for your applications

- **PostgreSQL**: localhost:5432
  - Username: `postgres`
  - Password: Your configured `POSTGRES_PASSWORD`

## Management Commands

The `docker-stack.sh` script provides several management commands:

```bash
# Start the stack
./docker-stack.sh start

# Stop the stack
./docker-stack.sh stop

# Restart the stack
./docker-stack.sh restart

# Show service status
./docker-stack.sh status

# View logs (all services)
./docker-stack.sh logs

# View logs for specific service
./docker-stack.sh logs db

# Setup database schema
./docker-stack.sh setup-db

# Generate secure secrets
./docker-stack.sh generate

# Clean up everything (destructive!)
./docker-stack.sh cleanup
```

## Using with DB Agent

Once the Docker stack is running, you can use the DB Agent:

1. **Ensure your `.env` file has**:
   ```bash
   SUPABASE_URL=http://localhost:8000
   SUPABASE_KEY=<your_anon_key_from_env>
   OPENAI_API_KEY=<your_openai_key>
   ```

2. **Run the DB Agent**:
   ```bash
   uv run python agent.py
   ```

3. **Test with natural language**:
   - "Create a customer with email john@example.com"
   - "Get the customer with email john@example.com"
   - "Update customer john@example.com with new bio"

## Troubleshooting

### Services Not Starting
- Check if ports 3000, 5432, 8000 are available
- Ensure Docker daemon is running
- Check logs: `./docker-stack.sh logs`

### Database Connection Issues
- Verify PostgreSQL is running: `./docker-stack.sh status`
- Check database logs: `./docker-stack.sh logs db`
- Ensure `.env` has correct `POSTGRES_PASSWORD`

### API Connection Issues
- Verify Kong gateway is running on port 8000
- Check Kong logs: `./docker-stack.sh logs kong`
- Ensure `SUPABASE_URL=http://localhost:8000` in `.env`

### Studio Access Issues
- Verify Studio is running on port 3000
- Check Studio logs: `./docker-stack.sh logs studio`
- Try refreshing the browser or clearing cache

## Data Persistence

Database data is persisted in the `volumes/db` directory. To completely reset:

```bash
./docker-stack.sh cleanup
```

**Warning**: This will delete all your data!

## Security Notes

For production use:
- Change all default passwords and secrets
- Use proper SSL certificates
- Configure proper firewall rules
- Enable Row Level Security (RLS) in Supabase
- Use environment-specific configuration

## Architecture

The Docker stack includes:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Supabase      │    │     Kong     │    │     DB      │
│   Studio        │◄───┤  API Gateway │◄───┤ Agent App   │
│  (Dashboard)    │    │              │    │             │
└─────────────────┘    └──────────────┘    └─────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼──┐ ┌────▼────┐ ┌──▼──────┐
            │   Auth   │ │  REST   │ │Storage  │
            │(GoTrue)  │ │(PostgREST)│ │   API   │
            └──────────┘ └─────────┘ └─────────┘
                              │
                    ┌─────────▼─────────┐
                    │    PostgreSQL     │
                    │    Database       │
                    └───────────────────┘
```

All services communicate through Docker's internal network, with Kong acting as the API gateway for external access.
