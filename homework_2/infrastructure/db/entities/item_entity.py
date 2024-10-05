from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from homework_2.infrastructure.db.utils import Base


class ItemEntity(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    carts = relationship("CartsItems", back_populates="item")
