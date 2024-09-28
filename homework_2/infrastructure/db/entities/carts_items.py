from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from homework_2.infrastructure.db.utils import Base


class CartsItems(Base):
    __tablename__ = "carts_items"

    cart_id = Column(Integer, ForeignKey("carts.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    cart = relationship("CartEntity", back_populates="items")
    item = relationship("ItemEntity", back_populates="carts")
