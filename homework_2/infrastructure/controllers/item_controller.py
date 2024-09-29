from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from homework_2.core.repositories.item_repository.dto import CreateItemDTO, PatchItemDTO, UpdateItemDTO
from homework_2.core.services.item_service import ItemService
from homework_2.infrastructure.controllers.dependencies import item_service

router = APIRouter(
    prefix="/item",
    tags=["Item"],
)


@router.post("")
async def add_item(
    item: CreateItemDTO,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    created_item = await item_service.create_item(item)
    return JSONResponse(content=created_item.model_dump(), status_code=201)


@router.get("/{id}")
async def get_item_by_id(
    id: int,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    try:
        found_item = await item_service.get_item_by_id(id)
        return found_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("")
async def get_items(
    item_service: Annotated[ItemService, Depends(item_service)],
    offset: int = Query(0, ge=0, description="Non-negative integer, offset for pagination."),
    limit: int = Query(10, gt=0, description="Positive integer, maximum number of items to return."),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter."),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter."),
    show_deleted: bool = Query(False, description="Whether to include deleted items."),
):
    try:
        items = await item_service.get_items(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            show_deleted=show_deleted,
        )
        return [item.model_dump() for item in items]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/{id}")
async def update_item(
    id: int,
    update_dto: UpdateItemDTO,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    try:
        updated_item = await item_service.update_item(id, update_dto)
        return updated_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch("/{id}")
async def patch_item(
    id: int,
    patch_dto: PatchItemDTO,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    try:
        patched_item = await item_service.patch_item(id, patch_dto)
        return patched_item.model_dump()
    except TypeError as e:
        raise HTTPException(status_code=304, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/{id}")
async def delete_item(
    id: int,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    try:
        deleted_item = await item_service.delete_item(id)
        return deleted_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
