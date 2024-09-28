from abc import ABC, abstractmethod
from typing import Optional

from homework_2.core.entities import Item
from homework_2.core.repositories.item_repository.dto import CreateItemDTO, PatchItemDTO, UpdateItemDTO


class IItemService(ABC):
    @abstractmethod
    async def create_item(self, item_dto: CreateItemDTO) -> Item:
        """
        Creates a new item in the system
        :param item_dto: information about the item to be created
        :return: created item
        """

    @abstractmethod
    async def get_item_by_id(self, item_id: int) -> Item:
        """
        Returns an item by its id
        :param item_id: id of the item to be returned, positive integer
        :return: found item
        """

    @abstractmethod
    async def get_items(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        show_deleted: bool = False,
    ) -> list[Item]:
        """
        Returns a list of items with filtering and pagination
        :param offset: _description_, defaults to 0
        :param limit: _description_, defaults to 10
        :param min_price: _description_, defaults to None
        :param max_price: _description_, defaults to None
        :param show_deleted: _description_, defaults to False
        :return: list of items with filtering and pagination
        """

    @abstractmethod
    async def update_item(self, item_id: int, update_dto: UpdateItemDTO) -> Item:
        """
        Updates an existing item in the system
        :param item_id: id of the item to be updated, positive integer
        :param update_dto: information about the item to be updated
        :return: updated item
        """

    @abstractmethod
    async def patch_item(self, item_id: int, patch_dto: PatchItemDTO) -> Item:
        """
        Updates an existing item in the system partially
        :param item_id: id of the item to be updated, positive integer
        :param patch_dto: information about the item to be updated
        :return: updated item
        """

    @abstractmethod
    async def delete_item(self, item_id: int) -> Item:
        """
        Deletes an existing item in the system
        :param item_id: id of the item to be deleted, positive integer
        :return: deleted item
        """
