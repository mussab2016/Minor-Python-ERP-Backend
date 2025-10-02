from typing import Generic, TypeVar
from pydantic import BaseModel  
T = TypeVar("T")


class HttpListResponse(BaseModel, Generic[T]):
    total: int
    body: list[T]

    @staticmethod
    def from_data(items: list[T], total: int) -> "HttpListResponse[T]":
        return HttpListResponse(total=total, body=items)
