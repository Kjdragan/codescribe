"""
Setup script for the DB Agent project.

This script helps users set up the project environment and dependencies.
"""
import os
import subprocess
import sys
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)


def run_command(command, description, check_success=True):
    """Run a shell command and handle errors."""
    print(f"{Fore.BLUE}📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check_success and result.returncode != 0:
            print(f"{Fore.RED}❌ Failed: {result.stderr}")
            return False
        else:
            print(f"{Fore.GREEN}✅ Success!")
            if result.stdout.strip():
                print(f"{Fore.YELLOW}{result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        return False


def check_prerequisites():
    """Check if required tools are installed."""
    print(f"{Fore.CYAN}🔍 Checking prerequisites...")
    
    prerequisites = [
        ("python3", "Python 3.13+"),
        ("uv", "UV package manager"),
        ("docker", "Docker"),
        ("node", "Node.js"),
        ("npm", "npm")
    ]
    
    missing = []
    for cmd, name in prerequisites:
        if not run_command(f"which {cmd}", f"Checking {name}", check_success=False):
            missing.append(name)
    
    if missing:
        print(f"{Fore.RED}❌ Missing prerequisites: {', '.join(missing)}")
        print(f"{Fore.YELLOW}Please install the missing tools and run this script again.")
        return False
    
    print(f"{Fore.GREEN}✅ All prerequisites are installed!")
    return True


def setup_environment():
    """Set up the project environment."""
    print(f"\n{Fore.CYAN}🛠️  Setting up project environment...")
    
    # Install dependencies
    if not run_command("uv sync", "Installing Python dependencies"):
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print(f"{Fore.YELLOW}⚠️  .env file not found. Please:")
        print(f"{Fore.YELLOW}   1. Copy .env.example to .env")
        print(f"{Fore.YELLOW}   2. Add your OpenAI API key")
        print(f"{Fore.YELLOW}   3. Add your Supabase URL and key after running 'npx supabase start'")
        return False
    
    return True


def setup_supabase():
    """Set up Supabase local instance."""
    print(f"\n{Fore.CYAN}🗄️  Setting up Supabase...")
    
    # Install Supabase CLI locally
    if not run_command("npm install supabase --save-dev", "Installing Supabase CLI"):
        return False
    
    # Initialize Supabase project if not already done
    if not os.path.exists("supabase"):
        if not run_command("npx supabase init", "Initializing Supabase project"):
            return False
    
    print(f"{Fore.YELLOW}📝 Next steps for Supabase:")
    print(f"{Fore.YELLOW}   1. Run: npx supabase start")
    print(f"{Fore.YELLOW}   2. Copy the API URL and anon key to your .env file")
    print(f"{Fore.YELLOW}   3. Open Supabase Studio and create the 'customers' table")
    print(f"{Fore.YELLOW}   4. Add columns: full_name (text), email (text, unique), bio (text)")
    print(f"{Fore.YELLOW}   5. Disable Row Level Security for development")
    
    return True


def main():
    """Main setup function."""
    print(f"{Fore.CYAN}🚀 DB Agent Setup Script")
    print(f"{Fore.CYAN}=" * 40)
    
    if not check_prerequisites():
        sys.exit(1)
    
    if not setup_environment():
        sys.exit(1)
    
    if not setup_supabase():
        sys.exit(1)
    
    print(f"\n{Fore.GREEN}🎉 Setup completed successfully!")
    print(f"{Fore.GREEN}Next steps:")
    print(f"{Fore.YELLOW}   1. Complete the Supabase setup as described above")
    print(f"{Fore.YELLOW}   2. Run: uv run python agent.py")
    print(f"{Fore.YELLOW}   3. Or test with: uv run python test_agent.py")


if __name__ == "__main__":
    main()
