"""
Pydantic data models for the DB Agent project.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer data model for the database agent."""
    id: Optional[str] = None
    email: str = ""
    full_name: str = ""
    bio: str = ""
