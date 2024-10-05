from typing import Optional

from homework_2.core.entities import Item
from homework_2.core.repositories import IItemRepository
from homework_2.core.repositories.item_repository.dto import CreateItemDTO, PatchItemDTO, UpdateItemDTO
from homework_2.core.services.interfaces import IItemService


class ItemService(IItemService):
    def __init__(self, item_repository: IItemRepository):
        self._item_repository = item_repository

    async def create_item(self, item_dto: CreateItemDTO) -> Item:
        return await self._item_repository.create_item(item_dto)

    async def get_item_by_id(self, item_id: int) -> Item:
        found_item = await self._item_repository.get_item_by_id(item_id)
        if found_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return found_item

    async def get_items(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        show_deleted: bool = False,
    ) -> list[Item]:
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

        return await self._item_repository.get_items(offset, limit, min_price, max_price, show_deleted)

    async def update_item(self, item_id: int, update_dto: UpdateItemDTO) -> Item:
        updated_item = await self._item_repository.update_item(item_id, update_dto)
        if updated_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return updated_item

    async def patch_item(self, item_id: int, patch_dto: PatchItemDTO) -> Item:
        existing_item = await self._item_repository.get_item_by_id(item_id)
        if existing_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        if existing_item.deleted:
            raise TypeError(f"Item with ID {item_id} is deleted so cannot be modified.")

        patched_item = await self._item_repository.patch_item(item_id, patch_dto)
        if patched_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return patched_item

    async def delete_item(self, item_id: int) -> Item:
        deleted_item = await self._item_repository.delete_item(item_id)
        if deleted_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return deleted_item
