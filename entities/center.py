from pydantic import BaseModel, Field


class Center(BaseModel):
    """
    Entity class representing a Center in the system.
    - id: optional on creation (DB auto-generates it).
    - name: required name of the center.
    - city, address: required location details.
    - phone/email: optional contact details.
    """
    id: int | None = Field(default=None, description="Primary key in the database")
    name: str = Field(..., min_length=2, max_length=100, description="Center name")
    city: str = Field(..., min_length=2, max_length=50, description="Center city")
    address: str = Field(..., max_length=255, description="Center address")
    phone: str | None = Field(None, max_length=20, description="Optional phone number")
    email: str | None = Field(None, max_length=100, description="Optional email address")
