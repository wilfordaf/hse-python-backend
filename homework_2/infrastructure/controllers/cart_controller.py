from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from homework_2.core.services.cart_service import CartService
from homework_2.infrastructure.controllers.dependencies import cart_service

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("")
async def create_cart(
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        cart_id = await cart_service.create_cart()
        return JSONResponse(
            content={"id": cart_id},
            headers={"location": f"/cart/{cart_id}"},
            status_code=201,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{id}")
async def get_cart_by_id(
    id: int,
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        found_cart = await cart_service.get_cart_by_id(id)
        return found_cart.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("")
async def get_carts(
    cart_service: Annotated[CartService, Depends(cart_service)],
    offset: int = Query(0, ge=0, description="Non-negative integer, offset for pagination."),
    limit: int = Query(10, gt=0, description="Positive integer, maximum number of carts to return."),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter."),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter."),
    min_quantity: Optional[int] = Query(None, ge=0, description="Minimum quantity filter."),
    max_quantity: Optional[int] = Query(None, ge=0, description="Maximum quantity filter."),
):
    try:
        carts = await cart_service.get_carts(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
        )
        return [cart.model_dump() for cart in carts]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{cart_id}/add/{item_id}")
async def add_item_to_cart(
    cart_id: int,
    item_id: int,
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        updated_cart = await cart_service.add_item_to_cart(cart_id, item_id)
        return updated_cart.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
