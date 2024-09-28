from pydantic import BaseModel, Field


class UpdateItemsCartDTO(BaseModel):
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)
