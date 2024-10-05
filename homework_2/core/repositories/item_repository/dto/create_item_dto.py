from pydantic import BaseModel, ConfigDict, Field


class CreateItemDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
