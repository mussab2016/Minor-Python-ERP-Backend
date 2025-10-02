from pydantic import BaseModel, Field


class Stock(BaseModel):
    """
    Entity class representing a Stock in the system.
    - id: optional on creation (DB auto-generates it).
    - name: required name of the stock.
    - city, address: required location details.
    - center_id: foreign key linking this stock to a Center.
    """
    id: int | None = Field(default=None, description="Primary key in the database")
    name: str = Field(..., min_length=2, max_length=100, description="Stock name")
    city: str = Field(..., min_length=2, max_length=50, description="Stock city")
    address: str = Field(..., max_length=255, description="Stock address")
    center_id: int = Field(..., ge=1, description="ID of the Center this stock belongs to")
