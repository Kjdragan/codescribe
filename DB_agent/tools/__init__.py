"""
CRUD operation tools for the DB Agent.
"""
from .create import create_customer
from .retrieve import get_customer_by_email
from .update import update_customer_by_email
from .delete import delete_customer_by_email

__all__ = [
    "create_customer",
    "get_customer_by_email", 
    "update_customer_by_email",
    "delete_customer_by_email"
]
