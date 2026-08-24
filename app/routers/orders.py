from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.orders import (
    OrderCancelRequest,
    OrderGetRequest,
    OrderListRequest,
    OrderNewRequest,
    OrderUpdateRequest,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/new")
async def order_new(payload: OrderNewRequest, client: StarMFClient = Depends(get_client)):
    """Place purchase ("p"), redemption ("r"), or switch ("s") orders (batchable)."""
    return await client.post("order_new", payload.model_dump(exclude_none=True))


@router.post("/update")
async def order_update(payload: OrderUpdateRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("order_update", payload.model_dump(exclude_none=True))


@router.post("/list")
async def order_list(payload: OrderListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("order_list", payload.model_dump(exclude_none=True))


@router.post("/get")
async def order_get(payload: OrderGetRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("order_get", payload.model_dump(exclude_none=True))


@router.post("/cancel")
async def order_cancel(payload: OrderCancelRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("order_cancel", payload.model_dump(exclude_none=True))
