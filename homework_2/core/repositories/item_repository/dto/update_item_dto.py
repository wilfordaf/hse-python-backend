from pydantic import BaseModel, ConfigDict, Field


class UpdateItemDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
