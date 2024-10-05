from homework_2.core.entities import Cart, CartItem
from homework_2.infrastructure.db.entities.cart_entity import CartEntity
from homework_2.infrastructure.db.mappers.interfaces import IMapper


class CartMapper(IMapper[Cart, CartEntity]):
    @staticmethod
    def to_domain(entity: CartEntity) -> Cart:
        cart_items = [
            CartItem(
                id=cart_item.item.id,
                name=cart_item.item.name,
                quantity=cart_item.quantity,
                available=not cart_item.item.deleted,
            )
            for cart_item in entity.items
        ]

        return Cart(id=int(entity.id), items=cart_items, price=float(entity.price))

    @staticmethod
    def to_entity(domain: Cart) -> CartEntity:
        return CartEntity(id=domain.id, price=domain.price)
