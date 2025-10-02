from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional


class Supplier(BaseModel):
    """
    Entity class representing a Supplier in the system.
    - id: optional on creation (DB auto-generates it).
    - firstname, lastname: required strings with validation.
    - type: restricted to "provider" or "consumer" or "both".
    - contract_date: datetime of the contract agreement.
    """
    id: Optional[int] = Field(default=None, description="Primary key in the database")
    firstname: str = Field(..., min_length=2, max_length=50, description="First name of the Supplier")
    lastname: str = Field(..., min_length=2, max_length=50, description="Last name of the Supplier")
    type: Literal["provider", "consumer", "both"] = Field(..., description="Role of the Supplier in the system")
    contract_date: datetime = Field(..., description="The datetime of the Supplier contract (ISO 8601)")
