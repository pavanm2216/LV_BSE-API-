from fastapi import APIRouter, Depends

from app.clients.starmf_client import StarMFClient
from app.dependencies import get_client
from app.schemas.payment_gateway import (
    PaymentGatewayServiceRequest,
    PaymentGatewayStatusRequest,
    SendPaymentInfoRequest,
)

router = APIRouter(prefix="/payment-gateway", tags=["Payment Gateway"])


@router.post("/exchpg-service")
async def exchpg_service(payload: PaymentGatewayServiceRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("get_exchpg_service", payload.model_dump(exclude_none=True))


@router.post("/send-payment-info")
async def send_payment_info(payload: SendPaymentInfoRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("send_payment_info", payload.model_dump(exclude_none=True))


@router.post("/status")
async def payment_status(payload: PaymentGatewayStatusRequest, client: StarMFClient = Depends(get_client)):
    return await client.post("get_bse_pg_payment_status", payload.model_dump(exclude_none=True))
