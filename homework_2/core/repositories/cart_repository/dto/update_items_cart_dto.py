from pydantic import BaseModel, ConfigDict, Field


class UpdateItemsCartDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)
