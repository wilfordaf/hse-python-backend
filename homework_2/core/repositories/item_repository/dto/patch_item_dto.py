from typing import Optional

from pydantic import BaseModel, Field


class PatchItemDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, gt=0)
