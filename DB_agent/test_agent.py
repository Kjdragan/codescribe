"""
Test script for the DB Agent to validate CRUD operations.

This script tests the agent's ability to handle various natural language commands
for database operations without requiring manual input.
"""
import asyncio
from colorama import Fore, init
from database import get_supabase_client, seed_database
from agent import agent

# Initialize colorama
init(autoreset=True)


def test_agent_operations():
    """
    Test the agent with various CRUD operations.
    """
    print(Fore.CYAN + "🧪 Testing DB Agent CRUD Operations")
    print(Fore.CYAN + "=" * 50)
    
    # Initialize Supabase client
    supabase_client = get_supabase_client()
    if not supabase_client:
        print(Fore.RED + "❌ Failed to initialize Supabase client")
        return False
    
    # Seed the database
    print(Fore.BLUE + "📊 Seeding database...")
    seed_database(supabase_client)
    
    # Test cases
    test_cases = [
        {
            "description": "Retrieve existing customer",
            "query": "Get the customer with email johndoe@gmail.com"
        },
        {
            "description": "Create new customer",
            "query": "Create a new customer with email test@example.com, name Test User, and bio 'Test customer for validation'"
        },
        {
            "description": "Retrieve newly created customer",
            "query": "Get the customer with email test@example.com"
        },
        {
            "description": "Update customer information",
            "query": "Update the customer test@example.com with name 'Updated Test User' and bio 'Updated bio for testing'"
        },
        {
            "description": "Retrieve updated customer",
            "query": "Get the customer with email test@example.com"
        },
        {
            "description": "Delete customer",
            "query": "Delete the customer with email test@example.com"
        },
        {
            "description": "Try to retrieve deleted customer (should fail)",
            "query": "Get the customer with email test@example.com"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{Fore.YELLOW}Test {i}: {test_case['description']}")
        print(f"{Fore.WHITE}Query: {test_case['query']}")
        
        try:
            # Use run_sync for synchronous execution
            result = agent.run_sync(test_case['query'], deps=supabase_client)
            print(f"{Fore.GREEN}✅ Result: {result.data}")
            success_count += 1
        except Exception as e:
            if "No customer found" in str(e) and "should fail" in test_case['description']:
                print(f"{Fore.GREEN}✅ Expected failure: {e}")
                success_count += 1
            else:
                print(f"{Fore.RED}❌ Error: {e}")
    
    print(f"\n{Fore.CYAN}=" * 50)
    print(f"{Fore.CYAN}Test Results: {success_count}/{len(test_cases)} tests passed")
    
    if success_count == len(test_cases):
        print(f"{Fore.GREEN}🎉 All tests passed! The DB Agent is working correctly.")
        return True
    else:
        print(f"{Fore.RED}⚠️  Some tests failed. Please check the configuration.")
        return False


if __name__ == "__main__":
    test_agent_operations()
