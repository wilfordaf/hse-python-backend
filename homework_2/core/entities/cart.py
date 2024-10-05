from pydantic import BaseModel, ConfigDict

from homework_2.core.entities.cart_item import CartItem


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: list[CartItem]
    price: float
