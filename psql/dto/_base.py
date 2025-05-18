from datetime import datetime

from pydantic import BaseModel


class _BaseDTO(BaseModel):
    id: int
    created_at: datetime
