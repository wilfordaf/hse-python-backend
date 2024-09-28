from abc import ABC, abstractmethod
from typing import Optional

from homework_2.core.entities import Cart


class ICartService(ABC):
    @abstractmethod
    async def create_cart(self) -> int:
        """
        Creates a new cart
        """

    @abstractmethod
    async def get_cart_by_id(self, cart_id: int) -> Cart:
        """
        Returns cart by id
        """

    @abstractmethod
    async def get_carts(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
    ) -> list[Cart]:
        """
        Returns all carts with given filters
        """

    @abstractmethod
    async def add_item_to_cart(self, cart_id: int, item_id: int, quantity: int) -> Cart:
        """
        Adds a quantity of items to the cart with given id
        """
