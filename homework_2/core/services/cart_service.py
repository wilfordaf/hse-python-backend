from typing import Optional

from homework_2.core.entities import Cart
from homework_2.core.repositories import ICartRepository, IItemRepository
from homework_2.core.services.interfaces import ICartService


class CartService(ICartService):
    def __init__(self, cart_repository: ICartRepository, item_repository: IItemRepository):
        self._cart_repository = cart_repository
        self._item_repository = item_repository

    async def create_cart(self) -> int:
        return await self._cart_repository.create_cart()

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        repo_cart = await self._cart_repository.get_cart_by_id(cart_id)
        if repo_cart is None:
            raise ValueError(f"Cart with ID {cart_id} not found.")

        return repo_cart

    async def get_carts(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
    ) -> list[Cart]:
        if offset < 0:
            raise ValueError("Offset must be a non-negative integer.")

        if limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        if min_price is not None and min_price < 0:
            raise ValueError("Minimum price cannot be negative.")

        if max_price is not None and max_price < 0:
            raise ValueError("Maximum price cannot be negative.")

        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price.")

        if min_quantity is not None and min_quantity < 0:
            raise ValueError("Minimum quantity cannot be negative.")

        if max_quantity is not None and max_quantity < 0:
            raise ValueError("Maximum quantity cannot be negative.")

        if min_quantity is not None and max_quantity is not None and min_quantity > max_quantity:
            raise ValueError("Minimum quantity cannot be greater than maximum quantity.")

        return await self._cart_repository.get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)

    async def add_item_to_cart(self, cart_id: int, item_id: int, quantity: int) -> Cart:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        updated_cart = await self._cart_repository.add_item_to_cart(cart_id, item_id, quantity)
        if updated_cart is None:
            raise ValueError(f"Encountered error updating cart {cart_id} with {item_id} {quantity}.")

        return updated_cart
