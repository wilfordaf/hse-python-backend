from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    deleted: bool
