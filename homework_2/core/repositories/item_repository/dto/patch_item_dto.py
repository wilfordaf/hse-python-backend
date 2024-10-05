from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PatchItemDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, gt=0)
