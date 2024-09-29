from homework_2.core.services import CartService, ItemService
from homework_2.infrastructure.db.repositories import CartRepository, ItemRepository


def item_service():
    return ItemService(ItemRepository)


def cart_service():
    return CartService(CartRepository, ItemRepository)
