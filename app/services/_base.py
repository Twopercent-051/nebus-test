from typing import TypeVar, Generic
from pydantic import BaseModel


_T = TypeVar("_T")


class ServiceResponse(BaseModel, Generic[_T]):
    data: _T | None = None
    error: str | None = None
    status_code: int = 200
