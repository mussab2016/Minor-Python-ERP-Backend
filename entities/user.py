from pydantic import BaseModel, Field


class User(BaseModel):  # BaseModel provie functions like  __init__, __repr__, __eq__,
    """
    Entity class representing a User in the system.
    - id: optional on creation (DB auto-generates it).
    - name, username: required with length validation.
    - password & salt: stored hashed, never plain text.
    - rank: role indicator (0=user, 1=admin, up to 10).
    """
    id: int | None = Field(default=None, description="Primary key in the database")
    name: str = Field(..., min_length=2, max_length=50, description="Full name of the user") # ... → means required field.
    username: str = Field(..., min_length=3, max_length=30, description="Unique username")
    # salt: str = Field(..., min_length=6, description="Password salt (hashed)") # NOT NEEDED BECAUSE OF BCRYPT FUNCTION
    password: str = Field(..., min_length=6, description="Hashed password, never plain text")
    rank: int = Field(default=0, ge=0, le=3, description="0=user, 1=admin, max=3")

