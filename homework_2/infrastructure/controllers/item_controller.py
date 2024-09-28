from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from homework_2.core.repositories.item_repository.dto import CreateItemDTO
from homework_2.core.services.item_service import ItemService
from homework_2.infrastructure.controllers.dependencies import item_service

router = APIRouter(
    prefix="/item",
    tags=["Item"],
)


@router.post("")
async def add_task(
    item: CreateItemDTO,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    created_item = await item_service.create_item(item)
    return created_item.model_dump()


@router.get("/{item_id}")
async def get_task_by_id(
    item_id: int,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    try:
        found_item = await item_service.get_item_by_id(item_id)
        return found_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
