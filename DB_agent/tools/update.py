"""
Update operation tool for the DB Agent.
"""
from pydantic_ai import RunContext
from supabase import Client


async def update_customer_by_email(ctx: RunContext[Client], email: str, full_name: str, bio: str):
    """
    Update a customer record from their email address.
    
    Args:
        ctx: PydanticAI run context with Supabase client
        email: Customer email address to update
        full_name: New full name for the customer
        bio: New biography/description for the customer
        
    Returns:
        dict: Response from Supabase update operation
    """
    response = (
        ctx.deps.table("customers")
        .update({"full_name": full_name, "bio": bio})
        .eq("email", email)
        .execute()
    )
    return response
