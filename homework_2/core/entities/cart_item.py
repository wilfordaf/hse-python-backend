from pydantic import BaseModel, ConfigDict


class CartItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    quantity: int
    available: bool
