from pydantic import BaseModel, Field


class UpdateItemDTO(BaseModel):
    name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
