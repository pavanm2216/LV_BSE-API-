from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.payment_detail import PaymentDetailGetRequest, PaymentDetailListRequest

router = APIRouter(prefix="/payment-detail", tags=["Payment Detail"])


@router.post("/get")
async def payment_detail_get(payload: PaymentDetailGetRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("get_payment_detail", payload.model_dump(exclude_none=True))


@router.post("/list")
async def payment_detail_list(payload: PaymentDetailListRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("list_payment_detail", payload.model_dump(exclude_none=True))
