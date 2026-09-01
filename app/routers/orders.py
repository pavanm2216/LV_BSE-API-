from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.orders import (
    OrderCancelRequest,
    OrderGetRequest,
    OrderListRequest,
    OrderNewPurchaseDematRequest,
    OrderNewPurchaseNominationRequest,
    OrderNewPurchasePanHolderRequest,
    OrderNewPurchasePhysicalRequest,
    OrderNewRedeemDematRequest,
    OrderNewRedeemPhysicalRequest,
    OrderNewSwitchDematRequest,
    OrderNewSwitchPhysicalRequest,
    OrderUpdateRequest,
)

router = APIRouter(prefix="/orders", tags=["Orders"])

BSE_ORDER_NEW = "order_new"
BSE_ORDER_UPDATE = "order_update"


# ---------------------------------------------------------------------------
# order_new — 8 dedicated sub-type endpoints
# ---------------------------------------------------------------------------

@router.post("/new/purchase-physical", response_model=Dict[str, Any],
             summary="order_new — Purchase Physical")
async def order_new_purchase_physical(
    payload: OrderNewPurchasePhysicalRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/purchase-pan-holder", response_model=Dict[str, Any],
             summary="order_new — Purchase with PAN Holder")
async def order_new_purchase_pan_holder(
    payload: OrderNewPurchasePanHolderRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/purchase-demat", response_model=Dict[str, Any],
             summary="order_new — Purchase Demat")
async def order_new_purchase_demat(
    payload: OrderNewPurchaseDematRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/purchase-nomination", response_model=Dict[str, Any],
             summary="order_new — Purchase with Nomination")
async def order_new_purchase_nomination(
    payload: OrderNewPurchaseNominationRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/redeem-physical", response_model=Dict[str, Any],
             summary="order_new — Redeem Physical")
async def order_new_redeem_physical(
    payload: OrderNewRedeemPhysicalRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/redeem-demat", response_model=Dict[str, Any],
             summary="order_new — Redeem Demat")
async def order_new_redeem_demat(
    payload: OrderNewRedeemDematRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/switch-physical", response_model=Dict[str, Any],
             summary="order_new — Switch Physical")
async def order_new_switch_physical(
    payload: OrderNewSwitchPhysicalRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/new/switch-demat", response_model=Dict[str, Any],
             summary="order_new — Switch Demat")
async def order_new_switch_demat(
    payload: OrderNewSwitchDematRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_NEW, payload.model_dump(exclude_none=True, mode="json"))


# ---------------------------------------------------------------------------
# order_update / order_list / order_get / order_cancel
# ---------------------------------------------------------------------------

@router.post("/update", response_model=Dict[str, Any],
             summary="order_update_purchase")
async def order_update(
    payload: OrderUpdateRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post(BSE_ORDER_UPDATE, payload.model_dump(exclude_none=True, mode="json"))


@router.post("/list", response_model=Dict[str, Any],
             summary="order_list")
async def order_list(
    payload: OrderListRequest,
    client: StarMFClient = Depends(get_client),
):
    data = payload.model_dump(exclude_none=True, mode="json")
    data.setdefault("filter_param", {})
    return await client.post("order_list", data)


@router.post("/get", response_model=Dict[str, Any],
             summary="order_get")
async def order_get(
    payload: OrderGetRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post("order_get", payload.model_dump(exclude_none=True, mode="json"))


@router.post("/cancel", response_model=Dict[str, Any],
             summary="order_cancel")
async def order_cancel(
    payload: OrderCancelRequest,
    client: StarMFClient = Depends(get_client),
):
    return await client.post("order_cancel", payload.model_dump(exclude_none=True, mode="json"))
