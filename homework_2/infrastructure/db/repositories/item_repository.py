from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from homework_2.core.entities import Item
from homework_2.core.repositories import IItemRepository
from homework_2.core.repositories.item_repository.dto import CreateItemDTO, PatchItemDTO, UpdateItemDTO
from homework_2.infrastructure.db.entities.item_entity import ItemEntity
from homework_2.infrastructure.db.utils import async_session_maker


class ItemRepository(IItemRepository):
    @staticmethod
    async def create_item(item: CreateItemDTO) -> Item:
        new_item = ItemEntity(name=item.name, price=item.price, deleted=False)

        async with async_session_maker() as session:
            session.add(new_item)

            await session.commit()
            await session.refresh(new_item)

        return Item.model_validate(new_item)

    @staticmethod
    async def get_item_by_id(item_id: int) -> Optional[Item]:
        query = select(ItemEntity).where(ItemEntity.id == item_id)
        async with async_session_maker() as session:
            result = await session.execute(query)

        try:
            item = result.scalar_one()
            return Item.model_validate(item)
        except NoResultFound:
            return None

    @staticmethod
    async def get_items(
        offset: int,
        limit: int,
        min_price: Optional[float],
        max_price: Optional[float],
        show_deleted: bool,
    ) -> List[Item]:
        query = select(ItemEntity).offset(offset).limit(limit)

        if not show_deleted:
            query = query.where(ItemEntity.deleted.is_(False))

        if min_price is not None:
            query = query.where(ItemEntity.price >= min_price)

        if max_price is not None:
            query = query.where(ItemEntity.price <= max_price)

        async with async_session_maker() as session:
            result = await session.execute(query)

        items = result.scalars().all()

        return [Item.model_validate(item) for item in items]

    @staticmethod
    async def update_item(item_id: int, update_dto: UpdateItemDTO) -> Optional[Item]:
        query = select(ItemEntity).where(ItemEntity.id == item_id)
        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                item = result.scalar_one()
                item.name = update_dto.name  # type: ignore
                item.price = update_dto.price  # type: ignore

                await session.commit()
                await session.refresh(item)

                return Item.model_validate(item)
            except NoResultFound:
                return None

    @staticmethod
    async def patch_item(item_id: int, patch_dto: PatchItemDTO) -> Optional[Item]:
        query = select(ItemEntity).where(ItemEntity.id == item_id)
        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                item = result.scalar_one()

                if patch_dto.name is not None:
                    item.name = patch_dto.name  # type: ignore

                if patch_dto.price is not None:
                    item.price = patch_dto.price  # type: ignore

                await session.commit()
                await session.refresh(item)

                return Item.model_validate(item)
            except NoResultFound:
                return None

    @staticmethod
    async def delete_item(item_id: int) -> Optional[Item]:
        query = select(ItemEntity).where(ItemEntity.id == item_id)
        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                item = result.scalar_one()
                item.deleted = True  # type: ignore

                await session.commit()
                await session.refresh(item)

                return Item.model_validate(item)
            except NoResultFound:
                return None
