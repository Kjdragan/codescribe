#!/bin/bash

# Supabase Docker Stack Management Script
# This script helps manage the Supabase Docker stack for the DB Agent project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        print_warning "Please copy .env.example to .env and configure your secrets:"
        echo "  cp .env.example .env"
        echo ""
        print_warning "Required environment variables:"
        echo "  - POSTGRES_PASSWORD: Secure password for PostgreSQL"
        echo "  - JWT_SECRET: JWT signing secret (use: openssl rand -hex 64)"
        echo "  - ANON_KEY: Public API key"
        echo "  - SERVICE_ROLE_KEY: Service role API key"
        echo "  - OPENAI_API_KEY: Your OpenAI API key"
        exit 1
    fi
}

# Function to generate secure secrets
generate_secrets() {
    print_status "Generating secure secrets for Supabase..."
    
    if ! command -v openssl &> /dev/null; then
        print_error "OpenSSL is required to generate secure secrets"
        exit 1
    fi
    
    POSTGRES_PASSWORD=$(openssl rand -hex 16)
    JWT_SECRET=$(openssl rand -hex 64)
    
    print_success "Generated secrets:"
    echo "  POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
    echo "  JWT_SECRET: $JWT_SECRET"
    echo ""
    print_warning "Please add these to your .env file along with your OpenAI API key"
}

# Function to start the stack
start_stack() {
    print_status "Starting Supabase Docker stack..."
    check_env_file
    
    # Create necessary directories
    mkdir -p volumes/db
    
    # Start the services
    docker-compose up -d
    
    print_success "Supabase stack started successfully!"
    echo ""
    print_status "Services available at:"
    echo "  🎛️  Supabase Studio: http://localhost:3000"
    echo "  🔌 API Gateway: http://localhost:8000"
    echo "  🗄️  PostgreSQL: localhost:5432"
    echo ""
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check if services are healthy
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Supabase Studio is ready!"
    else
        print_warning "Supabase Studio may still be starting up..."
    fi
}

# Function to stop the stack
stop_stack() {
    print_status "Stopping Supabase Docker stack..."
    docker-compose down
    print_success "Supabase stack stopped successfully!"
}

# Function to restart the stack
restart_stack() {
    print_status "Restarting Supabase Docker stack..."
    docker-compose down
    docker-compose up -d
    print_success "Supabase stack restarted successfully!"
}

# Function to show logs
show_logs() {
    if [ -n "$2" ]; then
        print_status "Showing logs for service: $2"
        docker-compose logs -f "$2"
    else
        print_status "Showing logs for all services..."
        docker-compose logs -f
    fi
}

# Function to show status
show_status() {
    print_status "Supabase Docker stack status:"
    docker-compose ps
}

# Function to clean up (remove containers and volumes)
cleanup() {
    print_warning "This will remove all containers and data volumes!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Supabase Docker stack..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to setup database schema
setup_database() {
    print_status "Setting up database schema for DB Agent..."
    
    # Wait for database to be ready
    sleep 5
    
    # Create customers table
    docker-compose exec db psql -U postgres -d postgres -c "
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            bio TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create anon role if it doesn't exist
        DO \$\$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
                CREATE ROLE anon;
            END IF;
        END
        \$\$;
        
        -- Grant permissions
        GRANT USAGE ON SCHEMA public TO anon;
        GRANT SELECT, INSERT, UPDATE, DELETE ON customers TO anon;
        GRANT USAGE ON SEQUENCE customers_id_seq TO anon;
    "
    
    print_success "Database schema setup completed!"
}

# Function to show help
show_help() {
    echo "Supabase Docker Stack Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the Supabase Docker stack"
    echo "  stop        Stop the Supabase Docker stack"
    echo "  restart     Restart the Supabase Docker stack"
    echo "  status      Show status of all services"
    echo "  logs [svc]  Show logs (optionally for specific service)"
    echo "  setup-db    Setup database schema for DB Agent"
    echo "  generate    Generate secure secrets for .env file"
    echo "  cleanup     Remove all containers and volumes (destructive!)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                 # Start all services"
    echo "  $0 logs db              # Show database logs"
    echo "  $0 setup-db             # Setup customers table"
}

# Main script logic
case "${1:-help}" in
    start)
        start_stack
        ;;
    stop)
        stop_stack
        ;;
    restart)
        restart_stack
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$@"
        ;;
    setup-db)
        setup_database
        ;;
    generate)
        generate_secrets
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
