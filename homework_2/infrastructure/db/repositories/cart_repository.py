from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from homework_2.core.entities import Cart
from homework_2.core.repositories import ICartRepository
from homework_2.infrastructure.db.entities.cart_entity import CartEntity
from homework_2.infrastructure.db.entities.carts_items import CartsItems
from homework_2.infrastructure.db.mappers.cart_mapper import CartMapper
from homework_2.infrastructure.db.utils import async_session_maker


class CartRepository(ICartRepository):
    @staticmethod
    async def create_cart() -> int:
        async with async_session_maker() as session:
            new_cart = CartEntity(price=0.0)
            session.add(new_cart)
            await session.commit()
            await session.refresh(new_cart)

            return int(new_cart.id)

    @staticmethod
    async def get_cart_by_id(cart_id: int) -> Optional[Cart]:
        query = (
            select(CartEntity)
            .where(CartEntity.id == cart_id)
            .options(selectinload(CartEntity.items).selectinload(CartsItems.item))
        )

        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                cart = result.scalar_one()
            except NoResultFound:
                return None

        return CartMapper.to_domain(cart)

    @staticmethod
    async def get_carts(
        offset: int,
        limit: int,
        min_price: Optional[float],
        max_price: Optional[float],
        min_quantity: Optional[int],
        max_quantity: Optional[int],
    ) -> List[Cart]:
        query = (
            select(CartEntity)
            .offset(offset)
            .limit(limit)
            .options(selectinload(CartEntity.items).selectinload(CartsItems.item))
        )

        if min_price is not None:
            query = query.where(CartEntity.price >= min_price)

        if max_price is not None:
            query = query.where(CartEntity.price <= max_price)

        if min_quantity is not None or max_quantity is not None:
            subquery = (
                select(CartsItems.cart_id, func.count(CartsItems.item_id).label("total_quantity"))
                .group_by(CartsItems.cart_id)
                .subquery()
            )
            query = query.join(subquery, subquery.c.cart_id == CartEntity.id)

        if min_quantity is not None:
            query = query.where(subquery.c.total_quantity >= min_quantity)

        if max_quantity is not None:
            query = query.where(subquery.c.total_quantity <= max_quantity)

        async with async_session_maker() as session:
            result = await session.execute(query)
            carts = result.scalars().all()

        return [CartMapper.to_domain(cart) for cart in carts]

    @staticmethod
    async def add_item_to_cart(cart_id: int, item_id: int, item_price: float) -> Optional[Cart]:
        query = (
            select(CartEntity)
            .where(CartEntity.id == cart_id)
            .options(selectinload(CartEntity.items).selectinload(CartsItems.item))
        )

        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                cart = result.scalar_one()
            except NoResultFound:
                return None

            existing_item = next((ci for ci in cart.items if ci.item_id == item_id), None)

            if existing_item:
                existing_item.quantity += 1
            else:
                new_cart_item = CartsItems(cart_id=cart_id, item_id=item_id, quantity=1)
                session.add(new_cart_item)

            cart.price += item_price  # type: ignore

            await session.commit()
            await session.refresh(cart)

            updated_cart_query = (
                select(CartEntity)
                .where(CartEntity.id == cart_id)
                .options(selectinload(CartEntity.items).selectinload(CartsItems.item))
            )
            updated_cart_result = await session.execute(updated_cart_query)
            updated_cart = updated_cart_result.scalar_one()

        return CartMapper.to_domain(updated_cart)
