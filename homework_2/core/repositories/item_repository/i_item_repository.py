from abc import ABC, abstractmethod
from typing import List, Optional

from homework_2.core.entities import Item
from homework_2.core.repositories.item_repository.dto.create_item_dto import CreateItemDTO
from homework_2.core.repositories.item_repository.dto.patch_item_dto import PatchItemDTO
from homework_2.core.repositories.item_repository.dto.update_item_dto import UpdateItemDTO


class IItemRepository(ABC):
    @staticmethod
    @abstractmethod
    async def create_item(item: CreateItemDTO) -> Item:
        """Create a new item"""

    @staticmethod
    @abstractmethod
    async def get_item_by_id(item_id: int) -> Optional[Item]:
        """Retrieve an item by its ID"""

    @staticmethod
    @abstractmethod
    async def get_items(
        offset: int,
        limit: int,
        min_price: Optional[float],
        max_price: Optional[float],
        show_deleted: bool,
    ) -> List[Item]:
        """Retrieve a list of items, with optional filters and pagination"""

    @staticmethod
    @abstractmethod
    async def update_item(item_id: int, item: UpdateItemDTO) -> Optional[Item]:
        """Replace an item with new data"""

    @staticmethod
    @abstractmethod
    async def patch_item(item_id: int, item: PatchItemDTO) -> Optional[Item]:
        """Partially update an item"""

    @staticmethod
    @abstractmethod
    async def delete_item(item_id: int) -> Optional[Item]:
        """Mark an item as deleted"""
