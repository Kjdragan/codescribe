"""
Delete operation tool for the DB Agent.
"""
from pydantic_ai import RunContext
from supabase import Client


async def delete_customer_by_email(ctx: RunContext[Client], email: str):
    """
    Delete a customer record from their email address.
    
    Args:
        ctx: PydanticAI run context with Supabase client
        email: Customer email address to delete
        
    Returns:
        dict: Response from Supabase delete operation
    """
    response = ctx.deps.table("customers").delete().eq("email", email).execute()
    return response
