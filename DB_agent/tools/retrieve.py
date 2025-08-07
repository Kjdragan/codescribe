"""
Retrieve operation tool for the DB Agent.
"""
from pydantic_ai import RunContext
from supabase import Client


async def get_customer_by_email(ctx: RunContext[Client], email: str):
    """
    Retrieve a customer record by their email address.
    
    Args:
        ctx: PydanticAI run context with Supabase client
        email: Customer email address to search for
        
    Returns:
        dict: Response from Supabase select operation
    """
    response = (
        ctx.deps.table("customers")
        .select("*")
        .eq("email", email)
        .execute()
    )
    return response
