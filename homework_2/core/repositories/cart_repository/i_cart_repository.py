from abc import ABC, abstractmethod
from typing import List, Optional

from homework_2.core.entities import Cart


class ICartRepository(ABC):
    @staticmethod
    @abstractmethod
    async def create_cart(self) -> int:
        """
        Create a new cart and return the cart ID.
        """

    @staticmethod
    @abstractmethod
    async def get_cart_by_id(self, cart_id: int) -> Optional[Cart]:
        """
        Retrieve a cart by its ID.
        """

    @staticmethod
    @abstractmethod
    async def get_carts(
        self,
        offset,
        limit,
        min_price: Optional[float],
        max_price: Optional[float],
        min_quantity: Optional[int],
        max_quantity: Optional[int],
    ) -> List[Cart]:
        """
        Retrieve a list of carts, with optional filters and pagination.
        """

    @staticmethod
    @abstractmethod
    async def add_item_to_cart(self, cart_id: int, item_id: int, quantity: int) -> Optional[Cart]:
        """
        Add an item to the cart with a specified quantity. If the item already exists in the cart,
        its quantity is increased. Returns the updated cart data.
        """
