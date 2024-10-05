from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import relationship

from homework_2.infrastructure.db.utils import Base


class CartEntity(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)

    items = relationship("CartsItems", back_populates="cart")
