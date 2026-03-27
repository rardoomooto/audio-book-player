from typing import Optional
from pydantic import BaseModel


class Limit(BaseModel):
    id: int
    user_id: Optional[int] = None
    duration_minutes: int


class GlobalLimit(BaseModel):
    duration_minutes: int
