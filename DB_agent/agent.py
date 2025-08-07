"""
Main DB Agent implementation using PydanticAI and PostgreSQL.

This agent can perform CRUD operations on a customers database using natural language commands.
"""
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from supabase import create_client, Client
from database import seed_database
from tools import create_customer, get_customer_by_email, update_customer_by_email, delete_customer_by_email

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load environment variables
load_dotenv()


def get_openai_model(model_name: str = "gpt-4o-mini") -> OpenAIModel:
    """
    Initialize and return an OpenAI model instance.
    
    Args:
        model_name: Name of the OpenAI model to use
        
    Returns:
        OpenAIModel: Configured OpenAI model instance
        
    Raises:
        ValueError: If OPENAI_API_KEY is not found in environment
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        raise ValueError(
            Fore.RED + "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    
    try:
        # Set the API key in environment for PydanticAI to pick up
        os.environ["OPENAI_API_KEY"] = openai_api_key
        model = OpenAIModel(model_name)
        return model
    except Exception as e:
        print(Fore.RED + f"Error initializing OpenAI model: {e}")
        raise


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be set in environment variables")
    
    return create_client(supabase_url, supabase_key)


# System prompt for the agent
SYSTEM_PROMPT = """
You are a customer service agent for a tech company. Use the tools provided to assist customers with their queries.

You have access to the following CRUD operations for managing customer records:
- create_customer: Create a new customer record with email, full_name, and bio
- get_customer_by_email: Retrieve a customer record by their email address
- update_customer_by_email: Update a customer's full_name and bio using their email
- delete_customer_by_email: Delete a customer record by their email address

Always be helpful and professional in your responses. When performing operations, provide clear feedback about what was accomplished.
"""

# Initialize the agent with OpenAI model
model = get_openai_model()
agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT
)

# Register the CRUD tools with the agent
agent.tool(retries=3)(create_customer)
agent.tool(retries=3)(get_customer_by_email)
agent.tool(retries=3)(update_customer_by_email)
agent.tool(retries=3)(delete_customer_by_email)


def main():
    """
    Main function to run the DB Agent CLI.
    """
    init()  # Initialize colorama
    
    print(f"{Fore.CYAN}🤖 DB Agent - Natural Language Database Interface{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'quit' or 'exit' to stop the agent.{Style.RESET_ALL}\n")
    
    # Initialize Supabase client
    try:
        supabase_client = get_supabase_client()
        print(f"{Fore.GREEN}✅ Connected to Supabase successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to connect to Supabase: {e}{Style.RESET_ALL}")
        return
    
    # Seed the database with initial data
    try:
        seed_database()
        print(f"{Fore.GREEN}✅ Database seeded successfully!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️ Database seeding failed (might already be seeded): {e}{Style.RESET_ALL}\n")

    # Main interaction loop
    while True:
        try:
            user_input = input(Fore.WHITE + ">> Enter a query: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print(Fore.GREEN + "Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            print(Fore.BLUE + "Processing your request...")
            try:
                # Run the agent with the user's query
                result = agent.run_sync(user_input, deps=supabase_client)
                print(f"{Fore.GREEN}🤖 Agent: {result.data}{Style.RESET_ALL}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}\n")
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\nInterrupted by user. Goodbye! 👋")
                break
            except Exception as e:
                print(Fore.RED + f"❌ An unexpected error occurred: {e}")
            print()  # Add spacing between interactions
        except Exception as e:
            print(Fore.RED + f"❌ An unexpected error occurred: {e}")
        print()  # Add spacing between interactions


if __name__ == "__main__":
    main()
