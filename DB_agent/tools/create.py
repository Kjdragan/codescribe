"""
Create operation tool for the DB Agent.
"""
from pydantic_ai import RunContext
from supabase import Client


async def create_customer(ctx: RunContext[Client], email: str, full_name: str, bio: str):
    """
    Create a new customer record in the database.
    
    Args:
        ctx: PydanticAI run context with Supabase client
        email: Customer email address
        full_name: Customer's full name
        bio: Customer biography/description
        
    Returns:
        dict: Response from Supabase insert operation
    """
    response = (
        ctx.deps.table("customers")
        .insert({"email": email, "full_name": full_name, "bio": bio})
        .execute()
    )
    return response
